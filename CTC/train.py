from mapReader import mapReader
from collections import deque

class Train:

    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.current_authority = 0
        self.suggested_speed = 0
        self.current_block = 0
        self.route_authorities = deque()

    def set_name(self, new_name):
        self.name = new_name

    def set_line(self, new_line):
        self.line = new_line

    def set_current_authority(self, new_auth):
        self.current_authority = new_auth

    def set_suggested_speed(self, new_speed):
        self.suggested_speed = new_speed

    def set_current_block(self, new_block):
        self.current_block = new_block

    def get_authority(self):
        return self.current_authority
    
    def get_suggested_speed(self):
        return self.suggested_speed
    
    def get_suggested_speed_for_wayside(self, hazard):
        if hazard == True:
            return 0
        else:
            return self.suggested_speed

    def get_route_from_schedule(self):
        if (self.line == 'Green'):
            authorities_list = self.calculate_green_authorities(self.name)
            for authority in authorities_list:
                self.route_authorities.append(authority)
        #elif (self.line == 'Red'):
            #authorities_list = self.myReader.calculate_red_authorities(self.name)
            #for authority in authorities_list:
                #self.route_authorities.append(authority)
    
    def get_authority_from_map(self):
        pass

    def updateAuthority(self):
        # Remove the previous authority
        old_authority = self.route_authorities.popleft()

        # Set authority to next station
        if self.route_authorities:
            self.set_current_authority(self.route_authorities[0])

    def add_authority(self, new_authority):
        self.route_authorities.append(new_authority)

    def find_current_block(self, occupied_blocks):
        pass
        