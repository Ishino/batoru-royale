import random

from sqlalchemy.orm import sessionmaker
from interfaces.db import Engine
from ningyo.models.weaponry import Item as StoredItem


class Item:
    def __init__(self):
        self.name = None
        self.level = 1
        self.type_id = None


class Weapon(Item):

    def __init__(self):
        Item.__init__(self)
        self.attributes = {'base_damage': 1, 'variable_damage': 0}

    def get_damage(self):
        damage = self.attributes['base_damage']
        if self.attributes['variable_damage'] > 0:
            damage += random.randint(0, self.attributes['variable_damage'])
        return damage


class Shield(Item):

    def __init__(self):
        Item.__init__(self)
        self.attributes = {'base_shielding': 1, 'variable_shielding': 0}

    def get_shielding(self):
        shielding = self.attributes['base_shielding']
        if self.attributes['variable_shielding'] > 0:
            shielding += random.randint(0, self.attributes['variable_shielding'])
        return shielding


class Weaponry:

    def __init__(self):
        self.db_engine = Engine()
        self.session = sessionmaker(bind=self.db_engine.get_engine())
        self.item_session = self.session()

    def select_item(self, item_id):
        item_details = self.item_session.query(StoredItem).filter(StoredItem.id == item_id).first()
        return item_details

    def search_item(self, name):
        item_details = self.item_session.query(StoredItem).filter(StoredItem.name == name).first()
        return item_details.id

    def generate_item(self, name, type_id, level):

        item = None

        if type_id == 'weapon':
            item = Weapon()
            item.type_id = 'weapon'
            item.attributes['base_damage'] *= level**2
            item.attributes['variable_damage'] = level - 1

        if type_id == 'shield':
            item = Shield()
            item.type_id = 'shield'
            item.attributes['base_shielding'] *= level**2
            item.attributes['variable_shielding'] = level - 1

        if item is not None:
            item.level = level
            item.name = name
            self.item_session.add(item)
            self.item_session.commit()

        return item
