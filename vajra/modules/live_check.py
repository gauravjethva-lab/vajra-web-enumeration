import subprocess
import os

from core.utils import require_tool


def check_live_subdomains(domain):
    input_file  = f"output/{domain}/final_subdomains.txt"
    output_file = f"output/{domain}/live_subdomains.txt"

    print("\n[+] Checking live subdomains...")

    httpx_bin = require_tool("httpx")

    if not httpx_bin:
        with open(input_file, "r") as src, open(output_file, "w") as dst:
            dst.write(src.read())
        print("[!] httpx missing — using final_subdomains as-is.")
        return

    command = (
        f"cat {input_file} | "
        f"{httpx_bin} "
        f"-silent "
        f"-threads 200 "      # 50 → 200 (4x faster)
        f"-timeout 5 "        # 10s → 5s per host
        f"-retries 1 "        # 1 retry only
        f"-o {output_file} "
        f"> /dev/null 2>&1"
    )

    try:
        subprocess.run(command, shell=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("[!] httpx timed out — using partial results.")

    count = 0
    if os.path.exists(output_file):
        with open(output_file) as f:
            count = sum(1 for l in f if l.strip())

    print(f"[+] Live hosts found: {count}")
    print(f"[+] Saved → {output_file}")
