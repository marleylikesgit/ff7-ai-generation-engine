"""
Seeds the database with FF7 data: characters, a materia list,
equipment tiers based on stage of game and additional notes.

Every Materia/Equipment row is tagged with story_stage ("early" / "mid" / "late"),
marking the EARLIEST point in the story it's realistically obtainable. The
/recommend endpoint filters against this so players aren't recommended gear
they can't have reached yet. Stage boundaries used here (approximate, for
gameplay-planning purposes rather than a frame-perfect walkthrough):
  - early: Midgar, through escaping the city and reaching the outside - Kalm
  - mid:   Outside world exploration through before the Temple of the Ancients
  - late:  Temple of the Ancients onward, including postgame/superbosses
  
"""
from database import engine, SessionLocal, Base
from models import Character, Materia, Equipment, SynergyNote
from embeddings import embed_text

Base.metadata.create_all(bind=engine)

characters = [
    Character(name="Cloud", role_archetype="physical dps", strengths="High strength and solid magic, best all-rounder, huge single-target Limit damage",
              innate_stat_bias="high strength, above-average magic", default_limit_break="Braver",
              weapon_slot_profile="swords, up to 8 slots on late-game weapons, several linked pairs"),
    Character(name="Barret", role_archetype="physical dps / ranged", strengths="Gun-arm means no weapon reach restrictions, great HP growth, good Counter Attack chassis",
              innate_stat_bias="high vitality/HP, moderate strength", default_limit_break="Big Shot",
              weapon_slot_profile="up to 8 slots, generous linked pairs"),
    Character(name="Tifa", role_archetype="physical dps", strengths="Fast, benefits from multi-hit support materia, strong Limit damage multipliers",
              innate_stat_bias="high dexterity/strength", default_limit_break="Beat Rush",
              weapon_slot_profile="up to 8 slots"),
    Character(name="Aerith", role_archetype="mixed caster / support", strengths="Best magic and spirit stats in the game, only user of the strongest healing Limit",
              innate_stat_bias="very high magic and spirit, low HP/strength", default_limit_break="Healing Wind / Great Gospel",
              weapon_slot_profile="staves, up to 8 slots"),
    Character(name="Red XIII", role_archetype="mixed physical/magic", strengths="Balanced stats, good natural magic defense, solid all-around materia host",
              innate_stat_bias="balanced, slight magic lean", default_limit_break="Sled Fang",
              weapon_slot_profile="up to 8 slots"),
    Character(name="Yuffie", role_archetype="physical dps", strengths="Highest dexterity, strong late-game strength, elemental weapon-swap potential",
              innate_stat_bias="very high dexterity", default_limit_break="Greased Lightning",
              weapon_slot_profile="up to 8 slots"),
    Character(name="Cid", role_archetype="physical dps", strengths="High strength, spear reach, good all-around late joiner",
              innate_stat_bias="high strength, decent vitality", default_limit_break="Boost Jump",
              weapon_slot_profile="up to 8 slots"),
    Character(name="Cait Sith", role_archetype="support / gambler", strengths="Slots limit break for random powerful effects, decent support materia host",
              innate_stat_bias="low-moderate across the board", default_limit_break="Dice / Slots",
              weapon_slot_profile="up to 8 slots"),
    Character(name="Vincent", role_archetype="mixed / transform dps", strengths="Limit Break transforms into powerful monster forms with unique abilities",
              innate_stat_bias="high magic, moderate strength", default_limit_break="Galian Beast",
              weapon_slot_profile="up to 8 slots"),
]

