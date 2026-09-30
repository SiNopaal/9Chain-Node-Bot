"""
API Client for 9Chain API v2.
Handles authentication, requests, rate-limiting, and error handling.
"""
import json
import time
import urllib.request
import urllib.error
from config import BASE_API_URL, DEFAULT_HEADERS, TIMEOUT, MAX_RETRIES

class NineChainClient:
    def __init__(self, base_url=BASE_API_URL):
        self.base_url = base_url.rstrip("/")
        self.token = None

    def _request(self, method, path, body=None, token=None, retries=MAX_RETRIES):
        url = f"{self.base_url}{path}"
        headers = dict(DEFAULT_HEADERS)
        headers["x-device-id"] = f"h9c-{int(time.time())}"
        
        auth_token = token or self.token
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        data = json.dumps(body).encode("utf-8") if body is not None else None

        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    raw = resp.read()
                    res_json = json.loads(raw.decode("utf-8")) if raw else {}
                    return resp.status, res_json
            except urllib.error.HTTPError as e:
                # Handle Rate Limiting
                if e.code == 429:
                    wait_sec = 5 * (attempt + 1)
                    time.sleep(wait_sec)
                    continue
                try:
                    err_json = json.loads(e.read().decode("utf-8"))
                except Exception:
                    err_json = {"error": f"HTTP {e.code}"}
                return e.code, err_json
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                return 0, {"error": str(e)}
            except Exception as e:
                return 0, {"error": str(e)}

        return 0, {"error": "Max retries reached"}

    def login(self, email, password):
        """Authenticates with 9Chain and stores accessToken."""
        payload = {"email": email, "password": password}
        code, resp = self._request("POST", "/auth/login", body=payload)
        if code in (200, 201) and resp.get("success"):
            token = resp.get("data", {}).get("accessToken")
            self.token = token
            return True, token
        err_msg = resp.get("error", {}).get("message", "Login failed") if isinstance(resp.get("error"), dict) else str(resp.get("error", "Unknown error"))
        return False, err_msg

    def get_checkin_status(self):
        """Checks if today's checkin has already been claimed."""
        code, resp = self._request("GET", "/me/check-in")
        if code == 200 and resp.get("success"):
            return True, resp.get("data", {})
        return False, resp

    def claim_checkin(self):
        """Claims daily checkin reward."""
        code, resp = self._request("POST", "/me/check-in")
        if code in (200, 201) and resp.get("success"):
            reward = resp.get("data", {}).get("reward", 0)
            return True, reward
        return False, resp

    def get_program_state(self):
        """Fetches current player state (XP, tapsRemaining, nextTier, etc.)."""
        code, resp = self._request("GET", "/program/state")
        if code == 200 and resp.get("success"):
            return True, resp.get("data", {})
        return False, resp

    def tap(self, count):
        """Sends batch tap request."""
        payload = {"count": count}
        code, resp = self._request("POST", "/program/tap", body=payload)
        if code in (200, 201) and resp.get("success"):
            data = resp.get("data", {})
            return True, data
        return False, resp

    def upgrade_node_tier(self, to_tier):
        """Upgrades node tier."""
        payload = {"toTier": to_tier}
        code, resp = self._request("POST", "/program/node/upgrade", body=payload)
        if code in (200, 201) and resp.get("success"):
            return True, resp.get("data", {})
        return False, resp

    def get_catalog(self):
        """Fetches components catalog with upgrades and costs."""
        code, resp = self._request("GET", "/program/catalog")
        if code == 200 and resp.get("success"):
            return True, resp.get("data", {})
        return False, resp

    def upgrade_component(self, component_key, to_level):
        """Upgrades a specific component."""
        payload = {"componentKey": component_key, "toLevel": to_level}
        code, resp = self._request("POST", "/program/upgrade", body=payload)
        if code in (200, 201) and resp.get("success"):
            return True, resp.get("data", {})
        return False, resp
