import smtplib
from email.message import EmailMessage
from utils.constant import SMTP_SERVER_ADDRESS, SMTP_PORT, SMTP_MAIL_ADDRESS, SMTP_PASSWORD, FRONTEND_HOST

def send_preregister_mail(To: str, signUpToken: str):
    msg = EmailMessage()
    msg['To'] = To
    msg['From'] = SMTP_MAIL_ADDRESS
    msg['Subject'] = "[See A Scale] 회원가입 이메일 인증"
    url = f"{FRONTEND_HOST}/signup?pretoken={signUpToken}"
    msg.set_content(url)
    html_content = f"""<html><body><p>See A Scale의 회원가입을 원하신다면 아래 '회원가입'을 눌러주세요!</p><a href="{url}">회원가입</a></body></html>"""
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL(SMTP_SERVER_ADDRESS, SMTP_PORT) as server:
        server.login(SMTP_MAIL_ADDRESS, SMTP_PASSWORD)
        server.send_message(msg)
