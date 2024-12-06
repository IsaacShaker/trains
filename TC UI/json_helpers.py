import os
import json

# Load the JSON data from a file
def load_json(filename='track_model.json'):
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, filename)
    with open(json_file_path, 'r') as file:
        return json.load(file)

# Save the updated JSON data to the file
def save_json(data, filename='track_model.json'):
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, filename)
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)