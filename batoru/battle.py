from interfaces.logger import RedisLogger
from ningyo.fighter import Fighter
from ningyo.monster import Monster
from ningyo.modifiers import Accuracy, Power
from ningyo.attributes import Attributes
from combat.combat_logs import CombatLogs
from combat.combat_stats import CombatStats
from combat.combat_calculations import CombatCalculations
from simulate.tournament import Tournament
from simulate.player import Player


class Battle:
    def __init__(self):
        self.attributes = Attributes()
        self.player_factory = Player()
        self.stats = CombatStats()
        self.fight = CombatLogs()
        self.logger = RedisLogger()

        self.levelCap = 2
        self.tournament_rounds = 10

        self.main()

    def main(self):

        name = self.player_factory.generate_player_name()
        self.leveling(name, self.levelCap)

        # tournament_round = 1
        #
        # while tournament_round <= self.tournament_rounds:
        #     tournament_id = self.logger.load_sequence("tournament_id")
        #
        #     self.tournament(self.levelCap, tournament_id, tournament_round)
        #     tournament_round += 1

    def create_player(self, name):
        player = self.player_factory.load_player(name)

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
            self.compete(str(int(player_fight_id)), player_one, player_two)

            self.fight.print_newline = False
            self.fight.print_event(".", 0)
            mod10 = int(player_fight_id) % 200
            if mod10 == 0:
                self.fight.print_newline = True
                self.fight.print_event(" ( " + str(int(player_fight_id)) + " )", 0)

        self.fight.print_event("\n", 0)

        self.player_factory.save_player(player_one)

    def tournament(self, level_goal, tournament_id, tournament_round):
        # tournament = Tournament()
        # players = tournament.generate_tournament_table()
        return

    @staticmethod
    def compete(fight_id, hero: Fighter, mob: Monster):

        fight = CombatLogs()
        fight.enabledScroll = False
        fight.logLevel = 0

        stats = CombatStats()

        swing = 1

        while True:
            skill_modifier = CombatCalculations.calc_modifier(hero.typeStat, mob.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(hero.accuracy()), int(mob.accuracy()))
            if result == 1:

                damage = hero.offence() - mob.defence()
                if damage < 1:
                    damage = 0

                hero.empower(skill_modifier, swing)
                mob.weaken(damage, skill_modifier, swing)

                fight.scroll(hero, mob, damage, skill_modifier)

            elif result == 2:

                damage = mob.offence() - hero.defence()
                if damage < 1:
                    damage = 0

                mob.empower(skill_modifier, swing)
                hero.weaken(damage, skill_modifier, swing)

                fight.scroll(mob, hero, damage, skill_modifier)

            else:
                fight.scroll(mob, hero, 0, 0)

            if mob.is_dead():
                event_text = "After " + str(swing) + " swings, " + hero.name + " won!"
                fight.log_event("tournament", event_text, 0)
                fight.log_event("tournament", "******************************************", 0)
                stats.register_fight(hero, mob, swing, fight_id, 'win')
                hero.gain_experience(mob.level)
                hero.calculate_stats()
                return

            if hero.is_dead():
                event_text = "After " + str(swing) + " swings, " + mob.name + " won!"
                fight.log_event("tournament", event_text, 0)
                fight.log_event("tournament", "******************************************", 0)
                stats.register_fight(hero, mob, swing, fight_id, 'loss')
                hero.calculate_stats()
                return

            swing += 1


if __name__ == "__main__":
    Battle()
