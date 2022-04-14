from db.config import engine
from db.config import Base
from fastapi import FastAPI
from routers.generator import generator_router
from routers.modules import modules_router
from routers.servers import servers_router
from routers.sockets import sockets_router
from routers.tasks import tasks_router
import uvicorn


app = FastAPI()
for router in [modules_router, tasks_router, servers_router, sockets_router, generator_router]:
    app.include_router(router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=1111)
