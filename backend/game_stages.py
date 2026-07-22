"""
Story-progression stage definitions.

Used to filter equipment/materia recommendations so players don't get
recommended anything they can't have obtained yet at their point in the story.
Stages are ordered — selecting a stage includes everything tagged at that
stage or earlier.
"""

STAGE_ORDER = ["early", "mid", "late"]

STAGE_INFO = {
    "early": {
        "label": "Early Game",
        "description": "Before leaving Midgar (up through the escape and reaching the overworld/Kalm)",
    },
    "mid": {
        "label": "Mid Game",
        "description": "From reaching the overworld through before the Temple of the Ancients / Forgotten City",
    },
    "late": {
        "label": "Late Game",
        "description": "From the Temple of the Ancients onward, including post-game and superboss content",
    },
}


def stage_rank(stage: str) -> int:
    try:
        return STAGE_ORDER.index(stage)
    except ValueError:
        return len(STAGE_ORDER) - 1  # unknown stage treated as most-permissive


def stages_up_to(stage: str) -> list[str]:
    """Returns this stage and every stage before it, e.g. 'mid' -> ['early', 'mid']."""
    rank = stage_rank(stage)
    return STAGE_ORDER[: rank + 1]
