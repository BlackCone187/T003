import json
import os

def log_request(data):
    os.makedirs("logs", exist_ok=True)

    log_file = "logs/server_log.json"

    with open(log_file, "a") as f:
        json.dump(data, f)
        f.write("\n")