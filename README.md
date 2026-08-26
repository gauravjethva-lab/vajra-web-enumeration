<div align="center">

![VAJRA Banner](assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.1.0-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge)

</div>

---

## 🔱 What is VAJRA?

**VAJRA** is a full auto-pipeline reconnaissance framework built for **Kali Linux**. It chains together the best open-source recon tools into a **single automated workflow** with **self-healing dependency installation**.

> Run one command. VAJRA does the rest.

---

## ✨ Features

- 🔍 **Subdomain Enumeration** — powered by `subfinder` + `amass` (parallel threads)
- 🌐 **Live Host Detection** — via `httpx` with status codes + page titles
- 🗺️ **Endpoint Collection** — `katana` + `gau` + `waybackurls` with smart deduplication & static file filtering
- 🔌 **Port Scanning** — `masscan` (full 1-65535) + `naabu` (top 1000), results merged
- 🧠 **Technology Fingerprinting** — via `whatweb`
- 🔧 **Self-Healing Install** — auto-installs every missing tool on first run
- 📊 **HTML Report Generator** — beautiful dark-theme scan report
- 📋 **Markdown Summary** — clean recon summary in `.md` format
- ⏱️ **Per-stage Timing** — see exactly how long each stage takes
- 🎨 **Rich Terminal UI** — colored output, progress bars, summary table

---

## 🖥️ Terminal Preview

```
 Stage [1/5] : Subdomain Enumeration
 ──────────────────────────────────────────────────
 [+] Running Subfinder...
 [✓] Subfinder: 43 subdomains
 [+] Running Amass (passive)...
 [✓] Amass: 31 subdomains
 [✓] Total Unique Subdomains: 58

 Stage [2/5] : Live Host Detection
 ──────────────────────────────────────────────────
 [+] Running httpx (status + titles)...
 [✓] Live Hosts Found: 24

 Stage [3/5] : Endpoint Collection
 ──────────────────────────────────────────────────
 [+] Running Katana, GAU, Waybackurls...
 [✓] Unique Useful Endpoints: 1342

 Stage [4/5] : Port Scanning
 ──────────────────────────────────────────────────
 [+] Running Naabu + Masscan (1-65535)...
 [✓] Open Ports Found: 38

 Stage [5/5] : Technology Fingerprinting
 ──────────────────────────────────────────────────
 [+] Running WhatWeb...
 [✓] 24 hosts fingerprinted

 +-----------------------+--------+---------+
 | Stage                 | Status |    Time |
 +-----------------------+--------+---------+
 | Subdomain Enumeration |   Done |  45.2s  |
 | Live Host Check       |   Done |  12.1s  |
 | Endpoint Collection   |   Done |  88.4s  |
 | Port Scanning         |   Done |  33.7s  |
 | Tech Fingerprinting   |   Done |  18.9s  |
 +-----------------------+--------+---------+
 Results saved in: output/example.com/
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/gauravjethva-lab/vajra-web-enumeration.git
cd vajra-web-enumeration/vajra

# 2. Run installer (handles everything automatically)
bash install.sh

# 3. Launch VAJRA
python3 main.py
```

> ⚠️ First run may take longer as VAJRA installs missing tools automatically. Every run after that is fast.

---

## 📊 Pipeline Overview

| # | Stage | Tool(s) | Output File |
|---|-------|---------|-------------|
| 1 | 🔍 Subdomain Enumeration | `subfinder`, `amass` | `output/<domain>/final_subdomains.txt` |
| 2 | 🌐 Live Host Check | `httpx` (status + title) | `output/<domain>/live_subdomains.txt` |
| 3 | 🗺️ Endpoint Collection | `katana`, `gau`, `waybackurls` | `output/<domain>/all_endpoints.txt` |
| 4 | 🔌 Port Scanning | `masscan` (1-65535), `naabu` (top 1000) | `output/<domain>/open_ports.txt` |
| 5 | 🧠 Tech Fingerprinting | `whatweb` | `output/<domain>/technologies.txt` |

---

## 📈 Generate Reports

```bash
# HTML Report (dark themed)
python3 report_generator.py example.com

# Markdown Summary
python3 recon_summary.py example.com
```

---

## 📁 Project Structure

```
vajra/
├── main.py                   # Entry point — full pipeline + summary table
├── install.sh                # One-click dependency installer
├── requirements.txt          # Python dependencies
├── report_generator.py       # HTML scan report generator
├── recon_summary.py          # Markdown recon summary generator
├── modules/
│   ├── subdomains.py         # Subfinder + Amass (parallel threads)
│   ├── live_check.py         # httpx with status + title
│   ├── endpoints.py          # Katana + GAU + Wayback + dedup + filter
│   ├── ports.py              # Masscan (1-65535) + Naabu merged
│   └── tech_detect.py        # WhatWeb fingerprinting
└── core/
    ├── banner.py             # Rich UI, ASCII banner, loading animation
    ├── utils.py              # Tool path resolver
    └── setup_check.py        # Auto dependency installer
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

### v1.1.0 — Bug Fix Release
| Fix | Description |
|-----|-------------|
| 🎨 Banner Fix | ASCII art rendering fixed |
| 🌐 httpx | Status codes + page titles for live hosts |
| 🗺️ Endpoints | Static file filtering + deduplication |
| 🔌 Masscan | Port range expanded to full 1-65535 |
| ⏱️ Timing | Per-stage timing in final summary table |

### v1.0.0 — Initial Release
- Full auto-pipeline, self-healing installer, HTML + Markdown reports

---

## ⚠️ Legal Disclaimer

> **VAJRA is for authorized security testing only.**
> Only use on systems you own or have explicit permission to test.
> The author is not responsible for any misuse.

---

## 👤 Author

**Gaurav Jethva** — [@gauravjethva-lab](https://github.com/gauravjethva-lab)

---

<div align="center">

**⚡ Built for the security community. Use responsibly. ⚡**

*If VAJRA helps you, give it a ⭐ on GitHub!*

</div>
