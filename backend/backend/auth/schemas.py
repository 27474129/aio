from pydantic import BaseModel

from backend.user.schemas import BaseUserSchema


class UserAuth(BaseModel):
    email: str = BaseUserSchema.email
    password: str = BaseUserSchema.password
