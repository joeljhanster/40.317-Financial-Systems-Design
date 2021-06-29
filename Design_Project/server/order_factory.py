
from singleton import Singleton
from order import Order
import random

class OrderFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.curr_id = 0
        self.orders = []
    
    def create_order(self, team_id, dir=None, status="LIVE", price=None, size=50):
        if dir == None:
            dir = "BUY" if random.random() < 0.5 else "SELL"
        if price == None:
            price = random.randint(90, 110)
        order = Order(self.curr_id, team_id, dir, status, price, size)
        self.orders.append(order)
        self.curr_id += 1
        return order

# def create_order(id=0, team_id=0, dir=None, status="LIVE", price=None, size=50):
#     if dir == None:
#         dir = "BUY" if random.random() < 0.5 else "SELL"
#     if price == None:
#         price = random.randint(90, 110)
#     return Order(id, team_id, dir, status, price, size)

    def create_batch_orders(self, team_id, num=8):
        batch_orders = []
        for i in range(num):
            order = self.create_order(team_id)
            batch_orders.append(order)
        return batch_orders

    def format_orders(self, orders):
        formatted = ""
        for order in orders:
            formatted += " "
            formatted += repr(order)
        return formatted