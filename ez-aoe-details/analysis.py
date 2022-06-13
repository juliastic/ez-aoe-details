import os
import math
import csv
import time
import typing
from pathlib import Path
from mgz import header, fast
from mgz.summary.objects import TC_IDS
from datetime import datetime
from player import Player
from units import MainType, SkillLevel, FilterType, TECHNOLOGY_IDS, UNIT_IDS, BuildingType
from visualisation import AoEGraphs

class Analysis():
    """This class holds all the relevant information for a specific replay. It also contains instances of player.Player to hold player specific information. It relies on mgz.fast for parsing the replay file data.
    """
    def __init__(self, replayfile: str):
        self.replayfile = replayfile
        self.time = 0
        self.players = {}
        self.summary_players = []
        self.added_timestamps = []
        self.map_dimensions = 0

    def find_player(self, player_id: int) -> Player:
        """Finds a player given a specific id

        Args:
            player_id (int): player id

        Returns:
            Player: the player object associated with the player id
        """
        return self.players[player_id]

    def start_analysis(self) -> None:
        """This function invokes the analysis of the given replay data. The game data is iterated over and parsed accordingly.
        """
        start = time.time()
        print("Parsing Data ...")
        with open(self.replayfile, 'rb') as data:
            # parse game metadata
            eof = os.fstat(data.fileno()).st_size
            _header = header.parse_stream(data)
            self.map_dimensions = _header.map_info.size_x # map size
            for player in _header.initial.players:
                player_id = 0
                for obj in player.objects:
                    if player_id != obj.player_id:
                        player_id = obj.player_id
                    if obj.object_type in TC_IDS:
                        self.players[player_id] = Player(player_id, (obj.x, obj.y))
                if player_id not in self.players and player_id > 0: # in case of nomad: starting position will be set later
                    self.players[player_id] = Player(player_id)
            fast.meta(data)

            # parse game data
            while data.tell() < eof:
                operation = fast.operation(data)
                if operation[0] == fast.Operation.ACTION:
                    action = operation[1][0]
                    details = operation[1][1]
                    if action == fast.Action.DE_QUEUE:
                        player_id = details['player_id']
                        unit_id = details['unit_id']
                        self.get_and_prepare_player(player_id, details).add_unit(unit_id)
                    elif action == fast.Action.RESEARCH:
                        player_id = details['player_id']
                        technology_id = details['technology_id']
                        seconds = math.floor((self.time / 1000))
                        self.get_and_prepare_player(player_id, details).add_technology(technology_id, seconds)
                    elif action == fast.Action.BUILD or action == fast.Action.WALL:
                        player_id = details['player_id']
                        building_id = details['building_id']
                        player = self.get_and_prepare_player(player_id, details)
                        if building_id in TC_IDS and player.get_starting_position() == (0, 0):
                            player.set_starting_position((details['x'], details['y']))
                        player.add_building(building_id)
                    elif action == fast.Action.TOWN_BELL or action == fast.Action.PATROL or action == fast.Action.FORMATION or action == fast.Action.DE_ATTACK_MOVE or action == fast.Action.MOVE or action == fast.Action.ATTACK_GROUND:
                        self.get_and_prepare_player(player_id, details, action)
                elif operation[0] == fast.Operation.SYNC:
                    self.time += operation[1][0]
                    minutes = math.floor((self.time / (1000 * 60)))
                    if minutes not in self.added_timestamps and minutes % 2 == 0:
                        seconds = minutes * 60
                        self.added_timestamps.append(minutes)
                        [player.calculate_state_for_timestamp(seconds) for _, player in self.players.items()]

            minutes = math.ceil((self.time / (1000 * 60)))
            [player.set_gameduration(minutes) for player in self.players.values()]

            print(f'Parsed file {self.replayfile} in {time.time() - start} seconds')

    def get_and_prepare_player(self, player_id: int, details: typing.Dict[str, any], action: fast.Action = -1) -> Player:
        player = self.find_player(player_id)
        player.increase_eAPM()
        if 'x' in details and 'y' in details:
            # calculate with starting position of player -> differrence -> final result: relative to map size -> %
            player.add_action({'x': details['x'], 'y': details['y'], 'timestamp': self.get_gameduration() * 60, 'action': action})
        return player

    def get_players(self) -> typing.Dict[int, Player]:
        return self.players
    
    def get_map_dimensions(self) -> int:
        return self.map_dimensions

    def get_gameduration(self) -> int:
        return math.ceil((self.time / (1000 * 60)))

    def create_header_with_types(self, list: list) -> list[str]:
        header = ['player']
        for key, entries in list.items():
            header.append(key)
            for entry in entries.values():
                header.append(entry)
        return header

    def create_analysis_report(self) -> None:
        header_units = self.create_header_with_types(UNIT_IDS)
        header_technologies = self.create_header_with_types(TECHNOLOGY_IDS)
        header_unit_timestamps = ['timestamp']
        rows_units = []
        rows_technologies = []
        player_state = {}
        timestamps = []
        for player_id, player in self.players.items():
            header_unit_timestamps.append(f'player{player_id}')
            if len(timestamps) == 0:
                [timestamps.append(timestamp) for timestamp in player.get_state_for_timestamps().keys()]

            row_units = {'player': player_id}
            self.fetch_player_data(player.get_units(), row_units)
            rows_units.append(row_units)

            row_technologies = {'player': player_id}
            self.fetch_player_data(player.get_technologies(), row_technologies)
            rows_technologies.append(row_technologies)

            player_state[player_id] = player.get_state_for_timestamps()
        
        rows_unit_timestamps = {MainType.MIL: [], MainType.ECO: []}
        for timestamp in timestamps:
            row_unit_timestamps = {MainType.MIL : [timestamp], MainType.ECO: [timestamp]}
            for player_id, player in player_state.items():
                units = player_state[player_id][timestamp][FilterType.UNITS]
                row_unit_timestamps[MainType.MIL].append(units[MainType.MIL])
                row_unit_timestamps[MainType.ECO].append(units[MainType.ECO])
            rows_unit_timestamps[MainType.MIL].append(row_unit_timestamps[MainType.MIL])
            rows_unit_timestamps[MainType.ECO].append(row_unit_timestamps[MainType.ECO])

        folder_timestamp = datetime.now().strftime('%Y-%m-%d_%H_%M')

        base_path = Path(__file__).parent
        general_path = str((base_path / 'output').resolve())
        replayfile_name = os.path.basename(self.replayfile)
        file_path = general_path + f'/{folder_timestamp}/{replayfile_name}'
        os.makedirs(file_path, exist_ok=True)

        self.create_csv_file(str(file_path) + '/units.csv', header_units, rows_units)
        self.create_csv_file(str(file_path) + '/technologies.csv', header_technologies, rows_technologies)
        self.create_csv_file(str(file_path) + '/mil_unit_timestamps.csv', header_unit_timestamps, rows_unit_timestamps[MainType.MIL], False)
        self.create_csv_file(str(file_path) + '/vil_unit_timestamps.csv', header_unit_timestamps, rows_unit_timestamps[MainType.ECO], False)

    def fetch_player_data(self, data: typing.Dict[MainType, typing.Dict[str, int]], row: typing.Dict[str, any]) -> None:
        for key, entries in data.items():
            row[key] = '/'
            for entry, value in entries.items():
                row[entry] = value

    def create_csv_file(self, filename, header: list[str], rows: list[str], use_dict_writer=True) -> None:
        with open(filename, 'w', encoding='UTF8', newline='') as file:
            if use_dict_writer:
                writer = csv.DictWriter(file, fieldnames=header,restval=0)
                writer.writeheader()
            else:
                writer = csv.writer(file)
                writer.writerow(header)
            writer.writerows(rows)
