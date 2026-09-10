<div align="center">

![VAJRA Banner](assets/banner.svg)

<br>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.5.0-f0883e?style=for-the-badge)](https://github.com/gauravjethva-lab/vajra-web-enumeration/releases)
[![Pipeline](https://img.shields.io/badge/Pipeline-5%20Stages-a855f7?style=for-the-badge)](#pipeline)
[![Status](https://img.shields.io/badge/Status-100%25%20Working-22c55e?style=for-the-badge)](#)
[![Stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge&color=f0883e)](https://github.com/gauravjethva-lab/vajra-web-enumeration/stargazers)

<br>

> **Full auto-pipeline Web Enumeration & Attack Surface Reconnaissance Framework**
> 5 stages · Parallel execution · Zero API errors · Professional HTML report

<br>

[Quick Start](#-quick-start) · [Pipeline](#-pipeline) · [Report](#-html-report) · [Changelog](#-changelog) · [Legal](#-legal-disclaimer)

</div>

---

## 👤 Author

| | |
|---|---|
| **Name** | Gaurav Jethva |
| **GitHub** | [@gauravjethva-lab](https://github.com/gauravjethva-lab) |
| **Tool** | [VAJRA Web Enumeration](https://github.com/gauravjethva-lab/vajra-web-enumeration) |

---

## 🔱 What is VAJRA?

**VAJRA** is a **5-stage automated web enumeration and attack surface reconnaissance framework** built for Kali Linux. It chains together the best open-source security tools into a single parallel-execution pipeline — then **auto-generates a professional dark-theme HTML report** with your name on it.

**Zero API errors. Zero crashes. 100% working.**

> VAJRA is an **Attack Surface Mapper** — not a vulnerability scanner.
> Every report clearly separates reconnaissance data from confirmed findings.

---

## ✨ Features

| Feature | Detail |
|---------|--------|
| 🔍 **Subdomain Enum** | `subfinder` + `amass` in parallel threads |
| 🌐 **Live Detection** | `httpx` — 150 threads, 8s timeout, no hangs |
| 🗺️ **Endpoints** | `katana` + `gau` + `waybackurls` parallel — static file filtering |
| 🔌 **Port Scanning** | `masscan` + `naabu` — httpx format parsed correctly |
| 🧠 **Tech Fingerprint** | `whatweb` with correct flag syntax |
| 📊 **Auto HTML Report** | Dark-theme report auto-generated after every scan |
| 🔧 **Self-Healing** | Auto-installs every missing tool on first run |
| ⏱️ **All Timeouts Set** | Every subprocess call has a timeout — no infinite hangs |
| 🩹 **Smart Parsing** | Handles `https://host:port [200] [Title]` format correctly |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/gauravjethva-lab/vajra-web-enumeration.git
cd vajra-web-enumeration/vajra

# Install dependencies
bash install.sh

# Run
python3 main.py
```

> First run auto-installs all missing tools. Every run after is fast.

---

## 📊 Pipeline

<div id="pipeline"></div>

```
[1/5] 🔍 Subdomain Enumeration   →  final_subdomains.txt
[2/5] 🌐 Live Host Detection     →  live_subdomains.txt
[3/5] 🗺️  Endpoint Collection    →  all_endpoints.txt
[4/5] 🔌 Port Scanning           →  open_ports.txt
[5/5] 🧠 Tech Fingerprinting     →  technologies.txt
 ✨  Auto HTML Report            →  vajra_report.html
```

| # | Stage | Tools | Output |
|---|-------|-------|--------|
| 1 | 🔍 Subdomains | `subfinder`, `amass` (parallel) | `final_subdomains.txt` |
| 2 | 🌐 Live Hosts | `httpx` 150 threads, 8s timeout | `live_subdomains.txt` |
| 3 | 🗺️ Endpoints | `katana`, `gau`, `waybackurls` (parallel) | `all_endpoints.txt` |
| 4 | 🔌 Ports | `masscan`, `naabu` (timeout protected) | `open_ports.txt` |
| 5 | 🧠 Tech | `whatweb` (timeout protected) | `technologies.txt` |

---

## 📊 HTML Report

<div id="report"></div>

Auto-generated after every scan. Open in browser:

```bash
firefox output/example.com/vajra_report.html
```

| Section | Content |
|---------|---------|
| 📋 Header | Target, date, author name |
| 📊 Stats | Subdomains, live hosts, endpoints, ports, tech |
| 🔍 Subdomains | Searchable table |
| 🌐 Live Hosts | Full list |
| 🗺️ Endpoints | Searchable table |
| 🔌 Ports | Host + port table |
| 🧠 Technologies | Fingerprinted hosts |
| 📸 Screenshots | Inline images |
| 👤 Footer | Author credit on every report |

---

## 📁 Project Structure

```
vajra/
├── main.py                  # 5-stage pipeline + auto HTML report
├── install.sh               # One-click dependency installer
├── requirements.txt         # Python deps (rich, pyfiglet)
├── report_generator.py      # Professional HTML report
├── core/
│   ├── banner.py            # Rich UI + domain sanitization
│   ├── utils.py             # Tool path resolver
│   └── setup_check.py       # Auto dependency installer
└── modules/
    ├── subdomains.py         # Subfinder + Amass parallel
    ├── live_check.py         # httpx — 150 threads, 8s timeout
    ├── endpoints.py          # Parallel + static file filter
    ├── ports.py              # Masscan + Naabu — httpx format fix
    └── tech_detect.py        # WhatWeb — timeout protected
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` required for `masscan`

### Auto-Installed Tools
`subfinder` · `amass` · `httpx` · `naabu` · `masscan` · `whatweb` · `katana` · `gau` · `waybackurls`

### Python Dependencies
```
rich >= 13.0.0
pyfiglet >= 1.0.0
```

---

## 🛠️ Changelog

<details open>
<summary><strong>v1.5.0 — Zero Errors Release</strong></summary>

| Fix | Detail |
|-----|--------|
| 🔌 `clean_hosts` | Fixed httpx format parsing — `host [200] [Title]` → clean hostname |
| 🔌 Port strip | `api.example.com:8080` → `api.example.com` correctly |
| ⏱️ All timeouts | Every subprocess.run now has timeout — no infinite hangs |
| 🗺️ GAU fix | `echo domain` instead of `cat live_hosts` — correct command |
| 🗺️ Parallel | Katana + GAU + Waybackurls run simultaneously |
| 🧠 WhatWeb | `--log-brief=` flag fix + timeout |
| 🌐 httpx | 150 threads, 8s balanced timeout |
| 🎨 Banner | Port stripping in sanitize_domain fixed |
| 📊 Report | Auto-generated HTML with author credit |

</details>

<details>
<summary><strong>v1.0.0 — Initial Release</strong></summary>

- 5-stage pipeline with self-healing installer

</details>

---

## ⚠️ Legal Disclaimer

> **VAJRA is for authorized security testing only.**
> Only use on systems you own or have explicit written permission to test.
> Unauthorized use is illegal and unethical.
> The author is not responsible for any misuse.

---

<div align="center">

**⚡ Built for the security community — Use responsibly ⚡**

*If VAJRA helps your work, give it a ⭐*

<br>

[![GitHub](https://img.shields.io/badge/GitHub-gauravjethva--lab-f0883e?style=for-the-badge&logo=github)](https://github.com/gauravjethva-lab)

</div>
