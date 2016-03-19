import random

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from interfaces.db import Engine
from ningyo.models.ningyo import Fighter as StoredFighter
from simulator.models.player import PlayerList
from ningyo.fighter import Fighter
from ningyo.modifiers import Accuracy, Power
from ningyo.attributes import Attributes
from ningyo.experience import Experience


class Player:

    def __init__(self):
        self.db_engine = Engine()
        self.session = sessionmaker(bind=self.db_engine.get_engine())
        self.player_session = self.session()

    def select_player(self, name):
        player_details = self.player_session.query(StoredFighter).filter(StoredFighter.name == name).first()
        return player_details

    def load_player(self, name):

        player = Fighter(Attributes())
        player.set_experience_calculator(Experience())
        player.set_accuracy_calculator(Accuracy())
        player.set_power_calculator(Power())

        # load player
        player_details = self.select_player(name)

        if player_details is not None:
            player.create(player_details.name, int(player_details.level), 0, 0, 0)

            player.type = player_details.type
            player.skill = player_details.skill
            player.strength = player_details.strength
            player.stamina = player_details.stamina
            player.hitPoints = player_details.hitpoints
            player.experience = player_details.experience

        # create player
        else:
            player.create(name, 1, 0, 0, 0)

        return player

    def save_player(self, player):

        player_details = self.select_player(player.name)

        if player_details is not None:
            player_details.type = player.type
            player_details.level = player.level
            player_details.skill = player.skill
            player_details.strength = player.strength
            player_details.stamina = player.stamina
            player_details.hitpoints = player.hitPoints
            player_details.experience = player.experience
        else:
            player_details = StoredFighter(
                name=player.name,
                type=player.type,
                level=player.level,
                skill=player.skill,
                strength=player.strength,
                stamina=player.stamina,
                hitpoints=player.hitPoints,
                experience=player.experience
            )
        self.player_session.add(player_details)
        self.player_session.commit()

    @staticmethod
    def generate_player_name():

        pre = ['Sir', 'Dame', 'Super', 'Doctor', 'Dark']

        middle = [
            ['A', 'E', 'I', 'O', 'U', 'Y', 'Qa', 'Be', 'Xi', 'Mo', 'Zu'],
            ['na', 'de', 'vi', 'co', 'su', 'ty'],
            ['las', 'tef', 'vic', 'rot', 'pun', 'wyn'],
            ['ca', 're', 'bi', 'no', 'lu', 'y']
        ]

        names_random = []
        parts = random.randint(2, 4)
        for i in range(int(parts)):
            parts = middle[i]
            names_random.append(random.choice(parts))

        return random.choice(pre) + ' ' + ''.join(names_random)

    def generate_player_list(self, x):
        players = []
        for i in range(x):
            players.append(self.generate_player_name())

        return players

    def use_player_list(self, list_id, x):

        player_list = []
        for player in self.player_session.query(PlayerList).filter(PlayerList.list_id == list_id).all():
            player_list.append(player.name)
        if len(player_list) == 0:
            player_list = self.generate_player_list(x)
            for player in player_list:
                player_details = PlayerList(
                    list_id=list_id,
                    name=player
                )
                self.player_session.add(player_details)
                self.player_session.commit()
        return player_list
