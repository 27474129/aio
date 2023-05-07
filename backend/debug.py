from aiohttp import web

from sources.routes import get_routes


app = web.Application(debug=True)
get_routes(app)
web.run_app(app, port=8090)
