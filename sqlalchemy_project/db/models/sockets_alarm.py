from .sockets_info import SocketsInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TEXT


class SocketsAlarm(Base):
    __tablename__ = "alarm"
    __table_args__ = {"schema": "sockets"}

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    socket_id = Column(Integer,
                       ForeignKey(f"{SocketsInfo.__table_args__['schema']}"
                                  f".{SocketsInfo.__tablename__}"
                                  f".{SocketsInfo.socket_id.name}"),
                       nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    name = Column(TEXT, nullable=False)
    alarm_type = Column(TEXT, nullable=False)
    message = Column(TEXT)
