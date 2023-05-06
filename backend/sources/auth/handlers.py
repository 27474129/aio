import logging

from aiohttp import web
from pydantic import ValidationError

from sources.base.utils import (
    get_response_template, serialize_response, execute_validation_error_action
)
from sources.constants import BAD_REQUEST, WARN_INVALID_LOGIN_DATA
from sources.auth.schemas import UserAuth
from sources.auth.services import AuthService
from sources.user.repositories import UserRepository
from sources.base.utils import execute_ok_action


logger = logging.getLogger(__name__)


async def auth(request):
    response = get_response_template()
    try:
        body = UserAuth.parse_raw(await request.read()).dict()
    except ValidationError as e:
        return web.Response(
            body=serialize_response(execute_validation_error_action(
                response, request, e, method='POST')
            ),
            status=BAD_REQUEST
        )

    user = await UserRepository().get_user_by_email(body['email'])
    if not user:
        response['warnings'].append(WARN_INVALID_LOGIN_DATA)
        logger.info(WARN_INVALID_LOGIN_DATA)
        return web.Response(
            body=serialize_response(response),
            status=BAD_REQUEST
        )

    token = AuthService().generate_token(uid=user['id'], email=user['email'])
    return web.Response(
        body=serialize_response(
            execute_ok_action(response, request, {'token': token}, 'POST')
        )
    )
