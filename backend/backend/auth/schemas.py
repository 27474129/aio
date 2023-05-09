from pydantic import BaseModel

from backend.user.schemas import BaseUser


class UserAuth(BaseModel):
    email: str = BaseUser.email
    password: str = BaseUser.password
