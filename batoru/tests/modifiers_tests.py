import unittest
from batoru.ningyo.modifiers import Power, PowerAbility, Accuracy


class TestExperience(unittest.TestCase):

    def setUp(self):
        self.accuracy = Accuracy()
        self.power = Power()
        self.power_ability = PowerAbility()

    def test_accuracy_set_accuracy_modifier(self):
        value = 100
        self.accuracy.set_accuracy_modifier(value)
        self.assertEqual(self.accuracy.accuracyModifier, value)

    def test_accuracy_get_accuracy(self):
        self.assertLessEqual(self.accuracy.get_accuracy(1, 1), 2)
        self.assertGreaterEqual(self.accuracy.get_accuracy(1, 1), 0)

    def test_power_set_power_modifier(self):
        value = 100
        self.power.set_power_modifier(value)
        self.assertEqual(self.power.powerModifier, value)

    def test_power_set_power_reduction(self):
        value = 100
        self.power.set_power_reduction(value)
        self.assertEqual(self.power.powerReduction, value)

    def test_power_get_power(self):
        power = 100
        energy = 100
        self.power.set_power_modifier(1)
        self.power.set_power_reduction(1)
        self.assertEqual(self.power.get_power(power, energy), 200)

    def test_power_ability_get_power(self):
        power = 100
        energy = 100
        self.power_ability.ticker = self.power_ability.abilityPointRefresh + 1
        self.power_ability.set_power_modifier(1)
        self.power_ability.set_power_reduction(1)
        self.assertEqual(self.power_ability.get_power(power, energy), 200)
        self.power_ability.ticker = self.power_ability.abilityPointRefresh
        self.assertEqual(self.power_ability.get_power(power, energy), 400)


if __name__ == '__main__':
    unittest.main()
