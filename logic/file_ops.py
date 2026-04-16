import json
import os

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def load_json(file):
    if not os.path.exists(file):
        return None
    with open(file, "r") as f:
        return json.load(f)