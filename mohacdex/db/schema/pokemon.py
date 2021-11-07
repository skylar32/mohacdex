from sqlalchemy import Column, ForeignKey, Integer, Unicode, Numeric, Boolean
from sqlalchemy.orm import relationship, backref, configure_mappers
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection, collection
from sqlalchemy.orm.relationships import foreign
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
    ability = relationship("Ability", lazy="joined")
    pokemon = relationship("Pokemon", backref=backref("_ability_table", cascade="all, delete-orphan"))
    
class PokemonFlavor(Base):
    __tablename__ = "pokemon_flavor"
    
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    entry_number = Column(Integer, primary_key=True)
    flavor_text = Column(Unicode, nullable=False)
    pokemon = relationship("Pokemon", backref=backref("_dex_entries", cascade="all, delete-orphan"))

class EvolutionChain(Base):
    __tablename__ = "evolution_chains"
    base_form_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    stages = relationship("PokemonEvolution", backref="evolution_chain")
    base_form = relationship("Pokemon")

class PokemonEvolution(Base):
    __tablename__ = "pokemon_evolutions"

    base_form_identifier = Column(Integer, ForeignKey("evolution_chains.base_form_identifier"), nullable=False)
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    evolution_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    method = Column(Unicode, nullable=False)
    quantity = Column(Integer)
    item_identifier = Column(Unicode, ForeignKey("items.identifier"))
    move_identifier = Column(Unicode, ForeignKey("moves.identifier"))
    ability_identifier = Column(Unicode, ForeignKey("abilities.identifier"))
    gender = Column(Unicode)
    region = Column(Unicode)
    time = Column(Unicode)
    knows_move_type = Column(Unicode, ForeignKey("types.identifier"))
    location = Column(Unicode)
    needed_pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"))
    party_type_identifier = Column(Unicode, ForeignKey("types.identifier"))
    direction = Column(Unicode)
    weather = Column(Unicode)

    move = relationship("Move")
    ability = relationship("Ability")
    needed_pokemon = relationship("Pokemon", foreign_keys=[needed_pokemon_identifier])
    item = relationship("Item")

    pokemon = relationship("Pokemon", backref=backref("evolution", cascade="all, delete-orphan"), foreign_keys=[pokemon_identifier])
    evolution = relationship("Pokemon", foreign_keys=[evolution_identifier])

class PokemonEggGroup(Base):
    __tablename__ = "pokemon_egg_groups"

    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    egg_group = Column(Unicode, primary_key=True)
    pokemon = relationship("Pokemon", backref=backref("_egg", cascade="all, delete-orphan"))

class PokemonStat(Base):
    __tablename__ = "pokemon_stats"

    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    stat_identifier = Column(Unicode, ForeignKey("stats.identifier"), primary_key=True)
    base_stat = Column(Integer)
    stat = relationship("Stat")
    
class PokemonEffortYield(Base):
    __tablename__ = "pokemon_effort_yields"
    
    pokemon_identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    stat_identifier = Column(Unicode, ForeignKey("stats.identifier"), primary_key=True)
    value = Column(Integer, nullable=False)
    stat = relationship("Stat")

class Pokemon(Base):
    __tablename__ = "pokemon"
    
    def __repr__(self):
        return f"Pokemon<{self.identifier}>"
    
    order = Column(Integer, unique=True, nullable=False)
    number = Column(Integer, ForeignKey("pokemon_names.number"), nullable=False)
    identifier = Column(Unicode, primary_key=True)
    height_m = Column(Numeric(4,1), nullable=False)
    weight_kg = Column(Numeric(4,1))
    gender = Column(Integer, nullable=False)
    capture_rate = Column(Integer, nullable=False)
    growth_rate = Column(Unicode, nullable=False)
    form = relationship("PokemonForm", uselist=False)

    type1 = Column(Unicode, ForeignKey("types.identifier"), nullable=False)
    type2 = Column(Unicode, ForeignKey("types.identifier"))

    _name_table = relationship("PokemonName")
    name = association_proxy("_name_table", "name")
    stats = relationship("PokemonStat", collection_class=attribute_mapped_collection('stat.abbreviation'))
    effort_yield = relationship("PokemonEffortYield", collection_class=attribute_mapped_collection('stat.name'),)

    flavor = association_proxy("_dex_entries", "flavor_text")
    egg_groups = association_proxy("_egg", "egg_group")
    
    @property
    def species(self):
        if self.form and self.form.species:
            return self.form.species
        else:
            return self._name_table.species

    @property
    def types(self):
        return [self.type1, self.type2]

    @property
    def abilities(self):
        ability_dict = {"ability_1": [], "ability_2": [], "hidden_ability": [], "unique_ability": []}
        for ability in self._ability_table:
            ability_dict[ability.slot].append(ability.ability)
        return {k: v for k, v in ability_dict.items() if v}

    # moves

    @property
    def levelup_moves(self):
        moves = {}
        for move in self.pokemon_levelup_moves:
            if move.level not in moves:
                moves[move.level] = []
            moves[move.level].append(move.move)
        return {key: moves[key] for key in sorted(moves.keys())}


    egg_moves = association_proxy("pokemon_egg_moves", "move")
    tutor_moves = association_proxy("pokemon_tutor_moves", "move")
    machine_moves = association_proxy("pokemon_tm_moves", "move")
    max_moves = association_proxy("pokemon_max_moves", "move")

class PokemonForm(Base):
    __tablename__ = "pokemon_forms"

    identifier = Column(Unicode, ForeignKey("pokemon.identifier"), primary_key=True)
    name = Column(Unicode, nullable=False)
    display_separately = Column(Boolean, nullable=False)
    species = Column(Unicode)
    evolution_chain_identifier = Column(Unicode, ForeignKey("evolution_chains.base_form_identifier"))
    evolution_chain = relationship(EvolutionChain)

Pokemon.evolutions = relationship(PokemonEvolution, primaryjoin=Pokemon.identifier==PokemonEvolution.pokemon_identifier)
Pokemon.evolution_chain = relationship(
    EvolutionChain,
    secondary=PokemonEvolution.__table__,
    primaryjoin="or_(Pokemon.identifier==PokemonEvolution.pokemon_identifier, Pokemon.identifier==PokemonEvolution.evolution_identifier)",
    secondaryjoin="PokemonEvolution.base_form_identifier==EvolutionChain.base_form_identifier",
    uselist=False
)