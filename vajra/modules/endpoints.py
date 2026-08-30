import subprocess
import os
import threading

from core.utils import require_tool

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

    print("\n[+] Starting Endpoint Collection (parallel)...")

    katana_bin  = require_tool("katana")
    gau_bin     = require_tool("gau")
    wayback_bin = require_tool("waybackurls")

    # ── Run all 3 in PARALLEL ────────────────────────────────
    def run_katana():
        if not katana_bin: return
        print("[+] Running Katana...")
        try:
            subprocess.run(
                f"cat {input_file} | {katana_bin} -silent -jc -kf all -d 3 -o {katana_output} > /dev/null 2>&1",
                shell=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            print("[!] Katana timed out.")

    def run_gau():
        if not gau_bin: return
        print("[+] Running GAU...")
        try:
            subprocess.run(
                f"echo {domain} | {gau_bin} --threads 20 > {gau_output} 2>/dev/null",
                shell=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            print("[!] GAU timed out — using partial results.")

    def run_wayback():
        if not wayback_bin: return
        print("[+] Running Waybackurls...")
        try:
            subprocess.run(
                f"echo {domain} | {wayback_bin} > {wayback_output} 2>/dev/null",
                shell=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            print("[!] Waybackurls timed out — using partial results.")

    threads = [
        threading.Thread(target=run_katana),
        threading.Thread(target=run_gau),
        threading.Thread(target=run_wayback),
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    # ── Merge + Filter ───────────────────────────────────────
    print("[+] Merging and filtering endpoints...")
    all_urls  = set()
    raw_count = 0

    for fp in [katana_output, gau_output, wayback_output]:
        if os.path.exists(fp):
            with open(fp) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        raw_count += 1
                        if is_useful_url(line):
                            all_urls.add(line)

    with open(final_output, "w") as f:
        for url in sorted(all_urls):
            f.write(url + "\n")

    print(f"[+] Raw URLs      : {raw_count}")
    print(f"[+] After filter  : {len(all_urls)} (static files removed)")
    print(f"[+] Saved → {final_output}")
    print("\n[+] Endpoint Collection Completed!")
