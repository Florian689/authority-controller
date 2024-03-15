import json
import os

def read_voters():
    file_path = os.path.join('/app', 'data', 'voters_registry.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_voters(data):
    file_path = os.path.join('/app', 'data', 'voters_registry.json')
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)