import logging

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from sources.base.utils import (
    serialize_response, execute_validation_error_action, execute_ok_action
)
from sources.message.schemas import Message
from sources.constants import BAD_REQUEST
from sources.message.repositories import MessageRepository
from sources.base.handlers import BaseView
from sources.base.utils import auth_required


logger = logging.getLogger(__name__)


class MessageHandler(BaseView):
    repository = MessageRepository()
    schema = Message
    allowed_methods = ('OPTIONS', 'POST')

    @auth_required
    async def post(self):
        response, obj = await self._validate_body('POST')
        if type(response) is web.Response:
            return response

        try:
            message = await self.repository.insert_row(obj)
        except IntegrityError:
            return web.Response(
                body=serialize_response(execute_validation_error_action(
                    response, self.request, 'ERR_INVALID_MSG_SEND', 'POST')
                ),
                status=BAD_REQUEST
            )

        return web.Response(body=serialize_response(
            execute_ok_action(response, self.request, message, 'POST'))
        )
