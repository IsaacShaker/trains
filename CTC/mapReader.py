import pandas as pd

class mapReader():

    def __init__(self):
        self.route_authorities_list = []

    def calculate_green_authorities(self, routes):
        # Open the track layout
        file_path = '' # insert file path hardcoded
        df = pd.read_excel(file_path, sheet_name = 'Green Line')

        # Calculate the authority for the train


        return self.route_authorities_list
    
    def calculate_red_authorities(self, routes):
        # Open the track layout
        file_path = '' # insert file path hardcoded
        df = pd.read_excel(file_path, sheet_name = 'Red Line')

        # Calculate the authority for the train


        return self.route_authorities_list