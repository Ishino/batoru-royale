from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from interfaces.models.base import Base


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class TournamentTable(Base):
    __tablename__ = 'tournament_table'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    fighter_id = Column(Integer, ForeignKey('fighter.id'))
    tournament = relationship("Tournament")
    fighter = relationship("Fighter")
