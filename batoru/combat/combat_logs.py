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

        self.publish_event("\n", 0, 'fight log', '/fight', room)

        if gain > 0:
            if damage > 0:
                self.publish_event(winner.name + " has knocked " + str(damage) + " hit points from " + loser.name + "!",
                                   0, 'fight log', '/fight', room)
                event = {}
                event['name'] = winner.name
                event['damage'] = damage
                json.dumps(event)

                self.publish_event(json.dumps(event), 0, 'fight scroll', '/fight', room)
            else:
                self.publish_event(winner.name + " checked " + loser.name + " for weaknesses!", 0, 'fight log', '/fight', room)

            self.publish_event(winner.name + " gained " + str(gain) + " attack points!", 0, 'fight log', '/fight', room)
        else:
            self.publish_event("Both fighters miss their swings! Pathetic!", 0, 'fight log', '/fight', room)

        self.publish_event("After this round " + winner.name + " has < " + str(winner.fightSkill) + " ap | " + str(
            winner.hitPoints) + " hp >", 0, 'fight log', '/fight', room)
        self.publish_event("After this round " + loser.name + " has < " + str(loser.fightSkill) + " ap | " + str(
            loser.hitPoints) + " hp >", 0, 'fight log', '/fight', room)

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
                        self.socketio.emit(stream, {'data': text}, namespace=namespace, room=value)
                else:
                    self.socketio.emit(stream, {'data': text}, namespace=namespace, room=room)