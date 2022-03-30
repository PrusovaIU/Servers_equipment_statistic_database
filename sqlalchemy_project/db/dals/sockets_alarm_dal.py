from .sockets_info_dal import SocketsInfoDAL
from db.dals.dal_meta import DAL
from db.models.sockets_alarm import SocketsAlarm
from typing import Type


class SocketsAlarmDAL(DAL):
    @property
    def _table(self) -> Type[SocketsAlarm]:
        return SocketsAlarm

    async def add(self, server_id: int, port: int, name: str, alarm_type: str, message: str):
        socket_id = await SocketsInfoDAL(self._db_session).get_socket_id(server_id, port)
        new_data = SocketsAlarm(
            socket_id=socket_id,
            name=name,
            alarm_type=alarm_type,
            message=message
        )
        await self._add(new_data)
