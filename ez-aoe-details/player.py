from units import UNIT_IDS, BUILDING_IDS, TECHNOLOGY_IDS, MainType, UnitType, Unit

class Player:

    def __init__(self, id):
        self.id = id
        self.units = {MainType.ECO: {}}
        for type in UnitType:
            self.units[type] = {}
        self.units_for_timestamps = {0: {MainType.ECO: 0, MainType.MIL: 0}}
        # self.units[UnitType.CAV][Unit.SCOUT] = 1 #todo: handle civ specific differences ...?? -> maybe not required
        self.technologies = {MainType.ECO: {}, MainType.MIL: {}}
        self.buildings = {MainType.ECO: {}, MainType.MIL: {}}


    def get_all_unit_count(self):
        """Returns the unit count based on type, e.g. {Economy: 72, Infantry: 1, Cavalary: 46, Archer: 17, Monk: 4, Siege: 17}

        Returns:
            dict: containing all UNIT_IDS keys + corresponding unit count
        """
        count = {}
        for key, value in self.units.items():
            count[key] = sum(value.values())
        return count

    def get_units(self):
        return self.units
    
    def add_unit(self, unit):
        for type, units in UNIT_IDS.items():
            if unit in units:
                unit = units[unit]
                self.units[type][unit] = self.units[type].get(unit, 0) + 1
                return

    def calculate_units_for_timestamp(self, timestamp):
        vil_count = sum(self.units[MainType.ECO].values())
        mil_count = 0
        for type, unit in self.units.items():
            if type != MainType.ECO:
                mil_count += sum(unit.values())
        self.units_for_timestamps[timestamp] = {MainType.ECO: vil_count, MainType.MIL: mil_count}

    def get_units_for_timestamps(self):
        return self.units_for_timestamps

    def get_filtered_units_for_timestamps(self):
        """Filters all units for timestamp entries for a specific type and returns them as a dictionary

        Returns:
            dict: dict filtered in MainType.ECO and MainType.MIL
        """
        vil_unit_timestamps = {}
        mil_unit_timestamps = {}
        for timestamp, values in self.units_for_timestamps.items():
            for type, value in values.items():
                if type == MainType.ECO:
                    vil_unit_timestamps[timestamp] = value
                else:
                    mil_unit_timestamps[timestamp] = value

        return {MainType.ECO: vil_unit_timestamps, MainType.MIL: mil_unit_timestamps}

    def get_technologies_for_type(self, type):
        if type in self.technologies:
            return self.technologies[type]
        return {}

    def get_technologies(self):
        return self.technologies

    def add_technology(self, technology, time):
        for type, technologies in TECHNOLOGY_IDS.items():
            if technology in technologies:
                technology = technologies[technology]
                self.technologies[type][technology] = time
                return
    
    def add_building(self, building, time, coordinates):
        for type, buildings in BUILDING_IDS.items():
            if building in buildings:
                self.buildings[type].setdefault(buildings[building], []).append([time, coordinates])
                return

    def get_buildings_for_type(self, type):
        if type in self.buildings:
            return self.buildings[type]
        return {}
    
    def get_buildings(self):
        return self.buildings
