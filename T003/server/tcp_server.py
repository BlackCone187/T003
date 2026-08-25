from socket import *
import threading

from T003.server.client_handler import handle_client
from T003.config.config_loader import load_config

config = load_config()

SERVER_PORT = config["tcp_port"]


def start_tcp_server():

    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(('', SERVER_PORT))

    #server_socket.listen(config["max_clients"])
    server_socket.listen(2)
    print("TCP Server is listening...")

    while True:

        connection_socket, client_address = server_socket.accept()

        print("Client connected:", client_address)

        thread = threading.Thread(
            target=handle_client,
            args=(connection_socket, client_address)
        )

        thread.start()