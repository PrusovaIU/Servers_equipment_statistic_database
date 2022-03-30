from datetime import datetime
from db.dals.statistic_dal_meta import StatisticDAL
from db.models.servers_statistic import ServersStatistic
from typing import Type, Optional


class ServersStatisticDAL(StatisticDAL):
    @property
    def _table(self) -> Type[ServersStatistic]:
        return ServersStatistic

    async def add(self, server_id: int, workload_percentage: float, temperature: Optional[float],
                  ram_used: int, disk_used: int, time: Optional[datetime] = None):
        await self._add_statistic(
            time,
            server_id=server_id,
            workload_percentage=workload_percentage,
            temperature=temperature,
            ram_used=ram_used,
            disk_used=disk_used
        )
