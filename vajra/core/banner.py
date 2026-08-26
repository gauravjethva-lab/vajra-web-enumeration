from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

import random
import time
import os
from urllib.parse import urlparse


VAJRA_ASCII = r"""
██╗   ██╗ █████╗      ██╗██████╗  █████╗
██║   ██║██╔══██╗     ██║██╔══██╗██╔══██╗
██║   ██║███████║     ██║██████╔╝███████║
╚██╗ ██╔╝██╔══██║██   ██║██╔══██╗██╔══██║
 ╚████╔╝ ██║  ██║╚█████╔╝██████╔╝██║  ██║
  ╚═══╝  ╚═╝  ╚═╝ ╚════╝ ╚═════╝ ╚═╝  ╚═╝
        ⚡ WEB ENUMERATION FRAMEWORK ⚡
             ॐ  VAJRA  ॐ
"""


def sanitize_domain(raw_target):
    """
    User agar 'https://www.example.com/path' jaisa kuch bhi de,
    isse saaf karke sirf 'www.example.com' (netloc) nikaal deta hai.
    Agar plain 'example.com' diya to wahi wapas milega.

    Ye function is liye add kiya gaya hai kyunki purane version mein
    raw input seedha folder path mein use ho raha tha, jisse
    'output/https:/www.example.com/' jaise broken nested folders
    ban rahe the.
    """

    target = raw_target.strip()

    if "://" not in target:
        target = "http://" + target

    parsed = urlparse(target)

    host = parsed.netloc or parsed.path

    host = host.strip("/").split("/")[0]

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

    for line in VAJRA_ASCII.splitlines():
        console.print(
            line,
            style=f"bold {selected_color}"
        )
        time.sleep(0.02)

    subtitle = Text()

    subtitle.append(
        "⚡ Advanced Recon Automation Framework ⚡\n",
        style="bold yellow"
    )

    subtitle.append(
        "Auto-installs missing tools • Kali Linux Ready",
        style="bold white"
    )

    panel = Panel(
        Align.center(subtitle),
        border_style=selected_color,
        box=box.DOUBLE,
        padding=(1, 4),
        title="[bold orange1]VAJRA[/bold orange1]",
        subtitle="[bold white]Web Enumeration Framework[/bold white]",
    )

    console.print(panel)

    raw_target = Prompt.ask(
        "\n[bold cyan][?][/bold cyan] Enter Domain or URL"
    )

    target = sanitize_domain(raw_target)

    target_panel = Panel(
        f"""
[bold green]TARGET[/bold green] : {target}

[bold yellow]MODE[/bold yellow] : Full Recon

[bold cyan]STATUS[/bold cyan] : Initializing
""",
        border_style="bright_cyan",
        title="[bold yellow]SCAN CONFIGURATION[/bold yellow]",
        box=box.ROUNDED,
    )

    console.print(target_panel)

    modules = [
        "Loading Subdomain Engine",
        "Loading Alive Checker",
        "Loading Endpoint Collector",
        "Loading Port Scanner",
        "Loading Tech Fingerprinter",
    ]

    console.print()

    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn(
            "[progress.description]{task.description}"
        ),
        console=console,
    ) as progress:

        for module in modules:

            task = progress.add_task(
                f"[cyan]{module}...",
                total=None
            )

            time.sleep(0.4)

            progress.remove_task(task)

    console.print(
        "\n[bold bright_green][✓][/bold bright_green] All modules loaded successfully!\n"
    )

    return target
