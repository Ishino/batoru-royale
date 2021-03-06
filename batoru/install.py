from interfaces.db import Engine
from interfaces.models.base import Base

# although we don't use them directly in the code, also import the models for which we create tables.
from ningyo.models.ningyo import Fighter
from ningyo.models.weaponry import Item
from simulator.models.tournament import Tournament, TournamentTable
from battlefront.models.player import PlayerList

db_engine = Engine()
Base.metadata.create_all(db_engine.get_engine())
print("Schema installed")
