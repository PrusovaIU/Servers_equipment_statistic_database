from .modules_info_dal import ModulesInfoDAL
from datetime import datetime
from db.dals.META.statistic_dal_meta import StatisticDAL
from db.models.modules.modules_statistic import ModulesStatistic
from typing import Type, Optional


class ModulesStatisticDAL(StatisticDAL):
    @property
    def _table(self) -> Type[ModulesStatistic]:
        return ModulesStatistic

    async def add(self, server_id: int, position: int, status: int, message: Optional[str], data: dict,
                  time: Optional[datetime] = None):
        module_id = await ModulesInfoDAL(self._db_session).get_module_id(server_id, position)
        await self._add_statistic(
            time,
            module_id=module_id,
            status=status,
            message=message,
            data=data
        )
