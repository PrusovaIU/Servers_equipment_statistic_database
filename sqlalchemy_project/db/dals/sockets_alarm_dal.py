from .sockets_info_dal import SocketsInfoDAL
from datetime import datetime
from db.dals.statistic_dal_meta import StatisticDAL
from db.models.sockets_alarm import SocketsAlarm
from typing import Type


class SocketsAlarmDAL(StatisticDAL):
    @property
    def _table(self) -> Type[SocketsAlarm]:
        return SocketsAlarm

    async def add(self, server_id: int, port: int, name: str, alarm_type: str, message: str, time: datetime):
        socket_id = await SocketsInfoDAL(self._db_session).get_socket_id(server_id, port)
        await self._add_statistic(
            time,
            socket_id=socket_id,
            name=name,
            alarm_type=alarm_type,
            message=message
        )
