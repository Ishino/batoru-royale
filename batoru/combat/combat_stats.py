import datetime

from interfaces.logger import RedisLogger, ElasticSearchLogger


class CombatStats:

    @staticmethod
    def register_fight(player, opponent, swings, fight_id, outcome):

        outcome_value = -1
        if outcome == 'win':
            outcome_value = 1

        win_doc = {
            'fighter_name': player.name,
            'fighter_type': player.type,
            'fighter_level': player.level,
            'opponent_name': opponent.name,
            'opponent_type': opponent.type,
            'opponent_level': opponent.level,
            'swings': swings,
            'outcome': outcome,
            'outcome_value': outcome_value,
            'timestamp': datetime.datetime.now(),
        }

        elastic_search_logger = ElasticSearchLogger('fights', 'fight')
        elastic_search_logger.write(fight_id, win_doc)

    @staticmethod
    def register_creation(player):

        redis_logger = RedisLogger()
        character_id = redis_logger.load_sequence(player.name)

        character_doc = {
            'character_name': player.name,
            'character_type': player.type,
            'character_level': player.level,
            'timestamp': datetime.datetime.now(),
        }

        elastic_search_logger = ElasticSearchLogger('creation', 'character')
        elastic_search_logger.write(character_id, character_doc)
