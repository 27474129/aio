import logging

from sources.base.handlers import BaseView
from sources.notification.repository import NotificationRepository
from sources.notification.schemas import Notification


logger = logging.getLogger(__name__)


class NotificationHandler(BaseView):
    repository = NotificationRepository()
    schema = Notification
    allowed_methods = ('OPTIONS', 'POST')
