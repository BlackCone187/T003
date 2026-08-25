import json
from pathlib import Path


def log_request(data, log_file):

    log_file = Path(__file__).parent.parent / log_file

    with open(log_file, "r") as f:
        logs = json.load(f)

    logs.append(data)

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)