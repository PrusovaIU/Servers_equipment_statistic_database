from db.dals.dal_meta import DAL
from db.models.servers_info import ServersInfo
from sqlalchemy.orm import DeclarativeMeta
from typing import Type


class ServersInfoDAL(DAL):
    @property
    def _table(self) -> Type[DeclarativeMeta]:
        return ServersInfo

    async def add_server(self, server_id: int, task_name: str, host: str):
        new_server = ServersInfo(
            server_id=server_id,
            task=task_name,
            host=host
        )
        await self._add(new_server)
