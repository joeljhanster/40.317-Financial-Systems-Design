
from order import Order

trade_status_types = ["MATCHED", "UNMATCHED", "ERROR"]

class Trade:

    def __init__(self, our_order, their_order=None):
        self.our_order = our_order
        self.their_order = their_order


    @property                   # decorate the getter method
    def our_order(self): 
        return self._our_order

    @our_order.setter           # decorate the setter method
    # our_order must be of Order instantiation
    def our_order(self, o):
        if isinstance(o, Order):
            self._our_order = o
        else:
            raise TypeError(f"attr our_order must be of {Order}")

    @property        
    def their_order(self): 
        return self._their_order

    @their_order.setter     
    # their_order can be of None, or of Order instantiation
    def their_order(self, o):
        if isinstance(o, Order) or o == None:
            self._their_order = o
        else:
            raise TypeError(f"attr their_order must be either None, or of {Order}")


    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, s):
        if s not in trade_status_types:
            raise ValueError(f"status {s} must be 1 of {trade_status_types}.")
        else:
            self._status = s
    
    