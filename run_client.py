from socket import *
server_name = gethostname ()
server_port = 5566
client_socket = socket (AF_INET, SOCK_STREAM)
client_socket. connect ( (server_name, server_port) )
welcome = input ('''========================
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
Select:''')
client_socket. send (welcome.encode ())
modified_sentence = client_socket. recv (2048)
print ('From Server: ', modified_sentence.decode () )
client_socket.close ()