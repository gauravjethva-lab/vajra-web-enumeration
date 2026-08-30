"""
VAJRA Nuclei Integration
========================
Runs nuclei templates on live hosts.
Auto-installs nuclei if missing.
"""

import subprocess
import os
import shutil
from rich.console import Console
from core.utils import require_tool

console = Console()


def nuclei_scan(domain):
    live_file   = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/nuclei_findings.txt"

    print("\n[+] Running Nuclei Vulnerability Scan...")

    nuclei_bin = require_tool("nuclei")
    if not nuclei_bin:
        console.print("[yellow][!] nuclei not found. Install:[/yellow]")
        console.print("[white]    go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest[/white]")
        console.print("[white]    Then run: nuclei -update-templates[/white]")
        return

    if not os.path.exists(live_file):
        print("[-] No live hosts file found.")
        return

    # Count live hosts
    with open(live_file) as f:
        hosts = [l.strip().split()[0] for l in f if l.strip() and l.strip().startswith("http")]

    if not hosts:
        print("[-] No live hosts to scan.")
        return

    console.print(f"[cyan][+] Running nuclei on {len(hosts)} live hosts...[/cyan]")
    console.print(f"[dim]    Templates: cves, exposures, misconfigurations, takeovers[/dim]")

    # Write hosts to temp file
    hosts_file = f"output/{domain}/_nuclei_hosts.txt"
    with open(hosts_file, "w") as f:
        for h in hosts:
            f.write(h + "\n")

    try:
        result = subprocess.run(
            f"{nuclei_bin} "
            f"-l {hosts_file} "
            f"-t cves,exposures,misconfigurations,takeovers "
            f"-severity critical,high,medium "
            f"-silent "
            f"-o {output_file} "
            f"-timeout 10 "
            f"-c 25 "
            f"2>/dev/null",
            shell=True, timeout=600
        )
        os.remove(hosts_file)
    except subprocess.TimeoutExpired:
        console.print("[yellow][!] Nuclei timed out — using partial results.[/yellow]")
        if os.path.exists(hosts_file):
            os.remove(hosts_file)

    # Count findings
    count = 0
    critical = high = medium = 0
    if os.path.exists(output_file):
        with open(output_file) as f:
            for line in f:
                count += 1
                line_lower = line.lower()
                if "critical" in line_lower: critical += 1
                elif "high" in line_lower:   high += 1
                elif "medium" in line_lower: medium += 1

    if count > 0:
        console.print(f"\n[bold red][!] Nuclei Findings: {count} total[/bold red]")
        if critical: console.print(f"[bold red]    CRITICAL: {critical}[/bold red]")
        if high:     console.print(f"[bold red]    HIGH    : {high}[/bold red]")
        if medium:   console.print(f"[bold yellow]    MEDIUM  : {medium}[/bold yellow]")
    else:
        console.print(f"\n[bold green][✓] Nuclei: No findings detected[/bold green]")

    console.print(f"[white]    Saved → {output_file}[/white]")
