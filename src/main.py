import requests
import smtplib
from email.mime.text import MIMEText

from src.config import  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, \
    MONITORED_URLS, ALERT_TO_EMAIL, CHECK_TIMEOUT


def send_alert(receiver, errors):
    body = '\n'.join(errors)
    msg = MIMEText(body)

    msg['Subject'] = "Website Monitor Alert"
    msg['From'] = SMTP_USER
    msg['To'] = receiver
    
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


def check_urls():
    errors = []
    for url in MONITORED_URLS:
        response = requests.get(url, timeout=CHECK_TIMEOUT)
        if response.status_code != 200:
            errors.append(f"Error! Url [{url}] was down!!! Return status code is [{response.status_code}].")
            print(f"URL [{url}] return failed!")
        else:
            print(f"URL [{url}] return OK!")

    return errors


if __name__ == '__main__':
    errors = check_urls()
    if errors:
       send_alert(ALERT_TO_EMAIL, errors)

    print("Monitor runned done.")

