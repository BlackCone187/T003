from socket import *

SERVER_PORT = 6462

server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind(('', SERVER_PORT))

server_socket.listen(5)

print("HTTP Server is listening...")


def create_response(status, content):
    response = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html\r\n"
        "\r\n"
        f"{content}"
    )
    return response


def home_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Network Diagnostic System</title>
    </head>
    <body>
        <h1>Network Diagnostic System</h1>

        <h2>Team Information</h2>
        <p>Team Number: T003</p>
        <p>Course: ENCS3320</p>
        <p>Project: Socket Programming</p>

        <h2>Pages</h2>

        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/history">Command History</a></li>
            <li><a href="/stats">Statistics</a></li>
            <li><a href="/search">Search</a></li>
            <li><a href="/download">Download</a></li>
        </ul>
    </body>
    </html>
    """


def dashboard_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h1>Dashboard</h1>
        <p>Number of executed commands: 0</p>
        <p>Number of connected clients: 0</p>
        <p>Last execution time: -</p>
        <p>Server uptime: 0 seconds</p>
    </body>
    </html>
    """


def history_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Command History</title>
    </head>
    <body>
        <h1>Command History</h1>

        <table border="1">
            <tr>
                <th>Time</th>
                <th>Client IP</th>
                <th>Command</th>
                <th>Parameter</th>
                <th>Execution Time</th>
                <th>Status</th>
            </tr>
        </table>
    </body>
    </html>
    """


def stats_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Statistics</title>
    </head>
    <body>
        <h1>Statistics</h1>
        <p>Most frequently used command: -</p>
        <p>Average execution time: -</p>
        <p>Total successful requests: 0</p>
        <p>Total failed requests: 0</p>
    </body>
    </html>
    """


def search_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search</title>
    </head>
    <body>
        <h1>Search</h1>

        <form>
            <label>Command:</label>
            <input type="text">

            <br><br>

            <label>Hostname:</label>
            <input type="text">

            <br><br>

            <label>Client IP:</label>
            <input type="text">

            <br><br>

            <input type="submit" value="Search">
        </form>
    </body>
    </html>
    """


def download_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Download</title>
    </head>
    <body>
        <h1>Download</h1>
        <p>Download log file</p>
    </body>
    </html>
    """


def error_page(status):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{status}</title>
    </head>
    <body>
        <h1>{status}</h1>
        <p>The requested resource cannot be accessed.</p>
    </body>
    </html>
    """


while True:
    connection_socket, client_address = server_socket.accept()

    request = connection_socket.recv(4096).decode()

    if not request:
        connection_socket.close()
        continue

    parts = request.split()

    if len(parts) < 2:
        response = create_response("400 Bad Request", error_page("400 Bad Request"))

    else:
        method = parts[0]
        path = parts[1]

        if method != "GET":
            response = create_response("400 Bad Request", error_page("400 Bad Request"))

        elif path == "/":
            response = create_response("200 OK", home_page())

        elif path == "/dashboard":
            response = create_response("200 OK", dashboard_page())

        elif path == "/history":
            response = create_response("200 OK", history_page())

        elif path == "/stats":
            response = create_response("200 OK", stats_page())

        elif path == "/search":
            response = create_response("200 OK", search_page())

        elif path == "/download":
            response = create_response("403 Forbidden", error_page("403 Forbidden"))

        else:
            response = create_response("404 Not Found", error_page("404 Not Found"))

    connection_socket.send(response.encode())
    connection_socket.close()