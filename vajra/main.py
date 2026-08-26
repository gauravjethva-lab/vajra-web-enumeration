import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from core.setup_check import ensure_all_tools
from core.banner import start_banner
from modules.subdomains import enumerate_subdomains
from modules.live_check import check_live_subdomains
from modules.endpoints import collect_endpoints
from modules.ports import scan_ports
from modules.tech_detect import detect_technologies

console = Console()

def print_stage(num, total, title, icon):
    console.print(f"\n[bold bright_cyan]{'─'*55}[/bold bright_cyan]")
    console.print(f"[bold yellow] {icon} Stage [{num}/{total}] : {title}[/bold yellow]")
    console.print(f"[bold bright_cyan]{'─'*55}[/bold bright_cyan]\n")

def print_final_summary(domain, timings):
    table = Table(
        title="⚡ VAJRA Scan Summary",
        box=box.ROUNDED,
        border_style="bright_cyan",
        title_style="bold yellow",
        show_lines=True,
    )
    table.add_column("Stage", style="bold cyan", min_width=28)
    table.add_column("Status", style="bold green", justify="center")
    table.add_column("Time", style="white", justify="right")

    stages = [
        ("🔍 Subdomain Enumeration", "✅ Done"),
        ("🌐 Live Host Check",       "✅ Done"),
        ("🗺️  Endpoint Collection",  "✅ Done"),
        ("🔌 Port Scanning",         "✅ Done"),
        ("🧠 Tech Fingerprinting",   "✅ Done"),
    ]
    for (stage, status), t in zip(stages, timings):
        table.add_row(stage, status, f"{t:.1f}s")

    console.print(table)
    console.print(
        Panel(
            f"[bold green]✅ Recon Complete![/bold green]\n"
            f"[white]Results saved in:[/white] [bold cyan]output/{domain}/[/bold cyan]\n\n"
            f"[bold yellow]📊 HTML Report:[/bold yellow]  [white]python3 report_generator.py {domain}[/white]\n"
            f"[bold yellow]📋 MD Summary:[/bold yellow]   [white]python3 recon_summary.py {domain}[/white]",
            border_style="bright_green",
            box=box.ROUNDED,
            title="[bold bright_green]⚡ VAJRA COMPLETE[/bold bright_green]",
        )
    )

def main():
    ensure_all_tools()
    domain = start_banner()
    timings = []

    print_stage(1, 5, "Subdomain Enumeration", "🔍")
    t = time.time(); enumerate_subdomains(domain); timings.append(time.time() - t)

    print_stage(2, 5, "Live Host Detection", "🌐")
    t = time.time(); check_live_subdomains(domain); timings.append(time.time() - t)

    print_stage(3, 5, "Endpoint Collection", "🗺️")
    t = time.time(); collect_endpoints(domain); timings.append(time.time() - t)

    print_stage(4, 5, "Port Scanning", "🔌")
    t = time.time(); scan_ports(domain); timings.append(time.time() - t)

    print_stage(5, 5, "Technology Fingerprinting", "🧠")
    t = time.time(); detect_technologies(domain); timings.append(time.time() - t)

    print_final_summary(domain, timings)

if __name__ == "__main__":
    main()
