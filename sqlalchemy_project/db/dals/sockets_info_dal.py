from db.dals.dal_meta import DAL
from db.models.sockets_info import SocketsInfo
from db.models.servers_info import ServersInfo
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.future import select
from typing import Type


class SocketsInfoDAL(DAL):
    @property
    def _table(self) -> Type[SocketsInfo]:
        return SocketsInfo

    async def add_socket(self, server_id: int, name: str, port: int, socket_type: str):
        if await self.get_socket(server_id, port) is None:
            new_socket = SocketsInfo(
                server_id=server_id,
                name=name,
                port=port,
                socket_type=socket_type
            )
            await self._add(new_socket)
        else:
            raise HTTPException(status_code=HTTPStatus.CONFLICT,
                                detail=f"There is socket on server {server_id} on port {port}")

    async def get_host_sockets(self, host: str):
        query = await self.db_session.execute(
            select(self._table)
            .join(ServersInfo, ServersInfo.server_id == self._table.server_id)
            .where(ServersInfo.host == host)
        )
        return query.all()

    async def get_server_sockets(self, server_id: int):
        query = await self.db_session.execute(
            select(self._table)
            .where(self._table.server_id == server_id)
        )
        return query.all()

    async def get_socket(self, server_id: int, port: int):
        query = await self.db_session.execute(
            select(self._table)
            .where(self._table.server_id == server_id)
            .where(self._table.port == port)
        )
        return query.first()

    async def get_sockets_by_type(self, socket_type: str):
        query = await self.db_session.execute(
            select(self._table)
            .where(self._table.socket_type == socket_type)
        )
        return query.all()
