# EZ-AOE-Details
## Description
This module visualises Age of Empires II DE statistics of replays segmented into multiple skill levels:
* PRO (ELO > 2200)
* HIGH (ELO > 1800)
* MID (ELO > 1000)
* LOW (ELO ≤ 1000)

It also generates CSV files for each replay file calculated for each player. This can be deactivated by commenting line 337 in `analysis.py`.

The replays are added to `ez-aoe-details/replays`. The current replays have been taken from aoe2.net and all feature games played as 1v1 on Arabia. Graphs generated with the given replay files can be found in `ez-aoe-details/graphs`.

It aims at understanding how player behaviour varies based on skill level, for me a more thourough explanation, see [the project Summary](./SUMMARY.MD).

### Supported Visualisations
* average eAPM
* average villagers queued over the course of a game with average age up times
* average villagers queued over the course of a game with key economy research
* average military units queued over the course of a game with key military research
* average military buildings built over the course of a game
* average pallisade walls built over the course of a game
* average occurence of attacking actions in game
* average distance of moving actions from starting position
* average distance of attacking actions (i.e., formation, attacking or patrol) from starting position
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