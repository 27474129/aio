import logging

from aiohttp import web

from sources.base.utils import serialize_response
from sources.constants import BAD_REQUEST, WARN_INVALID_LOGIN_DATA
from sources.auth.schemas import UserAuth
from sources.auth.services import AuthService
from sources.user.repositories import UserRepository
from sources.base.utils import execute_ok_action
from sources.base.handlers import BaseView


logger = logging.getLogger(__name__)


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
            logger.info(WARN_INVALID_LOGIN_DATA)
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
