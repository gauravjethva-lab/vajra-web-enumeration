from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt
from rich.table import Table

import random
import time
import os
from urllib.parse import urlparse

# Fixed ASCII art - using simple reliable characters
VAJRA_ASCII = r"""
 __   __  ___     _______       ______     ___  
|  | |  ||   \   |   __  \    |   _  \   |   | 
|  |_|  ||    \  |  |__|  |   |  |_|  |  |   | 
|       ||     \ |      _/    |      _/   |   | 
 \     / |  |\  ||  |\  \___  |  |\  \    |   | 
  \___/  |__| \__||__| \_____|  |__| \__|  |___| 
"""

VAJRA_ASCII_V2 = """
██╗   ██╗ █████╗      ██╗██████╗  █████╗ 
██║   ██║██╔══██╗     ██║██╔══██╗██╔══██╗
██║   ██║███████║     ██║██████╔╝███████║
╚██╗ ██╔╝██╔══██║██   ██║██╔══██╗██╔══██║
 ╚████╔╝ ██║  ██║╚█████╔╝██████╔╝██║  ██║
  ╚═══╝  ╚═╝  ╚═╝ ╚════╝ ╚═════╝ ╚═╝  ╚═╝
"""


def sanitize_domain(raw_target):
    target = raw_target.strip()
    if "://" not in target:
        target = "http://" + target
    parsed = urlparse(target)
    host = parsed.netloc or parsed.path
    host = host.strip("/").split("/")[0]
    host = host.split(":")[0]   # remove port if any
    host = host.rstrip(".")
    return host


def start_banner():
    console = Console()

    colors = [
        "bright_cyan",
        "bright_magenta",
        "bright_green",
        "bright_yellow",
    ]
    selected_color = random.choice(colors)

    os.system("clear")

    # Print ASCII line by line with animation
    for line in VAJRA_ASCII_V2.splitlines():
        console.print(line, style=f"bold {selected_color}", highlight=False)
        time.sleep(0.04)

    # Subtitle text
    subtitle = Text()
    subtitle.append("⚡ Advanced Web Enumeration & Recon Framework ⚡\n", style="bold yellow")
    subtitle.append("Subdomain • LiveCheck • Endpoints • Ports • Tech", style="bold white")

    panel = Panel(
        Align.center(subtitle),
        border_style=selected_color,
        box=box.DOUBLE,
        padding=(1, 4),
        title="[bold orange1]⚡ VAJRA ⚡[/bold orange1]",
        subtitle="[bold white]v1.0.0 | Kali Linux Ready[/bold white]",
    )
    console.print(panel)

    # Info table
    info_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info_table.add_column(style="bold cyan")
    info_table.add_column(style="white")
    info_table.add_row("Author",  "Gaurav Jethva")
    info_table.add_row("GitHub",  "github.com/gauravjethva-lab/vajra-web-enumeration")
    info_table.add_row("Warning", "Use only on authorized targets!")
    console.print(Align.center(info_table))
    console.print()

    # Get target
    raw_target = Prompt.ask("[bold cyan][?][/bold cyan] Enter Domain or URL")
    target = sanitize_domain(raw_target)

    # Scan config panel
    target_panel = Panel(
        f"""
[bold green]TARGET[/bold green]  : [bold white]{target}[/bold white]
[bold yellow]MODE[/bold yellow]    : [bold white]Full Auto Recon Pipeline[/bold white]
[bold cyan]MODULES[/bold cyan] : [bold white]Subdomains → Live → Endpoints → Ports → Tech[/bold white]
[bold red]STATUS[/bold red]  : [bold white]Initializing...[/bold white]
""",
        border_style="bright_cyan",
        title="[bold yellow]⚡ SCAN CONFIGURATION[/bold yellow]",
        box=box.ROUNDED,
    )
    console.print(target_panel)

    # Loading animation
    modules = [
        ("🔍", "Subdomain Engine"),
        ("🌐", "Live Host Checker"),
        ("🗺️ ", "Endpoint Collector"),
        ("🔌", "Port Scanner"),
        ("🧠", "Tech Fingerprinter"),
    ]

    console.print()
    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20, style="cyan", complete_style="bright_green"),
        console=console,
    ) as progress:
        for icon, module in modules:
            task = progress.add_task(f"[cyan]Loading {icon} {module}...", total=10)
            for _ in range(10):
                time.sleep(0.03)
                progress.advance(task)
            progress.remove_task(task)

    console.print("\n[bold bright_green][✓] All modules loaded! Starting scan...[/bold bright_green]\n")
    return target
