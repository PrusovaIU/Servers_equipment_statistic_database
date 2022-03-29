from db.config import Servers
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TEXT
from sqlalchemy import VARCHAR


class ServersInfo(Servers):
    __tablename__ = "info"
    __table_args__ = {'schema': 'servers'}

    server_id = Column(Integer, primary_key=True)
    task = Column(TEXT, nullable=False)
    host = Column(VARCHAR(length=15), nullable=False)
