import csv
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from ..base import Base
 
class Move(Base):
    __tablename__ = "moves"
     
    identifier = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)
    
    type = Column(Unicode, nullable=False)
    damage_class = Column(Unicode, nullable=False)
    
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)

    target_identifier = Column(Unicode, ForeignKey("targets.identifier"), nullable=False)
    target = relationship("Target")

    flavor_text = Column(Unicode, nullable=False)
    
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
