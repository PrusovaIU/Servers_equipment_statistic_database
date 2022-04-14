from .__modules_parameters_statistic_dal import ModulesParametersStatisticDAL
from .modules_info_dal import ModulesInfoDAL, ModulesInfo
from datetime import datetime
from db.dals.META.statistic_dal_meta import StatisticDAL
from db.models.modules.modules_statistic import ModulesStatistic
from sqlalchemy import select, insert
from sqlalchemy.sql.expression import SelectBase
from typing import Type, Optional, Dict, Any


class ModulesStatisticDAL(StatisticDAL):
    @property
    def _table(self) -> Type[ModulesStatistic]:
        return ModulesStatistic

    # async def add(self, server_id: int, position: int, status: int, message: Optional[str], data: Dict[str, Any],
    #               time: Optional[datetime] = None):
        # module_id = await ModulesInfoDAL(self._db_session).get_module_id(server_id, position)
        # await self._add_statistic(
        #     time,
        #     module_id=module_id,
        #     status=status,
        #     message=message
        # )
        # await ModulesParametersStatisticDAL(self._db_session).add(module_id, data, time)
    # async def add(self, server_id: int, position: int, status: int, message: Optional[str]):
    #     statement = insert(ModulesStatistic).values(
    #         module_id=SelectBase.scalar_subquery(
    #             select(ModulesInfo.module_id)
    #             .where(ModulesInfo.server_id == server_id)
    #             .where(ModulesInfo.position == position)
    #         ),
    #         status=status,
    #         message=message
    #     )
    #     await self._db_session.execute(statement)
    #     await self._db_session.flush()

    async def add(self, server_id: int, position: int, status: int, message: Optional[str],
                  time: Optional[datetime] = None):
        # module_id = await ModulesInfoDAL(self._db_session).get_module_id(server_id, position)
        await self._add_statistic(
            time,
            module_id=SelectBase.scalar_subquery(
                select(ModulesInfo.module_id)
                .where(ModulesInfo.server_id == server_id)
                .where(ModulesInfo.position == position)
            ),
            status=status,
            message=message
        )
        # await ModulesParametersStatisticDAL(self._db_session).add(module_id, data, time)

