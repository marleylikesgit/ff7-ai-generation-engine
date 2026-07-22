from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from database import Base

EMBEDDING_DIM = 1536  # matches text-embedding-3-small


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    role_archetype = Column(String)          # e.g. "physical dps", "mixed caster", "tank"
    strengths = Column(Text)                 # short free-text description
    innate_stat_bias = Column(String)        # e.g. "high strength, low magic"
    default_limit_break = Column(String)
    weapon_slot_profile = Column(String)     # e.g. "up to 4 slots, 2 pairs of links"


class Materia(Base):
    __tablename__ = "materia"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)    # magic | support | command | independent | summon
    description = Column(Text)
    pairs_well_with = Column(String)         # comma separated materia names, for linked-slot logic
    ap_to_master = Column(Integer)
    stat_effects = Column(String)            # e.g. "+MP, -HP" freeform
    story_stage = Column(String, default="early")  # early | mid | late — earliest point it's obtainable


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    slot_type = Column(String, nullable=False)  # weapon | armor | accessory
    character_name = Column(String)              # null/blank if usable by anyone
    total_slots = Column(Integer, default=0)
    linked_slots = Column(Integer, default=0)
    growth_rate = Column(String)                 # normal | growth | double growth
    notes = Column(Text)
    story_stage = Column(String, default="early")  # early | mid | late — earliest point it's obtainable


class SynergyNote(Base):
    """
    Curated strategy write-ups used for retrieval-augmented generation.
    Each row is a short paragraph about a team synergy pattern, embedded
    with the OpenAI embeddings API and searched via pgvector cosine distance.
    """
    __tablename__ = "synergy_notes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String)                      # comma separated character/materia names for pre-filtering
    embedding = Column(Vector(EMBEDDING_DIM))
