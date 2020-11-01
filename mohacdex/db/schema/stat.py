from sqlalchemy import Column, Integer, Unicode
from ..base import Base 

class Stat(Base):
    __tablename__ = "stats"
     
    identifier = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)
    abbreviation = Column(Unicode, nullable=False)
