from abc import ABCMeta, abstractmethod
from sqlalchemy.future import select
from sqlalchemy.orm import Session, DeclarativeMeta
from fastapi import HTTPException
from http import HTTPStatus
from typing import Type


class DAL(metaclass=ABCMeta):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    @property
    @abstractmethod
    def _table(self) -> Type[DeclarativeMeta]:
        pass

    async def _add(self, data: DeclarativeMeta):
        self._db_session.add(data)
        await self._db_session.flush()

    async def _get_id(self, statement: select, error_detail: str):
        try:
            query = await self._db_session.execute(statement)
            result = query.scalars().all()
            result_id = result[0]
        except IndexError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error_detail)
        return result_id

    async def get_all(self) -> list:
        query = await self._db_session.execute(
            select(self._table)
        )
        return query.scalars().all()
