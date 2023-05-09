from aiohttp import web

from backend.user.handlers import UserDetailHandler, UserHandler
from backend.message.handlers import MessageHandler
from backend.auth.handlers import AuthHandler
from backend.websocket.handlers import ChatWebsocketHandler
from backend.config import BASE_API_URL
from backend.notification.handlers import NotificationHandler


def create_route(route: str) -> str:
    """Adding an API prefix."""
    return f'{BASE_API_URL}{route}'


routes = [
    # User actions
    web.view(create_route('user/{id}'), UserDetailHandler),
    web.view(create_route('user'), UserHandler),

    # Auth actions
    web.post(create_route('auth'), AuthHandler),

    # Message actions
    web.post(create_route('message'), MessageHandler),

    # Notification actions
    web.view(create_route('notification'), NotificationHandler),

    # Websockets
    web.get(create_route('ws/{to}'), ChatWebsocketHandler),
]


def get_routes(app: web.Application):
    app.add_routes(routes)
