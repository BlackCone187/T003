from socket import *
from menu import show_menu

from T003.config.config_loader import load_config


config = load_config()

SERVER_NAME = "localhost"
SERVER_PORT = config["tcp_port"]


def start_client():

    while True:

        choice = show_menu()

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