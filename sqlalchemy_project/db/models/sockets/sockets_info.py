from db.config import Base
from db.models.servers.servers_info import ServersInfo
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TEXT


class SocketsInfo(Base):
    __tablename__ = "info"
    __table_args__ = {"schema": "sockets"}

    socket_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer,
                       ForeignKey(f"{ServersInfo.__table_args__['schema']}"
                                  f".{ServersInfo.__tablename__}"
                                  f".{ServersInfo.server_id.name}"),
                       nullable=False)
    name = Column(TEXT, nullable=False)
    port = Column(Integer, CheckConstraint("port>=0"), nullable=False)
    socket_type = Column(TEXT, nullable=False)
