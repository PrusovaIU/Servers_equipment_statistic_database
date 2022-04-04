from .__schema_name import SCHEMA
from ..meta_table import MetaTable
from datetime import datetime
from db.config import Base
from db.models.servers.servers_info import ServersInfo
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import Integer


class TasksUpdateInfo(Base, MetaTable):
    __tablename__ = "update_info"
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
    task_configuration = Column(JSON, nullable=False)