materia = [
    # --- Magic: early ---
    Materia(name="Restore", type="magic", description="Cure line spells for HP recovery",
            pairs_well_with="HP Absorb, All, Added Effect", ap_to_master=48000, stat_effects="+MP", story_stage="early"),
    Materia(name="Heal", type="magic", description="Status ailment cures",
            pairs_well_with="All", ap_to_master=27000, stat_effects="+MP", story_stage="early"),
    Materia(name="Fire", type="magic", description="Fire elemental offensive spells",
            pairs_well_with="Elemental, All, Quadra Magic", ap_to_master=20000, stat_effects="+MP, -HP", story_stage="early"),
    Materia(name="Poison", type="magic", description="Poison elemental damage plus poison status",
            pairs_well_with="Elemental, All", ap_to_master=14000, stat_effects="+MP", story_stage="early"),
    Materia(name="Revive", type="magic", description="Revives KO'd party members",
            pairs_well_with="Added Effect, All", ap_to_master=54000, stat_effects="+MP", story_stage="early"),
    # --- Magic: mid ---
    Materia(name="Ice", type="magic", description="Ice elemental offensive spells",
            pairs_well_with="Elemental, All, Quadra Magic", ap_to_master=20000, stat_effects="+MP, -HP", story_stage="mid"),
    Materia(name="Bolt", type="magic", description="Lightning elemental offensive spells",
            pairs_well_with="Elemental, All, Quadra Magic", ap_to_master=20000, stat_effects="+MP, -HP", story_stage="mid"),
    Materia(name="Earth", type="magic", description="Earth elemental offensive spells",
            pairs_well_with="Elemental, All", ap_to_master=22000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Gravity", type="magic", description="Percentage-based HP damage, ignores defense",
            pairs_well_with="All", ap_to_master=30000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Time", type="magic", description="Haste, Slow, Stop utility spells",
            pairs_well_with="All", ap_to_master=22000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Barrier", type="magic", description="Physical and magic defense buffs (Barrier/MBarrier)",
            pairs_well_with="All", ap_to_master=25000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Seal", type="magic", description="Silence and Sleep status inflicts",
            pairs_well_with="Added Effect", ap_to_master=16000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Mystify", type="magic", description="Confuse and Berserk status inflicts",
            pairs_well_with="Added Effect", ap_to_master=18000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Transform", type="magic", description="Mini and Frog status inflicts",
            pairs_well_with="Added Effect", ap_to_master=12000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Destruct", type="magic", description="Death and instant-death-adjacent effects",
            pairs_well_with="Added Effect", ap_to_master=30000, stat_effects="+MP", story_stage="mid"),
    # --- Magic: late ---
    Materia(name="Contain", type="magic", description="Powerful elemental spells: Freeze, Break, Bio, Tornado",
            pairs_well_with="Elemental, All, Quadra Magic", ap_to_master=140000, stat_effects="+MP, -HP", story_stage="late"),
    Materia(name="Comet", type="magic", description="Non-elemental heavy damage, hits random targets on Comet2",
            pairs_well_with="Quadra Magic", ap_to_master=60000, stat_effects="+MP, -HP", story_stage="late"),
    Materia(name="Ultima", type="magic", description="Strongest standard spell, heavy non-elemental damage to all",
            pairs_well_with="All", ap_to_master=180000, stat_effects="+MP, -HP", story_stage="late"),
    Materia(name="Full Cure", type="magic", description="Full HP restore + status cure in one cast",
            pairs_well_with="All", ap_to_master=1400000, stat_effects="+MP", story_stage="late"),

    # --- Support: early ---
    Materia(name="Counter Attack", type="support", description="Automatically counters physical hits when linked to a command materia",
            pairs_well_with="Sense, W-Item, Deathblow", ap_to_master=45000, stat_effects="none", story_stage="early"),
    # --- Support: mid ---
    Materia(name="All", type="support", description="Extends linked materia's effect to hit all targets",
            pairs_well_with="Restore, Fire, Ice, Bolt, Heal", ap_to_master=250000, stat_effects="-HP, -MP when linked", story_stage="mid"),
    Materia(name="Elemental", type="support", description="Attaches an elemental property to weapon or armor when linked",
            pairs_well_with="Fire, Ice, Bolt, Poison, Restore(absorb setups)", ap_to_master=100000, stat_effects="none", story_stage="mid"),
    Materia(name="Added Effect", type="support", description="Attaches a status effect to weapon or armor when linked",
            pairs_well_with="Restore(auto-regen tanks), poison/paralyze materia", ap_to_master=20000, stat_effects="none", story_stage="mid"),
    Materia(name="HP Absorb", type="support", description="Converts linked attack damage into HP recovery",
            pairs_well_with="Fire, Ice, Bolt, All", ap_to_master=45000, stat_effects="none", story_stage="mid"),
    Materia(name="MP Absorb", type="support", description="Converts linked attack damage into MP recovery",
            pairs_well_with="Fire, Ice, Bolt, All", ap_to_master=45000, stat_effects="none", story_stage="mid"),
    Materia(name="Sneak Attack", type="support", description="Guarantees a critical hit on the first strike of battle when linked",
            pairs_well_with="Steal, Deathblow", ap_to_master=20000, stat_effects="none", story_stage="mid"),
    Materia(name="Final Attack", type="support", description="Triggers the linked materia's effect for free when the wearer is KO'd",
            pairs_well_with="Revive, Life-tier spells", ap_to_master=25000, stat_effects="none", story_stage="mid"),
    Materia(name="Magic Counter", type="support", description="Automatically casts a linked spell in retaliation when hit",
            pairs_well_with="Ultima, Comet, elemental spells", ap_to_master=60000, stat_effects="none", story_stage="mid"),
    # --- Support: late ---
    Materia(name="Quadra Magic", type="support", description="Quadruples a linked single spell cast for one MP cost",
            pairs_well_with="Fire, Ice, Bolt, Comet, Knights of the Round", ap_to_master=100000, stat_effects="none", story_stage="late"),
    Materia(name="Added Cut", type="support", description="Automatically performs a linked command materia's action after a normal attack",
            pairs_well_with="Deathblow, Flash", ap_to_master=60000, stat_effects="none", story_stage="late"),

    # --- Independent: mid ---
    Materia(name="HP <-> MP", type="independent", description="Converts a portion of HP into MP",
            pairs_well_with="none (independent)", ap_to_master=99000, stat_effects="trade HP for MP", story_stage="mid"),
    Materia(name="Long Range", type="independent", description="Removes back-row damage penalty",
            pairs_well_with="none (independent)", ap_to_master=20000, stat_effects="none", story_stage="mid"),
    Materia(name="Counter", type="independent", description="Chance to automatically counter any attack, no link needed",
            pairs_well_with="none (independent)", ap_to_master=40000, stat_effects="none", story_stage="mid"),
    Materia(name="Enemy Away", type="independent", description="Reduces random encounter rate",
            pairs_well_with="none (independent)", ap_to_master=8000, stat_effects="none", story_stage="mid"),
    Materia(name="Enemy Lure", type="independent", description="Increases random encounter rate",
            pairs_well_with="none (independent)", ap_to_master=8000, stat_effects="none", story_stage="mid"),
    # --- Independent: late ---
    Materia(name="Underwater", type="independent", description="Allows fighting underwater (required for a late submarine boss)",
            pairs_well_with="none (independent)", ap_to_master=1000, stat_effects="none", story_stage="late"),

    # --- Command: early ---
    Materia(name="Steal", type="command", description="Steals an item from an enemy",
            pairs_well_with="Added Effect, Sneak Attack", ap_to_master=100000, stat_effects="none", story_stage="early"),
    Materia(name="Sense", type="command", description="Reveals enemy stats and weaknesses",
            pairs_well_with="Counter Attack", ap_to_master=100000, stat_effects="none", story_stage="early"),
    Materia(name="Deathblow", type="command", description="Guaranteed critical hit at the cost of accuracy",
            pairs_well_with="Counter Attack, Added Cut, Sneak Attack", ap_to_master=45000, stat_effects="none", story_stage="early"),
    Materia(name="Throw", type="command", description="Throws items at enemies for damage",
            pairs_well_with="none (command)", ap_to_master=45000, stat_effects="none", story_stage="early"),
    Materia(name="Manipulate", type="command", description="Takes control of an enemy for a turn",
            pairs_well_with="none (command)", ap_to_master=45000, stat_effects="none", story_stage="early"),
    # --- Command: mid ---
    Materia(name="W-Item", type="command", description="Use two items in a single turn",
            pairs_well_with="none (command)", ap_to_master=100000, stat_effects="none", story_stage="mid"),
    Materia(name="W-Magic", type="command", description="Cast two spells in a single turn",
            pairs_well_with="none (command)", ap_to_master=250000, stat_effects="none", story_stage="mid"),
    # --- Command: late ---
    Materia(name="Mime", type="command", description="Repeats the last action used, including Limit Breaks, for free",
            pairs_well_with="none (command)", ap_to_master=250000, stat_effects="none", story_stage="late"),
    Materia(name="W-Summon", type="command", description="Summon twice in a single turn",
            pairs_well_with="none (command)", ap_to_master=300000, stat_effects="none", story_stage="late"),

    # --- Summon: early/mid ---
    Materia(name="Choco/Mog", type="summon", description="Summons chocobos for a moderate non-elemental hit",
            pairs_well_with="none (summon)", ap_to_master=30000, stat_effects="+MP", story_stage="early"),
    Materia(name="Shiva", type="summon", description="Ice-elemental summon, moderate group damage",
            pairs_well_with="Quadra Magic", ap_to_master=30000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Ifrit", type="summon", description="Fire-elemental summon, moderate group damage",
            pairs_well_with="Quadra Magic", ap_to_master=30000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Ramuh", type="summon", description="Lightning-elemental summon, moderate group damage",
            pairs_well_with="Quadra Magic", ap_to_master=30000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Titan", type="summon", description="Earth-elemental summon, heavy group damage",
            pairs_well_with="Quadra Magic", ap_to_master=40000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Odin", type="summon", description="Instant-death-style non-elemental summon (Zantetsuken)",
            pairs_well_with="none (summon)", ap_to_master=60000, stat_effects="+MP", story_stage="mid"),
    Materia(name="Phoenix", type="summon", description="Fire-elemental summon that also revives and heals the party",
            pairs_well_with="none (summon)", ap_to_master=60000, stat_effects="+MP", story_stage="mid"),
    # --- Summon: late ---
    Materia(name="Bahamut", type="summon", description="Strong non-elemental single-hit summon",
            pairs_well_with="Quadra Magic", ap_to_master=70000, stat_effects="+MP", story_stage="late"),
    Materia(name="Neo Bahamut", type="summon", description="Stronger non-elemental multi-hit summon",
            pairs_well_with="Quadra Magic", ap_to_master=90000, stat_effects="+MP", story_stage="late"),
    Materia(name="Bahamut ZERO", type="summon", description="High non-elemental multi-hit summon, one of the strongest standard summons",
            pairs_well_with="Quadra Magic", ap_to_master=120000, stat_effects="+MP", story_stage="late"),
    Materia(name="Alexander", type="summon", description="Massive non-elemental holy damage summon",
            pairs_well_with="Quadra Magic", ap_to_master=80000, stat_effects="+MP", story_stage="late"),
    Materia(name="Kjata", type="summon", description="Multi-elemental (fire/ice/lightning) group summon",
            pairs_well_with="Quadra Magic", ap_to_master=80000, stat_effects="+MP", story_stage="late"),
    Materia(name="Knights of the Round", type="summon", description="Strongest summon, hits 13 times, huge non-elemental damage",
            pairs_well_with="Quadra Magic (endgame)", ap_to_master=1000000, stat_effects="+MP, -HP", story_stage="late"),
]

