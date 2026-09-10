import subprocess
import os
from core.utils import require_tool


def clean_hosts(input_file, clean_file):
    """Extract clean hostnames from live_subdomains.txt (httpx format)."""
    hosts = set()
    if not os.path.exists(input_file):
        return 0
    try:
        with open(input_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # httpx format: "https://host [200] [Title]"
                # Take first token only (the URL)
                url = line.split()[0] if line.split() else line
                # Strip scheme
                url = url.replace("https://", "").replace("http://", "")
                # Strip path
                url = url.split("/")[0]
                # Strip port
                url = url.split(":")[0]
                # Strip any leftover brackets
                url = url.strip("[]")
                if url and "." in url:
                    hosts.add(url)
    except Exception as e:
        print(f"[-] Error reading input file: {e}")
        return 0

    try:
        with open(clean_file, "w") as f:
            for host in sorted(hosts):
                f.write(host + "\n")
    except Exception as e:
        print(f"[-] Error writing clean hosts: {e}")
        return 0

    return len(hosts)


def scan_ports(domain):
    input_file       = f"output/{domain}/live_subdomains.txt"
    clean_hosts_file = f"output/{domain}/clean_hosts.txt"
    masscan_output   = f"output/{domain}/masscan.txt"
    naabu_output     = f"output/{domain}/naabu.txt"
    final_output     = f"output/{domain}/open_ports.txt"

    print("\n[+] Preparing Hosts For Port Scanning...")

    count = clean_hosts(input_file, clean_hosts_file)

    if count == 0:
        print("[-] No hosts to scan.")
        try:
            open(final_output, "w").close()
        except Exception:
            pass
        return

    print(f"[+] Scanning {count} hosts...")

    masscan_bin = require_tool("masscan")
    naabu_bin   = require_tool("naabu")

    if masscan_bin:
        print("[+] Running Masscan...")
        sudo = "" if os.geteuid() == 0 else "sudo "
        try:
            subprocess.run(
                f"{sudo}{masscan_bin} -p1-1000 --rate 1000 "
                f"-iL {clean_hosts_file} -oL {masscan_output} > /dev/null 2>&1",
                shell=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            print("[!] Masscan timed out.")
        except Exception as e:
            print(f"[-] Masscan error: {e}")

    if naabu_bin:
        print("[+] Running Naabu...")
        try:
            subprocess.run(
                f"cat {clean_hosts_file} | {naabu_bin} -top-ports 1000 "
                f"-silent -o {naabu_output} > /dev/null 2>&1",
                shell=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            print("[!] Naabu timed out.")
        except Exception as e:
            print(f"[-] Naabu error: {e}")

    combined = set()

    if os.path.exists(naabu_output):
        try:
            with open(naabu_output) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        combined.add(line)
        except Exception:
            pass

    if os.path.exists(masscan_output):
        try:
            with open(masscan_output) as f:
                for line in f:
                    if "open" in line:
                        parts = line.split()
                        try:
                            port = parts[2].split("/")[0]
                            host = parts[3]
                            combined.add(f"{host}:{port}")
                        except (IndexError, ValueError):
                            pass
        except Exception:
            pass

    try:
        with open(final_output, "w") as f:
            for item in sorted(combined):
                f.write(item + "\n")
    except Exception as e:
        print(f"[-] Error saving ports: {e}")

    print(f"[+] Open ports found: {len(combined)}")
    print(f"[+] Saved → {final_output}")
    print("\n[+] Port Scanning Completed!")
