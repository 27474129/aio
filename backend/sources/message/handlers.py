import logging

from sources.message.schemas import Message
from sources.message.repositories import MessageRepository
from sources.base.handlers import BaseView


logger = logging.getLogger(__name__)


class MessageHandler(BaseView):
    repository = MessageRepository()
    schema = Message
    allowed_methods = ('OPTIONS', 'POST')
