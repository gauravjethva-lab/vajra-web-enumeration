import subprocess
import os
import threading
from urllib.parse import urlparse

from core.utils import require_tool

SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".css", ".woff", ".woff2", ".ttf", ".eot",
    ".mp4", ".mp3", ".avi", ".pdf", ".zip", ".map"
}

API_PATTERNS = ["/api/", "/v1/", "/v2/", "/v3/", "/graphql", "/rest/", "/ws/", "/rpc/"]


def is_useful_url(url):
    try:
        ext = os.path.splitext(url.split("?")[0].lower())[1]
        return ext not in SKIP_EXT
    except:
        return True


def classify_urls(all_urls, domain):
    """Classify URLs into: in-scope, api, third-party."""
    in_scope    = []
    api_urls    = []
    third_party = []

    for url in all_urls:
        try:
            host = urlparse(url).netloc.lower()
        except:
            continue

        if domain.lower() in host:
            in_scope.append(url)
            if any(p in url.lower() for p in API_PATTERNS):
                api_urls.append(url)
        else:
            third_party.append(url)

    return in_scope, api_urls, third_party


def collect_endpoints(domain):
    input_file     = f"output/{domain}/live_subdomains.txt"
    katana_output  = f"output/{domain}/katana.txt"
    gau_output     = f"output/{domain}/gau.txt"
    wayback_output = f"output/{domain}/wayback.txt"
    final_output   = f"output/{domain}/all_endpoints.txt"
    inscope_output = f"output/{domain}/inscope_endpoints.txt"
    api_output     = f"output/{domain}/api_endpoints.txt"
    third_output   = f"output/{domain}/third_party_urls.txt"

    print("\n[+] Starting Endpoint Collection (parallel)...")

    katana_bin  = require_tool("katana")
    gau_bin     = require_tool("gau")
    wayback_bin = require_tool("waybackurls")

    # ── All 3 tools in parallel ──────────────────────────────
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
    print("[+] Merging, filtering and classifying endpoints...")
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

    # Save all
    with open(final_output, "w") as f:
        for url in sorted(all_urls):
            f.write(url + "\n")

    # Classify
    in_scope, api_urls, third_party = classify_urls(all_urls, domain)

    with open(inscope_output, "w") as f:
        for url in sorted(in_scope):
            f.write(url + "\n")

    with open(api_output, "w") as f:
        for url in sorted(api_urls):
            f.write(url + "\n")

    with open(third_output, "w") as f:
        for url in sorted(third_party):
            f.write(url + "\n")

    print(f"[+] Raw URLs collected  : {raw_count}")
    print(f"[+] After filtering     : {len(all_urls)}")
    print(f"[+] In-scope URLs       : {len(in_scope)}")
    print(f"[+] API endpoints       : {len(api_urls)}")
    print(f"[+] Third-party URLs    : {len(third_party)}")
    print(f"[+] Saved → {final_output}")
    print("\n[+] Endpoint Collection Completed!")
