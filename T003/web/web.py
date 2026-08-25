import json
import time
from pathlib import Path

from T003.config.config_loader import load_config

config = load_config()

LOG_FILE = config["log_file"]

start_time = time.time()


def read_logs():

    logs = []

    if not Path(LOG_FILE).exists():
        return logs

    file = open(LOG_FILE, "r")

    for line in file:

        line = line.strip()

        if line:

            try:
                logs.append(json.loads(line))
            except:
                pass

    file.close()

    return logs


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

    content = ""

    content += "<h2>Home Page</h2>"

    content += "<p><b>Team Number:</b> T003</p>"

    content += "<p><b>Student Names:</b></p>"
    content += "<ul>"
    content += "<li>Jaber Jaber</li>"
    content += "<li>Noor Aldeen Alatrash</li>"
    content += "<li>Mohammad Hasiba</li>"
    content += "</ul>"

    content += "<p><b>Student IDs:</b></p>"
    content += "<ul>"
    content += "<li>1240929</li>"
    content += "<li>1242462</li>"
    content += "<li>1242780</li>"
    content += "</ul>"

    content += "<p><b>Section:</b> 2</p>"

    content += "<h3>About the Course</h3>"
    content += "<p>ENCS3320 - Computer Networks</p>"

    return create_page("Home", content)


def dashboard_page(logs):

    clients = []

    for log in logs:

        if log.get("client_ip", "") not in clients:
            clients.append(log.get("client_ip", ""))

    last_time = "-"

    if len(logs) > 0:
        last_time = logs[-1].get("timestamp", "-")

    content = "<h2>Dashboard</h2>"
    content += "<p><b>Number of executed commands:</b> " + str(len(logs)) + "</p>"
    content += "<p><b>Number of connected clients:</b> " + str(len(clients)) + "</p>"
    content += "<p><b>Last execution time:</b> " + str(last_time) + "</p>"
    content += "<p><b>Server uptime:</b> " + str(int(time.time() - start_time)) + " seconds</p>"

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

    content = "<h2>Statistics</h2>"
    content += "<p><b>Most frequently used command:</b> " + most_used + "</p>"
    content += "<p><b>Average execution time:</b> " + str(round(average, 4)) + " seconds</p>"
    content += "<p><b>Total successful requests:</b> " + str(successful) + "</p>"
    content += "<p><b>Total failed requests:</b> " + str(failed) + "</p>"

    return create_page("Statistics", content)


def search_page(logs, command, hostname, client_ip):

    content = "<h2>Search</h2>"

    content += '<form method="GET" action="/search" id="search-form">'

    content += "<p>Command:</p>"

    content += '<select name="command" id="command">'

    commands = ["ping", "tracert", "nslookup", "ipconfig", "route", "arp", "netstat"]

    if command == "":
        content += '<option value="" selected>All</option>'
    else:
        content += '<option value="">All</option>'

    for item in commands:

        if command == item:
            content += '<option value="' + item + '" selected>' + item + '</option>'
        else:
            content += '<option value="' + item + '">' + item + '</option>'

    content += "</select>"

    content += "<p>Hostname:</p>"
    content += '<input type="text" name="hostname" id="hostname" value="' + hostname + '">'

    content += "<p>Client IP:</p>"
    content += '<input type="text" name="client_ip" id="client_ip" value="' + client_ip + '">'

    content += "<br><br>"

    content += '<input type="submit" value="Search"> '
    content += '<input type="button" value="Clear" onclick="clearSearch()">'

    content += "</form>"

    content += '<div id="saved-results"></div>'

    content += """
    <script>

    window.onload = function() {

        if (localStorage.getItem("search_command") !== null) {
            document.getElementById("command").value =
                localStorage.getItem("search_command");
        }

        if (localStorage.getItem("search_hostname") !== null) {
            document.getElementById("hostname").value =
                localStorage.getItem("search_hostname");
        }

        if (localStorage.getItem("search_client_ip") !== null) {
            document.getElementById("client_ip").value =
                localStorage.getItem("search_client_ip");
        }

        if (localStorage.getItem("search_results") !== null) {
            document.getElementById("saved-results").innerHTML =
                localStorage.getItem("search_results");
        }
    };


    document.getElementById("search-form").addEventListener("submit", function() {

        localStorage.setItem(
            "search_command",
            document.getElementById("command").value
        );

        localStorage.setItem(
            "search_hostname",
            document.getElementById("hostname").value
        );

        localStorage.setItem(
            "search_client_ip",
            document.getElementById("client_ip").value
        );
    });


    function clearSearch() {

        document.getElementById("command").value = "";
        document.getElementById("hostname").value = "";
        document.getElementById("client_ip").value = "";

        localStorage.removeItem("search_command");
        localStorage.removeItem("search_hostname");
        localStorage.removeItem("search_client_ip");
        localStorage.removeItem("search_results");

        document.getElementById("saved-results").innerHTML = "";
    }

    </script>
    """

    if command != "" or hostname != "" or client_ip != "":

        content += "<h3>Search Results</h3>"

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

            log_command = str(log.get("command", ""))
            log_parameter = str(log.get("parameter", ""))
            log_ip = str(log.get("client_ip", ""))

            if command != "" and command.lower() not in log_command.lower():
                continue

            if hostname != "" and hostname.lower() not in log_parameter.lower():
                continue

            if client_ip != "" and client_ip.lower() not in log_ip.lower():
                continue

            content += "<tr>"
            content += "<td>" + str(log.get("timestamp", "")) + "</td>"
            content += "<td>" + log_ip + "</td>"
            content += "<td>" + log_command + "</td>"
            content += "<td>" + log_parameter + "</td>"
            content += "<td>" + str(log.get("execution_time", "")) + "</td>"
            content += "<td>" + str(log.get("result", "")) + "</td>"
            content += "</tr>"

        content += "</table>"

    return create_page("Search", content)


def error_page(status):

    content = "<h2>" + status + "</h2>"
    content += "<p>The requested page cannot be accessed.</p>"

    return create_page(status, content)