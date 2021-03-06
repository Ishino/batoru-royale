import random
import math


class Accuracy:

    def __init__(self):
        self.accuracyModifier = 1

    def set_accuracy_modifier(self, value):
        self.accuracyModifier = value

    def get_accuracy(self, power, energy):
        value = power + energy
        accuracy = random.randint(0, value) * self.accuracyModifier
        return accuracy


class Power:

    def __init__(self):
        self.base = 10
        self.powerModifier = 1
        self.powerReduction = 1

    def set_power_modifier(self, value):
        self.powerModifier = value

    def set_power_reduction(self, value):
        self.powerReduction = value

    def get_power(self, power, energy):
        power_modifier = (energy * self.powerModifier) / self.powerReduction
        power = math.floor(math.fabs(power + power_modifier))
        return power


class PowerAbility(Power):

    def __init__(self):
        self.ability = 0
        self.abilityPointRefresh = 3
        self.ticker = 0
        Power.__init__(self)

    def get_power(self, power, energy):
        power = Power.get_power(self, power, energy)

        if self.ticker % self.abilityPointRefresh == 0:
            self.ability += 1

        if self.ability > 0:
            power += power

        self.ticker += 1

        return power
