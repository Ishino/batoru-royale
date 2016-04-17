import unittest
import math
from batoru.ningyo.attributes import Attributes


class TestAttributes(unittest.TestCase):
    def setUp(self):
        self.attributes_calc = Attributes()

    def test_choose_attribute_order(self):
        number_attributes = 5
        random_attributes = self.attributes_calc.choose_attribute_order(number_attributes)

        self.assertEqual(len(random_attributes), number_attributes)

        i = 1
        while i <= number_attributes:
            self.assertTrue(1 in random_attributes)
            i += 1

    def test_generate_attribute_values(self):
        attributes_modifier = 1

        y = 1
        while y < 100:
            level = y
            z = 1
            while z < 20:
                while attributes_modifier < 3:
                    number_of_attributes = z
                    random_attributes_values = self.attributes_calc.generate_attribute_values(
                        level, number_of_attributes, attributes_modifier
                    )

                    # the modifier needs to be a positive natural number
                    calc_attributes_modifier = math.floor(attributes_modifier)
                    if calc_attributes_modifier < 1:
                        calc_attributes_modifier = 1

                    level_modifier = calc_attributes_modifier * level

                    self.assertEqual(len(random_attributes_values), number_of_attributes)

                    i = 0
                    while i < number_of_attributes:
                        self.assertGreater(random_attributes_values[i], 0)
                        self.assertGreaterEqual(random_attributes_values[i], level_modifier)
                        if i == 0:
                            self.assertGreaterEqual(random_attributes_values[i], level_modifier * 2)
                        i += 1

                    total = level_modifier * number_of_attributes * (number_of_attributes + 1)
                    if number_of_attributes == 1:
                        total = level_modifier * 2

                    total_values = 0
                    i = 0

                    while i < len(random_attributes_values):
                        total_values += int(random_attributes_values[i])
                        i += 1

                    self.assertEqual(total, total_values)

                    attributes_modifier += 0.5

                z += 1

            y += 1
