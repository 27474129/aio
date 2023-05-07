import logging

from aiohttp import web
from pydantic.error_wrappers import ValidationError

from sources.user.schemas import User, UserUpdate
from sources.constants import BAD_REQUEST
from sources.user.repositories import UserRepository
from sources.base.utils import (
    get_response_template, serialize_response, execute_validation_error_action,
    execute_ok_action, auth_required
)
from sources.base.handlers import BaseView


logger = logging.getLogger(__name__)


@auth_required
async def create_user(request):
    response = get_response_template()
    try:
        user = User.parse_raw(await request.read())
    except ValidationError as e:
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, e, 'POST')
            ),
            status=BAD_REQUEST
        )

    user = await UserRepository().insert_row(user)
    return web.Response(body=serialize_response(
        execute_ok_action(response, request, user, 'POST'))
    )

# TODO: Добавить получение реестра пользователей
# TODO: Добавить PATCH запрос к юзеру, с возможность обновления email


class UserHandler(BaseView):
    repository = UserRepository()
    schema = User
    allowed_methods = ('OPTIONS', 'GET', 'PUT', 'DELETE')

    async def put(self):
        self.schema = UserUpdate
        return await super().put()


class UserCreationHandler(UserHandler):
    allowed_methods = ('OPTIONS', 'POST')
