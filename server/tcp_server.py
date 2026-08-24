from socket import *
import threading
import subprocess
import time
from datetime import datetime

SERVER_PORT = 5780

server_socket = socket(AF_INET, SOCK_STREAM)#make tcp socket that use IPv4

server_socket.bind(('', SERVER_PORT))# link a socket with port number

server_socket.listen(5)


def handle_client(connection_socket):
    message = connection_socket.recv(1024).decode()

    print("Client sent:", message)

    parts = message.split()


    allowedCommands = ["ping", "tracert", "nslookup", "ipconfig", "route", "arp", "netstat", "exit"]

    if not parts:
        print("Empty command")
        return

    command = parts[0]

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

    response = (f"Command: {command} | Status: {status} | Execution Time: {execution_time:.4f} "
                f"seconds | Timestamp: {timestamp} | Output: {result.stdout}")
    connection_socket.send(response.encode())

    connection_socket.close()


#----------------------------------------------------------------------------------------
def ping(host): # check if we can connect with server and return the RTT
    result = subprocess.run(["ping", host], capture_output=True,text=True)
    return result

def tracert(host): # trace the path(hops) that the packets pass through it
    result = subprocess.run(["tracert", host], capture_output=True,text=True)
    return result

def nslookup(host):#asks a DNS server for the IP address associated with a domain name
    result = subprocess.run(["nslookup", host], capture_output=True,text=True)
    return result

def ipconfig():#show the info of the network on ur device like ip address,dns, and default gateway
    result = subprocess.run(["ipconfig"], capture_output=True,text=True)
    return result

def route():#show a routing table that the sender device take it as evidence to arrived to the destination
    result = subprocess.run(["route"], capture_output=True,text=True)
    return result

def arp():#showing the relation b/t ip address and mac address that are exist in the arp chach
    # (to know the mac for the destination device)
    result = subprocess.run(["arp"], capture_output=True,text=True)
    return result

def netstat():#showing the current connection server and info about tcp or udp
    result = subprocess.run(["netstat"], capture_output=True,text=True)
    return result
#----------------------------------------------------------------------------------------

print("Server is listening...")

while True:
    connection_socket, client_address = server_socket.accept()

    print("Client connected:", client_address)#client_address==>(IP address, port)

    thread = threading.Thread(
        target=handle_client,
        args=(connection_socket,)
    )

    thread.start()