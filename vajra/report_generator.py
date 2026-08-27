"""
VAJRA - Professional HTML Report Generator
==========================================
Generates a full dark-theme website-style report after scan.
Usage: python3 report_generator.py <domain>
"""

import os, sys, datetime, json

def read_file(path, limit=None):
    try:
        with open(path) as f:
            lines = [l.strip() for l in f if l.strip()]
        return lines[:limit] if limit else lines
    except:
        return []

def count_file(path):
    try:
        with open(path) as f:
            return sum(1 for l in f if l.strip())
    except:
        return 0

def make_table_rows(items, cols=1, limit=200):
    if not items:
        return "<tr><td colspan='{}' class='empty'>No data found.</td></tr>".format(cols)
    html = ""
    for item in items[:limit]:
        if cols == 2:
            parts = item.split(":", 1)
            html += f"<tr><td class='mono'>{parts[0]}</td><td class='mono'>{parts[1] if len(parts)>1 else ''}</td></tr>"
        else:
            html += f"<tr><td class='mono'>{item}</td></tr>"
    if len(items) > limit:
        html += f"<tr><td class='more'>... and {len(items)-limit} more entries</td></tr>"
    return html

def badge(text, color):
    colors = {
        "green": ("#00ff88", "#001a0e"),
        "red":   ("#ff4444", "#1a0000"),
        "yellow":("#ffcc00", "#1a1300"),
        "blue":  ("#4488ff", "#00001a"),
        "gray":  ("#888888", "#111111"),
    }
    fg, bg = colors.get(color, colors["gray"])
    return f"<span class='badge' style='background:{bg};color:{fg};border:1px solid {fg}'>{text}</span>"

