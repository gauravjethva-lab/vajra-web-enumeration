import subprocess, os
from rich.console import Console
from core.utils import require_tool

console = Console()

def take_screenshots(domain):
    input_file  = f"output/{domain}/live_subdomains.txt"
    output_dir  = f"output/{domain}/screenshots"
    os.makedirs(output_dir, exist_ok=True)

    gowitness_bin = require_tool("gowitness")
    if not gowitness_bin:
        console.print("[yellow][!] gowitness missing — skipping screenshots.[/yellow]")
        return

    console.print("[cyan][+] Taking screenshots of live hosts (gowitness)...[/cyan]")

    subprocess.run(
        f"{gowitness_bin} file -f {input_file} --screenshot-path {output_dir} --timeout 10 > /dev/null 2>&1",
        shell=True, timeout=600
    )

    count = len([f for f in os.listdir(output_dir) if f.endswith(".png")])
    console.print(f"[bold green][✓] Screenshots Captured: {count}[/bold green]")
    console.print(f"[white]    Saved → {output_dir}/[/white]")
