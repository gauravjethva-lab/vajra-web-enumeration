<div align="center">

![VAJRA Banner](assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.2.0-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge)

</div>

---

## 🔱 What is VAJRA?

**VAJRA** is a full auto-pipeline web enumeration & reconnaissance framework built for **Kali Linux**. It chains together the best open-source recon tools into a **5-stage automated workflow** with **self-healing dependency installation** — and auto-generates a **professional HTML report** when the scan is done.

> Run one command. VAJRA scans. VAJRA reports.

---

## ✨ Features

- 🔍 **Subdomain Enumeration** — `subfinder` + `amass` running in parallel threads
- 🌐 **Live Host Detection** — `httpx` with timeout protection
- 🗺️ **Endpoint Collection** — `katana` + `gau` + `waybackurls` with timeout handling
- 🔌 **Port Scanning** — `masscan` + `naabu` with graceful empty-host handling
- 🧠 **Technology Fingerprinting** — `whatweb` with fixed flag syntax
- 📊 **Auto HTML Report** — professional dark-theme report auto-generated after every scan
- 🔧 **Self-Healing Install** — auto-installs every missing tool on first run
- 🩹 **Smart Domain Sanitization** — handles full URLs like `https://example.com/path` cleanly

---

## 🖥️ Terminal Preview

```
  ██╗   ██╗ █████╗      ██╗██████╗  █████╗
  ██║   ██║██╔══██╗     ██║██╔══██╗██╔══██╗
  ██║   ██║███████║     ██║██████╔╝███████║
  ╚██╗ ██╔╝██╔══██║██╗ ██║██╔══██╗██╔══██║
   ╚████╔╝ ██║  ██║╚█████╔╝██║  ██║██║  ██║
    ╚═══╝  ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

[?] Enter Domain or URL: example.com

[+] Target: example.com
[+] Running Subfinder...
[+] Running Amass...
[+] Total Unique Subdomains: 47
[+] Results saved in output/example.com

[+] Checking live subdomains...
[+] Live hosts saved to output/example.com/live_subdomains.txt

[+] Starting Endpoint Collection...
[+] Running Katana...
[+] Running gau...
[+] Running waybackurls...
[+] Total Unique Endpoints: 1342

[+] Preparing Hosts For Port Scanning...
[+] Running Masscan...
[+] Running Naabu...
[+] Open ports saved to output/example.com/open_ports.txt

[+] Detecting Technologies...
[+] Technology results saved to output/example.com/technologies.txt

[+] VAJRA Recon Pipeline Completed Successfully!
[*] Generating HTML Report...
✅ Report saved: output/example.com/vajra_report.html
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/gauravjethva-lab/vajra-web-enumeration.git
cd vajra-web-enumeration/vajra

# 2. Run installer
bash install.sh

# 3. Launch VAJRA
python3 main.py
```

> ⚠️ First run installs all missing tools automatically. Every run after that is fast.

---

## 📊 Pipeline Overview

| # | Stage | Tool(s) | Output File |
|---|-------|---------|-------------|
| 1 | 🔍 Subdomain Enumeration | `subfinder`, `amass` (parallel) | `final_subdomains.txt` |
| 2 | 🌐 Live Host Check | `httpx` | `live_subdomains.txt` |
| 3 | 🗺️ Endpoint Collection | `katana`, `gau`, `waybackurls` | `all_endpoints.txt` |
| 4 | 🔌 Port Scanning | `masscan`, `naabu` | `open_ports.txt` |
| 5 | 🧠 Tech Fingerprinting | `whatweb` | `technologies.txt` |
| ✨ | 📊 HTML Report (auto) | `report_generator.py` | `vajra_report.html` |

All results saved in `output/<domain>/` directory.

---

## 📊 HTML Report

After every scan, VAJRA **automatically generates** a professional dark-theme HTML report. Open it in any browser:

```bash
firefox output/example.com/vajra_report.html
```

**Report includes:**
- 📈 Stats dashboard — subdomains, live hosts, endpoints, ports, technologies
- 🔍 Searchable tables for subdomains, endpoints, directories
- 🚨 Security alerts — CORS issues, JS secrets highlighted in red
- 🌍 Passive recon, DNS records, WAF detection results
- 🔌 Open ports table, 🧠 technology fingerprints
- 📸 Screenshots (if gowitness is used)
- 🗂️ Sidebar navigation — jump to any section instantly

---

## 📁 Project Structure

```
vajra/
├── main.py                  # Entry point — 5-stage pipeline + auto report
├── install.sh               # One-click dependency installer
├── requirements.txt         # Python deps (rich, pyfiglet)
├── report_generator.py      # Auto HTML report generator
├── recon_summary.py         # Markdown summary generator
├── modules/
│   ├── subdomains.py        # Subfinder + Amass (parallel threads)
│   ├── live_check.py        # httpx with timeout
│   ├── endpoints.py         # Katana + GAU + Wayback (timeout fixed)
│   ├── ports.py             # Masscan + Naabu (empty host fix)
│   └── tech_detect.py       # WhatWeb (flag fix)
└── core/
    ├── banner.py            # Rich UI + ASCII banner
    ├── utils.py             # Tool path resolver
    └── setup_check.py       # Auto dependency installer
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` access (required for `masscan`)

### External Tools (Auto-installed)
`subfinder` • `amass` • `httpx` • `naabu` • `masscan` • `whatweb` • `katana` • `gau` • `waybackurls`

---

## 🛠️ Changelog

### v1.2.0 — Stability Release
| Fix | Description |
|-----|-------------|
| 📊 Auto HTML Report | Professional dark-theme report auto-generated after every scan |
| 🗺️ endpoints.py | `gau` timeout fixed (120s), correct `echo domain` command |
| 🔌 ports.py | Crash fixed when live hosts file is empty |
| 🧠 tech_detect.py | `--log-brief=` flag syntax fixed |
| 🩹 Pipeline | Restored clean working 5-stage pipeline |

### v1.1.0 — Bug Fix Release
| Fix | Description |
|-----|-------------|
| 🎨 Banner | ASCII art rendering fixed |
| 🌐 httpx | Status codes + titles added |
| 🗺️ Endpoints | Static file filtering + deduplication |

### v1.0.0 — Initial Release
- Full auto-pipeline, self-healing installer

---

## ⚠️ Legal Disclaimer

> **VAJRA is for authorized security testing only.**
> Only use on systems you own or have explicit written permission to test.
> The author is not responsible for any misuse.

---

## 👤 Author

**Gaurav Jethva** — [@gauravjethva-lab](https://github.com/gauravjethva-lab)

---

<div align="center">

**⚡ Built for the security community. Use responsibly. ⚡**

*If VAJRA helps you, give it a ⭐ on GitHub!*

</div>
