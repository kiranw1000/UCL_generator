from ..src.datatypes import Team, Match, Pot, Schedule
from ..src.algorithm import run_draw
import json, pytest

with open("teams.json") as f:
    teams = json.load(f)
teams = [Team(team["name"], Pot(team["pot"]), team["country"]) for team in teams]
schedule = run_draw(teams)

def verify_different_countries_match(match: Match):
    '''
    Verifies that the two teams in the match are from different countries.
    '''
    return match.home.country != match.away.country

def verify_different_teams_match(match: Match):
    '''
    Verifies that the two teams in the match are different teams.
    '''
    return match.home.name != match.away.name

def verify_match_symmetry(match: Match, fixtures: list[Match]):
    '''
    Verifies that if team A is playing team B at home, then team B is playing team A away.
    '''
    return match in fixtures

@pytest.mark.parametrize("team, schedule", schedule.items())
def test_schedule(team: Team, schedule: Schedule):
    '''
    Verifies that the team is scheduled to play 8 games, 1 home and 1 away from each of 4 pots with each team being different.
    '''
    home_games = set()
    away_games = set()
    # Verify that each match has different teams from different countries
    for pot, matches in schedule.matches.items():
        for match in matches:
            assert verify_different_countries_match(match), "Teams are from the same country"
            assert verify_different_teams_match(match), "Teams are the same"
            assert verify_match_symmetry(match, matches), "Match symmetry is broken"
            if match.home == team:
                home_games.add(match.away)
            elif match.away == team:
                away_games.add(match.home)
    # Verify that there are 4 home games and 4 away games
    assert len(home_games) == 4, "Incorrect number of home games"
    assert len(away_games) == 4, "Incorrect number of away games"
    assert len(home_games.union(away_games)) == 8, "Incorrect total number of games"
    # Verify that there are 4 pots represented in home games and away games
    home_pots = set()
    for opponent in home_games:
        assert opponent.pot not in home_pots, "Duplicate pot found in home games"
        home_pots.add(opponent.pot)
    away_pots = set()
    for opponent in away_games:
        assert opponent.pot not in away_pots, "Duplicate pot found in away games"
        away_pots.add(opponent.pot)
    assert home_pots == away_pots, "Home pots and away pots do not match"

# def test_run_draw():
#     with open("teams.json") as f:
#         teams = json.load(f)
#     teams = [Team(team["name"], Pot(team["pot"]), team["country"]) for team in teams]
#     schedule = run_draw(teams)
#     for team, matches in schedule.items():
#         assert verify_schedule(team, matches)