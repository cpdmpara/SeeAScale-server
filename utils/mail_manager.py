import smtplib
from email.message import EmailMessage
from utils.constant import SMTP_SERVER, SMTP_PORT, SMTP_SERVER_MAIL, SMTP_PASSWORD, SMTP_MAIL_TITLE

def send_preregister_mail(To: str, Message: str):
    msg = EmailMessage()
    msg.set_content(Message)
    msg['To'] = To
    msg['From'] = SMTP_SERVER_MAIL
    msg['Subject'] = SMTP_MAIL_TITLE

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_SERVER_MAIL, SMTP_PASSWORD)
        server.send_message(msg)
