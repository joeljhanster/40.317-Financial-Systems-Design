from player import Player
from order import Order

class Team:
    def __init__(self, id, name, players, orders=[]):
        self.id = id
        self.name = name
        self.players = players
        self.orders = orders
        self.pnl = 0.0
    
    @property
    def id(self):
        return self._id

    @id.setter
    # id must be non-negative integer
    def id(self, x):
        try:
            float(x)
            if x == int(x) and x >= 0:
                self._id = x
            else:
                raise ValueError(f"id must be non-negative integer")
        except ValueError:
            raise ValueError(f"id must be non-negative integer")
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, s):
        self._name = s

    @property
    def players(self):
        return self._players
    
    @id.setter
    def players(self, p):
        if isinstance(p, list):
            for player in p:
                if not isinstance(player, Player):
                    raise TypeError(f"Element in players list must be of Player type")
            self._players = p
        else:
            raise TypeError(f"Players must be of List type")
    
    @property
    def orders(self):
        return self._orders
    
    @orders.setter
    def orders(self, o):
        if isinstance(o, list):
            for order in o:
                if not isinstance(order, Order):
                    raise TypeError(f"Element in orders list must be of Order type")
            self._orders = o
        else:
            raise TypeError(f"Orders must be of List type")
    
    @property
    def pnl(self):
        return self._pnl
    
    @pnl.setter
    def pnl(self, x):
        try:
            x = float(x)
            self._pnl = x
        except ValueError:
            raise ValueError(f"pnl must be a Float type")