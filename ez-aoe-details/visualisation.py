import math
import pandas as pd
import matplotlib.pyplot as plt
import typing
from units import MainType, FilterType, SkillLevel, Technology

class AoELineGraph():
    # analysis_results: dict of analysis reports
    # results == dict with list containing players
    # assumed: only units present -> need to split end data into multiple dicts ...
    def __init__(self, average_timestamp_analysis_results: typing.Dict[SkillLevel, typing.Dict[int, typing.Dict[FilterType, typing.Dict[MainType, int]]]], average_results: typing.Dict[FilterType, typing.Dict[SkillLevel, any]]):
        self.average_timestamp_analysis_results = average_timestamp_analysis_results
        self.average_results = average_results

    def output_results(self) -> None:
        timestamps = []
        vil_unit_values = {k: [] for k in self.average_timestamp_analysis_results}
        eco_technology_values = {k: {} for k in self.average_timestamp_analysis_results}
        mil_building_values = {k: [] for k in self.average_timestamp_analysis_results}
        mil_unit_values = {k: [] for k in self.average_timestamp_analysis_results}
        for type, values in self.average_timestamp_analysis_results.items():
            eco_technology_values[type][Technology.WHEELBARROW] = self.average_results[FilterType.TECHNOLOGIES][type][MainType.ECO][Technology.WHEELBARROW] / 60
            for timestamp, entries in values.items():
                timestamps.append(timestamp/60)
                vil_unit_values[type].append(entries[FilterType.UNITS][MainType.ECO])
                mil_building_values[type].append(entries[FilterType.BUILDINGS][MainType.MIL])
                mil_unit_values[type].append(entries[FilterType.UNITS][MainType.MIL])

        timestamps_length = len(timestamps)

        # fill up array with none for missing values
        for entries in vil_unit_values.values():
            entries.extend([None]*(timestamps_length - len(entries)))

        for entries in mil_building_values.values():
            entries.extend([None]*(timestamps_length - len(entries)))

        # Average Vil Count
        df = pd.DataFrame(vil_unit_values, timestamps)
        df.plot()
        plt.xlabel('Timestamp (in min)')
        plt.ylabel('Avg Villagers')
        plt.title('Avg Villagers in Games')
        # Handle Different colour and line types .. rework legend to not contain so many entries -> Maybe show text WITH Line?
        for type, technologies in eco_technology_values.items():
            filtered_vil_unit_values = list(filter(None.__ne__, vil_unit_values[type]))
            for technology, timestamp in technologies.items():
                vil_min = min(filtered_vil_unit_values)
                vil_max = max(filtered_vil_unit_values)
                plt.vlines(x=timestamp, ymin=vil_min, ymax=vil_max, colors='purple', ls='--', lw=2, label='')
                plt.text(timestamp, vil_max / 2, f'{technology} {type}', rotation=90, verticalalignment='center', size=8)
        plt.figure(1)

        # Average Mil Building Count
        df = pd.DataFrame(mil_building_values, index=timestamps)
        df.plot()
        plt.xlabel('Timestamp (in min)')
        plt.ylabel('Avg Mil Units')
        plt.title('Avg Mil Units in Games')
        plt.figure(2)

        # Average eAPM
        df = pd.DataFrame({'Average eAPM': self.average_results[FilterType.EAPM].values()}, index=self.average_results[FilterType.EAPM].keys())
        df.plot.bar(rot=0)
        plt.figure(3)

        # Average Action from Starting Position
        # think of a better visualisation technique
        distances = [math.sqrt(math.pow(coordinates['x'], 2) + math.pow(coordinates['y'], 2)) for coordinates in self.average_results[FilterType.ACTION_COORDINATES].values()]
        df = pd.DataFrame({'Average Action From Starting Position': distances}, index=self.average_results[FilterType.ACTION_COORDINATES].keys())
        df.plot.bar(rot=0)
        plt.figure(4)

        # Show all figures
        plt.show()
