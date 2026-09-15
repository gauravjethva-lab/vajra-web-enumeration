from core.setup_check import ensure_all_tools
from core.banner import start_banner

from modules.subdomains    import enumerate_subdomains
from modules.live_check    import check_live_subdomains
from modules.endpoints     import collect_endpoints
from modules.ports         import scan_ports
from modules.service_detect import detect_services
from modules.tech_detect   import detect_technologies
from modules.js_cors_check import run_js_cors_check
from modules.nuclei_scan   import nuclei_scan

from rich.console import Console
import os, subprocess, sys

console = Console()


def run_stage(num, total, title, func, domain):
    console.print(f"\n[bold bright_cyan]{'─'*58}[/bold bright_cyan]")
    console.print(f"[bold yellow] Stage [{num}/{total}] : {title}[/bold yellow]")
    console.print(f"[bold bright_cyan]{'─'*58}[/bold bright_cyan]\n")
    try:
        func(domain)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        console.print(f"[red][-] {title} error: {e}[/red]")


def main():
    ensure_all_tools()
    domain = start_banner()

    stages = [
        (1, 8, "Subdomain Enumeration",       enumerate_subdomains),
        (2, 8, "Live Host Detection",          check_live_subdomains),
        (3, 8, "Endpoint Collection",          collect_endpoints),
        (4, 8, "Port Scanning",               scan_ports),
        (5, 8, "Service Detection (nmap -sV)", detect_services),
        (6, 8, "Technology Fingerprinting",    detect_technologies),
        (7, 8, "JS Secrets + CORS Check",      run_js_cors_check),
        (8, 8, "Nuclei Vulnerability Scan",    nuclei_scan),
    ]

    for num, total, title, func in stages:
        run_stage(num, total, title, func, domain)

    console.print("\n[bold bright_green][+] VAJRA Recon Pipeline Completed![/bold bright_green]")

    # Auto HTML Report
    report_script = os.path.join(os.path.dirname(__file__), "report_generator.py")
    if os.path.exists(report_script):
        console.print("\n[bold cyan][*] Generating HTML Report...[/bold cyan]")
        subprocess.run([sys.executable, report_script, domain])

    console.print(f"\n[bold green]Results saved in: output/{domain}/[/bold green]")


if __name__ == "__main__":
    main()
