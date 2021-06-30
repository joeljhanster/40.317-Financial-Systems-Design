
from order import Order
from datetime import datetime

trade_status_types = ["MATCHED", "UNMATCHED", "ERROR"]

class Trade:
    def __init__(self, id, price, size, buy_order=None, sell_order=None, status="UNMATCHED"):
        self.id = id
        self.buy_order = buy_order
        self.sell_order = sell_order
        self.status = status
        self.price = price
        self.size = size
        self.submitted_time = datetime.now()

    @property
    def id(self):
        return self._id
    
    @id.setter
    # id must be non-negative integer
    def id(self, x):
        if isinstance(x, int):
            if x >= 0:
                self._id = x
            else:
                raise ValueError("id must be non-negative integer")
        else:
            raise TypeError("id must be of Integer type")

    @property             
    def buy_order(self): 
        return self._buy_order

    @buy_order.setter          
    # buy_order must be of Order instantiation
    def buy_order(self, o):
        if o is None:
            self._buy_order = None
        elif isinstance(o, Order):
            self._buy_order = o
        else:
            raise TypeError(f"attr buy_order must be of {Order}")

    @property        
    def sell_order(self): 
        return self._sell_order

    @sell_order.setter     
    # sell_order can be of None, or of Order instantiation
    def sell_order(self, o):
        if o is None:
            self._sell_order = None
        elif isinstance(o, Order) or o == None:
            self._sell_order = o
        else:
            raise TypeError(f"attr sell_order must be either None, or of {Order}")

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, s):
        if s not in trade_status_types:
            raise ValueError(f"status {s} must be 1 of {trade_status_types}.")
        else:
            self._status = s
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    # price must be positive number
    def price(self, x):
        if x is None:
            raise ValueError("price must not be None")
        try:
            float(x)
            if float(x) <= 0:
                raise ValueError("price must be positive")
            self._price = x
        except ValueError:
            raise ValueError(f"price must be (positive) float")
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    # size must be positive integer
    def size(self, x):
        if isinstance(x, int):
            if x > 0:
                self._size = x
            else:
                raise ValueError(f"size must be positive")
        else:
            raise TypeError(f"size must be (positive) integer")

    @property
    def submitted_time(self):
        return self._submitted_time
    
    @submitted_time.setter
    # submitted_time must be datetime object
    def submitted_time(self, x):
        if isinstance(x, datetime):
            self._submitted_time = x
        else:
            raise TypeError(f"submitted_time must be of Datetime type")
    
    def __str__(self):
        return f"Trade ID {self.id}. Price {self.price}. Size {self.size}. Buy {self.buy_order}. Sell {self.sell_order}"