--- Migrations:
alembic upgrade head
P.S. Before migrations you need to create local db: aio

--- Run app server:
gunicorn app:init_app --bind localhost:8000 --worker-class aiohttp.GunicornWebWorker --reload

--- To create new alembic migrations:
alembic revision --autogenerate -m "Revision message"
alembic upgrade head
