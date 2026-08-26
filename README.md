<div align="center">

```
██╗   ██╗ █████╗      ██╗██████╗  █████╗
██║   ██║██╔══██╗     ██║██╔══██╗██╔══██╗
██║   ██║███████║     ██║██████╔╝███████║
╚██╗ ██╔╝██╔══██║██   ██║██╔══██╗██╔══██║
 ╚████╔╝ ██║  ██║╚█████╔╝██████╔╝██║  ██║
  ╚═══╝  ╚═╝  ╚═╝ ╚════╝ ╚═════╝ ╚═╝  ╚═╝
```

### ⚡ VAJRA — Web Enumeration Framework ⚡
### ॐ  Automated Recon. Zero Setup. Full Pipeline.  ॐ

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge)

</div>

---

## 🔱 What is VAJRA?

**VAJRA** is a full auto-pipeline reconnaissance framework built for **Kali Linux**. It chains together the best open-source recon tools — subdomain enumeration, live host checking, endpoint collection, port scanning, and technology fingerprinting — into a **single automated workflow** with **self-healing dependency installation**.

> Run one command. VAJRA does the rest.

---

## ✨ Features

- 🔍 **Subdomain Enumeration** — powered by `subfinder` + `amass`
- 🌐 **Live Host Detection** — via `httpx`
- 🗺️ **Endpoint Collection** — using `katana`, `gau`, `waybackurls`
- 🔌 **Port Scanning** — with `masscan` + `naabu`
- 🧠 **Technology Fingerprinting** — via `whatweb`
- 🔧 **Self-Healing Install** — auto-installs missing tools on first run
- 🩹 **Smart Domain Sanitization** — handles full URLs gracefully
- ⚡ **Zero Manual Setup** — one script, everything works

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/gauravjethva-lab/vajra-web-enumeration.git
cd vajra-web-enumeration/vajra

# 2. Run installer (handles everything)
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
| 2 | 🌐 Live Host Check | `httpx` | `output/<domain>/live_subdomains.txt` |
| 3 | 🗺️ Endpoint Collection | `katana`, `gau`, `waybackurls` | `output/<domain>/all_endpoints.txt` |
| 4 | 🔌 Port Scanning | `masscan`, `naabu` | `output/<domain>/open_ports.txt` |
| 5 | 🧠 Tech Fingerprinting | `whatweb` | `output/<domain>/technologies.txt` |

All results are saved in `output/<domain>/` directory.

---

## 📁 Project Structure

```
vajra/
├── main.py                  # Entry point — runs the full pipeline
├── install.sh               # Dependency installer
├── requirements.txt         # Python dependencies
├── README.md
├── modules/
│   ├── subdomains.py        # Subdomain enumeration
│   ├── live_check.py        # Live host checker
│   ├── endpoints.py         # Endpoint collection
│   ├── ports.py             # Port scanner
│   └── tech_detect.py       # Technology fingerprinter
└── core/
    ├── banner.py            # ASCII banner & UI
    ├── utils.py             # Shared utilities
    └── setup_check.py       # Tool availability checker
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / any Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` access (required for `masscan`)

### Python Dependencies
```
rich>=13.0.0
pyfiglet>=1.0.0
```

### External Tools (Auto-installed by VAJRA)
`subfinder` • `amass` • `httpx` • `naabu` • `masscan` • `whatweb` • `katana` • `gau` • `waybackurls`

---

## 🛠️ Changelog & Improvements

| Fix | Description |
|-----|-------------|
| 🩹 Domain Sanitization | Full URLs like `https://example.com/path` are cleaned to hostname only |
| 🔗 Endpoint Pipeline | Endpoint collection was built but not wired — now fully integrated |
| 🔐 Masscan sudo | Auto-prefixes `sudo` when not running as root |
| 🛡️ Graceful Fallback | Each module checks for its tool before running — no silent failures |

---

## ⚠️ Legal Disclaimer

> **VAJRA is intended for authorized security testing only.**
> Only use VAJRA against domains and systems you **own** or have **explicit written permission** to test.
> Unauthorized use is illegal and unethical. The author is not responsible for any misuse.

---

## 👤 Author

**Gaurav Jethva**
- GitHub: [@gauravjethva-lab](https://github.com/gauravjethva-lab)

---

<div align="center">

**⚡ Built for the community. Use responsibly. ⚡**

*If you find VAJRA useful, consider giving it a ⭐ on GitHub!*

</div>
