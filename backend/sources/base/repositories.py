from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from sqlalchemy import select, insert
from pydantic import BaseModel

from sources.config import POSTGRES_CONN_STRING


Base = declarative_base()
engine = create_async_engine(POSTGRES_CONN_STRING, echo=True)


class BaseRepository:
    model = Base
    schema = BaseModel

    def __init__(self):
        self._async_session = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_row(self, rid: int) -> dict:
        try:
            async with engine.connect() as conn:
                row = (
                    await conn.execute(
                        select(self.model).where(self.model.id == rid).limit(1)
                    )
                ).fetchone()
                return dict(row._mapping) if row else None
        except NoResultFound:
            ...

    async def insert_row(self, data: schema) -> dict:
        async with engine.connect() as conn:
            row = (
                await conn.execute(
                    insert(self.model).values(**data.dict())
                    .returning(self.model)
                )
            ).fetchone()
            await conn.commit()
            return dict(row._mapping)
