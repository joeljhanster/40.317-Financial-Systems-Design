
from .order import Order
import random


def create_order(id=0, dir=None, status="LIVE", price=None, size=50):
    if dir == None:
        dir = "BUY" if random.random() < 0.5 else "SELL"
    if price == None:
        price = random.randint(90, 110)
    return Order(id, dir, status, price, size)


def market_open_new_orders(start_id):
    """
    start_id: Integer
    return: List of 8 LIVE Order instances in increasing id from start_id.
    The first 4 Order instances will be BUY.
    The latter 4 Order instances will be SELL.
    """
    raise NotImplementedError
    order_ls       = [ Order(i, 'BUY', 'LIVE', price=random.randint(90, 110)) for i in range(start_id, start_id+4) ]
    order_ls.extend( [ Order(i, 'SELL', 'LIVE', price=random.randint(90, 110)) for i in range(start_id+4, start_id+8)  ] )
    return order_ls

def one_new_order(id, dir=None):
    """
    id: Integer
    dir: Optional arg. 
        If None, then Order return has its dir (BUY/SELL) randomised.
    return: Order object with input id, with status LIVE, and direction dir.
    """
    raise NotImplementedError
    price = random.randint(90, 110)
    if dir == None:
        if random.random() < 0.5:
            return Order(id, 'BUY', 'LIVE', price=price)
        else:
            return Order(id, 'SELL', 'LIVE', price=price)
    else:
        return Order(id, dir, 'LIVE', price=price)