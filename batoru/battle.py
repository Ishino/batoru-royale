from interfaces.logger import RedisLogger
from ningyo.fighter import Fighter
from ningyo.monster import Monster
from ningyo.modifiers import Accuracy, Power
from ningyo.attributes import Attributes
from combat.combat_logs import CombatLogs
from combat.combat_stats import CombatStats
from combat.combat_calculations import CombatCalculations
from simulate.tournament import Tournament, TournamentExperience
from simulate.player import Player


class Battle:
    def __init__(self):
        self.attributes = Attributes()
        self.player_engine = Player()
        self.stats = CombatStats()
        self.fight = CombatLogs()
        self.logger = RedisLogger()

        self.levelCap = 2
        self.tournament_rounds = 10

        self.main()

    def main(self):

        # name = self.player_factory.generate_player_name()
        # self.leveling(name, self.levelCap)

        tournament_round = 1

        while tournament_round <= self.tournament_rounds:
            self.tournament()
            tournament_round += 1

    def create_player(self, name):
        self.fight.logLevel = 0
        player = self.player_engine.load_player(name)

        event_text = "******************************************\nPlayer " + player.name + " created: < " + str(
            player.skill) + " ap | " + str(
            player.strength) + " str | " + str(player.stamina) + " sta | " + str(
            player.hitPoints) + " hp >\n------------------------------------------"

        self.fight.print_event(event_text, 0)

        self.stats.register_creation(player)
        return player

    def create_mob(self):
        mob = Monster(self.attributes)
        mob.set_accuracy_calculator(Accuracy())
        mob.set_power_calculator(Power())
        return mob

    def leveling(self, name, level_goal):
        self.fight.logLevel = 1

        player_one = self.create_player(name)

        player_two = self.create_mob()

        while player_one.level < level_goal:

            player_fight_id = self.logger.load_sequence(name + '_fight_count')

            event_text = "At level " + str(player_one.level) + " " + player_one.name + " has < " \
                         + str(player_one.skill) + " ap | " + str(player_one.strength) + " str | " \
                         + str(player_one.stamina) + " sta | " + str(player_one.hitPoints) + " hp | " \
                         + str(player_one.experience) + " XP | needed: " \
                         + str(player_one.experienceCalc.calculate_experience_need(player_one.level,
                                                                                   player_one.experience_modifier
                                                                                   )) + " >"
            self.fight.print_event(event_text, 1)

            player_two.generate('Ogre', player_one.level)

            self.stats.register_creation(player_two)
            event_text = "At level " + str(player_two.level) + " " + player_two.name + " has < " \
                         + str(player_two.skill) + " ap | " + str(player_two.strength) + " str | " \
                         + str(player_two.stamina) + " sta | " + str(player_two.hitPoints) + " hp >"
            self.fight.print_event(event_text, 1)
            self.battle(player_one.name + "." + str(player_fight_id), player_one, player_two)

            self.fight.print_newline = False
            self.fight.print_event(".", 0)
            mod10 = int(player_fight_id) % 200
            if mod10 == 0:
                self.fight.print_newline = True
                self.fight.print_event(" ( " + str(int(player_fight_id)) + " )", 0)

        self.fight.print_event("\n", 0)

        self.player_engine.save_player(player_one)

    def tournament(self):

        players = self.player_engine.generate_player_list(32)

        tournament = Tournament()
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
                player_one.set_experience_calculator(TournamentExperience())
                winner = self.compete(str(tournament.tournament_id) + "." + str(tournament_fight_id), player_one, player_two)
                tournament.register_win(winner.name)

                self.fight.logLevel = 1
                self.fight.print_newline = False
                self.fight.print_event(".", 0)
                mod10 = int(tournament_fight_id) % 50
                if mod10 == 0:
                    self.fight.print_newline = True
                    self.fight.print_event(" ( " + str(int(tournament_fight_id)) + " )", 0)

        self.fight.print_event(" ( " + str(int(tournament_fight_id)) + " )\n", 0)

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
        self.fight.logLevel = 0

        event_text = "After " + str(swings) + " swings, " + winner.name + " won " + str(fight_id) \
                     + "!\n******************************************"
        self.fight.print_event(event_text, 0)

        self.stats.register_fight(winner, loser, swings, fight_id, 'win')
        self.stats.register_fight(loser, winner, swings, fight_id, 'loss')

        winner.gain_experience(loser.level)

        winner.calculate_stats()
        loser.calculate_stats()

        return winner

    def battle(self, fight_id, hero: Fighter, mob: Monster):

        self.fight.enabledScroll = False
        self.fight.logLevel = 0

        swing = 1

        while True:
            skill_modifier = CombatCalculations.calc_modifier(hero.typeStat, mob.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(hero.accuracy()), int(mob.accuracy()))
            if result == 1:

                damage = hero.offence() - mob.defence()
                if damage < 1:
                    damage = 0

                hero.empower(skill_modifier)
                mob.weaken(damage, skill_modifier, swing)

                self.fight.scroll(hero, mob, damage, skill_modifier)

            elif result == 2:

                damage = mob.offence() - hero.defence()
                if damage < 1:
                    damage = 0

                mob.empower(skill_modifier, swing)
                hero.weaken(damage, skill_modifier)

                self.fight.scroll(mob, hero, damage, skill_modifier)

            else:
                self.fight.scroll(mob, hero, 0, 0)

            if mob.is_dead():
                event_text = "After " + str(swing) + " swings, " + hero.name + " won!"
                self.fight.print_event(event_text, 0)
                self.fight.print_event("******************************************", 0)
                self.stats.register_fight(hero, mob, swing, fight_id, 'win')
                hero.gain_experience(mob.level)
                hero.calculate_stats()
                return

            if hero.is_dead():
                event_text = "After " + str(swing) + " swings, " + mob.name + " won!"
                self.fight.print_event(event_text, 0)
                self.fight.print_event("******************************************", 0)
                self.stats.register_fight(hero, mob, swing, fight_id, 'loss')
                hero.calculate_stats()
                return

            swing += 1


if __name__ == "__main__":
    Battle()
