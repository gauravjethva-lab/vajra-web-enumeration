"""
VAJRA - Professional HTML Report Generator
Usage: python3 report_generator.py <domain>
Auto-called by main.py after scan.
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
                     and not l.strip().startswith("WHOIS")]
        return lines[:limit] if limit else lines
    except:
        return []

def badge(text, color):
    c = {"green":("#00ff88","#001a0e"),"red":("#ff4444","#1a0000"),
         "yellow":("#ffcc00","#1a1300"),"blue":("#4488ff","#00001a"),
         "orange":("#ff8844","#1a0800"),"gray":("#888888","#111111")}
    fg,bg = c.get(color,c["gray"])
    return f"<span class='badge' style='background:{bg};color:{fg};border:1px solid {fg}'>{text}</span>"

def rows(items, limit=300):
    if not items: return "<tr><td class='empty'>No data found.</td></tr>"
    html = "".join(f"<tr><td class='mono'>{i}</td></tr>" for i in items[:limit])
    if len(items)>limit: html += f"<tr><td class='more'>... and {len(items)-limit} more</td></tr>"
    return html

def rows2(items, limit=300):
    if not items: return "<tr><td class='empty' colspan='2'>No data found.</td></tr>"
    html = ""
    for item in items[:limit]:
        p = item.split(":",1)
        html += f"<tr><td class='mono col1'>{p[0]}</td><td class='mono'>{p[1].strip() if len(p)>1 else ''}</td></tr>"
    if len(items)>limit: html += f"<tr><td class='more' colspan='2'>... and {len(items)-limit} more</td></tr>"
    return html

def port_rows(items, limit=300):
    if not items: return "<tr><td class='empty' colspan='2'>No data found.</td></tr>"
    html = ""
    for item in items[:limit]:
        if ":" in item:
            host,port = item.rsplit(":",1)
            html += f"<tr><td class='mono'>{host}</td><td class='mono'>{port}</td></tr>"
        else:
            html += f"<tr><td class='mono' colspan='2'>{item}</td></tr>"
    if len(items)>limit: html += f"<tr><td class='more' colspan='2'>... and {len(items)-limit} more</td></tr>"
    return html

def generate_report(domain):
    base = f"output/{domain}"
    now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subdomains = read_file(f"{base}/final_subdomains.txt")
    live_hosts = read_file(f"{base}/live_subdomains.txt")
    endpoints  = read_file(f"{base}/all_endpoints.txt")
    ports      = read_file(f"{base}/open_ports.txt")
    techs      = read_file(f"{base}/technologies.txt")

    ss_dir = f"{base}/screenshots"
    ss_html = ""
    ss_count = 0
    if os.path.exists(ss_dir):
        for root,_,files in os.walk(ss_dir):
            for fname in files:
                if fname.endswith(".png"):
                    ss_count += 1
                    try:
                        with open(os.path.join(root,fname),"rb") as f:
                            enc = base64.b64encode(f.read()).decode()
                        label = fname.replace(".png","")[:50]
                        ss_html += f'<div class="ss-card"><img src="data:image/png;base64,{enc}" loading="lazy"/><div class="ss-label">{label}</div></div>'
                    except: pass
    if not ss_html: ss_html = "<p class='empty-msg'>No screenshots captured.</p>"

    nav_sections = [
        ("overview","📊 Overview"),("subdomains","🔍 Subdomains"),
        ("live","🌐 Live Hosts"),("endpoints","🗺️ Endpoints"),
        ("ports","🔌 Ports"),("tech","🧠 Technologies"),("screenshots","📸 Screenshots"),
    ]
    nav = "".join(f'<a href="#{s}" class="nav-link">{l}</a>' for s,l in nav_sections)

    HTML = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VAJRA Report — {domain}</title>
<style>
:root{{--bg:#0d1117;--bg2:#161b22;--bg3:#1c2128;--border:#30363d;--accent:#f0883e;--green:#00ff88;--red:#ff4444;--blue:#4488ff;--text:#c9d1d9;--muted:#8b949e;--font:'Courier New',monospace;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);display:flex;min-height:100vh;}}
.sidebar{{width:210px;min-height:100vh;background:var(--bg2);border-right:1px solid var(--border);position:fixed;top:0;left:0;overflow-y:auto;z-index:100;}}
.logo{{padding:16px;border-bottom:1px solid var(--border);text-align:center;}}
.logo-text{{color:var(--accent);font-size:18px;font-weight:bold;letter-spacing:3px;}}
.logo-sub{{color:var(--muted);font-size:9px;margin-top:4px;}}
.logo-meta{{color:var(--muted);font-size:10px;margin-top:8px;line-height:1.7;}}
.nav-link{{display:block;padding:9px 18px;color:var(--muted);text-decoration:none;font-size:11px;border-left:3px solid transparent;transition:all .15s;}}
.nav-link:hover{{color:var(--accent);border-left-color:var(--accent);background:rgba(240,136,62,.06);}}
.main{{margin-left:210px;padding:28px 32px;width:100%;}}
.page-header{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:22px 26px;margin-bottom:20px;}}
.page-header h1{{color:var(--accent);font-size:18px;margin-bottom:6px;}}
.page-header .meta{{color:var(--muted);font-size:11px;line-height:2;}}
.stats-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px;}}
.stat-card{{background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;}}
.stat-card:hover{{border-color:var(--accent);}}
.stat-icon{{font-size:18px;margin-bottom:6px;}}
.stat-num{{font-size:24px;font-weight:bold;margin-bottom:3px;}}
.stat-label{{color:var(--muted);font-size:10px;}}
.section{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;margin-bottom:18px;overflow:hidden;}}
.section-header{{padding:12px 20px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;background:var(--bg3);}}
.section-header h2{{font-size:13px;color:var(--accent);}}
.section-body{{padding:16px 20px;}}
table{{width:100%;border-collapse:collapse;font-size:11px;}}
th{{background:var(--bg3);color:var(--muted);padding:8px 12px;text-align:left;border-bottom:1px solid var(--border);font-size:10px;}}
td{{padding:7px 12px;border-bottom:1px solid rgba(48,54,61,.4);}}
tr:hover td{{background:rgba(240,136,62,.03);}}
td.mono{{font-family:var(--font);word-break:break-all;}}
td.col1{{color:var(--muted);min-width:60px;}}
td.empty{{color:var(--muted);text-align:center;padding:16px;font-style:italic;}}
td.more{{color:var(--muted);text-align:center;font-style:italic;font-size:10px;padding:6px;}}
.badge{{padding:2px 9px;border-radius:20px;font-size:10px;font-weight:bold;display:inline-block;}}
.search-bar{{width:100%;background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:7px 12px;border-radius:5px;font-family:var(--font);font-size:11px;margin-bottom:12px;outline:none;}}
.search-bar:focus{{border-color:var(--accent);}}
.ss-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}}
.ss-card{{background:var(--bg3);border:1px solid var(--border);border-radius:7px;overflow:hidden;}}
.ss-card img{{width:100%;display:block;}}
.ss-label{{padding:6px 10px;font-size:10px;color:var(--muted);word-break:break-all;}}
.empty-msg{{color:var(--muted);font-size:11px;padding:16px;text-align:center;font-style:italic;}}
.footer{{text-align:center;color:var(--muted);font-size:10px;padding:20px 0 8px;border-top:1px solid var(--border);margin-top:8px;}}
</style></head><body>
<nav class="sidebar">
  <div class="logo">
    <div class="logo-text">⚡ VAJRA</div>
    <div class="logo-sub">WEB ENUMERATION</div>
    <div class="logo-meta">🎯 {domain}<br>📅 {now}<br>👤 {AUTHOR}</div>
  </div>
  {nav}
</nav>
<main class="main">
  <div id="overview" class="page-header">
    <h1>⚡ VAJRA Reconnaissance Report</h1>
    <div class="meta">
      🎯 Target &nbsp;: <strong style="color:var(--accent)">{domain}</strong><br>
      📅 Date &nbsp;&nbsp;&nbsp;: {now}<br>
      👤 Author &nbsp;: <strong style="color:var(--accent)">{AUTHOR}</strong><br>
      📋 Type &nbsp;&nbsp;&nbsp;: External Attack Surface Reconnaissance
    </div>
  </div>
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-icon">🔍</div><div class="stat-num" style="color:#4488ff">{len(subdomains)}</div><div class="stat-label">Subdomains</div></div>
    <div class="stat-card"><div class="stat-icon">🌐</div><div class="stat-num" style="color:#00ff88">{len(live_hosts)}</div><div class="stat-label">Live Hosts</div></div>
    <div class="stat-card"><div class="stat-icon">🗺️</div><div class="stat-num" style="color:#aa88ff">{len(endpoints)}</div><div class="stat-label">Endpoints</div></div>
    <div class="stat-card"><div class="stat-icon">🔌</div><div class="stat-num" style="color:#ffaa00">{len(ports)}</div><div class="stat-label">Open Ports</div></div>
    <div class="stat-card"><div class="stat-icon">🧠</div><div class="stat-num" style="color:#ff8844">{len(techs)}</div><div class="stat-label">Technologies</div></div>
  </div>
  <div id="subdomains" class="section">
    <div class="section-header"><h2>🔍 Subdomains</h2>{badge(f"{len(subdomains)} Found","blue")}</div>
    <div class="section-body">
      <input class="search-bar" placeholder="🔍 Filter subdomains..." oninput="filterTable(this,'sub-tbl')">
      <table id="sub-tbl"><tr><th>Subdomain</th></tr>{rows(subdomains)}</table>
    </div>
  </div>
  <div id="live" class="section">
    <div class="section-header"><h2>🌐 Live Hosts</h2>{badge(f"{len(live_hosts)} Live","green")}</div>
    <div class="section-body"><table><tr><th>Host</th></tr>{rows(live_hosts)}</table></div>
  </div>
  <div id="endpoints" class="section">
    <div class="section-header"><h2>🗺️ Endpoints</h2>{badge(f"{len(endpoints)} URLs","purple" if False else "orange")}</div>
    <div class="section-body">
      <input class="search-bar" placeholder="🔍 Filter endpoints..." oninput="filterTable(this,'ep-tbl')">
      <table id="ep-tbl"><tr><th>URL</th></tr>{rows(endpoints)}</table>
    </div>
  </div>
  <div id="ports" class="section">
    <div class="section-header"><h2>🔌 Open Ports</h2>{badge(f"{len(ports)} Found","orange")}</div>
    <div class="section-body"><table><tr><th>Host</th><th>Port</th></tr>{port_rows(ports)}</table></div>
  </div>
  <div id="tech" class="section">
    <div class="section-header"><h2>🧠 Technologies</h2>{badge(f"{len(techs)} Hosts","orange")}</div>
    <div class="section-body"><table><tr><th>Host + Technologies</th></tr>{rows(techs)}</table></div>
  </div>
  <div id="screenshots" class="section">
    <div class="section-header"><h2>📸 Screenshots</h2>{badge(f"{ss_count} Captured","green")}</div>
    <div class="section-body"><div class="ss-grid">{ss_html}</div></div>
  </div>
  <div class="footer">
    <p>⚡ <strong style="color:var(--accent)">VAJRA Web Enumeration Framework</strong> &nbsp;|&nbsp;
    👤 <strong style="color:var(--accent)">{AUTHOR}</strong> &nbsp;|&nbsp;
    <a href="{GITHUB}" style="color:var(--accent)">GitHub</a></p>
    <p style="margin-top:4px">⚠️ For authorized security testing only.</p>
  </div>
</main>
<script>
function filterTable(input,tableId){{
  const filter=input.value.toLowerCase();
  const rows=document.getElementById(tableId).getElementsByTagName('tr');
  for(let i=1;i<rows.length;i++){{
    rows[i].style.display=rows[i].textContent.toLowerCase().includes(filter)?'':'none';
  }}
}}
const sections=document.querySelectorAll('[id]');
const navLinks=document.querySelectorAll('.nav-link');
window.addEventListener('scroll',()=>{{
  let current='';
  sections.forEach(s=>{{if(window.scrollY>=s.offsetTop-100)current=s.id;}});
  navLinks.forEach(a=>{{
    const active=a.href.includes(current);
    a.style.color=active?'var(--accent)':'';
    a.style.borderLeftColor=active?'var(--accent)':'transparent';
  }});
}});
</script>
</body></html>"""

    out = f"{base}/vajra_report.html"
    os.makedirs(base, exist_ok=True)
    with open(out,"w",encoding="utf-8") as f: f.write(HTML)
    print(f"\n✅ Report saved: {out}")
    print(f"   Open: firefox {out} &")

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python3 report_generator.py <domain>")
        sys.exit(1)
    generate_report(sys.argv[1])
