import subprocess
import os

from core.utils import require_tool


def clean_hosts(input_file, clean_file):

    hosts = set()

    with open(input_file, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            line = line.replace("https://", "")
            line = line.replace("http://", "")

            line = line.split("/")[0]

            hosts.add(line)

    with open(clean_file, "w") as file:

        for host in sorted(hosts):
            file.write(host + "\n")


def scan_ports(domain):

    input_file = f"output/{domain}/live_subdomains.txt"

    clean_hosts_file = f"output/{domain}/clean_hosts.txt"

    masscan_output = f"output/{domain}/masscan.txt"

    naabu_output = f"output/{domain}/naabu.txt"

    final_output = f"output/{domain}/open_ports.txt"

    print("\n[+] Preparing Hosts For Port Scanning...")

    clean_hosts(input_file, clean_hosts_file)

    # =========================================================
    # MASSCAN (needs raw sockets -> requires root)
    # =========================================================

    masscan_bin = require_tool("masscan")

    if masscan_bin:

        print("[+] Running Masscan...")

        sudo_prefix = "" if os.geteuid() == 0 else "sudo "

        masscan_command = (
            f"{sudo_prefix}{masscan_bin} "
            f"-p1-1000 "
            f"--rate 1000 "
            f"-iL {clean_hosts_file} "
            f"-oL {masscan_output} "
            f"> /dev/null 2>&1"
        )

        subprocess.run(masscan_command, shell=True)

    # =========================================================
    # NAABU
    # =========================================================

    naabu_bin = require_tool("naabu")

    if naabu_bin:

        print("[+] Running Naabu...")

        naabu_command = (
            f"cat {clean_hosts_file} | "
            f"{naabu_bin} "
            f"-top-ports 1000 "
            f"-silent "
            f"-o {naabu_output} "
            f"> /dev/null 2>&1"
        )

        subprocess.run(naabu_command, shell=True)

    # =========================================================
    # MERGE RESULTS
    # =========================================================

    print("[+] Merging Port Results...")

    combined_ports = set()

    if os.path.exists(naabu_output):

        with open(naabu_output, "r") as file:

            for line in file:
                line = line.strip()
                if line:
                    combined_ports.add(line)

    if os.path.exists(masscan_output):

        with open(masscan_output, "r") as file:

            for line in file:

                if "open" in line:

                    parts = line.split()

                    try:
                        port = parts[2]
                        host = parts[3]

                        combined_ports.add(
                            f"{host}:{port}"
                        )

                    except IndexError:
                        pass

    with open(final_output, "w") as file:

        for item in sorted(combined_ports):
            file.write(item + "\n")

    print(
        f"[+] Open ports saved to {final_output}"
    )

    print("\n[+] Port Scanning Completed!")
