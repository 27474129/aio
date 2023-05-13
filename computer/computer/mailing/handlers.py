import pika
import requests

from computer.base.handlers import BaseView
from computer.config import BACKEND_HOST, BACKEND_PORT
from computer.base.utils import backend_auth
from computer.mailing.tasks import mailing_task


class MailingView(BaseView):
    methods = ('OPTIONS', 'GET', 'POST')

    def get(self):
        # TODO: Delete test method
        conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = conn.channel()
        channel.queue_declare(queue='mailing')
        channel.basic_publish(exchange='',
                              routing_key='mailing',
                              body='Hello World!')
        conn.close()
        return 'asd'

    def post(self):
        # TODO: Сделать возможность планировать рассылку
        jwt_token = backend_auth()
        headers = {
            'Authorization': f'Token {jwt_token}'
        }
        response = requests.get(
            f'{BACKEND_HOST}:{BACKEND_PORT}/api/user', headers=headers
        ).json()

        emails = []
        for row in response['rows']:
            emails.append(row['email'])

        mailing_task.delay(emails)

        return 'Mailing started successfully'
