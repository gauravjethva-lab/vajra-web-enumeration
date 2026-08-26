import subprocess, os, threading
from urllib.parse import urlparse
from rich.console import Console
from core.utils import require_tool

console = Console()

SKIP_EXT = {".png",".jpg",".jpeg",".gif",".svg",".ico",".css",".woff",".woff2",".ttf",".eot",".mp4",".mp3",".pdf",".zip",".map",".xml"}

def is_useful(url):
    try:
        ext = os.path.splitext(urlparse(url).path.lower())[1]
        return ext not in SKIP_EXT
    except:
        return True

def collect_endpoints(domain):
    input_file     = f"output/{domain}/live_subdomains.txt"
    katana_output  = f"output/{domain}/katana.txt"
    gau_output     = f"output/{domain}/gau.txt"
    wayback_output = f"output/{domain}/wayback.txt"
    final_output   = f"output/{domain}/all_endpoints.txt"

    katana_bin  = require_tool("katana")
    gau_bin     = require_tool("gau")
    wayback_bin = require_tool("waybackurls")

    # ── Run all 3 tools in PARALLEL threads ──────────────────
    def run_katana():
        if not katana_bin: return
        console.print("[cyan][+] Running Katana (active crawl)...[/cyan]")
        subprocess.run(
            f"cat {input_file} | {katana_bin} -silent -jc -kf all -d 3 -o {katana_output} > /dev/null 2>&1",
            shell=True, timeout=300
        )
        count = sum(1 for _ in open(katana_output)) if os.path.exists(katana_output) else 0
        console.print(f"[green][✓] Katana: {count} URLs[/green]")

    def run_gau():
        if not gau_bin: return
        console.print("[cyan][+] Running GAU (passive URLs)...[/cyan]")
        subprocess.run(
            f"echo {domain} | {gau_bin} --threads 10 > {gau_output} 2>/dev/null",
            shell=True, timeout=300
        )
        count = sum(1 for _ in open(gau_output)) if os.path.exists(gau_output) else 0
        console.print(f"[green][✓] GAU: {count} URLs[/green]")

    def run_wayback():
        if not wayback_bin: return
        console.print("[cyan][+] Running Waybackurls...[/cyan]")
        subprocess.run(
            f"echo {domain} | {wayback_bin} > {wayback_output} 2>/dev/null",
            shell=True, timeout=300
        )
        count = sum(1 for _ in open(wayback_output)) if os.path.exists(wayback_output) else 0
        console.print(f"[green][✓] Waybackurls: {count} URLs[/green]")

    threads = [
        threading.Thread(target=run_katana),
        threading.Thread(target=run_gau),
        threading.Thread(target=run_wayback),
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    # ── Merge + Deduplicate + Filter ─────────────────────────
    console.print("[cyan][+] Merging and deduplicating...[/cyan]")
    all_urls = set()
    for fp in [katana_output, gau_output, wayback_output]:
        if os.path.exists(fp):
            with open(fp) as f:
                for line in f:
                    url = line.strip()
                    if url and is_useful(url):
                        all_urls.add(url)

    with open(final_output, "w") as f:
        for url in sorted(all_urls):
            f.write(url + "\n")

    console.print(f"[bold green][✓] Unique Useful Endpoints: {len(all_urls)}[/bold green]")
    console.print(f"[white]    Saved → {final_output}[/white]")
