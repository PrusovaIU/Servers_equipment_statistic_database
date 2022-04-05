from .__schema_name import SCHEMA
from .sockets_info import SocketsInfo
from ..meta_table import MetaTable
from datetime import datetime
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Index
from sqlalchemy import TEXT
from sqlalchemy.sql import func


class SocketsAlarm(Base, MetaTable):
    __tablename__ = "alarm"
    _schema = SCHEMA
    __ix_name = f"ix_{_schema}_{__tablename__}"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    socket_id = Column(Integer,
                       ForeignKey(f"{SocketsInfo.get_full_name()}"
                                  f".{SocketsInfo.socket_id.name}"),
                       nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    name = Column(TEXT, nullable=False)
    alarm_type = Column(TEXT, nullable=False)
    message = Column(TEXT)

    __table_args__ = (
        Index(
            f"{__ix_name}_alarm_type",
            func.to_tsvector('english', alarm_type),
            postgresql_using='gin'
        ),
        {"schema": _schema}
    )
