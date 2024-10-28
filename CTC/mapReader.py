import pandas as pd

class MapReader():

    def __init__(self):
        self.route_authorities_list = []

    def calculate_green_authorities(self, stops):
        # Open the track layout
        file_path = 'C:/Trains C/trains/Train Paths.xlsx'
        df = pd.read_excel(file_path, sheet_name='Green Line')
        
        for i in range(len(stops)):
            # Determine the current and next stop
            if i == 0:
                current_stop = 'START'
                next_stop = stops[i]
            else:
                current_stop = stops[i - 1]
                next_stop = stops[i]

            # Find indices for the current and next stops
            current_stop_index = df[df['Infrastructure'] == current_stop].index
            next_stop_index = df[df['Infrastructure'] == next_stop].index

            # Check if indices are found to avoid errors
            if not current_stop_index.empty and not next_stop_index.empty:
                start = current_stop_index[0]
                end = next_stop_index[0]
                # Sum the block lengths from start to end
                authority = df.loc[start:end, 'Block Length (m)'].sum()
                self.route_authorities_list.append(int(authority))
            else:
                print(f"Stop '{current_stop}' or '{next_stop}' not found in the data.")

        # Final addition from the last stop to "END"
        if stops:
            print('going home')
            last_stop = stops[-1]
            last_stop_index = df[df['Infrastructure'] == last_stop].index
            end_index = df[df['Infrastructure'] == 'END'].index

            if not last_stop_index.empty and not end_index.empty:
                start = last_stop_index[0]
                end = end_index[0]
                # Sum the block lengths from the last stop to "END"
                authority = df.loc[start:end, 'Block Length (m)'].sum()
                self.route_authorities_list.append(int(authority))
            else:
                print(f"Stop '{last_stop}' or 'END' not found in the data.")

        return self.route_authorities_list

    
    def calculate_red_authorities(self, routes):
        # Open the track layout
        file_path = '' # insert file path hardcoded
        df = pd.read_excel(file_path, sheet_name = 'Red Line')

        # Calculate the authority for the train


        return self.route_authorities_list