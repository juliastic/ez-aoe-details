import os
import math
import csv
import time
import typing
from pathlib import Path
from mgz import header, fast
from datetime import datetime
from player import Player
from units import Filter, MainType, SkillLevel, FilterType, TECHNOLOGY_IDS, UNIT_IDS
from mgz.summary.objects import TC_IDS
from visualisation import AoELineGraph

class Analysis():
    def __init__(self, replayfile: str):
        self.replayfile = replayfile
        self.time = 0
        self.players = {}
        self.summary_players = []
        self.added_timestamps = []
        self.map_dimensions = 0
    
    def output_time(self) -> str:
        seconds = math.floor((self.time / 1000) % 60)
        minutes = math.floor((self.time / (1000 * 60)))
        return str(minutes).zfill(2) + ':' + str(seconds).zfill(2)

    def find_player(self, player_id: int) -> Player:
        return self.players[player_id]

    def start_analysis(self) -> None:
        # consider retrieving starting position of player and calculate something????
        start = time.time()
        print("Parsing Data ...")
        with open(self.replayfile, 'rb') as data:
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
            #todo: track scouting? maybe track activity on map for the entire game? save with move????
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
                    elif action == fast.Action.BUILD:
                        player_id = details['player_id']
                        building_id = details['building_id']
                        player = self.get_and_prepare_player(player_id, details)
                        if building_id in TC_IDS and player.get_starting_position() == (0, 0):
                            player.set_starting_position((details['x'], details['y']))
                        player.add_building(building_id)
                    elif action == fast.Action.GATHER_POINT:
                        pass #maybe add this?
                    elif action == fast.Action.RESIGN:
                        pass
                    elif action == fast.Action.TOWN_BELL or action == fast.Action.PATROL or action == fast.Action.FORMATION or action == fast.Action.DE_ATTACK_MOVE or action == fast.Action.MOVE:
                        self.get_and_prepare_player(player_id, details)
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

    def get_and_prepare_player(self, player_id: int, details: typing.Dict[str, any]) -> Player:
        player = self.find_player(player_id)
        player.increase_eAPM()
        if 'x' in details and 'y' in details:
            # calculate with starting position of player -> differrence -> final result: relative to map size -> %
            player.add_action({'x': details['x'], 'y': details['y']})
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
            for _, entry in entries.items():
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
        self.average_results = {FilterType.EAPM: {}, FilterType.TECHNOLOGIES: {k: {MainType.ECO: {}, MainType.MIL: {}} for k in self.analyses}, FilterType.GAMEDURATION: {}, FilterType.ACTION_COORDINATES: {k: {'x': 0, 'y': 0} for k in self.analyses}}

    def start_analyses(self) -> None:
        [analysis.start_analysis() for analysis in self.combined_analyses]
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
        values_for_timestamps_type_avg = self.average_timestamp_results[type]
        total_eAPM = 0
        average_action_coordinates = self.average_results[FilterType.ACTION_COORDINATES][type]
        average_technologies = self.average_results[FilterType.TECHNOLOGIES][type]
        for player in players:
            total_eAPM += player.get_average_eAPM()
            for timestamp, values in player.get_state_for_timestamps().items():
                values_for_timestamp = values_for_timestamps_type_avg.setdefault(timestamp, {
                    FilterType.UNITS: {MainType.ECO: 0, MainType.MIL: 0}, 
                    FilterType.BUILDINGS: {MainType.ECO: 0, MainType.MIL: 0}, 
                    'count': 0})
                for key, value in values.items():
                    values_for_timestamp[key][MainType.ECO] += value[MainType.ECO]
                    values_for_timestamp[key][MainType.MIL] += value[MainType.MIL]
                values_for_timestamp['count'] += 1
            for main_type, technologies in player.get_technologies().items():
                average_technologies_for_type = average_technologies[main_type]
                for technology, timestamp in technologies.items():
                    average_technology = average_technologies_for_type.setdefault(technology, {'timestamp': 0, 'count': 0})
                    average_technology['timestamp'] += timestamp
                    average_technology['count'] += 1
            action_coordinates = player.get_average_action_coordinates()
            average_action_coordinates['x'] += action_coordinates[0]
            average_action_coordinates['y'] += action_coordinates[1]

        average_action_coordinates['x'] /= len(players)
        average_action_coordinates['y'] /= len(players)

        self.average_results[FilterType.EAPM][type] = total_eAPM / len(players)

        for main_type, technologies in average_technologies.items():
            for technology, values in technologies.items():
                average_technologies[main_type][technology] = values['timestamp'] / values['count']

        for timestamp, results in values_for_timestamps_type_avg.items():
            count = results['count']
            for key, value in results.items():
                if isinstance(value, dict):
                    value[MainType.ECO] = value[MainType.ECO] / count
                    value[MainType.MIL] = value[MainType.MIL] / count
            results.pop('count', None)

    def output_results(self) -> None:
        visualisation = AoELineGraph(self.average_timestamp_results, self.average_results)
        visualisation.output_results()

    def create_analyses_report(self) -> None:
        [analysis.create_analysis_report() for analysis in self.combined_analyses]

if __name__ == '__main__':
    base_path = Path(__file__).parent
    file_path = str((base_path / 'replays').resolve())
    analyses = MultipleAnalyses({SkillLevel.PRO: file_path + '/pro', SkillLevel.HIGH: file_path + '/high', SkillLevel.MIDDLE: file_path + '/middle', SkillLevel.LOW: file_path + '/low'})
    analyses.start_analyses()
    analyses.output_results()
    analyses.create_analyses_report()
