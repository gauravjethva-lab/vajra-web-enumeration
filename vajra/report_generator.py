"""
VAJRA - Professional HTML Report Generator v2.0
================================================
Generates a full dark-theme website-style report.
Usage: python3 report_generator.py <domain>
"""

import os, sys, datetime, base64

AUTHOR = "Gaurav Jethva"
GITHUB = "https://github.com/gauravjethva-lab/vajra-web-enumeration"


def read_file(path, limit=None):
    try:
        with open(path) as f:
            lines = [l.strip() for l in f
                     if l.strip()
                     and not l.strip().startswith("=")
                     and not l.strip().startswith("WHOIS —")]
        return lines[:limit] if limit else lines
    except:
        return []


def badge(text, color):
    colors = {
        "green":  ("#00ff88", "#001a0e"),
        "red":    ("#ff4444", "#1a0000"),
        "yellow": ("#ffcc00", "#1a1300"),
        "blue":   ("#4488ff", "#00001a"),
        "purple": ("#cc88ff", "#0d0020"),
        "gray":   ("#888888", "#111111"),
        "orange": ("#ff8844", "#1a0800"),
    }
    fg, bg = colors.get(color, colors["gray"])
    return f"<span class='badge' style='background:{bg};color:{fg};border:1px solid {fg}'>{text}</span>"


def rows(items, limit=300):
    if not items:
        return "<tr><td class='empty'>No data found.</td></tr>"
    html = ""
    for item in items[:limit]:
        html += f"<tr><td class='mono'>{item}</td></tr>"
    if len(items) > limit:
        html += f"<tr><td class='more'>... and {len(items)-limit} more — see output file</td></tr>"
    return html


def rows2(items, limit=300):
    if not items:
        return "<tr><td class='empty' colspan='2'>No data found.</td></tr>"
    html = ""
    for item in items[:limit]:
        parts = item.split(":", 1)
        html += f"<tr><td class='mono col1'>{parts[0]}</td><td class='mono'>{parts[1].strip() if len(parts)>1 else ''}</td></tr>"
    if len(items) > limit:
        html += f"<tr><td class='more' colspan='2'>... and {len(items)-limit} more</td></tr>"
    return html


def port_rows(items, limit=300):
    if not items:
        return "<tr><td class='empty' colspan='3'>No data found.</td></tr>"
    html = ""
    for item in items[:limit]:
        if ":" in item:
            host, port = item.rsplit(":", 1)
            html += f"<tr><td class='mono'>{host}</td><td class='mono'>{port}</td><td class='mono gray'>TCP — Requires Validation</td></tr>"
        else:
            html += f"<tr><td class='mono' colspan='3'>{item}</td></tr>"
    if len(items) > limit:
        html += f"<tr><td class='more' colspan='3'>... and {len(items)-limit} more</td></tr>"
    return html


def service_rows(items, limit=200):
    if not items or (len(items)==1 and "No services" in items[0]):
        return "<tr><td class='empty' colspan='3'>No services validated — nmap not available or no open ports.</td></tr>"
    html = ""
    for item in items[:limit]:
        parts = item.split("|", 1)
        host = parts[0].strip()
        info = parts[1].strip() if len(parts) > 1 else item
        html += f"<tr><td class='mono'>{host}</td><td class='mono'>{info}</td></tr>"
    return html


