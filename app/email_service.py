import smtplib
from email.message import EmailMessage
from config import Config


def send_email(to_address, subject, body):
    """Send a plain text email using Gmail SMTP."""
    message = EmailMessage()
    message["From"] = Config.MAIL_SENDER
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(Config.MAIL_SENDER, Config.MAIL_APP_PASSWORD)
        server.send_message(message)