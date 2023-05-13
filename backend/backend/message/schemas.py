from pydantic import BaseModel


class MessageSchema(BaseModel):
    text: str
    to: int
    by: int
