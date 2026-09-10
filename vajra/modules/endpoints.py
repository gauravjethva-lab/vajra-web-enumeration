import subprocess
import os
import threading
from core.utils import require_tool

SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".css", ".woff", ".woff2", ".ttf", ".eot",
    ".mp4", ".mp3", ".avi", ".pdf", ".zip", ".map",
    ".xml", ".txt", ".gz", ".tar", ".exe", ".dmg",
}


def is_useful_url(url):
    try:
        ext = os.path.splitext(url.split("?")[0].lower())[1]
        return ext not in SKIP_EXT
    except Exception:
        return True


def collect_endpoints(domain):
    input_file     = f"output/{domain}/live_subdomains.txt"
    katana_output  = f"output/{domain}/katana.txt"
    gau_output     = f"output/{domain}/gau.txt"
    wayback_output = f"output/{domain}/wayback.txt"
    final_output   = f"output/{domain}/all_endpoints.txt"

    print("\n[+] Starting Endpoint Collection (parallel)...")

    if not os.path.exists(input_file):
        print(f"[-] Input file not found: {input_file}")
        open(final_output, "w").close()
        return

    katana_bin  = require_tool("katana")
    gau_bin     = require_tool("gau")
    wayback_bin = require_tool("waybackurls")

    def run_katana():
        if not katana_bin:
            return
        print("[+] Running Katana...")
        try:
            subprocess.run(
                f"cat {input_file} | {katana_bin} -silent -jc -kf all -d 3 -o {katana_output} > /dev/null 2>&1",
                shell=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            print("[!] Katana timed out.")
        except Exception as e:
            print(f"[-] Katana error: {e}")

    def run_gau():
        if not gau_bin:
            return
        print("[+] Running gau...")
        try:
            subprocess.run(
                f"echo {domain} | {gau_bin} --threads 10 > {gau_output} 2>/dev/null",
                shell=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            print("[!] gau timed out — using partial results.")
        except Exception as e:
            print(f"[-] gau error: {e}")

    def run_wayback():
        if not wayback_bin:
            return
        print("[+] Running waybackurls...")
        try:
            subprocess.run(
                f"echo {domain} | {wayback_bin} > {wayback_output} 2>/dev/null",
                shell=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            print("[!] waybackurls timed out — using partial results.")
        except Exception as e:
            print(f"[-] waybackurls error: {e}")

    threads = [
        threading.Thread(target=run_katana),
        threading.Thread(target=run_gau),
        threading.Thread(target=run_wayback),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("[+] Merging and filtering endpoints...")
    all_urls  = set()
    raw_count = 0

    for fp in [katana_output, gau_output, wayback_output]:
        if os.path.exists(fp):
            try:
                with open(fp) as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            raw_count += 1
                            if is_useful_url(line):
                                all_urls.add(line)
            except Exception as e:
                print(f"[-] Error reading {fp}: {e}")

    try:
        with open(final_output, "w") as f:
            for url in sorted(all_urls):
                f.write(url + "\n")
    except Exception as e:
        print(f"[-] Error saving endpoints: {e}")

    print(f"[+] Raw URLs      : {raw_count}")
    print(f"[+] After filter  : {len(all_urls)}")
    print(f"[+] Saved → {final_output}")
    print("\n[+] Endpoint Collection Completed!")
