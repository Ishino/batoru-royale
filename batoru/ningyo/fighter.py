import random
from . import Ningyo


class Fighter(Ningyo):
    def __init__(self, attribute_calc):
        Ningyo.__init__(self, attribute_calc)
        self.type = None

        self.strength = 1
        self.stamina = 1

        self.experience = 0

        self.attributeCalc = attribute_calc

    def set_experience_calculator(self, experience_calc):
        self.experienceCalc = experience_calc

    def set_attribute_calculator(self, attribute_calc):
        self.attributeCalc = attribute_calc

    def gain_experience(self, opponent_level):

        self.experience += self.experienceCalc.calculate_experience_gain(self.level, opponent_level)
        if self.level_up(self.experienceCalc.calculate_experience_need(self.level)):
            self.level_up_stats()

    def level_up(self, calculated_experience):
        if calculated_experience <= self.experience:
            self.level += 1
            return True
        return False

    def offence(self):
        offence = self.powerCalc.get_power(self.strength, self.fightSkill)
        return offence

    def defence(self):
        self.powerCalc.powerReduction = 0.4
        defence = self.powerCalc.get_power(self.stamina, self.fightSkill)
        return defence

    def level_up_stats(self):
        if self.type == 'A':
            self.strength += 6
            self.stamina += 6

        if self.type == 'B':
            self.stamina += 6
            self.skill += 6

        if self.type == 'C':
            self.skill += 6
            self.strength += 6

        if self.type == 'D':
            self.skill += 6
            self.strength += 3
            self.stamina += 3

        if self.type == 'E':
            self.skill += 3
            self.strength += 6
            self.stamina += 3

        if self.type == 'F':
            self.skill += 3
            self.strength += 3
            self.stamina += 6

        self.calculate_stats()

    def create(self, name, start_level, skill_bonus, strength_bonus, stamina_bonus):

        self.name = str(name)

        self.level = start_level

        number_attributes = 3
        attributes_modifier = 1

        random_attribute_values = self.attributeCalc.generate_attribute_values(
            self.level, number_attributes, attributes_modifier
        )

        random.shuffle(random_attribute_values)

        (self.skill, self.strength, self.stamina) = random_attribute_values

        self.skill += skill_bonus
        self.strength += strength_bonus
        self.stamina += stamina_bonus

        self.calculate_stats()

    def calculate_stats(self):
        self.hitPoints = self.hitPointsBase * self.stamina
        self.fightSkill = self.skill

        primary_stat = self.skill
        secondary_stat = (self.strength + self.stamina)
        primary_type = 'A'
        secondary_type = 'D'

        if self.strength > primary_stat:
            primary_stat = self.strength
            secondary_stat = (self.skill + self.stamina)
            primary_type = 'B'
            secondary_type = 'E'

        if self.stamina > primary_stat:
            primary_stat = self.stamina
            secondary_stat = (self.strength + self.skill)
            primary_type = 'C'
            secondary_type = 'F'

        self.type = primary_type
        self.typeStat = primary_stat
        self.fightSkill = primary_stat

        if secondary_stat > primary_stat:
            self.typeStat = secondary_stat
            self.type = secondary_type
