from db.dals.tasks.tasks_update_info_dal import TasksUpdateInfoDAL
from fastapi import APIRouter, HTTPException
from json import loads, JSONDecodeError
from http import HTTPStatus
from initers import get_dal


tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("/update", status_code=HTTPStatus.CREATED)
async def update_task(server_id: int, configuration: str):
    try:
        config_dict = loads(configuration)
        async with get_dal(TasksUpdateInfoDAL) as dal:
            return await dal.add_info(server_id, config_dict)
    except JSONDecodeError as err:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=f"Configuration error: {err}")


@tasks_router.get("/history/servers/{server_id}")
async def get_history_of_server_task(server_id: int):
    async with get_dal(TasksUpdateInfoDAL) as dal:
        return await dal.get_history(server_id)


@tasks_router.get("/history/tasks/{task_name}")
async def get_history_of_task(task_name: str):
    async with get_dal(TasksUpdateInfoDAL) as dal:
        return await dal.get_history_of_task(task_name)
