from collections import deque

class Station():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.authorities = deque()

    def get_name(self):
        return self.name
    
    def get_location(self):
        return self.location

    def add_authority(self, auth):
        self.authorities.append(auth)

    def pop_authority(self):
        if (self.authorities.count() > 0):
            return self.authorities.popleft()
        else:
            print("No authority left in station!")
    
