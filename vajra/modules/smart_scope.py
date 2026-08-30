"""
VAJRA Smart Scope
=================
Filters subdomains — prioritizes important ones for deep scanning.
Dev/staging/admin/api get priority. CDN/static get deprioritized.
"""

import os
from rich.console import Console

console = Console()

# High priority patterns — scan deeply
HIGH_PRIORITY = [
    "admin", "api", "dev", "staging", "stg", "test", "uat",
    "auth", "login", "sso", "oauth", "portal", "dashboard",
    "manage", "internal", "corp", "vpn", "remote", "secure",
    "app", "web", "service", "backend", "server", "prod",
    "git", "gitlab", "github", "jenkins", "ci", "deploy",
    "k8s", "kube", "monitor", "prometheus", "grafana",
    "db", "database", "mysql", "redis", "elastic", "kafka",
    "ftp", "smtp", "mail", "exchange",
]

# Low priority — skip deep scanning
LOW_PRIORITY = [
    "cdn", "static", "assets", "images", "img", "media",
    "fonts", "js", "css", "files", "download", "upload",
    "docs", "help", "support", "blog", "news", "www",
]


def classify_subdomain(sub):
    sub_lower = sub.lower()
    for pat in HIGH_PRIORITY:
        if pat in sub_lower:
            return "high"
    for pat in LOW_PRIORITY:
        if pat in sub_lower:
            return "low"
    return "medium"


def smart_scope(domain):
    subdomains_file = f"output/{domain}/final_subdomains.txt"
    high_file       = f"output/{domain}/scope_high.txt"
    medium_file     = f"output/{domain}/scope_medium.txt"
    low_file        = f"output/{domain}/scope_low.txt"
    priority_file   = f"output/{domain}/priority_targets.txt"

    print("\n[+] Running Smart Scope Analysis...")

    if not os.path.exists(subdomains_file):
        print("[-] No subdomains file found.")
        return

    with open(subdomains_file) as f:
        subdomains = [l.strip() for l in f if l.strip()]

    high, medium, low = [], [], []

    for sub in subdomains:
        priority = classify_subdomain(sub)
        if priority == "high":
            high.append(sub)
        elif priority == "medium":
            medium.append(sub)
        else:
            low.append(sub)

    # Save classified lists
    with open(high_file, "w") as f:
        for s in sorted(high): f.write(s + "\n")

    with open(medium_file, "w") as f:
        for s in sorted(medium): f.write(s + "\n")

    with open(low_file, "w") as f:
        for s in sorted(low): f.write(s + "\n")

    # Priority targets = high + medium (skip low for deep scans)
    priority_targets = high + medium
    with open(priority_file, "w") as f:
        for s in sorted(priority_targets): f.write(s + "\n")

    # Display
    console.print(f"\n[bold red]    🎯 High Priority  : {len(high)} subdomains[/bold red]")
    for s in high[:10]:
        console.print(f"[red]       → {s}[/red]")
    if len(high) > 10:
        console.print(f"[dim]       ... and {len(high)-10} more[/dim]")

    console.print(f"\n[bold yellow]    📋 Medium Priority: {len(medium)} subdomains[/bold yellow]")
    console.print(f"\n[bold dim]    📦 Low Priority    : {len(low)} subdomains (cdn/static)[/bold dim]")

    console.print(f"\n[bold green][✓] Smart Scope: {len(priority_targets)} priority targets identified[/bold green]")
    console.print(f"[white]    High priority targets → {high_file}[/white]")
    console.print(f"[white]    All priority targets  → {priority_file}[/white]")
