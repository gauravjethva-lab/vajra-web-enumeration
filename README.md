<div align="center">

![VAJRA Banner](assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.3.0-orange?style=for-the-badge)
![Stages](https://img.shields.io/badge/Pipeline-9%20Stages-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge)

</div>

---

## 🔱 What is VAJRA?

**VAJRA** is a full auto-pipeline web enumeration & reconnaissance framework built for **Kali Linux**. It chains 9 stages of recon — from WHOIS all the way to subdomain takeover checks and screenshots — into a **single automated workflow**, then auto-generates a **professional HTML + Markdown report** with your name on it.

> Run one command. VAJRA scans everything. Reports everything.

---

## 👤 Author

**Gaurav Jethva**
- GitHub: [@gauravjethva-lab](https://github.com/gauravjethva-lab)
- Tool: [VAJRA Web Enumeration](https://github.com/gauravjethva-lab/vajra-web-enumeration)

---

## ✨ Features

- 🌍 **WHOIS Recon** — Registrar, creation/expiry date, nameservers
- 🔎 **DNS Recon** — A, AAAA, MX, NS, TXT, CNAME, SOA records via `dig`
- 🔍 **Subdomain Enumeration** — `subfinder` + `amass` in parallel threads
- 🌐 **Live Host Detection** — `httpx` with timeout protection
- 🗺️ **Endpoint Collection** — `katana` + `gau` + `waybackurls` with static file filtering
- 🔌 **Port Scanning** — `masscan` + `naabu` with graceful error handling
- 🧠 **Technology Fingerprinting** — `whatweb`
- 🔗 **Subdomain Takeover Check** — 25 services (GitHub Pages, Heroku, AWS S3, Azure, Fastly, Zendesk, and more)
- 📸 **Smart Screenshots** — screenshots of live subdomains + directories, only genuinely alive URLs
- 📊 **Auto HTML Report** — professional dark-theme report with author name, auto-generated after scan
- 📋 **Auto Markdown Summary** — clean `.md` summary auto-generated after scan
- 🔧 **Self-Healing Install** — auto-installs every missing tool on first run
- 🩹 **Smart Domain Sanitization** — handles full URLs like `https://example.com/path`

---

## 🖥️ Terminal Preview

```
 ─────────────────────────────────────────────────────
  Stage [1/9] : WHOIS Reconnaissance
 ─────────────────────────────────────────────────────
    Registrar: GoDaddy.com LLC
    Creation Date: 2010-04-14
    Name Server: NS1.EXAMPLE.COM
 [+] WHOIS entries found: 5

 Stage [2/9] : DNS Reconnaissance
 ─────────────────────────────────────────────────────
    [A]   93.184.216.34
    [MX]  mail.example.com
    [NS]  ns1.example.com
    [TXT] v=spf1 include:_spf.google.com ~all
 [+] DNS Records Found: 8

 Stage [3/9] : Subdomain Enumeration
 ─────────────────────────────────────────────────────
 [+] Running Subfinder...
 [+] Running Amass...
 [+] Total Unique Subdomains: 47

 Stage [4/9] : Live Host Detection
 ─────────────────────────────────────────────────────
 [+] Live hosts saved → live_subdomains.txt

 Stage [5/9] : Endpoint Collection
 ─────────────────────────────────────────────────────
 [+] Raw URLs collected : 8420
 [+] After filtering    : 1342 (static files removed)

 Stage [6/9] : Port Scanning
 ─────────────────────────────────────────────────────
 [+] Open ports saved → open_ports.txt

 Stage [7/9] : Technology Fingerprinting
 ─────────────────────────────────────────────────────
 [+] Technology results saved → technologies.txt

 Stage [8/9] : Subdomain Takeover Check
 ─────────────────────────────────────────────────────
 [*] Checking 47 subdomains for takeover...
 [VULNERABLE] old.example.com → CNAME: example.github.io (github.io)
 [✓] No further takeover vulnerabilities found.

 Stage [9/9] : Screenshots (Live + Dirs)
 ─────────────────────────────────────────────────────
 [+] Live subdomains : 23 URLs
 [+] Directories     : 12 URLs
 [+] Verifying genuinely alive URLs...
 [✓] Genuinely alive: 31 / 35 URLs
 [✓] Screenshots Captured: 31

 [+] VAJRA Recon Pipeline Completed!
 [*] Generating HTML Report...
 ✅ Report saved: output/example.com/vajra_report.html
 [*] Generating Markdown Summary...
 [+] Markdown summary saved: output/example.com/recon_summary.md
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

## 📊 Full Pipeline — 9 Stages

| # | Stage | Tool(s) | Output File |
|---|-------|---------|-------------|
| 1 | 🌍 WHOIS Recon | `whois` + Python socket | `whois.txt` |
| 2 | 🔎 DNS Recon | `dig` + Python socket | `dns_records.txt` |
| 3 | 🔍 Subdomains | `subfinder`, `amass` (parallel) | `final_subdomains.txt` |
| 4 | 🌐 Live Hosts | `httpx` | `live_subdomains.txt` |
| 5 | 🗺️ Endpoints | `katana`, `gau`, `waybackurls` + filter | `all_endpoints.txt` |
| 6 | 🔌 Port Scan | `masscan`, `naabu` | `open_ports.txt` |
| 7 | 🧠 Tech Detect | `whatweb` | `technologies.txt` |
| 8 | 🔗 Takeover Check | Python (25 service fingerprints) | `takeover_results.txt` |
| 9 | 📸 Screenshots | `gowitness` (live + dirs verified) | `screenshots/` |
| ✨ | 📊 HTML Report (auto) | `report_generator.py` | `vajra_report.html` |
| ✨ | 📋 MD Summary (auto) | `recon_summary.py` | `recon_summary.md` |

---

## 📊 HTML Report

After every scan, VAJRA **automatically generates** a professional dark-theme HTML report. Open it in any browser:

```bash
firefox output/example.com/vajra_report.html
```

**Report includes:**
- 👤 **Author credit** — Gaurav Jethva on every report
- 📈 Stats dashboard — all findings at a glance
- 🚨 Security alerts — takeover vulnerabilities highlighted in red
- 🔍 Searchable tables for subdomains, endpoints, directories
- 🌍 WHOIS + DNS records
- 🔗 Takeover results, 🔌 Open ports, 🧠 Technologies
- 📸 Embedded screenshots (inline in report)
- 🗂️ Sidebar navigation

---

## 📁 Project Structure

```
vajra/
├── main.py                    # 9-stage pipeline + auto reports
├── install.sh                 # One-click dependency installer
├── requirements.txt           # Python deps (rich, pyfiglet)
├── report_generator.py        # Auto HTML report (with author name)
├── recon_summary.py           # Auto Markdown summary
├── modules/
│   ├── whois_recon.py         # WHOIS + IP/hostname fallback
│   ├── dns_recon.py           # dig + Python socket fallback
│   ├── subdomains.py          # Subfinder + Amass (parallel)
│   ├── live_check.py          # httpx with timeout
│   ├── endpoints.py           # Katana + GAU + Wayback + filter
│   ├── ports.py               # Masscan + Naabu
│   ├── tech_detect.py         # WhatWeb
│   ├── takeover_check.py      # 25-service takeover fingerprints
│   └── screenshot.py          # Alive-verified screenshots
└── core/
    ├── banner.py              # Rich UI + ASCII banner
    ├── utils.py               # Tool path resolver
    └── setup_check.py         # Auto dependency installer
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` access (required for `masscan`)

### External Tools (Auto-installed)
`subfinder` • `amass` • `httpx` • `naabu` • `masscan` • `whatweb` • `katana` • `gau` • `waybackurls` • `gowitness`

---

## 🛠️ Changelog

### v1.3.0 — Full Recon Release
| Addition | Description |
|----------|-------------|
| 🔗 Takeover Check | 25 service fingerprints — GitHub, Heroku, S3, Azure, Fastly, Zendesk + more |
| 📸 Smart Screenshots | Live subdomains + directories, genuinely alive URLs only |
| 🌍 WHOIS Module | whois command + Python IP fallback |
| 🔎 DNS Module | dig + Python socket fallback |
| 🩹 Endpoint Filter | Static files (.png .css .woff etc.) removed |
| 📋 Markdown Summary | Auto-generated after every scan |
| 👤 Author Credit | Gaurav Jethva on every HTML report |

### v1.2.0 — Stability Release
| Fix | Description |
|-----|-------------|
| 📊 Auto HTML Report | Auto-generated after scan |
| 🗺️ Endpoints | gau timeout fixed |
| 🔌 Ports | Empty host crash fixed |
| 🧠 Tech | whatweb flag fixed |

### v1.0.0 — Initial Release
- 5-stage pipeline, self-healing installer

---

## ⚠️ Legal Disclaimer

> **VAJRA is for authorized security testing only.**
> Only use on systems you own or have explicit written permission to test.
> The author is not responsible for any misuse.

---

<div align="center">

**⚡ Built for the security community. Use responsibly. ⚡**

*If VAJRA helps you, give it a ⭐ on GitHub!*

</div>
