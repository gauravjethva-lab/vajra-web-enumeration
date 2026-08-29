from core.setup_check import ensure_all_tools
from core.banner import start_banner

from modules.subdomains import enumerate_subdomains
from modules.live_check import check_live_subdomains
from modules.endpoints import collect_endpoints
from modules.ports import scan_ports
from modules.tech_detect import detect_technologies

from rich.console import Console
import os, subprocess, sys

console = Console()


def main():
    ensure_all_tools()
    domain = start_banner()

    enumerate_subdomains(domain)
    check_live_subdomains(domain)
    collect_endpoints(domain)
    scan_ports(domain)
    detect_technologies(domain)

    console.print("\n[bold bright_green][+] VAJRA Recon Pipeline Completed Successfully![/bold bright_green]")

    # Auto-generate HTML report
    report_script = os.path.join(os.path.dirname(__file__), "report_generator.py")
    if os.path.exists(report_script):
        console.print(f"\n[bold cyan][*] Generating HTML Report...[/bold cyan]")
        subprocess.run([sys.executable, report_script, domain])


if __name__ == "__main__":
    main()
