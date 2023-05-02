from sources.base.repositories import BaseRepository
from sources.user.models import User
from sources.user.schemas import User as UserSchema


class UserRepository(BaseRepository):
    model = User
    schema = UserSchema
