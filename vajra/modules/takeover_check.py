import subprocess
import os
import urllib.request
import urllib.error
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console

console = Console()

TAKEOVER_FINGERPRINTS = {
    "github.io":          "There isn't a GitHub Pages site here",
    "herokuapp.com":      "No such app",
    "s3.amazonaws.com":   "NoSuchBucket",
    "s3-website":         "NoSuchBucket",
    "amazonaws.com":      "NoSuchBucket",
    "azurewebsites.net":  "404 Web Site not found",
    "cloudapp.net":       "404 Web Site not found",
    "fastly.net":         "Fastly error: unknown domain",
    "pantheon.io":        "404 error unknown site",
    "zendesk.com":        "Help Center Closed",
    "freshdesk.com":      "May be for sale",
    "readme.io":          "Project doesnt exist",
    "surge.sh":           "project not found",
    "bitbucket.io":       "Repository not found",
    "ghost.io":           "404",
    "helpjuice.com":      "We could not find what you're looking for",
    "helpscoutdocs.com":  "No settings were found",
    "cargo.site":         "If you're moving your domain away from Cargo",
    "launchrock.com":     "It looks like you may have taken a wrong turn",
    "smugmug.com":        "Page Not Found",
    "strikingly.com":     "page not found",
    "tumblr.com":         "There's nothing here",
    "unbounce.com":       "The requested URL was not found",
    "wordpress.com":      "Do you want to register",
    "feedpress.me":       "The feed has not been found",
}


def get_cname(subdomain):
    try:
        if shutil.which("dig"):
            out = subprocess.check_output(
                f"dig +short CNAME {subdomain} 2>/dev/null",
                shell=True, text=True, timeout=4
            ).strip()
            return out if out else None
    except:
        pass
    return None


def check_http_response(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 VAJRA-Scanner"}
        )
        with urllib.request.urlopen(req, timeout=6) as r:
            return r.read(2000).decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        try:
            return e.read(2000).decode("utf-8", errors="ignore")
        except:
            return ""
    except:
        return ""


def check_one(subdomain):
    """Check a single subdomain — returns (subdomain, cname, service) or None."""
    cname = get_cname(subdomain)
    if not cname:
        return None
    for service, fingerprint in TAKEOVER_FINGERPRINTS.items():
        if service in cname.lower():
            for scheme in ["https", "http"]:
                body = check_http_response(f"{scheme}://{subdomain}")
                if fingerprint.lower() in body.lower():
                    return (subdomain, cname, service)
    return None


def takeover_check(domain):
    subdomains_file = f"output/{domain}/final_subdomains.txt"
    output_file     = f"output/{domain}/takeover_results.txt"

    print("\n[+] Running Subdomain Takeover Check (parallel)...")

    if not os.path.exists(subdomains_file):
        print("[-] No subdomains file found.")
        return

    with open(subdomains_file) as f:
        subdomains = [l.strip() for l in f if l.strip()]

    print(f"[*] Checking {len(subdomains)} subdomains (20 threads)...")

    vulnerable = []
    done = 0

    # 20 parallel workers — much faster than serial
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_one, sub): sub for sub in subdomains}
        for future in as_completed(futures):
            done += 1
            result = future.result()
            if result:
                sub, cname, service = result
                msg = f"[VULNERABLE] {sub} → CNAME: {cname} ({service})"
                console.print(f"[bold red]{msg}[/bold red]")
                vulnerable.append(msg)
            else:
                sub = futures[future]
                console.print(f"[dim][{done}/{len(subdomains)}] {sub} — Safe[/dim]")

    with open(output_file, "w") as f:
        if vulnerable:
            for v in vulnerable:
                f.write(v + "\n")
        else:
            f.write("No subdomain takeover vulnerabilities found.\n")

    if vulnerable:
        console.print(f"\n[bold red][!] VULNERABLE: {len(vulnerable)} subdomain(s)![/bold red]")
    else:
        console.print(f"\n[bold green][✓] No takeover vulnerabilities found.[/bold green]")

    print(f"[+] Saved → {output_file}")
