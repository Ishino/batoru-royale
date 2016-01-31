from interfaces.db import Engine
from interfaces.models.base import Base

# although we don't use them directly in the code, also import the models for which we create tables.
from ningyo.models.ningyo import Fighter
from simulator.models.tournament import Tournament, TournamentTable
from simulator.models.player import PlayerList

db_engine = Engine()
Base.metadata.create_all(db_engine.get_engine())
