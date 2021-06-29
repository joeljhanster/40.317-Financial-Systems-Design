order_dir_types = ["BUY", "SELL"]
order_status_types = ["LIVE", "SUBMITTED", "FILLED", "CANCELLED", "CANCELLABLE"]

class Order:
    def __init__(self, id, team_id, dir, status, price, size):
        self.id = id
        self.team_id = team_id
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
        except:
            raise ValueError(f"id '{x}' must be numeric (non-negative integer) ")
        if float(x) != int(x):
            raise ValueError(f"id '{x}' must be integer (non-float)")
        elif int(x) < 0:
            raise ValueError(f"if '{x}' must be non-negative")
        else:
            self._id = int(x)
    
    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, x):
        try:
            float(x)
        except:
            raise ValueError(f"id '{x}' must be numeric (non-negative integer) ")
        if float(x) != int(x):
            raise ValueError(f"id '{x}' must be integer (non-float)")
        elif int(x) < 0:
            raise ValueError(f"if '{x}' must be non-negative")
        else:
            self._team_id = int(x)

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
            raise ValueError(f"status {s} must be 1 of {order_status_types}.")
        else:
            self._status = s  

    @property
    def price(self):
        return self._price

    @price.setter
    # price must be positive number
    def price(self, x):
        if x == None:
            raise ValueError(f"price must not be None")
        try:
            float(x)
            if float(x) <= 0:
                raise ValueError(f"price must be positive")
            self._price = x
        except ValueError:
            raise ValueError(f"price must be (positive) float")

    def __repr__(self):
        return f"{self.id}_{self.size}_{self.price}_{self.dir}_{self.status}"
        # return f"(Order: {self.id}, {self.dir}, {self.status}, {self.price})"

    def __str__(self):
        return f"Order ID {self.id}. Direction: {self.dir}. Status: {self.status}"

