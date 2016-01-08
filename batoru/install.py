from interfaces.db import Engine
from interfaces.models.base import Base

# although we don't use them directly in the code, also import the models for which we create tables.
from ningyo.models.ningyo import Fighter
from simulate.models.tournament import Tournament, TournamentTable

db_engine = Engine()
Base.metadata.create_all(db_engine.get_engine())
