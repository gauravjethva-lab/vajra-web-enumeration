import os, shutil, subprocess, sys
from rich.console import Console

console = Console()
GO_BIN = os.path.expanduser("~/go/bin")

APT_TOOLS = {
    "masscan":  "masscan",
    "whatweb":  "whatweb",
    "nmap":     "nmap",
    "wafw00f":  "wafw00f",
    "ffuf":     "ffuf",
    "dnsutils": "dnsutils",
    "whois":    "whois",
}

GO_TOOLS = {
    "subfinder":  "github.com/projectdiscovery/subfinder/v2/cmd/subfinder",
    "httpx":      "github.com/projectdiscovery/httpx/cmd/httpx",
    "naabu":      "github.com/projectdiscovery/naabu/v2/cmd/naabu",
    "katana":     "github.com/projectdiscovery/katana/cmd/katana",
    "dnsx":       "github.com/projectdiscovery/dnsx/cmd/dnsx",
    "gau":        "github.com/lc/gau/v2/cmd/gau",
    "waybackurls":"github.com/tomnomnom/waybackurls",
    "amass":      "github.com/owasp-amass/amass/v4/...",
    "gowitness":  "github.com/sensepost/gowitness",
}

PYTHON_PACKAGES = ["rich", "pyfiglet"]

def _binary_exists(name):
    if shutil.which(name): return True
    candidate = os.path.join(GO_BIN, name)
    return os.path.isfile(candidate) and os.access(candidate, os.X_OK)

def _run(cmd, quiet=True):
    try:
        subprocess.run(cmd, shell=True, check=True,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None)
        return True
    except subprocess.CalledProcessError:
        return False

def _ensure_go_installed():
    if shutil.which("go"): return True
    console.print("[yellow][!] Go toolchain missing. Installing...[/yellow]")
    ok = _run("sudo apt-get update -y && sudo apt-get install -y golang-go")
    if ok and shutil.which("go"):
        console.print("[green][+] Go installed.[/green]")
        return True
    console.print("[red][-] Go install failed. Go-based tools will be skipped.[/red]")
    return False

def _ensure_apt_tool(binary_name, apt_pkg):
    if _binary_exists(binary_name): return True
    console.print(f"[yellow][!] '{binary_name}' missing. Installing via apt...[/yellow]")
    ok = _run(f"sudo apt-get install -y {apt_pkg}")
    if ok and _binary_exists(binary_name):
        console.print(f"[green][+] '{binary_name}' installed.[/green]")
        return True
    console.print(f"[red][-] '{binary_name}' install failed.[/red]")
    return False

def _ensure_go_tool(binary_name, go_path):
    if _binary_exists(binary_name): return True
    console.print(f"[yellow][!] '{binary_name}' missing. Installing via go...[/yellow]")
    ok = _run(f"go install -v {go_path}@latest")
    if not ok and "amass" in go_path:
        ok = _run(f"go install -v {go_path}@master")
    if ok and _binary_exists(binary_name):
        console.print(f"[green][+] '{binary_name}' installed.[/green]")
        return True
    console.print(f"[red][-] '{binary_name}' install failed.[/red]")
    return False

def _ensure_python_packages():
    missing = [p for p in PYTHON_PACKAGES if not __import__('importlib').util.find_spec(p)]
    if not missing: return
    console.print(f"[yellow][!] Missing Python packages: {', '.join(missing)}[/yellow]")
    _run(f"{sys.executable} -m pip install --break-system-packages {' '.join(missing)}", quiet=False)

def ensure_all_tools():
    console.print("\n[bold cyan][*] Checking VAJRA dependencies...[/bold cyan]\n")
    _ensure_python_packages()
    go_ok = _ensure_go_installed()
    if go_ok:
        os.environ["PATH"] = GO_BIN + os.pathsep + os.environ.get("PATH", "")
    for binary, pkg in APT_TOOLS.items():
        _ensure_apt_tool(binary, pkg)
    if go_ok:
        for binary, path in GO_TOOLS.items():
            _ensure_go_tool(binary, path)
    console.print("\n[bold green][+] Dependency check complete![/bold green]\n")
