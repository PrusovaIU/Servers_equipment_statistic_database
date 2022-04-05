from .__schema_name import SCHEMA
from ..meta_table import MetaTable
from db.config import Base
from db.models.servers.servers_info import ServersInfo
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import TEXT
from sqlalchemy.sql import func


class SocketsInfo(Base, MetaTable):
    __tablename__ = "info"
    _schema = SCHEMA
    __ix_name = f"ix_{_schema}_{__tablename__}"

    socket_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(
        Integer,
        ForeignKey(f"{ServersInfo.get_full_name()}"
                   f".{ServersInfo.server_id.name}"),
        nullable=False,
        index=True
    )
    name = Column(TEXT, nullable=False)
    port = Column(Integer, CheckConstraint("port>=0"), nullable=False)
    socket_type = Column(TEXT, nullable=False)

    __table_args__ = (
        Index(f"{__ix_name}_server_id_port", server_id, port, unique=True),
        Index(
            f"{__ix_name}_socket_type",
            func.to_tsvector('english', socket_type),
            postgresql_using='gin'
        ),
        {"schema": _schema}
    )
