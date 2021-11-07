from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from ..base import Base 

class Item(Base):
    __tablename__ = "items"
     
    identifier = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)
    value = Column(Integer, nullable=False)
    pocket = Column(Unicode, nullable=False)
    flavor_text = Column(Unicode)
    type_associations = association_proxy("_types", "type_identifier")
    move_associations = association_proxy("_moves", "move")
    pokemon_associations = association_proxy("_pokemon", "pokemon")

class ItemTypeAssocation(Base):
    __tablename__ = "item_type_associations"
    item_identifier = Column(Unicode, ForeignKey("items.identifier"), primary_key=True)
    type_identifier = Column(Unicode, ForeignKey("types.identifier"), primary_key=True)
    item = relationship("Item", backref=backref(
        "_types",
        cascade="all, delete-orphan"
    ))

class ItemMoveAssociation(Base):
    __tablename__ = "item_move_associations"
    item_identifier = Column(Unicode, ForeignKey("items.identifier"), primary_key=True)
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    move = relationship("Move")
    item = relationship("Item", backref=backref(
        "_moves",
        cascade="all, delete-orphan"
    ))

class ItemPokemonAssociation(Base):
    __tablename__ = "item_pokemon_associations"
    item_identifier = Column(Unicode, ForeignKey("items.identifier"), primary_key=True)
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    pokemon = relationship("Pokemon")
    item = relationship("Item", backref=backref(
        "_pokemon",
        cascade="all, delete-orphan"
    ))