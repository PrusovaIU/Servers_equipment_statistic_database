from datetime import datetime
from db.dals.META.statistic_dal_meta import StatisticDAL
from db.models.tasks.tasks_statistic import TasksStatistic
from typing import Type, Optional


class TasksStatisticDAL(StatisticDAL):
    @property
    def _table(self) -> Type[TasksStatistic]:
        return TasksStatistic

    async def add(self, server_id: int, speed_in: int, speed_out: int,
                  total_in: int, total_out: int, total_dropped: int, time: Optional[datetime] = None):
        await self._add_statistic(
            time,
            server_id=server_id,
            speed_in=speed_in,
            speed_out=speed_out,
            total_in=total_in,
            total_out=total_out,
            total_dropped=total_dropped
        )
