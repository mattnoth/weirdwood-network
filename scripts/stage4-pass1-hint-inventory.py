#!/usr/bin/env python3
"""stage4-pass1-hint-inventory.py

Walk all Pass 1 extraction files, parse every '## Relationships Observed'
markdown table, and produce a full inventory of the free-text hint phrases
that appear in the Relationship column.

Outputs
-------
- Printed report (stdout): file counts, total rows, distinct hints, top 25
  by frequency, per-book breakdown, malformed files, and two-tier coverage
  numbers (exact+prefix baseline vs. exact+prefix+keyword combined).
- working/stage4-hint-inventory.md: full sorted inventory + draft
  deterministic HINT_TO_EDGE map + unmapped tail + coverage estimate.
- working/stage4-hint-residue.md: phrases the combined deterministic layers
  still cannot type — the genuine LLM tail, sorted by frequency.

No LLM calls. No network. Deterministic.

Usage
-----
    python3 scripts/stage4-pass1-hint-inventory.py [--extractions-dir PATH]
                                                    [--output PATH]
                                                    [--residue PATH]
"""

import argparse
import collections
import pathlib
import re
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# Draft deterministic HINT_TO_EDGE map.
# Keys: lowercased, stripped hint phrase (or a substring/prefix that matches).
# Values: canonical edge type from locked-vocab-159.md / architecture.md.
#
# Strategy: only map hints where the intent is unambiguous. Prefer exact
# substring matches over fuzzy. Leave ambiguous multi-interpretation hints
# unmapped (they go to the LLM tail).
#
# Phrases are matched by checking whether the normalized hint:
#   (a) exactly equals a key, OR
#   (b) starts with a key prefix (see HINT_PREFIX_MAP below)
#
HINT_EXACT_MAP: dict[str, str] = {
    # --- Emotional: LOVES ---
    "deep love and longing for": "LOVES",
    "deep closeness": "LOVES",
    "deep love/trust": "LOVES",
    "deep love / trust": "LOVES",
    "daughter of, deep love/trust": "LOVES",
    "loves": "LOVES",
    "love for": "LOVES",
    "deep affection for": "LOVES",
    "familial love": "LOVES",
    "deeply loves": "LOVES",

    # --- Emotional: MOURNS ---
    "mourning": "MOURNS",
    "mourns": "MOURNS",
    "mourns/grieves": "MOURNS",
    "mourns / grieves": "MOURNS",
    "grieves for": "MOURNS",

    # --- Emotional: FEARS ---
    "fears": "FEARS",
    "fear of": "FEARS",
    "afraid of": "FEARS",
    "terrified of": "FEARS",
    "fears (after fight)": "FEARS",

    # --- Emotional: HATES ---
    "hates": "HATES",
    "hatred toward": "HATES",
    "hatred of": "HATES",
    "deep hatred of": "HATES",
    "loathes": "HATES",
    "contempt for": "HATES",
    "contempt toward": "HATES",
    "contemptuous of": "HATES",
    "holds in contempt": "HATES",
    "mocks": "OPPOSES",
    "blames": "OPPOSES",

    # --- Emotional: RESENTS ---
    "resents": "RESENTS",
    "resentment toward": "RESENTS",
    "resents/mocks (privately)": "RESENTS",
    "resents / mocks (privately)": "RESENTS",
    "bitterness toward": "RESENTS",

    # --- Emotional: DISTRUSTS ---
    "distrusts": "DISTRUSTS",
    "distrust of": "DISTRUSTS",
    "suspicious of": "DISTRUSTS",
    "does not trust": "DISTRUSTS",
    "dismissive of": "DISTRUSTS",
    "wary of": "DISTRUSTS",
    "skeptical of": "DISTRUSTS",
    "skeptical of / disapproves of": "DISTRUSTS",

    # --- Emotional: TRUSTS ---
    "trusts": "TRUSTS",
    "trust in": "TRUSTS",

    # --- Emotional: RESPECTS ---
    "respects": "RESPECTS",
    "respects authority of": "RESPECTS",
    "respects knowledge of": "RESPECTS",
    "respects/fears (implied)": "RESPECTS",

    # --- Emotional: OPPOSES ---
    "antagonized by": "OPPOSES",
    "antagonized by (after fight)": "OPPOSES",
    "antagonizes": "OPPOSES",
    "opposes": "OPPOSES",
    "hostile toward": "OPPOSES",
    "hostile toward / attempting to capture": "OPPOSES",
    "hostile toward, attempting to capture": "OPPOSES",
    "hostility toward": "OPPOSES",
    "hostile to": "OPPOSES",
    "defiant toward": "OPPOSES",
    "enemies": "OPPOSES",
    "antagonistic toward": "OPPOSES",
    "threatens": "OPPOSES",
    "defies": "OPPOSES",

    # --- Emotional: COMPANION_OF ---
    "companion of": "COMPANION_OF",
    "friend of": "COMPANION_OF",
    "close friend of": "COMPANION_OF",
    "friends with": "COMPANION_OF",
    "friendship with": "COMPANION_OF",
    "sworn brothers": "COMPANION_OF",
    "sworn-brothers": "COMPANION_OF",
    "sworn brother": "COMPANION_OF",

    # --- Emotional: PROTECTS ---
    "protects": "PROTECTS",
    "protects / defends": "PROTECTS",
    "protective of": "PROTECTS",
    "protector of": "PROTECTS",
    "protected by": "PROTECTS",
    "protective toward": "PROTECTS",
    "protective concern for": "PROTECTS",

    # --- Kinship: PARENT_OF / child relationships ---
    "father of": "PARENT_OF",
    "mother of": "PARENT_OF",
    "parent of": "PARENT_OF",
    "son of": "PARENT_OF",
    "daughter of": "PARENT_OF",

    # --- Kinship: SIBLING_OF ---
    "sibling of": "SIBLING_OF",
    "brother of": "SIBLING_OF",
    "sister of": "SIBLING_OF",
    "half-brother of": "SIBLING_OF",
    "half-sister of": "SIBLING_OF",
    "half brother of": "SIBLING_OF",
    "half sister of": "SIBLING_OF",

    # --- Kinship: SPOUSE_OF ---
    "married to": "SPOUSE_OF",
    "husband of": "SPOUSE_OF",
    "wife of": "SPOUSE_OF",
    "spouse of": "SPOUSE_OF",

    # --- Kinship: BETROTHED_TO ---
    "betrothed to": "BETROTHED_TO",
    "promised to": "BETROTHED_TO",

    # --- Kinship: LOVER_OF ---
    "lover of": "LOVER_OF",
    "lovers": "LOVER_OF",
    "has affair with": "LOVER_OF",
    "mistress of": "LOVER_OF",

    # --- Kinship: WARD_OF ---
    "ward of": "WARD_OF",
    "fostered by": "WARD_OF",
    "foster son of": "WARD_OF",
    "foster-son of": "WARD_OF",
    "ward/foster son of": "WARD_OF",

    # --- Kinship: UNCLE_OF ---
    "uncle of": "UNCLE_OF",
    "aunt of": "UNCLE_OF",
    "niece of": "UNCLE_OF",
    "nephew of": "NEPHEW_OF",

    # --- Kinship: COUSIN_OF ---
    "cousin of": "COUSIN_OF",

    # --- Kinship: HEIR_TO ---
    "heir to": "HEIR_TO",
    "heir of": "HEIR_TO",

    # --- Knowledge: TUTORS / TEACHES ---
    "student of": "TUTORS",
    "student of (recalled)": "TUTORS",
    "student / pupil of": "TUTORS",
    "student/pupil of": "TUTORS",
    "apprentice of": "TUTORS",
    "tutor of": "TUTORS",
    "tutors": "TUTORS",
    "teaches": "TEACHES",
    "taught by": "TUTORS",
    "trains": "TEACHES",
    "teacher/protector of": "TUTORS",
    "teacher of": "TUTORS",
    "trained by": "TUTORS",

    # --- Political: SERVES ---
    "serves": "SERVES",
    "serves (resentfully)": "SERVES",
    "servant of": "SERVES",
    "squire to": "SERVES",
    "handmaiden of": "SERVES",
    "steward of": "SERVES",
    "sworn shield to": "SERVES",
    "loyal to": "SERVES",
    "loyalty to": "SERVES",
    "loyal service to": "SERVES",
    "formerly served": "SERVES",
    "in service to": "SERVES",

    # --- Political: COMMANDS ---
    "commands": "COMMANDS",
    "leads": "COMMANDS",
    "rules over": "RULES",
    "rules": "RULES",
    "authority over": "COMMANDS",
    "controls": "COMMANDS",

    # --- Political: ADVISES ---
    "advises": "ADVISES",
    "counsels": "ADVISES",
    "advisor to": "ADVISES",

    # --- Political: SWORN_TO ---
    "sworn to": "SWORN_TO",
    "sworn sword of": "SWORN_TO",
    "pledged to": "SWORN_TO",
    "fealty to": "SWORN_TO",

    # --- Political: MEMBER_OF ---
    "member of": "MEMBER_OF",
    "recruiter/escort for": "MEMBER_OF",

    # --- Political: ALLIES_WITH ---
    "allies with": "ALLIES_WITH",
    "allied with": "ALLIES_WITH",
    "ally of": "ALLIES_WITH",

    # --- Political: OPPOSES (political) ---
    "political rival of": "OPPOSES",
    "rival of": "OPPOSES",

    # --- Political: BETROTHED (already covered) ---

    # --- Military: KILLS ---
    "killed": "KILLS",
    "kills": "KILLS",
    "murders": "KILLS",
    "slays": "KILLS",
    "slew": "KILLS",

    # --- Military: ATTACKS ---
    "attacks": "ATTACKS",
    "assaults": "ATTACKS",
    "strikes": "ATTACKS",

    # --- Military: CAPTURES ---
    "captures": "CAPTURES",
    "captured": "CAPTURES",
    "takes prisoner": "CAPTURES",

    # --- Military: PRISONER_OF ---
    "prisoner of": "PRISONER_OF",
    "captive of": "PRISONER_OF",

    # --- Military: PROTECTS (again) ---
    "defends": "PROTECTS",
    "defender of": "PROTECTS",

    # --- Military: GUARDS ---
    "guards": "GUARDS",
    "guardian of": "GUARDS",

    # --- Military: RESCUES ---
    "rescued/escorted": "RESCUES",
    "rescues": "RESCUES",
    "saved by": "RESCUES",

    # --- Military: DEFEATS ---
    "defeats": "DEFEATS",
    "defeated by": "DEFEATS",

    # --- Military: EXECUTES ---
    "executes": "EXECUTES",
    "executed by": "EXECUTES",

    # --- Military: BETRAYS ---
    "betrays": "BETRAYS",
    "betrayed by": "BETRAYS",

    # --- Identity: DISGUISED_AS ---
    "disguised as": "DISGUISED_AS",
    "disguised protégée of": "DISGUISED_AS",
    "disguised protegee of": "DISGUISED_AS",
    "in disguise as": "DISGUISED_AS",

    # --- Identity: ALIAS_OF ---
    "alias of": "ALIAS_OF",
    "also known as": "ALIAS_OF",
    "known as": "ALIAS_OF",

    # --- Possession: GIFTED_TO / owns ---
    "gave needle to": "GIFTED_TO",
    "gifted to": "GIFTED_TO",
    "gave to": "GIFTED_TO",
    "gift from": "GIFTED_TO",
    "owns": "OWNS",

    # --- Knowledge: REVEALS_TO ---
    "reveals to": "REVEALS_TO",
    "reveals information to": "REVEALS_TO",
    "informs": "REVEALS_TO",
    # "connected to unnamed messenger regarding" — too indirect/ambiguous, leave for LLM

    # --- Knowledge: DECEIVES ---
    "deceives": "DECEIVES",
    "manipulates": "MANIPULATES",
    "manipulated by": "MANIPULATES",

    # --- Perceptual: PERCEIVED_AS ---
    "perceives as": "PERCEIVED_AS",
    "perceived as": "PERCEIVED_AS",
    "sees as": "PERCEIVED_AS",
    "views as": "PERCEIVED_AS",

    # --- Spatial: TRAVELS_WITH ---
    "travels with": "TRAVELS_WITH",
    "traveling with": "TRAVELS_WITH",
    "journeys with": "TRAVELS_WITH",
    "accompanies": "TRAVELS_WITH",

    # --- Magic: BONDED_TO ---
    "bonded to": "BONDED_TO",
    "wargs into": "WARGS_INTO",
    "skinchanges into": "WARGS_INTO",

    # --- Magic: DREAMS_OF ---
    "dreams of": "DREAMS_OF",
    "has visions of": "DREAMS_OF",

    # --- Hospitality ---
    "guest of": "GUEST_OF",
    "host of": "GUEST_OF",

    # --- Factional: CONSPIRES_WITH ---
    "conspires with": "CONSPIRES_WITH",
    "plots with": "CONSPIRES_WITH",
    "in conspiracy with": "CONSPIRES_WITH",

    # --- Transactional ---
    "transactional relationship with": "CONTRACTED_WITH",

    # --- Other ---
    "named after": "NAMED_AFTER",
    "worships": "WORSHIPS",
    "clergy of": "CLERGY_OF",
    "afflicted by": "AFFLICTED_BY",
    "died of": "DIED_OF",
    "buried at": "BURIED_AT",
    "born at": "BORN_AT",
    "investigated by": "INVESTIGATES",
    "investigates": "INVESTIGATES",
    "seeks": "SEEKS",
    "searching for": "SEEKS",
    "pursues": "SEEKS",
    "spies on": "SPIES_ON",
    "negotiates with": "NEGOTIATES_WITH",
    "ransoms": "RANSOMS",
    "heals": "HEALS",
    "treated by": "HEALS",
    "poisons": "POISONS",
    "tortures": "TORTURES",
    "tortured by": "TORTURES",
    "vows to": "VOWS_TO",
    "heir to/competes with": "HEIR_TO",
    "disciplinarian over": "COMMANDS",
}

