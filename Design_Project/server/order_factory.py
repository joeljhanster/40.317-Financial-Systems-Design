
from .order import Order
import random


def create_order(id=0, team_id=0, dir=None, status="LIVE", price=None, size=50):
    if dir == None:
        dir = "BUY" if random.random() < 0.5 else "SELL"
    if price == None:
        price = random.randint(90, 110)
    return Order(id, team_id, dir, status, price, size)

