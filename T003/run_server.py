import threading

from T003.server.tcp_server import start_tcp_server
from T003.server.http_server import start_http_server


tcp_thread = threading.Thread(target=start_tcp_server)
http_thread = threading.Thread(target=start_http_server)

tcp_thread.start()
http_thread.start()