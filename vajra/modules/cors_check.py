import urllib.request, urllib.error, os
from rich.console import Console

console = Console()

def check_cors(domain):
    input_file  = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/cors_issues.txt"

    console.print("[cyan][+] Checking for CORS misconfigurations...[/cyan]")

    issues = []
    hosts = []
    if os.path.exists(input_file):
        with open(input_file) as f:
            hosts = [l.strip().split()[0] for l in f if l.strip()][:20]

    for host in hosts:
        try:
            req = urllib.request.Request(
                host,
                headers={
                    "Origin": "https://evil.com",
                    "User-Agent": "Mozilla/5.0"
                }
            )
            with urllib.request.urlopen(req, timeout=8) as r:
                headers = dict(r.headers)
                acao = headers.get("Access-Control-Allow-Origin", "")
                acac = headers.get("Access-Control-Allow-Credentials", "")

                if acao == "*":
                    issues.append(f"[WILDCARD CORS] {host} → ACAO: *")
                elif "evil.com" in acao:
                    if acac.lower() == "true":
                        issues.append(f"[CRITICAL - CORS+CREDS] {host} → Reflects origin + credentials!")
                    else:
                        issues.append(f"[CORS REFLECT] {host} → Reflects arbitrary origin")
        except Exception:
            pass

    with open(output_file, "w") as f:
        for issue in issues:
            f.write(issue + "\n")

    if issues:
        console.print(f"[bold red][!] CORS Issues Found: {len(issues)}![/bold red]")
    else:
        console.print(f"[bold green][✓] CORS Check: No obvious misconfigurations[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
