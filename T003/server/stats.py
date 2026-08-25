import json

from T003.config.config_loader import load_config

config = load_config()

LOG_FILE = config["log_file"]

def read_logs(log_file):

    with open(log_file, "r") as f:
        return json.load(f)


def successful_requests(logs):
    count = 0

    for log in logs:
        if log["result"] == "Success":
            count += 1

    return count


def failed_requests(logs):
    count = 0

    for log in logs:
        if log["result"] == "Failure":
            count += 1

    return count


def average_execution_time(logs):
    if len(logs) == 0:
        return 0

    total = 0

    for log in logs:
        total += log["execution_time"]

    return total / len(logs)


def most_used_command(logs):
    commands = {}

    for log in logs:
        command = log["command"]

        if command not in commands:
            commands[command] = 1
        else:
            commands[command] = commands[command] + 1

    most_used = "-"
    highest = 0

    for command in commands:
        if commands[command] > highest:
            highest = commands[command]
            most_used = command

    return most_used

logs = read_logs(config["log_file"])

print("Most used command:", most_used_command(logs))
print("Average execution time:", average_execution_time(logs))
print("Successful requests:", successful_requests(logs))
print("Failed requests:", failed_requests(logs))