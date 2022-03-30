from .servers_info import ServersInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import REAL


class ServersStatistic(Base):
    __tablename__ = "statistic"
    __table_args__ = {"schema": "servers"}

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    server_id = Column(Integer,
                       ForeignKey(f"{ServersInfo.__table_args__['schema']}"
                                  f".{ServersInfo.__tablename__}"
                                  f".{ServersInfo.server_id.name}"),
                       nullable=False)
    workload_percentage = Column(REAL, CheckConstraint("workload_percentage >= 0"), nullable=False)
    temperature = Column(REAL)
    ram_used = Column(BigInteger, CheckConstraint("ram_used >= 0"), nullable=False)
    disk_used = Column(BigInteger, CheckConstraint("disk_used >= 0"), nullable=False)
