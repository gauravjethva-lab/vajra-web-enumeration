import subprocess
import os

from core.utils import require_tool


def collect_endpoints(domain):

    input_file = f"output/{domain}/live_subdomains.txt"

    katana_output = f"output/{domain}/katana.txt"

    gau_output = f"output/{domain}/gau.txt"

    wayback_output = f"output/{domain}/wayback.txt"

    final_output = f"output/{domain}/all_endpoints.txt"

    print("\n[+] Starting Endpoint Collection...")

    # =========================================================
    # KATANA
    # =========================================================

    katana_bin = require_tool("katana")

    if katana_bin:

        print("[+] Running Katana...")

        katana_command = (
            f"cat {input_file} | "
            f"{katana_bin} "
            f"-silent "
            f"-jc "
            f"-kf all "
            f"-d 3 "
            f"-o {katana_output} "
            f"> /dev/null 2>&1"
        )

        subprocess.run(katana_command, shell=True)

    # =========================================================
    # GAU
    # =========================================================

    gau_bin = require_tool("gau")

    if gau_bin:

        print("[+] Running gau...")

        gau_command = (
            f"cat {input_file} | "
            f"{gau_bin} "
            f"--threads 10 "
            f"> {gau_output} 2>/dev/null"
        )

        subprocess.run(gau_command, shell=True)

    # =========================================================
    # WAYBACKURLS
    # =========================================================

    wayback_bin = require_tool("waybackurls")

    if wayback_bin:

        print("[+] Running waybackurls...")

        wayback_command = (
            f"cat {input_file} | "
            f"{wayback_bin} "
            f"> {wayback_output} 2>/dev/null"
        )

        subprocess.run(wayback_command, shell=True)

    # =========================================================
    # MERGE RESULTS
    # =========================================================

    print("[+] Merging Endpoints...")

    all_urls = set()

    files = [
        katana_output,
        gau_output,
        wayback_output
    ]

    for file_path in files:

        if os.path.exists(file_path):

            with open(file_path, "r") as file:

                for line in file:

                    line = line.strip()

                    if line:
                        all_urls.add(line)

    with open(final_output, "w") as file:

        for url in sorted(all_urls):
            file.write(url + "\n")

    print(
        f"[+] Endpoints saved to {final_output}"
    )

    print(
        f"[+] Total Unique Endpoints: {len(all_urls)}"
    )

    print("\n[+] Endpoint Collection Completed!")
