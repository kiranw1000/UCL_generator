# UCL Generator
Repository for emulating the Champions League League Phase Draw.

# Description
Each year, the UEFA Champions League draws 8 matches for each of the 36 teams in the competition. The teams are split into 4 pots based on their ranking coming into the competition with pot 1 containing the highest ranked teams and pot 4 containing the lowest ranked teams.

## Requirements
1. Each team plays 8 total games.
2. A team cannot play another team twice
3. Each team plays 1 home game and 1 away game against teams from each pot including their own pot.
4. A team cannot play a team from its own country.

# Repository Usage
### Implementation
Rewrite `core_algorithm` in [src/algorithm.py](https://github.com/kiranw1000/UCL_generator/blob/main/src/algorithm.py) to take in the list of teams and output a list of schedules.
### Testing
1. Clone this repo and navigate to its root directory.
2. Run `pip install -r requirements.txt`
3. Run `pytest` and observe the results.

## Input Format
The algorithm should take in a list of `Team` objects as defined in [src/datatypes.py](https://github.com/kiranw1000/UCL_generator/blob/main/src/datatypes.py).

## Output Format
Th algorithm should return a dictionary mapping each `Team` object provided to it to a corresponding `Schedule` object. Each `Schedule` object holds multiple `Match` objects that will be used to check the validity of the solution and can be added to a schedule by using the `add_match` function of `Schedule`. Each of these object classes are defined in [src/datatypes.py](https://github.com/kiranw1000/UCL_generator/blob/main/src/datatypes.py).