from datetime import datetime
from db.dals.META.statistic_dal_meta import StatisticDAL
from db.models.servers.servers_info import ServersInfo
from db.models.tasks.tasks_update_info import TasksUpdateInfo
from sqlalchemy.future import select
from typing import Type, Optional


class TasksUpdateInfoDAL(StatisticDAL):
    @property
    def _table(self) -> Type[TasksUpdateInfo]:
        return TasksUpdateInfo

    async def add_info(self, server_id: int, task_configuration: dict, time: Optional[datetime] = None):
        await self._add_statistic(
            time,
            server_id=server_id,
            task_configuration=task_configuration
        )

    async def get_history(self, server_id: int):
        query = await self._db_session.execute(
            select(self._table).where(self._table.server_id == server_id)
        )
        return query.scalars().all()

    async def get_history_of_task(self, task_name: str):
        query = await self._db_session.execute(
            select(self._table)
            .join(ServersInfo, ServersInfo.task == task_name)
        )
        return query.scalars().all()
