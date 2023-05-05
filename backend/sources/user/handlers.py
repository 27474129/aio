import logging

from aiohttp import web
from pydantic.error_wrappers import ValidationError

from sources.user.schemas import User, UpdateUser
from sources.constants import (
    BAD_REQUEST, NOT_FOUND, WARN_OBJECT_NOT_FOUND, REQUEST_SENT_INFO, OK_CODE
)
from sources.user.repositories import UserRepository
from sources.base.utils import (
    get_response_template, serialize_response, execute_validation_error_action,
    execute_ok_action
)


logger = logging.getLogger(__name__)


async def create_user(request):
    response = get_response_template()
    try:
        user = User.parse_raw(await request.read())
    except ValidationError as e:
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, e)
            ),
            status=BAD_REQUEST
        )

    user = await UserRepository().insert_row(user)
    return web.Response(body=serialize_response(
        execute_ok_action(response, request, user))
    )


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

    return web.Response(
        body=serialize_response(execute_ok_action(response, request, user))
    )


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

    return web.Response(
        body=serialize_response(execute_ok_action(response, request, user))
    )


async def update_user(request):
    response = get_response_template()

    try:
        user = UpdateUser.parse_raw(await request.read())
    except ValidationError as e:
        execute_validation_error_action(response, request, e)
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, e)
            ),
            status=BAD_REQUEST
        )

    user_repository = UserRepository()
    user_repository.schema = UpdateUser
    user = await user_repository.update_row(user, int(request.match_info['id']))

    if not user:
        response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
        return web.Response(body=serialize_response(response), status=NOT_FOUND)

    return web.Response(
        body=serialize_response(execute_ok_action(response, request, user))
    )

# TODO: Добавить получение реестра пользователей
# TODO: Добавить PATCH запрос к юзеру, с возможность обновления email
