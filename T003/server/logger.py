import json

def log_request(entry, log_file="logs/server_log.json"):
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")