import logging

from aiohttp import web
from pydantic.error_wrappers import ValidationError

from sources.user.schemas import User
from sources.constants import (
    BAD_REQUEST, NOT_FOUND, WARN_OBJECT_NOT_FOUND, REQUEST_SENT_INFO, OK_CODE
)
from sources.user.repositories import UserRepository
from sources.base.utils import get_response_template, serialize_response


logger = logging.getLogger('__name__')


async def create_user(request):
    response = get_response_template()
    try:
        user = User.parse_raw(await request.read())
    except ValidationError as e:
        response['errors'] = (e.errors())
        status = BAD_REQUEST
        logger.info(
            REQUEST_SENT_INFO.format(path=request.rel_url, status=status)
        )
        return web.Response(
            body=serialize_response(response), status=status
        )

    user = await UserRepository().insert_row(user)
    response['rows'].append(user)
    logger.info(
        REQUEST_SENT_INFO.format(path=request.rel_url, status=OK_CODE)
    )
    return web.Response(body=serialize_response(response))


async def get_user(request):
    response = get_response_template()
    user = await UserRepository().get_row(int(request.match_info['id']))
    if not user:
        response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
        status = NOT_FOUND
        logger.info(
            REQUEST_SENT_INFO.format(path=request.rel_url, status=status)
        )
        return web.Response(text=serialize_response(response), status=status)

    response['rows'].append(user)
    logger.info(REQUEST_SENT_INFO.format(path=request.rel_url, status=OK_CODE))
    return web.Response(body=serialize_response(response))


async def delete_user(request):
    response = get_response_template()
    user = await UserRepository().delete_row(int(request.match_info['id']))
    if not user:
        response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
        status = NOT_FOUND
        logger.info(
            REQUEST_SENT_INFO.format(path=request.rel_url, status=status)
        )
        return web.Response(text=serialize_response(response), status=status)

    logger.info(
        REQUEST_SENT_INFO.format(path=request.rel_url, status=OK_CODE)
    )
    response['rows'].append(user)
    return web.Response(body=serialize_response(response))
