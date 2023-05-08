import logging
import json

import requests_async as requests
from aiohttp import WSMsgType
from aiohttp import web

from sources.base.handlers import BaseView
from sources.base.utils import auth_required
from sources.auth.services import AuthService
from sources.config import HOST, PORT


logger = logging.getLogger(__name__)


class ChatWebsocketHandler(BaseView):
    allowed_methods = ('OPTIONS', 'GET')

    @auth_required
    async def get(self):
        token = self.request.headers['Authorization'].split()[1]
        payload = AuthService().decode_token(token)
        to = self.request.match_info['to']

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        logger.info('Connected to websocket')

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                msg = msg.data.strip()
                if 'close' == msg:
                    logger.info('Connection closed')
                    await ws.close()
                    return ws

                body = {'to': int(to), 'by': payload['uid'], 'text': msg}
                response = await requests.post(
                    f'{HOST}:{PORT}/api/message',
                    data=json.dumps(body),
                    headers={'Authorization': f'Token {token}'}
                )

                if response.status_code != 200:
                    await ws.send_str('failed')
                    logger.info('Failed to send message')
                    continue
                logger.info('Sended message')
                await ws.send_str('sended')
        return ws
