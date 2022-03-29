from .servers_info import ServersInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import Integer


class TasksUpdateInfo(Base):
    __tablename__ = "update_info"
    __table_args__ = {'schema': 'tasks'}

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    server_id = Column(Integer,
                       ForeignKey(f"{ServersInfo.__table_args__['schema']}"
                                  f".{ServersInfo.__tablename__}"
                                  f".{ServersInfo.server_id.name}"),
                       nullable=False)
    task_configuration = Column(JSON, nullable=False)
