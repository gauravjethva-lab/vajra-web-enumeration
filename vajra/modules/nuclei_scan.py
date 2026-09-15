import subprocess
import os
import shutil
from core.utils import require_tool


def nuclei_scan(domain):
    live_file   = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/nuclei_findings.txt"

    print("\n[+] Running Nuclei Vulnerability Scan...")

    if not os.path.exists(live_file):
        print(f"[-] Input file not found: {live_file}")
        try:
            open(output_file, "w").close()
        except Exception:
            pass
        return

    nuclei_bin = require_tool("nuclei")
    if not nuclei_bin:
        print("[!] nuclei not found — install:")
        print("    go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest")
        print("    nuclei -update-templates")
        try:
            open(output_file, "w").close()
        except Exception:
            pass
        return

    # Extract clean URLs from live_subdomains.txt
    hosts = []
    try:
        with open(live_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                url = line.split()[0]
                if url.startswith("http"):
                    hosts.append(url)
    except Exception as e:
        print(f"[-] Error reading live hosts: {e}")
        return

    if not hosts:
        print("[-] No live hosts to scan.")
        open(output_file, "w").close()
        return

    # Write hosts to temp file
    hosts_tmp = f"output/{domain}/_nuclei_tmp.txt"
    try:
        with open(hosts_tmp, "w") as f:
            for h in hosts:
                f.write(h + "\n")
    except Exception as e:
        print(f"[-] Error writing temp file: {e}")
        return

    print(f"[+] Scanning {len(hosts)} hosts with nuclei...")
    print(f"    Templates: cves, exposures, misconfigurations, takeovers")

    try:
        subprocess.run(
            f"{nuclei_bin} "
            f"-l {hosts_tmp} "
            f"-t cves,exposures,misconfigurations,takeovers "
            f"-severity critical,high,medium "
            f"-silent "
            f"-o {output_file} "
            f"-timeout 10 "
            f"-c 25 "
            f"> /dev/null 2>&1",
            shell=True,
            timeout=600
        )
    except subprocess.TimeoutExpired:
        print("[!] Nuclei timed out — using partial results.")
    except Exception as e:
        print(f"[-] Nuclei error: {e}")
    finally:
        try:
            if os.path.exists(hosts_tmp):
                os.remove(hosts_tmp)
        except Exception:
            pass

    # Count and display findings
    critical = high = medium = total = 0
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                for line in f:
                    if line.strip():
                        total += 1
                        ll = line.lower()
                        if "critical" in ll:
                            critical += 1
                        elif "high" in ll:
                            high += 1
                        elif "medium" in ll:
                            medium += 1
        except Exception:
            pass

    if total > 0:
        print(f"[!] Nuclei Findings: {total} total")
        if critical:
            print(f"    CRITICAL : {critical}")
        if high:
            print(f"    HIGH     : {high}")
        if medium:
            print(f"    MEDIUM   : {medium}")
    else:
        print("[+] Nuclei: No findings detected")

    print(f"[+] Saved → {output_file}")
