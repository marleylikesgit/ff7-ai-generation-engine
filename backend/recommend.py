
import json
from sqlalchemy.orm import Session
from sqlalchemy import select
from openai import OpenAI

from database import settings
from models import Character, Materia, Equipment, SynergyNote
from embeddings import embed_text
from schemas import RecommendRequest, RecommendResponse
from game_stages import stages_up_to, STAGE_INFO

client = OpenAI(api_key=settings.OPENAI_API_KEY)

TOP_K_NOTES = 6


def retrieve_synergy_notes(db: Session, query_text: str, k: int = TOP_K_NOTES) -> list[SynergyNote]:
    query_embedding = embed_text(query_text)
    stmt = (
        select(SynergyNote)
        .order_by(SynergyNote.embedding.cosine_distance(query_embedding))
        .limit(k)
    )
    return db.execute(stmt).scalars().all()


def build_facts_blob(db: Session, character_names: list[str], game_stage: str = "late") -> str:
    allowed_stages = stages_up_to(game_stage)

    chars = db.query(Character).filter(Character.name.in_(character_names)).all()
    equip = db.query(Equipment).filter(
        (Equipment.character_name.in_(character_names)) | (Equipment.character_name.is_(None)),
        Equipment.story_stage.in_(allowed_stages),
    ).all()
    all_materia = db.query(Materia).filter(Materia.story_stage.in_(allowed_stages)).all()

    lines = ["## Characters"]
    for c in chars:
        lines.append(
            f"- {c.name}: role={c.role_archetype}; strengths={c.strengths}; "
            f"stat_bias={c.innate_stat_bias}; limit={c.default_limit_break}; "
            f"slots={c.weapon_slot_profile}"
        )

    lines.append(
        f"\n## Available Equipment (progression: {STAGE_INFO[game_stage]['label']} — "
        f"{STAGE_INFO[game_stage]['description']}. ONLY use items listed below; "
        f"do not recommend anything not obtainable yet at this stage.)"
    )
    for e in equip:
        owner = e.character_name or "anyone"
        lines.append(
            f"- {e.name} ({e.slot_type}, for {owner}): {e.total_slots} slots, "
            f"{e.linked_slots} linked, growth={e.growth_rate}. {e.notes or ''}"
        )

    lines.append("\n## Available Materia (filtered to the same progression stage)")
    for m in all_materia:
        lines.append(
            f"- {m.name} ({m.type}): {m.description}. Pairs well with: {m.pairs_well_with}"
        )

    return "\n".join(lines)


SYSTEM_PROMPT = """You are a Final Fantasy VII (1997) team-building expert. You will be given:
1. A FACTS block listing the real characters, equipment, and materia available — treat this as ground truth and do not invent items, stats, or slot counts not listed there.
2. A NOTES block of curated strategy notes retrieved for this specific party.
3. The player's chosen 3-character party, optional playstyle preference, and their current game progression stage.

CRITICAL: The FACTS block is already filtered to only include equipment and materia obtainable at or before the player's stated progression stage. Never recommend an item that is not explicitly listed in the FACTS block, even if you know it exists later in the game — the player cannot access it yet and recommending it would break their playthrough.

Recommend a weapon, armor, accessory, and 2-4 materia (respecting realistic linked-slot pairings) for EACH of the 3 characters, optimized for team synergy within what's currently available. Give a short rationale per character grounded in the facts and notes provided.

Respond ONLY with valid JSON matching this exact shape, no markdown fences, no commentary:
{
  "team_summary": "2-3 sentence overview of the team's strategy",
  "loadouts": [
    {
      "character": "name",
      "weapon": "name or null",
      "armor": "name or null",
      "accessory": "name or null",
      "materia": ["name", "name"],
      "rationale": "2-3 sentences"
    }
  ]
}
"""


def generate_recommendation(db: Session, request: RecommendRequest) -> RecommendResponse:
    if len(request.character_names) != 3:
        raise ValueError("Exactly 3 character names are required.")

    game_stage = request.game_stage or "late"
    if game_stage not in STAGE_INFO:
        game_stage = "late"

    query_text = (
        f"Team synergy for party: {', '.join(request.character_names)}. "
        f"Playstyle preference: {request.playstyle_hint or 'none specified'}. "
        f"Game progression: {STAGE_INFO[game_stage]['label']}"
    )

    notes = retrieve_synergy_notes(db, query_text)
    facts_blob = build_facts_blob(db, request.character_names, game_stage)
    notes_blob = "\n\n".join(f"### {n.title}\n{n.content}" for n in notes)

    user_prompt = (
        f"FACTS:\n{facts_blob}\n\n"
        f"NOTES:\n{notes_blob}\n\n"
        f"PARTY: {', '.join(request.character_names)}\n"
        f"PLAYSTYLE PREFERENCE: {request.playstyle_hint or 'none specified'}\n"
        f"GAME PROGRESSION STAGE: {STAGE_INFO[game_stage]['label']} — "
        f"{STAGE_INFO[game_stage]['description']}. "
        f"Only recommend items from the FACTS list above; nothing from a later stage."
    )

    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
    )

    parsed = json.loads(response.choices[0].message.content)
    parsed["retrieved_notes"] = [n.title for n in notes]
    return RecommendResponse(**parsed)
