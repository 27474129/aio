from typing import Optional

import requests

from computer.config import (
    BACKEND_EMAIL, BACKEND_PASSWORD, BACKEND_HOST, BACKEND_PORT
)
from computer.constants import OK_CODE


def backend_auth() -> Optional[str]:
    """Authentication in backend, getting JWT token for future requests."""
    body = {
        'email': BACKEND_EMAIL, 'password': BACKEND_PASSWORD
    }
    response = requests.post(
        f'{BACKEND_HOST}:{BACKEND_PORT}/api/auth', json=body
    )
    if response.status_code == OK_CODE:
        return response.json()['rows'][0]['token']
