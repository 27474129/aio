from backend.base.repositories import BaseRepository
from backend.notification.models import Notification
from backend.notification.schemas import NotificationSchema as NotificationSchema


class NotificationRepository(BaseRepository):
    model = Notification
    schema = NotificationSchema
