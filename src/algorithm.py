from ..src.datatypes import Team, Match, Pot
import time, random

def run_draw(teams: list[Team]) -> dict[Team, list[Match]]:
    '''
    Runs the draw algorithm to schedule matches for each team.
    Each team should play 8 matches: 4 home and 4 away against teams from different pots and countries.
    '''
    start = time.time()
    schedules = {team: [] for team in teams}
    # Start implementation here
    p1 = set(filter(lambda t: t.pot == Pot.ONE, teams))
    p2 = set(filter(lambda t: t.pot == Pot.TWO, teams))
    p3 = set(filter(lambda t: t.pot == Pot.THREE, teams))
    p4 = set(filter(lambda t: t.pot == Pot.FOUR, teams))
    pots = {
        Pot.ONE: p1,
        Pot.TWO: p2,
        Pot.THREE: p3,
        Pot.FOUR: p4
    }
    for pot, pot_teams in pots.items():
        for team in pot_teams:
            team_filter = lambda t: remove_same_country(team, [t])
            available_p1 = list(filter(team_filter, p1))
            p1_opponents = random.sample(available_p1, 1-len(get_pot_teams(team, schedules[team], Pot.ONE)))
            available_p2 = list(filter(team_filter, p2))
            p2_opponents = random.sample(available_p2, 1-len(get_pot_teams(team, schedules[team], Pot.TWO)))
            available_p3 = list(filter(team_filter, p3))
            p3_opponents = random.sample(available_p3, 1-len(get_pot_teams(team, schedules[team], Pot.THREE)))
            available_p4 = list(filter(team_filter, p4))
            p4_opponents = random.sample(available_p4, 1-len(get_pot_teams(team, schedules[team], Pot.FOUR)))
            opponents = p1_opponents + p2_opponents + p3_opponents + p4_opponents
            for opponent in opponents:
                schedules[team].append(Match(home=team, away=opponent))
                schedules[opponent].append(Match(home=team, away=opponent))
    # End implementation here
    end = time.time()
    print(f"Draw algorithm took {end - start} seconds")
    return schedules

def get_pot_teams(team: Team, schedule: list[Match], pot: Pot) -> set[Team]:
    '''
    Returns the set of teams from the given pot in the schedule.
    '''
    return set(filter(lambda t: t.pot == pot and t != team, [match.home for match in schedule] + [match.away for match in schedule]))

def remove_same_country(team: Team, opponents: list[Team]) -> list[Team]:
    '''
    Filters out opponents that are from the same country or are the same team.
    '''
    return list(filter(lambda t: t.country != team.country, opponents))