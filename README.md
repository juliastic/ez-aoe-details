# EZ-AOE-Details
## Description
This module visualises Age of Empires II DE statistics of replays segmented into multiple skill levels:
* PRO (ELO > 2200)
* HIGH (ELO > 1800)
* MID (ELO > 1000)
* LOW (ELO ≤ 1000)

It also generates CSV files for each replay file calculated for each player. This can be deactivated by commenting line 337 in `analysis.py`.

The replays are added to `ez-aoe-details/replays`. The current replays have been taken from aoe2.net and all feature games played as 1v1 on Arabia. Graphs generated with the given replay files can be found in `ez-aoe-details/graphs`.

It aims to understand how player behaviour varies based on skill level, for me a more thourough explanation, see [Problem Description](PROBLEM_DESCRIPTION.md) and [Summary](SUMMARY.md).
## How does this tool help other players?
Players are able to understand their own actions in game by analaysing their replay files. In particular, the tool enables them to understand their weak points.
## Installation
* `git clone https://github.com/juliastic/ez-aoe-details.git`
* `pip3 install pandas`
* `pip3 install matplotlib`
* `pip3 install git+https://github.com/happyleavesaoc/aoc-mgz.git@fix-fast`
## Execution
`python3 ez-aoe-details/analysis.py`
## Data Structure
Data is passed as dictionary through the different classes. All player relevant data is stored in a `player.Player` instance. The players are held in their respective `analysis.Analysis` classes which are again part of `analysis.MultipleAnalyses`. All project relevant constants are stored in `units.py`, i.e., technologies, units and buildings. The data is visualised in `visualisation.AoEGraphs`.

The replay files are parsed seperately in `analysis.Analysis` and the actions are added to their players. This is done by checking the ID of the action and handling it accordingly, For example, in case of a unit queue, the unit ID is parsed. In `player.Player`, the data is matched with its name and stored accordingly. Every two minutes, the data is calculated and stored in a dictionary entry:

`{0: {'units': {Economy: 0, Military: 0}, 'buildings: {Economy: 0, Military: 0}, 'action_move_coordinates': {'x': 0, 'y': 0, count: 0}, 'action_move_coordinates': {'x': 0, 'y': 0, count: 0}}}`.

After all analyses have been concluded, the data from all players from the same skill levels are averaged and a dictionary with relevant calculations is created in `analysis.MultipleAnalyses`: 

` {'low': {120: {'units': {Economy: 4.8, Military: 0.05}, 'buildings': {Economy: 0.1, Military: 0.05, Wall: 0.0}, 'action_move_coordinates': {'x': 17.178742296106446, 'y': 24.073642806206504, 'count': 564}, 'action_unit_coordinates': {'x': 0.0, 'y': 0.0, 'count': 0}}}}`. 

The key is a specific timestamp, the subkeys store the average amount of TOTAL created units/buildings up to the timestamp and the action location between the last timestamp and the current one timestamp. `Count` is required for the coordinate calculations since all coordinates are added and later divided by their number of occurence (key `count`).

In order to calculate the average research time of technologies and effective actions per minute (i.e., moving units, attacking), a similar approach is utlised. The average research time for all players is stored in seconds. In the end, the total resarch time is divided by the number of players who have researched the technology: 

`{'eapm': {'pro': 45.921025117599676, 'high': 44.40773592782665, 'middle': 29.72721939895853, 'low': 16.29198645698805}, 'technologies': {'pro': {Economy: {Loom: 367.25, Feudal Age: 463.6, Double Bit Axe: 639.8421052631579}}}`. 

All relevant averaging calculations happen in `analysis.MultipleAnalyses.compute_average_results_for_type()`. The data points are then visualised in the graphs.
## Supported Visualisations
* Average eAPM
* Average villagers queued over the course of a game with average age up times
* Average villagers queued over the course of a game with key economy research
* Average military units queued over the course of a game with key military research
* Average military buildings built over the course of a game
* Average pallisade walls built over the course of a game
* Average occurence of attacking actions in game
* Average distance of moving actions from starting position
* Average distance of attacking actions (i.e., formation, attacking or patrol) from starting position
## Implemented CSV Content
* Military count for all timestamps
* Villager count for all timestamps
* Technology research time
* Queued units

The calculations are done for each player.

The generated CSV files are added to `output/timestamp/REPLAY_FILE`.
## Usage of Parser
The parser can be used with any replay files from the game Age of Empires II DE.
## Customisation
### General
To customise the analysed replays, the main method in `ez-aoe-details/analysis.py` can be adapted. Notably, constants `SkillLevel.CUSTOM_A` and `SkillLevel.CUSTOM_B` have been added to facilicate this action. They can be used when referencing paths containing other replays:

`analyses = MultipleAnalyses({SkillLevel.CUSTOM_A: file_path + '/custom_a', SkillLevel.CUSTOM_B: file_path + '/custom_b'})`
### Visualisation Modifications
To amend the visualisations, file `visualisation.py` needs to be modified. Modification of displayed technologies can be easily changed by amending the technologies below comment `# set relevant technologies`. For an overview of currently implemented technologies see also `units.Technology`.
## Outline - Possible Extensions
* Abstract visualsations to enable easier reuse, i.e., enable users to decide which technologies to visualise
* Add missing IDs: Not all unit and technology IDs have been added as they were not relevant for the selected replay files
* Extend CSV implementation
* Add pip package support
