
order_dir_types = ["BUY", "SELL"]
order_status_types = ["LIVE", "SUBMITTED", "FILLED", "CANCELLED", "CANCELLABLE"]

class Order:
    def __init__(self, id, dir, status, price=None, size=50):
        self.id = id
        self.dir = dir
        self.status = status
        self.price = price
        self.size = size

    @property         # decorate the getter method
    def id(self): 
        return self._id

    @id.setter        # decorate the setter method
    # id must be non-negative integer
    def id(self, x):
        try:
            float(x)
            if x == int(x) and x >= 0:
                self._id = x
            else:
                raise ValueError(f"id must be non-negative integer")
        except ValueError:
            raise ValueError(f"id must be non-negative integer")
    

    @property           
    def dir(self): 
        return self._dir

    @dir.setter      
    # dir must be be either 'BUY' or 'SELL'    
    def dir(self, s):
        if s not in order_dir_types:
            raise ValueError(f"status must be 1 of {order_dir_types}.")
        else:
            self._dir = s  


    @property         
    def status(self): 
        return self._status
    
    @status.setter
    # status must be in the allowable list of words     
    def status(self, s):
        if s not in order_status_types:
            raise ValueError(f"status must be 1 of {order_status_types}.")
        else:
            self._status = s  


    @property
    def price(self, x):
        return self._price

    @price.setter
    # price must be positive number
    def price(self, x):
        try:
            float(x)
            if float(x) <= 0:
                raise ValueError(f"price must be positive")
            self._price = x
        except ValueError:
            raise ValueError(f"price must be (positive) float")




    def __repr__(self):
        return f"<Order {self.id}, {self.dir}, {self.status}>"

    def __str__(self):
        return f"Order ID {self.id}. Direction: {self.dir}. Status: {self.status}"

