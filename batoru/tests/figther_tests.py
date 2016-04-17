import unittest
from unittest.mock import Mock

from batoru.ningyo.fighter import Fighter


class TestFighter(unittest.TestCase):

    def setUp(self):
        self.test_attributes = Mock()
        self.test_experience_calc = Mock()
        self.test_power_calc = Mock()

        self.player = Fighter(self.test_attributes)
        self.player.name = 'name'

    def test_get_max_hitpoints(self):
        self.player.stamina = 100
        self.player.hitPointsBase = 10
        self.assertEqual(self.player.get_max_hitpoints(), 1000)

    def test_advance(self):
        player_level = 10
        opponent_level = 10

        self.player.level = player_level
        self.player.experience = 10

        self.player.set_experience_calculator(self.test_experience_calc)
        self.player.experienceCalc.calculate_experience_gain.return_value = player_level + opponent_level
        self.player.experienceCalc.calculate_experience_need.return_value = player_level * 100

        self.player.advance(opponent_level)
        self.assertEqual(self.player.experience, 30)

        self.player.experienceCalc.calculate_experience_gain.assert_called_with(player_level, opponent_level)
        self.player.experienceCalc.calculate_experience_need.assert_called_with(player_level)

        # Allow the user to reach the next level.
        self.player.experienceCalc.calculate_experience_need.return_value = player_level

        self.player.advance(opponent_level)
        self.assertEqual(self.player.experience, 50)
        self.assertEqual(self.player.level, 11)

        self.player.experienceCalc.calculate_experience_gain.assert_called_with(player_level, opponent_level)
        self.player.experienceCalc.calculate_experience_need.assert_called_with(player_level)

    def test_gain_experience(self):
        self.player.experience = 10
        experience_gain = 10
        self.player.gain_experience(experience_gain)
        self.assertEqual(self.player.experience, 20)

    def test_level_up(self):
        self.player.level = 1
        self.player.level_up()
        self.assertEqual(self.player.level, 2)

    def reset_player_stats(self):
        self.player.skill = 0
        self.player.strength = 0
        self.player.stamina = 0

    def test_level_up_stats(self):
        self.player.type = 'A'
        self.reset_player_stats()
        self.player.level_up_stats()
        self.assertEqual(self.player.skill, 0)
        self.assertEqual(self.player.strength, 6)
        self.assertEqual(self.player.stamina, 6)

        self.player.type = 'B'
        self.reset_player_stats()
        self.player.level_up_stats()
        self.assertEqual(self.player.skill, 6)
        self.assertEqual(self.player.strength, 0)
        self.assertEqual(self.player.stamina, 6)

        self.player.type = 'C'
        self.reset_player_stats()
        self.player.level_up_stats()
        self.assertEqual(self.player.skill, 6)
        self.assertEqual(self.player.strength, 6)
        self.assertEqual(self.player.stamina, 0)

        self.player.type = 'D'
        self.reset_player_stats()
        self.player.level_up_stats()
        self.assertEqual(self.player.skill, 6)
        self.assertEqual(self.player.strength, 3)
        self.assertEqual(self.player.stamina, 3)

        self.player.type = 'E'
        self.reset_player_stats()
        self.player.level_up_stats()
        self.assertEqual(self.player.skill, 3)
        self.assertEqual(self.player.strength, 6)
        self.assertEqual(self.player.stamina, 3)

        self.player.type = 'F'
        self.reset_player_stats()
        self.player.level_up_stats()
        self.assertEqual(self.player.skill, 3)
        self.assertEqual(self.player.strength, 3)
        self.assertEqual(self.player.stamina, 6)

    def test_create(self):
        name = 'test name'
        level = 1
        skill_bonus = 10
        strength_bonus = 10
        stamina_bonus = 10

        self.player.attributeCalc.generate_attribute_values.return_value = [2, 2, 2]

        self.player.create(name, level, skill_bonus, strength_bonus, stamina_bonus)
        self.assertEqual(self.player.name, name)
        self.assertEqual(self.player.level, level)

        self.player.attributeCalc.generate_attribute_values.assert_called_with(level, 3, 1)

        self.assertGreaterEqual(self.player.skill, skill_bonus + 1)
        self.assertGreaterEqual(self.player.strength, strength_bonus + 1)
        self.assertGreaterEqual(self.player.stamina, stamina_bonus + 1)

    def test_calculate_stats(self):
        self.reset_player_stats()
        self.player.skill = 4
        self.player.strength = 2
        self.player.stamina = 1
        self.player.calculate_stats()

        self.assertEqual(self.player.type, 'A')
        self.assertEqual(self.player.typeStat, 4)
        self.assertEqual(self.player.fightSkill, 4)
        self.assertEqual(self.player.hitPoints, 100)

        self.reset_player_stats()
        self.player.skill = 3
        self.player.strength = 2
        self.player.stamina = 2
        self.player.calculate_stats()

        self.assertEqual(self.player.type, 'D')
        self.assertEqual(self.player.typeStat, 4)
        self.assertEqual(self.player.fightSkill, 3)
        self.assertEqual(self.player.hitPoints, 200)

        self.reset_player_stats()
        self.player.skill = 2
        self.player.strength = 4
        self.player.stamina = 1
        self.player.calculate_stats()

        self.assertEqual(self.player.type, 'B')
        self.assertEqual(self.player.typeStat, 4)
        self.assertEqual(self.player.fightSkill, 4)
        self.assertEqual(self.player.hitPoints, 100)

        self.reset_player_stats()
        self.player.skill = 2
        self.player.strength = 3
        self.player.stamina = 2
        self.player.calculate_stats()

        self.assertEqual(self.player.type, 'E')
        self.assertEqual(self.player.typeStat, 4)
        self.assertEqual(self.player.fightSkill, 3)
        self.assertEqual(self.player.hitPoints, 200)

        self.reset_player_stats()
        self.player.skill = 2
        self.player.strength = 1
        self.player.stamina = 4
        self.player.calculate_stats()

        self.assertEqual(self.player.type, 'C')
        self.assertEqual(self.player.typeStat, 4)
        self.assertEqual(self.player.fightSkill, 4)
        self.assertEqual(self.player.hitPoints, 400)

        self.reset_player_stats()
        self.player.skill = 2
        self.player.strength = 2
        self.player.stamina = 3
        self.player.calculate_stats()

        self.assertEqual(self.player.type, 'F')
        self.assertEqual(self.player.typeStat, 4)
        self.assertEqual(self.player.fightSkill, 3)
        self.assertEqual(self.player.hitPoints, 300)

if __name__ == '__main__':
    unittest.main()
