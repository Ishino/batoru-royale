import random
import math


class Attributes:

    @staticmethod
    def choose_attribute_order(number_of_attributes):

        attributes_random = []
        for i in range(int(number_of_attributes)):
            attributes_random.append(i)

        random.shuffle(attributes_random)

        return attributes_random

    @staticmethod
    def generate_attribute_values(level, number_of_attributes, attributes_modifier):

        # the modifier needs to be a positive natural number
        attributes_modifier = math.floor(attributes_modifier)
        if attributes_modifier < 1:
            attributes_modifier = 1

        stat_lower = attributes_modifier * level
        stat_upper = attributes_modifier * number_of_attributes * level

        attributes_random_values = []

        rest_value = 0
        attribute_value_total = 0

        for i in range(1, int(number_of_attributes)):
            value = random.randint(rest_value, stat_upper)

            rest_value = stat_upper - value

            value += stat_lower
            if i == 1:
                value += stat_lower

            attribute_value_total += value
            attributes_random_values.append(value)

        last_attribute_value = int(stat_upper * (number_of_attributes + 1)) - attribute_value_total

        if number_of_attributes == 1:
            last_attribute_value = attributes_modifier * level * 2

        attributes_random_values.append(last_attribute_value)

        print(attributes_random_values)

        return attributes_random_values
