import subprocess

def ping(host): # check if we can connect with server and return the RTT
    result = subprocess.run(["ping", host], capture_output=True,text=True)
    return result

def tracert(host): # trace the path(hops) that the packets pass through it
    result = subprocess.run(["tracert", host], capture_output=True,text=True)
    return result

def nslookup(host):#asks a DNS server for the IP address associated with a domain name
    result = subprocess.run(["nslookup", host], capture_output=True,text=True)
    return result

def ipconfig():#show the info of the network on ur device like ip address,dns, and default gateway
    result = subprocess.run(["ipconfig"], capture_output=True,text=True)
    return result

def route():#show a routing table that the sender device take it as evidence to arrived to the destination
    result = subprocess.run(["route"], capture_output=True,text=True)
    return result

def arp():#showing the relation b/t ip address and mac address that are exist in the arp chach
    # (to know the mac for the destination device)
    result = subprocess.run(["arp"], capture_output=True,text=True)
    return result

def netstat():#showing the current connection server and info about tcp or udp
    result = subprocess.run(["netstat"], capture_output=True,text=True)
    return result