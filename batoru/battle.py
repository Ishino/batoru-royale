from interfaces.logger import RedisLogger

from ningyo.fighter import Fighter
from ningyo.monster import Monster
from ningyo.modifiers import Accuracy, Power
from ningyo.attributes import Attributes

from combat.combat_logs import CombatLogs
from combat.combat_stats import CombatStats
from combat.combat_calculations import CombatCalculations

from tournament.tournament import Tournament


class Battle:

    def __init__(self):
        self.attributes = Attributes()
        self.levelCap = 10
        self.tournament_rounds = 3
        self.main()

    def main(self):

        logger = RedisLogger()
        tournament_round = 1

        while tournament_round <= self.tournament_rounds:

            tournament_id = logger.load_sequence("tournament_id")

            self.tournament(self.levelCap, tournament_id, tournament_round)
            tournament_round += 1

    def tournament(self, level_goal, tournament_id, tournament_round):
        tournament = Tournament()

        fight = CombatLogs()
        fight.logLevel = 1

        stats = CombatStats()

        player_one = tournament.load_player('Ishino_' + str(tournament_round))

        player_two = Monster(self.attributes)
        player_two.set_accuarcy_calculator(Accuracy())
        player_two.set_power_calculator(Power())

        fight.print_event("******************************************", 0)
        fight.print_event("Player " + player_one.name + " created: < "\
                         + str(player_one.skill) + " ap | " + str(player_one.strength) + " str | "\
                         + str(player_one.stamina) + " sta | " + str(player_one.hitPoints) + " hp >", 0)
        fight.print_event("------------------------------------------", 0)

        stats.register_creation(player_one)

        fight_id = 1

        while player_one.level < level_goal:
            event_text = "At level " + str(player_one.level) + " " + player_one.name + " has < "\
                         + str(player_one.skill) + " ap | " + str(player_one.strength) + " str | "\
                         + str(player_one.stamina) + " sta | " + str(player_one.hitPoints) + " hp | "\
                         + str(player_one.experience) + " XP | needed: "\
                         + str(player_one.experienceCalc.calculate_experience_need(player_one.level,
                                                                                   player_one.experience_modifier
                                                                                   )) + " >"
            fight.print_event(event_text, 1)

            player_two.generate('Ogre', player_one.level)

            stats.register_creation(player_two)
            event_text = "At level " + str(player_two.level) + " " + player_two.name + " has < "\
                         + str(player_two.skill) + " ap | " + str(player_two.strength) + " str | "\
                         + str(player_two.stamina) + " sta | " + str(player_two.hitPoints) + " hp >"
            fight.print_event(event_text, 1)
            self.compete(str(tournament_id) + "." + str(fight_id), player_one, player_two)

            fight.print_newline = False
            fight.print_event(".", 0)
            mod10 = fight_id % 200
            if mod10 == 0:
                fight.print_newline = True
                fight.print_event(" ( " + str(fight_id) + " )", 0)
            fight_id += 1

        fight.print_event("\n", 0)

        tournament.save_player(player_one)


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
