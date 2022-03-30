from .servers_info import ServersInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


class TasksStatistic(Base):
    __tablename__ = "statistic"
    __table_args__ = {'schema': 'tasks'}

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    server_id = Column(Integer,
                       ForeignKey(f"{ServersInfo.__table_args__['schema']}"
                                  f".{ServersInfo.__tablename__}"
                                  f".{ServersInfo.server_id.name}"),
                       nullable=False)
    speed_in = Column(Integer, CheckConstraint("speed_in >= 0"))
    speed_out = Column(Integer, CheckConstraint("speed_out >= 0"))
    total_in = Column(Integer, CheckConstraint("total >= 0"))
    total_out = Column(Integer, CheckConstraint("total_out >= 0"))
    total_dropped = Column(Integer, CheckConstraint("total_dropped >= 0"))
