from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from interfaces.models.base import Base


class Fighter(Base):
    __tablename__ = 'fighter'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    level = Column(String)
    skill = Column(Integer)
    strength = Column(Integer)
    stamina = Column(Integer)
    hitpoints = Column(Integer)
    experience = Column(Integer)
    tournament_table = relationship("TournamentTable")
