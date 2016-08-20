from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from interfaces.models.base import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type_id = Column(String)
    level = Column(Integer)
    attributes = Column(Integer)


class Weaponry(Base):
    __tablename__ = 'weaponry'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    fighter_id = Column(Integer, ForeignKey('fighter.id'))
    item = relationship("Item")
    fighter = relationship("Fighter")
