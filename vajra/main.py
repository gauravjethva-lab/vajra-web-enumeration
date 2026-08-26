from core.setup_check import ensure_all_tools
from core.banner import start_banner

from modules.subdomains import enumerate_subdomains
from modules.live_check import check_live_subdomains
from modules.endpoints import collect_endpoints
from modules.ports import scan_ports
from modules.tech_detect import detect_technologies


def main():

    # Pehle saare required tools check/install karo
    ensure_all_tools()

    domain = start_banner()

    enumerate_subdomains(domain)

    check_live_subdomains(domain)

    collect_endpoints(domain)

    scan_ports(domain)

    detect_technologies(domain)

    print("\n[+] VAJRA Recon Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()
