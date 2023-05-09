from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA

from backend.base.models import BaseModel
from backend.base.repositories import Base


class Notification(Base, BaseModel):
    __tablename__ = 'notification'

    starting_at = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('user.id'), index=True)
    html_file = Column(BYTEA)
