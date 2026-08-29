import subprocess
import os
import shutil
import urllib.request
import urllib.error
from rich.console import Console
from core.utils import require_tool

console = Console()


def get_live_urls(domain):
    """Read live subdomains file and extract clean URLs."""
    live_file = f"output/{domain}/live_subdomains.txt"
    urls = set()

    if not os.path.exists(live_file):
        return list(urls)

    with open(live_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # httpx output format: "https://example.com [200] [Title]"
            url = line.split()[0]
            if url.startswith("http"):
                urls.add(url)
            elif line.startswith("http"):
                urls.add(line)

    return sorted(urls)


def get_directory_urls(domain):
    """Read discovered directories and return live ones."""
    dirs_file = f"output/{domain}/directories.txt"
    urls = set()

    if not os.path.exists(dirs_file):
        return list(urls)

    with open(dirs_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Extract URL part
            url = line.split()[0]
            if url.startswith("http"):
                urls.add(url)

    return sorted(urls)


def verify_url_alive(url):
    """Quick check if URL actually responds."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 VAJRA-Scanner"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status < 500
    except urllib.error.HTTPError as e:
        # 403, 401 etc = still alive
        return e.code < 500
    except:
        return False


def safe_filename(url):
    """Convert URL to safe filename."""
    return url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")[:100]


def take_screenshots_gowitness(urls, output_dir, gowitness_bin):
    """Take screenshots using gowitness."""
    # Write URLs to temp file
    url_file = os.path.join(output_dir, "_urls_to_screenshot.txt")
    with open(url_file, "w") as f:
        for url in urls:
            f.write(url + "\n")

    console.print(f"[cyan][+] Running gowitness on {len(urls)} URLs...[/cyan]")
    subprocess.run(
        f"{gowitness_bin} file -f {url_file} --screenshot-path {output_dir} --timeout 10 > /dev/null 2>&1",
        shell=True, timeout=600
    )
    os.remove(url_file)


def take_screenshots(domain):
    screenshots_dir = f"output/{domain}/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    print("\n[+] Collecting URLs for screenshots...")

    # Gather live subdomains
    live_urls = get_live_urls(domain)
    console.print(f"[white]    Live subdomains : {len(live_urls)} URLs[/white]")

    # Gather discovered directories
    dir_urls = get_directory_urls(domain)
    console.print(f"[white]    Directories     : {len(dir_urls)} URLs[/white]")

    # Combine all unique URLs
    all_urls = sorted(set(live_urls + dir_urls))
    console.print(f"[white]    Total unique    : {len(all_urls)} URLs[/white]")

    if not all_urls:
        print("[-] No URLs to screenshot.")
        return

    # Verify only genuinely alive URLs
    console.print(f"\n[cyan][+] Verifying which URLs are genuinely alive...[/cyan]")
    alive_urls = []
    for i, url in enumerate(all_urls, 1):
        alive = verify_url_alive(url)
        status = "[bold green]ALIVE[/bold green]" if alive else "[dim]DEAD[/dim]"
        console.print(f"[dim]    [{i}/{len(all_urls)}] {url[:60]} → [/dim]{status}")
        if alive:
            alive_urls.append(url)

    console.print(f"\n[bold green][✓] Genuinely alive: {len(alive_urls)} / {len(all_urls)} URLs[/bold green]")

    if not alive_urls:
        print("[-] No alive URLs found for screenshots.")
        return

    # Save alive URLs list
    alive_file = f"output/{domain}/alive_urls.txt"
    with open(alive_file, "w") as f:
        for url in alive_urls:
            f.write(url + "\n")
    print(f"[+] Alive URLs saved → {alive_file}")

    # Take screenshots
    gowitness_bin = require_tool("gowitness")

    if gowitness_bin:
        take_screenshots_gowitness(alive_urls, screenshots_dir, gowitness_bin)
    else:
        console.print("[yellow][!] gowitness not found.[/yellow]")
        console.print("[cyan][*] Install: go install github.com/sensepost/gowitness@latest[/cyan]")
        console.print(f"[cyan][*] Then run manually:[/cyan]")
        console.print(f"[white]    gowitness file -f {alive_file} --screenshot-path {screenshots_dir}[/white]")

    # Count screenshots taken
    count = len([f for f in os.listdir(screenshots_dir) if f.endswith(".png")])
    console.print(f"\n[bold green][✓] Screenshots Captured: {count}[/bold green]")
    console.print(f"[white]    Saved → {screenshots_dir}/[/white]")
