import subprocess
import os
from core.utils import require_tool


def check_live_subdomains(domain):
    input_file  = f"output/{domain}/final_subdomains.txt"
    output_file = f"output/{domain}/live_subdomains.txt"

    print("\n[+] Checking live subdomains...")

    if not os.path.exists(input_file):
        print(f"[-] Input file not found: {input_file}")
        open(output_file, "w").close()
        return

    httpx_bin = require_tool("httpx")

    if not httpx_bin:
        with open(input_file, "r") as src, open(output_file, "w") as dst:
            dst.write(src.read())
        print("[!] httpx missing — using final_subdomains as-is.")
        return

    command = (
        f"cat {input_file} | {httpx_bin} "
        f"-silent -threads 150 -timeout 8 -retries 1 "
        f"-o {output_file} > /dev/null 2>&1"
    )

    try:
        subprocess.run(command, shell=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("[!] httpx timed out — using partial results.")

    count = 0
    if os.path.exists(output_file):
        with open(output_file) as f:
            count = sum(1 for l in f if l.strip())
    else:
        open(output_file, "w").close()

    print(f"[+] Live hosts found: {count}")
    print(f"[+] Saved → {output_file}")
