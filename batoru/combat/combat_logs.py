import time
from interfaces.logger import Logger
from flask_socketio import SocketIO
from server.batoru_front import app


class CombatLogs:

    def __init__(self):
        self.enabledScroll = True
        self.verboseEvent = True
        self.scrollSpeed = 0.4
        self.print_newline = True

        self.logLevel = 1
        self.logger = Logger()

        self.socketio = SocketIO(app, message_queue='redis://localhost:6379/0')

    def set_logger(self, logger: Logger):
        self.logger = logger

    def scroll(self, winner, loser, damage, gain):

        if not self.enabledScroll:
            return

        if gain > 0:
            if damage > 0:
                self.publish_event(winner.name + " has knocked " + str(damage) + " hit points from " + loser.name + "!",
                                   0)
            else:
                self.publish_event(winner.name + " checked " + loser.name + " for weaknesses!", 0)

            self.publish_event(winner.name + " gained " + str(gain) + " attack points!", 0)
        else:
            self.publish_event("Both fighters miss their swings! Pathetic!", 0)

        self.publish_event("After this round " + winner.name + " has < " + str(winner.fightSkill) + " ap | " + str(
            winner.hitPoints) + " hp >", 0)
        self.publish_event("After this round " + loser.name + " has < " + str(loser.fightSkill) + " ap | " + str(
            loser.hitPoints) + " hp >", 0)
        self.publish_event("\n", 0)

        time.sleep(self.scrollSpeed)

    def log_event(self, key, text, level):

        if level < self.logLevel:
            self.logger.write(key, text)

    def print_event(self, text, level):
        if level < self.logLevel:
            print(text, end="", flush=True)
            if self.print_newline:
                print("\n", end="")

    def publish_event(self, text, level):
        if level < self.logLevel:
            self.socketio.emit('my response', {'data': text}, namespace='/fight')
