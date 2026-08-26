import subprocess, os, threading
from rich.console import Console
from core.utils import require_tool

console = Console()

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
        return [l.strip() for l in result.splitlines() if l.strip()]
    except subprocess.CalledProcessError:
        return []

def save_results(filepath, data):
    with open(filepath, "w") as f:
        for item in sorted(set(data)):
            f.write(item + "\n")

def enumerate_subdomains(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    console.print(f"[bold white][*] Target: [bold cyan]{domain}[/bold cyan][/bold white]")

    subfinder_results, amass_results = [], []
    subfinder_bin = require_tool("subfinder")
    amass_bin     = require_tool("amass")

    def run_subfinder():
        nonlocal subfinder_results
        if not subfinder_bin: return
        console.print("[cyan][+] Running Subfinder...[/cyan]")
        subfinder_results = run_command(f"{subfinder_bin} -d {domain} -silent")
        save_results(f"{output_dir}/subfinder.txt", subfinder_results)
        console.print(f"[green][✓] Subfinder: {len(subfinder_results)} subdomains[/green]")

    def run_amass():
        nonlocal amass_results
        if not amass_bin: return
        console.print("[cyan][+] Running Amass (passive)...[/cyan]")
        amass_results = run_command(f"{amass_bin} enum -passive -d {domain}")
        save_results(f"{output_dir}/amass.txt", amass_results)
        console.print(f"[green][✓] Amass: {len(amass_results)} subdomains[/green]")

    t1 = threading.Thread(target=run_subfinder)
    t2 = threading.Thread(target=run_amass)
    t1.start(); t2.start()
    t1.join();  t2.join()

    final_results = sorted(set(subfinder_results + amass_results)) or [domain]
    save_results(f"{output_dir}/final_subdomains.txt", final_results)
    console.print(f"\n[bold green][✓] Total Unique Subdomains: {len(final_results)}[/bold green]")
    console.print(f"[white]    Saved → output/{domain}/final_subdomains.txt[/white]")
    return final_results
