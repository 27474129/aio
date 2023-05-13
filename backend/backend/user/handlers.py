from aiohttp import web

from backend.user.schemas import UserSchema, UserUpdateSchema
from backend.user.repositories import UserRepository
from backend.base.handlers import BaseView
from backend.base.utils import (
    get_response_template, auth_required, serialize_response
)
from backend.constants import NOT_ALLOWED, REQUEST_SENT_INFO, OK_CODE
from backend.user.models import User


# TODO: Добавить PATCH запрос к юзеру, с возможность обновления email
class UserDetailHandler(BaseView):
    repository = UserRepository()
    schema = UserSchema
    allowed_methods = ('OPTIONS', 'GET', 'PUT', 'DELETE')
    model = User

    async def put(self):
        self.schema = UserUpdateSchema
        return await super().put()


class UserHandler(UserDetailHandler):
    # TODO: Add hashing password
    allowed_methods = ('OPTIONS', 'GET', 'POST')

    @auth_required
    async def get(self):
        if 'GET' not in self.allowed_methods:
            return web.Response(status=NOT_ALLOWED)
        response = get_response_template()

        registry = await self.repository.get_registry()
        for row in registry:
            response['rows'].append(row)

        self.logger.info(
            REQUEST_SENT_INFO.format(
                path=self.request.rel_url, status=OK_CODE, method='GET'
            )
        )
        return web.Response(body=serialize_response(response))
