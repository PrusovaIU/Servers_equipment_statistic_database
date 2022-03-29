from contextlib import asynccontextmanager
from db.config import async_session, engine
from db.config import Base
from db.dals.dal_meta import DAL
from db.dals.servers_info_dal import ServersInfoDAL, ServersInfo
from db.dals.modules_info_dal import ModulesInfoDAL, ModulesInfo
from fastapi import FastAPI
from http import HTTPStatus
from typing import List, Type
import uvicorn


app = FastAPI()


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


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Servers.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post("/servers")
async def add_server(server_id: int, task_name: str, host: str):
    async with get_session() as session:
        servers_info_dal = ServersInfoDAL(session)
        return await servers_info_dal.add_server(server_id, task_name, host)


@app.get("/servers")
async def get_all_servers() -> List[ServersInfo]:
    # async with get_session() as session:
    #     servers_info_dal = ServersInfoDAL(session)
    #     return await servers_info_dal.get_all()
    return await get_all(ServersInfoDAL)


@app.post("/modules", status_code=HTTPStatus.CREATED)
async def add_module(server_id: int, position: int, module_type: str):
    async with get_session() as session:
        modules_info_dal = ModulesInfoDAL(session)
        return await modules_info_dal.add_module(server_id, position, module_type)


@app.get("/modules")
async def get_all_modules() -> List[ModulesInfo]:
    return await get_all(ModulesInfoDAL)


@app.get("/module")
async def get_module(server_id: int, position: int):
    async with get_dal(ModulesInfoDAL) as dal:
        return await dal.get_module(server_id, position)


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=1111)
