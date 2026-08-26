import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Confirm

from core.setup_check import ensure_all_tools
from core.banner import start_banner

from modules.subdomains   import enumerate_subdomains
from modules.live_check   import check_live_subdomains
from modules.endpoints    import collect_endpoints
from modules.ports        import scan_ports
from modules.tech_detect  import detect_technologies
from modules.dns_recon    import dns_recon
from modules.waf_detect   import detect_waf
from modules.passive_recon import passive_recon
from modules.cors_check   import check_cors
from modules.js_analysis  import analyze_js
from modules.dir_bruteforce import bruteforce_dirs
from modules.screenshot   import take_screenshots

console = Console()

STAGES = [
    (1,  "Passive Recon (WHOIS/ASN/IP)",     "🌍", passive_recon),
    (2,  "DNS Reconnaissance",                "🔎", dns_recon),
    (3,  "Subdomain Enumeration",             "🔍", enumerate_subdomains),
    (4,  "Live Host Detection",               "🌐", check_live_subdomains),
    (5,  "WAF Detection",                     "🛡️", detect_waf),
    (6,  "Endpoint Collection",               "🗺️", collect_endpoints),
    (7,  "JS File Analysis",                  "📜", analyze_js),
    (8,  "CORS Misconfiguration Check",       "⚡", check_cors),
    (9,  "Port Scanning",                     "🔌", scan_ports),
    (10, "Technology Fingerprinting",         "🧠", detect_technologies),
    (11, "Directory Bruteforce",              "📂", bruteforce_dirs),
    (12, "Screenshots",                       "📸", take_screenshots),
]

def print_stage(num, total, title, icon):
    console.print(f"\n[bold bright_cyan]{'─'*58}[/bold bright_cyan]")
    console.print(f"[bold yellow] {icon} Stage [{num}/{total}] : {title}[/bold yellow]")
    console.print(f"[bold bright_cyan]{'─'*58}[/bold bright_cyan]\n")

def print_final_summary(domain, timings):
    table = Table(
        title="⚡ VAJRA Full Recon Summary",
        box=box.ROUNDED,
        border_style="bright_cyan",
        title_style="bold yellow",
        show_lines=True,
    )
    table.add_column("Stage", style="bold cyan", min_width=32)
    table.add_column("Status", style="bold green", justify="center")
    table.add_column("Time", style="white", justify="right")

    for (num, title, icon, _), t in zip(STAGES, timings):
        table.add_row(f"{icon} {title}", "✅ Done", f"{t:.1f}s")

    console.print(table)

    total_time = sum(timings)
    console.print(Panel(
        f"[bold green]✅ Full Recon Complete![/bold green]\n"
        f"[white]Total Time:[/white] [bold yellow]{total_time:.0f}s ({total_time/60:.1f} min)[/bold yellow]\n"
        f"[white]Results in:[/white] [bold cyan]output/{domain}/[/bold cyan]\n\n"
        f"[bold yellow]📊 HTML Report:[/bold yellow]  [white]python3 report_generator.py {domain}[/white]\n"
        f"[bold yellow]📋 MD Summary:[/bold yellow]   [white]python3 recon_summary.py {domain}[/white]",
        border_style="bright_green",
        box=box.ROUNDED,
        title="[bold bright_green]⚡ VAJRA COMPLETE[/bold bright_green]",
    ))

def main():
    ensure_all_tools()
    domain = start_banner()
    timings = []
    total = len(STAGES)

    for num, title, icon, func in STAGES:
        print_stage(num, total, title, icon)
        t = time.time()
        try:
            func(domain)
        except Exception as e:
            console.print(f"[red][-] {title} failed: {e}[/red]")
        timings.append(time.time() - t)

    print_final_summary(domain, timings)

if __name__ == "__main__":
    main()
