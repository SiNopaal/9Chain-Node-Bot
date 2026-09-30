"""
Configuration module for 9Chain Automation Bot.
Handles loading environment variables, default settings, and accounts.
"""
import os
import sys

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")
ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.txt")

def load_env_file():
    """Simple parser for .env file without external dependencies."""
    if not os.path.exists(ENV_FILE):
        return
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())
    except Exception as e:
        print(f"[!] Warning reading .env: {e}")

load_env_file()

# API Configuration
BASE_API_URL = os.environ.get("BASE_API_URL", "https://api.9chain.com/v2")
DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD", "Naufal123")

# Bot Execution Settings
TAP_BATCH_SIZE = int(os.environ.get("TAP_BATCH_SIZE", 500))
DELAY_BETWEEN_ACCOUNTS = float(os.environ.get("DELAY_BETWEEN_ACCOUNTS", 2.0))
LOOP_REST_MINUTES = int(os.environ.get("LOOP_REST_MINUTES", 60))
AUTO_UPGRADE_TIER = os.environ.get("AUTO_UPGRADE_TIER", "true").lower() in ("true", "1", "yes")
AUTO_UPGRADE_COMPONENTS = os.environ.get("AUTO_UPGRADE_COMPONENTS", "true").lower() in ("true", "1", "yes")
RESERVE_TIER_COST = os.environ.get("RESERVE_TIER_COST", "true").lower() in ("true", "1", "yes")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 3))
TIMEOUT = int(os.environ.get("TIMEOUT", 15))

# Common HTTP Headers
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://www.9chain.com",
    "Referer": "https://www.9chain.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def load_accounts(file_path=ACCOUNTS_FILE):
    """
    Loads accounts from accounts.txt.
    Supports lines formatted as 'email:password' or simply 'email' (uses DEFAULT_PASSWORD).
    """
    if not os.path.exists(file_path):
        print(f"[!] File akun tidak ditemukan: {file_path}")
        return []
    
    accounts = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if ":" in line:
                parts = line.split(":", 1)
                email = parts[0].strip()
                password = parts[1].strip()
            else:
                email = line.strip()
                password = DEFAULT_PASSWORD
                
            if "@" in email:
                accounts.append({"email": email, "password": password})
            else:
                print(f"[!] Baris {line_num} dilewati (format email tidak valid): {line}")

    return accounts
