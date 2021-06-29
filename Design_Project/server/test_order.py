import unittest
from .order import Order
from . import order_factory as order

class Test(unittest.TestCase):

    def test_successful_Order_instantiation(self):
        Order(7, 1, 'BUY', 'LIVE', 105, 50)
        Order(8, 1, 'SELL', 'CANCELLABLE', 95, 50)

    def test_unsuccessful_Order_instantiation_1(self):
        # 'HOLD' is not a valid status
        try:
            Order(7, 1, 'HOLD', 'LIVE', 105, 50)
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_Order_instantiation_2(self):
        # negative price is invalid
        try:
            Order(7, 1, 'BUY', 'LIVE', -100, 50) 
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_Order_instantiation_3(self):
        # 'abc' (non-numeric string) price is invalid 
        try:
            Order(7, 1, 'BUY', 'LIVE', 'abc', 50) 
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_attr_set_1(self):
        # changing status attr to an illegal value
        x = Order(7, 1, 'BUY', 'LIVE', 105, 50)
        try:
            x.status = 'INVALID_STATUS'
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_attr_set_2(self):
        # changing dir to an illegal value ('SHORT')
        o = Order(7, 1, 'BUY', 'LIVE', 105, 50)
        try:
            o.dir = 'SHORT'
            self.assertTrue(0)
        except ValueError:
            pass

    def test_unsuccessful_attr_set_3(self):
        # test for invalid ids
        invalid_id = [-3, 1.50, 'sus']
        for x in invalid_id:
            o = Order(0, 1, 'BUY', 'LIVE', 105, 50)
            try:
                o.id = x # setting id to invalid value
                print(f"fail to catch invalid id: {x}")
                self.assertTrue(0)
            except ValueError:
                pass

    def test_create_order(self):
        # test Order factory method
        order.create_order()
        order.create_order(id=1001)
        order.create_order(id=1001, team_id=2, dir='BUY')

if __name__ == '__main__':
    unittest.main()
