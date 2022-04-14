from db.dals.modules.modules_info_dal import ModulesInfoDAL, ModulesInfo
from db.dals.modules.modules_statistic_dal import ModulesStatisticDAL
from fastapi import APIRouter
from http import HTTPStatus
from initers import get_all, get_dal, get_session
from typing import List, Optional


modules_router = APIRouter(prefix="/modules")


@modules_router.post("/", status_code=HTTPStatus.CREATED)
async def add_module(server_id: int, position: int, module_type: str):
    async with get_session() as session:
        modules_info_dal = ModulesInfoDAL(session)
        return await modules_info_dal.add_module(server_id, position, module_type)


@modules_router.get("/")
async def get_all_modules() -> List[ModulesInfo]:
    return await get_all(ModulesInfoDAL)


@modules_router.get("/module")
async def get_module(server_id: int, position: int):
    async with get_dal(ModulesInfoDAL) as dal:
        return await dal.get_module(server_id, position)


@modules_router.get("/module/id")
async def get_module(server_id: int, position: int):
    async with get_dal(ModulesInfoDAL) as dal:
        return await dal.get_module_id(server_id, position)


@modules_router.post("/statistic")
async def add_module_statistic(server_id: int, position: int, status: int, message: Optional[str] = None):
    async with get_dal(ModulesStatisticDAL) as dal:
        return await dal.add(server_id, position, status, message)
