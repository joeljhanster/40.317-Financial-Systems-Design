from singleton import Singleton
from datetime import timedelta, datetime
from team import Team
from trade import Trade

# Requires elapsed time since open: 00:03:53
# Requires last trade price: 102.0
# Hands out orders to be filled to different teams

class Exchange(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.teams = []
        self.trade_history = []
        self.unmatched_trade = []
        self.error_trade = []
        self.is_open = False
        self.start_time = None

    @property
    def teams(self):
        return self._teams
    
    @teams.setter
    def teams(self, t):
        if isinstance(t, list):
            for team in t:
                if not isinstance(team, Team):
                    raise TypeError("Element in teams list must be of Team type")
            self._teams = t
        else:
            raise TypeError("teams must be of List type")

    @property
    def trade_history(self):
        return self._trade_history

    @trade_history.setter
    def trade_history(self, t):
        if isinstance(t, list):
            for trade in t:
                if not isinstance(trade, Trade):
                    raise TypeError("Element in trade_history list must be of Trade type")
            self._trade_history = t
        else:
            raise TypeError("trade_history must be of List type")
    
    @property
    def unmatched_trade(self):
        return self._unmatched_trade

    @unmatched_trade.setter
    def unmatched_trade(self, t):
        if isinstance(t, list):
            for trade in t:
                if not isinstance(trade, Trade):
                    raise TypeError("Element in unmatched_trade list must be of Trade type")
            self._unmatched_trade = t
        else:
            raise TypeError("unmatched_trade must be of List type")
    
    @property
    def error_trade(self):
        return self._error_trade

    @error_trade.setter
    def error_trade(self, t):
        if isinstance(t, list):
            for trade in t:
                if not isinstance(trade, Trade):
                    raise TypeError("Element in error_trade list must be of Trade type")
            self._error_trade = t
        else:
            raise TypeError("error_trade must be of List type")

    @property
    def is_open(self):
        return self._is_open
    
    @is_open.setter
    def is_open(self, b):
        if isinstance(b, bool):
            self._is_open = b
        else:
            raise TypeError("is_open must be of Boolean type")
    
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, x):
        if x is None:
            self._start_time = None
        elif isinstance(x, datetime):
            self._start_time = x
        else:
            raise TypeError("start_time must be of Datetime type")
