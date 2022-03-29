from contextlib import asynccontextmanager
from db.config import async_session
from db.dals.dal_meta import DAL
from typing import Type


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session


@asynccontextmanager
async def get_dal(dal_type: Type[DAL]):
    async with get_session() as session:
        dal = dal_type(session)
        yield dal


async def get_all(dal_type: Type[DAL]):
    async with get_dal(dal_type) as dal:
        return await dal.get_all()
