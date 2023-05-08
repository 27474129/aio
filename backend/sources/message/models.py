from datetime import datetime

from sqlalchemy import Column, Text, ForeignKey, Integer, TIMESTAMP

from sources.base.models import BaseModel
from sources.base.repositories import Base


class Message(Base, BaseModel):
    __tablename__ = 'message'

    text = Column(Text)
    to = Column(Integer, ForeignKey('user.id'), index=True)
    by = Column(Integer, ForeignKey('user.id'), index=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
