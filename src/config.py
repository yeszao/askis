import os
from pathlib import Path

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))
CHECK_TIMEOUT = int(os.getenv("CHECK_TIMEOUT", 7))

ROOT_DIR =  Path(__file__).parent.parent
MONITORED_URLS = ROOT_DIR.joinpath("monitored_urls.txt").read_text().split()
LOGS_DIR = ROOT_DIR.joinpath("logs")

LOGS_DIR.mkdir(exist_ok=True)

ALERT_TO_EMAIL = os.getenv("ALERT_TO_EMAIL")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_PASS")
SMTP_PASS = os.getenv("SMTP_PASS")

