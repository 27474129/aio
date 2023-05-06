from sources.base.repositories import BaseRepository
from sources.message.models import Message
from sources.message.schemas import Message as MessageSchema


class MessageRepository(BaseRepository):
    model = Message
    schema = MessageSchema
