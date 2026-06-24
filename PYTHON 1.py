import requests
import threading
import queue
import sys

# Target domain and basic configuration
TARGET_DOMAIN = "example.com"
THREADS = 10
wordlist_queue = queue.Queue()

# Simple common subdomains list (expand this in your repo)
subdomains = ["www", "mail", "ftp", "admin", "blog", "api", "dev", "staging", "test", "ssh"]
for sub in subdomains:
    wordlist_queue.put(sub)

def scan_subdomains():
    while not wordlist_queue.empty():
        subdomain = wordlist_queue.get()
        url = f"http://{subdomain}.{TARGET_DOMAIN}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"[+] Active Subdomain Found: {url} (Status: 200)")
            elif response.status_code in [401, 403]:
                print(f"[!] Restricted Subdomain: {url} (Status: {response.status_code})")
        except requests.ConnectionError:
            pass
        finally:
            wordlist_queue.task_done()

def main():
    print(f"[*] Starting OSINT Subdomain Scan for {TARGET_DOMAIN}...")
    for _ in range(THREADS):
        t = threading.Thread(target=scan_subdomains)
        t.daemon = True
        t.start()
        
    wordlist_queue.join()
    print("[*] Scan complete.")

if __name__ == "__main__":
    main()
