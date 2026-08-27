import subprocess
import os
import threading

from core.utils import require_tool


def run_command(command):

    try:

        result = subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL,
        )

        return result.splitlines()

    except subprocess.CalledProcessError:
        return []


def save_results(filepath, data):

    with open(filepath, "w") as file:

        for item in sorted(set(data)):
            file.write(item + "\n")


def enumerate_subdomains(domain):

    output_dir = f"output/{domain}"

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[+] Target: {domain}")

    subfinder_results = []
    amass_results = []

    subfinder_bin = require_tool("subfinder")
    amass_bin = require_tool("amass")

    # =========================================================
    # SUBFINDER
    # =========================================================

    def run_subfinder():

        nonlocal subfinder_results

        if not subfinder_bin:
            return

        print("[+] Running Subfinder...")

        subfinder_results = run_command(
            f"{subfinder_bin} -d {domain} -silent"
        )

        save_results(
            f"{output_dir}/subfinder.txt",
            subfinder_results
        )

    # =========================================================
    # AMASS
    # =========================================================

    def run_amass():

        nonlocal amass_results

        if not amass_bin:
            return

        print("[+] Running Amass...")

        amass_results = run_command(
            f"{amass_bin} enum -passive -d {domain}"
        )

        save_results(
            f"{output_dir}/amass.txt",
            amass_results
        )

    # =========================================================
    # THREADS
    # =========================================================

    t1 = threading.Thread(target=run_subfinder)
    t2 = threading.Thread(target=run_amass)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    print("[+] Removing duplicates...")

    final_results = sorted(
        set(
            subfinder_results +
            amass_results
        )
    )

    # Agar dono tools missing the, to at least the domain khud
    # include kar do taaki pipeline aage chal sake.
    if not final_results:
        final_results = [domain]

    save_results(
        f"{output_dir}/final_subdomains.txt",
        final_results
    )

    print(
        f"[+] Total Unique Subdomains: {len(final_results)}"
    )

    print(
        f"[+] Results saved in {output_dir}"
    )

    return final_results
