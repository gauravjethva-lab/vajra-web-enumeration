"""
VAJRA Google Dorking
====================
Generates targeted Google dork queries for manual use.
Also uses duckduckgo-search if available for auto results.
"""

import os
import urllib.parse
from rich.console import Console

console = Console()

DORK_TEMPLATES = [
    ('Login/Admin Pages',    'site:{domain} inurl:admin OR inurl:login OR inurl:dashboard'),
    ('Config Files',         'site:{domain} ext:conf OR ext:config OR ext:cfg OR ext:env'),
    ('Backup Files',         'site:{domain} ext:bak OR ext:backup OR ext:old OR ext:zip'),
    ('Database Files',       'site:{domain} ext:sql OR ext:db OR ext:sqlite'),
    ('Log Files',            'site:{domain} ext:log'),
    ('API Keys Exposed',     'site:{domain} intext:"api_key" OR intext:"api_secret" OR intext:"access_token"'),
    ('Error Pages',          'site:{domain} intext:"error" OR intext:"exception" OR intext:"stack trace"'),
    ('Open Directories',     'site:{domain} intitle:"index of" OR intitle:"directory listing"'),
    ('Exposed Git',          'site:{domain} inurl:.git'),
    ('Sensitive Params',     'site:{domain} inurl:id= OR inurl:user= OR inurl:token= OR inurl:key='),
    ('Exposed Credentials',  'site:{domain} intext:"password" OR intext:"username" filetype:txt'),
    ('S3/Cloud Storage',     'site:s3.amazonaws.com "{domain}"'),
    ('Pastebin Leaks',       'site:pastebin.com "{domain}"'),
    ('GitHub Code Leaks',    'site:github.com "{domain}" password OR secret OR token'),
    ('Subdomains (CT logs)', 'site:crt.sh "{domain}"'),
    ('Trello Boards',        'site:trello.com "{domain}"'),
    ('JIRA/Confluence',      'site:atlassian.net "{domain}"'),
    ('Swagger/API Docs',     'site:{domain} inurl:swagger OR inurl:api-docs OR inurl:openapi'),
    ('phpinfo Exposed',      'site:{domain} inurl:phpinfo.php'),
    ('XML/JSON Exposed',     'site:{domain} ext:xml OR ext:json inurl:config'),
]


def generate_dorks(domain):
    output_file = f"output/{domain}/google_dorks.txt"
    html_file   = f"output/{domain}/google_dorks.html"

    print("\n[+] Generating Google Dork Queries...")

    dorks = []
    for label, template in DORK_TEMPLATES:
        query = template.replace("{domain}", domain)
        url   = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        dorks.append((label, query, url))

    # Save plain text
    with open(output_file, "w") as f:
        f.write(f"Google Dork Queries — {domain}\n")
        f.write("=" * 60 + "\n\n")
        for label, query, url in dorks:
            f.write(f"[{label}]\n")
            f.write(f"Query: {query}\n")
            f.write(f"URL:   {url}\n\n")

    # Save clickable HTML
    rows = ""
    for label, query, url in dorks:
        rows += f"""
        <tr>
            <td>{label}</td>
            <td class="mono">{query}</td>
            <td><a href="{url}" target="_blank" class="btn">Search</a></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>VAJRA Dorks — {domain}</title>
<style>
body{{background:#0d1117;color:#c9d1d9;font-family:'Courier New',monospace;padding:30px;}}
h1{{color:#f0883e;margin-bottom:20px;}}
table{{width:100%;border-collapse:collapse;}}
th{{background:#161b22;color:#8b949e;padding:10px;text-align:left;border-bottom:1px solid #30363d;}}
td{{padding:10px;border-bottom:1px solid #21262d;vertical-align:top;}}
td.mono{{font-size:11px;color:#79c0ff;word-break:break-all;}}
a.btn{{background:#f0883e;color:#000;padding:4px 12px;border-radius:4px;text-decoration:none;font-size:11px;font-weight:bold;}}
a.btn:hover{{background:#e07020;}}
</style>
</head><body>
<h1>⚡ VAJRA — Google Dorks</h1>
<p style="color:#8b949e;margin-bottom:20px;">Target: <strong style="color:#f0883e">{domain}</strong> — {len(dorks)} queries generated</p>
<table>
<tr><th>Category</th><th>Dork Query</th><th>Action</th></tr>
{rows}
</table>
<p style="color:#8b949e;margin-top:20px;font-size:11px;">⚠️ For authorized security testing only — Gaurav Jethva</p>
</body></html>"""

    with open(html_file, "w") as f:
        f.write(html)

    console.print(f"[bold green][✓] Generated {len(dorks)} dork queries[/bold green]")
    console.print(f"[white]    Text  → {output_file}[/white]")
    console.print(f"[white]    HTML  → {html_file} (clickable links)[/white]")

    # Show top 5
    console.print(f"\n[cyan]    Sample dorks:[/cyan]")
    for label, query, _ in dorks[:5]:
        console.print(f"[dim]    [{label}] {query}[/dim]")
