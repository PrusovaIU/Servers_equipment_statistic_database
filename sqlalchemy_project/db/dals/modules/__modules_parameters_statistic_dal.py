from .modules_info_dal import ModulesInfoDAL
from datetime import datetime
from db.dals.META.statistic_dal_meta import StatisticDAL
from db.models.modules.modules_parameter_statistic import ModulesParametersStatistic
from numbers import Number
from typing import Type, Dict, Any, Optional


class ModulesParametersStatisticDAL(StatisticDAL):
    @property
    def _table(self) -> Type[ModulesParametersStatistic]:
        return ModulesParametersStatistic

    async def add(self, module_id: int, data: Dict[str, Any], time: Optional[datetime] = None,
                  parent_name: Optional[str] = None):
        for parameter, value in data.items():
            if isinstance(value, dict):
                await self.add(module_id, value, time, parameter)
                value = None
            await self._add_statistic(
                time,
                module_id=module_id,
                parameter_name=parameter,
                parent_parameter=parent_name,
                value=value
            )
