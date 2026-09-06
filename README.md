<div align="center">

![VAJRA Banner](assets/banner.svg)

<br>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-f0883e?style=for-the-badge)](https://github.com/gauravjethva-lab/vajra-web-enumeration/releases)
[![Pipeline](https://img.shields.io/badge/Pipeline-14%20Stages-a855f7?style=for-the-badge)](#pipeline)
[![Tests](https://img.shields.io/badge/Tests-16%2F16%20Passing-22c55e?style=for-the-badge)](#)
[![Stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge&color=f0883e)](https://github.com/gauravjethva-lab/vajra-web-enumeration/stargazers)

<br>

> **Full auto-pipeline Web Enumeration & Attack Surface Reconnaissance Framework**
> 14 stages · Parallel execution · Resume & Cache · Professional HTML report

<br>

[Quick Start](#-quick-start) · [Pipeline](#-pipeline) · [Features](#-features) · [Report](#-html-report) · [Changelog](#-changelog) · [Legal](#-legal-disclaimer)

</div>

---

## 👤 Author

| Field | Info |
|-------|------|
| **Name** | Gaurav Jethva |
| **GitHub** | [@gauravjethva-lab](https://github.com/gauravjethva-lab) |
| **Tool** | [VAJRA Web Enumeration Framework](https://github.com/gauravjethva-lab/vajra-web-enumeration) |

---

## 🔱 What is VAJRA?

**VAJRA** is a **14-stage automated web enumeration and attack surface reconnaissance framework** built for Kali Linux.

It chains together the best open-source security tools into a **single parallel-execution pipeline** — from WHOIS all the way to Nuclei vulnerability scanning and smart screenshots — then **auto-generates a professional HTML report** and Markdown summary with full scan coverage metrics.

Key design principles:
- **Resume** — scan interrupted? Run again, pick up where you stopped
- **Cache** — same domain rescanned? Unchanged stages skip instantly
- **Smart Scope** — auto-classifies subdomains as High / Medium / Low priority
- **Parallel** — every slow stage runs multiple tools simultaneously
- **100% working** — 16/16 automated tests pass before every release

> VAJRA is an **Attack Surface Mapper**, not a vulnerability scanner.
> Every report clearly separates raw reconnaissance from confirmed findings.

---

## ✨ Features

### Speed & Performance
| Feature | Detail |
|---------|--------|
| ⚡ **Parallel Execution** | Subfinder+Amass, Katana+GAU+Wayback, Masscan+Naabu — all run simultaneously |
| 💾 **Cache System** | Results cached per domain+stage — rescan is instant for unchanged data |
| 🔄 **Resume Scan** | Ctrl+C mid-scan? Run again — VAJRA resumes from last completed stage |
| 🎯 **Smart Scope** | Auto-classifies subdomains: High (admin/api/dev) · Medium · Low (cdn/static) |

### Detection & Coverage
| Feature | Detail |
|---------|--------|
| 🌍 **WHOIS Recon** | Registrar, dates, nameservers — Python fallback if whois missing |
| 🔎 **DNS Recon** | A, AAAA, MX, NS, TXT, CNAME, SOA — Python socket fallback if dig missing |
| 🔍 **Subdomain Enum** | `subfinder` + `amass` in parallel threads |
| 🌐 **Live Detection** | `httpx` — 150 threads, 8s balanced timeout |
| 🔐 **SSL/TLS Analysis** | Cert expiry, weak ciphers, TLS version — pure Python, no extra tools |
| 🗺️ **Endpoints** | `katana` + `gau` + `waybackurls` parallel — auto-classified: In-Scope / API / Third-Party |
| 📧 **Email Recon** | Finds emails in endpoints + WHOIS, generates common patterns, breach check link |
| 🕵️ **Google Dorks** | 20 targeted dork queries auto-generated — clickable HTML file |
| 🔌 **Port Scanning** | `masscan` + `naabu` parallel — raw observations |
| ✅ **Service Validation** | `nmap -sV` confirms actual services on found ports |
| 🧠 **Tech Fingerprint** | `whatweb` technology detection |
| 🔴 **Nuclei Scan** | 1000+ vulnerability templates — CVEs, misconfigs, exposures |
| 🔗 **Takeover Check** | 25 service fingerprints — 20 parallel workers |
| 📸 **Smart Screenshots** | Alive-verified (30 threads), gowitness v2+v3 support |

### Reporting
| Feature | Detail |
|---------|--------|
| 📊 **HTML Report** | Dark-theme, tabbed sections, searchable tables, scan coverage, author credit |
| 📋 **Markdown Summary** | Clean `.md` summary auto-generated after every scan |
| 🗂️ **URL Classification** | In-Scope / API endpoints / Third-Party automatically separated |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/gauravjethva-lab/vajra-web-enumeration.git
cd vajra-web-enumeration/vajra

# Install all dependencies
bash install.sh

# Run
python3 main.py
```

> First run auto-installs all missing tools. Every run after that is fast.
> If a scan is interrupted — just run `python3 main.py` again with the same domain to resume.

---

## 📊 Pipeline

<div id="pipeline"></div>

```
[01/14] 🌍  WHOIS Reconnaissance
[02/14] 🔎  DNS Reconnaissance
[03/14] 🔍  Subdomain Enumeration      ← parallel: subfinder + amass
[04/14] 🎯  Smart Scope Analysis
[05/14] 🌐  Live Host Detection         ← 150 threads
[06/14] 🔐  SSL/TLS Analysis           ← 20 parallel workers
[07/14] 🗺️   Endpoint Collection        ← parallel: katana + gau + waybackurls
[08/14] 📧  Email & Breach Recon
[09/14] 🕵️   Google Dork Generation
[10/14] 🔌  Port Scanning & Validation  ← parallel: masscan + naabu + nmap
[11/14] 🧠  Technology Fingerprinting
[12/14] 🔴  Nuclei Vulnerability Scan   ← 25 parallel workers
[13/14] 🔗  Subdomain Takeover Check   ← 20 parallel workers
[14/14] 📸  Screenshots                 ← 30 thread alive-verify + gowitness
       ✨   Auto HTML Report            → vajra_report.html
       ✨   Auto Markdown Summary       → recon_summary.md
```

| # | Stage | Tools | Output File |
|---|-------|-------|------------|
| 1 | 🌍 WHOIS | `whois` + Python socket | `whois.txt` |
| 2 | 🔎 DNS | `dig` + Python socket | `dns_records.txt` |
| 3 | 🔍 Subdomains | `subfinder`, `amass` | `final_subdomains.txt` |
| 4 | 🎯 Smart Scope | Python classifier | `scope_high/medium/low.txt` |
| 5 | 🌐 Live Hosts | `httpx` 150 threads | `live_subdomains.txt` |
| 6 | 🔐 SSL/TLS | Python ssl module | `ssl_analysis.txt` |
| 7 | 🗺️ Endpoints | `katana`, `gau`, `waybackurls` | `all_endpoints.txt` + classified |
| 8 | 📧 Email Recon | Python + WHOIS parse | `email_recon.txt` |
| 9 | 🕵️ Dorks | Python generator | `google_dorks.txt` + `.html` |
| 10 | 🔌 Ports + ✅ Services | `masscan`, `naabu` + `nmap -sV` | `open_ports.txt` + `validated_services.txt` |
| 11 | 🧠 Tech | `whatweb` | `technologies.txt` |
| 12 | 🔴 Nuclei | `nuclei` templates | `nuclei_findings.txt` |
| 13 | 🔗 Takeover | Python 25 fingerprints | `takeover_results.txt` |
| 14 | 📸 Screenshots | `gowitness` v2/v3 | `screenshots/` |

---

## 📊 HTML Report

<div id="report"></div>

Auto-generated after every scan. Open in any browser:

```bash
firefox output/example.com/vajra_report.html
```

| Section | Content |
|---------|---------|
| 📋 Executive Summary | Target, date, author, scan type, confidence level |
| ⚠️ Confidence Note | Clearly states recon vs pentest distinction |
| 📊 Stats Dashboard | 10 key metrics at a glance |
| 🚨 Alerts | Only confirmed findings highlighted in red |
| 🌍 WHOIS | Registrar, creation/expiry dates |
| 🔎 DNS Records | All record types |
| 🔍 Subdomains | Searchable table |
| 🌐 Live Hosts | Status codes + titles |
| 🗺️ Endpoints | **Tabbed**: In-Scope / API / All URLs |
| 🔌 Ports | **Tabbed**: Validated Services / Raw Observations |
| 🧠 Technologies | Fingerprinted hosts |
| 🔗 Takeover | Vulnerable subdomains in red |
| 📸 Screenshots | Inline embedded images |
| 📊 Scan Coverage | Full metrics — what was tested |
| 👤 Footer | Author credit on every report |

---

## 📁 Project Structure

```
vajra/
├── main.py                    # 14-stage pipeline + resume + cache
├── install.sh                 # One-click dependency installer
├── requirements.txt           # Python dependencies
├── report_generator.py        # Professional HTML report
├── recon_summary.py           # Markdown summary
├── core/
│   ├── banner.py              # Rich UI + domain sanitization
│   ├── cache.py               # Cache system (~/.vajra_cache)
│   ├── resume.py              # Resume system (~/.vajra_resume)
│   ├── utils.py               # Tool path resolver
│   └── setup_check.py         # Auto dependency installer
└── modules/
    ├── whois_recon.py          # WHOIS + Python fallback
    ├── dns_recon.py            # dig + socket fallback
    ├── subdomains.py           # Subfinder + Amass parallel
    ├── smart_scope.py          # High/Medium/Low classifier
    ├── live_check.py           # httpx 150 threads
    ├── ssl_analysis.py         # SSL/TLS pure Python
    ├── endpoints.py            # Parallel + URL classification
    ├── email_recon.py          # Email patterns + breach link
    ├── google_dork.py          # 20 dork queries + HTML
    ├── ports.py                # Masscan+Naabu parallel + nmap
    ├── tech_detect.py          # WhatWeb
    ├── nuclei_scan.py          # Nuclei templates
    ├── takeover_check.py       # 25 fingerprints, 20 workers
    └── screenshot.py           # 30-thread verify + gowitness
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` required for `masscan`

### Auto-Installed Tools
`subfinder` · `amass` · `httpx` · `naabu` · `masscan` · `whatweb` · `katana` · `gau` · `waybackurls` · `nuclei` · `gowitness`

### Python Dependencies
```
rich >= 13.0.0
pyfiglet >= 1.0.0
```

---

## 🛠️ Changelog

<details open>
<summary><strong>v2.0.0 — Full Recon Suite (Current)</strong></summary>

| Change | Detail |
|--------|--------|
| 💾 Cache System | Results cached — rescan skips unchanged stages instantly |
| 🔄 Resume Scan | Ctrl+C and resume from exact stage — no data lost |
| 🎯 Smart Scope | Auto High/Medium/Low priority classification |
| 🔐 SSL/TLS | Cert expiry, weak ciphers, TLS version — pure Python |
| 📧 Email Recon | Email patterns from endpoints + WHOIS + breach link |
| 🕵️ Google Dorks | 20 targeted queries + clickable HTML file |
| 🔴 Nuclei | 1000+ CVE/misconfiguration templates |
| ⚡ Parallel | Every slow stage now runs simultaneously |
| 🐛 Port stripping | `sub.example.com:8080` → `sub.example.com` fixed |
| ✅ 16 tests | Automated test suite passes before every release |

</details>

<details>
<summary><strong>v1.4.0 — Professional Report + Speed</strong></summary>

- URL classification: In-Scope / API / Third-Party
- Service validation with nmap -sV
- Tabbed HTML report sections
- Coverage table in every report

</details>

<details>
<summary><strong>v1.3.0 — Takeover + Screenshots</strong></summary>

- Subdomain takeover check (25 fingerprints)
- Smart screenshots with alive verification
- gowitness v2 + v3 support

</details>

<details>
<summary><strong>v1.0.0 — Initial Release</strong></summary>

- 5-stage pipeline, self-healing installer

</details>

---

## ⚠️ Legal Disclaimer

> **VAJRA is designed for authorized security testing only.**
>
> Only use VAJRA against domains you **own** or have **explicit written permission** to test.
> Unauthorized use is **illegal** and **unethical**.
>
> VAJRA generates **attack surface reconnaissance reports** — not penetration test reports.
> All findings require authorized human validation.

---

<div align="center">

**⚡ Built for the security community — Use responsibly ⚡**

*If VAJRA helps your work, give it a ⭐*

<br>

[![GitHub](https://img.shields.io/badge/GitHub-gauravjethva--lab-f0883e?style=for-the-badge&logo=github)](https://github.com/gauravjethva-lab)

</div>
