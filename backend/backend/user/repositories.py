from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from backend.base.repositories import BaseRepository
from backend.user.models import User
from backend.user.schemas import UserSchema as UserSchema


class UserRepository(BaseRepository):
    model = User
    schema = UserSchema

    registry_query = select(model.email)

    async def get_user_by_email(self, email: str) -> Optional[str]:
        """Getting user password by email for authentication."""
        query = select(self.model).where(self.model.email == email)
        try:
            return await self._execute_query(query)
        except NoResultFound:
            ...
