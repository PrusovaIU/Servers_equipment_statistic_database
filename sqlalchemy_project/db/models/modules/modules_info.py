from .__schema_name import SCHEMA
from ..meta_table import MetaTable
from db.config import Base
from db.models.servers.servers_info import ServersInfo
from sqlalchemy import CheckConstraint
from sqlalchemy import Index
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TEXT


class ModulesInfo(Base, MetaTable):
    __tablename__ = "info"
    _schema = SCHEMA

    module_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(
        Integer,
        ForeignKey(f"{ServersInfo.get_full_name()}"
                   f".{ServersInfo.server_id.name}"),
        nullable=False,
        index=True
    )
    position = Column(Integer, CheckConstraint("position>=0"), nullable=False)
    module_type = Column(TEXT, nullable=False)

    __table_args__ = (
        Index("server_id_position_idx", server_id, position, unique=True),
        {"schema": _schema}
    )
