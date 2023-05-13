import logging
from typing import Type, Optional, Union

from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from sqlalchemy import select, insert, delete, update
from sqlalchemy.sql._dml_constructors import Update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Insert, Delete
from pydantic import BaseModel as BaseSchema

from backend.config import ASYNC_POSTGRES_CONN_STRING


Base = declarative_base()
engine = create_async_engine(ASYNC_POSTGRES_CONN_STRING)


class BaseRepository:
    model: Type[Base] = Base
    schema: Type[BaseSchema] = BaseSchema

    registry_type = Union[Select, Insert, Delete, Update]
    registry_query: registry_type = None

    logger = logging.getLogger(__name__)

    def get_registry_query(self) -> registry_type:
        return select(self.model) if self.registry_query is None \
            else self.registry_query

    def __init__(self):
        self._async_session = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    async def _execute_query(
        self, query: registry_type, is_select: bool = False
    ) -> Optional[Union[dict, str]]:
        self.logger.info(str(query))

        async with self._async_session() as s:
            row = (await s.execute(query)).scalar()
            if not row:
                return

            # Condition for select requests, which have more than one column
            if type(row) is self.model:
                row = row.__dict__
                # Delete useless column
                del row["_sa_instance_state"]

            if not is_select:
                await s.commit()
            return row

    async def get_row(self, rid: int) -> Optional[dict]:
        query = select(self.model).where(self.model.id == rid)
        try:
            return await self._execute_query(query)
        except NoResultFound:
            ...

    async def insert_row(self, data: schema) -> dict:
        query = insert(self.model).values(**data.dict()).returning(self.model)
        return await self._execute_query(query)

    async def delete_row(self, rid: int) -> dict:
        query = delete(self.model).where(self.model.id == rid)\
            .returning(self.model)
        return await self._execute_query(query)

    async def update_row(self, data: schema, uid: int) -> dict:
        """Updating first_name, last_name, password."""
        query = update(self.model).where(self.model.id == uid)\
            .values(**data.dict()).returning(self.model)
        return await self._execute_query(query)

    async def get_registry(self) -> list:
        query = self.get_registry_query()
        self.logger.info(str(query))
        async with self._async_session() as s:
            rows = (await s.execute(query)).all()

        parsed_rows = []
        for row in rows:
            parsed_rows.append(dict(row._mapping))
        return parsed_rows
