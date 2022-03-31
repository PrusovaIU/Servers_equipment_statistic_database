from db.dals.servers.servers_info_dal import ServersInfoDAL, ServersInfo
from fastapi import APIRouter
from fastapi import HTTPException
from http import HTTPStatus
from json import loads, JSONDecodeError
from initers import get_all, get_dal
from typing import List


servers_router = APIRouter(prefix="/servers")


@servers_router.post("/", status_code=HTTPStatus.CREATED)
async def add_server(server_id: int, task_name: str, host: str, task_configuration: str):
    try:
        task_configuration_dict = loads(task_configuration)
        async with get_dal(ServersInfoDAL) as dal:
            return await dal.add_server(server_id, task_name, host, task_configuration_dict)
    except JSONDecodeError as err:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=f"Configuration error: {err}")


@servers_router.get("/")
async def get_all_servers() -> List[ServersInfo]:
    return await get_all(ServersInfoDAL)
