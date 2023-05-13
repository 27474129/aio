from typing import List

from celery_ import celery_app


@celery_app.task
def mailing_task(emails_list: List[str]):
    ...
