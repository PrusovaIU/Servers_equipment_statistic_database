from .__schema_name import SCHEMA
from ..meta_table import MetaTable
from datetime import datetime
from db.models.servers.servers_info import ServersInfo
from db.config import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger


class TasksStatistic(Base, MetaTable):
    __tablename__ = "statistic"
    _schema = SCHEMA
    __table_args__ = {
        "schema": _schema
    }

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    server_id = Column(Integer,
                       ForeignKey(f"{ServersInfo.get_full_name()}"
                                  f".{ServersInfo.server_id.name}"),
                       nullable=False)
    speed_in = Column(BigInteger, CheckConstraint("speed_in >= 0"))
    speed_out = Column(BigInteger, CheckConstraint("speed_out >= 0"))
    total_in = Column(BigInteger, CheckConstraint("total_in >= 0"))
    total_out = Column(BigInteger, CheckConstraint("total_out >= 0"))
    total_dropped = Column(BigInteger, CheckConstraint("total_dropped >= 0"))
