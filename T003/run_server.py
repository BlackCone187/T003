from socket import *
server_port = 5566
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('The server is ready to receive')
while True:
    connection_socket, addr = server_socket.accept ()
    selection = connection_socket. recv (2048) .decode ()
    print("IP: " + addr [0] + ", Port: " + str (addr [1]) )
    print (selection)
    capitalized_sentence = selection.upper ()
    print (capitalized_sentence)
    connection_socket. send(capitalized_sentence.encode ())
    connection_socket.close ()