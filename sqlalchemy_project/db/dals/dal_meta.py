from abc import ABCMeta, abstractmethod
from sqlalchemy.future import select
from sqlalchemy.orm import Session, DeclarativeMeta
from typing import Type


class DAL(metaclass=ABCMeta):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @property
    @abstractmethod
    def _table(self) -> Type[DeclarativeMeta]:
        pass

    async def _add(self, data: DeclarativeMeta):
        self.db_session.add(data)
        await self.db_session.flush()

    async def get_all(self) -> list:
        query = await self.db_session.execute(
            select(self._table)
        )
        return query.scalars().all()
