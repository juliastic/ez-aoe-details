import typing
from units import UNIT_IDS, BUILDING_IDS, TECHNOLOGY_IDS, MainType, UnitType, FilterType, Technology, Building, BuildingType
from mgz import fast
class Player:
    """This class contains all the necessary information for a player.
    In particular: buildings built, military queued, villagers queued and actions.
    """
    def __init__(self, id: int, starting_position: typing.Tuple[float, float]=(0, 0)):
        self.id = id
        self.units = {MainType.ECO: {}}
        for type in UnitType:
            self.units[type] = {}
        self.technologies = {MainType.ECO: {}, MainType.MIL: {}}
        self.buildings = {MainType.ECO: {}, MainType.MIL: {}, BuildingType.WALL: {}}
        self.eAPM = 0
        self.gameduration = -1
        self.state_for_timestamps = {0: {FilterType.UNITS: {MainType.ECO: 0, MainType.MIL: 0}, FilterType.BUILDINGS: {MainType.ECO: 0, MainType.MIL: 0, BuildingType.WALL: 0}, FilterType.ACTION_MOVE_COORDINATES: {'x': 0, 'y': 0}}}
        self.actions = []
        self.starting_position = starting_position

    def get_all_unit_count(self) -> int:
        """Returns the unit count based on type, e.g. {Economy: 72, Infantry: 1, Cavalary: 46, Archer: 17, Monk: 4, Siege: 17}

        Returns:
            dict: containing all UNIT_IDS keys + corresponding unit count
        """
        count = {}
        for key, value in self.units.items():
            count[key] = sum(value.values())
        return count

    def get_units(self) -> typing.Dict[MainType, typing.Dict[str, int]]:
        return self.units
    
    def add_unit(self, unit: int) -> None:
        """Adds a queued unit id to the corresponding unit id count

        Args:
            unit (int): unit id
        """
        for type, units in UNIT_IDS.items():
            if unit in units:
                unit = units[unit]
                self.units[type][unit] = self.units[type].get(unit, 0) + 1
                return

    def calculate_state_for_timestamp(self, timestamp: int):
        """Calculates all relevant information, i.e. military buildings and player actions, for a specific timestamp. The values are added to a dictionary holding all timestamp results.
        See get_state_for_timestamp(self) for an overview regarding the added value.

        Args:
            timestamp (int): the relevant timestamp 
        """
        # calculate unit and building counts
        vil_count = sum(self.units[MainType.ECO].values())
        mil_count = 0
        for type, unit in self.units.items():
            if type != MainType.ECO:
                mil_count += sum(unit.values())

        eco_building_count = sum(self.buildings[MainType.ECO].values())
        mil_building_count = sum(self.buildings[MainType.MIL].values())
        wall_count = sum(self.buildings[BuildingType.WALL].values())

        # calculate average action coordinates
        action_move_coordinates = {'x': 0, 'y': 0, 'count': 0}
        action_unit_coordinates = {'x': 0, 'y': 0, 'count': 0}
        for action in self.actions:
            if action['timestamp'] > timestamp - 120 and action['timestamp'] < timestamp: # 120 == update every two min
                if action['action'] == fast.Action.MOVE:
                    action_move_coordinates['x'] += abs(self.starting_position[0] - action['x'])
                    action_move_coordinates['y'] += abs(self.starting_position[1] - action['y'])
                    action_move_coordinates['count'] += 1
                elif action['action'] == fast.Action.DE_ATTACK_MOVE or fast.Action.PATROL == action['action'] or fast.Action.FORMATION == action['action'] or fast.Action.ATTACK_GROUND == action['action']:
                    action_unit_coordinates['x'] += abs(self.starting_position[0] - action['x'])
                    action_unit_coordinates['y'] += abs(self.starting_position[1] - action['y'])
                    action_unit_coordinates['count'] += 1    
  
        # average based on occurence of actions
        if action_move_coordinates['count'] > 0:
            action_move_coordinates['x'] /= action_move_coordinates['count']
            action_move_coordinates['y'] /= action_move_coordinates['count']

        if action_unit_coordinates['count'] > 0:
            action_unit_coordinates['x'] /= action_unit_coordinates['count']
            action_unit_coordinates['y'] /= action_unit_coordinates['count']     

        self.state_for_timestamps[timestamp] = {
            FilterType.UNITS: {MainType.ECO: vil_count, MainType.MIL: mil_count}, 
            FilterType.BUILDINGS: {MainType.ECO: eco_building_count, MainType.MIL: mil_building_count, BuildingType.WALL: wall_count}, 
            FilterType.ACTION_MOVE_COORDINATES: action_move_coordinates,
            FilterType.ACTION_UNIT_COORDINATES: action_unit_coordinates}

    def get_state_for_timestamps(self) -> typing.Dict[int, typing.Dict[FilterType, typing.Dict[MainType, int]]]:
        """Gets the state for all timestamps, e.g. {0: {FilterType.UNITS: {MainType.ECO: 0, MainType.MIL: 0}, FilterType.BUILDINGS: {MainType.ECO: 0, MainType.MIL: 0}, FilterType.ACTION_MOVE_COORDINATES: {'x': 0, 'y': 0, count: 0}, FilterType.ACTION_UNIT_COORDINATES: {'x': 0, 'y': 0, count: 0}}}

        Returns:
            typing.Dict[int, typing.Dict[FilterType, typing.Dict[MainType, int]]]: state for all timestamps
        """
        return self.state_for_timestamps

    def get_technologies_for_type(self, type: MainType) -> typing.Dict[Technology, int]:
        """Gets all technologies for a specific type, i.e. MainType.ECO and MainType.MIL

        Args:
            type (MainType): the type of technologies

        Returns:
            typing.Dict[Technology, int]: all technologies for a given type
        """
        if type in self.technologies:
            return self.technologies[type]
        return {}

    def get_technologies(self) -> typing.Dict[MainType, typing.Dict[Technology, int]]:
        """Gets all technologies with their corresponding timestamps

        Returns:
            typing.Dict[MainType, typing.Dict[Technology, int]]: all technologies
        """
        return self.technologies

    def add_technology(self, technology: str, time: int):
        """Adds a technology with its corresponding research time

        Args:
            technology (str): technology id
            time (int): time
        """
        for type, technologies in TECHNOLOGY_IDS.items():
            if technology in technologies:
                technology = technologies[technology]
                self.technologies[type][technology] = time
                return

    def set_starting_position(self, starting_position: typing.Tuple[int, int]):
        """Sets the starting position of the player, required if the game is started in nomad

        Args:
            starting_position (typing.Tuple[int, int]): TC starting position 
        """
        self.starting_position = starting_position

    def get_starting_position(self) -> typing.Tuple[int, int]:
        return self.starting_position

    def add_building(self, building_id: int) -> None:
        """Adds a queued building id to the corresponding unit id count.

        Args:
            building_id (int): building id
        """
        for type, buildings in BUILDING_IDS.items():
            if building_id in buildings:
                building = buildings[building_id]
                self.buildings[type][building] = self.buildings[type].get(building, 0) + 1
                return

    def get_buildings_for_type(self, type: str) -> typing.Dict[str, int]:
        if type in self.buildings:
            return self.buildings[type]
        return {}
    
    def get_buildings(self) -> typing.Dict[MainType, typing.Dict[Building, int]]:
        return self.buildings

    def increase_eAPM(self) -> None:
        self.eAPM += 1
    
    def set_gameduration(self, gameduration: int) -> None:
        self.gameduration = gameduration

    def get_average_eAPM(self) -> float:
        return self.eAPM / self.gameduration

    def add_action(self, action: typing.Dict[str, any]):
        self.actions.append(action)

    def get_actions(self) -> list[typing.Dict[str, float]]:
        return self.actions

    def get_average_action_coordinates(self) -> typing.Tuple[float, float]:
        return self.get_average_coordinates(self.actions)

    def get_average_move_action_coordinates(self) -> typing.Tuple[float, float]:
        filtered_actions = [action for action in self.actions if fast.Action.MOVE == action['action']]
        return self.get_average_coordinates(filtered_actions)

    def get_average_unit_coordinates(self) -> typing.Tuple[float, float]:
        filtered_actions = [action for action in self.actions if fast.Action.DE_ATTACK_MOVE == action['action'] or fast.Action.PATROL == action['action'] or fast.Action.FORMATION == action['action'] or fast.Action.ATTACK_GROUND == action['action']]
        return self.get_average_coordinates(filtered_actions)

    def get_average_coordinates(self, actions: list[typing.Dict[str, any]]) -> typing.Tuple[float, float]:
        """Gets the average coordinates for all actions passed as parameter

        Args:
            actions (list[typing.Dict[str, any]]): the action containing x and y coordinates

        Returns:
            typing.Tuple[float, float]: the average x and y action location
        """
        actions_count = len(actions)
        if actions_count == 0:
            return (0, 0)
        average_x = sum(abs(self.starting_position[0] - action['x']) for action in actions) / actions_count
        average_y = sum(abs(self.starting_position[1] - action['y']) for action in actions) / actions_count
        return (average_x, average_y)
