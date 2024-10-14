import pandas as pd

class Train:

    def __init__(self, name, line, destination, arrival_time):
        self.name = name
        self.line = line
        self.destination = destination
        self.authority = 0
        self.suggested_speed = 0
        self.arrival_time = arrival_time
        self.on_track = False
        self.current_block = ()

    def setName(self, new_name):
        self.name = new_name

    def setLine(self, new_line):
        self.line = new_line

    def setDestination(self, new_destination):
        self.destination = new_destination

    def setAuthority(self, new_auth):
        self.authority = new_auth

    def setSuggestedSpeed(self, new_speed):
        self.suggested_speed = new_speed

    def setArrivalTime(self, new_time):
        self.arrival_time = new_time

    def setStatus(self, status):
        self.status = status

    def calcAuthority(self, station):
        # Open the track layout
        file_path = 'C:/Trains C/trains/Track Layout & Vehicle Data vF5.xlsx'
        df = pd.read_excel(file_path, sheet_name = 'Blue Line')

        # Calculate the authority for the train
        