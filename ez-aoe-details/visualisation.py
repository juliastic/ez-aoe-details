import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import typing
from units import MainType, FilterType, SkillLevel, Technology, BuildingType

class AoEGraphs():
    """This class handles the visualisation of analysis results. It relies on helper classes from units.* to not rely on hardcoded values.
    """
    def __init__(self, average_timestamp_analysis_results: typing.Dict[SkillLevel, typing.Dict[int, typing.Dict[FilterType, typing.Dict[MainType, int]]]], average_results: typing.Dict[FilterType, typing.Dict[SkillLevel, any]]):
        """Constructor

        Args:
            average_timestamp_analysis_results (typing.Dict[SkillLevel, typing.Dict[int, typing.Dict[FilterType, typing.Dict[MainType, int]]]]): All the analysis results, example structure:
             {'low': {120: {'units': {Economy: 4.8, Military: 0.05}, 'buildings': {Economy: 0.1, Military: 0.05, Wall: 0.0}, 'action_move_coordinates': {'x': 17.178742296106446, 'y': 24.073642806206504, 'count': 564}, 'action_unit_coordinates': {'x': 0.0, 'y': 0.0, 'count': 0}}}}
            average_results (typing.Dict[FilterType, typing.Dict[SkillLevel, any]]): holds eAPM and average technology research times for all players, e.g. {'eapm': {'pro': 45.921025117599676, 'high': 44.40773592782665, 'middle': 29.72721939895853, 'low': 16.29198645698805}, 'technologies': {'pro': {Economy: {Loom: 367.25, Feudal Age: 463.6, Double Bit Axe: 639.8421052631579}}}
        """
        self.average_timestamp_analysis_results = average_timestamp_analysis_results
        self.average_results = average_results

    def output_results(self) -> None:
        """Outputs all relevant graphs
        """
        timestamps = []
        vil_unit_values = {k: [] for k in self.average_timestamp_analysis_results}
        eco_age_values = {k: {} for k in self.average_timestamp_analysis_results}
        eco_technology_values = {k: {} for k in self.average_timestamp_analysis_results}

        mil_unit_values = {k: [] for k in self.average_timestamp_analysis_results}
        mil_technology_values = {k: {} for k in self.average_timestamp_analysis_results}

        eco_building_values = {k: [] for k in self.average_timestamp_analysis_results}
        mil_building_values = {k: [] for k in self.average_timestamp_analysis_results}
        wall_values = {k: [] for k in self.average_timestamp_analysis_results}

        action_coordinate_values = {k: [] for k in self.average_timestamp_analysis_results}
        action_coordinate_unit_values = {k: [] for k in self.average_timestamp_analysis_results}
        action_coordinate_unit_count_values = {k: [] for k in self.average_timestamp_analysis_results}

        for type, values in self.average_timestamp_analysis_results.items():
            # set relevant technologies
            eco_age_values[type][Technology.FEUDAL_AGE] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.FEUDAL_AGE] / 60
            eco_age_values[type][Technology.CASTLE_AGE] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.CASTLE_AGE] / 60
            eco_age_values[type][Technology.IMPERIAL_AGE] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.IMPERIAL_AGE] / 60

            eco_technology_values[type][Technology.HAND_CART] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.HAND_CART] / 60
            eco_technology_values[type][Technology.WHEELBARROW] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.WHEELBARROW] / 60
            eco_technology_values[type][Technology.LOOM] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.LOOM] / 60

            mil_technology_values[type][Technology.FLETCHING] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.MIL][Technology.FLETCHING] / 60
            mil_technology_values[type][Technology.FORGING] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.MIL][Technology.FORGING] / 60
            mil_technology_values[type][Technology.BALLISTICS] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.MIL][Technology.BALLISTICS] / 60

            # set entries for timestamps
            for timestamp, entries in values.items():
                timestamps.append(timestamp / 60)
                mil_building_values[type].append(entries[FilterType.BUILDINGS][MainType.MIL])
                wall_values[type].append(entries[FilterType.BUILDINGS][BuildingType.WALL])
                eco_building_values[type].append(entries[FilterType.BUILDINGS][MainType.ECO])

                vil_unit_values[type].append(entries[FilterType.UNITS][MainType.ECO])
                mil_unit_values[type].append(entries[FilterType.UNITS][MainType.MIL])

                action_coordinate_values[type].append(math.sqrt(math.pow(entries[FilterType.ACTION_MOVE_COORDINATES]['x'], 2) + math.pow(entries[FilterType.ACTION_MOVE_COORDINATES]['y'], 2)))
                action_coordinate_unit_values[type].append(math.sqrt(math.pow(entries[FilterType.ACTION_UNIT_COORDINATES]['x'], 2) + math.pow(entries[FilterType.ACTION_UNIT_COORDINATES]['y'], 2)))
                action_coordinate_unit_count_values[type].append(entries[FilterType.ACTION_UNIT_COORDINATES]['count'])
        timestamps_length = len(timestamps)

        # fill up array with none for missing values
        value_entries = [vil_unit_values, mil_building_values, eco_building_values, wall_values, mil_unit_values, action_coordinate_values, action_coordinate_unit_values, action_coordinate_unit_count_values]
        for entry in value_entries:
            for entries in entry.values():
                entries.extend([None] * (timestamps_length - len(entries)))

        type_colors = {SkillLevel.PRO: 'blue', SkillLevel.HIGH: 'orange', SkillLevel.MIDDLE: 'green', SkillLevel.LOW: 'red'}

        # Average Villager Count + Age Technologies
        self.generate_line_chart_with_technologies(vil_unit_values, timestamps, type_colors, eco_age_values, 1, 'Average Villager Count')
        # Average Villager Count + Eco Technologies
        self.generate_line_chart_with_technologies(vil_unit_values, timestamps, type_colors, eco_technology_values, 2, 'Average Villager Count')
        # Average Military Count + Technologies
        self.generate_line_chart_with_technologies(mil_unit_values, timestamps, type_colors, mil_technology_values, 3, 'Average Military Count')

        # Average Mil Building Count
        self.generate_line_chart(mil_building_values, timestamps, type_colors, 4, 'Average Military Buildings')
        # Average Eco Building Count
        self.generate_line_chart(eco_building_values, timestamps, type_colors, 5, 'Average Eco Buildings')

        # Average eAPM
        df = pd.DataFrame({'Average eAPM': self.average_results[FilterType.EAPM].values()}, index=self.average_results[FilterType.EAPM].keys())
        ax = df.plot(kind='bar', legend=False)
        index = 0
        for bar in ax.patches:
            bar.set_color(list(type_colors.values())[index])
            index += 1
        plt.ylabel('Average Count')
        plt.title('Average eAPM Activity')
        plt.figure(6)

        # Average Action from Starting Position
        self.generate_line_chart(action_coordinate_values, timestamps, type_colors, 7, 'Distance of Moving Actions from Starting TC in Game')
        self.generate_line_chart(action_coordinate_unit_values, timestamps, type_colors, 8, 'Distance of Attacking Actions from Starting TC in Game')
        self.generate_line_chart(action_coordinate_unit_count_values, timestamps, type_colors, 9, 'Occurence of Attacking Actions in Game')

        # Average Wall Count
        self.generate_line_chart(wall_values, timestamps, type_colors, 10, 'Average Walls Built')

        # Show all figures
        plt.show()

    def generate_line_chart_with_technologies(self, values: typing.Dict[SkillLevel, list[float]], timestamps: list[int], colors: typing.Dict[str, str], technologies: typing.Dict[SkillLevel, typing.Dict[Technology, int]], figure_count: int, title: str, linestyles: list[str] = ['-', '--', ':', '-.']) -> None:
        """Generates a line chart with given technologies

        Args:
            values (typing.Dict[SkillLevel, list[float]): y axis values categorised by skill level
            timestamps (list[int]): x axis values
            colors (typing.Dict[str, str]): colors for skill level
            technologies (typing.Dict[SkillLevel, typing.Dict[Technology, int]]): technologies with average research time
            figure_count (int): figure count
            title (str): title of line chart
            linestyle (list[str]): the linestyles used for the chart. Default value ['-', '--', ':', '-.'].
        """
        _, ax = plt.subplots()
        ax_twin = ax.twinx()
        df = pd.DataFrame(values, timestamps)
        ax = df.plot(color=colors.values(), ax=ax)
        plt.xlabel('Timestamp (in min)')
        plt.ylabel(title)
        plt.title(title)

        lines = []
        for l in linestyles:
            lines.append(Line2D([0,1],[0,1],linestyle=l, color='0.8'))
        technology_list = []
        max_key = max(values, key = lambda k: list(filter(None.__ne__, k[1])))
        max_value_avg = max(list(filter(None.__ne__, values[max_key]))) / 1.5

        for type, technologies in technologies.items():
            index = 0
            for technology, timestamp in technologies.items():
                if index > len(linestyles) - 1:
                    index = 0
                line = plt.vlines(x=timestamp, ymin=0, ymax=max_value_avg, colors=colors[type], ls=linestyles[index], lw=1, label='')
                if technology not in technology_list:
                    technology_list.append(technology)
                index += 1

        ax_twin.legend(lines, technology_list, loc=4)
        plt.figure(figure_count)
    
    def generate_line_chart(self, values: typing.Dict[SkillLevel, list[float]], timestamps: list[int], colors: typing.Dict[str, str], figure_count: int, title: str) -> None:
        """Generates a line chart

        Args:
            values (list[float]): y axis values sorted categorised by skill level
            timestamps (list[int]): x axis values
            colors (typing.Dict[str, str]): colors of the lines mapped by skill level
            figure_count (int): the figure count
            title (str): title of the figure
        """
        df = pd.DataFrame(values, index=timestamps)
        df.plot(color=colors.values())
        plt.xlabel('Timestamp (in min)')
        plt.ylabel(title)
        plt.title(title)
        plt.figure(figure_count)
