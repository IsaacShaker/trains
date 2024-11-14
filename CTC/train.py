from collections import deque
from CTC.mapReader import MapReader
import pandas as pd

class Train:

    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.current_authority = 0.00
        self.suggested_speed = 0.00
        self.current_block = 0
        self.first_arrival = 0
        self.dispatch_time = 0
        self.on_track = False
        self.route_authorities = deque()
        self.station_stops = []
        self.myReader = MapReader()

    def set_name(self, new_name):
        self.name = new_name

    def set_line(self, new_line):
        self.line = new_line

    def set_current_authority(self, new_auth):
        self.current_authority = new_auth

    def set_suggested_speed(self, new_speed):
        self.suggested_speed = new_speed

    def set_first_arrival_time(self, time):
        self.first_arrival = time
        self.calculate_dispatch_time(self.first_arrival)
    
    def calculate_dispatch_time(self, arrival_time):
        file_path = 'C:/Trains C/trains/Train Paths.xlsx'
        df = pd.read_excel(file_path, sheet_name='Green Line')

        time_sum = 0
        for index, row in df.iterrows():
            if row['Infrastructure'] == self.station_stops[0]:
                time_sum += row['seconds to traverse block']
                break
            else:
                time_sum += row['seconds to traverse block']
        time_sum = int(time_sum)
        dispatch_time = self.first_arrival - time_sum
        if (dispatch_time < 21600):
            self.dispatch_time = 21600
        else:
            self.dispatch_time = dispatch_time
                    

    def set_current_block(self, new_block):
        self.current_block = new_block

    def dispatched(self):
        self.on_track = True

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
            authority_list = self.calculate_green_authorities(self.name)
            for authority in authority_list:
                self.route_authorities.append(authority)
        #else (self.line == 'Red'):
            #authorities_list = self.myReader.calculate_red_authorities(self.name)
            #for authority in authorities_list:
                #self.route_authorities.append(authority)
    
    def get_authority_from_map(self):
        #self.route_authorities.clear()
        if self.line == 'Green':
            authority_list = self.myReader.calculate_green_authorities(self.station_stops)
            for authority in authority_list:
                self.route_authorities.append(authority)
        #else:
            #authority_list = self.calculate_red_authorites(self.station_stops)
            #for authority in authority_list:
                #self.route_authorities.append(authority)

        self.set_current_authority(self.route_authorities[0])

    def updateAuthority(self):
        # Remove the previous authority
        old_authority = self.route_authorities.popleft()

        # Set authority to next station
        if self.route_authorities:
            self.set_current_authority(self.route_authorities[0])

    def add_authority(self, new_authority):
        self.route_authorities.append(new_authority)
    
    def add_stop(self, station):
        station = "STATION; "+station
        self.station_stops.append(station)

    def get_station_stops(self):
        return self.station_stops

    def find_current_block(self, occupied_blocks):
        pass
        