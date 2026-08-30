"""
VAJRA Resume System
===================
Tracks which stages completed.
Scan beech mein ruk jaye toh wahan se continue karo.
"""

import os
import json
import datetime

RESUME_DIR = os.path.expanduser("~/.vajra_resume")


def _resume_file(domain):
    safe = domain.replace(".", "_").replace("/", "_")
    return os.path.join(RESUME_DIR, f"{safe}.json")


def mark_done(domain, stage):
    """Mark a stage as completed."""
    os.makedirs(RESUME_DIR, exist_ok=True)
    path  = _resume_file(domain)
    data  = load_progress(domain)
    data["completed"][stage] = datetime.datetime.now().isoformat()
    data["domain"]           = domain
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def is_done(domain, stage):
    """Check if stage already completed."""
    return stage in load_progress(domain).get("completed", {})


def load_progress(domain):
    path = _resume_file(domain)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except:
            pass
    return {"domain": domain, "completed": {}}


def clear_progress(domain):
    path = _resume_file(domain)
    if os.path.exists(path):
        os.remove(path)


def show_progress(domain):
    data = load_progress(domain)
    completed = data.get("completed", {})
    return completed
