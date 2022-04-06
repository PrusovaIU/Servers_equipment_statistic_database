from .__modules_parameters_statistic_dal import ModulesParametersStatisticDAL
from .modules_info_dal import ModulesInfoDAL
from datetime import datetime
from db.dals.META.statistic_dal_meta import StatisticDAL
from db.models.modules.modules_statistic import ModulesStatistic
from typing import Type, Optional, Dict, Any


class ModulesStatisticDAL(StatisticDAL):
    @property
    def _table(self) -> Type[ModulesStatistic]:
        return ModulesStatistic

    async def add(self, server_id: int, position: int, status: int, message: Optional[str], data: Dict[str, Any],
                  time: Optional[datetime] = None):
        module_id = await ModulesInfoDAL(self._db_session).get_module_id(server_id, position)
        await self._add_statistic(
            time,
            module_id=module_id,
            status=status,
            message=message
        )
        await ModulesParametersStatisticDAL(self._db_session).add(module_id, data, time)
