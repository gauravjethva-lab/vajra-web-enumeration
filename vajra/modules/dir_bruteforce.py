import subprocess, os
from rich.console import Console
from core.utils import require_tool

console = Console()

def bruteforce_dirs(domain):
    input_file  = f"output/{domain}/live_subdomains.txt"
    output_dir  = f"output/{domain}/dirscan"
    final_output= f"output/{domain}/directories.txt"
    os.makedirs(output_dir, exist_ok=True)

    ffuf_bin = require_tool("ffuf")
    if not ffuf_bin:
        console.print("[yellow][!] ffuf missing — skipping directory bruteforce.[/yellow]")
        return

    # Common wordlist locations on Kali
    wordlists = [
        "/usr/share/seclists/Discovery/Web-Content/common.txt",
        "/usr/share/wordlists/dirb/common.txt",
        "/usr/share/dirb/wordlists/common.txt",
    ]
    wordlist = next((w for w in wordlists if os.path.exists(w)), None)
    if not wordlist:
        console.print("[yellow][!] No wordlist found — install seclists: sudo apt install seclists[/yellow]")
        return

    console.print(f"[cyan][+] Running directory bruteforce (ffuf) on top hosts...[/cyan]")
    console.print(f"[white]    Wordlist: {wordlist}[/white]")

    all_results = []
    if os.path.exists(input_file):
        with open(input_file) as f:
            hosts = [l.strip().split()[0] for l in f if l.strip()][:5]  # top 5 hosts

    for host in hosts:
        out_file = f"{output_dir}/{host.replace('://', '_').replace('/', '_')}.txt"
        try:
            subprocess.run(
                f"{ffuf_bin} -u {host}/FUZZ -w {wordlist} -mc 200,301,302,403 -o {out_file} -of csv -t 50 -timeout 5 -s > /dev/null 2>&1",
                shell=True, timeout=120
            )
            if os.path.exists(out_file):
                with open(out_file) as f:
                    for line in f:
                        if not line.startswith("url") and line.strip():
                            all_results.append(line.strip())
        except Exception:
            pass

    with open(final_output, "w") as f:
        for r in all_results:
            f.write(r + "\n")

    console.print(f"[bold green][✓] Directories Found: {len(all_results)}[/bold green]")
    console.print(f"[white]    Saved → {final_output}[/white]")
