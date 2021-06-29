import unittest
from . import order_factory as order
from .trade import Trade

o1 = order.create_order()
o2 = order.create_order()

class Test(unittest.TestCase):

    def test_successful_Trade_instantiation(self):
        Trade(o1, o2)
        Trade(o1)

if __name__ == '__main__':
    unittest.main()
