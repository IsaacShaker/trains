import pandas as pd
from CTC.train import Train

class ScheduleReader(Train):

    def __init__(self):
        self.intermediate_routes = []

    def get_green_routes(self, file_path):
    # Open the track layout
        df = pd.read_excel(file_path)
        
        # Create the required number of trains necessary for the schedule
        greenTrains = []
        for column in df.columns:
            column = str(column)
            if column[:5] == 'Train':
                column = Train(column, 'Green')
                greenTrains.append(column)

        for i in range (len(greenTrains)):
            for index, rows in df.iterrows():
                # add stations stop
                i.station_stops.append(rows)
            print(i.name, 'has stops', i.station_stops)

        return greenTrains
    
    def get_red_route(self, train):
        # Open the track layout
        file_path = '' # insert file path hardcoded
        df = pd.read_excel(file_path, sheet_name = 'Red Line')

        # Calculate the authority for the train


        return self.intermediate_routes