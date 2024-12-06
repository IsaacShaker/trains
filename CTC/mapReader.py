import pandas as pd
from collections import deque
import os

class MapReader():

    def __init__(self):
        self.route_authorities_list = []

    def calculate_green_authorities(self, stops):
        # Open the train path file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'Train Paths.xlsx')
        print('file path is ', file_path)
        df = pd.read_excel(file_path, sheet_name='Green Line')
        df['Block Length (m)'] = df['Block Length (m)'].astype(float)
        
        for i in range(len(stops) + 1):
            # Determine the current and next stop
            print('i =', i)
            if i == 0:
                current_stop = 'START'
                next_stop = stops[i]
            elif i == len(stops):
                current_stop = stops[i - 1]
                next_stop = 'END'
            else:
                current_stop = stops[i - 1]
                next_stop = stops[i]
            print('current stop = ', current_stop)
            print('next stop = ', next_stop)
            # Find indices for the current and next stops
            current_stop_index = df[df['Infrastructure'] == current_stop].index
            print('current index =', current_stop_index)
            next_stop_index = df[df['Infrastructure'] == next_stop].index
            print('current index =', next_stop_index)

            authority = 0.00
            # Check if indices are found to avoid errors
            if not current_stop_index.empty and not next_stop_index.empty:
                if i == 0:
                    print('adding authority to the yard')
                    start = current_stop_index[0]
                    end = next_stop_index[0]
                    print('START = ', start)
                    print('END =', end)
                    # Sum the block lengths from start to end
                    authority = df.loc[start:end - 1, 'Block Length (m)'].sum()
                    authority += df.loc[end, 'Block Length (m)']/2 + 13 + 10
                    self.route_authorities_list.append(float(authority))
                else:
                    print('adding authority to pioneer')
                    start = current_stop_index[0]
                    end = next_stop_index[0]
                    # Sum the block lengths from start to end
                    authority = df.loc[start, 'Block Length (m)']/2  - 13
                    authority += df.loc[start + 1:end, 'Block Length (m)'].sum()
                    self.route_authorities_list.append(float(authority))
            else:
                print(f"Stop '{current_stop}' or '{next_stop}' not found in the data.")
            print('---------------------------------------------------')
        return self.route_authorities_list

    
    def calculate_red_authorities(self, routes):
        # Open the track layout
        file_path = '' # insert file path hardcoded
        df = pd.read_excel(file_path, sheet_name = 'Red Line')

        # Calculate the authority for the train


        return self.route_authorities_list