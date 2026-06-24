import os
import hashlib
import json

MONITOR_DIR = "./target_directory"  # Path you want to watch
BASELINE_FILE = "system_baseline.json"

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except PermissionError:
        return None

def create_baseline():
    baseline = {}
    if not os.path.exists(MONITOR_DIR):
        os.makedirs(MONITOR_DIR)
    
    for root, _, files in os.walk(MONITOR_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = calculate_sha256(full_path)
            if file_hash:
                baseline[full_path] = file_hash
                
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"[+] Baseline successfully generated with {len(baseline)} monitored files.")

def verify_integrity():
    if not os.path.exists(BASELINE_FILE):
        print("[-] Baseline configuration file missing. Run baseline creation first.")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    print("[*] Auditing files for unexpected modifications or compromises...")
    for root, _, files in os.walk(MONITOR_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            current_hash = calculate_sha256(full_path)
            
            if full_path not in baseline:
                print(f"[ALERT] Untrusted/New File Planted: {full_path}")
            elif current_hash != baseline[full_path]:
                print(f"[ALERT] File Tampered/Modified: {full_path}")

if __name__ == "__main__":
    # If baseline doesn't exist, create it. Otherwise, monitor changes.
    if not os.path.exists(BASELINE_FILE):
        create_baseline()
    else:
        verify_integrity()
