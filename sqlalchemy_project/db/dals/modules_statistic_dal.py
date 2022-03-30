from .modules_info_dal import ModulesInfoDAL
from db.dals.dal_meta import DAL
from db.models.modules_statistic import ModulesStatistic
from typing import Type, Optional


class ModulesStatisticDAL(DAL):
    @property
    def _table(self) -> Type[ModulesStatistic]:
        return ModulesStatistic

    async def add(self, server_id: int, position: int, status: int, message: Optional[str], data: dict):
        module_id = await ModulesInfoDAL(self._db_session).get_module_id(server_id, position)
        new_data = ModulesStatistic(
            module_id=module_id,
            status=status,
            message=message,
            data=data
        )
        await self._add(new_data)
