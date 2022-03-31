from .modules_info import ModulesInfo
from datetime import datetime
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import Integer
from sqlalchemy import TEXT


class ModulesStatistic(Base):
    __tablename__ = "statistic"
    __table_args__ = {'schema': 'modules'}

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.utcnow)
    module_id = Column(Integer,
                       ForeignKey(f"{ModulesInfo.__table_args__['schema']}"
                                  f".{ModulesInfo.__tablename__}"
                                  f".{ModulesInfo.module_id.name}"))
    status = Column(Integer, nullable=False)
    message = Column(TEXT)
    data = Column(JSON)
