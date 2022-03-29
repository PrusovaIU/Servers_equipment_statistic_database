from db.config import engine
from db.config import Base
from db.dals.servers_info_dal import ServersInfoDAL, ServersInfo
from db.dals.modules_info_dal import ModulesInfoDAL, ModulesInfo
from db.dals.tasks_update_info_dal import TasksUpdateInfoDAL, TasksUpdateInfo
from fastapi import FastAPI, HTTPException
from json import loads, JSONDecodeError
from http import HTTPStatus
from initers import get_all, get_dal, get_session
from typing import List
import uvicorn


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/servers", status_code=HTTPStatus.CREATED)
async def add_server(server_id: int, task_name: str, host: str):
    async with get_session() as session:
        servers_info_dal = ServersInfoDAL(session)
        return await servers_info_dal.add_server(server_id, task_name, host)


@app.get("/servers")
async def get_all_servers() -> List[ServersInfo]:
    return await get_all(ServersInfoDAL)


@app.post("/modules", status_code=HTTPStatus.CREATED)
async def add_module(server_id: int, position: int, module_type: str):
    async with get_session() as session:
        modules_info_dal = ModulesInfoDAL(session)
        return await modules_info_dal.add_module(server_id, position, module_type)


@app.get("/modules")
async def get_all_modules() -> List[ModulesInfo]:
    return await get_all(ModulesInfoDAL)


@app.get("/module")
async def get_module(server_id: int, position: int):
    async with get_dal(ModulesInfoDAL) as dal:
        return await dal.get_module(server_id, position)


@app.post("/update_task", status_code=HTTPStatus.CREATED)
async def update_task(server_id: int, configuration: str):
    try:
        config_dict = loads(configuration)
        async with get_dal(TasksUpdateInfoDAL) as dal:
            return await dal.add_info(server_id, config_dict)
    except JSONDecodeError as err:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=f"Configuration error: {err}")


@app.get("/task_history/servers/{server_id}")
async def get_history_of_server_task(server_id: int):
    async with get_dal(TasksUpdateInfoDAL) as dal:
        return await dal.get_history(server_id)


@app.get("/task_history/tasks/{task_name}")
async def get_history_of_task(task_name: str):
    async with get_dal(TasksUpdateInfoDAL) as dal:
        return await dal.get_history_of_task(task_name)


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=1111)
