from socket import *
import threading

from client_handler import handle_client


SERVER_PORT = 5462

server_socket = socket(AF_INET, SOCK_STREAM)#make tcp socket that use IPv4

server_socket.bind(('', SERVER_PORT))# link a socket with port number

server_socket.listen(5)

print("Server is listening...")

while True:
    connection_socket, client_address = server_socket.accept()

    print("Client connected:", client_address)#client_address==>(IP address, port)

    thread = threading.Thread(
        target=handle_client,
        args=(connection_socket, client_address)
    )

    thread.start()