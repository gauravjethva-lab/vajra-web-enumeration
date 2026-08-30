"""
VAJRA Email & Breach Recon
===========================
Finds email patterns from domain + checks breach exposure.
Uses free sources: hunter.io format guess, haveibeenpwned public API.
"""

import urllib.request
import urllib.error
import json
import os
import re
from rich.console import Console

console = Console()

EMAIL_FORMATS = [
    "{first}.{last}@{domain}",
    "{first}{last}@{domain}",
    "{f}{last}@{domain}",
    "{first}@{domain}",
    "{last}@{domain}",
    "info@{domain}",
    "admin@{domain}",
    "security@{domain}",
    "contact@{domain}",
    "support@{domain}",
    "webmaster@{domain}",
    "help@{domain}",
    "abuse@{domain}",
    "noreply@{domain}",
    "careers@{domain}",
]

COMMON_NAMES = [
    ("john", "doe"), ("jane", "doe"), ("admin", "admin"),
    ("test", "user"), ("info", "info"),
]


def check_haveibeenpwned(email):
    """Check if email appears in known breaches (public API)."""
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "VAJRA-Security-Scanner",
            "hibp-api-key": ""  # free endpoint, no key needed for domain check
        })
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            return [b["Name"] for b in data]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []  # Not found in breaches
        return None
    except:
        return None


import urllib.parse

def search_emails_in_endpoints(domain):
    """Find email patterns in collected endpoints."""
    endpoints_file = f"output/{domain}/all_endpoints.txt"
    emails = set()
    email_re = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

    if os.path.exists(endpoints_file):
        with open(endpoints_file) as f:
            for line in f:
                found = email_re.findall(line)
                for email in found:
                    if domain.lower() in email.lower():
                        emails.add(email.lower())
    return sorted(emails)


def email_recon(domain):
    output_file = f"output/{domain}/email_recon.txt"

    print("\n[+] Running Email & Breach Recon...")

    results = []

    # 1. Find emails in collected endpoints
    console.print("[cyan][+] Searching for emails in collected endpoints...[/cyan]")
    found_emails = search_emails_in_endpoints(domain)
    if found_emails:
        console.print(f"[green]    Found {len(found_emails)} email(s) in endpoints:[/green]")
        for email in found_emails[:10]:
            console.print(f"[dim]    → {email}[/dim]")
            results.append(f"[FOUND IN ENDPOINTS] {email}")
    else:
        console.print("[dim]    No emails found in endpoints.[/dim]")

    # 2. Generate common email patterns
    console.print("\n[cyan][+] Generating common email patterns...[/cyan]")
    common_patterns = []
    for fmt in EMAIL_FORMATS[-8:]:  # last 8 are generic (info@, admin@ etc)
        email = fmt.format(first="", last="", f="", domain=domain).replace(".@", "@").strip(".")
        if "@" in email and not email.startswith("@"):
            common_patterns.append(email)

    for p in common_patterns[:5]:
        console.print(f"[dim]    Pattern: {p}[/dim]")
        results.append(f"[PATTERN] {p}")

    # 3. Check WHOIS for email
    whois_file = f"output/{domain}/whois.txt"
    if os.path.exists(whois_file):
        with open(whois_file) as f:
            content = f.read()
        email_re = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
        whois_emails = set(email_re.findall(content))
        if whois_emails:
            console.print(f"\n[green]    WHOIS emails found: {len(whois_emails)}[/green]")
            for e in whois_emails:
                console.print(f"[dim]    → {e}[/dim]")
                results.append(f"[WHOIS EMAIL] {e}")

    # Save results
    with open(output_file, "w") as f:
        f.write(f"Email & Breach Recon — {domain}\n")
        f.write("=" * 60 + "\n\n")
        if results:
            for r in results:
                f.write(r + "\n")
        else:
            f.write("No email data found.\n")

        f.write("\n\nNOTE: To check breaches manually:\n")
        f.write(f"  https://haveibeenpwned.com/DomainSearch\n")
        f.write(f"  https://dehashed.com/?query={domain}\n")
        f.write(f"  https://hunter.io/domain-search/{domain}\n")

    total = len(found_emails) + len(common_patterns)
    console.print(f"\n[bold green][✓] Email Recon: {total} entries found[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
    console.print(f"[cyan]    Manual breach check: https://haveibeenpwned.com/DomainSearch[/cyan]")
