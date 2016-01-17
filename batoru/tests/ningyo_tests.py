import unittest
from batoru.ningyo.ningyo import Ningyo
from batoru.ningyo.attributes import Attributes
from batoru.ningyo.modifiers import Accuracy, Power


class TestNingyo(unittest.TestCase):

    def setUp(self):
        attributes = Attributes()
        self.player = Ningyo(attributes)
        self.player.name = 'name'
        self.player.set_accuracy_calculator(Accuracy())
        self.player.set_power_calculator(Power())

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
        self.assertEqual(self.player.fightSkill, 0)
        self.assertEqual(self.player.hitPoints, 0)

        self.player.weaken(1, 1)
        self.assertEqual(self.player.fightSkill, 0)
        self.assertEqual(self.player.hitPoints, -1)

    def test_offence(self):

        self.player.skill = 1
        self.player.strengthMultiplier = 1
        self.player.offenceReduction = 1
        self.player.fightSkill = 1
        self.player.ability = 0
        self.assertEqual(self.player.offence(), 1)

    def test_defence(self):

        self.player.skill = 1
        self.player.staminaMultiplier = 1
        self.player.defenceReduction = 1
        self.player.fightSkill = 1
        self.player.ability = 0
        self.assertEqual(self.player.defence(), 1)

if __name__ == '__main__':
    unittest.main()
