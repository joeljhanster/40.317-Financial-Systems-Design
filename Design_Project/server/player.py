class Player:
    def __init__(self, id, family_name, given_name):
        self.id = id
        self.family_name = family_name
        self.given_name = given_name
    
    @property
    def id(self):
        return self._id

    @id.setter
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
    def family_name(self):
        return self._family_name
    
    @family_name.setter
    def family_name(self, s):
        self._family_name = s
    
    @property
    def given_name(self):
        return self._given_name
    
    @given_name.setter
    def given_name(self, s):
        self._given_name = s
    
    def __repr__(self):
        return f"Player: {self.id}, {self.family_name}, {self.given_name}"

    def __str__(self):
        return f"Player ID {self.id}. Family Name: {self.family_name}. Given Name: {self.given_name}"
    