import json
import logging
from typing import Dict, List

from aiohttp.web import Request
from aiohttp import web

from sources.constants import (
    BAD_REQUEST, REQUEST_SENT_INFO, OK_CODE, NOT_AUTHORIZED, NOT_AUTHORIZED_MSG
)
from sources.auth.services import AuthService


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
    response: Dict[str, List], request: Request, e
) -> Dict[str, List]:
    """Function, which do some action on validation error."""
    response['errors'] = (e.errors())
    logger.info(
        REQUEST_SENT_INFO.format(path=request.rel_url, status=BAD_REQUEST)
    )
    return response


def execute_ok_action(
    response: Dict[str, List], request: Request, row
) -> Dict[str, List]:
    """Function, which do some action on success request to DB."""
    response['rows'].append(row)
    logger.info(
        REQUEST_SENT_INFO.format(path=request.rel_url, status=OK_CODE)
    )
    return response


def auth_required(func):
    """Decorator, which authenticate user."""
    async def wrapper(request):
        token = dict(request.headers)['Authorization'].split()[1]
        return web.Response(text=NOT_AUTHORIZED_MSG, status=NOT_AUTHORIZED) \
            if not AuthService().decode_token(token) else await func(request)
    return wrapper
