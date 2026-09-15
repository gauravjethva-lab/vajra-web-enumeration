import os
import re
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed


# Secret patterns to search in JS files
SECRET_PATTERNS = [
    (r'api[_-]?key[\s]*[=:]+[\s]*["\']([A-Za-z0-9_\-]{20,})',   "API Key"),
    (r'secret[\s]*[=:]+[\s]*["\']([A-Za-z0-9_\-]{20,})',        "Secret"),
    (r'token[\s]*[=:]+[\s]*["\']([A-Za-z0-9_\-\.]{20,})',       "Token"),
    (r'password[\s]*[=:]+[\s]*["\']([^\'"]{8,})',                "Password"),
    (r'(AKIA[0-9A-Z]{16})',                                       "AWS Key"),
    (r'([0-9a-f]{40})',                                           "Possible Hash/Token"),
]


def fetch_url(url, timeout=8):
    """Fetch URL content safely."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 VAJRA-Scanner"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(50000).decode("utf-8", errors="ignore")
    except Exception:
        return None


def check_cors(url):
    """Check for CORS misconfiguration on a URL."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 VAJRA-Scanner",
                "Origin": "https://evil.com",
            }
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            acao = r.headers.get("Access-Control-Allow-Origin", "")
            acac = r.headers.get("Access-Control-Allow-Credentials", "")
            if acao == "*":
                return f"[WILDCARD CORS] {url} → ACAO: *"
            elif "evil.com" in acao:
                if acac.lower() == "true":
                    return f"[CRITICAL CORS+CREDS] {url} → Reflects origin + credentials!"
                return f"[CORS REFLECT] {url} → Reflects arbitrary origin"
    except urllib.error.HTTPError as e:
        # Still check headers on error responses
        try:
            acao = e.headers.get("Access-Control-Allow-Origin", "")
            if "evil.com" in acao:
                return f"[CORS REFLECT on {e.code}] {url}"
        except Exception:
            pass
    except Exception:
        pass
    return None


def scan_js_secrets(js_url):
    """Scan a JS file for secrets."""
    content = fetch_url(js_url)
    if not content:
        return []
    findings = []
    for pattern, label in SECRET_PATTERNS:
        try:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches[:2]:
                val = match if isinstance(match, str) else match[0]
                if len(val) > 6:
                    findings.append(f"[{label}] {js_url} → {val[:60]}")
        except Exception:
            pass
    return findings


def run_js_cors_check(domain):
    endpoints_file = f"output/{domain}/all_endpoints.txt"
    live_file      = f"output/{domain}/live_subdomains.txt"
    js_output      = f"output/{domain}/js_findings.txt"
    cors_output    = f"output/{domain}/cors_issues.txt"

    print("\n[+] Running JS Secret Scan + CORS Check...")

    js_urls   = []
    live_urls = []

    # Get JS URLs from endpoints
    if os.path.exists(endpoints_file):
        try:
            with open(endpoints_file) as f:
                for line in f:
                    line = line.strip()
                    if line.endswith(".js") and line.startswith("http"):
                        js_urls.append(line)
        except Exception as e:
            print(f"[-] Error reading endpoints: {e}")

    # Get live URLs for CORS check
    if os.path.exists(live_file):
        try:
            with open(live_file) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    url = line.split()[0]
                    if url.startswith("http"):
                        live_urls.append(url)
        except Exception as e:
            print(f"[-] Error reading live hosts: {e}")

    # JS Secret Scan (parallel, max 40 files)
    js_findings = []
    if js_urls:
        print(f"[+] Scanning {min(len(js_urls), 40)} JS files for secrets...")
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = {ex.submit(scan_js_secrets, url): url for url in js_urls[:40]}
            for future in as_completed(futures):
                try:
                    findings = future.result()
                    js_findings.extend(findings)
                except Exception:
                    pass
    else:
        print("[!] No JS files found in endpoints.")

    # CORS Check (parallel, max 20 hosts)
    cors_issues = []
    if live_urls:
        print(f"[+] Checking {min(len(live_urls), 20)} hosts for CORS issues...")
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = {ex.submit(check_cors, url): url for url in live_urls[:20]}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        cors_issues.append(result)
                except Exception:
                    pass
    else:
        print("[!] No live hosts for CORS check.")

    # Save JS findings
    try:
        with open(js_output, "w") as f:
            if js_findings:
                for finding in js_findings:
                    f.write(finding + "\n")
            else:
                f.write("No secrets detected in JS files.\n")
    except Exception as e:
        print(f"[-] Error saving JS findings: {e}")

    # Save CORS findings
    try:
        with open(cors_output, "w") as f:
            if cors_issues:
                for issue in cors_issues:
                    f.write(issue + "\n")
            else:
                f.write("No CORS misconfigurations detected.\n")
    except Exception as e:
        print(f"[-] Error saving CORS findings: {e}")

    # Display results
    if js_findings:
        print(f"[!] JS Secrets Found: {len(js_findings)}")
        for f in js_findings[:3]:
            print(f"    {f}")
    else:
        print("[+] JS Scan: No secrets detected")

    if cors_issues:
        print(f"[!] CORS Issues: {len(cors_issues)}")
        for c in cors_issues:
            print(f"    {c}")
    else:
        print("[+] CORS Check: No issues detected")

    print(f"[+] JS findings → {js_output}")
    print(f"[+] CORS results → {cors_output}")
