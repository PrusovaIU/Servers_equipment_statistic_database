from db.dals.servers_info_dal import ServersInfoDAL, ServersInfo
from fastapi import APIRouter
from http import HTTPStatus
from initers import get_all, get_session
from typing import List


servers_router = APIRouter(prefix="/servers")


@servers_router.post("/", status_code=HTTPStatus.CREATED)
async def add_server(server_id: int, task_name: str, host: str):
    async with get_session() as session:
        servers_info_dal = ServersInfoDAL(session)
        return await servers_info_dal.add_server(server_id, task_name, host)


@servers_router.get("/")
async def get_all_servers() -> List[ServersInfo]:
    return await get_all(ServersInfoDAL)
