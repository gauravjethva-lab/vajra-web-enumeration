import subprocess
import os
import threading

from core.utils import require_tool


def run_command(command, timeout=300):
    try:
        result = subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
        return [l.strip() for l in result.splitlines() if l.strip()]
    except subprocess.TimeoutExpired:
        print(f"[!] Command timed out: {command[:60]}")
        return []
    except subprocess.CalledProcessError:
        return []
    except Exception:
        return []


def save_results(filepath, data):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            for item in sorted(set(data)):
                f.write(item + "\n")
    except Exception as e:
        print(f"[-] Could not save {filepath}: {e}")


def enumerate_subdomains(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[+] Target: {domain}")

    subfinder_results = []
    amass_results     = []

    subfinder_bin = require_tool("subfinder")
    amass_bin     = require_tool("amass")

    def run_subfinder():
        nonlocal subfinder_results
        if not subfinder_bin:
            return
        print("[+] Running Subfinder...")
        subfinder_results = run_command(
            f"{subfinder_bin} -d {domain} -silent",
            timeout=300
        )
        save_results(f"{output_dir}/subfinder.txt", subfinder_results)
        print(f"[+] Subfinder found: {len(subfinder_results)} subdomains")

    def run_amass():
        nonlocal amass_results
        if not amass_bin:
            return
        print("[+] Running Amass...")
        amass_results = run_command(
            f"{amass_bin} enum -passive -d {domain}",
            timeout=300
        )
        save_results(f"{output_dir}/amass.txt", amass_results)
        print(f"[+] Amass found: {len(amass_results)} subdomains")

    t1 = threading.Thread(target=run_subfinder)
    t2 = threading.Thread(target=run_amass)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("[+] Removing duplicates...")

    final_results = sorted(set(subfinder_results + amass_results))

    if not final_results:
        final_results = [domain]

    save_results(f"{output_dir}/final_subdomains.txt", final_results)

    print(f"[+] Total Unique Subdomains: {len(final_results)}")
    print(f"[+] Results saved in {output_dir}")

    return final_results
