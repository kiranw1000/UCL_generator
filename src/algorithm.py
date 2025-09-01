from ..src.datatypes import Team, Match, Pot, Schedule
import time, random

random.seed(42)

def run_draw(teams: list[Team]) -> dict[Team, list[Match]]:
    '''
    Runs the draw algorithm to schedule matches for each team.
    Each team should play 8 matches: 4 home and 4 away against teams from different pots and countries.
    '''
    start = time.time()
    schedules = {team: Schedule(team) for team in teams}
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
    opp_dict = {p:{"home":[], "away":[]} for p in pots.keys()}
    # Create lists of teams by what pot they are in and if they need each of a home and away match
    for team in teams:
        for p in list(Pot):
            opp_dict[p]["home"].append(team)
            opp_dict[p]["away"].append(team)
    for pot, pot_teams in pots.items():
        for team in pot_teams:
            for pot_to_choose in list(Pot):
                print(pot_to_choose)
                scheduled_pot_teams = schedules[team].matches[pot_to_choose]
                home = True if len(scheduled_pot_teams) == 0 else not scheduled_pot_teams[-1].home == team
                for _ in range(2-len(scheduled_pot_teams)):
                    available_opps = opp_dict[team.pot]["home" if not home else "away"]
                    available_opps = get_available_by_pot(schedules[team], pot_to_choose, available_opps)
                    chosen_team = random.choice(available_opps) if available_opps else None
                    try:
                        # print(chosen_team)
                        home_team = team if home else chosen_team
                        away_team = chosen_team if home else team
                        created_match = Match(home=home_team, away=away_team)
                        schedules[team].add_match(created_match)
                        schedules[chosen_team].add_match(created_match)
                        try:
                            opp_dict[team.pot]["home" if not home else "away"].remove(chosen_team)
                        except ValueError:
                            msg = f"Could not remove {chosen_team} from {opp_dict[team.pot]['home' if not home else 'away']}"
                            raise ValueError(msg)
                        try:
                            opp_dict[pot_to_choose]["home" if home else "away"].remove(team)
                        except ValueError:
                            msg = f"Could not remove {team} from {opp_dict[pot_to_choose]['home' if home else 'away']}"
                            raise ValueError(msg)
                        home = not home
                    except:
                        print(f"Could not schedule match for {team} from pot {pot} against pot {pot_to_choose}")
                # print(schedules[team])
    # End implementation here
    end = time.time()
    print(f"Draw algorithm took {end - start} seconds")
    print("Generated schedules:")
    for team, schedule in schedules.items():
        print(f"  {team}: {len(schedule)} matches")
        print(schedule)
    return schedules

def get_pot_teams(team: Team, schedule: Schedule, pot: Pot) -> set[Team]:
    '''
    Returns the set of teams from the given pot in the schedule.
    '''
    return set(filter(lambda t: t.pot == pot and t != team, [match.home for match in schedule.matches[pot]] + [match.away for match in schedule.matches[pot]]))

def remove_same_country(team: Team, opponents: list[Team]) -> list[Team]:
    '''
    Filters out opponents that are from the same country or are the same team.
    '''
    return list(filter(lambda t: t.country != team.country, opponents))

def get_available_by_pot(schedule: Schedule, pot: Pot, teams: list[Team]) -> list[Team]:
    '''
    Returns a list of teams from the given pot that are available to play.
    '''
    return list(filter(lambda t: t not in schedule.opponents and t.pot == pot, remove_same_country(schedule.team, teams)))

def is_available(team: Team, schedule:list[Match], home: bool, pot: Pot) -> bool:
    '''
    Checks if a team is available to play a match at home or away against a team from the given pot.
    '''
    if len(schedule) >= 8:
        return False
    if home:
        home_matches = list(filter(lambda m: m.home == team and m.away.pot == pot, schedule))
        return len(home_matches) == 0
    else:
        away_matches = list(filter(lambda m: m.away == team and m.home.pot == pot, schedule))
        return len(away_matches) == 0
