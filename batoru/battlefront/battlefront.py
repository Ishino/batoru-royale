import json

from interfaces.logger import RedisLogger
from flask_socketio import SocketIO


class Battlefront:

    def __init__(self):
        self.redis_logger = RedisLogger()
        self.war = 'global'
        self.socketio = SocketIO(message_queue='redis://localhost:6379/0')

        self.battlefront_key = 'battlefront_' + str(self.war)

    def add_player(self, player, room):
        battlefront = self.redis_logger.load(self.battlefront_key)

        stored_battlefront = {}
        if battlefront is not None:
            stored_battlefront = json.loads(battlefront)

        stored_battlefront[player] = room

        battlefront = json.dumps(stored_battlefront)
        self.redis_logger.write(self.battlefront_key, battlefront)

    def remove_player(self, name):
        battlefront = self.redis_logger.load(self.battlefront_key)

        stored_battlefront = {}
        if battlefront is not None:
            stored_battlefront = json.loads(battlefront)

        stored_battlefront.pop(name, None)

        battlefront = json.dumps(stored_battlefront)
        self.redis_logger.write(self.battlefront_key, battlefront)

    def get_player_by_room(self, room):
        battlefront = self.redis_logger.load(self.battlefront_key)

        stored_battlefront = {}
        if battlefront is not None:
            stored_battlefront = json.loads(battlefront)

        for key, value in stored_battlefront.items():
            if value == room:
                return str(key)

        return None

    def get_player_list(self):
        battlefront = self.redis_logger.load(self.battlefront_key)

        stored_battlefront = {}
        if battlefront is not None:
            stored_battlefront = json.loads(battlefront)

        return stored_battlefront

    def create_battle_field(self, player, target):
        return