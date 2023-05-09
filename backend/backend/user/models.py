from datetime import datetime

from sqlalchemy import String, Column, TIMESTAMP

from backend.base.models import BaseModel
from backend.base.repositories import Base


class User(Base, BaseModel):
    __tablename__ = 'user'

    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    first_name = Column(String(255))
    last_name = Column(String(255))
