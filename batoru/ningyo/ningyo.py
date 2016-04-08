import math


class Ningyo:

    def __init__(self, attribute_calc):
        self.name = ''
        self.type = ''
        self.typeStat = 1
        self.level = 1

        self.fightSkill = 1
        self.skill = 1

        self.hitPointsBase = 100
        self.hitPoints = 0

        self.offenceReduction = 100
        self.defenceReduction = 100

        self.experience = 0

        self.experience_modifier = 1000

        self.number_attributes = 1

        self.attributeCalc = attribute_calc
        self.experienceCalc = None
        self.powerCalc = None
        self.accuracyCalc = None

    def set_experience_calculator(self, experience_calc):
        self.experienceCalc = experience_calc

    def set_attribute_calculator(self, attribute_calc):
        self.attributeCalc = attribute_calc

    def set_power_calculator(self, power_calc):
        self.powerCalc = power_calc

    def set_accuracy_calculator(self, accuracy_calc):
        self.accuracyCalc = accuracy_calc

    def gain_experience(self, opponent_level):
        self.experience += self.experienceCalc.calculate_experience_gain(self.level, opponent_level)

    def level_up(self, calculated_experience):
        if calculated_experience <= self.experience:
            self.level += 1
            return True
        return False

    def empower(self, skill_modifier):
        self.fightSkill = int(self.fightSkill) + int(skill_modifier)

    def weaken(self, damage, skill_modifier):
        self.hitPoints = int(self.hitPoints) - int(damage)
        self.fightSkill = int(self.fightSkill) - int(skill_modifier)
        if int(self.fightSkill) <= 0:
            self.fightSkill = 1

    def is_dead(self):
        if int(self.hitPoints) > 0:
            return False
        return True

    def accuracy(self):
        chance = math.floor(self.typeStat + self.fightSkill)
        return self.accuracyCalc.get_accuracy(chance)

    def offence(self):
        offence = self.powerCalc.get_power(self.typeStat, self.fightSkill)
        return offence

    def defence(self):
        defence = self.powerCalc.get_power(self.typeStat, self.fightSkill)
        return defence
