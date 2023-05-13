from aiohttp import web

from backend.routes import get_routes


app = web.Application(debug=True)
get_routes(app)
web.run_app(app, port=8000)
