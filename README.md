# EZ-AOE-Details
## Description
This module visualises Age of Empires II DE statistics of replays segmented into multiple skill levels:
* PRO (ELO > 2200)
* HIGH (ELO > 1800)
* MID (ELO > 1000)
* LOW (ELO <= 1000)

The replays are added to `ez-aoe-details/replays`.

Currently supported:
* average eAPM
* average villagers queued over the course of a game
* average military buildings built over the course of a game

## Installation
* `pip3 install pandas`
* `pip3 install matplotlib`
* `pip3 install adjustText`
* `pip3 install git+https://github.com/happyleavesaoc/aoc-mgz.git@fix-fast`

## Execution
`python3 ez-aoe-details/analysis.py`