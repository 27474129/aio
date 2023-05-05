import logging

from aiohttp import web
from pydantic import ValidationError

from sources.base.utils import (
    get_response_template, serialize_response, execute_validation_error_action
)
from sources.constants import BAD_REQUEST


logger = logging.getLogger(__name__)


async def auth(request):
    response = get_response_template()
    try:
        # TODO: Реализовать схему итд
        body = SomeModel.parse_raw(await request.read())
    except ValidationError as e:
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, e)
            ),
            status=BAD_REQUEST
        )
    response['rows'].append(body)
    return web.Response(body=serialize_response(response))
