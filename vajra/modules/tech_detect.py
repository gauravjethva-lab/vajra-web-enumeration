import subprocess
import os

from rich.console import Console
from core.utils import require_tool

console = Console()


def detect_technologies(domain):
    input_file  = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/technologies.txt"

    whatweb_bin = require_tool("whatweb")
    if not whatweb_bin:
        return

    console.print("[cyan][+] Running WhatWeb (technology fingerprinting)...[/cyan]")

    subprocess.run(
        f"{whatweb_bin} -i {input_file} --no-errors --log-brief={output_file} > /dev/null 2>&1",
        shell=True
    )

    count = 0
    if os.path.exists(output_file):
        with open(output_file) as f:
            count = sum(1 for l in f if l.strip())

    console.print(f"[bold green][✓] Technology Results: {count} hosts fingerprinted[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
