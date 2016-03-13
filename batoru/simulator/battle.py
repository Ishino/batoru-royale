from interfaces.logger import RedisLogger
from ningyo.fighter import Fighter
from ningyo.monster import Monster
from ningyo.modifiers import Accuracy, Power
from ningyo.attributes import Attributes
from combat.combat_logs import CombatLogs
from combat.combat_stats import CombatStats
from combat.combat_calculations import CombatCalculations
from simulator.tournament import Tournament, TournamentExperience
from simulator.player import Player


class Battle:
    def __init__(self):
        self.attributes = Attributes()
        self.player_engine = Player()
        self.stats = CombatStats()
        self.fight = CombatLogs()
        self.logger = RedisLogger()

        self.level_gain = 1
        self.tournament_rounds = 1

        self.room = ''

    def simulate(self, name='', battle_type='single', room=''):
        self.room = room
        if battle_type == 'single':
            # Single fight with scroll
            if name == '':
                name = self.player_engine.generate_player_name()
            self.kill_monster(name)

        if battle_type == 'level':
            if name == '':
                name = self.player_engine.generate_player_name()
            self.leveling(name, self.level_gain)

        if battle_type == 'tournament':
            tournament_round = 1

            while tournament_round <= self.tournament_rounds:
                self.tournament()
                tournament_round += 1

    def kill_monster(self, name):
        self.fight.logLevel = 2

        player_one = self.create_player(name)

        player_two = self.create_mob()
        player_two.levelUp = 0
        player_two.generate('Ogre', player_one.level)

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

        action = 'loaded'
        if player.experience == 0:
            action = 'created'

        event_text = ">> Player " + player.name + " " + action + ": " + self.get_player_status(player)
        self.fight.publish_event(event_text, 0, 'fight status', '/fight', self.room)

        self.stats.register_creation(player)
        return player

    def create_mob(self):
        mob = Monster(self.attributes)
        mob.set_accuracy_calculator(Accuracy())
        mob.set_power_calculator(Power())
        return mob

    def leveling(self, name, level_gain):
        self.fight.logLevel = 1

        hero = self.create_player(name)
        level_goal = hero.level + level_gain

        mob = self.create_mob()

        while hero.level < level_goal:

            player_fight_id = self.logger.load_sequence(name + '_fight_count')

            mob.generate('Ogre', hero.level)

            self.stats.register_creation(mob)
            event_text = "At level " + str(mob.level) + " " + mob.name + " has < " \
                         + str(mob.skill) + " ap | " + str(mob.strength) + " str | " \
                         + str(mob.stamina) + " sta | " + str(mob.hitPoints) + " hp >"
            self.fight.print_event(event_text, 1)
            self.battle(hero.name + "." + str(player_fight_id), hero, mob)

            if mob.is_dead():
                self.fight.publish_event(self.get_player_status(hero), 0, 'fight log', '/fight', self.room)

            self.fight.print_newline = False
            self.fight.print_event(".", 1)
            mod10 = int(player_fight_id) % 200
            if mod10 == 0:
                self.fight.print_newline = True
                self.fight.print_event(" ( " + str(int(player_fight_id)) + " )", 1)

        self.fight.print_event("\n", 1)
        self.player_engine.save_player(hero)
        self.fight.publish_event(self.get_player_status(hero), 0, 'fight status', '/fight', self.room)

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

    def tournament(self):

        competition_id = 2

        tournament = Tournament()
        players = self.player_engine.use_player_list(competition_id, 6)
        tournament.set_player_list(players)
        table = tournament.generate_tournament_table()

        tournament_fight_id = 0

        for tournament_round in table:
            for match in tournament_round:
                tournament_fight_id = self.logger.load_sequence(
                    'tournament_' + str(tournament.tournament_id) + '_fight_count')
                player_one = self.create_player(match[0])
                player_one.set_experience_calculator(TournamentExperience())
                player_two = self.create_player(match[1])
                player_two.set_experience_calculator(TournamentExperience())
                winner = self.compete(str(tournament.tournament_id) + "." +
                                      str(tournament_fight_id), player_one, player_two)
                tournament.register_win(winner.name)

                self.fight.logLevel = 1
                self.fight.print_newline = False
                self.fight.print_event(".", 0)
                mod10 = int(tournament_fight_id) % 50
                if mod10 == 0:
                    self.fight.print_newline = True
                    self.fight.print_event(" ( " + str(int(tournament_fight_id)) + " )", 0)

        self.fight.print_event(" ( " + str(int(tournament_fight_id)) + " )\n", 0)

        for player in players:
            fighter = self.player_engine.load_player(player)
            self.fight.publish_event(" [ " + str(fighter.name) + " ] level: " + str(fighter.level) + " exp: " +
                                     str(fighter.experience) + "/" +
                                     str(TournamentExperience().calculate_experience_need(
                                         fighter.level, fighter.experience_modifier)) +
                                     " type: " + str(fighter.type), 0, 'fight log', '/fight', self.room)

    def compete(self, fight_id, player_one: Fighter, player_two: Fighter):

        self.fight.enabledScroll = False

        swing = 1

        while True:
            skill_modifier = CombatCalculations.calc_modifier(player_one.typeStat, player_two.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(player_one.accuracy()), int(player_two.accuracy()))
            if result == 1:

                damage = player_one.offence() - player_two.defence()
                if damage < 1:
                    damage = 0

                player_one.empower(skill_modifier)
                player_two.weaken(damage, skill_modifier)

                self.fight.scroll(player_one, player_two, damage, skill_modifier)

            elif result == 2:

                damage = player_two.offence() - player_one.defence()
                if damage < 1:
                    damage = 0

                player_two.empower(skill_modifier)
                player_one.weaken(damage, skill_modifier)

                self.fight.scroll(player_two, player_one, damage, skill_modifier)

            else:
                self.fight.scroll(player_two, player_one, 0, 0)

            if player_two.is_dead():
                return self.save_result(fight_id, player_one, player_two, swing)

            if player_one.is_dead():
                return self.save_result(fight_id, player_two, player_one, swing)

            swing += 1

    def save_result(self, fight_id, winner, loser, swings):

        event_text = "After " + str(swings) + " swings, " + winner.name + " won " + str(fight_id) + "!"
        self.fight.publish_event(event_text, 0, 'fight status', '/fight', self.room)

        self.stats.register_fight(winner, loser, swings, fight_id, 'win')
        self.stats.register_fight(loser, winner, swings, fight_id, 'loss')

        winner.gain_experience(loser.level)

        winner.calculate_stats()
        loser.calculate_stats()

        self.player_engine.save_player(winner)
        self.player_engine.save_player(loser)

        return winner

    def battle(self, fight_id, hero: Fighter, mob: Monster, scroll=False):

        self.fight.enabledScroll = False

        swing = 1

        while True:
            skill_modifier = CombatCalculations.calc_modifier(hero.typeStat, mob.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(hero.accuracy()), int(mob.accuracy()))
            if result == 1:

                damage = hero.offence() - mob.defence()
                if damage < 1:
                    damage = 0

                hero.empower(skill_modifier)
                mob.weaken(damage, skill_modifier)

                self.fight.scroll(hero, mob, damage, skill_modifier, self.room)

            elif result == 2:

                damage = mob.offence() - hero.defence()
                if damage < 1:
                    damage = 0

                mob.empower(skill_modifier)
                hero.weaken(damage, skill_modifier)

                self.fight.scroll(mob, hero, damage, skill_modifier, self.room)

            else:
                self.fight.scroll(mob, hero, 0, 0, self.room)

            if mob.is_dead():
                event_text = "After " + str(swing) + " swings, " + hero.name + " won!"
                self.fight.publish_event(event_text, 1, 'fight log', '/fight', self.room)
                self.stats.register_fight(hero, mob, swing, fight_id, 'win')
                hero.gain_experience(mob.level)
                hero.calculate_stats()
                return

            if hero.is_dead():
                event_text = "After " + str(swing) + " swings, " + mob.name + " won!"
                self.fight.publish_event(event_text, 1, 'fight log', '/fight', self.room)
                self.stats.register_fight(hero, mob, swing, fight_id, 'loss')
                hero.calculate_stats()
                return

            swing += 1


if __name__ == "__main__":
    Battle()