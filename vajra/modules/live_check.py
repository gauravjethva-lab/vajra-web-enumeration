import subprocess, os
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

    subprocess.run(
        f"cat {input_file} | {httpx_bin} -silent -threads 50 -timeout 10 -status-code -title -o {output_file} > /dev/null 2>&1",
        shell=True
    )

    count = 0
    if os.path.exists(output_file):
        with open(output_file) as f:
            count = sum(1 for l in f if l.strip())

    console.print(f"[bold green][✓] Live Hosts Found: {count}[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
