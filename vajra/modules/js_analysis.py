import subprocess, os, re, urllib.request
from rich.console import Console
from core.utils import require_tool

console = Console()

# Patterns to find in JS files
SECRET_PATTERNS = [
    (r'api[_-]?key[\s]*[=:]+[\s]*["\']([A-Za-z0-9_\-]{20,})', "API Key"),
    (r'secret[\s]*[=:]+[\s]*["\']([A-Za-z0-9_\-]{20,})', "Secret"),
    (r'token[\s]*[=:]+[\s]*["\']([A-Za-z0-9_\-]{20,})', "Token"),
    (r'password[\s]*[=:]+[\s]*["\']([^\'"]{8,})', "Password"),
    (r'aws_access_key_id[\s]*[=:]+[\s]*["\']([A-Z0-9]{20})', "AWS Key"),
    (r'(https?://[a-zA-Z0-9._/-]+/api/[^\s"\']+)', "API Endpoint"),
    (r'(https?://[a-zA-Z0-9._/-]+/v[0-9]/[^\s"\']+)', "Versioned API"),
]

def analyze_js(domain):
    endpoints_file = f"output/{domain}/all_endpoints.txt"
    output_file    = f"output/{domain}/js_findings.txt"

    console.print("[cyan][+] Analyzing JS files for secrets & endpoints...[/cyan]")

    js_urls = []
    if os.path.exists(endpoints_file):
        with open(endpoints_file) as f:
            js_urls = [l.strip() for l in f if l.strip().endswith(".js")][:50]

    if not js_urls:
        console.print("[yellow][!] No JS files found in endpoints.[/yellow]")
        return

    console.print(f"[white]    Analyzing {len(js_urls)} JS files...[/white]")
    findings = []

    for url in js_urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                content = r.read().decode("utf-8", errors="ignore")
            for pattern, label in SECRET_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches[:3]:
                    findings.append(f"[{label}] {url} → {match[:80]}")
        except Exception:
            pass

    with open(output_file, "w") as f:
        for finding in findings:
            f.write(finding + "\n")

    if findings:
        console.print(f"[bold red][!] JS Findings: {len(findings)} potential secrets/endpoints found![/bold red]")
    else:
        console.print(f"[bold green][✓] JS Analysis: No obvious secrets found[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
