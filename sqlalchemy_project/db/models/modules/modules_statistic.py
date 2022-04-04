from .__schema_name import SCHEMA
from ..meta_table import MetaTable
from .modules_info import ModulesInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import Integer
from sqlalchemy import TEXT


class ModulesStatistic(Base, MetaTable):
    __tablename__ = "statistic"
    _schema = SCHEMA
    __table_args__ = {
        "schema": _schema
    }

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    module_id = Column(Integer,
                       ForeignKey(f"{ModulesInfo.get_full_name()}"
                                  f".{ModulesInfo.module_id.name}"))
    status = Column(Integer, nullable=False)
    message = Column(TEXT)
    data = Column(JSON)
