import logging

from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from sqlalchemy import select, insert, delete
from pydantic import BaseModel

from sources.config import POSTGRES_CONN_STRING


Base = declarative_base()
engine = create_async_engine(POSTGRES_CONN_STRING)

logger = logging.getLogger(__name__)


class BaseRepository:
    model = Base
    schema = BaseModel

    def __init__(self):
        self._async_session = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_row(self, rid: int) -> dict:
        query = select(self.model).where(self.model.id == rid).limit(1)
        logger.info(str(query))
        try:
            async with self._async_session() as s:
                row = (await s.execute(query)).scalar().__dict__
                # Delete useless column
                del row["_sa_instance_state"]
                return row
        except NoResultFound:
            ...

    async def insert_row(self, data: schema) -> dict:
        query = insert(self.model).values(**data.dict()).returning(self.model)
        logger.info(str(query))
        async with self._async_session() as s:
            row = (await s.execute(query)).scalar().__dict__
            # Delete useless column
            del row["_sa_instance_state"]
            await s.commit()
            return row

    async def delete_row(self, rid: int) -> dict:
        query = delete(self.model).where(self.model.id == rid)\
            .returning(self.model)
        logger.info(str(query))
        async with self._async_session() as s:
            row = (await s.execute(query)).scalar().__dict__
            # Delete useless column
            del row["_sa_instance_state"]
            await s.commit()
            return row
