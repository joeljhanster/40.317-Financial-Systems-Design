from singleton import Singleton
from team import Team

class TeamFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.curr_id = 0
        self.teams = []
    
    def add_team(self, team_name, players, orders=[], trades=[]):
        team = Team(self.curr_id, team_name, players, orders, trades)
        self.teams.append(team)
        self.curr_id += 1
        return team
    
    def get_team(self, team_id):
        for team in self.teams:
            if str(team.id) == str(team_id):
                return team
        return None

    def add_orders(self, team_id, orders):
        team = self.get_team(team_id)
        team.orders = orders

    def get_live_orders(self, team_id):
        # return list of orders belonging to a specified team
        team = self.get_team(team_id)

        if team is not None:
            orders = team.orders
            return orders
        return None

    def get_team_trades_counts(self, team_id):
        # return list of 3 integers, where each integer represents no. of trades of each of the 3 possible status.
        # TODO
        return [5, 3, 0]
