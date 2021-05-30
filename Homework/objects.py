# Class variables and methods for Order and Trade objects

types = ["Buy", "Sell"]
order_status = ["Live", "Submitted", "Filled", "Cancelled", "Cancellable"]
trade_status = ["Unmatched", "Matched", "Error"]

class Order(Object):
    def __init__(self, order_type, status):
        self.order_id = 0   # Every order has an Order ID number. Order IDs are completely unique across all teams, i.e. never re-used
        self.order_type = order_type   # An order has a type, which can be either Buy or Sell
        self.status = status    # An order has a status


class Trade(Object):
    def __init__(self, ours, theirs, status):
        self.order_ours = ours
        self.order_theirs = theirs
        self.status = status