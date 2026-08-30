"""
VAJRA Cache System
==================
Saves scan results per domain + stage.
Same domain dobara scan karo — cached stages skip ho jaate hain.
"""

import os
import json
import hashlib
import datetime

CACHE_DIR = os.path.expanduser("~/.vajra_cache")


def _cache_file(domain, stage):
    safe = hashlib.md5(domain.encode()).hexdigest()[:8]
    return os.path.join(CACHE_DIR, f"{safe}_{stage}.json")


def cache_exists(domain, stage, max_age_hours=24):
    """Returns True if valid cache exists for this domain+stage."""
    path = _cache_file(domain, stage)
    if not os.path.exists(path):
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        saved = datetime.datetime.fromisoformat(data["timestamp"])
        age   = (datetime.datetime.now() - saved).total_seconds() / 3600
        return age < max_age_hours
    except:
        return False


def save_cache(domain, stage, result_files):
    """Cache metadata for completed stage."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = _cache_file(domain, stage)
    data = {
        "domain":    domain,
        "stage":     stage,
        "timestamp": datetime.datetime.now().isoformat(),
        "files":     result_files,
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def clear_cache(domain=None):
    """Clear cache for a domain or all domains."""
    if not os.path.exists(CACHE_DIR):
        return
    for f in os.listdir(CACHE_DIR):
        if f.endswith(".json"):
            os.remove(os.path.join(CACHE_DIR, f))


def get_cache_info(domain):
    """Return list of cached stages for a domain."""
    stages = ["whois","dns","subdomains","live","endpoints","ports","tech","takeover","screenshots"]
    cached = []
    for stage in stages:
        if cache_exists(domain, stage):
            cached.append(stage)
    return cached
