from socket import *
from pathlib import Path

from T003.config.config_loader import load_config

from T003.web.web import read_logs
from T003.web.web import home_page
from T003.web.web import dashboard_page
from T003.web.web import history_page
from T003.web.web import stats_page
from T003.web.web import search_page
from T003.web.web import error_page

config = load_config()

SERVER_PORT = config["http_port"]
LOG_FILE = config["log_file"]


def create_response(status, content):

    response = "HTTP/1.1 " + status + "\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: " + str(len(content.encode())) + "\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += content

    return response


def start_http_server():

    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(("", SERVER_PORT))
    server_socket.listen(5)

    print("HTTP Server is listening...")
    print("Open http://localhost:" + str(SERVER_PORT))

    while True:

        connection_socket, client_address = server_socket.accept()

        request = connection_socket.recv(4096).decode()

        if not request:
            connection_socket.close()
            continue

        parts = request.split()

        if len(parts) < 2:
            response = create_response(
                "400 Bad Request",
                error_page("400 Bad Request")
            )

        else:

            method = parts[0]
            path = parts[1]

            query = {}

            if "?" in path:

                path_parts = path.split("?", 1)

                path = path_parts[0]
                query_string = path_parts[1]

                for item in query_string.split("&"):

                    if "=" in item:

                        key, value = item.split("=", 1)
                        query[key] = value

            if method != "GET":

                response = create_response(
                    "400 Bad Request",
                    error_page("400 Bad Request")
                )

            elif path == "/":

                response = create_response(
                    "200 OK",
                    home_page()
                )

            elif path == "/dashboard":

                response = create_response(
                    "200 OK",
                    dashboard_page(read_logs())
                )

            elif path == "/history":

                response = create_response(
                    "200 OK",
                    history_page(read_logs())
                )

            elif path == "/stats":

                response = create_response(
                    "200 OK",
                    stats_page(read_logs())
                )

            elif path == "/search":

                response = create_response(
                    "200 OK",
                    search_page(
                        read_logs(),
                        query.get("command", ""),
                        query.get("hostname", ""),
                        query.get("client_ip", "")
                    )
                )

            elif path == "/download":

                if not Path(LOG_FILE).exists():

                    response = create_response(
                        "404 Not Found",
                        error_page("404 Not Found")
                    )

                else:

                    file = open(LOG_FILE, "rb")
                    data = file.read()
                    file.close()

                    response = "HTTP/1.1 200 OK\r\n"
                    response += "Content-Type: application/json\r\n"
                    response += "Content-Disposition: attachment; filename=server_log.json\r\n"
                    response += "Content-Length: " + str(len(data)) + "\r\n"
                    response += "Connection: close\r\n"
                    response += "\r\n"

                    connection_socket.send(response.encode() + data)
                    connection_socket.close()

                    continue

            elif path == "/forbidden":

                response = create_response(
                    "403 Forbidden",
                    error_page("403 Forbidden")
                )

            else:

                response = create_response(
                    "404 Not Found",
                    error_page("404 Not Found")
                )

        connection_socket.send(response.encode())
        connection_socket.close()


if __name__ == "__main__":
    start_http_server()