# Prefix-match map: if the normalized hint STARTS WITH one of these keys,
# map to the value. Checked in order; first match wins.
# Used for hints like "father of, protects" → PARENT_OF via prefix "father of".
HINT_PREFIX_MAP: list[tuple[str, str]] = [
    # Kinship prefixes (order matters — more specific first)
    ("half-brother", "SIBLING_OF"),
    ("half-sister", "SIBLING_OF"),
    ("half brother", "SIBLING_OF"),
    ("half sister", "SIBLING_OF"),
    ("step-", "PARENT_OF"),
    ("father of", "PARENT_OF"),
    ("mother of", "PARENT_OF"),
    ("son of", "PARENT_OF"),
    ("daughter of", "PARENT_OF"),
    ("sibling of", "SIBLING_OF"),
    ("brother of", "SIBLING_OF"),
    ("sister of", "SIBLING_OF"),
    ("uncle of", "UNCLE_OF"),
    ("aunt of", "UNCLE_OF"),
    ("cousin of", "COUSIN_OF"),
    ("heir to", "HEIR_TO"),
    ("heir of", "HEIR_TO"),
    ("betrothed", "BETROTHED_TO"),
    ("ward of", "WARD_OF"),
    ("foster", "WARD_OF"),
    # Emotional
    ("mourns", "MOURNS"),
    ("mourning", "MOURNS"),
    ("grieves", "MOURNS"),
    ("loves", "LOVES"),
    ("deep love", "LOVES"),
    ("deep affection", "LOVES"),
    ("fears", "FEARS"),
    ("fear of", "FEARS"),
    ("hates", "HATES"),
    ("hatred", "HATES"),
    ("loath", "HATES"),
    ("resents", "RESENTS"),
    ("resentment", "RESENTS"),
    ("distrusts", "DISTRUSTS"),
    ("distrust", "DISTRUSTS"),
    ("trusts", "TRUSTS"),
    ("trust in", "TRUSTS"),
    ("respects", "RESPECTS"),
    ("protects", "PROTECTS"),
    ("protective of", "PROTECTS"),
    ("protector of", "PROTECTS"),
    ("defender of", "PROTECTS"),
    ("defends", "PROTECTS"),
    ("guards", "GUARDS"),
    ("guardian of", "GUARDS"),
    ("rescues", "RESCUES"),
    ("rescued", "RESCUES"),
    ("antagonized by", "OPPOSES"),
    ("antagonizes", "OPPOSES"),
    ("opposes", "OPPOSES"),
    ("hostile toward", "OPPOSES"),
    ("enemy of", "OPPOSES"),
    ("enemies", "OPPOSES"),
    ("rival of", "OPPOSES"),
    ("companion of", "COMPANION_OF"),
    ("close companion", "COMPANION_OF"),
    ("friend of", "COMPANION_OF"),
    ("close friend", "COMPANION_OF"),
    # Knowledge / teaching
    ("student of", "TUTORS"),
    ("student/", "TUTORS"),
    ("student /", "TUTORS"),
    ("apprentice of", "TUTORS"),
    ("tutors", "TUTORS"),
    ("teaches", "TEACHES"),
    ("teacher of", "TUTORS"),
    ("teacher/", "TUTORS"),
    ("trained by", "TUTORS"),
    ("trains", "TEACHES"),
    ("instructs", "TEACHES"),
    ("reveals to", "REVEALS_TO"),
    ("reveals information", "REVEALS_TO"),
    ("informs", "REVEALS_TO"),
    ("deceives", "DECEIVES"),
    ("manipulates", "MANIPULATES"),
    ("seeks", "SEEKS"),
    ("searching for", "SEEKS"),
    ("investigates", "INVESTIGATES"),
    ("spies on", "SPIES_ON"),
    # Political
    ("serves", "SERVES"),
    ("servant of", "SERVES"),
    ("squire to", "SERVES"),
    ("commands", "COMMANDS"),
    ("leads", "COMMANDS"),
    ("rules", "RULES"),
    ("advises", "ADVISES"),
    ("advisor to", "ADVISES"),
    ("sworn to", "SWORN_TO"),
    ("sworn sword", "SWORN_TO"),
    ("member of", "MEMBER_OF"),
    ("allied with", "ALLIES_WITH"),
    ("allies with", "ALLIES_WITH"),
    ("ally of", "ALLIES_WITH"),
    ("conspires with", "CONSPIRES_WITH"),
    ("plots with", "CONSPIRES_WITH"),
    ("negotiates with", "NEGOTIATES_WITH"),
    # Military
    ("kills", "KILLS"),
    ("killed", "KILLS"),
    ("murders", "KILLS"),
    ("slays", "KILLS"),
    ("attacks", "ATTACKS"),
    ("assaults", "ATTACKS"),
    ("captures", "CAPTURES"),
    ("prisoner of", "PRISONER_OF"),
    ("captive of", "PRISONER_OF"),
    ("defeats", "DEFEATS"),
    ("defeated by", "DEFEATS"),
    ("executes", "EXECUTES"),
    ("executed by", "EXECUTES"),
    ("betrays", "BETRAYS"),
    ("betrayed by", "BETRAYS"),
    ("tortures", "TORTURES"),
    ("tortured by", "TORTURES"),
    ("poisons", "POISONS"),
    ("ransoms", "RANSOMS"),
    ("heals", "HEALS"),
    ("treated by", "HEALS"),
    # Identity / disguise
    ("disguised as", "DISGUISED_AS"),
    ("disguised protég", "DISGUISED_AS"),
    ("disguised protegee", "DISGUISED_AS"),
    ("alias of", "ALIAS_OF"),
    ("also known as", "ALIAS_OF"),
    # Possession
    ("gave", "GIFTED_TO"),
    ("gifted to", "GIFTED_TO"),
    ("gift from", "GIFTED_TO"),
    ("owns", "OWNS"),
    # Spatial
    ("travels with", "TRAVELS_WITH"),
    ("traveling with", "TRAVELS_WITH"),
    ("journeys with", "TRAVELS_WITH"),
    ("accompanies", "TRAVELS_WITH"),
    # Magic
    ("bonded to", "BONDED_TO"),
    ("wargs into", "WARGS_INTO"),
    ("skinchanges into", "WARGS_INTO"),
    ("dreams of", "DREAMS_OF"),
    ("has visions", "DREAMS_OF"),
    # Other
    ("worships", "WORSHIPS"),
    ("clergy of", "CLERGY_OF"),
    ("afflicted by", "AFFLICTED_BY"),
    ("named after", "NAMED_AFTER"),
    ("perceived as", "PERCEIVED_AS"),
    ("perceives as", "PERCEIVED_AS"),
    ("sees as", "PERCEIVED_AS"),
    ("guest of", "GUEST_OF"),
    ("disciplinarian over", "COMMANDS"),
    ("recruiter", "MEMBER_OF"),
    ("transactional", "CONTRACTED_WITH"),
    ("vows to", "VOWS_TO"),
    # Additional high-frequency phrases not in exact map
    ("contempt", "HATES"),
    ("hostile to", "OPPOSES"),
    ("hostility toward", "OPPOSES"),
    ("loyal to", "SERVES"),
    ("loyalty to", "SERVES"),
    ("loyal service", "SERVES"),
    ("formerly served", "SERVES"),
    ("in service to", "SERVES"),
    ("antagonistic", "OPPOSES"),
    ("friendship with", "COMPANION_OF"),
    ("niece of", "UNCLE_OF"),
    ("nephew of", "NEPHEW_OF"),
    ("authority over", "COMMANDS"),
    ("wary of", "DISTRUSTS"),
    ("dismissive of", "DISTRUSTS"),
    ("skeptical of", "DISTRUSTS"),
    ("threatens", "OPPOSES"),
    ("defies", "OPPOSES"),
    ("controls", "COMMANDS"),
    ("protected by", "PROTECTS"),
    ("protective toward", "PROTECTS"),
    ("protective concern", "PROTECTS"),
    ("mocks", "OPPOSES"),
    ("blames", "OPPOSES"),
]


