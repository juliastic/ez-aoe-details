import os
import math
import csv
from mgz import header, fast
from datetime import datetime
from player import Player
from units import Unit, MainType, Technology, TECHNOLOGY_IDS, UNIT_IDS, BUILDING_IDS

class Analysis():
    def __init__(self, replayfile):
        self.replayfile = replayfile
        self.time = 0
        self.players = {}
        self.added_timestamps = []
    
    def output_time(self):
        seconds = math.floor((self.time / 1000) % 60)
        minutes = math.floor((self.time / (1000 * 60)))
        return str(minutes).zfill(2) + ':' + str(seconds).zfill(2)

    def find_player(self, player_id):
        if player_id not in self.players:
            self.players[player_id] = Player(player_id)
        return self.players[player_id]

    def start_analysis(self):
        with open(self.replayfile, 'rb') as data:
            eof = os.fstat(data.fileno()).st_size
            header.parse_stream(data)
            fast.meta(data)
            while data.tell() < eof:
                #TODO: calculate idle time of tc
                operation = fast.operation(data)
                if operation[0] == fast.Operation.ACTION:
                    action = operation[1][0]
                    details = operation[1][1]
                    if action == fast.Action.DE_QUEUE:
                        player_id = details['player_id']
                        unit_id = details['unit_id']
                        # print(operation)
                        self.find_player(player_id).add_unit(unit_id)
                    elif action == fast.Action.DE_ATTACK_MOVE:
                        # print(operation)
                        pass
                    elif action == fast.Action.RESEARCH:
                        player_id = details['player_id']
                        technology_id = details['technology_id']
                        self.find_player(player_id).add_technology(technology_id, self.output_time())
                    elif action == fast.Action.BUILD:
                        player_id = details['player_id']
                        building_id = details['building_id']
                        coordinates = (details['x'], details['y'])
                        self.find_player(player_id).add_building(building_id, self.output_time(), coordinates)
                    elif action == fast.Action.GATHER_POINT:
                        # print(details)
                        pass #maybe add this?
                    elif action == fast.Action.RESIGN:
                        pass #handle winning player????
                elif operation[0] == fast.Operation.SYNC:
                    self.time += operation[1][0]
                    minutes = math.floor((self.time / (1000 * 60)))
                    if minutes not in self.added_timestamps and (minutes % 10 == 5 or minutes % 10 == 0):
                        # timestamp = self.output_time()
                        seconds = minutes * 60
                        self.added_timestamps.append(minutes)
                        [player.calculate_units_for_timestamp(seconds) for _, player in self.players.items()]
                elif operation[0] == fast.Operation.CHAT:
                    pass
    
    def get_players(self):
        return self.players
    
    def create_header_with_types(self, list):
        header = ['player']
        for key, entries in list.items():
            header.append(key)
            for _, entry in entries.items():
                header.append(entry)
        return header

    def create_analysis_report(self):
        # extend to cover buildings and technologies (done) as well

        header_units = self.create_header_with_types(UNIT_IDS)
        header_technologies = self.create_header_with_types(TECHNOLOGY_IDS)
        header_unit_timestamps = ['timestamp']
        rows_units = []
        rows_technologies = []
        player_units = {}
        timestamps = []
        for player_id, player in self.players.items():
            header_unit_timestamps.append(f'player{player_id}')
            if len(timestamps) == 0:
                [timestamps.append(timestamp) for timestamp in player.get_units_for_timestamps().keys()]

            row_units = {'player': player_id}
            self.fetch_player_data(player.get_units(), row_units)
            rows_units.append(row_units)

            row_technologies = {'player': player_id}
            self.fetch_player_data(player.get_technologies(), row_technologies)
            rows_technologies.append(row_technologies)

            player_units[player_id] = player.get_units_for_timestamps()
        
        rows_unit_timestamps = {MainType.MIL: [], MainType.ECO: []}
        for timestamp in timestamps:
            row_unit_timestamps = {MainType.MIL : [timestamp], MainType.ECO: [timestamp]}
            for player_id, player in player_units.items():
                row_unit_timestamps[MainType.MIL].append(player_units[player_id][timestamp][MainType.MIL])
                row_unit_timestamps[MainType.ECO].append(player_units[player_id][timestamp][MainType.ECO])
            rows_unit_timestamps[MainType.MIL].append(row_unit_timestamps[MainType.MIL])
            rows_unit_timestamps[MainType.ECO].append(row_unit_timestamps[MainType.ECO])

        folder_timestamp = datetime.now().strftime('%Y-%m-%d_%H_%M')

        self.create_csv_file(f'./output/{folder_timestamp}/units.csv', header_units, rows_units)
        self.create_csv_file(f'./{folder_timestamp}/technologies.csv', header_technologies, rows_technologies)
        self.create_csv_file(f'./{folder_timestamp}/mil_unit_timestamps.csv', header_unit_timestamps, rows_unit_timestamps[MainType.MIL], False)
        self.create_csv_file(f'./{folder_timestamp}/vil_unit_timestamps.csv', header_unit_timestamps, rows_unit_timestamps[MainType.ECO], False)

    def fetch_player_data(self, data, row):
        for key, entries in data.items():
            row[key] = '/'
            for entry, value in entries.items():
                row[entry] = value

    def create_csv_file(self, filename, header, rows, use_dict_writer=True):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='UTF8', newline='') as file:
            if use_dict_writer:
                writer = csv.DictWriter(file, fieldnames=header,restval=0)
                writer.writeheader()
            else:
                writer = csv.writer(file)
                writer.writerow(header)
            writer.writerows(rows)

if __name__ == '__main__':
    # read out console params / download relevant files -> probably should be invoked via init
    analysis = Analysis('replays/replay3.aoe2record')
    analysis.start_analysis()
    analysis.create_analysis_report()
    for player_id, player in analysis.get_players().items():
        pass
        # print(player.get_buildings())
        print(player_id, ' has created ', player.get_units(), '\n researched ', player.get_technologies_for_type(MainType.ECO), '\n built ', player.get_buildings_for_type(MainType.ECO))