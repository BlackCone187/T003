import json

def log_request(entry, log_file="logs/server_log.json"):
    with open(log_file, "a") as f:  # append
        f.write(json.dumps(entry) + "\n") # entry: info about the request // dumps: convent from dect -> JSON string