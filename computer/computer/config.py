EMAIL_HOST = "smtp.yandex.ru"
EMAIL_HOST_USER = 'milogt8@yandex.ru'
EMAIL_HOST_PASSWORD = 'Harlan483'
EMAIL_PORT = 465


RABBIT_MQ_USER = 'guest'
RABBIT_MQ_PASS = 'guest'
RABBIT_MQ_HOST = 'localhost'
RABBIT_MQ_PORT = 5672
RABBIT_MQ_CONN_STRING = f'amqp://{RABBIT_MQ_USER}:{RABBIT_MQ_PASS}' \
                        f'@{RABBIT_MQ_HOST}:{RABBIT_MQ_PORT}//'

CELERY_CONFIG_PATH = 'celery_.celery_settings'
CELERY_NAMESPACE = 'CELERY'


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB_NUMBER_FOR_CELERY = 0
REDIS_CONN_STRING = f'redis://{REDIS_HOST}:{REDIS_PORT}' \
                    f'/{REDIS_DB_NUMBER_FOR_CELERY}'

HOST = 'http://127.0.0.1'
PORT = 5003

BACKEND_HOST = 'http://127.0.0.1'
BACKEND_PORT = 8000

BACKEND_EMAIL = 'harlanvova03@gmail.com'
BACKEND_PASSWORD = 'Harlan483!'
