import logging
import json

import requests_async as requests
from aiohttp import WSMsgType
from aiohttp import web

from backend.base.handlers import BaseView
from backend.base.utils import auth_required
from backend.auth.services import AuthService
from backend.config import HOST, PORT
from backend.constants import OK_CODE
from backend.websocket.enums import Status


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

                if response.status_code != OK_CODE:
                    await ws.send_str(Status.failed)
                    logger.info('Failed to send message')
                    continue
                logger.info('Sended message')
                await ws.send_str(Status.sended)
        return ws
