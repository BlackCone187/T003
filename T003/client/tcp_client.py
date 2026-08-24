from socket import *

SERVER_NAME = "localhost"
SERVER_PORT = 5462

while True:

    choice = input("""
========================
Network Diagnostic System
========================
1. Ping Host
2. Trace Route
3. DNS Lookup
4. IP Configuration
5. Routing Table
6. ARP Table
7. Active TCP Connections
8. Exit
Select: """)

    if choice == "1":
        command = "ping"

    elif choice == "2":
        command = "tracert"

    elif choice == "3":
        command = "nslookup"

    elif choice == "4":
        command = "ipconfig"

    elif choice == "5":
        command = "route"

    elif choice == "6":
        command = "arp"

    elif choice == "7":
        command = "netstat"

    elif choice == "8":
        command = "exit"

    else:
        print("Invalid choice")
        continue

    if command in ["ping", "tracert", "nslookup"]:
        host = input("Enter host: ")
        command = command + " " + host

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_NAME, SERVER_PORT))

    client_socket.send(command.encode())

    response = client_socket.recv(4096).decode()

    print("Server response:")
    print(response)

    client_socket.close()

    if choice == "8":
        break