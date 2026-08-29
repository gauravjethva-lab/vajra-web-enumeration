import subprocess
import os
import socket
import urllib.request
import urllib.error

from rich.console import Console

console = Console()

# Known fingerprints for subdomain takeover
# If CNAME points to these services and they return this text = takeover possible
TAKEOVER_FINGERPRINTS = {
    "github.io":             "There isn't a GitHub Pages site here",
    "herokuapp.com":         "No such app",
    "s3.amazonaws.com":      "NoSuchBucket",
    "s3-website":            "NoSuchBucket",
    "amazonaws.com":         "NoSuchBucket",
    "azurewebsites.net":     "404 Web Site not found",
    "cloudapp.net":          "404 Web Site not found",
    "fastly.net":            "Fastly error: unknown domain",
    "pantheon.io":           "404 error unknown site",
    "zendesk.com":           "Help Center Closed",
    "freshdesk.com":         "May be for sale",
    "readme.io":             "Project doesnt exist",
    "surge.sh":              "project not found",
    "bitbucket.io":          "Repository not found",
    "ghost.io":              "404",
    "helpjuice.com":         "We could not find what you're looking for",
    "helpscoutdocs.com":     "No settings were found",
    "cargo.site":            "If you're moving your domain away from Cargo",
    "launchrock.com":        "It looks like you may have taken a wrong turn",
    "smugmug.com":           "Page Not Found",
    "strikingly.com":        "page not found",
    "tumblr.com":            "There's nothing here",
    "unbounce.com":          "The requested URL was not found",
    "wordpress.com":         "Do you want to register",
    "feedpress.me":          "The feed has not been found",
}


def get_cname(subdomain):
    """Get CNAME record for a subdomain."""
    try:
        import shutil
        if shutil.which("dig"):
            out = subprocess.check_output(
                f"dig +short CNAME {subdomain} 2>/dev/null",
                shell=True, text=True, timeout=5
            ).strip()
            return out if out else None
    except:
        pass
    return None


def check_http_response(url):
    """Get HTTP response body snippet."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 VAJRA-Scanner"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read(2000).decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        try:
            return e.read(2000).decode("utf-8", errors="ignore")
        except:
            return ""
    except:
        return ""


def is_dangling(subdomain):
    """Check if subdomain resolves but points to unclaimed service."""
    cname = get_cname(subdomain)
    if not cname:
        return None, None

    # Check if CNAME matches any known takeover service
    for service, fingerprint in TAKEOVER_FINGERPRINTS.items():
        if service in cname.lower():
            # Verify by checking HTTP response
            for scheme in ["https", "http"]:
                body = check_http_response(f"{scheme}://{subdomain}")
                if fingerprint.lower() in body.lower():
                    return cname, service

    return None, None


def takeover_check(domain):
    subdomains_file = f"output/{domain}/final_subdomains.txt"
    output_file     = f"output/{domain}/takeover_results.txt"

    print("\n[+] Running Subdomain Takeover Check...")

    if not os.path.exists(subdomains_file):
        print("[-] No subdomains file found — run subdomain enumeration first.")
        return

    with open(subdomains_file) as f:
        subdomains = [l.strip() for l in f if l.strip()]

    print(f"[*] Checking {len(subdomains)} subdomains for takeover...")

    vulnerable = []
    checked    = 0

    for sub in subdomains:
        checked += 1
        cname, service = is_dangling(sub)
        if cname:
            msg = f"[VULNERABLE] {sub} → CNAME: {cname} ({service})"
            console.print(f"[bold red]{msg}[/bold red]")
            vulnerable.append(msg)
        else:
            console.print(f"[dim][{checked}/{len(subdomains)}] {sub} — Safe[/dim]")

    with open(output_file, "w") as f:
        if vulnerable:
            for v in vulnerable:
                f.write(v + "\n")
        else:
            f.write("No subdomain takeover vulnerabilities found.\n")

    if vulnerable:
        console.print(f"\n[bold red][!] VULNERABLE: {len(vulnerable)} subdomain(s) may be takeable![/bold red]")
    else:
        console.print(f"\n[bold green][✓] No takeover vulnerabilities found.[/bold green]")

    print(f"[+] Checked: {checked} subdomains")
    print(f"[+] Saved → {output_file}")
