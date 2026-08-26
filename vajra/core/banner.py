from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt
from rich.table import Table
import random, time, os
from urllib.parse import urlparse

console = Console()

VAJRA_ASCII = (
    " __   __ _____    _  ____   ___ \n"
    " \\ \\ / /|  _  |  | ||  _ \\ /   |\n"
    "  \\ V / | |_| |  | || |_) | () |\n"
    "   \\_/  |_____|  | ||____/  \\___|\n"
    "                 |_|             \n"
)

VAJRA_LETTERS = [
    "██╗   ██╗",
    "██║   ██║",
    "██║   ██║",
    "╚██╗ ██╔╝",
    " ╚████╔╝ ",
    "  ╚═══╝  ",
]

def sanitize_domain(raw_target):
    target = raw_target.strip()
    if "://" not in target:
        target = "http://" + target
    parsed = urlparse(target)
    host = parsed.netloc or parsed.path
    host = host.strip("/").split("/")[0].split(":")[0].rstrip(".")
    return host

def start_banner():
    colors = ["bright_cyan", "bright_magenta", "bright_green", "bright_yellow"]
    color = random.choice(colors)
    os.system("clear")

    # Simple text-based banner that renders perfectly everywhere
    banner_lines = [
        "",
        "  ██╗   ██╗ █████╗      ██╗██████╗  █████╗  ",
        "  ██║   ██║██╔══██╗     ██║██╔══██╗██╔══██╗ ",
        "  ██║   ██║███████║     ██║██████╔╝███████║  ",
        "  ╚██╗ ██╔╝██╔══██║██╗ ██║██╔══██╗██╔══██║  ",
        "   ╚████╔╝ ██║  ██║╚█████╔╝██║  ██║██║  ██║  ",
        "    ╚═══╝  ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ",
        "",
    ]

    for line in banner_lines:
        console.print(line, style=f"bold {color}", highlight=False)
        time.sleep(0.03)

    subtitle = Text()
    subtitle.append("⚡ Advanced Web Enumeration & Recon Framework ⚡\n", style="bold yellow")
    subtitle.append("Subdomain  •  LiveCheck  •  Endpoints  •  Ports  •  Tech", style="bold white")

    console.print(Panel(
        Align.center(subtitle),
        border_style=color,
        box=box.DOUBLE,
        padding=(1, 4),
        title="[bold orange1]⚡ VAJRA ⚡[/bold orange1]",
        subtitle="[bold white]v1.1.0 | Kali Linux Ready[/bold white]",
    ))

    info = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info.add_column(style="bold cyan")
    info.add_column(style="white")
    info.add_row("Author",  "Gaurav Jethva")
    info.add_row("GitHub",  "github.com/gauravjethva-lab/vajra-web-enumeration")
    info.add_row("⚠️  Warning", "Use only on authorized targets!")
    console.print(Align.center(info))
    console.print()

    raw_target = Prompt.ask("[bold cyan][?][/bold cyan] Enter Domain or URL")
    target = sanitize_domain(raw_target)

    console.print(Panel(
        f"\n[bold green]TARGET[/bold green]  : [bold white]{target}[/bold white]\n"
        f"[bold yellow]MODE[/bold yellow]    : [bold white]Full Auto Recon Pipeline[/bold white]\n"
        f"[bold cyan]MODULES[/bold cyan] : [bold white]Subdomains → Live → Endpoints → Ports → Tech[/bold white]\n"
        f"[bold red]STATUS[/bold red]  : [bold white]Initializing...[/bold white]\n",
        border_style="bright_cyan",
        title="[bold yellow]⚡ SCAN CONFIGURATION[/bold yellow]",
        box=box.ROUNDED,
    ))

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
        BarColumn(bar_width=25, style="cyan", complete_style="bright_green"),
        console=console,
    ) as progress:
        for icon, name in modules:
            task = progress.add_task(f"[cyan]Loading {icon} {name}...", total=10)
            for _ in range(10):
                time.sleep(0.03)
                progress.advance(task)
            progress.remove_task(task)

    console.print("\n[bold bright_green][✓] All modules loaded! Starting scan...[/bold bright_green]\n")
    return target
