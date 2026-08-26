#!/usr/bin/env bash
#
# VAJRA - One-shot bootstrap installer
# =====================================
# Unzip karne ke baad sirf ye chalao:
#
#     bash install.sh
#
# Ye script:
#   1. python3 + pip present hona confirm karta hai
#   2. rich/pyfiglet install karta hai (banner ke liye zaroori)
#   3. main.py run karta hai, jo aage khud saare recon tools
#      (subfinder, amass, httpx, naabu, masscan, whatweb,
#      katana, gau, waybackurls) check/install karta hai.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "\033[1;36m[*] VAJRA Bootstrap Starting...\033[0m"

# ---------------------------------------------------------
# 1. Ensure python3 + pip
# ---------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo -e "\033[1;33m[!] python3 not found. Installing...\033[0m"
    sudo apt-get update -y
    sudo apt-get install -y python3
fi

if ! command -v pip3 >/dev/null 2>&1; then
    echo -e "\033[1;33m[!] pip3 not found. Installing...\033[0m"
    sudo apt-get install -y python3-pip
fi

# ---------------------------------------------------------
# 2. Ensure Python packages needed just to boot (banner UI)
# ---------------------------------------------------------

echo -e "\033[1;36m[*] Installing Python dependencies (rich, pyfiglet)...\033[0m"

pip3 install --break-system-packages -r requirements.txt \
    || pip3 install --user --break-system-packages -r requirements.txt

# ---------------------------------------------------------
# 3. Make sure PATH includes go bin (for already-installed tools)
# ---------------------------------------------------------

export PATH="$PATH:$HOME/go/bin:/usr/local/go/bin"

# ---------------------------------------------------------
# 4. Launch VAJRA
#    main.py khud age se baaki tools (subfinder, amass, httpx,
#    naabu, masscan, whatweb, katana, gau, waybackurls) check
#    karke missing wale install kar lega.
# ---------------------------------------------------------

echo -e "\033[1;32m[+] Bootstrap complete. Launching VAJRA...\033[0m\n"

python3 main.py
