import subprocess
import os
import shutil
from core.utils import require_tool


def detect_services(domain):
    """
    nmap -sV se confirmed services dhundta hai open ports pe.
    Input: open_ports.txt (host:port format)
    Output: validated_services.txt
    """
    ports_file  = f"output/{domain}/open_ports.txt"
    output_file = f"output/{domain}/validated_services.txt"

    print("\n[+] Running Service Detection (nmap -sV)...")

    if not os.path.exists(ports_file):
        print(f"[-] Input file not found: {ports_file}")
        try:
            open(output_file, "w").close()
        except Exception:
            pass
        return

    # Parse host:port pairs
    targets = {}
    try:
        with open(ports_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    host, port = line.rsplit(":", 1)
                    host = host.strip()
                    port = port.strip()
                    if host and port.isdigit():
                        if host not in targets:
                            targets[host] = []
                        targets[host].append(port)
    except Exception as e:
        print(f"[-] Error reading ports file: {e}")
        open(output_file, "w").close()
        return

    if not targets:
        print("[-] No valid host:port entries found.")
        open(output_file, "w").close()
        return

    if not shutil.which("nmap"):
        print("[!] nmap not found — skipping service detection.")
        print("    Install: sudo apt-get install -y nmap")
        open(output_file, "w").close()
        return

    print(f"[+] Validating services on {len(targets)} hosts...")

    results = []
    # Max 15 hosts to keep it fast
    for host, ports in list(targets.items())[:15]:
        port_str = ",".join(ports[:20])  # max 20 ports per host
        try:
            out = subprocess.check_output(
                f"nmap -sV --open -T4 -p {port_str} {host} 2>/dev/null",
                shell=True,
                text=True,
                timeout=30
            )
            for line in out.splitlines():
                if "/tcp" in line and "open" in line:
                    results.append(f"{host} | {line.strip()}")
        except subprocess.TimeoutExpired:
            print(f"[!] nmap timed out for {host}")
        except subprocess.CalledProcessError:
            pass
        except Exception as e:
            print(f"[-] nmap error for {host}: {e}")

    try:
        with open(output_file, "w") as f:
            if results:
                for r in results:
                    f.write(r + "\n")
            else:
                f.write("No services confirmed.\n")
    except Exception as e:
        print(f"[-] Error saving results: {e}")

    print(f"[+] Services confirmed: {len(results)}")
    print(f"[+] Saved → {output_file}")
