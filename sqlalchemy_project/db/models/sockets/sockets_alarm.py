from .__schema_name import SCHEMA
from .sockets_info import SocketsInfo
from ..meta_table import MetaTable
from datetime import datetime
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TEXT


class SocketsAlarm(Base, MetaTable):
    __tablename__ = "alarm"
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
    name = Column(TEXT, nullable=False)
    alarm_type = Column(TEXT, nullable=False)
    message = Column(TEXT)
