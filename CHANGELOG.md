# 📦 Changelog

All notable changes to VAJRA will be documented here.

---

## [1.1.0] - 2025-08-26 🔧 Bug Fix Release

### Fixed
- 🎨 **Banner Fix** — "VAJBA" rendering bug fixed, ASCII art now displays correctly as "VAJRA"
- 🌐 **httpx** — Now shows status codes + page titles for live hosts
- 🗺️ **Endpoints** — Added URL deduplication + static file filtering (.png, .css, .js, etc.)
- 🔌 **Masscan** — Port range expanded to 1-65535 (was 1-1000)
- 🔌 **Ports** — Better output parsing, cleaner host:port format
- 🧠 **WhatWeb** — Fixed log-brief flag format
- ⚡ **Pipeline** — Each stage now shows timing + result counts
- 📊 **Summary Table** — Final scan summary with time per stage

### Added
- ⏱️ Per-stage timing display in final summary
- 📋 Rich-formatted output throughout all modules
- 🔢 Result counts after every stage

---

## [1.0.0] - 2025-01-01 🎉 Initial Release

### Added
- 🔍 Subdomain enumeration via `subfinder` + `amass`
- 🌐 Live host detection via `httpx`
- 🗺️ Endpoint collection via `katana`, `gau`, `waybackurls`
- 🔌 Port scanning via `masscan` + `naabu`
- 🧠 Technology fingerprinting via `whatweb`
- 🔧 Self-healing dependency installer
- 📊 HTML Scan Report Generator
- 📋 Markdown Recon Summary Generator

---

> To see all releases: [GitHub Releases](https://github.com/gauravjethva-lab/vajra-web-enumeration/releases)
