import requests
import smtplib
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed
from apscheduler.schedulers.background import BackgroundScheduler

from src.config import  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, \
    MONITORED_URLS, ALERT_TO_EMAIL, CHECK_TIMEOUT, CHECK_INTERVAL


def send_alert(receiver, body):
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


def check_url(url):
    try:
        response = requests.get(url, timeout=CHECK_TIMEOUT)
        if response.status_code != 200:
            error = f"Error! Url [{url}] was down!!! Return status code is [{response.status_code}]."
            print(f"URL [{url}] return failed!")
            return error
        else:
            print(f"URL [{url}] return OK!")
            return None
    except Exception as e:
        error = f"Error! Url [{url}] failed with exception: {str(e)}"
        print(f"URL [{url}] failed with exception: {str(e)}")
        return error

def check_urls():
    errors = []
    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(check_url, url): url for url in MONITORED_URLS}
        for future in as_completed(future_to_url):
            error = future.result()
            if error:
                errors.append(error)

    if errors:
        body = '\n'.join(errors)
        send_alert(ALERT_TO_EMAIL, body)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_urls, 'interval', seconds=CHECK_INTERVAL)
    scheduler.start()
    
    # Run immediately on startup
    check_urls()
    
    print("Monitor started. Will run every 5 minutes.")
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Monitor stopped.")
