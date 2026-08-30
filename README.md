<div align="center">

![VAJRA Banner](assets/banner.svg)

<br>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.4.0-f0883e?style=for-the-badge)](https://github.com/gauravjethva-lab/vajra-web-enumeration/releases)
[![Pipeline](https://img.shields.io/badge/Pipeline-9%20Stages-a855f7?style=for-the-badge)](#pipeline)
[![Stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge&color=f0883e)](https://github.com/gauravjethva-lab/vajra-web-enumeration/stargazers)

<br>

> **Full auto-pipeline Web Enumeration & Attack Surface Reconnaissance Framework**
> Built for Kali Linux — 9 stages, parallel execution, professional HTML report with author credit.

<br>

[Quick Start](#-quick-start) · [Pipeline](#-pipeline) · [Report](#-html-report) · [Changelog](#-changelog) · [Legal](#-legal-disclaimer)

</div>

---

## 👤 Author

<table>
<tr>
<td><strong>Name</strong></td><td>Gaurav Jethva</td>
</tr>
<tr>
<td><strong>GitHub</strong></td><td><a href="https://github.com/gauravjethva-lab">@gauravjethva-lab</a></td>
</tr>
<tr>
<td><strong>Tool</strong></td><td><a href="https://github.com/gauravjethva-lab/vajra-web-enumeration">VAJRA Web Enumeration</a></td>
</tr>
</table>

---

## 🔱 What is VAJRA?

**VAJRA** is a **9-stage automated web enumeration and attack surface reconnaissance framework** built for Kali Linux. It chains together the best open-source security tools into a single parallel-execution pipeline — from WHOIS all the way to subdomain takeover detection and smart screenshots — then auto-generates a **professional dark-theme HTML report** and **Markdown summary** with full scan coverage metrics.

**VAJRA is an Attack Surface Mapper — not a vulnerability scanner.**
Every report clearly distinguishes between raw reconnaissance observations and confirmed security issues.

---

## ✨ Features

| Category | Feature |
|----------|---------|
| 🌍 **Passive Recon** | WHOIS lookup with Python fallback |
| 🔎 **DNS Recon** | A, AAAA, MX, NS, TXT, CNAME, SOA via `dig` + socket fallback |
| 🔍 **Subdomain Enum** | `subfinder` + `amass` running in parallel threads |
| 🌐 **Live Detection** | `httpx` — 150 threads, 8s balanced timeout |
| 🗺️ **Endpoints** | `katana` + `gau` + `waybackurls` in parallel — with URL classification |
| 🎯 **URL Classification** | Auto-sorts into In-Scope / API / Third-Party |
| 🔌 **Port Scanning** | `masscan` + `naabu` in parallel — raw observations |
| ✅ **Service Validation** | `nmap -sV` confirms actual services on found ports |
| 🧠 **Tech Fingerprint** | `whatweb` technology detection |
| 🔗 **Takeover Check** | 25 service fingerprints — parallel with 20 workers |
| 📸 **Smart Screenshots** | Verifies alive URLs (30 threads) before screenshotting |
| 📊 **HTML Report** | Professional dark-theme report with tabs, search, coverage table |
| 📋 **MD Summary** | Clean Markdown summary auto-generated after scan |
| 🔧 **Self-Healing** | Auto-installs every missing tool on first run |
| ⚡ **Parallel Execution** | Every stage optimized for maximum speed |

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
[1/9]  🌍 WHOIS Recon          →  whois.txt
[2/9]  🔎 DNS Recon            →  dns_records.txt
[3/9]  🔍 Subdomain Enum       →  final_subdomains.txt
[4/9]  🌐 Live Host Detection  →  live_subdomains.txt
[5/9]  🗺️  Endpoint Collection  →  all_endpoints.txt
                                   inscope_endpoints.txt
                                   api_endpoints.txt
                                   third_party_urls.txt
[6/9]  🔌 Port Scanning        →  open_ports.txt
       ✅ Service Validation   →  validated_services.txt
[7/9]  🧠 Tech Fingerprinting  →  technologies.txt
[8/9]  🔗 Takeover Check       →  takeover_results.txt
[9/9]  📸 Screenshots          →  screenshots/
        ✨ Auto HTML Report    →  vajra_report.html
        ✨ Auto MD Summary     →  recon_summary.md
```

| # | Stage | Tools | Output |
|---|-------|-------|--------|
| 1 | 🌍 WHOIS | `whois` + Python socket | `whois.txt` |
| 2 | 🔎 DNS | `dig` + Python socket | `dns_records.txt` |
| 3 | 🔍 Subdomains | `subfinder`, `amass` (parallel) | `final_subdomains.txt` |
| 4 | 🌐 Live Hosts | `httpx` 150 threads | `live_subdomains.txt` |
| 5 | 🗺️ Endpoints | `katana`, `gau`, `waybackurls` (parallel) | `all_endpoints.txt` + classified |
| 6 | 🔌 Ports + ✅ Services | `masscan`, `naabu` (parallel) + `nmap -sV` | `open_ports.txt` + `validated_services.txt` |
| 7 | 🧠 Tech | `whatweb` | `technologies.txt` |
| 8 | 🔗 Takeover | Python (25 fingerprints, 20 workers) | `takeover_results.txt` |
| 9 | 📸 Screenshots | `gowitness` v2/v3 | `screenshots/` |

---

## 📊 HTML Report

<div id="report"></div>

After every scan, VAJRA **automatically generates** a professional dark-theme HTML report. Open in any browser:

```bash
firefox output/example.com/vajra_report.html
```

### Report Sections

| Section | Content |
|---------|---------|
| 📋 Executive Summary | Target, date, author, scan type, confidence level |
| ⚠️ Confidence Note | Clearly states this is recon, not a pentest |
| 📊 Stats Dashboard | 10 key metrics at a glance |
| 🚨 Alerts | Only confirmed findings highlighted |
| 🌍 WHOIS | Registrar, dates, nameservers |
| 🔎 DNS | All record types |
| 🔍 Subdomains | Searchable table |
| 🌐 Live Hosts | Status codes + page titles |
| 🗺️ Endpoints | **Tabbed view** — In-Scope / API / All URLs |
| 🔌 Ports | **Tabbed view** — Validated Services / Raw Observations |
| 🧠 Technologies | Fingerprinted hosts |
| 🔗 Takeover | Vulnerable subdomains highlighted in red |
| 📸 Screenshots | Inline embedded images |
| 📊 Scan Coverage | Full coverage metrics table |
| 👤 Footer | Author credit on every report |

---

## 📁 Project Structure

```
vajra/
├── main.py                   # 9-stage pipeline entry point
├── install.sh                # One-click dependency installer
├── requirements.txt          # Python dependencies
├── report_generator.py       # Professional HTML report generator
├── recon_summary.py          # Markdown summary generator
├── modules/
│   ├── whois_recon.py        # WHOIS + Python fallback
│   ├── dns_recon.py          # dig + socket fallback
│   ├── subdomains.py         # Subfinder + Amass (parallel)
│   ├── live_check.py         # httpx — 150 threads, 8s timeout
│   ├── endpoints.py          # Katana + GAU + Wayback (parallel) + URL classification
│   ├── ports.py              # Masscan + Naabu (parallel) + nmap validation
│   ├── tech_detect.py        # WhatWeb fingerprinting
│   ├── takeover_check.py     # 25 service fingerprints, 20 workers
│   └── screenshot.py         # Alive verification (30 threads) + gowitness v2/v3
└── core/
    ├── banner.py             # Rich terminal UI
    ├── utils.py              # Tool path resolver
    └── setup_check.py        # Auto dependency installer
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` required for `masscan`

### Auto-Installed Tools
`subfinder` · `amass` · `httpx` · `naabu` · `masscan` · `whatweb` · `katana` · `gau` · `waybackurls` · `gowitness`

### Python Dependencies
```
rich >= 13.0.0
pyfiglet >= 1.0.0
```

---

## 🛠️ Changelog

<details>
<summary><strong>v1.4.0 — Professional Report + Speed Optimizations</strong></summary>

| Change | Detail |
|--------|--------|
| 🎯 URL Classification | Auto-sorts into In-Scope / API / Third-Party |
| ✅ Service Validation | `nmap -sV` confirms actual services on found ports |
| 📊 Coverage Table | Every report shows full scan coverage metrics |
| ⚠️ Confidence Level | Medium/Low confidence clearly stated in every report |
| 📋 Report Disclaimer | Clearly distinguishes recon from pentest |
| 🗂️ Tabbed Report | Endpoints and Ports have tabbed views |
| ⚡ Parallel Endpoints | Katana + GAU + Wayback run simultaneously |
| ⚡ Parallel Ports | Masscan + Naabu run simultaneously |
| ⚡ httpx 150 threads | Balanced speed with 8s timeout |
| ⚡ Takeover 20 workers | Parallel subdomain takeover checking |
| ⚡ Screenshot 30 threads | Parallel alive URL verification |

</details>

<details>
<summary><strong>v1.3.0 — Takeover + Screenshots</strong></summary>

- Subdomain takeover check (25 service fingerprints)
- Smart screenshots — alive-verified, supports gowitness v2/v3
- WHOIS and DNS modules added

</details>

<details>
<summary><strong>v1.2.0 — Stability</strong></summary>

- Auto HTML + Markdown reports after every scan
- gau timeout fixed, ports empty-host crash fixed
- whatweb flag syntax fixed

</details>

<details>
<summary><strong>v1.0.0 — Initial Release</strong></summary>

- 5-stage pipeline with self-healing installer

</details>

---

## ⚠️ Legal Disclaimer

> **VAJRA is designed for authorized security testing only.**
>
> Only use VAJRA against domains and systems you **own** or have **explicit written permission** to test. Unauthorized use against systems you do not have permission to test is **illegal** and **unethical**.
>
> The author is not responsible for any misuse or damage caused by this tool.
>
> VAJRA generates **reconnaissance reports** — not penetration test reports. All findings require authorized human validation before being classified as security vulnerabilities.

---

<div align="center">

**⚡ Built for the security community — Use responsibly ⚡**

*If VAJRA helps your work, give it a ⭐ on GitHub!*

<br>

[![GitHub](https://img.shields.io/badge/GitHub-gauravjethva--lab-f0883e?style=for-the-badge&logo=github)](https://github.com/gauravjethva-lab)

</div>
