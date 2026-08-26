# VAJRA ⚡ Web Enumeration Framework

```
██╗   ██╗ █████╗      ██╗██████╗  █████╗
██║   ██║██╔══██╗     ██║██╔══██╗██╔══██╗
██║   ██║███████║     ██║██████╔╝███████║
╚██╗ ██╔╝██╔══██║██   ██║██╔══██╗██╔══██║
 ╚████╔╝ ██║  ██║╚█████╔╝██████╔╝██║  ██║
  ╚═══╝  ╚═╝  ╚═╝ ╚════╝ ╚═════╝ ╚═╝  ╚═╝
        ⚡ WEB ENUMERATION FRAMEWORK ⚡
             ॐ  VAJRA  ॐ
```

A full auto-pipeline recon framework for Kali Linux: subdomain enumeration,
live host checking, endpoint collection, port scanning, and technology
fingerprinting — chained together automatically, with **self-healing
dependency installation**.

## 🚀 Usage (Kali Linux)

Unzip and run **one command**:

```bash
unzip vajra.zip
cd vajra
bash install.sh
```

That's it. `install.sh` bootstraps Python dependencies, and `main.py` itself
checks for every recon tool it needs (`subfinder`, `amass`, `httpx`, `naabu`,
`masscan`, `whatweb`, `katana`, `gau`, `waybackurls`) and installs whichever
one is missing via `apt` or `go install`, before starting the scan.

If you ever add VAJRA to a new machine, the very first run will take longer
since it's downloading/installing missing tools — every run after that is
fast since it only installs what's still missing.

### Manual run (after first-time setup)

```bash
python3 main.py
```

## 📋 What it does

| Stage | Tool(s) | Output |
|---|---|---|
| Subdomain Enumeration | `subfinder`, `amass` | `output/<domain>/final_subdomains.txt` |
| Live Host Check | `httpx` | `output/<domain>/live_subdomains.txt` |
| Endpoint Collection | `katana`, `gau`, `waybackurls` | `output/<domain>/all_endpoints.txt` |
| Port Scanning | `masscan`, `naabu` | `output/<domain>/open_ports.txt` |
| Tech Fingerprinting | `whatweb` | `output/<domain>/technologies.txt` |

## 🔧 Fixes over the original version

- **Domain sanitization**: entering a full URL (`https://example.com/path`)
  no longer creates broken nested output folders — only the clean hostname
  is used.
- **Endpoint collection wired in**: previously built but never called from
  `main.py`; now part of the pipeline.
- **`masscan` sudo handling**: automatically prefixes `sudo` when not
  already running as root, instead of silently failing.
- **Graceful tool-missing handling**: each module checks whether its tool
  exists before running, and prints a clear message instead of silently
  producing empty output files.

## ⚠️ Notes

- `masscan` needs raw-socket privileges — you may be prompted for your sudo
  password on first port scan.
- Only use VAJRA against domains you own or have explicit permission to test.
- First-time tool installation requires an internet connection.
