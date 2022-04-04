from .__schema_name import SCHEMA
from .sockets_info import SocketsInfo
from ..meta_table import MetaTable
from datetime import datetime
from db.config import Base
from sqlalchemy import BOOLEAN
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import TEXT


class SocketsStatistic(Base, MetaTable):
    __tablename__ = "statistic"
    _schema = SCHEMA
    __table_args__ = {
        "schema": _schema
    }

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    socket_id = Column(Integer,
                       ForeignKey(f"{SocketsInfo.get_full_name()}"
                                  f".{SocketsInfo.socket_id.name}"),
                       nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    status = Column(TEXT, nullable=False)
    direction = Column(BOOLEAN)
    bytes_per_sec = Column(BigInteger, CheckConstraint("bytes_per_sec >= 0"))
    packets_per_sec = Column(BigInteger, CheckConstraint("packets_per_sec >= 0"))
    crashed_packets_per_sec = Column(BigInteger, CheckConstraint("crashed_packets_per_sec >= 0"))
    bytes_total = Column(BigInteger, CheckConstraint("bytes_total >= 0"))
    packets_total = Column(BigInteger, CheckConstraint("packets_total >= 0"))
    crashed_packets_total = Column(BigInteger, CheckConstraint("crashed_packets_total >= 0"))
