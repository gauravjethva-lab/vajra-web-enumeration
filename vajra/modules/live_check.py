import subprocess

from core.utils import require_tool


def check_live_subdomains(domain):

    input_file = f"output/{domain}/final_subdomains.txt"

    output_file = f"output/{domain}/live_subdomains.txt"

    print("\n[+] Checking live subdomains...")

    httpx_bin = require_tool("httpx")

    if not httpx_bin:
        # Fallback: agar httpx nahi hai to final_subdomains ko hi
        # live maan lo taaki pipeline aage chalti rahe.
        with open(input_file, "r") as src, open(output_file, "w") as dst:
            dst.write(src.read())

        print("[yellow][!] httpx missing — using final_subdomains as-is.[/yellow]")
        return

    command = (
        f"cat {input_file} | "
        f"{httpx_bin} "
        f"-silent "
        f"-threads 50 "
        f"-o {output_file} "
        f"> /dev/null 2>&1"
    )

    subprocess.run(command, shell=True)

    print(
        f"[+] Live hosts saved to {output_file}"
    )
