def show_menu():
    choice = input("""
========================
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
Select: """)

    return choice