import subprocess
import os
from core.utils import require_tool


def detect_technologies(domain):
    input_file  = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/technologies.txt"

    print("\n[+] Detecting Technologies...")

    if not os.path.exists(input_file):
        print(f"[-] Input file not found: {input_file}")
        open(output_file, "w").close()
        return

    whatweb_bin = require_tool("whatweb")
    if not whatweb_bin:
        open(output_file, "w").close()
        return

    command = (
        f"{whatweb_bin} "
        f"-i {input_file} "
        f"--no-errors "
        f"--log-brief={output_file} "
        f"> /dev/null 2>&1"
    )

    try:
        subprocess.run(command, shell=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("[!] WhatWeb timed out — using partial results.")
    except Exception as e:
        print(f"[-] WhatWeb error: {e}")

    count = 0
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                count = sum(1 for l in f if l.strip())
        except Exception:
            pass

    print(f"[+] Technologies detected: {count} hosts")
    print(f"[+] Saved → {output_file}")
