from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import load_only

from sources.base.repositories import BaseRepository
from sources.user.models import User
from sources.user.schemas import User as UserSchema


class UserRepository(BaseRepository):
    model = User
    schema = UserSchema

    async def get_user_by_email(self, email: str) -> Optional[str]:
        """Getting user password by email for authentication."""
        query = select(self.model).where(self.model.email == email)
        try:
            return await self._execute_query(query)
        except NoResultFound:
            ...
