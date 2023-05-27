POSTGRES_USER = 'aiopostgres'
POSTGRES_PASS = 'sdfjuhSDt43'
POSTGRES_HOST = 'localhost'
POSTGRES_DB = 'aio'
POSTGRES_PORT = 5432

ASYNC_POSTGRES_CONN_STRING = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}' \
                             f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
SYNC_POSTGRES_CONN_STRING = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}' \
                            f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

BASE_API_URL = '/api/'

LOGGING_FORMAT = '%(asctime)s - [%(levelname)s] - %(name)s - ' \
                 '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

JWT_SECRET = 'as9erdfgfd9hg3e59vsdfogvdfk'
JWT_ALGORITHM = 'HS256'

HOST = 'http://127.0.0.1'
PORT = 8000