def generate_report(domain):
    base = f"output/{domain}"
    now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.now().strftime("%d %B %Y")

    # Read all data
    subdomains  = read_file(f"{base}/final_subdomains.txt")
    live_hosts  = read_file(f"{base}/live_subdomains.txt")
    endpoints   = read_file(f"{base}/all_endpoints.txt")
    inscope     = read_file(f"{base}/inscope_endpoints.txt")
    api_eps     = read_file(f"{base}/api_endpoints.txt")
    third_party = read_file(f"{base}/third_party_urls.txt")
    ports       = read_file(f"{base}/open_ports.txt")
    services    = read_file(f"{base}/validated_services.txt")
    techs       = read_file(f"{base}/technologies.txt")
    dns         = read_file(f"{base}/dns_records.txt")
    whois_data  = read_file(f"{base}/whois.txt")
    takeover    = read_file(f"{base}/takeover_results.txt")
    alive_urls  = read_file(f"{base}/alive_urls.txt")

    # Screenshots
    ss_dir  = f"{base}/screenshots"
    ss_html = ""
    ss_count = 0
    if os.path.exists(ss_dir):
        for root, dirs_, files in os.walk(ss_dir):
            for fname in files:
                if fname.endswith(".png"):
                    ss_count += 1
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "rb") as f:
                            enc = base64.b64encode(f.read()).decode()
                        label = fname.replace(".png", "").replace("_", ".")[:60]
                        ss_html += f"""<div class="ss-card">
                            <img src="data:image/png;base64,{enc}" alt="{label}" loading="lazy"/>
                            <div class="ss-label">{label}</div>
                        </div>"""
                    except:
                        pass

    if not ss_html:
        ss_html = "<p class='empty-msg'>No screenshots captured.</p>"

    # Takeover check
    takeover_vulns = [t for t in takeover if "VULNERABLE" in t]
    takeover_badge = badge(f"⚠️ {len(takeover_vulns)} Vulnerable", "red") if takeover_vulns else badge("✅ Clean", "green")

    # Alerts
    alerts_html = ""
    if takeover_vulns:
        for v in takeover_vulns:
            alerts_html += f"<div class='alert alert-red'>🔗 {v}</div>"
    if not alerts_html:
        alerts_html = "<div class='alert alert-green'>✅ No confirmed vulnerabilities detected by automated checks.</div>"

    # Confidence note
    confidence = "Medium" if len(live_hosts) > 0 else "Low"

    HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VAJRA Report — {domain}</title>
<style>
:root{{
  --bg:#0d1117;--bg2:#161b22;--bg3:#1c2128;--border:#30363d;
  --accent:#f0883e;--green:#00ff88;--red:#ff4444;--blue:#4488ff;
  --purple:#cc88ff;--yellow:#ffcc00;--text:#c9d1d9;--muted:#8b949e;
  --font:'Courier New',monospace;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);display:flex;min-height:100vh;}}

/* Sidebar */
.sidebar{{width:230px;min-height:100vh;background:var(--bg2);border-right:1px solid var(--border);position:fixed;top:0;left:0;overflow-y:auto;z-index:100;}}
.logo{{padding:16px;border-bottom:1px solid var(--border);text-align:center;}}
.logo-text{{color:var(--accent);font-size:20px;font-weight:bold;letter-spacing:3px;margin-bottom:4px;}}
.logo-sub{{color:var(--muted);font-size:9px;letter-spacing:1px;}}
.logo-meta{{margin-top:8px;font-size:10px;color:var(--muted);line-height:1.7;}}
.nav-link{{display:block;padding:9px 18px;color:var(--muted);text-decoration:none;font-size:11px;border-left:3px solid transparent;transition:all .15s;}}
.nav-link:hover,.nav-link.active{{color:var(--accent);border-left-color:var(--accent);background:rgba(240,136,62,.06);}}
.nav-section{{padding:10px 18px 4px;font-size:9px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-top:6px;}}

/* Main */
.main{{margin-left:230px;padding:28px 32px;width:100%;}}

/* Header */
.page-header{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:24px 28px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:flex-start;}}
.page-header h1{{color:var(--accent);font-size:20px;margin-bottom:6px;}}
.page-header .meta{{color:var(--muted);font-size:11px;line-height:2;}}
.header-right{{text-align:right;font-size:11px;color:var(--muted);}}

/* Stats */
.stats-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px;}}
.stat-card{{background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;transition:border-color .2s;}}
.stat-card:hover{{border-color:var(--accent);}}
.stat-icon{{font-size:18px;margin-bottom:6px;}}
.stat-num{{font-size:26px;font-weight:bold;margin-bottom:3px;}}
.stat-label{{color:var(--muted);font-size:10px;}}

/* Sections */
.section{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;margin-bottom:18px;overflow:hidden;}}
.section-header{{padding:13px 22px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;background:var(--bg3);}}
.section-header h2{{font-size:13px;color:var(--accent);}}
.section-body{{padding:18px 22px;}}

/* Table */
table{{width:100%;border-collapse:collapse;font-size:11px;}}
th{{background:var(--bg3);color:var(--muted);padding:8px 12px;text-align:left;border-bottom:1px solid var(--border);font-size:10px;letter-spacing:1px;}}
td{{padding:7px 12px;border-bottom:1px solid rgba(48,54,61,.4);}}
tr:hover td{{background:rgba(240,136,62,.03);}}
td.mono{{font-family:var(--font);word-break:break-all;}}
td.col1{{color:var(--muted);min-width:80px;}}
td.gray{{color:var(--muted);}}
td.empty{{color:var(--muted);text-align:center;padding:16px;font-style:italic;}}
td.more{{color:var(--muted);text-align:center;padding:6px;font-style:italic;font-size:10px;}}

