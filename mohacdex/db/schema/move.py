from sqlalchemy import Column, ForeignKey, Integer, Unicode, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from ..base import Base
 
class Move(Base):
    __tablename__ = "moves"
     
    identifier = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)
    
    type = Column(Unicode, ForeignKey("types.identifier"), nullable=False)
    damage_class = Column(Unicode, nullable=False)
    
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer)
    priority = Column(Integer, nullable=False)

    target_identifier = Column(Unicode, ForeignKey("targets.identifier"), nullable=False)
    target = relationship("Target")

    flavor_text = Column(Unicode, nullable=False)

class LevelUpMove(Base):
    __tablename__ = "pokemon_moves_levelup"
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    level = Column(Integer, primary_key=True)
    move = relationship("Move")
    pokemon = relationship("Pokemon", backref=backref(
        "pokemon_levelup_moves",
        cascade="all, delete-orphan"
    ))

class MachineMove(Base):
    __tablename__ = "pokemon_moves_machine"
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    move = relationship("Move")
    pokemon = relationship("Pokemon", backref=backref(
        "pokemon_tm_moves",
        cascade="all, delete-orphan"
    ))

class EggMove(Base):
    __tablename__ = "pokemon_moves_egg"
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    move = relationship("Move")
    needs_light_ball = Column(Boolean)
    pokemon = relationship("Pokemon", backref=backref(
        "pokemon_egg_moves",
        cascade="all, delete-orphan"
    ))

class TutorMove(Base):
    __tablename__ = "pokemon_moves_tutor"
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    move = relationship("Move")
    pokemon = relationship("Pokemon", backref=backref(
        "pokemon_tutor_moves",
        cascade="all, delete-orphan"
    ))

class MaxMove(Base):
    __tablename__ = "pokemon_moves_max"
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    move = relationship("Move")
    pokemon = relationship("Pokemon", backref=backref(
        "pokemon_max_moves",
        cascade="all, delete-orphan"
    ))
    
class Flag(Base):
    __tablename__ = "flags"
    
    identifier = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)
    description = Column(Unicode)
    
class MoveFlag(Base):
    __tablename__ = "move_flags"
    
    move = Column(Unicode, ForeignKey("moves.identifier"), primary_key=True)
    
    flag_name = Column(Unicode, ForeignKey("flags.identifier"), primary_key=True)
    flag = relationship("Flag")
    
class Target(Base):
    __tablename__ = "targets"
    
    identifier = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)
