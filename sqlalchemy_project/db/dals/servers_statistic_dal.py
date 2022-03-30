from db.dals.dal_meta import DAL
from db.models.servers_statistic import ServersStatistic
from typing import Type, Optional


class ServersStatisticDAL(DAL):
    @property
    def _table(self) -> Type[ServersStatistic]:
        return ServersStatistic

    async def add(self, server_id: int, workload_percentage: float, temperature: Optional[float],
                  ram_used: int, disk_used: int):
        new_data = ServersStatistic(
            server_id=server_id,
            workload_percentage=workload_percentage,
            temperature=temperature,
            ram_used=ram_used,
            disk_used=disk_used
        )
        return await self._add(new_data)
