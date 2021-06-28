
from .order import Order
import random

def market_open_new_orders(start_id):
    """
    start_id: Integer
    return: List of 8 LIVE Order instances in increasing id from start_id.
    The first 4 Order instances will be BUY.
    The latter 4 Order instances will be SELL.
    """
    order_ls       = [ Order(i, 'BUY', 'LIVE') for i in range(start_id, start_id+4) ]
    order_ls.append( [ Order(i, 'SELL', 'LIVE') for i in range(start_id+4, start_id+8)  ] )
    return order_ls

def one_new_order(id, dir=None):
    """
    id: Integer
    dir: Optional arg. 
        If None, then Order return has its dir (BUY/SELL) randomised.
    return: Order object with input id, with status LIVE, and direction dir.
    """
    if dir == None:
        if random.random() < 0.5:
            return Order(id, 'BUY', 'LIVE')
        else:
            return Order(id, 'SELL', 'LIVE')
    else:
        return Order(id, dir, 'LIVE')