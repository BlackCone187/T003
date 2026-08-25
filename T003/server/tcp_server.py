from socket import *
import threading
import subprocess
import time
from datetime import datetime

from server.logger import log_request
from server.command_execute import ping
from server.command_execute import tracert
from server.command_execute import nslookup
from server.command_execute import ipconfig
from server.command_execute import route
from server.command_execute import arp
from server.command_execute import netstat
    
from config.config_loader import load_config

config = load_config()

SERVER_PORT = config["tcp_port"]



def handle_client(connection_socket, client_address):

    message = connection_socket.recv(1024).decode()

    print("Client sent:", message)

    parts = message.split()

    allowedCommands = ["ping", "tracert", "nslookup", "ipconfig", "route", "arp", "netstat", "exit"]

    if not parts:
        print("Empty command")
        connection_socket.close()
        return

    command = parts[0]

    parameter = parts[1] if len(parts) > 1 else ""

    if command not in allowedCommands:
        print("Command not allowed")
        connection_socket.close()
        return

    if command == "exit":
        connection_socket.close()
        return

    if command in ["ping", "tracert", "nslookup"]:

        if len(parts) < 2:
            print("Missing parameter")
            connection_socket.close()
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
    }, config["log_file"])

    response = (
        f"Command: {command} | Status: {status} | "
        f"Execution Time: {execution_time:.4f} seconds | "
        f"Timestamp: {timestamp} | Output: {result.stdout}"
    )

    connection_socket.send(response.encode())

    connection_socket.close()


def ping(host):
    result = subprocess.run(
        ["ping", host],
        capture_output=True,
        text=True
    )
    return result


def tracert(host):
    result = subprocess.run(
        ["tracert", host],
        capture_output=True,
        text=True
    )
    return result


def nslookup(host):
    result = subprocess.run(
        ["nslookup", host],
        capture_output=True,
        text=True
    )
    return result


def ipconfig():
    result = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True
    )
    return result


def route():
    result = subprocess.run(
        ["route"],
        capture_output=True,
        text=True
    )
    return result


def arp():
    result = subprocess.run(
        ["arp"],
        capture_output=True,
        text=True
    )
    return result


def netstat():
    result = subprocess.run(
        ["netstat"],
        capture_output=True,
        text=True
    )
    return result


def start_tcp_server():

    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(('', SERVER_PORT))

    server_socket.listen(config["max_clients"])

    print("TCP Server is listening...")

    while True:

        connection_socket, client_address = server_socket.accept()

        print("Client connected:", client_address)

        thread = threading.Thread(
            target=handle_client,
            args=(connection_socket, client_address)
        )

        thread.start()