# EZ-AOE-Details
## Description
This module visualises Age of Empires II DE statistics of replays segmented into multiple skill levels:
* PRO (ELO > 2200)
* HIGH (ELO > 1800)
* MID (ELO > 1000)
* LOW (ELO ≤ 1000)

It also generates CSV files for each replay file calculated for each player. This can be deactivated by commenting line 337 in `analysis.py`.

The replays are added to `ez-aoe-details/replays`. The current replays have been taken from aoe2.net and all feature games played as 1v1 on Arabia. Graphs generated with the given replay files can be found in `ez-aoe-details/graphs`.

It aims at understanding how player behaviour varies based on skill level, for me a more thourough explanation, see [the project Summary](SUMMARY.md).

## Data Structure
Data is passed as dictionary through the different classes. All player relevant data is stored in a `player.Player` instance. The players are hold in their respecitve `analysis.Analysis` classes which are again part of `analysis.MultipleAnalyses`  There, the relevant data for every timestamp is calculated and stored, e.g. `{0: {'units': {Economy: 0, Military: 0}, 'buildings: {Economy: 0, Military: 0}, 'action_move_coordinates': {'x': 0, 'y': 0, count: 0}, 'action_move_coordinates': {'x': 0, 'y': 0, count: 0}}}`

After all analyses have been concluded, the data from all players from the same skill levels are averaged and a dictionary with relevant calculations is created, e.g. ` {'low': {120: {'units': {Economy: 4.8, Military: 0.05}, 'buildings': {Economy: 0.1, Military: 0.05, Wall: 0.0}, 'action_move_coordinates': {'x': 17.178742296106446, 'y': 24.073642806206504, 'count': 564}, 'action_unit_coordinates': {'x': 0.0, 'y': 0.0, 'count': 0}}}}`. The key is a specific timestamp, the subkeys store the average amount of units/action location for this timestamp. Count is required for the coordinate calculations since all coordinates are added and later divided by their number of frequency.

In order to calculate the average research time of technologies and effective actions per minute (i.e. moving units, attacking), a similar approach is utlised. The average research time for all players is stored. In the end, the total resarch time is divided by the number of players who have research the technology: `{'eapm': {'pro': 45.921025117599676, 'high': 44.40773592782665, 'middle': 29.72721939895853, 'low': 16.29198645698805}, 'technologies': {'pro': {Economy: {Loom: 367.25, Feudal Age: 463.6, Double Bit Axe: 639.8421052631579}}}`. 

All relevant averaging calculations happen in `analysis.MultipleAnalysis.compute_average_results_for_type()`. The data points are then visualised in the graphs.
### Supported Visualisations
* Average eAPM
* Average villagers queued over the course of a game with average age up times
* Average villagers queued over the course of a game with key economy research
* Average military units queued over the course of a game with key military research
* Average military buildings built over the course of a game
* Average pallisade walls built over the course of a game
* Average occurence of attacking actions in game
* Average distance of moving actions from starting position
* Average distance of attacking actions (i.e., formation, attacking or patrol) from starting position
### Implemented CSV Content
* Military count for all timestamps
* Villager count for all timestamps
* Technology research time
* Queued units

The calculations are done for each player.

The generated CSV files are added to output/timestamp/REPLAY_FILE.
### Usage of Parser
The parser can be used with any replay files from the game Age of Empires II DE.
### Visualisation Modifications
To amend the visualisations, file `visualisation.py` needs to be modified. In particular: Below the comment `# set relevant technologies`.
## Installation
* `pip3 install pandas`
* `pip3 install matplotlib`
* `pip3 install git+https://github.com/happyleavesaoc/aoc-mgz.git@fix-fast`

## Execution
`python3 ez-aoe-details/analysis.py`
## How does this tool help other players?
Players are able to understand their own actions in game by analaysing their replay files. In particular, the tool enables them to understand their weak points. 
## Outline - Possible Extensions
* Abstract visualsations to enable easier reuse, i.e., enable users to decide which technologies to visualise
* Add pip package support
