import json

def load_config():
    with open("T003/config.json", "r") as f:     
          return json.load(f)