class MultipleAnalyses():
    """This class contains all Analysis instances for a specific SkillLevel. Additionally, it relies on visualisation.AoEGraphs to visualise the results, as well as on helper classes from units.* to not rely on hardcoded values.
    """
    def __init__(self, paths_to_segmented_replayfiles: typing.Dict[SkillLevel, str]):
        self.analyses = {k: [] for k in paths_to_segmented_replayfiles}

        for type, path in paths_to_segmented_replayfiles.items():
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_file():
                        analysis = Analysis(f'{path}/{entry.name}')
                        self.analyses[type].append(analysis)
        self.combined_analyses = []
        [self.combined_analyses.extend(analysis_list) for analysis_list in self.analyses.values()]

        self.results = {k: [] for k in self.analyses}
        self.average_timestamp_results = {k: {} for k in self.analyses}
        self.average_results = {FilterType.EAPM: {}, FilterType.TECHNOLOGIES: {k: {MainType.ECO: {}, MainType.MIL: {}} for k in self.analyses}, FilterType.GAMEDURATION: {}, FilterType.ACTION_UNIT_COORDINATES: {k: {'x': 0, 'y': 0} for k in self.analyses}, FilterType.ACTION_MOVE_COORDINATES: {k: {'x': 0, 'y': 0} for k in self.analyses}}

    def start_analyses(self) -> None:
        """Starts all game analyses, also invokes compute_average_results()
        """
        [analysis.start_analysis() for analysis in self.combined_analyses]
        # calculate average game duration for skill level
        for type, analyses_for_type in self.analyses.items():
            total_gameduration = 0
            for analysis in analyses_for_type:
                total_gameduration += analysis.get_gameduration()
                self.results[type].extend([player for player in analysis.get_players().values()])
            average_gameduration = math.ceil(total_gameduration / len(analyses_for_type))
            self.average_results['gameduration'][type] = average_gameduration
            print(f'Average Game Duration for Skill Level {type}: {average_gameduration} min')
        self.compute_average_results()
    
    def compute_average_results(self) -> None:
        [self.compute_average_results_for_type(type, players) for type, players in self.results.items()]

    def compute_average_results_for_type(self, type: str, players: list[Player]) -> None:
        """Computes the average results for all players of a certain type

        Args:
            type (str): skill level type
            players (list[Player]): list holding all players
        """
        values_for_timestamps_type_avg = self.average_timestamp_results[type]
        total_eAPM = 0
        average_action_move_coordinates = self.average_results[FilterType.ACTION_MOVE_COORDINATES][type]
        average_action_unit_coordinates = self.average_results[FilterType.ACTION_UNIT_COORDINATES][type]
        average_technologies = self.average_results[FilterType.TECHNOLOGIES][type]
        for player in players:
            total_eAPM += player.get_average_eAPM()
            # calculate average units and buildings for timestamps
            for timestamp, values in player.get_state_for_timestamps().items():
                values_for_timestamp = values_for_timestamps_type_avg.setdefault(timestamp, {
                    FilterType.UNITS: {MainType.ECO: 0, MainType.MIL: 0}, 
                    FilterType.BUILDINGS: {MainType.ECO: 0, MainType.MIL: 0, BuildingType.WALL: 0},
                    FilterType.ACTION_MOVE_COORDINATES: {'x': 0, 'y': 0, 'count': 0},
                    FilterType.ACTION_UNIT_COORDINATES: {'x': 0, 'y': 0, 'count': 0},
                    'count': 0})
                for key, value in values.items():
                    for value_key in value.keys():
                        values_for_timestamp[key][value_key] += value[value_key]
                values_for_timestamp['count'] += 1
            # calculate average technology research time
            for main_type, technologies in player.get_technologies().items():
                average_technologies_for_type = average_technologies[main_type]
                for technology, timestamp in technologies.items():
                    average_technology = average_technologies_for_type.setdefault(technology, {'timestamp': 0, 'count': 0})
                    average_technology['timestamp'] += timestamp
                    average_technology['count'] += 1
            # add coordinates
            action_coordinates = player.get_average_move_action_coordinates()
            average_action_move_coordinates['x'] += action_coordinates[0]
            average_action_move_coordinates['y'] += action_coordinates[1]

            action_unit_coordinates = player.get_average_unit_coordinates()
            average_action_unit_coordinates['x'] += action_unit_coordinates[0]
            average_action_unit_coordinates['y'] += action_unit_coordinates[1]

        # average coordinate and eAPM values based on player count
        player_count = len(players)
        average_action_move_coordinates['x'] /= player_count
        average_action_move_coordinates['y'] /= player_count

        average_action_unit_coordinates['x'] /= player_count
        average_action_unit_coordinates['y'] /= player_count

        self.average_results[FilterType.EAPM][type] = total_eAPM / player_count

        # average technology, military and eco values based on frequency of timestamp 
        for main_type, technologies in average_technologies.items():
            for technology, values in technologies.items():
                average_technologies[main_type][technology] = values['timestamp'] / values['count']
        for timestamp, results in values_for_timestamps_type_avg.items():
            count = results['count']
            for value in results.values():
                if isinstance(value, dict):
                    if MainType.ECO in value:
                        for key in value.keys():
                            value[key] /= count
                    elif 'x' in value:
                        value['x'] /= count
                        value['y'] /= count
            results.pop('count', None)

    def output_results(self) -> None:
        """This invokes an visualisation.AoEGraphs instance to visualise the analaysis results.
        """
        visualisation = AoEGraphs(self.average_timestamp_results, self.average_results)
        visualisation.output_results()

    def create_analyses_report(self) -> None:
        """This invokes Analysis.create_analysis_report() for all stored analysis isntances
        """
        [analysis.create_analysis_report() for analysis in self.combined_analyses]

if __name__ == '__main__':
    base_path = Path(__file__).parent
    file_path = str((base_path / 'replays').resolve())
    analyses = MultipleAnalyses({SkillLevel.PRO: file_path + '/pro', SkillLevel.HIGH: file_path + '/high', SkillLevel.MIDDLE: file_path + '/middle', SkillLevel.LOW: file_path + '/low'})
    analyses.start_analyses()
    analyses.output_results()
    analyses.create_analyses_report()
