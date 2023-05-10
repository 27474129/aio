import smtplib
from email.mime.text import MIMEText

import pika

from computer.base.handlers import BaseView
from computer.config import (
    EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
)


class MailingView(BaseView):
    methods = ('OPTIONS', 'GET', 'POST')

    def _get(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = conn.channel()
        channel.queue_declare(queue='mailing')
        channel.basic_publish(exchange='',
                              routing_key='mailing',
                              body='Hello World!')
        conn.close()
        return 'asd'

    def _post(self):
        to = 'harlanvova15@gmail.com'

        msg = MIMEText('Test mailing')
        msg['Subject'] = 'Test mail'
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = to

        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp_serv:
            smtp_serv.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp_serv.sendmail(EMAIL_HOST_USER, to, msg.as_string())
        return 'Mail successfully sent'
