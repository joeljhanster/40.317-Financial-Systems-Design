
from singleton import Singleton
from order import Order
import random

class OrderFactory:
    __metaclass__ = Singleton

    def __init__(self):
        self.curr_id = 0
        self.orders = []
    
    def create_order(self, id=0, dir=None, status="LIVE", price=None, size=50):
        if dir == None:
            dir = "BUY" if random.random() < 0.5 else "SELL"
        if price == None:
            price = random.randint(90, 110)
        order = Order(self.curr_id, dir, status, price, size)
        self.orders.append(order)
        self.curr_id += 1
        return order

    def create_batch_orders(self, num=8):
        batch_orders = []
        for i in range(num):
            order = self.create_order()
            batch_orders.append(order)
        return batch_orders

    def format_orders(self, orders):
        formatted = ""
        for order in orders:
            formatted += " "
            formatted += repr(order)
            print(formatted)
        return formatted