def generate_report(domain):
    base = f"output/{domain}"
    now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read all data
    subdomains  = read_file(f"{base}/final_subdomains.txt")
    live_hosts  = read_file(f"{base}/live_subdomains.txt")
    endpoints   = read_file(f"{base}/all_endpoints.txt")
    ports       = read_file(f"{base}/open_ports.txt")
    techs       = read_file(f"{base}/technologies.txt")
    dns         = read_file(f"{base}/dns_records.txt")
    waf         = read_file(f"{base}/waf_results.txt")
    passive     = read_file(f"{base}/passive_recon.txt")
    cors        = read_file(f"{base}/cors_issues.txt")
    js          = read_file(f"{base}/js_findings.txt")
    dirs        = read_file(f"{base}/directories.txt")
    screenshots_dir = f"{base}/screenshots"
    screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")] if os.path.exists(screenshots_dir) else []

    # Severity badges
    cors_badge = badge(f"{len(cors)} Issues", "red") if cors else badge("Clean", "green")
    js_badge   = badge(f"{len(js)} Findings", "red") if js else badge("Clean", "green")
    waf_wafs   = [w for w in waf if "No WAF" not in w] if waf else []
    waf_badge  = badge(f"{len(waf_wafs)} WAFs", "yellow") if waf_wafs else badge("No WAF", "gray")

    # Stats cards data
    stats = [
        ("🔍", "Subdomains",   len(subdomains),  "#4488ff"),
        ("🌐", "Live Hosts",   len(live_hosts),  "#00ff88"),
        ("🗺️", "Endpoints",   len(endpoints),   "#aa88ff"),
        ("🔌", "Open Ports",   len(ports),       "#ffaa00"),
        ("🧠", "Technologies", len(techs),       "#ff8844"),
        ("📜", "JS Findings",  len(js),          "#ff4444"),
        ("⚡", "CORS Issues",  len(cors),        "#ff4444"),
        ("📂", "Directories",  len(dirs),        "#44aaff"),
    ]

    def stat_cards():
        html = ""
        for icon, label, count, color in stats:
            html += f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-num" style="color:{color}">{count}</div>
                <div class="stat-label">{label}</div>
            </div>"""
        return html

    # Nav items
    sections = [
        ("overview",   "📊 Overview"),
        ("passive",    "🌍 Passive Recon"),
        ("dns",        "🔎 DNS"),
        ("subdomains", "🔍 Subdomains"),
        ("live",       "🌐 Live Hosts"),
        ("waf",        "🛡️ WAF"),
        ("endpoints",  "🗺️ Endpoints"),
        ("js",         "📜 JS Analysis"),
        ("cors",       "⚡ CORS"),
        ("ports",      "🔌 Ports"),
        ("tech",       "🧠 Tech"),
        ("dirs",       "📂 Directories"),
        ("screenshots","📸 Screenshots"),
    ]

    nav_html = "".join(f'<a href="#{sid}" class="nav-link">{label}</a>' for sid, label in sections)

    # Screenshots HTML
    screenshots_html = ""
    if screenshots:
        for ss in screenshots[:30]:
            ss_path = os.path.join(screenshots_dir, ss)
            import base64 as b64mod
            try:
                with open(ss_path, "rb") as f:
                    encoded = b64mod.b64encode(f.read()).decode()
                screenshots_html += f'<div class="screenshot-card"><img src="data:image/png;base64,{encoded}" alt="{ss}"/><div class="ss-label">{ss.replace(".png","")}</div></div>'
            except:
                pass
    else:
        screenshots_html = "<p class='empty-msg'>No screenshots captured.</p>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VAJRA Report — {domain}</title>
<style>
  :root {{
    --bg: #0d1117; --bg2: #161b22; --bg3: #1c2128;
    --border: #30363d; --accent: #f0883e;
    --green: #00ff88; --red: #ff4444; --blue: #4488ff;
    --text: #c9d1d9; --muted: #8b949e;
    --font: 'Courier New', monospace;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--text); font-family:var(--font); display:flex; min-height:100vh; }}

  /* Sidebar */
  .sidebar {{
    width:220px; min-height:100vh; background:var(--bg2);
    border-right:1px solid var(--border); position:fixed;
    top:0; left:0; overflow-y:auto; z-index:100;
    display:flex; flex-direction:column;
  }}
  .sidebar-logo {{
    padding:20px 16px; border-bottom:1px solid var(--border); text-align:center;
  }}
  .sidebar-logo pre {{
    color:var(--accent); font-size:7px; line-height:1.1; white-space:pre;
  }}
  .sidebar-meta {{
    font-size:10px; color:var(--muted); margin-top:6px;
  }}
  .nav-link {{
    display:block; padding:10px 20px; color:var(--muted);
    text-decoration:none; font-size:12px; border-left:3px solid transparent;
    transition:all .2s;
  }}
  .nav-link:hover {{ color:var(--accent); border-left-color:var(--accent); background:rgba(240,136,62,.05); }}

  /* Main */
  .main {{ margin-left:220px; padding:30px; width:100%; }}

  /* Header */
  .page-header {{
    background:var(--bg2); border:1px solid var(--border); border-radius:12px;
    padding:28px 32px; margin-bottom:24px;
    display:flex; justify-content:space-between; align-items:center;
  }}
  .page-header h1 {{ color:var(--accent); font-size:22px; }}
  .page-header .meta {{ color:var(--muted); font-size:12px; margin-top:6px; line-height:1.8; }}
  .version-badge {{ background:var(--accent); color:#000; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:bold; }}

  /* Stats grid */
  .stats-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:24px; }}
  .stat-card {{
    background:var(--bg2); border:1px solid var(--border); border-radius:10px;
    padding:20px; text-align:center; transition:border-color .2s;
  }}
  .stat-card:hover {{ border-color:var(--accent); }}
  .stat-icon {{ font-size:22px; margin-bottom:8px; }}
  .stat-num {{ font-size:32px; font-weight:bold; margin-bottom:4px; }}
  .stat-label {{ color:var(--muted); font-size:11px; }}

  /* Sections */
  .section {{
    background:var(--bg2); border:1px solid var(--border); border-radius:12px;
    margin-bottom:20px; overflow:hidden;
  }}
  .section-header {{
    padding:16px 24px; border-bottom:1px solid var(--border);
    display:flex; justify-content:space-between; align-items:center;
    background:var(--bg3);
  }}
  .section-header h2 {{ font-size:15px; color:var(--accent); }}
  .section-body {{ padding:20px 24px; }}

  /* Table */
  table {{ width:100%; border-collapse:collapse; font-size:12px; }}
  th {{ background:var(--bg3); color:var(--muted); padding:10px 14px; text-align:left; border-bottom:1px solid var(--border); }}
  td {{ padding:8px 14px; border-bottom:1px solid rgba(48,54,61,.5); color:var(--text); }}
  tr:hover td {{ background:rgba(240,136,62,.04); }}
  td.mono {{ font-family:var(--font); font-size:11px; word-break:break-all; }}
  td.empty {{ color:var(--muted); text-align:center; padding:20px; }}
  td.more {{ color:var(--muted); font-size:11px; text-align:center; font-style:italic; padding:8px; }}

  /* Badge */
  .badge {{ padding:3px 10px; border-radius:20px; font-size:10px; font-weight:bold; }}
  .tag {{ display:inline-block; background:rgba(240,136,62,.15); color:var(--accent); padding:2px 8px; border-radius:4px; font-size:10px; margin:2px; }}

  /* Alert boxes */
  .alert {{ padding:14px 18px; border-radius:8px; margin-bottom:12px; font-size:12px; border-left:4px solid; }}
  .alert-red    {{ background:rgba(255,68,68,.08);  border-color:#ff4444; color:#ff8888; }}
  .alert-yellow {{ background:rgba(255,204,0,.08);  border-color:#ffcc00; color:#ffdd44; }}
  .alert-green  {{ background:rgba(0,255,136,.08);  border-color:#00ff88; color:#44ffaa; }}

  /* Screenshots */
  .screenshots-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
  .screenshot-card {{ background:var(--bg3); border:1px solid var(--border); border-radius:8px; overflow:hidden; }}
  .screenshot-card img {{ width:100%; display:block; }}
  .ss-label {{ padding:8px 12px; font-size:10px; color:var(--muted); word-break:break-all; }}
  .empty-msg {{ color:var(--muted); font-size:12px; padding:20px; text-align:center; }}

  /* Passive block */
  .passive-block {{ background:var(--bg3); border-radius:8px; padding:16px; font-size:11px; line-height:1.9; white-space:pre-wrap; word-break:break-all; }}

  /* Footer */
  .footer {{ text-align:center; color:var(--muted); font-size:11px; padding:30px 0 10px; }}

  /* Search */
  .search-bar {{ width:100%; background:var(--bg3); border:1px solid var(--border); color:var(--text); padding:8px 14px; border-radius:6px; font-family:var(--font); font-size:12px; margin-bottom:14px; outline:none; }}
  .search-bar:focus {{ border-color:var(--accent); }}
</style>
</head>
<body>

<!-- Sidebar -->
<nav class="sidebar">
  <div class="sidebar-logo">
    <pre>
██╗   ██╗
██║   ██║
██║   ██║
╚██╗ ██╔╝
 ╚████╔╝
  ╚═══╝
 █████╗      ██╗
██╔══██╗     ██║
███████║     ██║
██╔══██║██╗  ██║
██║  ██║╚█████╔╝
╚═╝  ╚═╝ ╚════╝
██████╗  █████╗
██╔══██╗██╔══██╗
██████╔╝███████║
██╔══██╗██╔══██║
██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝
    </pre>
    <div class="sidebar-meta">
      🎯 {domain}<br>
      📅 {now}<br>
      <span class="version-badge">v2.0.0</span>
    </div>
  </div>
  {nav_html}
</nav>

<!-- Main Content -->
<main class="main">

  <!-- Header -->
  <div class="page-header">
    <div>
      <h1>⚡ VAJRA Scan Report</h1>
      <div class="meta">
        🎯 Target: <strong style="color:var(--accent)">{domain}</strong><br>
        📅 Scan Date: {now}<br>
        🔱 12-Stage Full Recon Pipeline
      </div>
    </div>
    <div style="text-align:right">
      {cors_badge}&nbsp;{js_badge}&nbsp;{waf_badge}
      <div style="margin-top:10px;font-size:11px;color:var(--muted)">Security Indicators</div>
    </div>
  </div>

  <!-- Stats -->
  <div id="overview" class="stats-grid">
    {stat_cards()}
  </div>

  <!-- Quick Findings Alert -->
  {'<div class="alert alert-red">🚨 <strong>CORS Issues Detected!</strong> ' + str(len(cors)) + ' misconfiguration(s) found — check CORS section.</div>' if cors else ''}
  {'<div class="alert alert-red">🔑 <strong>JS Secrets Found!</strong> ' + str(len(js)) + ' potential secret(s) detected in JavaScript files.</div>' if js else ''}
  {'<div class="alert alert-green">✅ No critical CORS or JS issues found.</div>' if not cors and not js else ''}

  <!-- Passive Recon -->
  <div id="passive" class="section">
    <div class="section-header">
      <h2>🌍 Passive Recon — WHOIS / ASN / IP</h2>
    </div>
    <div class="section-body">
      <div class="passive-block">{chr(10).join(passive) if passive else 'No passive recon data found.'}</div>
    </div>
  </div>

  <!-- DNS -->
  <div id="dns" class="section">
    <div class="section-header">
      <h2>🔎 DNS Records</h2>
      <span class="badge" style="background:#001a1a;color:#00ffcc;border:1px solid #00ffcc">{len(dns)} Records</span>
    </div>
    <div class="section-body">
      <table>
        <tr><th>Type</th><th>Value</th></tr>
        {make_table_rows(dns, cols=2)}
      </table>
    </div>
  </div>

  <!-- Subdomains -->
  <div id="subdomains" class="section">
    <div class="section-header">
      <h2>🔍 Subdomains</h2>
      <span class="badge" style="background:#001020;color:#4488ff;border:1px solid #4488ff">{len(subdomains)} Found</span>
    </div>
    <div class="section-body">
      <input class="search-bar" placeholder="🔍 Filter subdomains..." oninput="filterTable(this,'subdomain-table')">
      <table id="subdomain-table">
        <tr><th>Subdomain</th></tr>
        {make_table_rows(subdomains)}
      </table>
    </div>
  </div>

  <!-- Live Hosts -->
  <div id="live" class="section">
    <div class="section-header">
      <h2>🌐 Live Hosts</h2>
      <span class="badge" style="background:#001a0e;color:#00ff88;border:1px solid #00ff88">{len(live_hosts)} Live</span>
    </div>
    <div class="section-body">
      <table>
        <tr><th>Host / URL + Status + Title</th></tr>
        {make_table_rows(live_hosts)}
      </table>
    </div>
  </div>

  <!-- WAF -->
  <div id="waf" class="section">
    <div class="section-header">
      <h2>🛡️ WAF Detection</h2>
      {waf_badge}
    </div>
    <div class="section-body">
      {''.join(f'<div class="alert alert-yellow">🛡️ {w}</div>' for w in waf) if waf else '<div class="alert alert-green">✅ No WAF detected on scanned hosts.</div>'}
    </div>
  </div>

  <!-- Endpoints -->
  <div id="endpoints" class="section">
    <div class="section-header">
      <h2>🗺️ Endpoints</h2>
      <span class="badge" style="background:#0a0020;color:#aa88ff;border:1px solid #aa88ff">{len(endpoints)} URLs</span>
    </div>
    <div class="section-body">
      <input class="search-bar" placeholder="🔍 Filter endpoints..." oninput="filterTable(this,'endpoint-table')">
      <table id="endpoint-table">
        <tr><th>URL</th></tr>
        {make_table_rows(endpoints, limit=300)}
      </table>
    </div>
  </div>

  <!-- JS Analysis -->
  <div id="js" class="section">
    <div class="section-header">
      <h2>📜 JS File Analysis — Secrets & Endpoints</h2>
      {js_badge}
    </div>
    <div class="section-body">
      {''.join(f'<div class="alert alert-red">🔑 {j}</div>' for j in js) if js else '<div class="alert alert-green">✅ No secrets or sensitive endpoints found in JS files.</div>'}
    </div>
  </div>

  <!-- CORS -->
  <div id="cors" class="section">
    <div class="section-header">
      <h2>⚡ CORS Misconfigurations</h2>
      {cors_badge}
    </div>
    <div class="section-body">
      {''.join(f'<div class="alert alert-red">⚡ {c}</div>' for c in cors) if cors else '<div class="alert alert-green">✅ No CORS misconfigurations detected.</div>'}
    </div>
  </div>

  <!-- Ports -->
  <div id="ports" class="section">
    <div class="section-header">
      <h2>🔌 Open Ports</h2>
      <span class="badge" style="background:#1a0d00;color:#ffaa00;border:1px solid #ffaa00">{len(ports)} Open</span>
    </div>
    <div class="section-body">
      <table>
        <tr><th>Host</th><th>Port</th></tr>
        {''.join(f"<tr><td class='mono'>{p.split(':')[0] if ':' in p else p}</td><td class='mono'>{p.split(':')[1] if ':' in p else '-'}</td></tr>" for p in ports[:200]) if ports else "<tr><td colspan='2' class='empty'>No open ports found.</td></tr>"}
      </table>
    </div>
  </div>

  <!-- Technologies -->
  <div id="tech" class="section">
    <div class="section-header">
      <h2>🧠 Technology Fingerprinting</h2>
      <span class="badge" style="background:#1a0900;color:#ff8844;border:1px solid #ff8844">{len(techs)} Hosts</span>
    </div>
    <div class="section-body">
      <table>
        <tr><th>Host + Technologies Detected</th></tr>
        {make_table_rows(techs)}
      </table>
    </div>
  </div>

  <!-- Directories -->
  <div id="dirs" class="section">
    <div class="section-header">
      <h2>📂 Directory Bruteforce Results</h2>
      <span class="badge" style="background:#001020;color:#44aaff;border:1px solid #44aaff">{len(dirs)} Found</span>
    </div>
    <div class="section-body">
      <input class="search-bar" placeholder="🔍 Filter directories..." oninput="filterTable(this,'dirs-table')">
      <table id="dirs-table">
        <tr><th>URL / Path Found</th></tr>
        {make_table_rows(dirs, limit=300)}
      </table>
    </div>
  </div>

  <!-- Screenshots -->
  <div id="screenshots" class="section">
    <div class="section-header">
      <h2>📸 Screenshots</h2>
      <span class="badge" style="background:#001a0e;color:#00ff88;border:1px solid #00ff88">{len(screenshots)} Captured</span>
    </div>
    <div class="section-body">
      <div class="screenshots-grid">
        {screenshots_html}
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>⚡ Generated by <strong style="color:var(--accent)">VAJRA Web Enumeration Framework v2.0.0</strong></p>
    <p style="margin-top:4px">⚠️ For authorized security testing only — <a href="https://github.com/gauravjethva-lab/vajra-web-enumeration" style="color:var(--accent)">GitHub</a></p>
  </div>

</main>

<script>
function filterTable(input, tableId) {{
  const filter = input.value.toLowerCase();
  const rows = document.getElementById(tableId).getElementsByTagName('tr');
  for (let i = 1; i < rows.length; i++) {{
    const text = rows[i].textContent.toLowerCase();
    rows[i].style.display = text.includes(filter) ? '' : 'none';
  }}
}}

// Highlight active nav on scroll
const sections = document.querySelectorAll('[id]');
const navLinks = document.querySelectorAll('.nav-link');
window.addEventListener('scroll', () => {{
  let current = '';
  sections.forEach(s => {{
    if (window.scrollY >= s.offsetTop - 80) current = s.id;
  }});
  navLinks.forEach(a => {{
    a.style.color = a.href.includes(current) ? 'var(--accent)' : '';
    a.style.borderLeftColor = a.href.includes(current) ? 'var(--accent)' : 'transparent';
  }});
}});
</script>
</body>
</html>"""

    out_path = f"{base}/vajra_report.html"
    os.makedirs(base, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Report saved: {out_path}")
    print(f"   Open in browser: firefox {out_path} &")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 report_generator.py <domain>")
        sys.exit(1)
    generate_report(sys.argv[1])