# ---------------------------------------------------------------------------
# Keyword / regex classifier (Layer 2)
# ---------------------------------------------------------------------------
# Runs ONLY on phrases that escape both the exact map and prefix map.
# Uses compiled regex for word-boundary correctness and speed.
#
# Precedence rules (documented):
#   1. EXCLUSION entries (edge=None) fire FIRST within the list order.
#      If a phrase matches an exclusion rule, it stays in the LLM tail.
#   2. Among positive rules, the FIRST matching rule wins — more-specific
#      patterns are listed before broader ones.
#   3. IN_LAW_OF is tested before SIBLING_OF so "brother-in-law" maps
#      to IN_LAW_OF, not SIBLING_OF.
#   4. LOVER_OF is tested before LOVES so "former lover of" doesn't
#      incorrectly map via the broader \blove\b rule.
#   5. FEARFUL is tested before FEAR so "\bfearful\b" fires specifically;
#      the exclusion on "feared by" blocks the wrong-direction case.
#   6. Compound (comma-outside-parens) phrases are NOT excluded here —
#      the existing prefix layer already gates those; keyword layer only
#      sees what escapes both prior layers, which may still contain commas
#      in rare single-keyword phrases.
#
# Conservative stance: a keyword must generalise with near-zero false
# positives. Ambiguous terms ("remembers", "bond with", "devoted",
# "supports", "relies on", "worried about") are intentionally left out.
#
# Format: list of (compiled_regex, edge_type | None, label)
#   edge_type = None  →  exclusion rule (match → skip to LLM tail)
#   edge_type = str   →  positive mapping
#
HINT_KEYWORD_RULES: list[tuple[re.Pattern, str | None, str]] = [
    # -----------------------------------------------------------------------
    # EXCLUSIONS — must come before any positive rules that share substrings
    # -----------------------------------------------------------------------
    # "feared by" is the *object* of fear, not the *subject* — wrong direction.
    (re.compile(r"\bfeared by\b"), None, "excl: feared by (wrong direction)"),
    # "disrespects" contains "respect" — exclude before the RESPECTS rule.
    (re.compile(r"\bdisrespect"), None, "excl: disrespects → not RESPECTS"),
    # "murderous intent", "murderous hatred" — no actual killing recorded yet.
    (re.compile(r"\bmurderous"), None, "excl: murderous (intent, not act)"),
    # "accuses of murder" is OPPOSES or DISTRUSTS, not KILLS.
    (re.compile(r"accuses of murder"), None, "excl: accuses of murder → not KILLS"),
    # "intends/plans to murder" — not yet executed.
    (re.compile(r"intends? to murder|plans? to murder"), None, "excl: intends to murder"),
    # "complicit in murder of" — indirect, not the killer.
    (re.compile(r"complicit in murder"), None, "excl: complicit in murder"),

    # -----------------------------------------------------------------------
    # KINSHIP — from most specific to broadest
    # -----------------------------------------------------------------------
    # In-law relationships BEFORE brother/sister to capture "brother-in-law of".
    (re.compile(r"\bin-law\b|\bin law\b"), "IN_LAW_OF", "in-law"),
    # "widow of" = was married to.
    (re.compile(r"\bwidow of\b"), "SPOUSE_OF", "widow of"),
    # Betrothal variants: "was betrothed to", "former betrothed of".
    (re.compile(r"\bbetroth"), "BETROTHED_TO", "betroth-"),
    # Grandparent / grandchild.
    (re.compile(r"\bgrandson\b|\bgranddaughter\b|\bgrandfather\b|\bgrandmother\b"),
     "PARENT_OF", "grand-kin"),
    # Great-grandparent / great-aunt / great-niece etc.
    (re.compile(r"\bgreat-(?:grandmother|grandfather|niece|nephew|uncle|aunt)\b"),
     "PARENT_OF", "great-X-kin"),
    # Cousin.
    (re.compile(r"\bcousin\b"), "COUSIN_OF", "cousin"),
    # Nephew before niece/uncle/aunt to catch "nephew" explicitly.
    (re.compile(r"\bnephew\b"), "NEPHEW_OF", "nephew"),
    # Niece → UNCLE_OF (the uncle_of edge is bidirectional by convention).
    (re.compile(r"\bniece\b"), "UNCLE_OF", "niece"),
    # Uncle / aunt.
    (re.compile(r"\buncle\b|\baunt\b"), "UNCLE_OF", "uncle/aunt"),
    # Sibling — AFTER in-law so "brother-in-law" doesn't land here.
    (re.compile(r"\bbrother\b|\bsister\b"), "SIBLING_OF", "brother/sister"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: grief / longing / mourning
    # -----------------------------------------------------------------------
    (re.compile(r"\bgrief\b|\bgriev"), "MOURNS", "grief/griev-"),
    # \bmiss with verb suffix; \b prevents 'dismiss' from matching.
    (re.compile(r"\bmiss(?:es|ing|ed)?\b"), "MOURNS", "misses/missing"),
    (re.compile(r"\bmourn"), "MOURNS", "mourn-"),
    # "longs for" = yearns for absent person — MOURNS in ASOIAF context.
    (re.compile(r"\blongs for\b"), "MOURNS", "longs for"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: LOVER_OF before LOVES (more specific)
    # -----------------------------------------------------------------------
    (re.compile(r"\blover\b"), "LOVER_OF", "lover"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: LOVES
    # -----------------------------------------------------------------------
    # \bloved?\b matches "love" and "loved"; word boundary avoids "beloved" FP.
    (re.compile(r"\bloved?\b"), "LOVES", "love/loved"),
    (re.compile(r"\bfond (?:of|toward)\b"), "LOVES", "fond of/toward"),
    (re.compile(r"\baffection(?:ate)?\b"), "LOVES", "affection/affectionate"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: FEARS (exclusion for "feared by" is above)
    # -----------------------------------------------------------------------
    (re.compile(r"\bfearful\b"), "FEARS", "fearful"),
    (re.compile(r"\bfear\b"), "FEARS", "fear"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: HATES
    # -----------------------------------------------------------------------
    (re.compile(r"\bdespis"), "HATES", "despis-"),
    (re.compile(r"\bdisdain"), "HATES", "disdain-"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: RESENTS
    # -----------------------------------------------------------------------
    (re.compile(r"\bresentful\b"), "RESENTS", "resentful"),
    (re.compile(r"\bbitter\b"), "RESENTS", "bitter"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: DISTRUSTS
    # -----------------------------------------------------------------------
    (re.compile(r"\bmistrust"), "DISTRUSTS", "mistrust-"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: RESPECTS (exclusion for "disrespects" is above)
    # -----------------------------------------------------------------------
    (re.compile(r"\badmir"), "RESPECTS", "admir-"),
    # Negative lookbehind prevents "disrespect" from matching "respect".
    (re.compile(r"(?<!dis)respect"), "RESPECTS", "respect (not disrespect)"),

    # -----------------------------------------------------------------------
    # EMOTIONAL: COMPANION_OF
    # -----------------------------------------------------------------------
    (re.compile(r"\bfriendl"), "COMPANION_OF", "friendl-"),
    (re.compile(r"\bfriendship\b"), "COMPANION_OF", "friendship"),
    (re.compile(r"\bcompanion\b"), "COMPANION_OF", "companion"),
    (re.compile(r"\bcamaraderie\b"), "COMPANION_OF", "camaraderie"),

    # -----------------------------------------------------------------------
    # KNOWLEDGE: TUTORS
    # -----------------------------------------------------------------------
    (re.compile(r"\bmentor"), "TUTORS", "mentor-"),

    # -----------------------------------------------------------------------
    # POLITICAL: COMMANDS
    # -----------------------------------------------------------------------
    (re.compile(r"\bcommand"), "COMMANDS", "command-"),

    # -----------------------------------------------------------------------
    # POLITICAL: SERVES
    # -----------------------------------------------------------------------
    (re.compile(r"\bobey"), "SERVES", "obey-"),
    (re.compile(r"\bsubordinat"), "SERVES", "subordinat-"),

    # -----------------------------------------------------------------------
    # POLITICAL: ADVISES
    # -----------------------------------------------------------------------
    (re.compile(r"\bwarn"), "ADVISES", "warn-"),
    (re.compile(r"\bcounsel"), "ADVISES", "counsel-"),

    # -----------------------------------------------------------------------
    # POLITICAL: ALLIES_WITH
    # -----------------------------------------------------------------------
    (re.compile(r"\b(?:ally|allied|alliance)\b"), "ALLIES_WITH", "ally/allied/alliance"),

    # -----------------------------------------------------------------------
    # POLITICAL: CONSPIRES_WITH
    # -----------------------------------------------------------------------
    (re.compile(r"\bconspir"), "CONSPIRES_WITH", "conspir-"),

    # -----------------------------------------------------------------------
    # MILITARY: KILLS — conservative: confirmed murder act only
    # "murders", "murdered", "murderer of" but NOT "murderous" (excluded above).
    # -----------------------------------------------------------------------
    (re.compile(r"\bmurders?\b|\bmurdered\b|\bmurderer\b"), "KILLS", "murders/murdered/murderer"),

    # -----------------------------------------------------------------------
    # MILITARY: CAPTURES
    # -----------------------------------------------------------------------
    (re.compile(r"\bcaptor\b"), "CAPTURES", "captor"),

    # -----------------------------------------------------------------------
    # MILITARY: PRISONER_OF
    # -----------------------------------------------------------------------
    (re.compile(r"\bholds? (?:captive|hostage)\b"), "PRISONER_OF", "holds captive/hostage"),

    # -----------------------------------------------------------------------
    # POLITICAL: IMPRISONS (distinct vocab type from PRISONER_OF)
    # -----------------------------------------------------------------------
    (re.compile(r"\bimprison"), "IMPRISONS", "imprison-"),

    # -----------------------------------------------------------------------
    # MAGIC: WARGS_INTO
    # "warg bond with", "warging bond", "warges into" — all clearly magical.
    # -----------------------------------------------------------------------
    (re.compile(r"\bwarg"), "WARGS_INTO", "warg-"),

    # -----------------------------------------------------------------------
    # MAGIC: BONDED_TO
    # "\bbonded\b" — past-tense static bond ("bonded with", "warg-bonded to").
    # Narrow form to avoid "bond with" which is too ambiguous (sibling bond, etc.).
    # -----------------------------------------------------------------------
    (re.compile(r"\bbonded\b"), "BONDED_TO", "bonded"),
]


def map_hint_keyword(hint_norm: str) -> str | None:
    """
    Apply the keyword/regex classifier layer to a normalized hint.

    This is layer 3, run ONLY after the exact map and prefix map both return
    None. Returns a locked-vocab edge type string, or None if no rule fires
    (including when an exclusion rule matches).

    Precedence: rules are checked in list order; first match wins.
    Exclusion rules (edge_type=None) cause an immediate None return.
    """
    for rx, edge_type, _label in HINT_KEYWORD_RULES:
        if rx.search(hint_norm):
            return edge_type  # None for exclusion, str for positive match
    return None


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def normalize_hint(hint: str) -> str:
    """Return trimmed, lowercased hint for counting/matching."""
    return hint.strip().lower()


def parse_table_row(line: str) -> list[str] | None:
    """
    Parse a markdown table row like '| A | B | C | D |' into cells.
    Returns list of stripped cell strings, or None if not a data row.
    """
    line = line.strip()
    if not line.startswith("|"):
        return None
    # Strip leading/trailing pipe
    inner = line.strip("|")
    cells = [c.strip() for c in inner.split("|")]
    return cells


def is_separator_row(cells: list[str]) -> bool:
    """Return True if this is a markdown table separator (|---|---|)."""
    return all(re.match(r"^-+$", c.replace(" ", "")) for c in cells if c)


def is_header_row(cells: list[str]) -> bool:
    """Return True if this looks like the column header row."""
    normalized = [c.lower() for c in cells]
    return any("character a" in c or "relationship" in c for c in normalized)


def extract_relationships_section(text: str) -> str | None:
    """
    Extract the text content of the '## Relationships Observed' section.
    Returns the section body (everything until the next ## heading or EOF),
    or None if the section is absent.
    """
    m = re.search(
        r"## Relationships Observed\s*\n(.*?)(?=\n## |\Z)",
        text,
        re.DOTALL,
    )
    if m:
        return m.group(1)
    return None


def parse_relationships_from_section(
    section_text: str,
    chapter_id: str,
    book: str,
) -> tuple[list[dict], list[str]]:
    """
    Parse rows from the Relationships Observed section body.

    Returns:
        rows: list of dicts with keys: source, hint, hint_norm, target, evidence,
              chapter_id, book, hint_original
        warnings: list of warning strings for malformed rows
    """
    rows = []
    warnings = []
    table_started = False

    for line in section_text.split("\n"):
        cells = parse_table_row(line)
        if cells is None:
            continue
        if is_header_row(cells):
            table_started = True
            continue
        if is_separator_row(cells):
            continue
        if not table_started:
            continue

        # Expect at least 3 non-empty cells (A, Relationship, B)
        # Evidence (4th) may be absent in rare rows
        non_empty = [c for c in cells if c]
        if len(non_empty) < 3:
            if non_empty and not all(c == "" for c in non_empty):
                warnings.append(
                    f"{chapter_id}: short row (only {len(non_empty)} cells): "
                    + " | ".join(non_empty)
                )
            continue

        source = cells[0].strip() if len(cells) > 0 else ""
        hint_original = cells[1].strip() if len(cells) > 1 else ""
        target = cells[2].strip() if len(cells) > 2 else ""
        evidence = cells[3].strip() if len(cells) > 3 else ""

        # Skip if all three main columns look empty or are "None"
        if not source or not hint_original or not target:
            continue
        if source.lower() == "none" and hint_original.lower() == "none":
            continue

        rows.append(
            {
                "source": source,
                "hint_original": hint_original,
                "hint_norm": normalize_hint(hint_original),
                "target": target,
                "evidence": evidence,
                "chapter_id": chapter_id,
                "book": book,
            }
        )

    return rows, warnings


def parse_all_extractions(
    base_dir: pathlib.Path,
) -> tuple[list[dict], dict, list[str]]:
    """
    Walk all extraction files under base_dir/{agot,acok,...}/ and parse
    Relationships Observed tables.

    Returns:
        all_rows: flat list of row dicts
        file_stats: dict with keys 'total', 'had_table', 'no_table'
        warnings: accumulated warning strings
    """
    all_rows: list[dict] = []
    warnings: list[str] = []
    total = 0
    had_table = 0
    no_table = 0

    for book in BOOKS:
        book_dir = base_dir / book
        if not book_dir.exists():
            warnings.append(f"Book directory not found: {book_dir}")
            continue

        extraction_files = sorted(book_dir.glob("*.extraction.md"))
        for fpath in extraction_files:
            total += 1
            chapter_id = fpath.stem.replace(".extraction", "")
            text = fpath.read_text(encoding="utf-8")
            section = extract_relationships_section(text)

            if section is None:
                no_table += 1
                warnings.append(f"{chapter_id}: no '## Relationships Observed' section")
                continue

            had_table += 1
            rows, file_warnings = parse_relationships_from_section(section, chapter_id, book)
            all_rows.extend(rows)
            warnings.extend(file_warnings)

    file_stats = {"total": total, "had_table": had_table, "no_table": no_table}
    return all_rows, file_stats, warnings


# ---------------------------------------------------------------------------
# Hint → edge-type mapping
# ---------------------------------------------------------------------------

def map_hint_to_edge_exact_prefix(hint_norm: str) -> str | None:
    """
    Layer 1 + 2: exact map then prefix map.

    Returns a locked-vocab edge type, or None if neither layer matches.
    Compound hints (comma outside parentheses) bypass the prefix map and
    go straight to None.
    """
    if hint_norm in HINT_EXACT_MAP:
        return HINT_EXACT_MAP[hint_norm]

    # Check for compound hints (comma outside parentheses → ambiguous → LLM)
    # Strip parenthesized portions before checking
    stripped = re.sub(r"\([^)]*\)", "", hint_norm)
    if "," in stripped:
        return None

    for prefix, edge_type in HINT_PREFIX_MAP:
        if hint_norm.startswith(prefix):
            return edge_type
    return None


def map_hint_to_edge(hint_norm: str) -> str | None:
    """
    Try to deterministically map a normalized hint to a locked-vocab edge type.

    Lookup order:
    1. Exact match in HINT_EXACT_MAP
    2. Prefix match in HINT_PREFIX_MAP (first match wins)
       - SKIP prefix matching if the hint contains a comma outside parentheses,
         which signals a compound/multi-dynamic hint that should go to LLM.
    3. Keyword/regex match in HINT_KEYWORD_RULES (additive second pass,
       checked only when layers 1+2 both return None).
    4. None (LLM tail)
    """
    result = map_hint_to_edge_exact_prefix(hint_norm)
    if result is not None:
        return result
    return map_hint_keyword(hint_norm)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def build_hint_stats(
    all_rows: list[dict],
) -> tuple[dict[str, int], dict[str, dict]]:
    """
    Build frequency counts and one example per hint (original casing).

    Returns:
        freq: hint_norm → count
        examples: hint_norm → {original, source, target, chapter_id}
    """
    freq: dict[str, int] = collections.Counter()
    examples: dict[str, dict] = {}

    for row in all_rows:
        hn = row["hint_norm"]
        freq[hn] += 1
        if hn not in examples:
            examples[hn] = {
                "original": row["hint_original"],
                "source": row["source"],
                "target": row["target"],
                "chapter_id": row["chapter_id"],
            }

    return dict(freq), examples


def per_book_counts(all_rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = collections.Counter()
    for row in all_rows:
        counts[row["book"]] += 1
    return dict(counts)


def print_report(
    all_rows: list[dict],
    file_stats: dict,
    warnings: list[str],
    freq: dict[str, int],
    examples: dict[str, dict],
    coverage_pct: float,
    mapped_rows: int,
    unmapped_rows: int,
    n_mapped_distinct: int,
    n_unmapped_distinct: int,
    # Layer-split numbers for two-tier coverage display
    exact_prefix_rows: int = 0,
    exact_prefix_distinct: int = 0,
    keyword_rows: int = 0,
    keyword_distinct: int = 0,
) -> None:
    """Print the summary report to stdout."""
    total_rows = len(all_rows)
    distinct_hints = len(freq)
    book_counts = per_book_counts(all_rows)

    print("=" * 70)
    print("STAGE 4 — PASS-1 HINT INVENTORY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print("\n--- FILE COUNTS ---")
    print(f"  Total extraction files found : {file_stats['total']}")
    print(f"  Files with table             : {file_stats['had_table']}")
    print(f"  Files without table          : {file_stats['no_table']}")

    print("\n--- ROW / PHRASE COUNTS ---")
    print(f"  Total relationship rows      : {total_rows:,}")
    print(f"  Distinct hint phrases        : {distinct_hints:,}")

    print("\n--- PER-BOOK ROW COUNTS ---")
    for book in BOOKS:
        print(f"  {book.upper():<8}: {book_counts.get(book, 0):>5,} rows")

    print("\n--- TOP 25 HINT PHRASES BY FREQUENCY ---")
    top25 = sorted(freq.items(), key=lambda x: -x[1])[:25]
    for rank, (hn, count) in enumerate(top25, 1):
        ex = examples[hn]
        print(f"  {rank:>2}. [{count:>4}] {ex['original']}")
        print(f"        Example: {ex['source']} → {ex['target']}  ({ex['chapter_id']})")

    print("\n--- DETERMINISTIC COVERAGE (TWO-TIER) ---")
    ep_pct = 100.0 * exact_prefix_rows / total_rows if total_rows else 0.0
    kw_pct = 100.0 * keyword_rows / total_rows if total_rows else 0.0
    combined_pct = ep_pct + kw_pct
    print(f"  Layer 1+2 (exact + prefix map):")
    print(f"    Rows typed   : {exact_prefix_rows:>5,}  ({ep_pct:.1f}% of {total_rows:,} total)")
    print(f"    Distinct     : {exact_prefix_distinct:>5,}  of {distinct_hints:,}")
    print(f"  Layer 3 (keyword / regex — additive):")
    print(f"    Rows typed   : {keyword_rows:>5,}  (+{kw_pct:.1f}%)")
    print(f"    Distinct     : {keyword_distinct:>5,}  new phrases")
    print(f"  Combined (all three layers):")
    print(f"    Rows typed   : {mapped_rows:>5,}  ({coverage_pct:.1f}% of total rows)")
    print(f"    Distinct     : {n_mapped_distinct:>5,}  of {distinct_hints:,}")
    print(f"  LLM tail:")
    print(f"    Rows         : {unmapped_rows:>5,}  ({100 - coverage_pct:.1f}%)")
    print(f"    Distinct     : {n_unmapped_distinct:>5,}")

    print("\n--- WARNINGS / MALFORMED FILES ---")
    if warnings:
        for w in warnings:
            print(f"  WARNING: {w}")
    else:
        print("  None.")

    print("=" * 70)


# ---------------------------------------------------------------------------
# Inventory file writer
# ---------------------------------------------------------------------------

def write_inventory(
    output_path: pathlib.Path,
    all_rows: list[dict],
    file_stats: dict,
    freq: dict[str, int],
    examples: dict[str, dict],
    coverage_pct: float,
    mapped_rows: int,
    unmapped_rows: int,
    mapped_hints: dict[str, str],
    unmapped_hints: list[str],
    # Layer-split for header annotation
    exact_prefix_rows: int = 0,
    keyword_rows: int = 0,
) -> None:
    """Write working/stage4-hint-inventory.md with full inventory."""
    total_rows = len(all_rows)
    distinct_hints = len(freq)
    book_counts = per_book_counts(all_rows)

    sorted_hints = sorted(freq.items(), key=lambda x: -x[1])
    ep_pct = 100.0 * exact_prefix_rows / total_rows if total_rows else 0.0
    kw_pct = 100.0 * keyword_rows / total_rows if total_rows else 0.0

    lines = [
        "# Stage 4 — Pass-1 Hint Inventory",
        "",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"> Total extraction files: {file_stats['total']} | With table: {file_stats['had_table']} | Without: {file_stats['no_table']}  ",
        f"> Total relationship rows: {total_rows:,} | Distinct hints: {distinct_hints:,}  ",
        f"> Layer 1+2 (exact + prefix): **{ep_pct:.1f}%** ({exact_prefix_rows:,} rows)  ",
        f"> Layer 3 (keyword/regex): **+{kw_pct:.1f}%** ({keyword_rows:,} rows)  ",
        f"> Combined deterministic: **{coverage_pct:.1f}%** of rows ({mapped_rows:,} rows)  ",
        f"> LLM tail: {100 - coverage_pct:.1f}% of rows ({unmapped_rows:,} rows, {len(unmapped_hints):,} distinct phrases)  ",
        "",
        "---",
        "",
        "## Per-Book Row Counts",
        "",
        "| Book | Rows |",
        "|------|------|",
    ]
    for book in BOOKS:
        lines.append(f"| {book.upper()} | {book_counts.get(book, 0):,} |")
    lines += [
        "",
        "---",
        "",
        "## Full Hint Inventory (sorted by frequency, desc)",
        "",
        "Format: `rank. [count] original phrase` → `EDGE_TYPE` | example A → B (chapter)  ",
        "Unmapped phrases show `(LLM tail)` instead of an edge type.",
        "",
        "| Rank | Count | Hint (original casing) | Edge Type | Example A → B | Chapter |",
        "|------|-------|----------------------|-----------|---------------|---------|",
    ]

    for rank, (hn, count) in enumerate(sorted_hints, 1):
        ex = examples[hn]
        edge = mapped_hints.get(hn, "(LLM tail)")
        # Escape pipes in cells
        orig = ex["original"].replace("|", "\\|")
        src = ex["source"].replace("|", "\\|")
        tgt = ex["target"].replace("|", "\\|")
        lines.append(
            f"| {rank} | {count} | {orig} | `{edge}` | {src} → {tgt} | {ex['chapter_id']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Draft Deterministic HINT_TO_EDGE Map",
        "",
        "> Only confidently-mapped phrases. Ambiguous ones left in LLM tail.",
        "> Coverage is measured against total rows (some high-freq hints are unmapped).",
        "",
        "| Hint Phrase (normalized) | Edge Type | Rows Covered |",
        "|--------------------------|-----------|-------------|",
    ]

    # Build per-mapped-type row counts
    mapped_type_counts: dict[str, int] = collections.Counter()
    for row in all_rows:
        hn = row["hint_norm"]
        edge = map_hint_to_edge(hn)
        if edge:
            mapped_type_counts[hn] += 1

    for hn, edge in sorted(mapped_hints.items(), key=lambda x: -mapped_type_counts.get(x[0], 0)):
        count = mapped_type_counts.get(hn, 0)
        lines.append(f"| {hn} | `{edge}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Unmapped Tail (LLM work)",
        "",
        f"> {len(unmapped_hints):,} distinct phrases covering {unmapped_rows:,} rows ({100 - coverage_pct:.1f}% of total).  ",
        "> These go to Haiku for hint → edge-type classification.",
        "",
        "| Hint Phrase (normalized) | Count | Example A → B | Chapter |",
        "|--------------------------|-------|---------------|---------|",
    ]

    for hn in unmapped_hints:
        count = freq[hn]
        ex = examples[hn]
        orig = ex["original"].replace("|", "\\|")
        src = ex["source"].replace("|", "\\|")
        tgt = ex["target"].replace("|", "\\|")
        lines.append(
            f"| {orig} | {count} | {src} → {tgt} | {ex['chapter_id']} |"
        )

    lines += ["", "---", "", "*End of inventory.*", ""]

    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Residue writer
# ---------------------------------------------------------------------------

def write_residue(
    residue_path: pathlib.Path,
    unmapped_hints: list[str],
    freq: dict[str, int],
    examples: dict[str, dict],
    unmapped_rows: int,
    total_rows: int,
    coverage_pct: float,
    exact_prefix_rows: int,
    keyword_rows: int,
) -> None:
    """
    Write working/stage4-hint-residue.md with every phrase the combined
    deterministic layers still cannot type, sorted by frequency desc.
    """
    ep_pct = 100.0 * exact_prefix_rows / total_rows if total_rows else 0.0
    kw_pct = 100.0 * keyword_rows / total_rows if total_rows else 0.0

    lines = [
        "# Stage 4 — Pass-1 Hint Residue (LLM Tail)",
        "",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        "> Phrases the combined deterministic layers (exact map + prefix map + keyword/regex)  ",
        "> could NOT confidently type. These are the genuine LLM work items.",
        "",
        "## Coverage Summary",
        "",
        f"| Layer | Rows | % of {total_rows:,} total |",
        "|-------|------|-------------|",
        f"| Layer 1+2 — exact map + prefix map | {exact_prefix_rows:,} | {ep_pct:.1f}% |",
        f"| Layer 3 — keyword / regex (additive) | {keyword_rows:,} | +{kw_pct:.1f}% |",
        f"| **Combined deterministic** | **{exact_prefix_rows + keyword_rows:,}** | **{coverage_pct:.1f}%** |",
        f"| **LLM tail** | **{unmapped_rows:,}** | **{100 - coverage_pct:.1f}%** |",
        "",
        f"Distinct phrases in LLM tail: **{len(unmapped_hints):,}**",
        "",
        "---",
        "",
        "## Residue Phrases (sorted by frequency, desc)",
        "",
        "| Phrase (normalized) | Count | Example: A → B | Chapter |",
        "|---------------------|-------|----------------|---------|",
    ]

    for hn in unmapped_hints:
        count = freq[hn]
        ex = examples[hn]
        orig = ex["original"].replace("|", "\\|")
        src = ex["source"].replace("|", "\\|")
        tgt = ex["target"].replace("|", "\\|")
        lines.append(
            f"| {orig} | {count} | {src} → {tgt} | {ex['chapter_id']} |"
        )

    lines += ["", "---", "", "*End of residue list.*", ""]
    residue_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Parse Pass 1 extraction Relationships Observed tables and build a "
            "hint inventory. Reports two-tier deterministic coverage (exact+prefix "
            "baseline vs. exact+prefix+keyword combined) and writes the genuine LLM "
            "tail to a separate residue file."
        )
    )
    parser.add_argument(
        "--extractions-dir",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent / "extractions" / "mechanical",
        help="Base directory containing per-book extraction subdirectories.",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent / "working" / "stage4-hint-inventory.md",
        help="Output path for the hint inventory markdown file.",
    )
    parser.add_argument(
        "--residue",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent / "working" / "stage4-hint-residue.md",
        help="Output path for the LLM-tail residue markdown file.",
    )
    args = parser.parse_args()

    base_dir = args.extractions_dir
    if not base_dir.exists():
        print(f"ERROR: extractions directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    # --- Parse ---
    all_rows, file_stats, warnings = parse_all_extractions(base_dir)
    freq, examples = build_hint_stats(all_rows)
    total_rows = len(all_rows)

    # --- Map hints: split by layer for two-tier accounting ---
    # Layer 1+2 (exact + prefix) counts
    ep_mapped_hints: dict[str, str] = {}
    ep_unmapped: list[str] = []
    for hn in sorted(freq.keys(), key=lambda x: -freq[x]):
        edge = map_hint_to_edge_exact_prefix(hn)
        if edge:
            ep_mapped_hints[hn] = edge
        else:
            ep_unmapped.append(hn)

    exact_prefix_rows = sum(freq[hn] for hn in ep_mapped_hints)
    exact_prefix_distinct = len(ep_mapped_hints)

    # Layer 3 (keyword) applied to what escaped layers 1+2
    kw_mapped_hints: dict[str, str] = {}
    kw_unmapped_hints: list[str] = []
    for hn in ep_unmapped:
        edge = map_hint_keyword(hn)
        if edge:
            kw_mapped_hints[hn] = edge
        else:
            kw_unmapped_hints.append(hn)

    keyword_rows = sum(freq[hn] for hn in kw_mapped_hints)
    keyword_distinct = len(kw_mapped_hints)

    # Combined
    all_mapped_hints = {**ep_mapped_hints, **kw_mapped_hints}
    mapped_rows = exact_prefix_rows + keyword_rows
    unmapped_hints = kw_unmapped_hints  # sorted by freq already (inherits ep_unmapped order)
    unmapped_rows = sum(freq[hn] for hn in unmapped_hints)
    coverage_pct = 100.0 * mapped_rows / total_rows if total_rows else 0.0

    n_mapped_distinct = len(all_mapped_hints)
    n_unmapped_distinct = len(unmapped_hints)

    # --- Print report ---
    print_report(
        all_rows,
        file_stats,
        warnings,
        freq,
        examples,
        coverage_pct,
        mapped_rows,
        unmapped_rows,
        n_mapped_distinct,
        n_unmapped_distinct,
        exact_prefix_rows=exact_prefix_rows,
        exact_prefix_distinct=exact_prefix_distinct,
        keyword_rows=keyword_rows,
        keyword_distinct=keyword_distinct,
    )

    # --- Write inventory ---
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_inventory(
        args.output,
        all_rows,
        file_stats,
        freq,
        examples,
        coverage_pct,
        mapped_rows,
        unmapped_rows,
        all_mapped_hints,
        unmapped_hints,
        exact_prefix_rows=exact_prefix_rows,
        keyword_rows=keyword_rows,
    )
    print(f"\nInventory written to: {args.output}")

    # --- Write residue ---
    args.residue.parent.mkdir(parents=True, exist_ok=True)
    write_residue(
        args.residue,
        unmapped_hints,
        freq,
        examples,
        unmapped_rows,
        total_rows,
        coverage_pct,
        exact_prefix_rows,
        keyword_rows,
    )
    print(f"Residue written to:   {args.residue}")


if __name__ == "__main__":
    main()
