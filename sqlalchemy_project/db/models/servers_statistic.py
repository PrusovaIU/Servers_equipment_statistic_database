from .servers_info import ServersInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import REAL


class ServersStatistic(Base):
    __tablename__ = "info"
    __table_args__ = {'schema': 'servers'}

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    server_id = Column(Integer,
                       ForeignKey(f"{ServersInfo.__table_args__['schema']}"
                                  f".{ServersInfo.__tablename__}"
                                  f".{ServersInfo.server_id.name}"),
                       nullable=False)
    workload_percentage = Column(REAL, CheckConstraint("workload_percentage >= 0"), nullable=False)
    temperature = Column(REAL)
    RAM_used = Column(Integer, CheckConstraint("RAM_used >= 0"), nullable=False)
    disk_used = Column(Integer, CheckConstraint("disk_used >= 0"), nullable=False)
