import logging

from backend.message.schemas import Message
from backend.message.repositories import MessageRepository
from backend.base.handlers import BaseView


logger = logging.getLogger(__name__)


class MessageHandler(BaseView):
    repository = MessageRepository()
    schema = Message
    allowed_methods = ('OPTIONS', 'POST')
