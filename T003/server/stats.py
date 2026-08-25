import json

LOG_FILE = "logs/server_log.json"


def read_logs():
    logs = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            logs.append(json.loads(line))

    return logs


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

        if command in commands:
            commands[command] += 1
        else:
            commands[command] = 1

    if len(commands) == 0:
        return "-"

    return max(commands, key=commands.get)

logs = read_logs()

print("Most used command:", most_used_command(logs))
print("Average execution time:", average_execution_time(logs))
print("Successful requests:", successful_requests(logs))
print("Failed requests:", failed_requests(logs))