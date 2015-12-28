from .player import Player


class Tournament:

    def __init__(self):
        self.players = Player()

    def generate_tournament_table(self):
        self.players.load_player('Ishino')