equipment = [
    # ===== Cloud weapons =====
    Equipment(name="Buster Sword", slot_type="weapon", character_name="Cloud", total_slots=2, linked_slots=2,
              growth_rate="normal", notes="Cloud's starting weapon, balanced growth", story_stage="early"),
    Equipment(name="Mythril Saber", slot_type="weapon", character_name="Cloud", total_slots=4, linked_slots=2,
              growth_rate="normal", notes="Early upgrade with more slots than the Buster Sword", story_stage="early"),
    Equipment(name="Nail Bat", slot_type="weapon", character_name="Cloud", total_slots=0, linked_slots=0,
              growth_rate="fixed", notes="Joke weapon with a random, sometimes huge, damage variance", story_stage="mid"),
    Equipment(name="Organics", slot_type="weapon", character_name="Cloud", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game sword with a good slot layout", story_stage="mid"),
    Equipment(name="Force Stealer", slot_type="weapon", character_name="Cloud", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Strong all-around late-game sword", story_stage="late"),
    Equipment(name="Ultima Weapon", slot_type="weapon", character_name="Cloud", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best endgame sword, huge slot count, damage scales with remaining MP", story_stage="late"),

    # ===== Barret weapons =====
    Equipment(name="Gatling Gun", slot_type="weapon", character_name="Barret", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Barret's starting gun-arm", story_stage="early"),
    Equipment(name="Assault Gun", slot_type="weapon", character_name="Barret", total_slots=4, linked_slots=2,
              growth_rate="normal", notes="Early-mid upgrade with more slots", story_stage="early"),
    Equipment(name="Missing Score", slot_type="weapon", character_name="Barret", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game gun-arm, high slot count", story_stage="mid"),
    Equipment(name="Microlaser", slot_type="weapon", character_name="Barret", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Mid-late gun-arm with strong base attack", story_stage="mid"),
    Equipment(name="Premium Heart", slot_type="weapon", character_name="Barret", total_slots=6, linked_slots=6,
              growth_rate="fixed high base", notes="Bonus damage scales with Barret's HP-to-max ratio, best used topped off", story_stage="late"),
    Equipment(name="Missing Score (Perfect)", slot_type="weapon", character_name="Barret", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Late-game variant with maximum slot count", story_stage="late"),

    # ===== Tifa weapons =====
    Equipment(name="Leather Glove", slot_type="weapon", character_name="Tifa", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Tifa's starting weapon", story_stage="early"),
    Equipment(name="Metal Knuckle", slot_type="weapon", character_name="Tifa", total_slots=4, linked_slots=2,
              growth_rate="normal", notes="Early slot upgrade", story_stage="early"),
    Equipment(name="Grand Glove", slot_type="weapon", character_name="Tifa", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game fist weapon", story_stage="mid"),
    Equipment(name="Motor Drive", slot_type="weapon", character_name="Tifa", total_slots=6, linked_slots=6,
              growth_rate="growth", notes="Strong mid-late fist weapon, well linked", story_stage="mid"),
    Equipment(name="Kaiser Knuckle", slot_type="weapon", character_name="Tifa", total_slots=8, linked_slots=6,
              growth_rate="growth", notes="Late weapon, very high attack", story_stage="late"),
    Equipment(name="Premium Heart (Tifa)", slot_type="weapon", character_name="Tifa", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best-in-slot late fist weapon, max slots", story_stage="late"),

    # ===== Aerith weapons =====
    Equipment(name="Guard Stick", slot_type="weapon", character_name="Aerith", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Aerith's starting staff", story_stage="early"),
    Equipment(name="Mythril Rod", slot_type="weapon", character_name="Aerith", total_slots=4, linked_slots=2,
              growth_rate="growth", notes="Boosts magic, good mid-game staff", story_stage="mid"),
    Equipment(name="Striking Staff", slot_type="weapon", character_name="Aerith", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Well-rounded mid-late staff", story_stage="mid"),
    Equipment(name="Princess Guard", slot_type="weapon", character_name="Aerith", total_slots=6, linked_slots=6,
              growth_rate="fixed high base", notes="Best-in-slot Aerith weapon, very high attack for her kit", story_stage="late"),

    # ===== Red XIII weapons =====
    Equipment(name="Mane Blaster", slot_type="weapon", character_name="Red XIII", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Red XIII's starting headdress weapon", story_stage="early"),
    Equipment(name="Spring Gun Clip", slot_type="weapon", character_name="Red XIII", total_slots=4, linked_slots=2,
              growth_rate="normal", notes="Early-mid slot upgrade", story_stage="early"),
    Equipment(name="Add-on Rocket", slot_type="weapon", character_name="Red XIII", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game option", story_stage="mid"),
    Equipment(name="Limited Moon", slot_type="weapon", character_name="Red XIII", total_slots=6, linked_slots=6,
              growth_rate="growth", notes="Strong mid-late headdress weapon", story_stage="mid"),
    Equipment(name="Spirit Lance", slot_type="weapon", character_name="Red XIII", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best-in-slot late weapon, max slots", story_stage="late"),

    # ===== Yuffie weapons =====
    Equipment(name="Boomerang", slot_type="weapon", character_name="Yuffie", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Yuffie's starting weapon", story_stage="early"),
    Equipment(name="Ashura", slot_type="weapon", character_name="Yuffie", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game shuriken", story_stage="mid"),
    Equipment(name="Superball", slot_type="weapon", character_name="Yuffie", total_slots=6, linked_slots=6,
              growth_rate="growth", notes="Strong mid-late shuriken", story_stage="mid"),
    Equipment(name="Conformer", slot_type="weapon", character_name="Yuffie", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best-in-slot late weapon, damage boosted by rare-item count in inventory", story_stage="late"),

    # ===== Cid weapons =====
    Equipment(name="Spear", slot_type="weapon", character_name="Cid", total_slots=2, linked_slots=0,
              growth_rate="normal", notes="Cid's starting spear", story_stage="mid"),
    Equipment(name="Vidal Spear", slot_type="weapon", character_name="Cid", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game upgrade", story_stage="mid"),
    Equipment(name="Trident", slot_type="weapon", character_name="Cid", total_slots=6, linked_slots=6,
              growth_rate="growth", notes="Strong mid-late spear", story_stage="mid"),
    Equipment(name="Venus Gospel", slot_type="weapon", character_name="Cid", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best-in-slot late spear, max slots", story_stage="late"),

    # ===== Cait Sith weapons =====
    Equipment(name="Yellow M-phone", slot_type="weapon", character_name="Cait Sith", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Cait Sith's starting megaphone", story_stage="mid"),
    Equipment(name="Umbrella", slot_type="weapon", character_name="Cait Sith", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Well-rounded, decent slot layout", story_stage="mid"),
    Equipment(name="HP Shout", slot_type="weapon", character_name="Cait Sith", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best-in-slot late megaphone, max slots", story_stage="late"),

    # ===== Vincent weapons =====
    Equipment(name="Quicksilver", slot_type="weapon", character_name="Vincent", total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Vincent's starting handgun", story_stage="mid"),
    Equipment(name="Long Barrel R", slot_type="weapon", character_name="Vincent", total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Solid mid-game handgun", story_stage="mid"),
    Equipment(name="Death Penalty", slot_type="weapon", character_name="Vincent", total_slots=8, linked_slots=8,
              growth_rate="growth", notes="Best-in-slot late handgun, damage scales with battles fought", story_stage="late"),

    # ===== Armor =====
    Equipment(name="Bronze Bangle", slot_type="armor", character_name=None, total_slots=1, linked_slots=0,
              growth_rate="normal", notes="Very early basic armor", story_stage="early"),
    Equipment(name="Silver Armlet", slot_type="armor", character_name=None, total_slots=2, linked_slots=0,
              growth_rate="normal", notes="Early upgrade, more slots", story_stage="early"),
    Equipment(name="Mythril Armlet", slot_type="armor", character_name=None, total_slots=4, linked_slots=2,
              growth_rate="normal", notes="Solid early-mid armor", story_stage="mid"),
    Equipment(name="Chain Mail", slot_type="armor", character_name=None, total_slots=5, linked_slots=2,
              growth_rate="normal", notes="Balanced mid-game defensive armor", story_stage="mid"),
    Equipment(name="Wizard Bracelet", slot_type="armor", character_name=None, total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Strong magic-defense-focused mid armor", story_stage="mid"),
    Equipment(name="Mystile", slot_type="armor", character_name="Aerith", total_slots=4, linked_slots=2,
              growth_rate="normal", notes="Aerith-exclusive, strong defensive stats, protects against instant death", story_stage="mid"),
    Equipment(name="Aurora Armlet", slot_type="armor", character_name=None, total_slots=6, linked_slots=4,
              growth_rate="growth", notes="Grants immunity to cold/freeze-related statuses, solid mid-late armor", story_stage="mid"),
    Equipment(name="Rune Armlet", slot_type="armor", character_name=None, total_slots=7, linked_slots=6,
              growth_rate="growth", notes="Strong late-mid armor with good slot count", story_stage="late"),
    Equipment(name="Premium Armlet", slot_type="armor", character_name=None, total_slots=8, linked_slots=6,
              growth_rate="growth", notes="Best general-purpose armor, huge slot count, usable by anyone", story_stage="late"),

    # ===== Accessories =====
    Equipment(name="Star Pendant", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Prevents Poison — cheap, widely available early defensive pick", story_stage="early"),
    Equipment(name="Peace Ring", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Prevents Fury and Sadness status", story_stage="early"),
    Equipment(name="Talisman", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Boosts both magic defense and magic power slightly", story_stage="mid"),
    Equipment(name="Sprint Shoes", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Always move first / acts like permanent Haste in some contexts", story_stage="mid"),
    Equipment(name="Fairy Ring", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Prevents Poison, Darkness, and Slow-Numb, a step up from Star Pendant", story_stage="mid"),
    Equipment(name="Touph Ring", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Prevents Poison, Darkness, Silence, Frog, Small — solid general defensive pick", story_stage="mid"),
    Equipment(name="Safety Bit", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Prevents instant death, Petrify, and Gravity-type damage", story_stage="mid"),
    Equipment(name="Fury Ring", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Permanent Berserk, huge physical damage boost, removes menu/magic access — pairs with Counter Attack setups", story_stage="mid"),
    Equipment(name="Reflect Ring", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Permanent Reflect status — bounces spells back, useful vs certain magic-heavy bosses", story_stage="late"),
    Equipment(name="Ribbon", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Immunity to nearly all negative status effects, best-in-slot for any character", story_stage="late"),
    Equipment(name="Genji Glove", slot_type="accessory", character_name=None, total_slots=0, linked_slots=0,
              growth_rate="n/a", notes="Allows dual-wielding two weapon slots' worth of materia effects at once for fist-fighters", story_stage="late"),
]

synergy_notes = [
    SynergyNote(title="Barret tank with Counter Attack + Restore",
                content="Pairing Counter Attack with a command materia like Deathblow on Barret, alongside a linked Restore+HP Absorb setup, turns him into a self-sustaining frontline tank. His naturally high HP growth means enemies get punished for attacking him while he recovers HP passively.",
                tags="Barret,Counter Attack,Restore,HP Absorb"),
    SynergyNote(title="Aerith as dedicated healer with All-linked Restore",
                content="Aerith's very high magic and spirit stats make her the best host for All+Restore, letting one cast heal the whole party for a large amount. Keep her in the back row to offset her low HP and physical defense."),
    SynergyNote(title="Quadra Magic elemental one-shot setup",
                content="Linking Quadra Magic with a single-target elemental spell like Ice quadruples the cast for the MP cost of one spell. This is devastating against bosses weak to that element and works especially well on Cloud or Aerith given their MP pools."),
    SynergyNote(title="Cloud and Tifa dual physical DPS core",
                content="Cloud and Tifa both scale well with strength and benefit from Added Effect linked to a status like Poison on their weapons for consistent physical damage plus chip damage over time. A third magic-focused member covers their weak elemental coverage."),
    SynergyNote(title="Fury Ring berserk glass cannon",
                content="The Fury Ring's permanent Berserk trades menu and magic access for a large physical damage boost. Best on a high-strength character like Cloud or Cid who doesn't need to cast spells, paired with a healer elsewhere on the team to offset the inability to self-heal."),
    SynergyNote(title="Mixed magic-physical team with Red XIII",
                content="Red XIII's balanced stat growth lets him flex between physical attacks and support magic like Time (Haste/Slow), making him a good glue character between a pure physical attacker and a pure caster."),
    SynergyNote(title="Knights of the Round plus Quadra Magic endgame combo",
                content="In the postgame, linking Quadra Magic to Knights of the Round quadruples the strongest summon in the game for a single MP cost, capable of dealing damage well beyond the game's HP caps. Requires very high MP and is typically reserved for optional superbosses."),
    SynergyNote(title="Yuffie elemental weapon swapping",
                content="Yuffie's high dexterity means she attacks fast and often, so equipping Elemental+appropriate element materia on her weapon exploits enemy weaknesses more times per turn than slower characters can."),
    SynergyNote(title="Ribbon as universal status immunity",
                content="Because Ribbon grants near-total status immunity and has no materia slots, it's best given to whichever party member is most vulnerable to being disabled — often a caster like Aerith whose death or silence cripples team healing."),
    SynergyNote(title="Early-game budget defense with Star Pendant and Peace Ring",
                content="Before better accessories are available, Star Pendant and Peace Ring are cheap, widely sold items that cover the most common early status ailments. Prioritize whichever party member is squishiest, often Aerith, until stronger options like Fairy Ring or Touph Ring appear."),
    SynergyNote(title="Mid-game W-Item stalling and healing",
                content="W-Item lets a character use two items per turn for free, which is strong for chaining Elixirs or Hi-Potions well before better Restore setups are affordable. It's especially useful on a support-leaning character like Cait Sith or Red XIII while All+Restore is still being mastered."),
    SynergyNote(title="Late-game Genji Glove dual-hand fist builds",
                content="Genji Glove lets fist-fighters like Tifa effectively use two weapons' worth of materia linkage at once, making her one of the best late-game hosts for stacking multiple elemental Added Effect and Counter setups simultaneously."),
    SynergyNote(title="Mime-based Limit Break loop",
                content="Once Mime is available late-game, using a powerful Limit Break once and then Miming it for free on subsequent turns lets a character repeat their strongest attack without waiting for the Limit gauge to refill, especially strong on high-damage Limits."),
]


def run():
    db = SessionLocal()
    try:
        db.query(SynergyNote).delete()
        db.query(Equipment).delete()
        db.query(Materia).delete()
        db.query(Character).delete()
        db.commit()

        db.add_all(characters)
        db.add_all(materia)
        db.add_all(equipment)
        db.commit()

        for note in synergy_notes:
            note.embedding = embed_text(f"{note.title}. {note.content}")
            db.add(note)
        db.commit()

        print(f"Seeded {len(characters)} characters, {len(materia)} materia, "
              f"{len(equipment)} equipment, {len(synergy_notes)} synergy notes.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
