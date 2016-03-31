import time
import json

from interfaces.logger import Logger
from flask_socketio import SocketIO


class CombatLogs:

    def __init__(self):
        self.enabledScroll = True
        self.verboseEvent = True
        self.scrollSpeed = 0.4
        self.print_newline = True

        self.logLevel = 1
        self.logger = Logger()

        self.socketio = SocketIO(message_queue='redis://localhost:6379/0')

    def set_logger(self, logger: Logger):
        self.logger = logger

    def scroll(self, winner, loser, damage, gain, room=None):

        if not self.enabledScroll:
            return

        event = {'winner': {'name': winner.name, 'hit_points': winner.hitPoints, 'skill_points': winner.fightSkill,
                            'skill': winner.skill},
                 'loser': {'name': loser.name, 'hit_points': loser.hitPoints, 'skill_points': loser.fightSkill,
                           'skill': loser.skill},
                 'damage': damage, 'gain': gain}

        self.publish_event(json.dumps(event), 0, 'fight scroll', '/fight', room)

        time.sleep(self.scrollSpeed)

    def log_event(self, key, text, level):

        if level < self.logLevel:
            self.logger.write(key, text)

    def print_event(self, text, level):
        if level < self.logLevel:
            print(text, end="", flush=True)
            if self.print_newline:
                print("\n", end="")

    def publish_event(self, text, level, stream='stream', namespace='', room=None):
        if level < self.logLevel:
            if not room:
                self.socketio.emit(stream, {'data': text}, namespace=namespace, broadcast=True)
            else:
                if type(room) is dict:
                    for key, value in room.items():
                        if value is not None:
                            self.socketio.emit(stream, {'data': text}, namespace=namespace, room=value)
                else:
                    self.socketio.emit(stream, {'data': text}, namespace=namespace, room=room)
