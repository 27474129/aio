from aiohttp import web

from backend.base.utils import serialize_response
from backend.constants import BAD_REQUEST, WARN_INVALID_LOGIN_DATA
from backend.auth.schemas import UserAuth
from backend.auth.services import AuthService
from backend.user.repositories import UserRepository
from backend.base.utils import execute_ok_action
from backend.base.handlers import BaseView


class AuthHandler(BaseView):
    allowed_methods = ('OPTIONS', 'POST')
    schema = UserAuth
    repository = UserRepository()

    async def post(self):
        response, obj = await self._validate_body('POST')
        if type(response) is web.Response:
            return response

        obj = obj.dict()

        user = await self.repository.get_user_by_email(obj['email'])
        if not user:
            response['warnings'].append(WARN_INVALID_LOGIN_DATA)
            self.logger.info(WARN_INVALID_LOGIN_DATA)
            return web.Response(
                body=serialize_response(response),
                status=BAD_REQUEST
            )

        token = AuthService().generate_token(
            uid=user['id'], email=user['email']
        )
        return web.Response(
            body=serialize_response(
                execute_ok_action(
                    response, self.request, {'token': token}, 'POST'
                )
            )
        )
