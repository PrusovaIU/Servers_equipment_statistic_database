from .sockets_info_dal import SocketsInfoDAL
from db.dals.dal_meta import DAL
from db.models.sockets_statistic import SocketsStatistic
from typing import Type


class SocketsStatisticDAL(DAL):
    @property
    def _table(self) -> Type[SocketsStatistic]:
        return SocketsStatistic

    async def add(self, server_id: int, port: int, status: str, direction: bool,
                  bytes_per_sec: int, packets_per_sec: int, crashed_packets_per_sec: int,
                  bytes_total: int, packets_total: int, crashed_packets_total: int):
        socket_id = await SocketsInfoDAL(self._db_session).get_socket_id(server_id, port)
        new_data = SocketsStatistic(
            socket_id=socket_id,
            status=status,
            direction=direction,
            bytes_per_sec=bytes_per_sec,
            packets_per_sec=packets_per_sec,
            crashed_packets_per_sec=crashed_packets_per_sec,
            bytes_total=bytes_total,
            packets_total=packets_total,
            crashed_packets_total=crashed_packets_total
        )
        await self._add(new_data)
