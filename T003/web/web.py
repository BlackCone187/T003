import json
import time
from pathlib import Path

from T003.config.config_loader import load_config

config = load_config()

LOG_FILE = config["log_file"]

start_time = time.time()


def read_logs():

    if not Path(LOG_FILE).exists():
        return []

    with open(LOG_FILE, "r") as f:
        return json.load(f)


def create_page(title, content):

    html = "<!DOCTYPE html>"
    html += "<html>"
    html += "<head>"
    html += "<title>" + title + "</title>"
    html += "</head>"
    html += "<body>"

    html += "<h1>Network Diagnostic System</h1>"

    html += "<p>"
    html += '<a href="/">Home</a> | '
    html += '<a href="/dashboard">Dashboard</a> | '
    html += '<a href="/history">Command History</a> | '
    html += '<a href="/stats">Statistics</a> | '
    html += '<a href="/search">Search</a> | '
    html += '<a href="/download">Download</a>'
    html += "</p>"

    html += "<hr>"
    html += content

    html += "</body>"
    html += "</html>"

    return html


def home_page():

    content = f"""
    <h2>Home Page</h2>

    <p><b>Team Number:</b> T003</p>

    <p><b>Student Names:</b></p>
    <ul>
        <li>Jaber Jaber</li>
        <li>Noor Aldeen Alatrash</li>
        <li>Mohammad Hasiba</li>
    </ul>

    <p><b>Student IDs:</b></p>
    <ul>
        <li>1240929</li>
        <li>1242462</li>
        <li>1242780</li>
    </ul>

    <p><b>Section:</b> 2</p>

    <h3>About the Course</h3>
    <p>ENCS3320 - Computer Networks</p>
    """

    return create_page("Home", content)


def dashboard_page(logs):

    clients = []

    for log in logs:

        if log.get("client_ip", "") not in clients:
            clients.append(log.get("client_ip", ""))

    last_time = "-"

    if len(logs) > 0:
        last_time = logs[-1].get("timestamp", "-")

    content = f"""
    <h2>Dashboard</h2>
    <p><b>Number of executed commands:</b> {len(logs)}</p>
    <p><b>Number of connected clients:</b> {len(clients)}</p>
    <p><b>Last execution time:</b> {last_time}</p>
    <p><b>Server uptime:</b> {int(time.time() - start_time)} seconds</p>
    """

    return create_page("Dashboard", content)


def history_page(logs):

    content = "<h2>Command History</h2>"

    content += "<table border='1' cellpadding='5'>"

    content += "<tr>"
    content += "<th>Time</th>"
    content += "<th>Client IP</th>"
    content += "<th>Command</th>"
    content += "<th>Parameter</th>"
    content += "<th>Execution Time</th>"
    content += "<th>Status</th>"
    content += "</tr>"

    for log in logs:

        content += "<tr>"
        content += "<td>" + str(log.get("timestamp", "")) + "</td>"
        content += "<td>" + str(log.get("client_ip", "")) + "</td>"
        content += "<td>" + str(log.get("command", "")) + "</td>"
        content += "<td>" + str(log.get("parameter", "")) + "</td>"
        content += "<td>" + str(log.get("execution_time", "")) + "</td>"
        content += "<td>" + str(log.get("result", "")) + "</td>"
        content += "</tr>"

    content += "</table>"

    return create_page("Command History", content)


def stats_page(logs):

    successful = 0
    failed = 0
    total_time = 0
    commands = {}

    for log in logs:

        command = str(log.get("command", ""))

        if command not in commands:
            commands[command] = 1
        else:
            commands[command] += 1

        if log.get("result", "") == "Success":
            successful += 1

        elif log.get("result", "") == "Failure":
            failed += 1

        try:
            total_time += float(log.get("execution_time", 0))
        except:
            pass

    most_used = "-"

    if len(commands) > 0:
        most_used = max(commands, key=commands.get)

    average = 0

    if len(logs) > 0:
        average = total_time / len(logs)

    content = f"""
    <h2>Statistics</h2>
    <p><b>Most frequently used command:</b> {most_used}</p>
    <p><b>Average execution time:</b> {round(average, 4)} seconds</p>
    <p><b>Total successful requests:</b> {successful}</p>
    <p><b>Total failed requests:</b> {failed}</p>
    """

    return create_page("Statistics", content)


def search_page(logs, command, hostname, client_ip):

    content = f"""
    <h2>Search</h2>

    <form method="GET" action="/search">

        <p>Command:</p>
        <select name="command">
            <option value="">All</option>
            <option value="ping">ping</option>
            <option value="tracert">tracert</option>
            <option value="nslookup">nslookup</option>
            <option value="ipconfig">ipconfig</option>
            <option value="route">route</option>
            <option value="arp">arp</option>
            <option value="netstat">netstat</option>
        </select>

        <p>Hostname:</p>
        <input type="text" name="hostname" value="{hostname}">

        <p>Client IP:</p>
        <input type="text" name="client_ip" value="{client_ip}">

        <br><br>

        <input type="submit" value="Search">

    </form>
    """

    if command != "" or hostname != "" or client_ip != "":

        content += """
        <h3>Search Results</h3>

        <table border="1" cellpadding="5">
            <tr>
                <th>Time</th>
                <th>Client IP</th>
                <th>Command</th>
                <th>Parameter</th>
                <th>Execution Time</th>
                <th>Status</th>
            </tr>
        """

        for log in logs:

            log_command = str(log.get("command", ""))
            log_parameter = str(log.get("parameter", ""))
            log_ip = str(log.get("client_ip", ""))

            if command and command.lower() not in log_command.lower():
                continue

            if hostname and hostname.lower() not in log_parameter.lower():
                continue

            if client_ip and client_ip.lower() not in log_ip.lower():
                continue

            content += f"""
            <tr>
                <td>{log.get("timestamp", "")}</td>
                <td>{log_ip}</td>
                <td>{log_command}</td>
                <td>{log_parameter}</td>
                <td>{log.get("execution_time", "")}</td>
                <td>{log.get("result", "")}</td>
            </tr>
            """

        content += "</table>"

    return create_page("Search", content)


def error_page(status):

    content = "<h2>" + status + "</h2>"
    content += "<p>The requested page cannot be accessed.</p>"

    return create_page(status, content)