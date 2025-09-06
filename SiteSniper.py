import subprocess
import os
import sys
import threading
from urllib.parse import urlparse
from datetime import datetime
import time
import re

# ANSI renkler
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"

BANNER_LINES = [
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

def animate_banner():
    for line in BANNER_LINES:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.0015)
        print()
    print()
    time.sleep(0.3)

def create_folder_name(url):
    domain = urlparse(url).netloc.replace('.', '_')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{domain}_{timestamp}"

def print_progress_bar(current, total, length=40):
    percent = int((current / total) * 100) if total else 0
    filled_length = int(length * current // total) if total else 0
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f"\r{YELLOW}[{bar}] {percent}%{RESET}")
    sys.stdout.flush()
    if current >= total and total != 0:
        print()

def download_site(url, base_folder):
    if not base_folder:
        target_folder = os.path.join(os.getcwd(), create_folder_name(url))
    else:
        target_folder = os.path.join(base_folder, create_folder_name(url))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

    print(f"{CYAN}[+] Downloading {url} into {target_folder}{RESET}")

    # Real byte-based progress using wget --progress=dot
    command = ["wget", "--mirror", "--convert-links", "--adjust-extension",
               "--page-requisites", "--no-parent", "--progress=dot", "-P", target_folder, url]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    total_bytes = 0
    downloaded_bytes = 0
    for line in process.stdout:
        # Parse total size if present
        match_total = re.search(r"Length: (\d+)", line)
        if match_total:
            total_bytes = int(match_total.group(1))
        # Parse downloaded bytes from dot style
        match_bytes = re.findall(r"(\d+)", line.replace('.', ''))
        if match_bytes:
            downloaded_bytes += sum(map(int, match_bytes))
            print_progress_bar(min(downloaded_bytes, total_bytes), max(total_bytes, 1))

    process.wait()
    print(f"{GREEN}[+] Finished downloading {url}{RESET}")

def main():
    animate_banner()
    base_folder = input(f"{CYAN}Enter the folder to save sites (leave empty for current folder): {RESET}")

    while True:
        urls = input(f"{CYAN}Enter URLs to clone (separated by space): {RESET}").split()
        threads = []
        for url in urls:
            t = threading.Thread(target=download_site, args=(url, base_folder))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        cont = input(f"{CYAN}Do you want to download another site? (y/n): {RESET}").strip().lower()
        if cont != 'y':
            break

    print(f"{MAGENTA}[+] All downloads completed!{RESET}")

if __name__ == "__main__":
    main()

