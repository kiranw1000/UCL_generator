from ..src.datatypes import Team, Match, Pot, Schedule
from ..src.algorithm import run_draw
import json, pytest

with open("teams.json") as f:
    teams = json.load(f)
teams = [Team(team["name"], Pot(team["pot"]), team["country"]) for team in teams]
schedules = run_draw(teams)

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

def test_match_symmetry():
    '''
    Verifies that if team A is playing team B at home, then team B is playing team A away.
    '''
    for team, schedule in schedules.items():
        for pot, matches in schedule.matches.items():
            for match in matches:
                home_team = match.home
                away_team = match.away
                home_schedule = schedules[home_team]
                away_schedule = schedules[away_team]
                found = False
                for away_pot, away_matches in away_schedule.matches.items():
                    for away_match in away_matches:
                        if away_match.home == away_team and away_match.away == home_team:
                            found = True
                            break
                    if found:
                        break
                assert found, f"Match symmetry failed for {home_team} and {away_team}"

def verify_unique_teams(schedule: Schedule):
    '''
    Verifies that each team is unique in the schedule.
    '''
    teams = set()
    for pot, matches in schedule.matches.items():
        for match in matches:
            opponent = match.home if schedule.team == match.away else match.away
            if opponent in teams:
                return False
            teams.add(opponent)
    return True

def verify_max_2_teams_from_country(schedule: Schedule):
    '''
    Verifies that there are no more than 2 teams from the same country in the schedule.
    '''
    country_counts = {}
    for pot, matches in schedule.matches.items():
        for match in matches:
            if match.home == schedule.team:
                country = match.away.country
            elif match.away == schedule.team:
                country = match.home.country
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1
    for count in country_counts.values():
        if count > 2:
            return False
    return True

@pytest.mark.parametrize("team, schedule", schedules.items())
def test_schedule(team: Team, schedule: Schedule):
    '''
    Verifies that the team is scheduled to play 8 games, 1 home and 1 away from each of 4 pots with each team being different.
    '''
    # Verify that there are 8 unique teams
    assert verify_unique_teams(schedule), "Duplicate teams found in schedule"
    # Verify that there are at most 2 teams from any other given country in a team's schedule
    assert verify_max_2_teams_from_country, "More than 2 teams from one country in schedule"
    home_games = set()
    away_games = set()
    # Verify that each match has different teams from different countries
    for pot, matches in schedule.matches.items():
        assert len(matches) == 2, "Incorrect number of matches in pot"
        for match in matches:
            assert verify_different_countries_match(match), "Teams are from the same country"
            assert verify_different_teams_match(match), "Teams are the same"
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