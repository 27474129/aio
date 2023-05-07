from aiohttp import web

from sources.user.handlers import UserHandler, UserCreationHandler
from sources.message.handlers import create_message
from sources.auth.handlers import auth
from sources.config import BASE_API_URL


def create_route(route: str) -> str:
    """Adding an API prefix."""
    return f'{BASE_API_URL}{route}'


routes = [
    # User actions
    web.view(create_route('user/{id}'), UserHandler),
    web.view(create_route('user'), UserCreationHandler),

    # TODO: Переписать на ООП
    # Auth actions
    web.post(create_route('auth'), auth),

    # TODO: Переписать на ООП
    # Message actions
    web.post(create_route('message'), create_message),
]


def get_routes(app: web.Application):
    app.add_routes(routes)
