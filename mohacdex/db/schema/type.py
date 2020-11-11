from sqlalchemy import Column, ForeignKey, Float, Unicode
from sqlalchemy.orm import relationship
from ..base import Base
 
class Type(Base):
    __tablename__ = "types"
     
    identifier = Column(Unicode, primary_key=True)
    
class TypeMatchup(Base):
    __tablename__ = "type_matchups"
    
    attacking_type_identifier = Column(Unicode, ForeignKey("types.identifier"), primary_key=True)
    defending_type_identifier = Column(Unicode, ForeignKey("types.identifier"), primary_key=True)
    
    matchup = Column(Float, nullable=False)
    
    attacking_type = relationship("Type", foreign_keys=[attacking_type_identifier])
    defending_type = relationship("Type", foreign_keys=[defending_type_identifier])
