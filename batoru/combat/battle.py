import pika
import json

from interfaces.logger import RedisLogger
from ningyo.fighter import Fighter
from ningyo.monster import Monster
from ningyo.modifiers import Accuracy, Power
from ningyo.attributes import Attributes
from combat.combat_logs import CombatLogs
from combat.combat_stats import CombatStats
from combat.combat_calculations import CombatCalculations
from battlefront.player import Player
from battlefront.battlefront import Battlefront


class Battle:
    def __init__(self):
        self.attributes = Attributes()
        self.player_engine = Player()
        self.stats = CombatStats()
        self.fight = CombatLogs()
        self.logger = RedisLogger()
        self.room = None
        self.opponent_room = None
        self.front = Battlefront()

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.player_one = None
        self.player_two = None

    def engage(self, name, opponent='monster', room=None):

        self.room = room
        self.channel.queue_declare(queue=self.room)

        pvp = True

        if name == '':
            name = self.player_engine.generate_player_name()

        if opponent == 'monster':
            pvp = False
            # Single fight with scroll
            self.kill_monster(name)

        if pvp:

            player_list = self.front.get_player_list()
            self.opponent_room = player_list[opponent]

            self.channel.queue_declare(queue=self.opponent_room)
            self.kill_player(name, opponent)

    def command(self, message):

        print(message)

        player = None

        if message['player'] == self.player_one.name:
            player = self.player_one

        if message['player'] == self.player_two.name:
            player = self.player_two

        if message['command'] == 'heal':
            if player is not None:
                player.hitPoints = player.hitPointsBase * player.stamina

        if message['command'] == 'boost':
            if player is not None:
                player.fightSkill = player.fightSkill * player.chanceMultiplier

        if message['player'] == self.player_one.name:
            self.player_one = player

        if message['player'] == self.player_two.name:
            self.player_two = player

    def kill_player(self, name, opponent):
        self.fight.logLevel = 2

        player_one = self.create_player(name)
        player_two = self.create_player(opponent)

        player_fight_id = self.logger.load_sequence(name + '_fight_count')
        self.compete(player_one.name + "." + str(player_fight_id), player_one, player_two, True)
        self.player_engine.save_player(player_one)
        self.player_engine.save_player(player_two)

    def kill_monster(self, name):
        self.fight.logLevel = 2

        player_one = self.create_player(name)

        player_two = self.create_mob()
        player_two.levelUp = 0
        player_two.generate('Ogre', player_one.level)

        player_two_obj = {'name': player_two.name,
                          'level': player_two.level,
                          'hit_points': player_two.hitPoints,
                          'skill_points': player_two.skill,
                          'strength': player_two.strength,
                          'stamina': player_two.stamina
                          }

        self.fight.publish_event(json.dumps(player_two_obj), 0, 'fight front', '/fight', self.room)

        event_text = ">> Player " + player_two.name + " created: < level " + str(
            player_two.level) + " | " + str(
            player_two.skill) + " ap | " + str(
            player_two.strength) + " str | " + str(player_two.stamina) + " sta | " + \
            str(player_two.hitPoints) + " hp >"

        self.fight.publish_event(event_text, 0, 'fight status', '/fight', self.room)

        player_fight_id = self.logger.load_sequence(name + '_fight_count')
        self.battle(player_one.name + "." + str(player_fight_id), player_one, player_two, True)
        self.player_engine.save_player(player_one)

    def create_player(self, name):
        player = self.player_engine.load_player(name)

        player_obj = {'name': player.name,
                      'level': player.level,
                      'hit_points': player.hitPoints,
                      'skill_points': player.skill,
                      'strength': player.strength,
                      'stamina': player.stamina,
                      'experience': player.experience,
                      'experience_needed': player.experienceCalc.calculate_experience_need(player.level,
                                                                                           player.experience_modifier
                                                                                           )
                      }

        self.fight.publish_event(json.dumps(player_obj), 0, 'fight front', '/fight', {0: self.room, 1: self.opponent_room})

        action = 'loaded'
        if player.experience == 0:
            action = 'created'

        event_text = ">> Player " + player.name + " " + action + ": " + self.get_player_status(player)
        self.fight.publish_event(event_text, 0, 'fight status', '/fight', {0: self.room, 1: self.opponent_room})

        self.stats.register_creation(player)
        return player

    def create_mob(self):
        mob = Monster(self.attributes)
        mob.set_accuracy_calculator(Accuracy())
        mob.set_power_calculator(Power())
        return mob

    @staticmethod
    def get_player_status(player):
        player_status_text = "At level " + str(player.level) + " " + player.name + " has < " \
                             + str(player.skill) + " ap | " + str(player.strength) + " str | " \
                             + str(player.stamina) + " sta | " + str(player.hitPoints) + " hp | " \
                             + str(player.experience) + " XP | needed: " \
                             + str(player.experienceCalc.calculate_experience_need(player.level,
                                                                                   player.experience_modifier
                                                                                   )) + " >"
        return player_status_text

    def compete(self, fight_id, player_one: Fighter, player_two: Fighter, scroll=False):

        self.player_one = player_one
        self.player_two = player_two

        self.fight.enabledScroll = scroll
        self.fight.scrollSpeed = 2

        swing = 1

        while True:
            method_frame, header_frame, body = self.channel.basic_get(self.room)

            if method_frame:
                message = json.loads(body.decode('utf-8'))
                self.command(message)
                self.channel.basic_ack(method_frame.delivery_tag)
            else:
                print('No message returned')

            method_frame, header_frame, body = self.channel.basic_get(self.opponent_room)

            if method_frame:
                message = json.loads(body.decode('utf-8'))
                self.command(message)
                self.channel.basic_ack(method_frame.delivery_tag)
            else:
                print('No message returned')

            skill_modifier = CombatCalculations.calc_modifier(self.player_one.typeStat, self.player_two.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(self.player_one.accuracy()), int(self.player_two.accuracy()))
            if result == 1:

                damage = self.player_one.offence() - self.player_two.defence()
                if damage < 1:
                    damage = 0

                self.player_one.empower(skill_modifier)
                self.player_two.weaken(damage, skill_modifier)

                self.fight.scroll(self.player_one, self.player_two, damage, skill_modifier,
                                  {0: self.room, 1: self.opponent_room})

            elif result == 2:

                damage = self.player_two.offence() - self.player_one.defence()
                if damage < 1:
                    damage = 0

                self.player_two.empower(skill_modifier)
                self.player_one.weaken(damage, skill_modifier)

                self.fight.scroll(self.player_two, self.player_one, damage, skill_modifier,
                                  {0: self.room, 1: self.opponent_room})

            else:
                self.fight.scroll(self.player_two, self.player_one, 0, 0, {0: self.room, 1: self.opponent_room})

            if player_two.is_dead():
                return self.save_result(fight_id, self.player_one, self.player_two, swing)

            if player_one.is_dead():
                return self.save_result(fight_id, self.player_two, self.player_one, swing)

            swing += 1

    def save_result(self, fight_id, winner, loser, swings):

        event_text = "After " + str(swings) + " swings, " + winner.name + " won!"

        self.fight.publish_event(event_text, 0, 'fight log', '/fight', {0: self.room, 1: self.opponent_room})

        self.stats.register_fight(winner, loser, swings, fight_id, 'win')
        self.stats.register_fight(loser, winner, swings, fight_id, 'loss')

        winner.gain_experience(loser.level)

        winner.calculate_stats()
        loser.calculate_stats()

        self.player_engine.save_player(winner)
        self.player_engine.save_player(loser)

        return winner

    def battle(self, fight_id, hero: Fighter, mob: Monster, scroll=False):

        self.player_one = hero
        self.player_two = mob

        self.fight.enabledScroll = scroll
        self.fight.scrollSpeed = 2

        swing = 1

        while True:
            method_frame, header_frame, body = self.channel.basic_get(self.room)

            if method_frame:
                message = json.loads(body.decode('utf-8'))
                self.command(message)
                self.channel.basic_ack(method_frame.delivery_tag)
            else:
                print('No message returned')

            skill_modifier = CombatCalculations.calc_modifier(self.player_one.typeStat, mob.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(self.player_one.accuracy()), int(mob.accuracy()))
            if result == 1:

                damage = self.player_one.offence() - mob.defence()
                if damage < 1:
                    damage = 0

                self.player_one.empower(skill_modifier)
                mob.weaken(damage, skill_modifier)

                self.fight.scroll(self.player_one, mob, damage, skill_modifier, self.room)

            elif result == 2:

                damage = mob.offence() - self.player_one.defence()
                if damage < 1:
                    damage = 0

                mob.empower(skill_modifier)
                hero.weaken(damage, skill_modifier)

                self.fight.scroll(mob, self.player_one, damage, skill_modifier, self.room)

            else:
                self.fight.scroll(mob, self.player_one, 0, 0, self.room)

            if mob.is_dead():
                event_text = "After " + str(swing) + " swings, " + self.player_one.name + " won!"
                self.fight.publish_event(event_text, 1, 'fight log', '/fight', self.room)
                self.stats.register_fight(self.player_one, mob, swing, fight_id, 'win')
                hero.gain_experience(mob.level)
                hero.calculate_stats()
                return

            if self.player_one.is_dead():
                event_text = "After " + str(swing) + " swings, " + mob.name + " won!"
                self.fight.publish_event(event_text, 1, 'fight log', '/fight', self.room)
                self.stats.register_fight(self.player_one, mob, swing, fight_id, 'loss')
                self.player_one.calculate_stats()
                return

            swing += 1

        self.channel.stop_consuming()


if __name__ == "__main__":
    Battle()
