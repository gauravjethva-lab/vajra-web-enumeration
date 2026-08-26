<div align="center">

![VAJRA Banner](assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Stages](https://img.shields.io/badge/Stages-12-purple?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/gauravjethva-lab/vajra-web-enumeration?style=for-the-badge)

</div>

---

## 🔱 What is VAJRA?

**VAJRA** is a full auto-pipeline web enumeration & reconnaissance framework built for **Kali Linux**. It chains together the best open-source security tools into a **12-stage automated workflow** — from passive recon all the way to screenshots and secret detection — with **self-healing dependency installation**.

> Run one command. VAJRA does the rest.

---

## ✨ Features

- 🌍 **Passive Recon** — WHOIS, ASN lookup, IP resolution, Reverse DNS
- 🔎 **DNS Reconnaissance** — A, MX, TXT, NS, CNAME, SOA records via `dnsx` + `dig`
- 🔍 **Subdomain Enumeration** — `subfinder` + `amass` running in **parallel threads**
- 🌐 **Live Host Detection** — `httpx` with status codes + page titles
- 🛡️ **WAF Detection** — fingerprint Web Application Firewalls via `wafw00f`
- 🗺️ **Endpoint Collection** — `katana` + `gau` + `waybackurls` running in **parallel** with smart deduplication
- 📜 **JS File Analysis** — scan JS files for API keys, tokens, secrets, and hidden endpoints
- ⚡ **CORS Check** — detect CORS misconfigurations (wildcard, credential leak)
- 🔌 **Port Scanning** — `masscan` (rate 5000) + `naabu` (top 1000), results merged
- 🧠 **Technology Fingerprinting** — via `whatweb`
- 📂 **Directory Bruteforce** — `ffuf` with seclists wordlist on top hosts
- 📸 **Screenshots** — auto-capture screenshots of all live hosts via `gowitness`
- 🔧 **Self-Healing Install** — auto-installs every missing tool on first run
- 📊 **HTML Report Generator** — dark-themed professional scan report
- 📋 **Markdown Summary** — clean recon summary per domain
- ⏱️ **Per-stage Timing** — see how long each of the 12 stages takes

---

## 🖥️ Terminal Preview

```
 ──────────────────────────────────────────────────────
  Stage [1/12] : Passive Recon (WHOIS/ASN/IP)
 ──────────────────────────────────────────────────────
 [+] Running WHOIS, ASN, Reverse DNS...
 [✓] Passive Recon Complete

  Stage [2/12] : DNS Reconnaissance
 ──────────────────────────────────────────────────────
 [+] Running dnsx + dig (A, MX, TXT, NS, CNAME)...
 [✓] DNS Records Found: 34

  Stage [3/12] : Subdomain Enumeration
 ──────────────────────────────────────────────────────
 [+] Running Subfinder... (parallel)
 [+] Running Amass...    (parallel)
 [✓] Total Unique Subdomains: 58

  Stage [4/12] : Live Host Detection
 ──────────────────────────────────────────────────────
 [+] Running httpx (status + titles)...
 [✓] Live Hosts Found: 24

  Stage [5/12] : WAF Detection
 ──────────────────────────────────────────────────────
 [+] Running wafw00f...
 [✓] WAF Detection: 3 WAFs found across 24 hosts

  Stage [6/12] : Endpoint Collection
 ──────────────────────────────────────────────────────
 [+] Running Katana...      (parallel)
 [+] Running GAU...         (parallel)
 [+] Running Waybackurls... (parallel)
 [✓] Unique Useful Endpoints: 1342

  Stage [7/12] : JS File Analysis
 ──────────────────────────────────────────────────────
 [+] Analyzing 50 JS files for secrets...
 [!] JS Findings: 4 potential secrets/endpoints found!

  Stage [8/12] : CORS Misconfiguration Check
 ──────────────────────────────────────────────────────
 [+] Testing 24 hosts for CORS issues...
 [!] CORS Issues Found: 2!

  Stage [9/12] : Port Scanning
 ──────────────────────────────────────────────────────
 [+] Running Naabu (top 1000 ports)...
 [+] Running Masscan (rate 5000)...
 [✓] Open Ports Found: 38

  Stage [10/12] : Technology Fingerprinting
 ──────────────────────────────────────────────────────
 [+] Running WhatWeb...
 [✓] 24 hosts fingerprinted

  Stage [11/12] : Directory Bruteforce
 ──────────────────────────────────────────────────────
 [+] Running ffuf on top 5 hosts...
 [✓] Directories Found: 127

  Stage [12/12] : Screenshots
 ──────────────────────────────────────────────────────
 [+] Taking screenshots via gowitness...
 [✓] Screenshots Captured: 24

 +------------------------------------+--------+---------+
 | Stage                              | Status |    Time |
 +------------------------------------+--------+---------+
 | Passive Recon (WHOIS/ASN/IP)       |   Done |   8.2s  |
 | DNS Reconnaissance                 |   Done |  12.4s  |
 | Subdomain Enumeration              |   Done |  45.2s  |
 | Live Host Detection                |   Done |  12.1s  |
 | WAF Detection                      |   Done |  18.3s  |
 | Endpoint Collection                |   Done |  55.4s  |
 | JS File Analysis                   |   Done |  22.1s  |
 | CORS Check                         |   Done |   9.8s  |
 | Port Scanning                      |   Done |  33.7s  |
 | Technology Fingerprinting          |   Done |  18.9s  |
 | Directory Bruteforce               |   Done |  95.0s  |
 | Screenshots                        |   Done |  42.5s  |
 +------------------------------------+--------+---------+
 Total Time: 373s (6.2 min)
 Results saved in: output/example.com/
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

## 📊 Full Pipeline — 12 Stages

| # | Stage | Tool(s) | Output File |
|---|-------|---------|-------------|
| 1 | 🌍 Passive Recon | `whois`, `dig`, socket | `passive_recon.txt` |
| 2 | 🔎 DNS Recon | `dnsx`, `dig` | `dns_records.txt` |
| 3 | 🔍 Subdomains | `subfinder`, `amass` | `final_subdomains.txt` |
| 4 | 🌐 Live Hosts | `httpx` (status + title) | `live_subdomains.txt` |
| 5 | 🛡️ WAF Detection | `wafw00f` | `waf_results.txt` |
| 6 | 🗺️ Endpoints | `katana`, `gau`, `waybackurls` | `all_endpoints.txt` |
| 7 | 📜 JS Analysis | Python urllib | `js_findings.txt` |
| 8 | ⚡ CORS Check | Python urllib | `cors_issues.txt` |
| 9 | 🔌 Port Scan | `masscan` (rate 5000), `naabu` | `open_ports.txt` |
| 10 | 🧠 Tech Detect | `whatweb` | `technologies.txt` |
| 11 | 📂 Dir Bruteforce | `ffuf` + seclists | `directories.txt` |
| 12 | 📸 Screenshots | `gowitness` | `screenshots/` |

---

## 📁 Project Structure

```
vajra/
├── main.py                    # 12-stage pipeline entry point
├── install.sh                 # One-click dependency installer
├── requirements.txt           # Python deps (rich, pyfiglet)
├── report_generator.py        # HTML scan report
├── recon_summary.py           # Markdown summary
├── modules/
│   ├── passive_recon.py       # WHOIS, ASN, IP, Reverse DNS
│   ├── dns_recon.py           # DNS records via dnsx + dig
│   ├── subdomains.py          # Subfinder + Amass (parallel)
│   ├── live_check.py          # httpx with timeout
│   ├── waf_detect.py          # WAF fingerprinting
│   ├── endpoints.py           # Katana + GAU + Wayback (parallel)
│   ├── js_analysis.py         # JS secret/endpoint scanner
│   ├── cors_check.py          # CORS misconfiguration checker
│   ├── ports.py               # Masscan (rate 5000) + Naabu
│   ├── tech_detect.py         # WhatWeb fingerprinter
│   ├── dir_bruteforce.py      # ffuf directory bruteforce
│   └── screenshot.py          # gowitness screenshots
└── core/
    ├── banner.py              # Rich UI + ASCII banner
    ├── utils.py               # Tool path resolver
    └── setup_check.py         # Auto dependency installer
```

---

## 📈 Generate Reports

```bash
# HTML Report (dark themed, open in browser)
python3 report_generator.py example.com

# Markdown Summary
python3 recon_summary.py example.com
```

---

## ⚙️ Requirements

- **OS:** Kali Linux (recommended) / Debian-based Linux
- **Python:** 3.8+
- **Permissions:** `sudo` access (required for `masscan`)

### External Tools (Auto-installed)
`subfinder` • `amass` • `httpx` • `naabu` • `masscan` • `whatweb` • `katana` • `gau` • `waybackurls` • `dnsx` • `wafw00f` • `ffuf` • `gowitness`

---

## 🛠️ Changelog

### v2.0.0 — Major Update
| Change | Description |
|--------|-------------|
| 🆕 Passive Recon | WHOIS, ASN, IP, Reverse DNS added |
| 🆕 DNS Recon | Full DNS record enumeration (dnsx + dig) |
| 🆕 WAF Detection | wafw00f integration |
| 🆕 JS Analysis | Scans JS files for API keys, tokens, secrets |
| 🆕 CORS Check | Detects wildcard + credential CORS issues |
| 🆕 Dir Bruteforce | ffuf + seclists directory scanning |
| 🆕 Screenshots | gowitness auto-screenshots all live hosts |
| ⚡ Endpoints | Katana+GAU+Wayback now run in parallel (3x faster) |
| ⚡ Ports | Masscan rate 500 → 5000 (10x faster) |
| 🔧 Timeouts | All subprocess calls have timeouts (no more hangs) |
| 📊 Pipeline | 5 stages → 12 stages |

### v1.1.0 — Bug Fix Release
| Fix | Description |
|-----|-------------|
| 🎨 Banner | ASCII art rendering fixed |
| 🌐 httpx | Status codes + titles added |
| 🗺️ Endpoints | Static file filtering + deduplication |
| 🔌 Masscan | Port range to 1-65535 |

### v1.0.0 — Initial Release
- Full auto-pipeline, self-healing installer, HTML + Markdown reports

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
