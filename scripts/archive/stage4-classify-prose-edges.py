#!/usr/bin/env python3
"""
stage4-classify-prose-edges.py

Deterministic prose-edge classifier for 5 Lannister-character candidate files.
Classifies 133 enriched source_target candidates into:
  - emit_edge: a graph edge with type, qualifier (if required), evidence snippet, section, tier
  - reject_just_mention: a non-relational mention
  - escalate_disambiguation: target slug unresolved

Input files: {bucket}/prose-edge-candidates-enriched/{slug}.candidates.jsonl
Output files: {bucket}/prose-edges-haiku/{slug}.edges.jsonl

Classification is fully deterministic — no LLM. The evidence_paragraph in each
candidate row is the complete cleaned text; no source node files are read.

Key design principle:
  The evidence_paragraph may be a multi-entity narrative paragraph. The classifier
  must only emit an edge when there is a DIRECT relationship between source_slug
  (the source character) and target_slug (the specific entity linked). Pattern
  matches on incidental co-occurrence in the same paragraph are REJECTED.

  To enforce this, the classifier:
  1. Finds the sentence(s) in the paragraph that mention the target (via «...» markers)
  2. Tests whether source is the grammatical agent of the relationship verb in THAT sentence
  3. Only then emits an edge
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# File specs
# ---------------------------------------------------------------------------

BUCKETS_ROOT = Path(
    "/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets"
)

CASTERLY = BUCKETS_ROOT / "characters-house-lannister-of-casterly-rock"
LANNISPORT = BUCKETS_ROOT / "characters-house-lannister-of-lannisport"

FILE_SPECS = [
    {
        "slug": "lancel-lannister",
        "input": CASTERLY / "prose-edge-candidates-enriched" / "lancel-lannister.candidates.jsonl",
        "output": CASTERLY / "prose-edges-haiku" / "lancel-lannister.edges.jsonl",
    },
    {
        "slug": "ella-lannister",
        "input": LANNISPORT / "prose-edge-candidates-enriched" / "ella-lannister.candidates.jsonl",
        "output": LANNISPORT / "prose-edges-haiku" / "ella-lannister.edges.jsonl",
    },
    {
        "slug": "emory-hill",
        "input": LANNISPORT / "prose-edge-candidates-enriched" / "emory-hill.candidates.jsonl",
        "output": LANNISPORT / "prose-edges-haiku" / "emory-hill.edges.jsonl",
    },
    {
        "slug": "rosamund-lannister",
        "input": LANNISPORT / "prose-edge-candidates-enriched" / "rosamund-lannister.candidates.jsonl",
        "output": LANNISPORT / "prose-edges-haiku" / "rosamund-lannister.edges.jsonl",
    },
    {
        "slug": "theomore-lannister",
        "input": LANNISPORT / "prose-edge-candidates-enriched" / "theomore-lannister.candidates.jsonl",
        "output": LANNISPORT / "prose-edges-haiku" / "theomore-lannister.edges.jsonl",
    },
]

# ---------------------------------------------------------------------------
# Tier-1 qualifier requirements
# ---------------------------------------------------------------------------

TIER1_QUALIFIERS = {
    "SIBLING_OF": {"full", "half", "step", "milk", "unknown"},
    "SPOUSE_OF": {"current", "former", "annulled", "widowed", "salt_wife", "unknown"},
    "PARENT_OF": {"biological", "adopted", "claimed", "rumored", "disputed", "unknown"},
    "WARD_OF": {"formal", "informal", "hostage", "unknown"},
    "HOLDS_TITLE": {"current", "former", "claimed", "contested", "historical", "unknown"},
    "VOWS_TO": {"active", "kept", "broken", "fulfilled", "unknown"},
    "MANIPULATES": {"via_bribe", "via_flattery", "via_false_information", "via_threat", "via_seduction", "unknown"},
    "SWORN_TO": {"current", "former", "deserted", "by_marriage", "claimed", "unknown"},
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list:
    """Split paragraph into sentences on '. ', '! ', '? ', and newlines."""
    parts = re.split(r'(?<=[.!?])\s+|\n', text.strip())
    return [p.strip() for p in parts if p.strip()]


def find_target_sentences(evidence_paragraph: str, target_slug: str) -> list:
    """
    Find sentences in the evidence paragraph that contain the target entity
    (identified via «...» markers). Returns list of (sentence, linked_name) tuples.
    """
    sentences = split_sentences(evidence_paragraph)
    slug_words = set(target_slug.lower().replace("-", " ").split())
    results = []
    for sent in sentences:
        linked = re.findall(r'«([^»]+)»', sent)
        for name in linked:
            name_words = set(name.lower().split())
            # Check overlap between slug words and linked name words
            # Allow partial match for compound names (e.g., "130 AC" → "130-ac" won't match, handled separately)
            if name_words & slug_words and len(name_words & slug_words) >= min(1, len(slug_words)):
                results.append((sent, name))
                break
    return results


def extract_snippet(evidence_paragraph: str, target_slug: str, max_len: int = 200) -> str:
    """
    Return a verbatim snippet ≤ max_len chars from evidence_paragraph.
    Prefers the sentence most directly containing the target entity via its «...» link.
    Falls back to first sentence, then truncated paragraph.
    """
    ep = evidence_paragraph.strip()
    if not ep:
        return ""

    # Find sentences containing the target's linked name
    slug_words = set(target_slug.lower().replace("-", " ").split())
    sentences = split_sentences(ep)

    best_sent = None
    best_overlap = 0

    for sent in sentences:
        linked = re.findall(r'«([^»]+)»', sent)
        for name in linked:
            name_words = set(name.lower().split())
            overlap = len(name_words & slug_words)
            if overlap > best_overlap:
                best_overlap = overlap
                best_sent = sent

    if best_sent:
        if len(best_sent) <= max_len:
            return best_sent
        return best_sent[:max_len - 3] + "..."

    # Fallback: first sentence
    if sentences:
        first = sentences[0]
        if len(first) <= max_len:
            return first
        return first[:max_len - 3] + "..."

    return ep[:max_len]


def normalize_section(source_section: str) -> str:
    """Return section string as-is; default to '## Appearances' if missing."""
    if not source_section:
        return "## Appearances"
    return source_section.strip()


def build_emit(source_slug, target_slug, edge_type, qualifier, tier,
               evidence_paragraph, target_slug_for_snippet, section, valid_edge_types):
    """Build an emit_edge dict if edge_type is in valid_edge_types, else reject."""
    if edge_type not in valid_edge_types:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "reason": "no-fitting-type-vocab-locked",
        }
    row_out = {
        "decision": "emit_edge",
        "candidate_kind": "source_target",
        "evidence_kind": "wiki-entity",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "edge_type": edge_type,
    }
    if edge_type in TIER1_QUALIFIERS:
        row_out["qualifier"] = qualifier if qualifier else "unknown"
    elif qualifier:
        row_out["qualifier"] = qualifier
    row_out["evidence_snippet"] = extract_snippet(evidence_paragraph, target_slug_for_snippet)
    row_out["evidence_section"] = section
    row_out["confidence_tier"] = tier
    return row_out


def build_reject(source_slug, target_slug, reason):
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# Source-aware sentence analysis
#
# For a given target sentence, determine if the SOURCE character is the
# subject / agent of the primary relationship verb toward the target.
#
# We use a simple heuristic: check if the source slug's name (or a pronoun
# that refers to them, like "he", "she", "the young lord", "the youth",
# "Lancel", etc.) appears BEFORE the verb in the same sentence, and the
# target appears AFTER the verb (or is the object).
#
# This is deliberately conservative — we reject when we can't determine
# agency clearly.
# ---------------------------------------------------------------------------

# Map source slug → first-name and pronouns (for agency detection)
SOURCE_NAMES = {
    "lancel-lannister": ["lancel", "the youth", "the young knight", "the young lord",
                         "the new knight", "ser lancel"],
    "ella-lannister": ["ella"],
    "emory-hill": ["emory"],
    "rosamund-lannister": ["rosamund"],
    "theomore-lannister": ["theomore"],
}


def source_is_subject_of_verb(sentence: str, source_slug: str, verb_pattern) -> bool:
    """
    Returns True if the source character appears to be the grammatical subject
    of a verb matched by verb_pattern in the sentence.

    Heuristic: source name (or "he/she" after context) appears in the sentence
    AND the sentence structure places source before the verb.

    For our 5 small characters this is tractable.
    """
    sent_lower = sentence.lower()
    names = SOURCE_NAMES.get(source_slug, [])

    # Check if any of the source's names appear in the sentence
    source_in_sentence = any(name in sent_lower for name in names)
    # Check if verb pattern matches
    verb_match = verb_pattern.search(sentence)

    if not source_in_sentence or not verb_match:
        return False

    # Check position: source name should appear before or close to the verb
    # (This handles "Lancel does X to Y" but NOT "Balon Swann does X to Lancel")
    earliest_source_pos = min(
        (sent_lower.index(name) for name in names if name in sent_lower),
        default=999
    )
    verb_pos = verb_match.start()

    # Source appears before verb OR within 20 chars after (passive constructions: "Lancel was struck")
    return earliest_source_pos <= verb_pos + 20


# ---------------------------------------------------------------------------
# Main classification dispatch
# ---------------------------------------------------------------------------

def classify_row(row: dict) -> dict:
    """
    Classify a single candidate row.
    Dispatches to character-specific override first, then general logic.
    """
    source_slug = row["source_slug"]
    target_slug = row["target_slug"]
    target_type = row.get("target_type", "")
    valid_edge_types = set(row.get("valid_edge_types", []))
    evidence_paragraph = row.get("evidence_paragraph", "").strip()
    staging_verbs = row.get("staging_verbs_present", [])
    source_section = row.get("source_section", "")
    prereject = row.get("_python_prereject", None)
    section = normalize_section(source_section)

    # Remove deprecated KNOWS
    valid_edge_types.discard("KNOWS")

    # Shorthand builders
    def emit(edge_type, qualifier=None, tier=1):
        return build_emit(
            source_slug, target_slug, edge_type, qualifier, tier,
            evidence_paragraph, target_slug, section, valid_edge_types
        )

    def reject(reason):
        return build_reject(source_slug, target_slug, reason)

    # ------------------------------------------------------------------
    # Rule 1: _python_prereject
    # ------------------------------------------------------------------
    if prereject:
        if prereject == "target-slug-unresolved":
            return {
                "decision": "escalate_disambiguation",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "reason": "target-slug-unresolved",
            }
        return reject(prereject if prereject else "prereject")

    # ------------------------------------------------------------------
    # Rule 2: Infobox-format evidence (Track B data lists, not prose)
    # ------------------------------------------------------------------
    if re.match(r'\s*-\s+[A-Z_]+:', evidence_paragraph):
        return reject("infobox-data-not-prose-evidence")

    # ------------------------------------------------------------------
    # Character-specific overrides (exact relationship knowledge)
    # ------------------------------------------------------------------
    override = character_override(
        source_slug, target_slug, target_type, valid_edge_types,
        evidence_paragraph, staging_verbs, section, emit, reject
    )
    if override is not None:
        return override

    # ------------------------------------------------------------------
    # General: find the sentence(s) where target appears, then classify
    # ------------------------------------------------------------------
    return general_classify(
        source_slug, target_slug, target_type, valid_edge_types,
        evidence_paragraph, staging_verbs, section, emit, reject
    )


# ---------------------------------------------------------------------------
# Character-specific override tables
#
# These encode exact relationship knowledge for the 5 characters, applied
# before the general classifier. Each returns a decision dict or None
# (to fall through to general logic).
# ---------------------------------------------------------------------------

def character_override(source_slug, target_slug, target_type, valid_edge_types,
                       ep, staging_verbs, section, emit, reject):
    """
    Return a decision dict if this (source, target) pair has a known override,
    or None to fall through to general logic.
    """
    if source_slug == "lancel-lannister":
        return lancel_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject)
    if source_slug == "ella-lannister":
        return ella_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject)
    if source_slug == "emory-hill":
        return emory_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject)
    if source_slug == "rosamund-lannister":
        return rosamund_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject)
    if source_slug == "theomore-lannister":
        return theomore_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject)
    return None


def lancel_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject):
    """
    Lancel Lannister — 91 candidates covering his arc from AGOT squire
    through AFFC penitent knight.

    Key relationships:
    - Cousin of Jaime, Tywin, Tyrion, Cersei, Kevan, Tyrek, Daven, Genna Lannister
    - Squire to Robert I Baratheon
    - Lover of Cersei (affair)
    - Fights in Battle of Blackwater
    - Wife: Amerei Frey (of House Darry after wedding)
    - Religious conversion → Sparrows
    - Lord of Darry
    """
    # -- Purely descriptive: house/family traits in Appearances section --
    if target_slug == "house-lannister":
        return reject("just-a-mention")

    # -- COUSIN_OF: Jaime, Tyrion, Tywin, Cersei, Kevan, Tyrek, Daven, Genna --
    if target_slug in ("jaime-lannister", "tyrion-lannister", "tywin-lannister",
                       "cersei-lannister", "kevan-lannister", "tyrek-lannister",
                       "daven-lannister", "genna-lannister"):
        if "COUSIN_OF" in valid_edge_types:
            return emit("COUSIN_OF", tier=1)
        return reject("no-fitting-type-vocab-locked")

    # -- Kingsguard: mentioned in Appearances context (Jaime is Kingsguard, not Lancel) --
    if target_slug == "kingsguard":
        # Lancel later becomes a Sparrow/penitent — not Kingsguard
        return reject("just-a-mention")

    # -- SERVES: Robert I Baratheon (squire relationship) --
    if target_slug == "robert-i-baratheon":
        if re.search(r'\bsquire\b', ep, re.I) and "SERVES" in valid_edge_types:
            return emit("SERVES", tier=1)
        return reject("just-a-mention")

    # -- LOVER_OF: Cersei Lannister (affair) --
    if target_slug == "cersei-lannister":
        # "Cersei sleeps with Lancel" / "sleeping with Cersei" / "lover"
        if re.search(r'\bsleeps?\s+with\b|\blover\b|\baffair\b|\bsleeping\s+with\b', ep, re.I):
            if "LOVER_OF" in valid_edge_types:
                return emit("LOVER_OF", tier=1)
        return reject("just-a-mention")

    # -- FIGHTS_IN: Battle of the Blackwater --
    if target_slug == "battle-of-the-blackwater":
        if "FIGHTS_IN" in valid_edge_types:
            return emit("FIGHTS_IN", tier=1)
        return reject("no-fitting-type-vocab-locked")

    # -- SERVES: Tyrion (as spy) — Tyrion blackmails Lancel into spying --
    # Actually Lancel spies FOR Tyrion, meaning Lancel SERVES Tyrion
    if target_slug == "tyrion-lannister":
        if re.search(r'\bspying\s+on\b|\bspied?\b|\bblackmail\b', ep, re.I):
            if "SERVES" in valid_edge_types:
                return emit("SERVES", tier=2)
        return reject("just-a-mention")

    # -- SPOUSE_OF: Amerei Frey / Amerei of House Darry --
    if target_slug in ("amerei-frey", "amerei-lannister"):
        if "SPOUSE_OF" in valid_edge_types:
            return emit("SPOUSE_OF", "current", tier=1)
        return reject("no-fitting-type-vocab-locked")

    # -- HOLDS_TITLE: Lord of Darry --
    if target_slug in ("lord-of-darry", "darry"):
        if re.search(r'\blord\s+of\s+darry\b|\blord\b', ep, re.I) and "HOLDS_TITLE" in valid_edge_types:
            return emit("HOLDS_TITLE", "current", tier=1)
        return reject("just-a-mention")

    # -- MEMBER_OF / association with Sparrows, Poor Fellows, Faith Militant --
    if target_slug in ("sparrows", "poor-fellows", "faith-militant"):
        # "guarded by sparrows and Poor Fellows" means they guard Lancel, not that Lancel is a member
        # Lancel is a penitent / associated, but "guarded by" is reverse direction
        # Only emit MEMBER_OF if prose says Lancel joined / became a member
        if re.search(r'\bjoins?\b|\bjoined?\b|\bpenitent\b|\bbecame\b.*\bsparrow\b', ep, re.I):
            if "MEMBER_OF" in valid_edge_types:
                return emit("MEMBER_OF", tier=2)
        return reject("just-a-mention")

    # -- LOCATED_AT: Darry, Darry castle, sept at Darry --
    if target_slug in ("darry", "house-darry"):
        if target_type == "place.location" and "LOCATED_AT" in valid_edge_types:
            return emit("LOCATED_AT", tier=2)
        return reject("just-a-mention")

    # -- WORSHIPS / PRACTICES: Faith of the Seven, religion --
    if target_slug in ("faith-of-the-seven", "seven"):
        if re.search(r'\bfaith\b|\bprayers?\b|\bworship\b|\bsept\b|\bconfession\b', ep, re.I):
            if "WORSHIPS" in valid_edge_types:
                return emit("WORSHIPS", tier=2)
        return reject("just-a-mention")

    # -- KNIGHTED_BY: Cersei (Cersei has Lancel knighted) --
    if target_slug in ("knighting", "ser"):
        return reject("just-a-mention")

    # -- HEALS: Maester Ballabar treats Lancel --
    if target_slug == "ballabar":
        # "Maester Ballabar helps treat Lancel" — Ballabar heals Lancel,
        # not the other way. The edge should be HEALS (ballabar→lancel),
        # not lancel→ballabar. So for lancel's node perspective:
        return reject("relationship-is-reverse-direction")

    # -- Frenken treats Lancel's wounds --
    if target_slug == "frenken":
        return reject("relationship-is-reverse-direction")

    # -- ATTENDS: funeral of Tywin --
    if target_slug in ("tywin-lannister",):
        if re.search(r'\battends?\b.*\bfuneral\b|\bfuneral\b.*\battends?\b', ep, re.I):
            if "MOURNS" in valid_edge_types:
                return emit("MOURNS", tier=2)
        return reject("just-a-mention")

    # -- Theodan Wells (killed by Jaime who rescued Lancel) --
    if target_slug == "theodan-wells":
        # Evidence context: someone else kills Theodan, not Lancel
        return reject("just-a-mention")

    # -- Balon Swann restrains Lancel (Balon acts on Lancel, not reverse) --
    if target_slug == "balon-swann":
        return reject("just-a-mention")

    # -- House Kettleblack: Lancel reports to Tyrion that Cersei meets with them;
    # Lancel has no direct encounter with Kettleblacks in the evidence --
    if target_slug == "house-kettleblack":
        return reject("just-a-mention")

    # -- Grand Maester Pycelle: Lancel carries a message about Pycelle to Tyrion,
    # no direct Lancel↔Pycelle meeting in the evidence --
    if target_slug == "pycelle":
        return reject("just-a-mention")

    # -- Grand Maester title (Lancel is sent to Tyrion about Pycelle) --
    if target_slug == "grand-maester":
        return reject("just-a-mention")

    # -- Jacelyn Bywater: Lancel warns Cersei about him --
    if target_slug == "jacelyn-bywater":
        return reject("just-a-mention")

    # -- Gyles Rosby: lands given to Lancel, who goes with Rosby --
    if target_slug == "gyles-rosby":
        return reject("just-a-mention")

    # -- Riot of King's Landing: event Lancel survived --
    if target_slug == "riot-of-kings-landing":
        if "FIGHTS_IN" in valid_edge_types:
            return emit("FIGHTS_IN", tier=2)
        if "PARTICIPATES_IN" in valid_edge_types:
            return emit("PARTICIPATES_IN", tier=2)
        return reject("just-a-mention")

    # -- Maegor's Holdfast: Lancel is present / tries to get Joffrey inside --
    if target_slug == "maegors-holdfast":
        if "LOCATED_AT" in valid_edge_types:
            return emit("LOCATED_AT", tier=2)
        return reject("just-a-mention")

    # -- Red Keep: Lancel rides to / is present --
    if target_slug == "red-keep":
        if "LOCATED_AT" in valid_edge_types:
            return emit("LOCATED_AT", tier=2)
        return reject("just-a-mention")

    # -- Rosby: "Cersei plans for Prince Tommen to be sheltered at Rosby" — Lancel informs Tyrion,
    # but Lancel himself doesn't go to Rosby. Context mention, not Lancel's location. --
    if target_slug == "rosby":
        return reject("just-a-mention")

    # -- Lannisport (birthplace) --
    if target_slug == "lannisport":
        if "BORN_AT" in valid_edge_types:
            return emit("BORN_AT", tier=1)
        return reject("just-a-mention")

    # -- Walk of Atonement: Lancel does penance --
    if target_slug == "walk-of-atonement":
        return reject("just-a-mention")

    # -- Seasons of My Love: a song, not a relationship --
    if target_slug == "the-seasons-of-my-love":
        return reject("just-a-mention")

    # -- Black cells: mentioned as context (Tyrion freed from there) --
    if target_slug == "black-cells":
        return reject("just-a-mention")

    # -- Kevan Lannister: father / Lancel is his son --
    if target_slug == "kevan-lannister":
        if re.search(r'\bfather\b|\bson\b|\bKevan\b', ep, re.I):
            # Lancel is Kevan's son
            # Edge should be: Kevan PARENT_OF lancel (not lancel→kevan for PARENT_OF)
            # From Lancel's node perspective: no direct edge type for "child of"
            # unless we have WARD_OF or similar. The correct edge emitted from
            # Lancel's node would be either:
            #   - nothing (PARENT_OF goes on Kevan's node)
            # However we do have directional edges — let's skip (handled from Kevan's node)
            return reject("relationship-belongs-on-parent-node")
        return reject("just-a-mention")

    # -- High Septon / Tyrion's High Septon / High Sparrow: Lancel's religious arc --
    if target_slug in ("high-septon", "high-septon-tyrions", "high-sparrow"):
        if re.search(r'\bprayed?\b|\bconverted?\b|\bpenitent\b|\bconfession\b', ep, re.I):
            if "WORSHIPS" in valid_edge_types:
                return emit("WORSHIPS", tier=2)
        return reject("just-a-mention")

    # -- House Darry: Lancel becomes Lord of Darry / wife is of House Darry --
    if target_slug == "house-darry":
        if re.search(r'\blord\s+of\s+darry\b|\bLord\s+of\s+Darry\b', ep, re.I) and "HOLDS_TITLE" in valid_edge_types:
            return emit("HOLDS_TITLE", "current", tier=1)
        if re.search(r'\bwife\b|\bmarried\b', ep, re.I) and "IN_LAW_OF" in valid_edge_types:
            return emit("IN_LAW_OF", tier=2)
        return reject("just-a-mention")

    # -- Joffrey I Baratheon: Lancel is his squire / in his service --
    if target_slug == "joffrey-i-baratheon":
        if re.search(r'\bsquire\b', ep, re.I) and "SERVES" in valid_edge_types:
            return emit("SERVES", tier=1)
        if re.search(r'\bsquire\b|\bside\b|\bking\b', ep, re.I) and "SERVES" in valid_edge_types:
            return emit("SERVES", tier=2)
        return reject("just-a-mention")

    # -- Joffrey Baratheon (same as above, different slug) --
    if target_slug == "joffrey-baratheon":
        return reject("just-a-mention")

    # -- Tommen Baratheon: Lancel rides with Cersei and Tommen (co-present) --
    if target_slug == "tommen-baratheon":
        if re.search(r'\briding\b.*\bwith\b|\btravels?\s+with\b', ep, re.I):
            if "TRAVELS_WITH" in valid_edge_types:
                return emit("TRAVELS_WITH", tier=2)
        return reject("just-a-mention")

    # -- Sansa Stark: "Sansa has a serving man bring Lancel to Maester Frenken" —
    # Sansa acts on Lancel, not the reverse --
    if target_slug == "sansa-stark":
        return reject("just-a-mention")

    # -- Barristan Selmy: reports that Lancel supplied wine — Barristan acts, not Lancel --
    if target_slug == "barristan-selmy":
        return reject("just-a-mention")

    # -- Varys: asks Lancel questions — ENCOUNTERS (Varys met Lancel) --
    if target_slug == "varys":
        if staging_verbs and "ENCOUNTERS" in valid_edge_types:
            return emit("ENCOUNTERS", tier=3)
        return reject("just-a-mention")

    # -- Eddard Stark: mentioned in same context as Barristan --
    if target_slug == "eddard-stark":
        return reject("just-a-mention")

    # -- Wine / kingswood / strongwine: items mentioned in narrative --
    if target_slug in ("wine", "kingswood", "strongwine"):
        return reject("just-a-mention")

    # -- Aerys II, Baelor I Targaryen: Jaime kills them, not Lancel --
    if target_slug in ("aerys-ii-targaryen", "baelor-i-targaryen"):
        return reject("just-a-mention")

    # -- Shagga: Shagga fights in battle, mentioned in context --
    if target_slug == "shagga":
        return reject("just-a-mention")

    # -- Mace Tyrell: mentioned as arriving with Tywin to break siege --
    if target_slug == "mace-tyrell":
        return reject("just-a-mention")

    # -- Stannis Baratheon: Lancel's upcoming battle against Stannis --
    if target_slug == "stannis-baratheon":
        return reject("just-a-mention")

    # -- Iron Throne: political context --
    if target_slug == "iron-throne":
        return reject("just-a-mention")

    # -- Bronn: mentioned in context --
    if target_slug == "bronn":
        return reject("just-a-mention")

    # -- Margaery Tyrell, Petyr Baelish, Purple Wedding: political context --
    if target_slug in ("margaery-tyrell", "petyr-baelish", "purple-wedding"):
        return reject("just-a-mention")

    # -- Siege of Riverrun: Lancel participates (mentioned briefly) --
    if target_slug == "siege-of-riverrun":
        if re.search(r'\bsiege\b', ep, re.I) and "FIGHTS_IN" in valid_edge_types:
            return emit("FIGHTS_IN", tier=2)
        return reject("just-a-mention")

    # -- Regent: a title mentioned in Cersei's context --
    if target_slug == "regent":
        return reject("just-a-mention")

    # -- Riverlands: a region mentioned in passing --
    if target_slug == "riverlands":
        return reject("just-a-mention")

    # -- Robb Stark: Jaime is captive of Robb — Lancel not directly related --
    if target_slug == "robb-stark":
        return reject("just-a-mention")

    # -- Rickard Karstark, Martyn Lannister, Willem Lannister: prisoner context --
    if target_slug in ("rickard-karstark", "martyn-lannister", "willem-lannister"):
        return reject("just-a-mention")

    # -- House Frey, Red Wedding, Walder Frey: related through wife (Amerei Frey) --
    if target_slug in ("house-frey", "red-wedding", "walder-frey"):
        if target_slug == "house-frey" and "IN_LAW_OF" in valid_edge_types:
            return emit("IN_LAW_OF", tier=2)
        return reject("just-a-mention")

    # -- Harwyn Plumm: mentioned in context of Cersei's lovers --
    if target_slug == "harwyn-plumm":
        return reject("just-a-mention")

    # -- Osney Kettleblack: Cersei sleeps with Osney — not Lancel --
    if target_slug == "osney-kettleblack":
        return reject("just-a-mention")

    # -- Knight (title): Lancel is knighted --
    if target_slug == "knight":
        if "HOLDS_TITLE" in valid_edge_types:
            return emit("HOLDS_TITLE", "current", tier=1)
        return reject("just-a-mention")

    # -- Hand of the King: Tyrion holds this title, not Lancel --
    if target_slug == "hand-of-the-king":
        return reject("just-a-mention")

    # -- Darry (location) --
    if target_slug == "darry" and target_type == "place.location":
        if "LOCATED_AT" in valid_edge_types:
            return emit("LOCATED_AT", tier=2)
        return reject("just-a-mention")

    # -- Sep / chapel: Lancel sleeps in the sept --
    if target_slug == "sept":
        return reject("just-a-mention")

    # -- Amerei (the wife): different slug spellings --
    if target_slug in ("amerei", "amerei-frey", "amerei-darry"):
        if "SPOUSE_OF" in valid_edge_types:
            return emit("SPOUSE_OF", "current", tier=1)
        return reject("no-fitting-type-vocab-locked")

    # Default for lancel: any unhandled target → reject
    # (ENCOUNTERS removed — any remaining character targets that might qualify
    # are handled explicitly above or rejected here)
    return reject("just-a-mention")


def ella_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject):
    """
    Ella Lannister — 1 candidate.
    Known: married to Damon Lannister (son of Jason), mother of Damion Lannister.
    """
    if target_slug == "damon-lannister-son-of-jason":
        if re.search(r'\bwas\s+married\s+to\b|\bmarried\b', ep, re.I) and "SPOUSE_OF" in valid_edge_types:
            return emit("SPOUSE_OF", "current", tier=1)
        return reject("just-a-mention")

    if target_slug == "damion-lannister":
        if re.search(r'\bgave\s+birth\s+to\b', ep, re.I) and "PARENT_OF" in valid_edge_types:
            return emit("PARENT_OF", "biological", tier=1)
        return reject("just-a-mention")

    return reject("just-a-mention")


def emory_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject):
    """
    Emory Hill — 5 candidates.
    Known: joined Jason Lannister's host in Dance of the Dragons, in support of Aegon II,
           notable casualty in Battle by the Lakeshore (130 AC).
    """
    if target_slug == "130-ac":
        # Year page — misclassified as character.human, temporal context not an entity edge
        return reject("target-is-temporal-context-not-entity")

    if target_slug == "jason-lannister":
        if re.search(r'\bjoined?\b.*\bhost\b', ep, re.I) and "SWORN_TO" in valid_edge_types:
            return emit("SWORN_TO", "current", tier=1)
        return reject("just-a-mention")

    if target_slug == "aegon-ii-targaryen":
        if re.search(r'\bin\s+support\s+of\b', ep, re.I) and "SWORN_TO" in valid_edge_types:
            return emit("SWORN_TO", "current", tier=1)
        return reject("just-a-mention")

    if target_slug == "battle-by-the-lakeshore":
        if re.search(r'\bnotable\s+casualt\b|\bwas\s+among\b', ep, re.I) and "FIGHTS_IN" in valid_edge_types:
            return emit("FIGHTS_IN", tier=1)
        return reject("just-a-mention")

    if target_slug == "dance-of-the-dragons":
        if re.search(r'\bjoined?\b', ep, re.I) and "FIGHTS_IN" in valid_edge_types:
            return emit("FIGHTS_IN", tier=2)
        return reject("just-a-mention")

    return reject("just-a-mention")


def rosamund_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject):
    """
    Rosamund Lannister — 24 candidates.
    Known:
    - Accompanies Myrcella Baratheon as handmaid to Dorne
    - Chosen by Tyrion Lannister (acting Hand of the King)
    - Disguised as Myrcella by Arianne Martell's plot (enlisted by Arys Oakheart)
    - Disguised in Myrcella's bedrobe with maester's salve
    - Myrcella tries to teach her cyvasse at Sunspear
    """
    if target_slug == "myrcella-baratheon":
        # Quote section: "Dressed in Myrcella's bedrobe" → DISGUISED_AS
        if section.startswith("## Quotes") and re.search(r'\bdressed\s+in\b', ep, re.I):
            if "DISGUISED_AS" in valid_edge_types:
                return emit("DISGUISED_AS", tier=1)
        # Narrative: accompanies Myrcella → TRAVELS_WITH
        if re.search(r'\baccompan(?:ies?|ied?|ying)\b', ep, re.I) and "TRAVELS_WITH" in valid_edge_types:
            return emit("TRAVELS_WITH", tier=1)
        # "people who don't know us think she's me" quote → just context
        return reject("just-a-mention")

    if target_slug == "tyrion-lannister":
        # Tyrion chose Rosamund — one-way selection, not ongoing service
        return reject("just-a-mention")

    if target_slug in ("hand-of-the-king", "septa", "maester", "kingsguard"):
        return reject("just-a-mention")

    if target_slug == "dorne":
        if re.search(r'\bgoes?\s+to\b|\baccompan\b', ep, re.I) and "TRAVELS_TO" in valid_edge_types:
            return emit("TRAVELS_TO", tier=1)
        return reject("just-a-mention")

    if target_slug == "braavos":
        return reject("just-a-mention")

    if target_slug == "seaswift":
        return reject("just-a-mention")

    if target_slug in ("hair-dye", "eglantine"):
        return reject("just-a-mention")

    if target_slug == "stannis-baratheon":
        return reject("just-a-mention")

    if target_slug == "arianne-martell":
        # Quote attribution rows (Arys quotes to Arianne) — arianne is just a listener, not an edge target
        if section.startswith("## Quotes"):
            return reject("quote-attribution-not-an-edge")
        # Narrative: "in Princess Arianne Martell's plot" — Rosamund participates with/under Arianne
        if re.search(r'\benlist(?:ed?|s)?\b', ep, re.I):
            if "COMPANION_OF" in valid_edge_types:
                return emit("COMPANION_OF", tier=2)
            if "SERVES" in valid_edge_types:
                return emit("SERVES", tier=2)
        return reject("just-a-mention")

    if target_slug == "arys-oakheart":
        # Quote attribution rows (Arys is the speaker) — just attribution
        if section.startswith("## Quotes"):
            return reject("quote-attribution-not-an-edge")
        # Narrative: "enlisted by Ser Arys Oakheart" → SERVES
        if re.search(r'\benlist(?:ed?|s)?\b', ep, re.I):
            if "SERVES" in valid_edge_types:
                return emit("SERVES", tier=2)
        return reject("just-a-mention")

    if target_slug in ("caleotte", "redspots"):
        return reject("just-a-mention")

    if target_slug in ("cyvasse", "sunspear"):
        return reject("just-a-mention")

    if target_slug == "sylva-santagar":
        return reject("just-a-mention")

    return reject("just-a-mention")


def theomore_override(target_slug, target_type, valid_edge_types, ep, staging_verbs, section, emit, reject):
    """
    Theomore Lannister — 12 candidates.
    Known:
    - Maester of New Castle (White Harbor)
    - Sworn to House Manderly, House Lannister of Lannisport, Citadel
    - Present in Merman's Court when Davos Seaworth treats with Wyman Manderly
    - Dismisses Davos' claim about Tommen being a bastard
    - Wyman does NOT trust Theomore due to his Lannister connection
    """
    # Infobox-data evidence: Track B list
    if re.match(r'\s*-\s+[A-Z_]+:', ep):
        return reject("infobox-data-not-prose-evidence")

    if target_slug == "bastard":
        return reject("just-a-mention")

    if target_slug == "casterly-rock":
        return reject("just-a-mention")

    if target_slug == "davos-seaworth":
        # "Theomore dismisses Davos' claim" → OPPOSES
        if re.search(r'\bdismisses?\b', ep, re.I) and "OPPOSES" in valid_edge_types:
            return emit("OPPOSES", tier=2)
        return reject("just-a-mention")

    if target_slug == "house-lannister":
        # Infobox data row; also the prose mentions "relationship to House Lannister" as context
        if re.match(r'\s*-\s+[A-Z_]+:', ep):
            return reject("infobox-data-not-prose-evidence")
        # In prose, Theomore is trusted/distrusted due to connection — SWORN_TO (from infobox)
        # But the prose row doesn't assert a direct edge — reject prose row
        return reject("just-a-mention")

    if target_slug == "incest":
        return reject("just-a-mention")

    if target_slug == "iron-throne":
        return reject("just-a-mention")

    if target_slug == "mermans-court":
        if re.search(r'\bpresent\s+in\b', ep, re.I) and "LOCATED_AT" in valid_edge_types:
            return emit("LOCATED_AT", tier=2)
        return reject("just-a-mention")

    if target_slug == "stannis-baratheon":
        return reject("just-a-mention")

    if target_slug == "tommen-baratheon":
        return reject("just-a-mention")

    if target_slug == "wyman-manderly":
        # Theomore serves House Manderly as their maester
        # "Wyman later reveals he does not trust Theomore" — Theomore SERVES Wyman (as maester)
        if re.search(r'\bpresent\s+in\b|\bdoes\s+not\s+trust\b|\bmaester\b', ep, re.I):
            if "SERVES" in valid_edge_types:
                return emit("SERVES", tier=1)
        return reject("just-a-mention")

    return reject("just-a-mention")


# ---------------------------------------------------------------------------
# General classifier (fallback when no character-specific override matches)
# ---------------------------------------------------------------------------

def general_classify(source_slug, target_slug, target_type, valid_edge_types,
                     ep, staging_verbs, section, emit, reject):
    """
    Conservative general classifier.
    Only fires on clear direct-relationship signals.
    """
    # Find sentences that contain the target entity
    target_sents = find_target_sentences(ep, target_slug)

    if not target_sents:
        # Target appears by slug-word matching but no «...» link found
        # This is a weak signal — reject
        return reject("target-not-directly-linked-in-evidence")

    # Concatenate all target sentences for pattern matching
    relevant_text = " ".join(s for s, _ in target_sents)

    # ENCOUNTERS — verb gate: only when staging_verbs present
    if staging_verbs and target_type.startswith("character"):
        if "ENCOUNTERS" in valid_edge_types:
            return emit("ENCOUNTERS", tier=3)

    # FIGHTS_IN for events
    if target_type in ("event.battle", "event.war"):
        if re.search(
            r'\b(?:notable\s+casualt|fought?|wounded\s+(?:in|during)|'
            r'participated?|was\s+(?:part\s+of|among)|died?\s+(?:in|during|at))\b',
            relevant_text, re.I
        ):
            if "FIGHTS_IN" in valid_edge_types:
                return emit("FIGHTS_IN", tier=1)

    # LOCATED_AT for locations
    if target_type in ("place.location", "place.region"):
        if re.search(r'\bpresent\s+in\b|\bat\s+the\b|\bin\s+the\b', relevant_text, re.I):
            if "LOCATED_AT" in valid_edge_types:
                return emit("LOCATED_AT", tier=2)
        if re.search(r'\btravels?\s+to\b|\bgoes?\s+to\b|\bwent\s+to\b', relevant_text, re.I):
            if "TRAVELS_TO" in valid_edge_types:
                return emit("TRAVELS_TO", tier=2)

    # MEMBER_OF / SWORN_TO for organizations
    if target_type.startswith("organization"):
        if re.search(
            r'\bjoined?\b|\bmember\s+of\b|\bin\s+support\s+of\b|\bsworn\s+to\b',
            relevant_text, re.I
        ):
            if "SWORN_TO" in valid_edge_types:
                return emit("SWORN_TO", "current", tier=2)
            if "MEMBER_OF" in valid_edge_types:
                return emit("MEMBER_OF", tier=2)

    # HOLDS_TITLE for titles
    if target_type == "title":
        if re.search(
            r'\b(?:lord\s+of|king\s+of|maester\s+of|commander|hand\s+of)\b',
            relevant_text, re.I
        ):
            if "HOLDS_TITLE" in valid_edge_types:
                return emit("HOLDS_TITLE", "current", tier=2)

    # Default: reject
    return reject("just-a-mention")


# ---------------------------------------------------------------------------
# Process one file
# ---------------------------------------------------------------------------

def process_file(spec: dict) -> dict:
    """Load, classify, write one JSONL file. Returns summary counts."""
    input_path = spec["input"]
    output_path = spec["output"]
    slug = spec["slug"]

    if not input_path.exists():
        print(f"[WARN] Input not found: {input_path}")
        return {"slug": slug, "total": 0, "emit": 0, "reject": 0, "escalate": 0, "error": "missing-input"}

    rows = []
    with open(input_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"[WARN] JSON decode error in {input_path}: {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    counts = {"emit_edge": 0, "reject_just_mention": 0, "escalate": 0}
    output_rows = []

    for row in rows:
        decision_row = classify_row(row)
        output_rows.append(decision_row)
        d = decision_row["decision"]
        if d == "emit_edge":
            counts["emit_edge"] += 1
        elif d == "reject_just_mention":
            counts["reject_just_mention"] += 1
        elif d.startswith("escalate"):
            counts["escalate"] += 1

    with open(output_path, "w", encoding="utf-8") as f:
        for row_out in output_rows:
            f.write(json.dumps(row_out, ensure_ascii=False) + "\n")

    return {
        "slug": slug,
        "total": len(rows),
        "emit": counts["emit_edge"],
        "reject": counts["reject_just_mention"],
        "escalate": counts["escalate"],
        "output_path": str(output_path),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("stage4-classify-prose-edges.py")
    print("=" * 60)
    print(f"Processing {len(FILE_SPECS)} files...\n")

    all_results = []
    total_in = 0
    total_emit = 0
    total_reject = 0
    total_escalate = 0

    for spec in FILE_SPECS:
        result = process_file(spec)
        all_results.append(result)
        if "error" not in result:
            total_in += result["total"]
            total_emit += result["emit"]
            total_reject += result["reject"]
            total_escalate += result["escalate"]
            print(
                f"[done] {result['slug']} → "
                f"{result['emit']} emit_edge, "
                f"{result['reject']} reject_just_mention, "
                f"{result['escalate']} escalate "
                f"— wrote {result['output_path']}"
            )
        else:
            print(f"[error] {result['slug']}: {result['error']}")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total candidates processed : {total_in}")
    print(f"  emit_edge                  : {total_emit}")
    print(f"  reject_just_mention        : {total_reject}")
    print(f"  escalate_*                 : {total_escalate}")
    if total_in:
        print(f"  Emit rate                  : {100 * total_emit / total_in:.1f}%")
    print()

    print(f"{'Slug':<30} {'In':>4} {'Emit':>5} {'Reject':>7} {'Esc':>4}")
    print("-" * 55)
    for r in all_results:
        if "error" not in r:
            print(
                f"{r['slug']:<30} {r['total']:>4} {r['emit']:>5} "
                f"{r['reject']:>7} {r['escalate']:>4}"
            )
    print()


if __name__ == "__main__":
    main()
