import subprocess
import os

from rich.console import Console
from core.utils import require_tool

console = Console()


def clean_hosts(input_file, clean_file):
    hosts = set()
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.replace("https://", "").replace("http://", "")
            line = line.split("/")[0].split(":")[0]
            if line:
                hosts.add(line)
    with open(clean_file, "w") as f:
        for h in sorted(hosts):
            f.write(h + "\n")
    return len(hosts)


def scan_ports(domain):
    input_file      = f"output/{domain}/live_subdomains.txt"
    clean_hosts_file= f"output/{domain}/clean_hosts.txt"
    masscan_output  = f"output/{domain}/masscan.txt"
    naabu_output    = f"output/{domain}/naabu.txt"
    final_output    = f"output/{domain}/open_ports.txt"

    host_count = clean_hosts(input_file, clean_hosts_file)
    console.print(f"[white][*] Scanning {host_count} hosts for open ports...[/white]")

    # ── Naabu (faster, recommended) ─────────────────────────
    naabu_bin = require_tool("naabu")
    if naabu_bin:
        console.print("[cyan][+] Running Naabu (top 1000 ports)...[/cyan]")
        subprocess.run(
            f"cat {clean_hosts_file} | {naabu_bin} -top-ports 1000 -silent -o {naabu_output} > /dev/null 2>&1",
            shell=True
        )

    # ── Masscan (raw socket, needs root) ────────────────────
    masscan_bin = require_tool("masscan")
    if masscan_bin:
        console.print("[cyan][+] Running Masscan (ports 1-65535, rate 500)...[/cyan]")
        sudo_prefix = "" if os.geteuid() == 0 else "sudo "
        subprocess.run(
            f"{sudo_prefix}{masscan_bin} -p1-65535 --rate 500 -iL {clean_hosts_file} -oL {masscan_output} > /dev/null 2>&1",
            shell=True
        )

    # ── Merge results ───────────────────────────────────────
    combined = set()

    if os.path.exists(naabu_output):
        with open(naabu_output) as f:
            for line in f:
                line = line.strip()
                if line:
                    combined.add(line)

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

    console.print(f"[bold green][✓] Open Ports Found: {len(combined)}[/bold green]")
    console.print(f"[white]    Saved → {final_output}[/white]")
