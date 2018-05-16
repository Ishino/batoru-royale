from sqlalchemy import Column, Integer, String
from interfaces.models.base import Base


class PlayerList(Base):
    __tablename__ = 'playerlist'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer)
    name = Column(String)
