from core.setup_check import ensure_all_tools
from core.banner import start_banner
from modules.subdomains  import enumerate_subdomains
from modules.live_check  import check_live_subdomains
from modules.endpoints   import collect_endpoints
from modules.ports       import scan_ports
from modules.tech_detect import detect_technologies
from rich.console import Console
import os, subprocess, sys

console = Console()

def run_stage(num, total, title, func, domain):
    console.print(f"\n[bold bright_cyan]{'─'*55}[/bold bright_cyan]")
    console.print(f"[bold yellow] Stage [{num}/{total}] : {title}[/bold yellow]")
    console.print(f"[bold bright_cyan]{'─'*55}[/bold bright_cyan]\n")
    func(domain)

def main():
    ensure_all_tools()
    domain = start_banner()
    stages = [
        (1,5,"Subdomain Enumeration",  enumerate_subdomains),
        (2,5,"Live Host Detection",    check_live_subdomains),
        (3,5,"Endpoint Collection",    collect_endpoints),
        (4,5,"Port Scanning",          scan_ports),
        (5,5,"Technology Fingerprint", detect_technologies),
    ]
    for num, total, title, func in stages:
        run_stage(num, total, title, func, domain)
    console.print("\n[bold bright_green][+] VAJRA Recon Pipeline Completed![/bold bright_green]")
    report_script = os.path.join(os.path.dirname(__file__), "report_generator.py")
    if os.path.exists(report_script):
        console.print("\n[bold cyan][*] Generating HTML Report...[/bold cyan]")
        subprocess.run([sys.executable, report_script, domain])
    console.print(f"\n[bold green]Results saved in: output/{domain}/[/bold green]")

if __name__ == "__main__":
    main()
