import json
import logging
from typing import Dict, List

from sources.constants import BAD_REQUEST, REQUEST_SENT_INFO, OK_CODE


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
    response: Dict[str, List], request, e
) -> Dict[str, List]:
    """Function, which do some action on validation error."""
    response['errors'] = (e.errors())
    logger.info(
        REQUEST_SENT_INFO.format(path=request.rel_url, status=BAD_REQUEST)
    )
    return response


def execute_ok_action(
    response: Dict[str, List], request, row
) -> Dict[str, List]:
    """Function, which do some action on success request to DB."""
    response['rows'].append(row)
    logger.info(
        REQUEST_SENT_INFO.format(path=request.rel_url, status=OK_CODE)
    )
    return response
