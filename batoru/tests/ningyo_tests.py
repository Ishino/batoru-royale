import unittest
from unittest.mock import Mock

from batoru.ningyo.ningyo import Ningyo


class TestNingyo(unittest.TestCase):

    def setUp(self):
        self.test_attributes = Mock()
        self.test_accuracy = Mock()
        self.test_power = Mock()
        self.test_experience_calc = Mock()

        self.player = Ningyo(self.test_attributes)
        self.player.name = 'name'
        self.player.set_accuracy_calculator(self.test_accuracy)
        self.player.set_power_calculator(self.test_power)

    def test_set_experience_calculator(self):
        self.player.set_experience_calculator(self.test_experience_calc)
        self.assertTrue(self.player.experienceCalc.get_me())

    def test_set_attribute_calculator(self):

        self.player.set_attribute_calculator(self.test_attributes())
        self.assertTrue(self.player.attributeCalc.get_me())

    def test_is_dead(self):
        self.player.hitPoints = 1
        self.assertFalse(self.player.is_dead())

        self.player.hitPoints = 0
        self.assertTrue(self.player.is_dead())

        self.player.hitPoints = -1
        self.assertTrue(self.player.is_dead())

    def test_empower(self):
        self.player.fightSkill = 1
        self.player.empower(1)
        self.assertEqual(self.player.fightSkill, 2)

    def test_weaken(self):
        self.player.fightSkill = 2
        self.player.hitPoints = 2

        self.player.weaken(1, 1)
        self.assertEqual(self.player.fightSkill, 1)
        self.assertEqual(self.player.hitPoints, 1)

        self.player.weaken(1, 1)
        self.assertEqual(self.player.fightSkill, 1)
        self.assertEqual(self.player.hitPoints, 0)

        self.player.weaken(1, 1)
        self.assertEqual(self.player.fightSkill, 1)
        self.assertEqual(self.player.hitPoints, -1)

    def test_offence(self):

        self.player.typeStat = 1
        self.player.fightSkill = 1
        self.player.offence()
        self.player.powerCalc.get_power.assert_called_with(self.player.typeStat, self.player.fightSkill)

    def test_defence(self):

        self.player.typeStat = 1
        self.player.fightSkill = 1
        self.player.defence()
        self.player.powerCalc.get_power.assert_called_with(self.player.typeStat, self.player.fightSkill)

    def test_accuracy(self):
        self.player.typeStat = 1
        self.player.fightSkill = 1
        self.player.accuracy()
        self.player.accuracyCalc.get_accuracy.assert_called_with(self.player.typeStat, self.player.fightSkill)


if __name__ == '__main__':
    unittest.main()
