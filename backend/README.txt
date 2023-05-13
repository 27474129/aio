--- Migrations:
alembic upgrade head

--- Run app server:
gunicorn app:init_app --bind localhost:8000 --worker-class aiohttp.GunicornWebWorker --reload

--- To create new alembic migrations:
alembic revision --autogenerate -m "Revision message"
alembic upgrade head
