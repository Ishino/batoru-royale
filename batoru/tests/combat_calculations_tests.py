import unittest
from batoru.combat.combat_calculations import CombatCalculations


class TestCombatCalculations(unittest.TestCase):

    def test_get_highest(self):
        self.assertEqual(CombatCalculations.get_highest(1, 2), 2)
        self.assertEqual(CombatCalculations.get_highest(2, 2), 0)
        self.assertEqual(CombatCalculations.get_highest(2, 1), 1)

    def test_calc_modifier(self):
        self.assertEqual(CombatCalculations.calc_modifier(1, 1, 1), 1)
        self.assertEqual(CombatCalculations.calc_modifier(1, 1, 0), 1)
        self.assertEqual(CombatCalculations.calc_modifier(4, 2, 1), 2)
        self.assertEqual(CombatCalculations.calc_modifier(8, 2, 0.5), 3)
        self.assertEqual(CombatCalculations.calc_modifier(2, 8, 0.5), 3)


if __name__ == '__main__':
    unittest.main()
