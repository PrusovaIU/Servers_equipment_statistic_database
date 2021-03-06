from db.dals.tasks.tasks_update_info_dal import TasksUpdateInfoDAL
from db.dals.META.dal_meta import DAL
from db.models.servers.servers_info import ServersInfo
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.future import select
from typing import Type


class ServersInfoDAL(DAL):
    @property
    def _table(self) -> Type[ServersInfo]:
        return ServersInfo

    async def add_server(self, server_id: int, task_name: str, host: str, task_configuration: dict):
        if await self.get_server(server_id) is None:
            new_server = ServersInfo(
                server_id=server_id,
                task=task_name,
                host=host
            )
            await self._add(new_server)
            task_update_dal = TasksUpdateInfoDAL(self._db_session)
            await task_update_dal.add_info(server_id, task_configuration)
        else:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Server with ID = {server_id} is already exists")

    async def get_server(self, server_id) -> str:
        query = await self._db_session.execute(
            select(self._table)
            .where(self._table.server_id == server_id)
        )
        return query.first()
