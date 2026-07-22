from pydantic import BaseModel
from typing import Optional


class CharacterOut(BaseModel):
    id: int
    name: str
    role_archetype: Optional[str] = None
    strengths: Optional[str] = None
    innate_stat_bias: Optional[str] = None
    default_limit_break: Optional[str] = None
    weapon_slot_profile: Optional[str] = None

    class Config:
        from_attributes = True


class MateriaOut(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    pairs_well_with: Optional[str] = None
    ap_to_master: Optional[int] = None
    stat_effects: Optional[str] = None
    story_stage: Optional[str] = None

    class Config:
        from_attributes = True


class EquipmentOut(BaseModel):
    id: int
    name: str
    slot_type: str
    character_name: Optional[str] = None
    total_slots: int
    linked_slots: int
    growth_rate: Optional[str] = None
    notes: Optional[str] = None
    story_stage: Optional[str] = None

    class Config:
        from_attributes = True


class GameStageOut(BaseModel):
    id: str
    label: str
    description: str


class RecommendRequest(BaseModel):
    character_names: list[str]  # exactly 3 party member names, e.g. ["Cloud", "Barret", "Aerith"]
    playstyle_hint: Optional[str] = None  # freeform, e.g. "I want heavy magic damage"
    game_stage: Optional[str] = "late"  # early | mid | late — defaults to no restriction


class CharacterLoadout(BaseModel):
    character: str
    weapon: Optional[str] = None
    armor: Optional[str] = None
    accessory: Optional[str] = None
    materia: list[str] = []
    rationale: str


class RecommendResponse(BaseModel):
    team_summary: str
    loadouts: list[CharacterLoadout]
    retrieved_notes: list[str]  # titles of the synergy notes used as context, for transparency
