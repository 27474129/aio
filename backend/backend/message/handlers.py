import logging

from backend.message.schemas import MessageSchema
from backend.message.repositories import MessageRepository
from backend.base.handlers import BaseView
from backend.message.models import Message


logger = logging.getLogger(__name__)


class MessageHandler(BaseView):
    repository = MessageRepository()
    schema = MessageSchema
    allowed_methods = ('OPTIONS', 'POST')
    model = Message
