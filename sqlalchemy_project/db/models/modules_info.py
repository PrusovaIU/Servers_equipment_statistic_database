from db.config import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TEXT


class ModulesInfo(Base):
    __tablename__ = "info"
    __table_args__ = {'schema': 'modules'}

    module_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey("servers.info.server_id"), nullable=False)
    position = Column(Integer, CheckConstraint("position>=0"), nullable=False)
    module_type = Column(TEXT, nullable=False)
