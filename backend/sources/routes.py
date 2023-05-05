from aiohttp import web

from sources.user.handlers import (
    create_user, get_user, delete_user, update_user
)
from sources.config import BASE_API_URL


def create_route(route: str) -> str:
    """Adding an API prefix."""
    return f'{BASE_API_URL}{route}'


routes = [
    # User actions
    web.get(create_route('user/{id}'), get_user),
    web.post(create_route('user'), create_user),
    web.delete(create_route('user/{id}'), delete_user),
    web.put(create_route('user/{id}'), update_user),
]


def get_routes(app: web.Application):
    app.add_routes(routes)
