import json

from interfaces.logger import RedisLogger
from ningyo.experience import Experience


# We are simulating a round-robin tournament with X players.
# See https://en.wikipedia.org/wiki/Round-robin_tournament
# Followed by a double-elimination tournament with the top Y players.
# See https://en.wikipedia.org/wiki/Double-elimination_tournament
class Tournament:

    def __init__(self):
        self.players = []
        self.tournament_table = []
        self.tournament_id = 1

        self.redis_logger = RedisLogger()

        self.start_tournament()

    def start_tournament(self):
        self.tournament_id = self.redis_logger.load_sequence('tournament_id')

    def set_player_list(self, players):
        self.players = players

    def generate_tournament_table(self):
        n = len(self.players)
        for i in range(n - 1):

            mid = n / 2
            l1 = self.players[:int(mid)]
            l2 = self.players[int(mid):]
            l2.reverse()

            # Switch sides after each round
            if i % 2 == 1:
                self.tournament_table.append(zip(l1, l2))
            else:
                self.tournament_table.append(zip(l2, l1))
            self.players.insert(1, self.players.pop())

        return self.tournament_table

    def register_win(self, name):
        tournament = self.redis_logger.load('tournament_' + str(self.tournament_id))

        stored_tournament = {}
        if tournament is not None:
            stored_tournament = json.loads(tournament)

        if name in stored_tournament:
            stored_tournament[name] += 1
        else:
            stored_tournament[name] = 1
        stored_tournament = json.dumps(stored_tournament)
        print(stored_tournament)
        self.redis_logger.write('tournament_' + str(self.tournament_id), stored_tournament)


class TournamentExperience(Experience):

    @staticmethod
    def calculate_experience_gain(tournament_round, opponent_level):
        experience_gain = opponent_level * opponent_level + tournament_round * tournament_round

        return experience_gain
