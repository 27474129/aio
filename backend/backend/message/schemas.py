from pydantic import BaseModel


class Message(BaseModel):
    text: str
    to: int
    by: int
