import unittest
from batoru.ningyo.fighter import Fighter
from batoru.ningyo.attributes import Attributes


class TestFighter(unittest.TestCase):

    def setUp(self):
        attributes = Attributes()
        self.player = Fighter(attributes)
        self.player.name = 'name'

    def test_get_max_hitpoints(self):
        self.player.stamina = 100
        self.player.hitPointsBase = 10
        self.assertEqual(self.player.get_max_hitpoints(), 1000)

if __name__ == '__main__':
    unittest.main()
