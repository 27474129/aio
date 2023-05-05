import re

from pydantic import BaseModel, Field, validator


class BaseUser(BaseModel):
    password: str = Field(max_length=100, min_length=8)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)

    @validator('password')
    def validate_password(cls, password) -> str:
        if not all([
            len(re.findall(r"[0-9]", password)) >= 2,
            len(re.findall(r"[a-z]", password)) +
            len(re.findall(r"[A-Z]", password)) >= 4,
        ]):
            raise ValueError('Password must contain at least 2 numbers '
                             'and 4 symbols')
        return password


class User(BaseUser):
    email: str = Field(max_length=50, min_length=6)

    @validator('email')
    def validate_email(cls, email) -> str:
        # TODO: Check unique
        if '@' not in email:
            raise ValueError('Email must contain @ symbol')
        return email


class UpdateUser(BaseUser):
    ...
