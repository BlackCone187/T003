import time
from datetime import datetime

from command_execute import ping
from command_execute import tracert
from command_execute import nslookup
from command_execute import ipconfig
from command_execute import route
from command_execute import arp
from command_execute import netstat

from logger import log_request


def handle_client(connection_socket, client_address):
    message = connection_socket.recv(1024).decode()

    print("Client sent:", message)

    parts = message.split()

    allowedCommands = ["ping", "tracert", "nslookup", "ipconfig", "route", "arp", "netstat", "exit"]

    if not parts:
        print("Empty command")
        return

    command = parts[0]
    parameter = parts[1] if len(parts) > 1 else ""

    if command not in allowedCommands:
        print("Command not allowed")
        return

    if command == "exit":
        connection_socket.close()
        return

    if command in ["ping", "tracert", "nslookup"]:
        if len(parts) < 2:
            print("Missing parameter")
            return
        parameter = parts[1]

    print("Command allowed")

    start_time = time.time()

    timestamp = datetime.now()

    if command == "ping":
        result = ping(parts[1])

    elif command == "tracert":
        result = tracert(parts[1])

    elif command == "nslookup":
        result = nslookup(parts[1])

    elif command == "ipconfig":
        result = ipconfig()

    elif command == "route":
        result = route()

    elif command == "arp":
        result = arp()

    elif command == "netstat":
        result = netstat()

    if result.returncode == 0:
        status = "Success"
    else:
        status = "Failure"

    end_time = time.time()
    execution_time = end_time - start_time

    log_request({
        "timestamp": str(timestamp),
        "client_ip": client_address[0],
        "client_port": client_address[1],
        "command": command,
        "parameter": parameter,
        "execution_time": execution_time,
        "result": status
    })

    response = (f"Command: {command} | Status: {status} | Execution Time: {execution_time:.4f} "
                f"seconds | Timestamp: {timestamp} | Output: {result.stdout}")

    connection_socket.send(response.encode())

    connection_socket.close()