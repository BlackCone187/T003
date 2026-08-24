from socket import *

SERVER_PORT = 6462

server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind(('', SERVER_PORT))

server_socket.listen(5)

print("HTTP Server is listening...")

while True:
    connection_socket, client_address = server_socket.accept()

    request = connection_socket.recv(4096).decode()

    response = """HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<html>
<head>
    <title>Network Diagnostic System</title>
</head>
<body>
    <h1>Network Diagnostic System</h1>
    <p>Hello from HTTP Server</p>
</body>
</html>
"""

    connection_socket.send(response.encode())
    connection_socket.close()