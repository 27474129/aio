from datetime import datetime

from sqlalchemy import String, Integer, Column, TIMESTAMP

from sources.base.repositories import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    first_name = Column(String(255))
    last_name = Column(String(255))
