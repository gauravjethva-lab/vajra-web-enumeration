import subprocess
import os
import shutil
import urllib.request
import urllib.error
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
            if not line:
                continue
            # httpx format: "https://example.com [200] [Title]"
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
            if not line:
                continue
            url = line.split()[0]
            if url.startswith("http"):
                urls.add(url)
    return sorted(urls)


def verify_url_alive(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 VAJRA-Scanner"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status < 500
    except urllib.error.HTTPError as e:
        return e.code < 500
    except:
        return False


def get_gowitness_version(bin_path):
    """Detect gowitness version to use correct command syntax."""
    try:
        out = subprocess.check_output(
            f"{bin_path} version 2>/dev/null || {bin_path} --version 2>/dev/null",
            shell=True, text=True, timeout=5
        )
        # v3+ uses "gowitness scan file"
        # v2 uses "gowitness file"
        if "3." in out:
            return 3
        return 2
    except:
        return 2  # default assume v2


def take_screenshots_gowitness(alive_file, output_dir, gowitness_bin):
    """Take screenshots — supports both gowitness v2 and v3."""
    version = get_gowitness_version(gowitness_bin)
    console.print(f"[white]    Detected gowitness v{version}[/white]")

    if version >= 3:
        # gowitness v3 syntax
        cmd = (
            f"{gowitness_bin} scan file "
            f"--filename {alive_file} "
            f"--screenshot-path {output_dir} "
            f"--timeout 10 "
            f"> /dev/null 2>&1"
        )
    else:
        # gowitness v2 syntax
        cmd = (
            f"{gowitness_bin} file "
            f"-f {alive_file} "
            f"--screenshot-path {output_dir} "
            f"--timeout 10 "
            f"> /dev/null 2>&1"
        )

    console.print(f"[cyan][+] Running gowitness (v{version})...[/cyan]")
    try:
        subprocess.run(cmd, shell=True, timeout=600)
    except subprocess.TimeoutExpired:
        console.print("[yellow][!] gowitness timed out — partial screenshots saved.[/yellow]")


def take_screenshots(domain):
    screenshots_dir = f"output/{domain}/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    console.print("\n[+] Collecting URLs for screenshots...")

    live_urls = get_live_urls(domain)
    console.print(f"[white]    Live subdomains : {len(live_urls)} URLs[/white]")

    dir_urls = get_directory_urls(domain)
    console.print(f"[white]    Directories     : {len(dir_urls)} URLs[/white]")

    all_urls = sorted(set(live_urls + dir_urls))
    console.print(f"[white]    Total unique    : {len(all_urls)} URLs[/white]")

    if not all_urls:
        console.print("[-] No URLs to screenshot.")
        return

    # Verify genuinely alive URLs
    console.print(f"\n[cyan][+] Verifying genuinely alive URLs...[/cyan]")
    alive_urls = []
    for i, url in enumerate(all_urls, 1):
        alive = verify_url_alive(url)
        status = "[bold green]ALIVE[/bold green]" if alive else "[dim]DEAD[/dim]"
        console.print(f"[dim]    [{i}/{len(all_urls)}] {url[:65]}[/dim] → {status}")
        if alive:
            alive_urls.append(url)

    console.print(f"\n[bold green][✓] Genuinely alive: {len(alive_urls)} / {len(all_urls)} URLs[/bold green]")

    if not alive_urls:
        console.print("[-] No alive URLs found for screenshots.")
        return

    # Save alive URLs
    alive_file = f"output/{domain}/alive_urls.txt"
    with open(alive_file, "w") as f:
        for url in alive_urls:
            f.write(url + "\n")
    console.print(f"[+] Alive URLs saved → {alive_file}")

    # Check gowitness
    gowitness_bin = require_tool("gowitness")

    if not gowitness_bin:
        console.print("\n[yellow][!] gowitness not found — install it:[/yellow]")
        console.print("[white]    go install github.com/sensepost/gowitness@latest[/white]")
        console.print(f"[white]    Then run: gowitness file -f {alive_file} --screenshot-path {screenshots_dir}[/white]")
        return

    take_screenshots_gowitness(alive_file, screenshots_dir, gowitness_bin)

    # Count results
    png_files = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
    count = len(png_files)

    if count == 0:
        # gowitness v3 saves in subdirectory — check recursively
        for root, dirs, files in os.walk(screenshots_dir):
            png_files += [f for f in files if f.endswith(".png")]
        count = len(png_files)

    console.print(f"\n[bold green][✓] Screenshots Captured: {count}[/bold green]")
    console.print(f"[white]    Saved → {screenshots_dir}/[/white]")
