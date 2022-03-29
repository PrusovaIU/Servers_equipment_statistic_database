from db.models.servers_info import ServersInfo
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import List


class ServersInfoDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_server(self, server_id: int, task_name: str, host: str):
        new_server = ServersInfo(
            server_id=server_id,
            task=task_name,
            host=host
        )
        self.db_session.add(new_server)
        await self.db_session.flush()

    async def get_all_servers(self) -> List[ServersInfo]:
        query = await self.db_session.execute(
            select(ServersInfo)
        )
        return query.scalars().all()
