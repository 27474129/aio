from celery import Celery

from computer.config import CELERY_CONFIG_PATH, CELERY_NAMESPACE


app = Celery('celery_')
app.config_from_object(CELERY_CONFIG_PATH, namespace=CELERY_NAMESPACE)
app.autodiscover_tasks()
