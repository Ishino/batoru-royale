import random
from . import Ningyo


class Fighter(Ningyo):
    def __init__(self, attribute_calc):
        Ningyo.__init__(self, attribute_calc)

        self.number_attributes = 3
        self.strength = 1
        self.stamina = 1

        self.experience = 0

    def advance(self, opponent_level):
        experience_gain = self.experienceCalc.calculate_experience_gain(self.level, opponent_level)
        experience_need = self.experienceCalc.calculate_experience_need(self.level)

        self.gain_experience(experience_gain)

        if experience_need < self.experience:
            self.level_up()
            self.level_up_stats()
            self.calculate_stats()

    def gain_experience(self, experience):
        self.experience += experience

    def level_up(self):
        self.level += 1

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
        self.hitPoints = self.get_max_hitpoints()
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

    def get_max_hitpoints(self):
        return self.hitPointsBase * self.stamina
