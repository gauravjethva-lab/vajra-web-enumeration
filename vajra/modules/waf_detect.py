import subprocess, os
from rich.console import Console
from core.utils import require_tool

console = Console()

def detect_waf(domain):
    input_file  = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/waf_results.txt"

    wafw00f_bin = require_tool("wafw00f")
    if not wafw00f_bin:
        console.print("[yellow][!] wafw00f missing — skipping WAF detection.[/yellow]")
        return

    console.print("[cyan][+] Running WAF detection (wafw00f)...[/cyan]")

    results = []
    if os.path.exists(input_file):
        with open(input_file) as f:
            hosts = [l.strip() for l in f if l.strip()]

    for host in hosts[:20]:  # limit to 20 hosts for speed
        try:
            out = subprocess.check_output(
                f"{wafw00f_bin} {host} 2>/dev/null",
                shell=True, text=True, timeout=15
            )
            for line in out.splitlines():
                if "is behind" in line or "No WAF" in line:
                    results.append(f"{host}: {line.strip()}")
        except Exception:
            pass

    with open(output_file, "w") as f:
        for r in results:
            f.write(r + "\n")

    waf_found = sum(1 for r in results if "No WAF" not in r)
    console.print(f"[bold green][✓] WAF Detection Complete: {waf_found} WAFs found across {len(results)} hosts[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
