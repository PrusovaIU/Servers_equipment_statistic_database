from db.dals.META.dal_meta import DAL
from db.models.modules.modules_info import ModulesInfo
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.future import select
from typing import Type


class ModulesInfoDAL(DAL):
    @property
    def _table(self) -> Type[ModulesInfo]:
        return ModulesInfo

    async def add_module(self, server_id: int, position: int, module_type: str):
        new_module = ModulesInfo(
            server_id=server_id,
            position=position,
            module_type=module_type
        )
        await self._add(new_module)
        # if await self.get_module(server_id, position) is None:
        #     new_module = ModulesInfo(
        #         server_id=server_id,
        #         position=position,
        #         module_type=module_type
        #     )
        #     await self._add(new_module)
        # else:
        #     raise HTTPException(status_code=HTTPStatus.CONFLICT,
        #                         detail=f"There is module on server {server_id} in position {position}")

    async def get_module(self, server_id: int, position: int):
        query = await self._db_session.execute(
            select(self._table)
            .where(self._table.server_id == server_id)
            .where(self._table.position == position)
        )
        return query.first()

    async def get_module_id(self, server_id: int, position: int) -> int:
        statement = select(self._table.module_id)\
            .where(self._table.server_id == server_id)\
            .where(self._table.position == position)
        return await self._get_id(statement,
                                  f"Module on server {server_id} in position {position} has not been registered")
