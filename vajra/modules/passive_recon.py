import subprocess, os, socket
from rich.console import Console

console = Console()

def passive_recon(domain):
    output_file = f"output/{domain}/passive_recon.txt"
    console.print("[cyan][+] Running passive recon (WHOIS, ASN, IP)...[/cyan]")

    results = []

    # WHOIS
    try:
        out = subprocess.check_output(f"whois {domain} 2>/dev/null", shell=True, text=True, timeout=10)
        important = []
        for line in out.splitlines():
            for key in ["Registrar:", "Registrant", "Admin Email", "Tech Email",
                        "Creation Date", "Expiry Date", "Name Server"]:
                if key.lower() in line.lower() and line.strip():
                    important.append(line.strip())
        results += ["=== WHOIS ==="] + important[:15]
    except Exception:
        pass

    # IP resolution
    try:
        ip = socket.gethostbyname(domain)
        results.append(f"\n=== IP ===\n{domain} → {ip}")

        # ASN lookup via whois
        asn_out = subprocess.check_output(f"whois -h whois.cymru.com ' -v {ip}' 2>/dev/null", shell=True, text=True, timeout=10)
        results.append(f"\n=== ASN ===\n{asn_out.strip()}")
    except Exception:
        pass

    # Reverse DNS
    try:
        rdns = socket.gethostbyaddr(ip)[0]
        results.append(f"\n=== Reverse DNS ===\n{ip} → {rdns}")
    except Exception:
        pass

    with open(output_file, "w") as f:
        f.write("\n".join(results))

    console.print(f"[bold green][✓] Passive Recon Complete[/bold green]")
    console.print(f"[white]    Saved → {output_file}[/white]")
