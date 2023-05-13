from celery import Celery


app = Celery('celery_', broker='amqp://guest@localhost//')


@app.task
def add(x):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f'SUCCESS: {x}')
    return x

