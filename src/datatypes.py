from enum import Enum


class Pot(Enum):
    '''
    Enumeration for the different pots in the draw.
    '''
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    
class Team():
    '''
    Represents a team in the draw.
    '''
    def __init__(self, name:str, pot: Pot, country: str, ):
        self.pot = pot
        self.country = country
        self.name = name
        
    def __eq__(self, value):
        if not isinstance(value, Team):
            return NotImplemented
        return self.name == value.name and self.pot == value.pot and self.country == value.country
    
    def __hash__(self):
        return hash((self.name, self.pot, self.country))
    
    def __repr__(self):
        return f"Team(name={self.name}, pot={self.pot}, country={self.country})"

class Match():
    '''
    Represents a match between two teams with one being the home team and the other being the away team.
    '''
    def __init__(self, home: Team, away: Team):
        self.home = home
        self.away = away

    def __eq__(self, value):
        if not isinstance(value, Match):
            return NotImplemented
        return self.home == value.home and self.away == value.away
    
    def __hash__(self):
        return hash((self.home, self.away))
    
    def __repr__(self):
        return f"Match(home={self.home}, away={self.away})"

class Schedule():
    '''
    Represents the schedule for a team.
    '''
    def __init__(self, team: Team):
        self.team = team
        self.matches = {p: [] for p in Pot}
        self.opponents = []

    def add_match(self, match: Match):
        if match.home == self.team:
            self.matches[match.away.pot].append(match)
            self.opponents.append(match.away)
        elif match.away == self.team:
            self.matches[match.home.pot].append(match)
            self.opponents.append(match.home)

    def __repr__(self):
        ret = f"Schedule for {self.team.name}: \n"
        for pot, matches in self.matches.items():
            if matches:
                ret += f"  Pot {pot}:\n"
            for match in matches:
                ret += f"    {match.home.name+'(A)' if match.away == self.team else match.away.name+'(H)'}\n"
        return ret
    
    def __len__(self):
        return sum(len(matches) for matches in self.matches.values())
