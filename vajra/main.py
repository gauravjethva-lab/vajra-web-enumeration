import os
import sys
import time
import subprocess
from rich.console import Console
from rich.prompt import Confirm
from rich import box
from rich.table import Table

from core.setup_check import ensure_all_tools
from core.banner import start_banner
from core.cache import cache_exists, save_cache, get_cache_info, clear_cache
from core.resume import mark_done, is_done, clear_progress, show_progress

from modules.whois_recon    import whois_recon
from modules.dns_recon      import dns_recon
from modules.subdomains     import enumerate_subdomains
from modules.live_check     import check_live_subdomains
from modules.smart_scope    import smart_scope
from modules.endpoints      import collect_endpoints
from modules.ssl_analysis   import ssl_analysis
from modules.ports          import scan_ports
from modules.tech_detect    import detect_technologies
from modules.takeover_check import takeover_check
from modules.nuclei_scan    import nuclei_scan
from modules.google_dork    import generate_dorks
from modules.email_recon    import email_recon
from modules.screenshot     import take_screenshots

console = Console()

STAGES = [
    ("whois",       "WHOIS Reconnaissance",      "🌍", whois_recon),
    ("dns",         "DNS Reconnaissance",         "🔎", dns_recon),
    ("subdomains",  "Subdomain Enumeration",      "🔍", enumerate_subdomains),
    ("scope",       "Smart Scope Analysis",       "🎯", smart_scope),
    ("live",        "Live Host Detection",        "🌐", check_live_subdomains),
    ("ssl",         "SSL/TLS Analysis",           "🔐", ssl_analysis),
    ("endpoints",   "Endpoint Collection",        "🗺️", collect_endpoints),
    ("email",       "Email & Breach Recon",       "📧", email_recon),
    ("dorks",       "Google Dork Generation",     "🕵️", generate_dorks),
    ("ports",       "Port Scanning & Validation", "🔌", scan_ports),
    ("tech",        "Technology Fingerprinting",  "🧠", detect_technologies),
    ("nuclei",      "Nuclei Vulnerability Scan",  "🔴", nuclei_scan),
    ("takeover",    "Subdomain Takeover Check",   "🔗", takeover_check),
    ("screenshots", "Screenshots",                "📸", take_screenshots),
]


def print_stage(num, total, title, icon, cached=False, skipped=False):
    status = "[bold yellow](CACHED — SKIPPING)[/bold yellow]" if cached else \
             "[bold dim](SKIPPING)[/bold dim]" if skipped else ""
    console.print(f"\n[bold bright_cyan]{'─'*58}[/bold bright_cyan]")
    console.print(f"[bold yellow] {icon} Stage [{num}/{total}] : {title}[/bold yellow] {status}")
    console.print(f"[bold bright_cyan]{'─'*58}[/bold bright_cyan]\n")


def print_summary(domain, timings):
    table = Table(
        title="⚡ VAJRA Scan Summary",
        box=box.ROUNDED,
        border_style="bright_cyan",
        title_style="bold yellow",
        show_lines=True,
    )
    table.add_column("Stage", style="bold cyan", min_width=30)
    table.add_column("Status", justify="center")
    table.add_column("Time", style="white", justify="right")

    for (key, title, icon, _), (status, t) in zip(STAGES, timings):
        color = "green" if status == "done" else "yellow" if status == "cached" else "dim"
        label = "✅ Done" if status == "done" else "⚡ Cached" if status == "cached" else "⏭️  Skipped"
        table.add_row(f"{icon} {title}", f"[{color}]{label}[/{color}]", f"{t:.1f}s")

    console.print(table)
    total_time = sum(t for _, t in timings)
    console.print(f"\n[bold green]Total Time: {total_time:.0f}s ({total_time/60:.1f} min)[/bold green]")
    console.print(f"[bold green]Results   : output/{domain}/[/bold green]\n")


def main():
    ensure_all_tools()
    domain = start_banner()

    total = len(STAGES)

    # Check for previous incomplete scan
    progress = show_progress(domain)
    resume_mode = False
    if progress:
        completed_stages = list(progress.keys())
        console.print(f"\n[bold yellow][*] Previous scan found for {domain}[/bold yellow]")
        console.print(f"[white]    Completed stages: {', '.join(completed_stages)}[/white]")
        resume_mode = Confirm.ask("[bold cyan]Resume from where it stopped?[/bold cyan]", default=True)
        if not resume_mode:
            clear_progress(domain)
            console.print("[dim]Starting fresh scan...[/dim]")

    # Cache check
    cached_stages = get_cache_info(domain)
    use_cache = False
    if cached_stages and not resume_mode:
        console.print(f"\n[bold yellow][*] Cached results found for: {', '.join(cached_stages)}[/bold yellow]")
        use_cache = Confirm.ask("[bold cyan]Use cached results for unchanged stages?[/bold cyan]", default=True)

    timings = []

    for num, (key, title, icon, func) in enumerate(STAGES, 1):

        # Resume check
        if resume_mode and is_done(domain, key):
            print_stage(num, total, title, icon, skipped=True)
            console.print(f"[dim]    Already completed — skipping.[/dim]")
            timings.append(("cached", 0.0))
            continue

        # Cache check
        if use_cache and cache_exists(domain, key):
            print_stage(num, total, title, icon, cached=True)
            timings.append(("cached", 0.0))
            continue

        print_stage(num, total, title, icon)
        t = time.time()
        try:
            func(domain)
            elapsed = time.time() - t
            timings.append(("done", elapsed))
            mark_done(domain, key)
            save_cache(domain, key, [])
        except KeyboardInterrupt:
            console.print(f"\n[bold red][!] Interrupted at Stage {num}: {title}[/bold red]")
            console.print(f"[yellow][*] Progress saved — run again to resume.[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[red][-] {title} failed: {e}[/red]")
            timings.append(("done", time.time() - t))
            mark_done(domain, key)

    print_summary(domain, timings)

    # Auto-generate reports
    report_script  = os.path.join(os.path.dirname(__file__), "report_generator.py")
    summary_script = os.path.join(os.path.dirname(__file__), "recon_summary.py")

    if os.path.exists(report_script):
        console.print("[bold cyan][*] Generating HTML Report...[/bold cyan]")
        subprocess.run([sys.executable, report_script, domain])

    if os.path.exists(summary_script):
        console.print("[bold cyan][*] Generating Markdown Summary...[/bold cyan]")
        subprocess.run([sys.executable, summary_script, domain])

    # Clear resume state after successful full scan
    clear_progress(domain)
    console.print(f"\n[bold bright_green]⚡ VAJRA Complete! Results → output/{domain}/[/bold bright_green]\n")


if __name__ == "__main__":
    main()
