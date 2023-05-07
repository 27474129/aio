import logging

from aiohttp import web
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError

from sources.base.utils import (
    auth_required, get_response_template, serialize_response,
    execute_validation_error_action, execute_ok_action
)
from sources.message.schemas import Message
from sources.constants import BAD_REQUEST
from sources.message.repositories import MessageRepository


logger = logging.getLogger(__name__)


@auth_required
async def create_message(request):
    response = get_response_template()

    try:
        message = Message.parse_raw(await request.read())
    except ValidationError as e:
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, e, 'POST')
            ),
            status=BAD_REQUEST
        )

    try:
        message = await MessageRepository().insert_row(message)
    except IntegrityError:
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, 'ERR_INVALID_MSG_SEND', 'POST')
            ),
            status=BAD_REQUEST
        )

    return web.Response(body=serialize_response(
        execute_ok_action(response, request, message, 'POST'))
    )
