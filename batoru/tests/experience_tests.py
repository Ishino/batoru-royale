import unittest
from batoru.ningyo.experience import Experience


class TestExperience(unittest.TestCase):

    def setUp(self):
        self.experienceCalc = Experience()

    def test_calculate_experience_need(self):
        level = 1
        result = 1001
        self.experienceCalc.experience_modifier = 1000
        self.assertEqual(self.experienceCalc.calculate_experience_need(level), result)

        level = 2
        result = 5009
        self.experienceCalc.experience_modifier = 1000
        self.assertEqual(self.experienceCalc.calculate_experience_need(level), result)

        level = 3
        result = 1436
        self.experienceCalc.experience_modifier = 100
        self.assertEqual(self.experienceCalc.calculate_experience_need(level), result)

    def test_calculate_experience_gain(self):
        level = 1
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 1), 1)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 2), 7)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 3), 17)

        level = 2
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 1), 0)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 2), 4)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 3), 14)

        level = 3
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 1), 0)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 2), 0)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 3), 9)

        level = 4
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 2), 0)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 3), 2)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 4), 16)

        level = 5
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 3), 0)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 4), 7)
        self.assertEqual(self.experienceCalc.calculate_experience_gain(level, 5), 25)

if __name__ == '__main__':
    unittest.main()
