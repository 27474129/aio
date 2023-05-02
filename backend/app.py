from aiohttp import web
from swagger_ui import api_doc

from sources.routes import get_routes
from sources.config import BASE_API_URL


async def init_app():
    app = web.Application(debug=True)
    get_routes(app)
    api_doc(
        app, config_path='./swagger.yaml', url_prefix=f'{BASE_API_URL}docs',
        title='API docs'
    )
    return app
