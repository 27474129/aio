from aiohttp import web

from sources.user.handlers import UserHandler, UserCreationHandler
from sources.message.handlers import MessageHandler
from sources.auth.handlers import AuthHandler
from sources.websocket.handlers import ChatWebsocketHandler
from sources.config import BASE_API_URL


def create_route(route: str) -> str:
    """Adding an API prefix."""
    return f'{BASE_API_URL}{route}'


routes = [
    # User actions
    web.view(create_route('user/{id}'), UserHandler),
    web.view(create_route('user'), UserCreationHandler),

    # Auth actions
    web.post(create_route('auth'), AuthHandler),

    # Message actions
    web.post(create_route('message'), MessageHandler),

    # Websockets
    web.get(create_route('ws/{to}'), ChatWebsocketHandler),
]


def get_routes(app: web.Application):
    app.add_routes(routes)
