import unittest
from .order import Order
from . import order_factory as order


class Test(unittest.TestCase):

    def test_successful_Order_instantiation(self):
        Order(7, 'BUY', 'LIVE', 105)
        Order(8, 'SELL', 'CANCELLABLE', 95)

    def test_unsuccessful_Order_instantiation_1(self):
        # 'HOLD' is not a valid status
        try:
            Order(7, 'HOLD', 'LIVE', 105)
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_Order_instantiation_2(self):
        # negative price is invalid
        try:
            Order(7, 'BUY', 'LIVE', -100) 
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_Order_instantiation_3(self):
        # 'abc' (non-numeric string) price is invalid 
        try:
            Order(7, 'BUY', 'LIVE', 'abc') 
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_attr_set_1(self):
        # changing status attr to an illegal value
        x = Order(7, 'BUY', 'LIVE', 105)
        try:
            x.status = 'INVALID_STATUS'
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_attr_set_2(self):
        # changing dir to an illegal value ('SHORT')
        x = Order(7, 'BUY', 'LIVE', 105)
        try:
            x.dir = 'SHORT'
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_attr_set_3(self):
        # 1.5 for id is invalid
        x = Order(0, 'BUY', 'LIVE', 105)
        try:
            Order(1.5, 'BUY', 'LIVE', ) 
            self.assertTrue(0)
        except ValueError:
            pass

    def test_market_open_new_orders(self):
        x = order.market_open_new_orders(1)
        print(x)

    def test_one_new_order(self):
        order.one_new_order(1)
        order.one_new_order(1, 'BUY')

if __name__ == '__main__':
    unittest.main()