/* Badges */
.badge{{padding:2px 9px;border-radius:20px;font-size:10px;font-weight:bold;display:inline-block;}}

/* Alerts */
.alert{{padding:12px 16px;border-radius:7px;margin-bottom:10px;font-size:11px;border-left:4px solid;}}
.alert-red{{background:rgba(255,68,68,.08);border-color:#ff4444;color:#ff8888;}}
.alert-yellow{{background:rgba(255,204,0,.08);border-color:#ffcc00;color:#ffdd44;}}
.alert-green{{background:rgba(0,255,136,.08);border-color:#00ff88;color:#44ffaa;}}
.alert-blue{{background:rgba(68,136,255,.08);border-color:#4488ff;color:#88aaff;}}

/* Confidence box */
.confidence-box{{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:14px 18px;margin-bottom:18px;font-size:11px;line-height:2;}}
.confidence-box strong{{color:var(--accent);}}

/* Passive block */
.passive-block{{background:var(--bg3);border-radius:7px;padding:14px;font-size:11px;line-height:1.8;white-space:pre-wrap;word-break:break-all;}}

/* Search */
.search-bar{{width:100%;background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:7px 12px;border-radius:5px;font-family:var(--font);font-size:11px;margin-bottom:12px;outline:none;}}
.search-bar:focus{{border-color:var(--accent);}}

/* Screenshots */
.ss-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}}
.ss-card{{background:var(--bg3);border:1px solid var(--border);border-radius:7px;overflow:hidden;}}
.ss-card img{{width:100%;display:block;}}
.ss-label{{padding:6px 10px;font-size:10px;color:var(--muted);word-break:break-all;}}
.empty-msg{{color:var(--muted);font-size:11px;padding:16px;text-align:center;font-style:italic;}}

/* Tabs */
.tabs{{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;}}
.tab{{padding:5px 14px;border-radius:20px;font-size:10px;cursor:pointer;border:1px solid var(--border);color:var(--muted);background:var(--bg3);transition:all .15s;}}
.tab.active,.tab:hover{{background:var(--accent);color:#000;border-color:var(--accent);}}

/* Footer */
.footer{{text-align:center;color:var(--muted);font-size:10px;padding:24px 0 8px;border-top:1px solid var(--border);margin-top:8px;}}
</style>
</head>
<body>

<!-- Sidebar -->
<nav class="sidebar">
  <div class="logo">
    <div class="logo-text">⚡ VAJRA</div>
    <div class="logo-sub">WEB ENUMERATION FRAMEWORK</div>
    <div class="logo-meta">
      🎯 {domain}<br>
      📅 {date}<br>
      👤 {AUTHOR}
    </div>
  </div>

  <div class="nav-section">Navigation</div>
  <a href="#executive" class="nav-link">📋 Executive Summary</a>
  <a href="#attack-surface" class="nav-link">🗺️ Attack Surface</a>
  <a href="#alerts" class="nav-link">🚨 Alerts</a>

  <div class="nav-section">Reconnaissance</div>
  <a href="#whois" class="nav-link">🌍 WHOIS</a>
  <a href="#dns" class="nav-link">🔎 DNS Records</a>
  <a href="#subdomains" class="nav-link">🔍 Subdomains</a>
  <a href="#live" class="nav-link">🌐 Live Hosts</a>

  <div class="nav-section">Analysis</div>
  <a href="#endpoints" class="nav-link">🗺️ Endpoints</a>
  <a href="#ports" class="nav-link">🔌 Ports & Services</a>
  <a href="#tech" class="nav-link">🧠 Technologies</a>
  <a href="#takeover" class="nav-link">🔗 Takeover Check</a>
  <a href="#screenshots" class="nav-link">📸 Screenshots</a>

  <div class="nav-section">Reports</div>
  <a href="#coverage" class="nav-link">📊 Scan Coverage</a>
</nav>

<!-- Main -->
<main class="main">

<!-- Executive Summary -->
<div id="executive" class="page-header">
  <div>
    <h1>⚡ VAJRA Reconnaissance Report</h1>
    <div class="meta">
      🎯 Target &nbsp;&nbsp;&nbsp;: <strong style="color:var(--accent)">{domain}</strong><br>
      📅 Scan Date : {now}<br>
      👤 Author &nbsp;&nbsp;&nbsp;: <strong style="color:var(--accent)">{AUTHOR}</strong><br>
      🔱 Scanner &nbsp;: VAJRA Web Enumeration Framework<br>
      📋 Type &nbsp;&nbsp;&nbsp;&nbsp;: External Attack Surface Reconnaissance
    </div>
  </div>
  <div class="header-right">
    {takeover_badge}<br><br>
    <span style="color:var(--muted)">Confidence: <strong style="color:var(--yellow)">{confidence}</strong></span><br>
    <span style="color:var(--muted)">Type: <strong style="color:var(--blue)">Recon Only</strong></span>
  </div>
</div>

<!-- Confidence Note -->
<div class="confidence-box">
  <strong>⚠️ Important:</strong> This is an <strong>External Attack Surface Reconnaissance Report</strong>, not a penetration test.
  Results represent discovered assets and raw observations — not confirmed vulnerabilities.
  Each finding requires authorized validation before classification as a security issue.<br>
  <strong>Confidence Level: {confidence}</strong> — based on scan coverage and data quality.
</div>

<!-- Stats -->
<div id="attack-surface" class="stats-grid">
  <div class="stat-card">
    <div class="stat-icon">🔍</div>
    <div class="stat-num" style="color:#4488ff">{len(subdomains)}</div>
    <div class="stat-label">Subdomains</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🌐</div>
    <div class="stat-num" style="color:#00ff88">{len(live_hosts)}</div>
    <div class="stat-label">Live Hosts</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🗺️</div>
    <div class="stat-num" style="color:#aa88ff">{len(endpoints)}</div>
    <div class="stat-label">Raw URLs</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🔌</div>
    <div class="stat-num" style="color:#ffaa00">{len(ports)}</div>
    <div class="stat-label">Port Observations</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🧠</div>
    <div class="stat-num" style="color:#ff8844">{len(techs)}</div>
    <div class="stat-label">Tech Fingerprints</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🎯</div>
    <div class="stat-num" style="color:#00ff88">{len(inscope)}</div>
    <div class="stat-label">In-Scope URLs</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">⚡</div>
    <div class="stat-num" style="color:#cc88ff">{len(api_eps)}</div>
    <div class="stat-label">API Endpoints</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🔗</div>
    <div class="stat-num" style="color:{'#ff4444' if takeover_vulns else '#00ff88'}">{len(takeover_vulns)}</div>
    <div class="stat-label">Takeover Risks</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">✅</div>
    <div class="stat-num" style="color:#00ff88">{len(services) if services and 'No services' not in ''.join(services) else 0}</div>
    <div class="stat-label">Validated Services</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">📸</div>
    <div class="stat-num" style="color:#44aaff">{ss_count}</div>
    <div class="stat-label">Screenshots</div>
  </div>
</div>

<!-- Alerts -->
<div id="alerts">
  {alerts_html}
  <div class="alert alert-blue">
    ℹ️ <strong>Recon Note:</strong> Raw port observations ({len(ports)}) require service-level validation.
    Raw URLs ({len(endpoints)}) include third-party ({len(third_party)}) and historical links — see in-scope ({len(inscope)}) for target-owned URLs.
  </div>
</div>

<!-- WHOIS -->
<div id="whois" class="section">
  <div class="section-header">
    <h2>🌍 WHOIS Information</h2>
    <span style="color:var(--muted);font-size:10px">{domain}</span>
  </div>
  <div class="section-body">
    <div class="passive-block">{chr(10).join(whois_data) if whois_data else 'No WHOIS data found.'}</div>
  </div>
</div>

<!-- DNS -->
<div id="dns" class="section">
  <div class="section-header">
    <h2>🔎 DNS Records</h2>
    {badge(f"{len(dns)} Records", "blue")}
  </div>
  <div class="section-body">
    <table>
      <tr><th>Type</th><th>Value</th></tr>
      {rows2(dns)}
    </table>
  </div>
</div>

<!-- Subdomains -->
<div id="subdomains" class="section">
  <div class="section-header">
    <h2>🔍 Subdomains Discovered</h2>
    {badge(f"{len(subdomains)} Found", "blue")}
  </div>
  <div class="section-body">
    <input class="search-bar" placeholder="🔍 Filter subdomains..." oninput="filterTable(this,'sub-table')">
    <table id="sub-table">
      <tr><th>Subdomain</th></tr>
      {rows(subdomains)}
    </table>
  </div>
</div>

<!-- Live Hosts -->
<div id="live" class="section">
  <div class="section-header">
    <h2>🌐 Live Hosts</h2>
    {badge(f"{len(live_hosts)} Live", "green")}
  </div>
  <div class="section-body">
    <table>
      <tr><th>Host — Status — Title</th></tr>
      {rows(live_hosts)}
    </table>
  </div>
</div>

<!-- Endpoints -->
<div id="endpoints" class="section">
  <div class="section-header">
    <h2>🗺️ Endpoint Analysis</h2>
    {badge(f"{len(endpoints)} Raw", "purple")}
    &nbsp;{badge(f"{len(inscope)} In-Scope", "green")}
    &nbsp;{badge(f"{len(api_eps)} API", "blue")}
    &nbsp;{badge(f"{len(third_party)} 3rd Party", "gray")}
  </div>
  <div class="section-body">
    <div class="alert alert-blue" style="margin-bottom:14px">
      Raw URLs: {len(endpoints)} &nbsp;|&nbsp;
      In-Scope (target-owned): {len(inscope)} &nbsp;|&nbsp;
      API Endpoints: {len(api_eps)} &nbsp;|&nbsp;
      Third-Party: {len(third_party)}
    </div>
    <div class="tabs">
      <div class="tab active" onclick="showTab('inscope-tab','endpoints-tabs',this)">🎯 In-Scope ({len(inscope)})</div>
      <div class="tab" onclick="showTab('api-tab','endpoints-tabs',this)">⚡ API ({len(api_eps)})</div>
      <div class="tab" onclick="showTab('all-tab','endpoints-tabs',this)">📋 All URLs ({len(endpoints)})</div>
    </div>
    <div id="endpoints-tabs">
      <div id="inscope-tab" class="tab-content">
        <input class="search-bar" placeholder="🔍 Filter in-scope URLs..." oninput="filterTable(this,'inscope-table')">
        <table id="inscope-table"><tr><th>In-Scope URL</th></tr>{rows(inscope)}</table>
      </div>
      <div id="api-tab" class="tab-content" style="display:none">
        <input class="search-bar" placeholder="🔍 Filter API endpoints..." oninput="filterTable(this,'api-table')">
        <table id="api-table"><tr><th>API Endpoint</th></tr>{rows(api_eps)}</table>
      </div>
      <div id="all-tab" class="tab-content" style="display:none">
        <input class="search-bar" placeholder="🔍 Filter all URLs..." oninput="filterTable(this,'all-table')">
        <table id="all-table"><tr><th>URL</th></tr>{rows(endpoints)}</table>
      </div>
    </div>
  </div>
</div>

<!-- Ports & Services -->
<div id="ports" class="section">
  <div class="section-header">
    <h2>🔌 Ports & Services</h2>
    {badge(f"{len(ports)} Observations", "orange")}
  </div>
  <div class="section-body">
    <div class="alert alert-yellow" style="margin-bottom:14px">
      ⚠️ Raw port observations require service-level validation before being classified as confirmed open services.
    </div>
    <div class="tabs">
      <div class="tab active" onclick="showTab('services-tab','ports-tabs',this)">✅ Validated Services</div>
      <div class="tab" onclick="showTab('raw-ports-tab','ports-tabs',this)">📋 Raw Observations ({len(ports)})</div>
    </div>
    <div id="ports-tabs">
      <div id="services-tab" class="tab-content">
        <table><tr><th>Host</th><th>Service Info (nmap -sV)</th></tr>{service_rows(services)}</table>
      </div>
      <div id="raw-ports-tab" class="tab-content" style="display:none">
        <table><tr><th>Host</th><th>Port</th><th>Status</th></tr>{port_rows(ports)}</table>
      </div>
    </div>
  </div>
</div>

<!-- Technologies -->
<div id="tech" class="section">
  <div class="section-header">
    <h2>🧠 Technology Fingerprinting</h2>
    {badge(f"{len(techs)} Hosts", "orange")}
  </div>
  <div class="section-body">
    <table>
      <tr><th>Host + Technologies Detected</th></tr>
      {rows(techs)}
    </table>
  </div>
</div>

<!-- Takeover -->
<div id="takeover" class="section">
  <div class="section-header">
    <h2>🔗 Subdomain Takeover Check</h2>
    {takeover_badge}
  </div>
  <div class="section-body">
    {''.join(f'<div class="alert alert-red">🔗 {t}</div>' for t in takeover_vulns) if takeover_vulns
     else '<div class="alert alert-green">✅ No subdomain takeover vulnerabilities detected.</div>'}
  </div>
</div>

<!-- Screenshots -->
<div id="screenshots" class="section">
  <div class="section-header">
    <h2>📸 Screenshots</h2>
    {badge(f"{ss_count} Captured", "green")}
  </div>
  <div class="section-body">
    <div class="ss-grid">{ss_html}</div>
  </div>
</div>

<!-- Scan Coverage -->
<div id="coverage" class="section">
  <div class="section-header">
    <h2>📊 Scan Coverage</h2>
    <span style="font-size:10px;color:var(--muted)">What was tested</span>
  </div>
  <div class="section-body">
    <table>
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td class="mono">Subdomains Discovered</td><td class="mono" style="color:var(--accent)">{len(subdomains)}</td></tr>
      <tr><td class="mono">Live Hosts Confirmed</td><td class="mono" style="color:var(--green)">{len(live_hosts)}</td></tr>
      <tr><td class="mono">Raw URLs Collected</td><td class="mono">{len(endpoints)}</td></tr>
      <tr><td class="mono">In-Scope URLs</td><td class="mono" style="color:var(--green)">{len(inscope)}</td></tr>
      <tr><td class="mono">API Endpoints</td><td class="mono" style="color:var(--purple)">{len(api_eps)}</td></tr>
      <tr><td class="mono">Third-Party URLs</td><td class="mono" style="color:var(--muted)">{len(third_party)}</td></tr>
      <tr><td class="mono">Raw Port Observations</td><td class="mono">{len(ports)}</td></tr>
      <tr><td class="mono">Validated Services (nmap)</td><td class="mono" style="color:var(--green)">{len([s for s in services if '|' in s]) if services else 0}</td></tr>
      <tr><td class="mono">Subdomains Checked for Takeover</td><td class="mono">{len(subdomains)}</td></tr>
      <tr><td class="mono">Takeover Vulnerabilities</td><td class="mono" style="color:{'var(--red)' if takeover_vulns else 'var(--green)'}">{len(takeover_vulns)}</td></tr>
      <tr><td class="mono">Screenshots Captured</td><td class="mono">{ss_count}</td></tr>
      <tr><td class="mono">DNS Records Found</td><td class="mono">{len(dns)}</td></tr>
    </table>
    <div class="alert alert-blue" style="margin-top:14px">
      ℹ️ This report covers external reconnaissance only. Manual validation, authenticated testing,
      and business logic review are outside this scan scope.
    </div>
  </div>
</div>

<!-- Footer -->
<div class="footer">
  <p>⚡ Generated by <strong style="color:var(--accent)">VAJRA Web Enumeration Framework</strong> &nbsp;|&nbsp;
  👤 <strong style="color:var(--accent)">{AUTHOR}</strong> &nbsp;|&nbsp;
  <a href="{GITHUB}" style="color:var(--accent)">GitHub</a></p>
  <p style="margin-top:4px">⚠️ For authorized security testing only. This is a reconnaissance report, not a penetration test.</p>
</div>

</main>

<script>
function filterTable(input, tableId) {{
  const filter = input.value.toLowerCase();
  const rows = document.getElementById(tableId).getElementsByTagName('tr');
  for (let i = 1; i < rows.length; i++) {{
    rows[i].style.display = rows[i].textContent.toLowerCase().includes(filter) ? '' : 'none';
  }}
}}

function showTab(tabId, groupId, btn) {{
  const group = document.getElementById(groupId);
  group.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
  document.getElementById(tabId).style.display = 'block';
  btn.closest('.section-body').querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
}}

// Active nav on scroll
const sections = document.querySelectorAll('[id]');
const navLinks = document.querySelectorAll('.nav-link');
window.addEventListener('scroll', () => {{
  let current = '';
  sections.forEach(s => {{ if (window.scrollY >= s.offsetTop - 100) current = s.id; }});
  navLinks.forEach(a => {{
    const active = a.href.includes(current);
    a.style.color = active ? 'var(--accent)' : '';
    a.style.borderLeftColor = active ? 'var(--accent)' : 'transparent';
  }});
}});
</script>
</body>
</html>"""

    out_path = f"{base}/vajra_report.html"
    os.makedirs(base, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HTML)

    print(f"\n✅ Report saved: {out_path}")
    print(f"   Open: firefox {out_path} &")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 report_generator.py <domain>")
        sys.exit(1)
    generate_report(sys.argv[1])
