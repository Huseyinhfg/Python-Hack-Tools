import requests
import os
import sys
import time

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Colors
BLUE = "\033[1;36m"
CYAN = "\033[1;96m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"

# Banner animation
def banner():
    b = f"""
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
    for c in b:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.0005)

# Loading animation
def loading(msg="Loading"):
    for i in range(6):
        sys.stdout.write(f"\r{MAGENTA}{msg}{'.'*i}{RESET}{' '*(6-i)}")
        sys.stdout.flush()
        time.sleep(0.08)
    print("\r", end="")

# Mini ASCII explosion effect
def ascii_explosion():
    frames = [
        f"{RED}   (    )   {RESET}",
        f"{YELLOW}  ( )  ( )  {RESET}",
        f"{GREEN}   )    (   {RESET}",
        f"{CYAN}  ( )  ( )  {RESET}",
        f"{MAGENTA}   (    )   {RESET}"
    ]
    for f in frames:
        print(f"\r{f}", end="")
        sys.stdout.flush()
        time.sleep(0.06)
    print("\r", end="")

# Fetch IP info
def fetch_ip(ip):
    try:
        loading("Fetching IP details")
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=5)
        data = response.json()
        if data['status'] != 'success':
            print(f"{RED}❌ IP not found or invalid.{RESET}")
            return None
        return data
    except Exception as e:
        print(f"{RED}💀 Error occurred: {e}{RESET}")
        return None

# Display IP info
def display_ip(data):
    ascii_explosion()
    print(f"{GREEN}═════════════════════════════════════════════{RESET}")
    print(f"{YELLOW}🌍 IP:{RESET} {CYAN}{data['query']}{RESET}")
    print(f"{YELLOW}📍 Country:{RESET} {CYAN}{data['country']} ({data['countryCode']}){RESET}")
    print(f"{YELLOW}🏙️ City:{RESET} {CYAN}{data['city']}{RESET}")
    print(f"{YELLOW}🔁 Region:{RESET} {CYAN}{data['regionName']}{RESET}")
    print(f"{YELLOW}🌐 ISP:{RESET} {CYAN}{data['isp']}{RESET}")
    print(f"{YELLOW}🌐 Org:{RESET} {CYAN}{data['org']}{RESET}")
    print(f"{YELLOW}🧭 Timezone:{RESET} {CYAN}{data['timezone']}{RESET}")
    print(f"{YELLOW}📡 LAT / LON:{RESET} {CYAN}{data['lat']} / {data['lon']}{RESET}")
    print(f"{YELLOW}🧪 Reverse DNS:{RESET} {CYAN}{data.get('reverse','N/A')}{RESET}")
    vpn_status = f"{RED}YES{RESET}" if data.get('proxy') or data.get('hosting') else f"{GREEN}NO{RESET}"
    print(f"{YELLOW}🛡️ Anonymous / VPN:{RESET} {vpn_status}")
    print(f"{YELLOW}🗺️ Google Maps:{RESET} https://www.google.com/maps?q={data['lat']},{data['lon']}")
    print(f"{GREEN}═════════════════════════════════════════════{RESET}\n")
    time.sleep(0.2)

# Main menu
def main():
    banner()
    while True:
        print(f"{YELLOW}1.{RESET} Query single IP")
        print(f"{YELLOW}2.{RESET} Query multiple IPs (comma separated)")
        print(f"{YELLOW}3.{RESET} Exit")
        choice = input(f"\n🟩 Your choice: ").strip()
        
        if choice == '1':
            while True:
                ip = input("🟩 Enter IP: ").strip()
                data = fetch_ip(ip)
                if data:
                    display_ip(data)
                again = input("Do you want to query another IP? (y/n): ").strip().lower()
                if again != 'y':
                    break

        elif choice == '2':
            ips = input("🟩 Enter IPs (comma separated): ").strip().split(',')
            for ip in ips:
                ip = ip.strip()
                data = fetch_ip(ip)
                if data:
                    display_ip(data)
            again = input("Do you want to query more IPs? (y/n): ").strip().lower()
            if again != 'y':
                continue

        elif choice == '3':
            print(f"{GREEN}Exiting...{RESET}")
            time.sleep(0.5)
            break
        else:
            print(f"{RED}❌ Invalid choice!{RESET}")

if __name__ == "__main__":
    main()

