import pandas as pd
from CTC.train import Train

class ScheduleReader(Train):

    def __init__(self):
        self.intermediate_routes = []

    def get_green_routes(self, file_path, num_trains):
    # Open the track layout
        df = pd.read_excel(file_path)
        
        # Create the required number of trains necessary for the schedule
        greenTrains = []
        # Create Train objects for each 'Train' column
        for column in df.columns:
            column = str(column)
            if column[:5] == 'Train':
                new_index = num_trains + len(greenTrains)
                name = "Train "+ str(new_index)
                train = Train(name, 'Green')  # Create a Train object
                greenTrains.append(train)

        # Process each train's data
        for i, train in enumerate(greenTrains):
            # Extract dispatch time from the first row
            train.time_to_dispatch = df.iloc[0, i + 1]  # Get the dispatch time from the first row of the train's column

            # Add station stops from remaining rows
            for index, row in df.iloc[1:].iterrows():  # Skip the first row (dispatch times)
                train.station_stops.append(row[i + 1])  # Append station stops from the train's column

        return greenTrains
    
    def get_red_route(self, train):
        # Open the track layout
        file_path = '' # insert file path hardcoded
        df = pd.read_excel(file_path, sheet_name = 'Red Line')

        # Calculate the authority for the train


        return self.intermediate_routes