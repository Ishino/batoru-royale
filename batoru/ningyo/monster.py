import random
from . import Ningyo


class Monster(Ningyo):
    def __init__(self, attribute_calc):
        Ningyo.__init__(self, attribute_calc)

        self.levelDown = 1
        self.levelUp = 2

        self.strength = 1
        self.stamina = 1

        self.strengthMultiplier = 10
        self.staminaMultiplier = 100
        self.chanceMultiplier = 1

        self.attributeCalc = attribute_calc

        self.ability = 0

    def set_attribute_calculator(self, attribute_calc):
        self.attributeCalc = attribute_calc

    def generate(self, name, level):

        lower_opponent_level = level - self.levelDown
        if lower_opponent_level < 1:
            lower_opponent_level = 1
        upper_opponent_level = level + self.levelUp

        monster_level = random.randint(lower_opponent_level, upper_opponent_level)

        self.name = str(name)

        self.level = monster_level

        number_attributes = 3
        attributes_modifier = 1

        random_attribute_values = self.attributeCalc.generate_attribute_values(
            self.level, number_attributes, attributes_modifier
        )

        random.shuffle(random_attribute_values)

        (self.skill, self.strength, self.stamina) = random_attribute_values

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

    def empower(self, skill_modifier, round_id):
        Ningyo.empower(self, skill_modifier, 1)

    def weaken(self, damage, skill_modifier, round_id):
        Ningyo.weaken(self, damage, skill_modifier, 1)
