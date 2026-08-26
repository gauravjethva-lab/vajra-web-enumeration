import subprocess
import os

from rich.console import Console
from core.utils import require_tool

console = Console()


def check_live_subdomains(domain):
    input_file  = f"output/{domain}/final_subdomains.txt"
    output_file = f"output/{domain}/live_subdomains.txt"

    console.print("[cyan][+] Running httpx to find live hosts...[/cyan]")

    httpx_bin = require_tool("httpx")

    if not httpx_bin:
        with open(input_file) as src, open(output_file, "w") as dst:
            dst.write(src.read())
        console.print("[yellow][!] httpx missing — using all subdomains as fallback.[/yellow]")
        return

    command = (
        f"cat {input_file} | "
        f"{httpx_bin} "
        f"-silent "
        f"-threads 50 "
        f"-timeout 10 "
        f"-status-code "
        f"-title "
        f"-o {output_file} "
        f"> /dev/null 2>&1"
    )
    subprocess.run(command, shell=True)

    # Count results
    count = 0
    if os.path.exists(output_file):
        with open(output_file) as f:
            count = sum(1 for l in f if l.strip())

    console.print(f"[bold green][✓] Live Hosts Found: {count}[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
