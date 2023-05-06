from sqlalchemy import Column, Text, ForeignKey, Integer

from sources.base.models import BaseModel
from sources.base.repositories import Base


class Message(Base, BaseModel):
    __tablename__ = 'message'

    text = Column(Text)
    to = Column(Integer, ForeignKey('user.id'), index=True)
    by = Column(Integer, ForeignKey('user.id'), index=True)
