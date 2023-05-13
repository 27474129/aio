from backend.base.repositories import BaseRepository
from backend.message.models import Message
from backend.message.schemas import MessageSchema as MessageSchema


class MessageRepository(BaseRepository):
    model = Message
    schema = MessageSchema
