# import math and random number functions
import random
import math
from fighter import Fighter
from combatLogs import CombatLogs
from combatStats import CombatStats


class Battle:

    levelCap = 1

    def __init__(self):
        self.levelCap = 10
        self.main()

    def main(self):
        stats = CombatStats()

        self.tournament(self.levelCap)

        tournament_stats = stats.get_stats()

        for player in tournament_stats:
            for player_type in tournament_stats[player]:
                print(str(player) + " - Type " + str(player_type) + ": " + str(tournament_stats[player][player_type]))

    def tournament(self, rounds):
        fight = CombatLogs()
        fight.logLevel = 1

        player_one = Fighter()
        player_two = Fighter()

        fight.log_event("\n******************************************", 0)
        player_one.create('Ishino', 1, 0, 0, 0)
        fight.log_event("------------------------------------------", 0)

        # for i in range(int(rounds)):
        while player_one.level < rounds:
            event_text = "At level " + str(player_one.level) + " " + player_one.name + " has < "\
                         + str(player_one.skill) + " ap | " + str(player_one.strength) + " str | "\
                         + str(player_one.stamina) + " sta | " + str(player_one.hitPoints) + " hp | "\
                         + str(player_one.experience) + " XP | needed: "\
                         + str(player_one.calculate_experience_need()) + " >"
            fight.log_event(event_text, 0)
            lower_opponent_level = player_one.level - 1
            if lower_opponent_level < 1:
                lower_opponent_level = 1
            upper_opponent_level = player_one.level + 2
            player_two_level = random.randint(lower_opponent_level, upper_opponent_level)
            player_two.create('Ogre', player_two_level, 0, 0, 0)
            event_text = "At level " + str(player_two.level) + " " + player_two.name + " has < "\
                         + str(player_two.skill) + " ap | " + str(player_two.strength) + " str | "\
                         + str(player_two.stamina) + " sta | " + str(player_two.hitPoints) + " hp >"
            fight.log_event(event_text, 0)
            self.compete(player_one, player_two)

    @staticmethod
    def fight_round(player_one_punch, player_two_punch):

        if not player_one_punch == player_two_punch:
            if player_one_punch > player_two_punch:
                return 1
            else:
                return 2
        else:
            return 0

    @staticmethod
    def calc_modifier(value_one, value_two, multiplier):
        difference = int(value_one) - int(value_two)
        modifier = math.floor(math.fabs(difference) * multiplier)
        if modifier == 0:
            modifier = 1
        return int(modifier)

    def compete(self, player_one: Fighter, player_two: Fighter):

        fight = CombatLogs()
        fight.enabledScroll = False
        fight.logLevel = 1

        stats = CombatStats()

        swing = 1

        while True:
            skill_modifier = Battle.calc_modifier(player_one.typeStat, player_two.typeStat, 0.2)

            result = self.fight_round(int(player_one.swing()), int(player_two.swing()))
            if result == 1:

                damage = player_one.punch() - player_two.block()
                if damage < 1:
                    damage = 0

                player_one.award_player(skill_modifier)
                player_two.punish_player(damage, skill_modifier)

                fight.scroll(player_one, player_two, damage, skill_modifier)

            elif result == 2:

                damage = player_two.punch() - player_one.block()
                if damage < 1:
                    damage = 0

                player_two.award_player(skill_modifier)
                player_one.punish_player(damage, skill_modifier)

                fight.scroll(player_two, player_one, damage, skill_modifier)

            else:
                fight.scroll(player_two, player_one, 0, 0)

            if not player_one.is_alive():
                event_text = "After " + str(swing) + " swings, " + player_two.name + " won!"\
                             + "\n******************************************"
                fight.log_event(event_text, 0)
                stats.register_win(player_two)
                player_one.calculate_stats()
                player_two.calculate_stats()
                return 2
            elif not player_two.is_alive():
                event_text = "After " + str(swing) + " swings, " + player_one.name + " won!"\
                             + "\n******************************************"
                fight.log_event(event_text, 0)
                stats.register_win(player_one)
                player_one.level_up(player_two.level)
                player_one.calculate_stats()
                player_two.calculate_stats()
                return 1
            swing += 1

battle = Battle()
