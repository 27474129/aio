import time
import logging
from typing import Optional, Dict

import jwt

from backend.config import JWT_SECRET, JWT_ALGORITHM


logger = logging.getLogger(__name__)


class AuthService:
    """Class responsible for authentication and authorization."""
    def generate_token(self, uid: int, email: str) -> str:
        logger.info('Generated JWT token')
        payload = {
            'uid': uid,
            'email': email,
            # expired in 48 hours
            'expires': time.time() + 3600 * 48
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            decode_token = jwt.decode(
                token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
            )
            return decode_token if decode_token['expires'] > time.time()\
                else None
        except jwt.InvalidSignatureError:
            logger.info('Invalid JWT token')
