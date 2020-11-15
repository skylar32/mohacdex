from sqlalchemy import Column, ForeignKey, Integer, Unicode, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from ..base import Base

class PokemonName(Base):
    __tablename__ = "pokemon_names"

    number = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    species = Column(Unicode, nullable=False)

class PokemonAbility(Base):
    __tablename__ = "pokemon_abilities"

    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    ability_identifier = Column(Unicode, ForeignKey("abilities.identifier"), primary_key=True)
    slot = Column(Unicode, nullable=False)

class PokemonEggGroup(Base):
    __tablename__ = "egg_groups"

    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    egg_group = Column(Unicode, primary_key=True)

class Pokemon(Base):
    __tablename__ = "pokemon"
    
    identifier = Column(Unicode, primary_key=True)
    number = Column(Integer, ForeignKey("pokemon_names.number"), nullable=False)
    height_m = Column(Numeric(4,1), nullable=False)
    weight_kg = Column(Numeric(4,1))
    form = relationship("PokemonForm", uselist=False)
    abilities = relationship("PokemonAbility")


    type1 = Column(Unicode, ForeignKey("types.identifier"), nullable=False)
    type2 = Column(Unicode, ForeignKey("types.identifier"))

    _name_table = relationship("PokemonName")
    _egg_table = relationship("PokemonEggGroup")

    egg_groups = association_proxy("_egg_table", "egg_group")

    @property
    def name(self):
        return self._name_table.name
    
    @property
    def species(self):
        if self.form and self.form.species:
            return self.form.species
        else:
            return self._name_table.species

    @property
    def types(self):
        return [self.type1, self.type2]

class PokemonForm(Base):
    __tablename__ = "pokemon_forms"

    identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    name = Column(Unicode, nullable=False)
    display_separately = Column(Boolean, nullable=False)
    species = Column(Unicode)