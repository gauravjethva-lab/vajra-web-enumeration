from core.setup_check import ensure_all_tools
from core.banner import start_banner

from modules.whois_recon   import whois_recon
from modules.dns_recon     import dns_recon
from modules.subdomains    import enumerate_subdomains
from modules.live_check    import check_live_subdomains
from modules.endpoints     import collect_endpoints
from modules.ports         import scan_ports
from modules.tech_detect   import detect_technologies
from modules.takeover_check import takeover_check
from modules.screenshot    import take_screenshots

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
        (1,  9, "WHOIS Reconnaissance",       whois_recon),
        (2,  9, "DNS Reconnaissance",         dns_recon),
        (3,  9, "Subdomain Enumeration",      enumerate_subdomains),
        (4,  9, "Live Host Detection",        check_live_subdomains),
        (5,  9, "Endpoint Collection",        collect_endpoints),
        (6,  9, "Port Scanning",              scan_ports),
        (7,  9, "Technology Fingerprinting",  detect_technologies),
        (8,  9, "Subdomain Takeover Check",   takeover_check),
        (9,  9, "Screenshots (Live + Dirs)",  take_screenshots),
    ]

    for num, total, title, func in stages:
        run_stage(num, total, title, func, domain)

    console.print("\n[bold bright_green][+] VAJRA Recon Pipeline Completed![/bold bright_green]")

    # Auto HTML Report
    report_script = os.path.join(os.path.dirname(__file__), "report_generator.py")
    if os.path.exists(report_script):
        console.print("\n[bold cyan][*] Generating HTML Report...[/bold cyan]")
        subprocess.run([sys.executable, report_script, domain])

    # Auto Markdown Summary
    summary_script = os.path.join(os.path.dirname(__file__), "recon_summary.py")
    if os.path.exists(summary_script):
        console.print("\n[bold cyan][*] Generating Markdown Summary...[/bold cyan]")
        subprocess.run([sys.executable, summary_script, domain])

    console.print(f"\n[bold green]Results saved in: output/{domain}/[/bold green]")


if __name__ == "__main__":
    main()
