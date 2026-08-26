import subprocess, os
from rich.console import Console
from core.utils import require_tool

console = Console()

DNS_RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA", "PTR"]

def dns_recon(domain):
    output_file = f"output/{domain}/dns_records.txt"
    dnsx_bin    = require_tool("dnsx")

    console.print("[cyan][+] Running DNS reconnaissance...[/cyan]")

    results = []

    # dnsx for bulk DNS resolution
    if dnsx_bin:
        subdomains_file = f"output/{domain}/final_subdomains.txt"
        dnsx_out = f"output/{domain}/dnsx.txt"
        subprocess.run(
            f"cat {subdomains_file} | {dnsx_bin} -silent -a -cname -mx -txt -resp -o {dnsx_out} > /dev/null 2>&1",
            shell=True, timeout=120
        )
        if os.path.exists(dnsx_out):
            with open(dnsx_out) as f:
                results += [l.strip() for l in f if l.strip()]

    # Manual dig for root domain records
    for rtype in DNS_RECORD_TYPES:
        try:
            out = subprocess.check_output(
                f"dig +short {rtype} {domain} 2>/dev/null",
                shell=True, text=True, timeout=5
            ).strip()
            if out:
                for line in out.splitlines():
                    results.append(f"{rtype}: {line.strip()}")
        except Exception:
            pass

    with open(output_file, "w") as f:
        for r in sorted(set(results)):
            f.write(r + "\n")

    console.print(f"[bold green][✓] DNS Records Found: {len(results)}[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
