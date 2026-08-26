# 📦 Changelog

All notable changes to VAJRA will be documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2025-01-01 🎉 Initial Release

### Added
- 🔍 Subdomain enumeration via `subfinder` + `amass`
- 🌐 Live host detection via `httpx`
- 🗺️ Endpoint collection via `katana`, `gau`, `waybackurls`
- 🔌 Port scanning via `masscan` + `naabu`
- 🧠 Technology fingerprinting via `whatweb`
- 🔧 Self-healing dependency installer (`install.sh`)
- ⚡ Full auto-pipeline — one command does everything
- 📊 HTML Scan Report Generator
- 📋 Markdown Recon Summary Report

### Fixed
- 🩹 Domain sanitization — full URLs cleaned to hostname
- 🔗 Endpoint collection now wired into main pipeline
- 🔐 `masscan` auto-prefixes `sudo` when not root
- 🛡️ Graceful handling when tools are missing

---

## [Unreleased] — Coming Soon

### Planned
- 🌍 Multiple target batch scanning
- 📧 Email notification on scan complete
- 🎨 Improved HTML report with charts
- 🔗 Integration with Shodan/Censys APIs
- 🐳 Docker support

---

> To see all releases: [GitHub Releases](https://github.com/gauravjethva-lab/vajra-web-enumeration/releases)
