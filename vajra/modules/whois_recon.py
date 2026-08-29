import subprocess
import os

from rich.console import Console

console = Console()

IMPORTANT_KEYS = [
    "registrar", "registrant", "admin email", "tech email",
    "creation date", "expiry date", "expiration date",
    "updated date", "name server", "dnssec", "org"
]


def whois_recon(domain):
    output_dir  = f"output/{domain}"
    output_file = f"{output_dir}/whois.txt"
    os.makedirs(output_dir, exist_ok=True)

    print("\n[+] Running WHOIS Lookup...")

    try:
        raw = subprocess.check_output(
            f"whois {domain} 2>/dev/null",
            shell=True, text=True, timeout=15
        )
    except Exception as e:
        print(f"[-] WHOIS failed: {e}")
        return

    # Extract important lines only
    important = []
    seen = set()
    for line in raw.splitlines():
        line_lower = line.lower().strip()
        if not line_lower or line_lower.startswith("%") or line_lower.startswith("#"):
            continue
        for key in IMPORTANT_KEYS:
            if line_lower.startswith(key):
                clean = line.strip()
                if clean not in seen:
                    important.append(clean)
                    seen.add(clean)
                break

    if not important:
        print("[!] No useful WHOIS info found.")
    else:
        for line in important:
            print(f"    {line}")

    with open(output_file, "w") as f:
        f.write(f"WHOIS — {domain}\n")
        f.write("=" * 50 + "\n\n")
        for line in important:
            f.write(line + "\n")

    print(f"[+] WHOIS entries found: {len(important)}")
    print(f"[+] Saved → {output_file}")
