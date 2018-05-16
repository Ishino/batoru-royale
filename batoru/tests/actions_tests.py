import unittest
from batoru.combat.combat_calculations import CombatCalculations
from batoru.ningyo.actions import Actions


class TestActions(unittest.TestCase):
    def setUp(self):
        self.actions = Actions(CombatCalculations())


if __name__ == '__main__':
    unittest.main()
