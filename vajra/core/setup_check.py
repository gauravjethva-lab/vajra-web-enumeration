"""
VAJRA - Auto Dependency Manager
=================================
Isse pehli baar tool run hone par saare required binaries check karta hai.
Jo bhi missing hoga, khud install karne ki koshish karega
(apt ke through system tools, aur `go install` ke through Go-based recon tools).

Design goals:
  - Kabhi bhi hard crash na ho agar ek tool install nahi hota
  - User ko clearly bataye ki kya install ho raha hai / kya fail hua
  - Dobara run karne par already-installed tools ko dobara install na kare
"""

import os
import shutil
import subprocess
import sys

from rich.console import Console

console = Console()

GO_BIN = os.path.expanduser("~/go/bin")

# =============================================================
# TOOL DEFINITIONS
# =============================================================
# type: "apt"  -> installed via `apt-get install -y <apt_pkg>`
# type: "go"   -> installed via `go install <go_path>@latest`

APT_TOOLS = {
    "masscan": "masscan",
    "whatweb": "whatweb",
    "nmap": "nmap",
}

GO_TOOLS = {
    "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder",
    "httpx": "github.com/projectdiscovery/httpx/cmd/httpx",
    "naabu": "github.com/projectdiscovery/naabu/v2/cmd/naabu",
    "katana": "github.com/projectdiscovery/katana/cmd/katana",
    "gau": "github.com/lc/gau/v2/cmd/gau",
    "waybackurls": "github.com/tomnomnom/waybackurls",
    "amass": "github.com/owasp-amass/amass/v4/...",
}

PYTHON_PACKAGES = ["rich", "pyfiglet"]


def _binary_exists(name):
    """Check PATH aur ~/go/bin dono jagah binary dhundta hai."""

    if shutil.which(name):
        return True

    candidate = os.path.join(GO_BIN, name)

    return os.path.isfile(candidate) and os.access(candidate, os.X_OK)


def _run(cmd, quiet=True):

    try:
        if quiet:
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.run(cmd, shell=True, check=True)

        return True

    except subprocess.CalledProcessError:
        return False


def _ensure_go_installed():

    if shutil.which("go"):
        return True

    console.print("[yellow][!] Go toolchain nahi mila. Installing golang-go...[/yellow]")

    ok = _run("sudo apt-get update -y && sudo apt-get install -y golang-go")

    if ok and shutil.which("go"):
        console.print("[green][+] Go installed successfully.[/green]")
        return True

    console.print(
        "[red][-] Go install nahi ho paya. Go-based tools (subfinder, httpx, "
        "naabu, katana, gau, waybackurls, amass) skip ho jayenge.[/red]"
    )

    return False


def _ensure_apt_tool(binary_name, apt_pkg):

    if _binary_exists(binary_name):
        return True

    console.print(f"[yellow][!] '{binary_name}' missing. Installing via apt...[/yellow]")

    ok = _run(f"sudo apt-get install -y {apt_pkg}")

    if ok and _binary_exists(binary_name):
        console.print(f"[green][+] '{binary_name}' installed successfully.[/green]")
        return True

    console.print(f"[red][-] '{binary_name}' install nahi ho paya. Manually install kar lena.[/red]")

    return False


def _ensure_go_tool(binary_name, go_path):

    if _binary_exists(binary_name):
        return True

    console.print(f"[yellow][!] '{binary_name}' missing. Installing via go install...[/yellow]")

    ok = _run(f"go install -v {go_path}@latest")

    # amass v4 needs @master sometimes; fallback attempt
    if not ok and "amass" in go_path:
        ok = _run(f"go install -v {go_path}@master")

    if ok and _binary_exists(binary_name):
        console.print(f"[green][+] '{binary_name}' installed successfully.[/green]")
        return True

    console.print(f"[red][-] '{binary_name}' install nahi ho paya. Manually install kar lena.[/red]")

    return False


def _ensure_python_packages():

    missing = []

    for pkg in PYTHON_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if not missing:
        return

    console.print(f"[yellow][!] Python packages missing: {', '.join(missing)}. Installing...[/yellow]")

    _run(
        f"{sys.executable} -m pip install --break-system-packages {' '.join(missing)}",
        quiet=False,
    )


def ensure_all_tools():
    """Main entry point - VAJRA start hone se pehle ye call hota hai."""

    console.print("\n[bold cyan][*] Checking VAJRA dependencies...[/bold cyan]\n")

    # ---------------------------------------------------------
    # 1. Python packages (rich/pyfiglet already needed for banner
    #    itself, so this mostly matters on very first ever run
    #    via a plain `python3 main.py` before rich is available)
    # ---------------------------------------------------------
    _ensure_python_packages()

    # ---------------------------------------------------------
    # 2. Go toolchain (needed for most recon tools)
    # ---------------------------------------------------------
    go_ok = _ensure_go_installed()

    if go_ok:
        os.environ["PATH"] = GO_BIN + os.pathsep + os.environ.get("PATH", "")

    # ---------------------------------------------------------
    # 3. APT-based tools
    # ---------------------------------------------------------
    for binary, pkg in APT_TOOLS.items():
        _ensure_apt_tool(binary, pkg)

    # ---------------------------------------------------------
    # 4. Go-based recon tools
    # ---------------------------------------------------------
    if go_ok:
        for binary, path in GO_TOOLS.items():
            _ensure_go_tool(binary, path)
    else:
        console.print("[red][-] Go missing hai isliye Go-based tools install skip kiye ja rahe hain.[/red]")

    console.print("\n[bold green][+] Dependency check complete![/bold green]\n")
