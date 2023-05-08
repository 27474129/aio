from sources.base.repositories import BaseRepository
from sources.notification.models import Notification
from sources.notification.schemas import Notification as NotificationSchema


class NotificationRepository(BaseRepository):
    model = Notification
    schema = NotificationSchema
