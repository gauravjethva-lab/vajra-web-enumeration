import subprocess

from core.utils import require_tool


def detect_technologies(domain):

    input_file = f"output/{domain}/live_subdomains.txt"
    output_file = f"output/{domain}/technologies.txt"

    print("\n[+] Detecting Technologies...")

    whatweb_bin = require_tool("whatweb")

    if not whatweb_bin:
        return

    # Fix: --log-brief= needs = not space
    command = (
        f"{whatweb_bin} "
        f"-i {input_file} "
        f"--no-errors "
        f"--log-brief={output_file} "
        f"> /dev/null 2>&1"
    )

    subprocess.run(command, shell=True)

    print(f"[+] Technology results saved to {output_file}")
