from singleton import Singleton
from trade import Trade

class TradeFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.curr_id = 0
        self.trades = []
    
    def add_unmatched_trade(self, order, price, size):
        dir_type = order.dir
        status = "UNMATCHED"

        if dir_type == "BUY":
            trade = Trade(
                id=self.curr_id,
                price=price,
                size=size,
                buy_order=order,
                sell_order=None,
                status=status
            )
        elif dir_type == "SELL":
            trade = Trade(
                id=self.curr_id,
                price=price,
                size=size,
                buy_order=None,
                sell_order=order,
                status=status
            )
        else:
            raise ValueError('Order type must be either "BUY" or "SELL"')
        
        self.trades.append(trade)
        self.curr_id += 1
        return trade
    
    def get_trade(self, trade_id):
        for trade in self.trades:
            if str(trade.id) == str(trade_id):
                return trade
        return None
    
    # def change_status(self, trade_id, status):
    #     trade = self.get_trade(trade_id)
    #     if trade:
    #         trade.status = status
    
    def change_status(self, trade, status):
        trade.status = status
    
    def match_trade(self, trade, order):
        dir_type = order.dir

        if dir_type == "BUY":
            trade.buy_order = order
        elif dir_type == "SELL":
            trade.sell_order = order