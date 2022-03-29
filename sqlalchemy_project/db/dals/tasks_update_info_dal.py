from db.dals.dal_meta import DAL
from db.models.servers_info import ServersInfo
from db.models.tasks_update_info import TasksUpdateInfo
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.future import select
from typing import Type, Optional


class TasksUpdateInfoDAL(DAL):
    @property
    def _table(self) -> Type[TasksUpdateInfo]:
        return TasksUpdateInfo

    async def add_info(self, server_id: int, task_configuration: dict):
        new_info = TasksUpdateInfo(
            server_id=server_id,
            task_configuration=task_configuration
        )
        await self._add(new_info)

    # async def get_history(self, server_id: int, task_name: Optional[str]):
    #     s = select(self._table)
    #     if task_name is not None:
    #         s = s.join(ServersInfo, ServersInfo.task == task_name)
    #     s = s.where(self._table.server_id == server_id)
    #     query = await self.db_session.execute(s)
    #     return query.scalars().all()
    async def get_history(self, server_id: int):
        query = await self.db_session.execute(
            select(self._table).where(self._table.server_id == server_id)
        )
        return query.scalars().all()

    async def get_history_of_task(self, task_name: str):
        query = await self.db_session.execute(
            select(self._table)
            .join(ServersInfo, ServersInfo.task == task_name)
        )
        return query.scalars().all()
