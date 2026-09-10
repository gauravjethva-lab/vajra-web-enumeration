<div align="center">

![VAJRA Banner](assets/banner.svg)

<br>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.6.0-f0883e?style=for-the-badge)](https://github.com/gauravjethva-lab/vajra-web-enumeration/releases)
[![Pipeline](https://img.shields.io/badge/Pipeline-5%20Stages-a855f7?style=for-the-badge)](#pipeline)
[![Errors](https://img.shields.io/badge/Errors-Zero-22c55e?style=for-the-badge)](#)
[![Stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge&color=f0883e)](https://github.com/gauravjethva-lab/vajra-web-enumeration/stargazers)

<br>

> **Full auto-pipeline Web Enumeration & Attack Surface Reconnaissance Framework**
> 5 stages · Parallel execution · Zero errors · Professional HTML report

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

---

## ✨ Features

| Feature | Detail |
|---------|--------|
| 🔍 **Subdomain Enum** | `subfinder` + `amass` parallel — timeout protected |
| 🌐 **Live Detection** | `httpx` 150 threads, 8s timeout, missing file safe |
| 🗺️ **Endpoints** | `katana` + `gau` + `waybackurls` parallel — 23 extension filters |
| 🔌 **Port Scanning** | `masscan` + `naabu` — httpx format parsed correctly |
| 🧠 **Tech Fingerprint** | `whatweb` — timeout + missing file protected |
| 📊 **Auto HTML Report** | Dark-theme report with sidebar, search, stats |
| 🔧 **Self-Healing** | Auto-installs every missing tool |
| ⏱️ **All Timeouts** | Every subprocess has timeout — no infinite hangs |
| 🛡️ **Error Handling** | Every module handles missing files + exceptions |
| 🩹 **Smart Parsing** | Correctly handles `https://host:port [200] [Title]` |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/gauravjethva-lab/vajra-web-enumeration.git
cd vajra-web-enumeration/vajra

# Install
bash install.sh

# Run
python3 main.py
```

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
| 1 | 🔍 Subdomains | `subfinder`, `amass` parallel | `final_subdomains.txt` |
| 2 | 🌐 Live Hosts | `httpx` 150 threads | `live_subdomains.txt` |
| 3 | 🗺️ Endpoints | `katana`, `gau`, `waybackurls` parallel | `all_endpoints.txt` |
| 4 | 🔌 Ports | `masscan`, `naabu` | `open_ports.txt` |
| 5 | 🧠 Tech | `whatweb` | `technologies.txt` |

---

## 📊 HTML Report

<div id="report"></div>

Auto-generated after every scan:

```bash
firefox output/example.com/vajra_report.html
```

| Section | Content |
|---------|---------|
| 📊 Stats | Subdomains, live hosts, endpoints, ports, tech |
| 🔍 Subdomains | Searchable table |
| 🌐 Live Hosts | Full list |
| 🗺️ Endpoints | Searchable table |
| 🔌 Ports | Host + port table |
| 🧠 Technologies | Fingerprinted hosts |
| 📸 Screenshots | Inline images |
| 👤 Footer | Author credit — Gaurav Jethva |

---

## 📁 Project Structure

```
vajra/
├── main.py                  # 5-stage pipeline + auto HTML report
├── install.sh               # One-click dependency installer
├── requirements.txt         # Python deps
├── report_generator.py      # Professional HTML report
├── core/
│   ├── banner.py            # Rich UI + domain sanitization
│   ├── utils.py             # Tool path resolver
│   └── setup_check.py       # Auto dependency installer
└── modules/
    ├── subdomains.py         # Parallel + timeout + safe save
    ├── live_check.py         # Missing file + partial results safe
    ├── endpoints.py          # Parallel + 23 filters + exception handling
    ├── ports.py              # httpx format + edge case handling
    └── tech_detect.py        # Missing file + timeout + count display
```

---

## ⚙️ Requirements

- **OS:** Kali Linux / Debian Linux
- **Python:** 3.8+
- **Permissions:** `sudo` for `masscan`

### Auto-Installed
`subfinder` · `amass` · `httpx` · `naabu` · `masscan` · `whatweb` · `katana` · `gau` · `waybackurls`

---

## 🛠️ Changelog

<details open>
<summary><strong>v1.6.0 — Zero Error Release</strong></summary>

| Fix | Detail |
|-----|--------|
| ⏱️ `run_command` | Timeout added — no more infinite hangs on slow tools |
| 🛡️ Missing files | All modules handle missing input files gracefully |
| 🔌 `clean_hosts` | Bracket strip — `[200]` no longer included in hostnames |
| 🔌 Port parsing | `IndexError` + `ValueError` caught in masscan parsing |
| 🗺️ Endpoints | Per-tool exception handling — one tool crash won't stop others |
| 🧠 Tech count | Technologies detected count now shown after scan |
| ⏱️ All timeouts | Every single subprocess.run has timeout — verified |

</details>

<details>
<summary><strong>v1.5.0 — Clean Foundation</strong></summary>

- clean_hosts httpx format fix
- gau echo command fix
- Parallel endpoint collection

</details>

<details>
<summary><strong>v1.0.0 — Initial Release</strong></summary>

- 5-stage pipeline with self-healing installer

</details>

---

## ⚠️ Legal Disclaimer

> **For authorized security testing only.**
> Only use on systems you own or have explicit written permission to test.
> The author is not responsible for any misuse.

---

<div align="center">

**⚡ Built for the security community — Use responsibly ⚡**

*Give it a ⭐ if VAJRA helps your work!*

[![GitHub](https://img.shields.io/badge/GitHub-gauravjethva--lab-f0883e?style=for-the-badge&logo=github)](https://github.com/gauravjethva-lab)

</div>
