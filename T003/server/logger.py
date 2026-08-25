import json
import os

def log_request(data, log_file):
    os.makedirs("logs", exist_ok=True)

    with open(log_file, "a") as f:
        json.dump(data, f)
        f.write("\n")