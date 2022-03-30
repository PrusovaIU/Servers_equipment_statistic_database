from db.dals.sockets_info_dal import SocketsInfoDAL
from fastapi import APIRouter, HTTPException
from json import loads, JSONDecodeError
from http import HTTPStatus
from initers import get_dal, get_all


sockets_router = APIRouter(prefix="/sockets")


@sockets_router.post("/", status_code=HTTPStatus.CREATED)
async def add_socket(server_id: int, name: str, port: int, socket_type: str):
    async with get_dal(SocketsInfoDAL) as dal:
        return await dal.add_socket(server_id, name, port, socket_type)


@sockets_router.get("/")
async def get_all_sockets():
    return await get_all(SocketsInfoDAL)


@sockets_router.get("/socket")
async def get_host_sockets(server_id: int, port: int):
    async with get_dal(SocketsInfoDAL) as dal:
        return await dal.get_socket(server_id, port)


@sockets_router.get("/hosts/{host}")
async def get_host_sockets(host: str):
    async with get_dal(SocketsInfoDAL) as dal:
        return await dal.get_host_sockets(host)


@sockets_router.get("/servers/{server_id}")
async def get_host_sockets(server_id: int):
    async with get_dal(SocketsInfoDAL) as dal:
        return await dal.get_server_sockets(server_id)


@sockets_router.get("/types/{socket_type}")
async def get_host_sockets(socket_type: str):
    async with get_dal(SocketsInfoDAL) as dal:
        return await dal.get_sockets_by_type(socket_type)
