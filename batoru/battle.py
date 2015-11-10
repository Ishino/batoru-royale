# import random number functions
import random
import elasticsearch


from ningyo.fighter import Fighter
from ningyo.attributes import Attributes
from ningyo.experience import Experience
from combat.combat_logs import CombatLogs
from combat.combat_stats import CombatStats
from combat.combat_calculations import CombatCalculations


class Battle:

    es = elasticsearch.Elasticsearch()

    def __init__(self):
        self.attributes = Attributes()
        self.levelCap = 2
        self.main()

    def main(self):

        self.tournament(self.levelCap, 1)

        res = self.es.get(index="stats", doc_type='stat', id=1)
        print(res['_source'])

        self.es.indices.refresh(index="stats")

        res = self.es.search(index="stats", body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(timestamp)s %(player)s: %(type)s" % hit["_source"])

    def tournament(self, level_goal, tournament_id):
        fight = CombatLogs()
        fight.logLevel = 1

        player_one = Fighter(self.attributes)
        player_one.set_experience_calculator(Experience())
        player_two = Fighter(self.attributes)

        fight.log_event("tournament", "******************************************", 0)
        player_one.create('Ishino', 1, 0, 0, 0)
        fight.log_event("tournament", "------------------------------------------", 0)

        while player_one.level < level_goal:
            event_text = "At level " + str(player_one.level) + " " + player_one.name + " has < "\
                         + str(player_one.skill) + " ap | " + str(player_one.strength) + " str | "\
                         + str(player_one.stamina) + " sta | " + str(player_one.hitPoints) + " hp | "\
                         + str(player_one.experience) + " XP | needed: "\
                         + str(player_one.experienceCalc.calculate_experience_need(player_one.level,
                                                                                   player_one.experience_modifier
                                                                                   )) + " >"
            fight.log_event("tournament", event_text, 0)
            lower_opponent_level = player_one.level - 1
            if lower_opponent_level < 1:
                lower_opponent_level = 1
            upper_opponent_level = player_one.level + 2
            player_two_level = random.randint(lower_opponent_level, upper_opponent_level)
            player_two.create('Ogre', player_two_level, 0, 0, 0)
            event_text = "At level " + str(player_two.level) + " " + player_two.name + " has < "\
                         + str(player_two.skill) + " ap | " + str(player_two.strength) + " str | "\
                         + str(player_two.stamina) + " sta | " + str(player_two.hitPoints) + " hp >"
            fight.log_event("tournament", event_text, 0)
            self.compete(tournament_id, player_one, player_two)

    @staticmethod
    def compete(tournament_id, player_one: Fighter, player_two: Fighter):

        fight = CombatLogs()
        fight.enabledScroll = False
        fight.logLevel = 1

        stats = CombatStats()

        swing = 1

        while True:
            skill_modifier = CombatCalculations.calc_modifier(player_one.typeStat, player_two.typeStat, 0.2)

            result = CombatCalculations.get_highest(int(player_one.swing()), int(player_two.swing()))
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
                event_text = "After " + str(swing) + " swings, " + player_two.name + " won!"
                fight.log_event("tournament", event_text, 0)
                fight.log_event("tournament", "******************************************", 0)
                stats.register_win(player_two, tournament_id)
                player_one.calculate_stats()
                player_two.calculate_stats()
                return 2
            elif not player_two.is_alive():
                event_text = "After " + str(swing) + " swings, " + player_one.name + " won!"
                fight.log_event("tournament", event_text, 0)
                fight.log_event("tournament", "******************************************", 0)
                stats.register_win(player_one, tournament_id)
                player_one.gain_experience(player_two.level)
                player_one.calculate_stats()
                player_two.calculate_stats()
                return 1
            swing += 1

if __name__ == "__main__":
    Battle()
