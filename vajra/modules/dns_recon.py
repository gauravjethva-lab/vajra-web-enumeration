import subprocess
import os

from rich.console import Console

console = Console()

DNS_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]


def run_dig(domain, record_type):
    try:
        out = subprocess.check_output(
            f"dig +short {record_type} {domain} 2>/dev/null",
            shell=True, text=True, timeout=8
        ).strip()
        return [l.strip() for l in out.splitlines() if l.strip()]
    except Exception:
        return []


def dns_recon(domain):
    output_dir  = f"output/{domain}"
    output_file = f"{output_dir}/dns_records.txt"
    os.makedirs(output_dir, exist_ok=True)

    print("\n[+] Running DNS Reconnaissance...")

    results = []

    for rtype in DNS_TYPES:
        records = run_dig(domain, rtype)
        for r in records:
            results.append(f"{rtype}: {r}")
            print(f"    [{rtype}] {r}")

    if not results:
        print("[!] No DNS records found.")

    with open(output_file, "w") as f:
        for r in results:
            f.write(r + "\n")

    print(f"[+] DNS Records Found  : {len(results)}")
    print(f"[+] Saved → {output_file}")
