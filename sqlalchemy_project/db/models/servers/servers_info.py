from .__schema_name import SCHEMA
from ..meta_table import MetaTable
from db.config import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TEXT
from sqlalchemy import VARCHAR


class ServersInfo(Base, MetaTable):
    __tablename__ = "info"
    _schema = SCHEMA
    __table_args__ = {
        "schema": _schema
    }

    server_id = Column(Integer, primary_key=True)
    task = Column(TEXT, nullable=False)
    host = Column(VARCHAR(length=15), nullable=False)
