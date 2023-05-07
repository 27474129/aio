import logging

from aiohttp.web import View
from aiohttp import web
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from sources.base.utils import (
    get_response_template, serialize_response, execute_ok_action,
    execute_validation_error_action, auth_required
)
from sources.base.repositories import BaseRepository
from sources.constants import (
    WARN_OBJECT_NOT_FOUND, NOT_FOUND, REQUEST_SENT_INFO, BAD_REQUEST,
    NOT_ALLOWED
)


logger = logging.getLogger(__name__)


# TODO: Вынести повторяющийся функционал в методы
class BaseView(View):
    repository = BaseRepository()
    schema = BaseModel
    allowed_methods = ('OPTIONS', 'GET', 'POST', 'PUT', 'DELETE')

    @auth_required
    async def get(self):
        if 'GET' not in self.allowed_methods:
            return web.Response(status=NOT_ALLOWED)
        response = get_response_template()

        obj = await self.repository.get_row(int(self.request.match_info['id']))
        if not obj:
            response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
            status = NOT_FOUND
            logger.info(
                REQUEST_SENT_INFO.format(
                    path=self.request.rel_url, status=status, method='GET'
                )
            )
            return web.Response(
                text=serialize_response(response), status=status
            )

        return web.Response(
            body=serialize_response(
                execute_ok_action(response, self.request, obj, 'GET')
            )
        )

    @auth_required
    async def post(self):
        if 'POST' not in self.allowed_methods:
            return web.Response(status=NOT_ALLOWED)
        response = get_response_template()

        try:
            obj = self.schema.parse_raw(await self.request.read())
        except ValidationError as e:
            return web.Response(
                body=serialize_response(execute_validation_error_action(
                    response, self.request, e, 'POST')
                ),
                status=BAD_REQUEST
            )

        user = await self.repository.insert_row(obj)
        return web.Response(body=serialize_response(
            execute_ok_action(response, self.request, user, 'POST'))
        )

    @auth_required
    async def delete(self):
        response = get_response_template()
        if 'DELETE' not in self.allowed_methods:
            return web.Response(status=NOT_ALLOWED)

        # TODO: Add a checkup, if id has int type
        obj = await self.repository.delete_row(
            int(self.request.match_info['id'])
        )
        if not obj:
            response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
            status = NOT_FOUND
            logger.info(
                REQUEST_SENT_INFO.format(
                    path=self.request.rel_url, status=status, method='DELETE'
                )
            )
            return web.Response(text=serialize_response(response),
                                status=status)

        return web.Response(
            body=serialize_response(
                execute_ok_action(response, self.request, obj, 'DELETE')
            )
        )

    @auth_required
    async def put(self):
        if 'PUT' not in self.allowed_methods:
            return web.Response(status=NOT_ALLOWED)
        response = get_response_template()

        try:
            obj = self.schema.parse_raw(await self.request.read())
        except ValidationError as e:
            execute_validation_error_action(response, self.request, e, 'PUT')
            return web.Response(
                body=serialize_response(execute_validation_error_action(
                    response, self.request, e, 'PUT')
                ),
                status=BAD_REQUEST
            )

        self.repository.schema = self.schema
        obj = await self.repository.update_row(
            obj, int(self.request.match_info['id'])
        )

        if not obj:
            response['warnings'].append(WARN_OBJECT_NOT_FOUND.format('User'))
            return web.Response(
                body=serialize_response(response), status=NOT_FOUND
            )

        return web.Response(
            body=serialize_response(
                execute_ok_action(response, self.request, obj, 'PUT')
            )
        )
