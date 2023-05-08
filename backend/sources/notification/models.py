from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, TEXT, Integer, ForeignKey

from sources.base.models import BaseModel
from sources.base.repositories import Base


class Notification(Base, BaseModel):
    __tablename__ = 'notification'

    starting_at = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('user.id'), index=True)
    html_file = Column(TEXT)