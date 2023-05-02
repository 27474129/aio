from aiohttp import web
from pydantic.error_wrappers import ValidationError

from sources.user.schemas import User
from sources.constants import BAD_REQUEST, NOT_FOUND, WARN_OBJECT_NOT_FOUND
from sources.user.repositories import UserRepository
from sources.base.utils import get_response_template, serialize_response


async def create_user(request):
    response = get_response_template()
    try:
        user = User.parse_raw(await request.read())
    except ValidationError as e:
        response['errors'] = (e.errors())
        return web.Response(
            body=serialize_response(response), status=BAD_REQUEST
        )

    user = await UserRepository().insert_row(user)
    response['rows'].append(user)
    return web.Response(body=serialize_response(response))


async def get_user(request):
    response = get_response_template()
    user = await UserRepository().get_row(int(request.match_info['id']))
    if not user:
        response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
        return web.Response(text=serialize_response(response), status=NOT_FOUND)
    response['rows'].append(user)
    return web.Response(body=serialize_response(response))


async def delete_user(request):
    # TODO: Дописать delete_row метод
    response = get_response_template()
    if not UserRepository().delete_row(request.match_info['id']):
        response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
        return web.Response(text=serialize_response(response), status=NOT_FOUND)
    return web.Response(body=serialize_response(response))
