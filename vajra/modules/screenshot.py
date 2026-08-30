import subprocess
import os
import shutil
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from core.utils import require_tool

console = Console()


def get_live_urls(domain):
    live_file = f"output/{domain}/live_subdomains.txt"
    urls = set()
    if not os.path.exists(live_file):
        return []
    with open(live_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            url = line.split()[0]
            if url.startswith("http"):
                urls.add(url)
    return sorted(urls)


def get_directory_urls(domain):
    dirs_file = f"output/{domain}/directories.txt"
    urls = set()
    if not os.path.exists(dirs_file):
        return []
    with open(dirs_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            url = line.split()[0]
            if url.startswith("http"):
                urls.add(url)
    return sorted(urls)


def verify_url_alive(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 VAJRA-Scanner"}
        )
        with urllib.request.urlopen(req, timeout=6) as r:
            return r.status < 500
    except urllib.error.HTTPError as e:
        return e.code < 500
    except:
        return False


def get_gowitness_version(bin_path):
    try:
        out = subprocess.check_output(
            f"{bin_path} version 2>/dev/null || {bin_path} --version 2>/dev/null",
            shell=True, text=True, timeout=5
        )
        return 3 if "3." in out else 2
    except:
        return 2


def take_screenshots_gowitness(alive_file, output_dir, gowitness_bin):
    version = get_gowitness_version(gowitness_bin)
    console.print(f"[white]    gowitness v{version} detected[/white]")

    if version >= 3:
        cmd = (
            f"{gowitness_bin} scan file "
            f"--filename {alive_file} "
            f"--screenshot-path {output_dir} "
            f"--timeout 10 > /dev/null 2>&1"
        )
    else:
        cmd = (
            f"{gowitness_bin} file "
            f"-f {alive_file} "
            f"--screenshot-path {output_dir} "
            f"--timeout 10 > /dev/null 2>&1"
        )

    console.print(f"[cyan][+] Running gowitness...[/cyan]")
    try:
        subprocess.run(cmd, shell=True, timeout=600)
    except subprocess.TimeoutExpired:
        console.print("[yellow][!] gowitness timed out — partial screenshots saved.[/yellow]")


def take_screenshots(domain):
    screenshots_dir = f"output/{domain}/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    console.print("\n[+] Collecting URLs for screenshots...")

    live_urls = get_live_urls(domain)
    dir_urls  = get_directory_urls(domain)
    all_urls  = sorted(set(live_urls + dir_urls))

    console.print(f"[white]    Live subdomains : {len(live_urls)}[/white]")
    console.print(f"[white]    Directories     : {len(dir_urls)}[/white]")
    console.print(f"[white]    Total unique    : {len(all_urls)}[/white]")

    if not all_urls:
        console.print("[-] No URLs to screenshot.")
        return

    # ── Parallel alive check (30 threads) ───────────────────
    console.print(f"\n[cyan][+] Verifying alive URLs (30 threads)...[/cyan]")
    alive_urls = []
    done = 0

    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(verify_url_alive, url): url for url in all_urls}
        for future in as_completed(futures):
            done += 1
            url   = futures[future]
            alive = future.result()
            status = "[bold green]ALIVE[/bold green]" if alive else "[dim]DEAD[/dim]"
            console.print(f"[dim]  [{done}/{len(all_urls)}] {url[:65]}[/dim] → {status}")
            if alive:
                alive_urls.append(url)

    console.print(f"\n[bold green][✓] Alive: {len(alive_urls)} / {len(all_urls)} URLs[/bold green]")

    if not alive_urls:
        console.print("[-] No alive URLs found.")
        return

    alive_file = f"output/{domain}/alive_urls.txt"
    with open(alive_file, "w") as f:
        for url in sorted(alive_urls):
            f.write(url + "\n")
    console.print(f"[+] Alive URLs → {alive_file}")

    gowitness_bin = require_tool("gowitness")
    if not gowitness_bin:
        console.print("\n[yellow][!] gowitness not found — install:[/yellow]")
        console.print("[white]    go install github.com/sensepost/gowitness@latest[/white]")
        console.print(f"[white]    gowitness file -f {alive_file} --screenshot-path {screenshots_dir}[/white]")
        return

    take_screenshots_gowitness(alive_file, screenshots_dir, gowitness_bin)

    # Count screenshots (check recursively for v3)
    count = 0
    for root, dirs, files in os.walk(screenshots_dir):
        count += len([f for f in files if f.endswith(".png")])

    console.print(f"\n[bold green][✓] Screenshots Captured: {count}[/bold green]")
    console.print(f"[white]    Saved → {screenshots_dir}/[/white]")
