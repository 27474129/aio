from aiohttp import WSMsgType
from aiohttp import web

from sources.base.handlers import BaseView
from sources.base.utils import auth_required


class WebsocketHandlerHandler(BaseView):
    allowed_methods = ('OPTIONS', 'GET')

    @auth_required
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = msg.data
                data = data.strip()
                if 'close' == data:
                    await ws.close()
                    print('closed')
                    return ws
                print('ok')
                await ws.send_str(data + 'answer')
        return ws
