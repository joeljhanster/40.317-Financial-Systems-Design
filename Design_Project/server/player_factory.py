from singleton import Singleton
from player import Player

class PlayerFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.curr_id = 0
        self.players = []
    
    def add_player(self, family_name, given_name):
        player = Player(self.curr_id, family_name, given_name)
        self.players.append(player)
        self.curr_id += 1
        return player
    
    def get_player(self, player_id):
        for player in self.players:
            if str(player.id) == str(player_id):
                return player
        return None
    


