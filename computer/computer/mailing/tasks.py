from typing import List

from celery_ import celery_app

from computer.mailing.services import MailingService


@celery_app.task
def mailing_task(emails_list: List[str]):
    # TODO: Add logging in celery tasks
    mailing_serv = MailingService()
    msg = mailing_serv.get_msg()
    for email in emails_list:
        msg['To'] = email
        mail = mailing_serv.send_mail(to=email, msg=msg)
        if not mail:
            # Logging here
            continue
        # Logging here
