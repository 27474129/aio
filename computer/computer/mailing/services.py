import smtplib
from email.mime.text import MIMEText

from computer.config import (
    EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
)


class MailingService:
    def get_msg(self) -> MIMEText:
        msg = MIMEText('Mailing')
        msg['Subject'] = 'Mail'
        msg['From'] = EMAIL_HOST_USER
        return msg

    def send_mail(self, to: str, msg: MIMEText):
        # TODO: Сейчас для каждого имейла происходит авторизация, пофиксить
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp_serv:
            smtp_serv.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            try:
                smtp_serv.sendmail(EMAIL_HOST_USER, to, msg.as_string())
            except smtplib.SMTPDataError:
                return False
            return True
