import math


class CombatCalculations:

    @staticmethod
    def get_highest(value_one, value_two):
        if not value_one == value_two:
            if value_one > value_two:
                return 1
            else:
                return 2
        else:
            return 0

    @staticmethod
    def calc_modifier(value_one, value_two, multiplier):
        difference = int(value_one) - int(value_two)
        modifier = math.floor(math.fabs(difference) * multiplier)
        if modifier == 0:
            modifier = 1
        return int(modifier)
