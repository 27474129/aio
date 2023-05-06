ASYNC_POSTGRES_CONN_STRING = 'postgresql+asyncpg://postgres@localhost/aio'
SYNC_POSTGRES_CONN_STRING = 'postgresql://postgres@localhost/aio'

BASE_API_URL = '/api/'

LOGGING_FORMAT = '%(asctime)s - [%(levelname)s] - %(name)s - ' \
                 '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

JWT_SECRET = 'as9erdfgfd9hg3e59vsdfogvdfk'
JWT_ALGORITHM = 'HS256'
