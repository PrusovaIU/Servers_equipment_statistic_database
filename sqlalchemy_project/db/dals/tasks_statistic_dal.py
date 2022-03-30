from db.dals.dal_meta import DAL
from db.models.tasks_statistic import TasksStatistic
from typing import Type


class TasksStatisticDAL(DAL):
    @property
    def _table(self) -> Type[TasksStatistic]:
        return TasksStatistic

    async def add(self, server_id: int, speed_in: int, speed_out: int,
                  total_in: int, total_out: int, total_dropped: int):
        new_info = TasksStatistic(
            server_id=server_id,
            speed_in=speed_in,
            speed_out=speed_out,
            total_in=total_in,
            total_out=total_out,
            total_dropped=total_dropped
        )
        await self._add(new_info)
