"""
VAJRA SSL/TLS Analysis
======================
Cert info, expiry, weak ciphers — pure Python ssl module.
No extra tools needed.
"""

import ssl
import socket
import os
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console

console = Console()

WEAK_CIPHERS = ["RC4", "DES", "3DES", "MD5", "NULL", "EXPORT", "anon"]


def get_cert_info(host, port=443):
    """Get SSL certificate details for a host."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE

        with socket.create_connection((host, port), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert    = ssock.getpeercert()
                cipher  = ssock.cipher()
                version = ssock.version()

        # Parse cert
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer  = dict(x[0] for x in cert.get("issuer", []))

        # Expiry
        not_after  = cert.get("notAfter", "")
        not_before = cert.get("notBefore", "")
        days_left  = None
        expired    = False

        if not_after:
            exp_dt    = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            days_left = (exp_dt - datetime.datetime.utcnow()).days
            expired   = days_left < 0

        # SANs
        sans = []
        for san_type, san_val in cert.get("subjectAltName", []):
            if san_type == "DNS":
                sans.append(san_val)

        # Weak cipher check
        weak = any(w in (cipher[0] or "") for w in WEAK_CIPHERS) if cipher else False

        return {
            "host":       host,
            "port":       port,
            "tls_version":version,
            "cipher":     cipher[0] if cipher else "Unknown",
            "cn":         subject.get("commonName", ""),
            "issuer":     issuer.get("organizationName", ""),
            "not_before": not_before,
            "not_after":  not_after,
            "days_left":  days_left,
            "expired":    expired,
            "expiring":   0 < days_left < 30 if days_left is not None else False,
            "sans":       sans[:10],
            "weak_cipher":weak,
            "error":      None,
        }

    except ssl.SSLError as e:
        return {"host": host, "port": port, "error": f"SSL Error: {e}"}
    except Exception as e:
        return {"host": host, "port": port, "error": str(e)}


def extract_hosts(live_file):
    """Extract clean hostnames from live_subdomains.txt."""
    hosts = set()
    if not os.path.exists(live_file):
        return []
    with open(live_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            url = line.split()[0]
            if url.startswith("https://"):
                host = url.replace("https://", "").split("/")[0].split(":")[0]
                if host:
                    hosts.add(host)
    return sorted(hosts)


def ssl_analysis(domain):
    live_file   = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/ssl_analysis.txt"

    print("\n[+] Running SSL/TLS Analysis...")

    hosts = extract_hosts(live_file)
    if not hosts:
        print("[-] No HTTPS hosts found for SSL analysis.")
        return

    print(f"[*] Checking {len(hosts)} HTTPS hosts (parallel)...")

    results  = []
    issues   = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(get_cert_info, host): host for host in hosts}
        for future in as_completed(futures):
            r = future.result()
            results.append(r)

            if r.get("error"):
                console.print(f"[dim]    [-] {r['host']}: {r['error']}[/dim]")
                continue

            # Display
            days  = r["days_left"]
            color = "green"
            if r["expired"]:
                color = "red"
                issues.append(f"[EXPIRED] {r['host']} — cert expired {abs(days)} days ago")
            elif r["expiring"]:
                color = "yellow"
                issues.append(f"[EXPIRING] {r['host']} — expires in {days} days")
            if r["weak_cipher"]:
                color = "red"
                issues.append(f"[WEAK CIPHER] {r['host']} — {r['cipher']}")

            status = "EXPIRED" if r["expired"] else f"{days}d left" if days else "?"
            console.print(
                f"    [{color}]{r['host']}[/{color}] | "
                f"{r['tls_version']} | "
                f"{r['cipher'][:30]} | "
                f"Issuer: {r['issuer'][:25]} | "
                f"Expires: {status}"
            )

    # Save results
    with open(output_file, "w") as f:
        f.write(f"SSL/TLS Analysis — {domain}\n")
        f.write("=" * 60 + "\n\n")

        if issues:
            f.write("ISSUES FOUND:\n")
            for issue in issues:
                f.write(f"  {issue}\n")
            f.write("\n")

        f.write("FULL RESULTS:\n")
        for r in sorted(results, key=lambda x: x["host"]):
            if r.get("error"):
                f.write(f"  {r['host']}: ERROR — {r['error']}\n")
            else:
                f.write(
                    f"  {r['host']} | {r['tls_version']} | "
                    f"{r['cipher']} | "
                    f"Issuer: {r['issuer']} | "
                    f"CN: {r['cn']} | "
                    f"Days left: {r['days_left']} | "
                    f"SANs: {', '.join(r['sans'][:3])}\n"
                )

    ok = len([r for r in results if not r.get("error")])
    console.print(f"\n[bold green][✓] SSL Analysis: {ok}/{len(hosts)} hosts checked[/bold green]")
    if issues:
        console.print(f"[bold red][!] Issues found: {len(issues)}[/bold red]")
        for issue in issues:
            console.print(f"[red]    {issue}[/red]")
    print(f"[+] Saved → {output_file}")
