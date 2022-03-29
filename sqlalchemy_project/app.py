from db.config import async_session, engine
from db.config import Servers
from db.dals.servers_info_dal import ServersInfoDAL
from db.models.servers_info import ServersInfo
from fastapi import FastAPI
from sqlalchemy.schema import CreateSchema
from typing import List
import uvicorn


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Servers.metadata.drop_all)
        await conn.run_sync(Servers.metadata.create_all)


@app.post("/servers")
async def add_server(server_id: int, task_name: str, host: str):
    async with async_session() as session:
        async with session.begin():
            servers_info_dal = ServersInfoDAL(session)
            return await servers_info_dal.add_server(server_id, task_name, host)


@app.get("/books")
async def get_all_servers() -> List[ServersInfo]:
    async with async_session() as session:
        async with session.begin():
            servers_info_dal = ServersInfoDAL(session)
            return await servers_info_dal.get_all_servers()


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=1111)
