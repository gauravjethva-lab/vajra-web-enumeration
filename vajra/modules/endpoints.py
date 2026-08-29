import subprocess
import os

from core.utils import require_tool

# Static file extensions to filter out
SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".css", ".woff", ".woff2", ".ttf", ".eot",
    ".mp4", ".mp3", ".avi", ".pdf", ".zip", ".map"
}

def is_useful_url(url):
    try:
        ext = os.path.splitext(url.split("?")[0].lower())[1]
        return ext not in SKIP_EXT
    except:
        return True


def collect_endpoints(domain):

    input_file     = f"output/{domain}/live_subdomains.txt"
    katana_output  = f"output/{domain}/katana.txt"
    gau_output     = f"output/{domain}/gau.txt"
    wayback_output = f"output/{domain}/wayback.txt"
    final_output   = f"output/{domain}/all_endpoints.txt"

    print("\n[+] Starting Endpoint Collection...")

    # ── KATANA ───────────────────────────────────────────────
    katana_bin = require_tool("katana")
    if katana_bin:
        print("[+] Running Katana...")
        subprocess.run(
            f"cat {input_file} | {katana_bin} -silent -jc -kf all -d 3 -o {katana_output} > /dev/null 2>&1",
            shell=True, timeout=300
        )

    # ── GAU ──────────────────────────────────────────────────
    gau_bin = require_tool("gau")
    if gau_bin:
        print("[+] Running gau...")
        try:
            subprocess.run(
                f"echo {domain} | {gau_bin} --threads 10 > {gau_output} 2>/dev/null",
                shell=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            print("[!] gau timed out — using partial results.")

    # ── WAYBACKURLS ──────────────────────────────────────────
    wayback_bin = require_tool("waybackurls")
    if wayback_bin:
        print("[+] Running waybackurls...")
        try:
            subprocess.run(
                f"echo {domain} | {wayback_bin} > {wayback_output} 2>/dev/null",
                shell=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            print("[!] waybackurls timed out — using partial results.")

    # ── MERGE + FILTER ───────────────────────────────────────
    print("[+] Merging and filtering endpoints...")

    all_urls   = set()
    raw_count  = 0

    for file_path in [katana_output, gau_output, wayback_output]:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        raw_count += 1
                        if is_useful_url(line):
                            all_urls.add(line)

    with open(final_output, "w") as f:
        for url in sorted(all_urls):
            f.write(url + "\n")

    print(f"[+] Raw URLs collected : {raw_count}")
    print(f"[+] After filtering    : {len(all_urls)} (static files removed)")
    print(f"[+] Endpoints saved to {final_output}")
    print("\n[+] Endpoint Collection Completed!")
