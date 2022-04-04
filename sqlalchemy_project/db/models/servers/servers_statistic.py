from .__schema_name import SCHEMA
from .servers_info import ServersInfo
from ..meta_table import MetaTable
from datetime import datetime
from db.config import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import REAL


class ServersStatistic(Base, MetaTable):
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
    workload_percentage = Column(REAL, CheckConstraint("workload_percentage >= 0"), nullable=False)
    temperature = Column(REAL)
    ram_used = Column(BigInteger, CheckConstraint("ram_used >= 0"), nullable=False)
    disk_used = Column(BigInteger, CheckConstraint("disk_used >= 0"), nullable=False)
