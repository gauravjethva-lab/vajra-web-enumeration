import subprocess
import os
import threading

from core.utils import require_tool


def clean_hosts(input_file, clean_file):
    hosts = set()
    if not os.path.exists(input_file):
        return 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            line = line.replace("https://", "").replace("http://", "")
            line = line.split("/")[0].split(":")[0]
            if line:
                hosts.add(line)
    with open(clean_file, "w") as f:
        for host in sorted(hosts):
            f.write(host + "\n")
    return len(hosts)


def scan_ports(domain):
    input_file       = f"output/{domain}/live_subdomains.txt"
    clean_hosts_file = f"output/{domain}/clean_hosts.txt"
    masscan_output   = f"output/{domain}/masscan.txt"
    naabu_output     = f"output/{domain}/naabu.txt"
    final_output     = f"output/{domain}/open_ports.txt"

    print("\n[+] Preparing hosts for port scanning...")

    count = clean_hosts(input_file, clean_hosts_file)
    if count == 0:
        print("[-] No hosts to scan.")
        open(final_output, "w").close()
        return

    print(f"[+] Scanning {count} hosts...")

    masscan_bin = require_tool("masscan")
    naabu_bin   = require_tool("naabu")

    # ── Run masscan + naabu in PARALLEL ─────────────────────
    def run_masscan():
        if not masscan_bin: return
        print("[+] Running Masscan (rate 5000)...")
        sudo = "" if os.geteuid() == 0 else "sudo "
        try:
            subprocess.run(
                f"{sudo}{masscan_bin} -p1-1000 --rate 5000 -iL {clean_hosts_file} -oL {masscan_output} > /dev/null 2>&1",
                shell=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            print("[!] Masscan timed out.")

    def run_naabu():
        if not naabu_bin: return
        print("[+] Running Naabu (top 1000)...")
        try:
            subprocess.run(
                f"cat {clean_hosts_file} | {naabu_bin} -top-ports 1000 -silent -c 50 -o {naabu_output} > /dev/null 2>&1",
                shell=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            print("[!] Naabu timed out.")

    t1 = threading.Thread(target=run_masscan)
    t2 = threading.Thread(target=run_naabu)
    t1.start(); t2.start()
    t1.join();  t2.join()

    # ── Merge ────────────────────────────────────────────────
    combined = set()
    if os.path.exists(naabu_output):
        with open(naabu_output) as f:
            for line in f:
                line = line.strip()
                if line: combined.add(line)

    if os.path.exists(masscan_output):
        with open(masscan_output) as f:
            for line in f:
                if "open" in line:
                    parts = line.split()
                    try:
                        port = parts[2].split("/")[0]
                        host = parts[3]
                        combined.add(f"{host}:{port}")
                    except IndexError:
                        pass

    with open(final_output, "w") as f:
        for item in sorted(combined):
            f.write(item + "\n")

    print(f"[+] Open ports found: {len(combined)}")
    print(f"[+] Saved → {final_output}")
    print("\n[+] Port Scanning Completed!")
