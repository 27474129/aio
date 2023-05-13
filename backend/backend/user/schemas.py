import re

from pydantic import BaseModel, Field, validator


class BaseUserSchema:
    email: str = Field(max_length=50, min_length=6)
    password: str = Field(max_length=100, min_length=8)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)

    @classmethod
    def validate_email(cls, email) -> str:
        # TODO: Check unique
        if '@' not in email:
            raise ValueError('Email must contain @ symbol')
        return email

    @classmethod
    def validate_password(cls, password) -> str:
        if not all([
            len(re.findall(r"[0-9]", password)) >= 2,
            len(re.findall(r"[a-z]", password)) +
            len(re.findall(r"[A-Z]", password)) >= 4,
        ]):
            raise ValueError('Password must contain at least 2 numbers '
                             'and 4 symbols')
        return password


class UserSchema(BaseModel):
    email: str = BaseUserSchema.email
    password: str = BaseUserSchema.password
    first_name: str = BaseUserSchema.first_name
    last_name: str = BaseUserSchema.last_name

    @validator('email')
    def validate_email(cls, email) -> str:
        return BaseUserSchema.validate_email(email)

    @validator('password')
    def validate_password(cls, password) -> str:
        return BaseUserSchema.validate_password(password)


class UserUpdateSchema(BaseModel):
    password: str = BaseUserSchema.password
    first_name: str = BaseUserSchema.first_name
    last_name: str = BaseUserSchema.last_name

    @validator('password')
    def validate_password(cls, password) -> str:
        return BaseUserSchema.validate_password(password)
