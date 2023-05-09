import json
import logging
from typing import Dict, List

from aiohttp.web import Request
from aiohttp import web

from backend.constants import (
    BAD_REQUEST, REQUEST_SENT_INFO, OK_CODE, NOT_AUTHORIZED, NOT_AUTHORIZED_MSG
)
from backend.auth.services import AuthService


logger = logging.getLogger(__name__)


def get_response_template() -> Dict[str, List]:
    return {
        'warnings': [],
        'errors': [],
        'rows': []
    }


def serialize_response(response: Dict[str, List]) -> str:
    return json.dumps(response, indent=4, sort_keys=True, default=str)


def execute_validation_error_action(
    response: Dict[str, List], request: Request, e, method: str
) -> Dict[str, List]:
    """Function, which do some action on validation error."""
    response['errors'] = e.errors() if type(e) is not str else e

    logger.info(
        REQUEST_SENT_INFO.format(
            path=request.rel_url, status=BAD_REQUEST, method=method
        )
    )
    return response


def execute_ok_action(
    response: Dict[str, List], request: Request, row, method: str
) -> Dict[str, List]:
    """Function, which do some action on success request to DB."""
    response['rows'].append(row)
    logger.info(
        REQUEST_SENT_INFO.format(
            path=request.rel_url, status=OK_CODE, method=method
        )
    )
    return response


def auth_required(func):
    """Decorator, which authenticate user."""
    async def _wrapper(self):
        token = dict(self.request.headers).get('Authorization')
        if not token:
            return web.Response(text=NOT_AUTHORIZED_MSG, status=NOT_AUTHORIZED)

        # Get token
        token = token.split()[1]

        return web.Response(text=NOT_AUTHORIZED_MSG, status=NOT_AUTHORIZED) \
            if not AuthService().decode_token(token) \
            else await func(self)
    return _wrapper
