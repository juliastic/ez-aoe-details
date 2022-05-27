import typing
from units import UNIT_IDS, BUILDING_IDS, TECHNOLOGY_IDS, MainType, UnitType, FilterType, Technology, Building
class Player:
    def __init__(self, id: int, starting_position: typing.Tuple[float, float]=(0, 0)):
        self.id = id
        self.units = {MainType.ECO: {}}
        for type in UnitType:
            self.units[type] = {}
        self.technologies = {MainType.ECO: {}, MainType.MIL: {}}
        self.buildings = {MainType.ECO: {}, MainType.MIL: {}}
        self.eAPM = 0
        self.gameduration = -1
        self.state_for_timestamps = {0: {FilterType.UNITS: {MainType.ECO: 0, MainType.MIL: 0}, FilterType.BUILDINGS: {MainType.ECO: 0, MainType.MIL: 0}}}
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
    
    def add_unit(self, unit) -> None:
        for type, units in UNIT_IDS.items():
            if unit in units:
                unit = units[unit]
                self.units[type][unit] = self.units[type].get(unit, 0) + 1
                return

    def calculate_state_for_timestamp(self, timestamp: int):
        vil_count = sum(self.units[MainType.ECO].values())
        mil_count = 0
        for type, unit in self.units.items():
            if type != MainType.ECO:
                mil_count += sum(unit.values())

        eco_building_count = sum(self.buildings[MainType.ECO].values())
        mil_building_count = sum(self.buildings[MainType.MIL].values())
        self.state_for_timestamps[timestamp] = {
            FilterType.UNITS: {MainType.ECO: vil_count, MainType.MIL: mil_count}, 
            FilterType.BUILDINGS: {MainType.ECO: eco_building_count, MainType.MIL: mil_building_count}}

    def get_state_for_timestamps(self) -> typing.Dict[int, typing.Dict[FilterType, typing.Dict[MainType, int]]]:
        return self.state_for_timestamps

    def get_technologies_for_type(self, type: str) -> typing.Dict[Technology, int]:
        if type in self.technologies:
            return self.technologies[type]
        return {}

    def get_technologies(self) -> typing.Dict[MainType, typing.Dict[Technology, int]]:
        return self.technologies

    def add_technology(self, technology: str, time: int):
        for type, technologies in TECHNOLOGY_IDS.items():
            if technology in technologies:
                technology = technologies[technology]
                self.technologies[type][technology] = time
                return

    def set_starting_position(self, starting_position: typing.Tuple[int, int]):
        self.starting_position = starting_position

    def get_starting_position(self) -> typing.Tuple[int, int]:
        return self.starting_position

    def add_building(self, building_id: int) -> None:
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

    def add_action(self, action: typing.Dict[str, float]):
        self.actions.append(action)

    def get_actions(self) -> list[typing.Dict[str, float]]:
        return self.actions

    def get_average_action_coordinates(self) -> typing.Tuple[float, float]:
        actions_count = len(self.actions)
        if actions_count == 0:
            return (0, 0)
        average_x = sum(abs(self.starting_position[0] - action['x']) for action in self.actions) / actions_count
        average_y = sum(abs(self.starting_position[1] - action['y']) for action in self.actions) / actions_count
        return (average_x, average_y)
