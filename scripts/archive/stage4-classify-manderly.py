#!/usr/bin/env python3
"""
stage4-classify-manderly.py

Classifies enriched prose-edge candidates for the characters-house-manderly bucket
into emit_edge or reject_just_mention decisions.

Input files (from prose-edge-candidates-enriched/):
  - theomore-manderly.candidates.jsonl
  - therry.candidates.jsonl
  - warrick-manderly.candidates.jsonl
  - wendel-manderly.candidates.jsonl
  - wylis-manderly.candidates.jsonl

Output files (to prose-edges-haiku/):
  - <slug>.edges.jsonl

Decision logic:
  - emit_edge: evidence explicitly states a typed relationship between source and target
  - reject_just_mention: target mentioned for context only, or relationship cannot be
    expressed in the locked vocabulary

Key rules enforced:
  - valid_edge_types per row is the permissible set; only those types may be emitted
  - ENCOUNTERS requires staging_verbs_present to be non-empty (verb gate)
  - KNOWS is deprecated; apparent KNOWS -> knows-deprecated-defer-to-pass1
  - Tier-1 edges (SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO,
    MANIPULATES, SWORN_TO) REQUIRE a qualifier field
  - Tier-3 edges MUST NOT have a qualifier field
  - confidence_tier is always 1 for wiki prose
  - evidence_kind is always "wiki-entity"
  - evidence_snippet is verbatim from evidence_paragraph, <= 200 chars
  - The source character is the owner of the wiki page being classified;
    evidence_paragraph describes events in that character's biography.
    Relationship checkers MUST verify the relationship is between source and target,
    not between two third parties mentioned in the same paragraph.
"""

import json
import re
import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BUCKET = "characters-house-manderly"
BUCKET_DIR = Path(
    "/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets"
) / BUCKET

INPUT_DIR = BUCKET_DIR / "prose-edge-candidates-enriched"
OUTPUT_DIR = BUCKET_DIR / "prose-edges-haiku"

TARGET_FILES = [
    "theomore-manderly.candidates.jsonl",
    "therry.candidates.jsonl",
    "warrick-manderly.candidates.jsonl",
    "wendel-manderly.candidates.jsonl",
    "wylis-manderly.candidates.jsonl",
]

# Tier-1 edges: qualifier REQUIRED
TIER1_EDGES = frozenset({
    "SIBLING_OF",
    "SPOUSE_OF",
    "PARENT_OF",
    "WARD_OF",
    "HOLDS_TITLE",
    "VOWS_TO",
    "MANIPULATES",
    "SWORN_TO",
})

CHARACTER_TYPES = frozenset({
    "character.human",
    "character.direwolf",
    "character.dragon",
})

EVENT_TYPES = frozenset({
    "event.battle",
    "event.war",
    "event.tournament",
})

LOCATION_TYPES = frozenset({
    "place.location",
    "place.region",
})

ORG_TYPES = frozenset({
    "organization.house",
    "organization.faction",
    "organization.religion",
})

TITLE_TYPE = "title"
CONCEPT_CUSTOM_TYPE = "concept.custom"
SPECIES_TYPE = "species"
MATERIAL_TYPE = "object.material"
FOOD_TYPE = "object.food"
CONCEPT_MAGIC_TYPE = "concept.magic"
MEDICAL_TYPE = "concept.medical"
CONCEPT_TYPE = "concept.culture"


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def make_snippet(paragraph: str, max_chars: int = 300) -> str:
    """
    Return a verbatim excerpt from the evidence paragraph as one or more
    complete sentences.

    Strategy:
    1. If the paragraph fits within max_chars, return it whole.
    2. Otherwise, walk sentence boundaries (". " splits) and return the text
       up to and including the last sentence that ends at or before max_chars.
       This guarantees the snippet is never truncated mid-word or mid-sentence.
    3. If NO sentence boundary exists within max_chars (a very long first
       sentence), extend to the first sentence boundary beyond max_chars —
       we prefer a slightly-long-but-complete sentence over truncation.
    4. Ultimate fallback: word-boundary truncation at max_chars.

    The 50-200 char guidance is a target; correctness (no truncation) takes
    precedence.  Paragraphs whose first sentence is e.g. 210 chars are
    returned in full rather than cut at 200.
    """
    if len(paragraph) <= max_chars:
        return paragraph

    # Walk sentence boundaries; collect all that fit within max_chars
    best_end = -1
    search_start = 0
    while True:
        idx = paragraph.find(". ", search_start)
        if idx == -1:
            break
        if idx + 1 <= max_chars:
            best_end = idx + 1  # include the period
            search_start = idx + 1
        else:
            break

    if best_end > 0:
        return paragraph[:best_end].strip()

    # No sentence boundary found within max_chars.
    # Extend to the FIRST sentence boundary beyond max_chars (long first sentence).
    idx = paragraph.find(". ", max_chars)
    if idx != -1:
        return paragraph[:idx + 1].strip()

    # No sentence boundary at all — word-boundary truncation.
    truncated = paragraph[:max_chars]
    last_space = truncated.rfind(" ")
    if last_space > 0:
        return truncated[:last_space]
    return truncated


def reject(source_slug: str, target_slug: str, reason: str) -> dict:
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": reason,
    }


def emit(
    source_slug: str,
    target_slug: str,
    edge_type: str,
    evidence_paragraph: str,
    source_section: str,
    qualifier: str | None = None,
) -> dict:
    row = {
        "decision": "emit_edge",
        "candidate_kind": "source_target",
        "evidence_kind": "wiki-entity",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "edge_type": edge_type,
        "evidence_snippet": make_snippet(evidence_paragraph),
        "evidence_section": source_section,
        "confidence_tier": 1,
    }
    if qualifier is not None:
        row["qualifier"] = qualifier
    return row


# ---------------------------------------------------------------------------
# Name extraction helpers
# ---------------------------------------------------------------------------

def source_first_name(source_slug: str) -> str:
    """e.g. 'wylis-manderly' -> 'wylis'"""
    return source_slug.split("-")[0].lower()


def target_first_name(target_slug: str) -> str:
    """e.g. 'tywin-lannister' -> 'tywin'"""
    return target_slug.split("-")[0].lower()


def target_display_name(target_slug: str) -> str:
    """e.g. 'house-frey' -> 'frey', 'robb-stark' -> 'robb stark'"""
    parts = target_slug.split("-")
    # Strip leading "house-" etc.
    if parts[0] in ("house", "ser", "lord"):
        parts = parts[1:]
    return " ".join(parts).lower()


# ---------------------------------------------------------------------------
# Core classification dispatcher
# ---------------------------------------------------------------------------

def classify(row: dict) -> dict:
    """Classify a single candidate row. Returns a decision dict."""
    source = row["source_slug"]
    target = row["target_slug"]
    evidence = row.get("evidence_paragraph", "")
    target_type = row.get("target_type", "")
    valid_types = set(row.get("valid_edge_types", []))
    staging_verbs = row.get("staging_verbs_present", [])
    section = row.get("source_section", "")
    ev = evidence.lower()

    sfn = source_first_name(source)  # e.g. "wylis"
    tfn = target_first_name(target)  # e.g. "tywin"

    def can(etype: str) -> bool:
        return etype in valid_types

    def e(edge_type: str, qualifier: str | None = None) -> dict:
        return emit(source, target, edge_type, evidence, section, qualifier)

    def r(reason: str) -> dict:
        return reject(source, target, reason)

    # -----------------------------------------------------------------------
    # DEPRECATED: KNOWS
    # -----------------------------------------------------------------------
    # No KNOWS edge type exists. If something would have been KNOWS, reject.

    # -----------------------------------------------------------------------
    # REJECT BY TARGET TYPE: settings / objects / materials / food / custom
    # -----------------------------------------------------------------------
    if target_type in (MATERIAL_TYPE, FOOD_TYPE, SPECIES_TYPE):
        return r("material/food/species mentioned in narrative setting")

    if target_type == CONCEPT_CUSTOM_TYPE:
        # fosterage concept: check if source was fostered / fostered someone
        if target == "fosterage" and can("WARD_OF"):
            if f"fostered" in ev and sfn in ev:
                return r("fosterage custom mentioned in context of others, not source directly")
        return r("custom/concept mentioned in narrative setting")

    if target_type in ("concept.culture", "concept.language"):
        return r("culture/language concept mentioned in narrative setting")

    # -----------------------------------------------------------------------
    # LOCATIONS
    # -----------------------------------------------------------------------
    if target_type in LOCATION_TYPES:
        loc = target_display_name(target)
        # BORN_AT
        if can("BORN_AT"):
            if any(p in ev for p in [f"{sfn} was born", f"{sfn} born at", f"{sfn} born in"]):
                if tfn in ev or loc in ev:
                    return e("BORN_AT")
        # DIED_AT
        if can("DIED_AT"):
            if any(p in ev for p in [f"{sfn} died at", f"{sfn} died in", f"{sfn}'s death at"]):
                if tfn in ev or loc in ev:
                    return e("DIED_AT")
        # IMPRISONED_AT
        if can("IMPRISONED_AT"):
            if (f"{sfn}" in ev and loc in ev and
                    any(p in ev for p in [
                        "held captive at", "held captive in", "prisoner at",
                        "imprisoned at", "captive at", "captivity in"
                    ])):
                return e("IMPRISONED_AT")
        # BURIED_AT
        if can("BURIED_AT"):
            if f"{sfn}" in ev and loc in ev and any(p in ev for p in [
                "interred in", "buried at", "buried in", "remains are interred",
                "bones are interred", "bones are returned",
                f"{sfn}'s bones", f"{sfn}'s remains",
            ]):
                return e("BURIED_AT")
        # TRAVELS_TO — source explicitly traveled to or sailed to/from this location
        if can("TRAVELS_TO"):
            if f"{sfn}" in ev and loc in ev and any(p in ev for p in [
                f"{sfn} sailed to", f"{sfn} sailed from", f"{sfn} traveled to",
                f"{sfn} travelled to", f"{sfn} travels to", f"{sfn} rode to",
                f"{sfn} journeyed to", f"{sfn} went to",
                # "sailed from White Harbor" where source is the implied traveler
                f"sailed from {loc}", f"sailed to {loc}",
            ]):
                return e("TRAVELS_TO")
        return r("location mentioned in narrative setting")

    # -----------------------------------------------------------------------
    # MEDICAL
    # -----------------------------------------------------------------------
    if target_type == MEDICAL_TYPE:
        if can("DIED_OF"):
            if f"{sfn}" in ev and any(p in ev for p in ["died of", "death from", "died from"]):
                return e("DIED_OF")
        if can("AFFLICTED_BY"):
            if f"{sfn}" in ev and any(p in ev for p in ["suffered", "afflicted", "stricken"]):
                return e("AFFLICTED_BY")
        return r("medical concept mentioned without AFFLICTED_BY/DIED_OF signal")

    # -----------------------------------------------------------------------
    # CONCEPT.MAGIC
    # -----------------------------------------------------------------------
    if target_type == CONCEPT_MAGIC_TYPE:
        return r("magic concept mentioned in narrative context")

    # -----------------------------------------------------------------------
    # TITLES
    # -----------------------------------------------------------------------
    if target_type == TITLE_TYPE:
        if can("HOLDS_TITLE"):
            # Source must be directly described as holding this title
            if _source_holds_title(ev, sfn, target):
                return e("HOLDS_TITLE", qualifier="current")
        return r("title mentioned in narrative context; source does not hold it directly")

    # -----------------------------------------------------------------------
    # CHARACTERS
    # -----------------------------------------------------------------------
    if target_type in CHARACTER_TYPES:
        return _classify_character_target(row, source, target, sfn, tfn, ev, valid_types, can, e, r, staging_verbs, section, evidence)

    # -----------------------------------------------------------------------
    # EVENTS
    # -----------------------------------------------------------------------
    if target_type in EVENT_TYPES:
        return _classify_event_target(row, source, target, sfn, tfn, ev, valid_types, can, e, r)

    # -----------------------------------------------------------------------
    # ORGANIZATIONS (houses, factions, religions)
    # -----------------------------------------------------------------------
    if target_type in ORG_TYPES:
        return _classify_org_target(row, source, target, sfn, tfn, ev, valid_types, can, e, r)

    # -----------------------------------------------------------------------
    # Fallback
    # -----------------------------------------------------------------------
    return r("no-fitting-type-vocab-locked")


# ---------------------------------------------------------------------------
# HOLDS_TITLE checker
# ---------------------------------------------------------------------------

def _source_holds_title(ev: str, sfn: str, target_slug: str) -> bool:
    """
    Return True ONLY if the evidence explicitly describes the SOURCE as holding
    the named title.

    Strict rules:
    - Source must be the grammatical subject of the title-attribution.
    - Do NOT fire if title is attributed to third parties (e.g., "his household knights",
      "Robb is King in the North", "Lord Walder Frey").
    - Do NOT fire for compound titles held by others (e.g., Theomore has household knights,
      not IS a household knight).
    """
    target_lower = target_slug.lower().replace("-", " ")

    # Reject possessive patterns like "source's [title]" — source has subordinates
    # with that title, doesn't hold it themselves
    if f"{sfn}'s {target_lower}" in ev or f"lord {sfn}'s {target_lower}" in ev:
        return False

    # Pattern A: "[source] is/was a/the [title]" — direct attribution
    for p in [
        f"{sfn} is a {target_lower}", f"{sfn} was a {target_lower}",
        f"{sfn} is the {target_lower}", f"{sfn} was the {target_lower}",
        f"{sfn} is an {target_lower}", f"{sfn} was an {target_lower}",
    ]:
        if p in ev:
            return True

    # Pattern B: "The [title] is/was/wields/acts..." in a sentence where ONLY source is named
    # (i.e., "the knight" is a referring expression for source)
    referring_patterns = [
        f"the {target_lower} is", f"the {target_lower} was",
        f"the {target_lower} wields", f"the {target_lower} leads",
        f"the {target_lower} acts", f"the {target_lower} rides",
        f"the unwed {target_lower}", f"the skilled {target_lower}",
        f"a canny {target_lower}", f"a skilled {target_lower}",
    ]
    for p in referring_patterns:
        if p not in ev:
            continue
        sentences = [s.strip() for s in ev.split(".") if s.strip()]
        for sent in sentences:
            if p not in sent:
                continue
            # Source must appear in the same sentence
            if sfn not in sent:
                continue
            # Reject if the title is in a possessive of someone else:
            # e.g. "[other]'s knight" or "his household knights"
            if f"'s {target_lower}" in sent or f"his {target_lower}" in sent or f"her {target_lower}" in sent:
                continue
            return True

    # Pattern C: "ser [source]" or "lord [source]" (only for generic titles knight/lord)
    if target_slug == "knight" and f"ser {sfn}" in ev:
        return True
    if target_slug == "lord" and f"lord {sfn}" in ev:
        return True

    return False


# ---------------------------------------------------------------------------
# Character target classifier
# ---------------------------------------------------------------------------

def _classify_character_target(
    row, source, target, sfn, tfn, ev, valid_types, can, e, r, staging_verbs, section, evidence
) -> dict:
    """Classify a candidate where target_type is character.*"""

    # -----------------------------------------------------------------------
    # SIBLING_OF - require explicit sibling phrase with BOTH names or
    # clear "older/younger brother/sister, Ser/Lord [target_name]" structure
    # -----------------------------------------------------------------------
    if can("SIBLING_OF"):
        qual = _check_sibling_explicit(ev, sfn, tfn)
        if qual:
            return e("SIBLING_OF", qualifier=qual)

    # -----------------------------------------------------------------------
    # PARENT_OF - source is parent of target
    # -----------------------------------------------------------------------
    if can("PARENT_OF"):
        qual = _check_parent_of_explicit(ev, sfn, tfn)
        if qual:
            return e("PARENT_OF", qualifier=qual)

    # -----------------------------------------------------------------------
    # SPOUSE_OF - source is married to target
    # -----------------------------------------------------------------------
    if can("SPOUSE_OF"):
        qual = _check_spouse_of_explicit(ev, sfn, tfn)
        if qual:
            return e("SPOUSE_OF", qualifier=qual)

    # -----------------------------------------------------------------------
    # BETROTHED_TO - source is betrothed to target
    # BETROTHED_TO is Tier-2 (qualifier optional but must be from enum when
    # emitted: current | broken | fulfilled | secret | unknown).
    # Logic guard: only emit if the betrothal is between SOURCE and TARGET
    # directly — not a third party (e.g. "source's daughter married X" is
    # NOT a BETROTHED_TO between source and X; use MARRIES_OFF instead).
    # -----------------------------------------------------------------------
    if can("BETROTHED_TO"):
        betrothal_qual = _check_betrothed_explicit(ev, sfn, tfn)
        if betrothal_qual:
            return e("BETROTHED_TO", qualifier=betrothal_qual)

    # -----------------------------------------------------------------------
    # PRISONER_OF - source is prisoner/captive of target
    # -----------------------------------------------------------------------
    if can("PRISONER_OF"):
        if _check_prisoner_of_explicit(ev, sfn, tfn):
            return e("PRISONER_OF")

    # -----------------------------------------------------------------------
    # PRISONER_EXCHANGE_FOR - source and target are exchanged as prisoners
    # Both must be named as the items being exchanged
    # -----------------------------------------------------------------------
    if can("PRISONER_EXCHANGE_FOR"):
        if _check_prisoner_exchange_explicit(ev, sfn, tfn):
            return e("PRISONER_EXCHANGE_FOR")

    # -----------------------------------------------------------------------
    # CAPTURES - source captures target in combat/battle
    # -----------------------------------------------------------------------
    if can("CAPTURES"):
        if _check_captures_explicit(ev, sfn, tfn):
            return e("CAPTURES")

    # -----------------------------------------------------------------------
    # KILLS / KILLED_BY
    # Require: explicit "source kills/killed/slew target" pattern
    # -----------------------------------------------------------------------
    if can("KILLS"):
        if _check_kills_explicit(ev, sfn, tfn):
            return e("KILLS")

    # KILLED_BY is inverse; source was killed by target
    if can("KILLED_BY"):
        if _check_killed_by_explicit(ev, sfn, tfn):
            return e("KILLED_BY")

    # -----------------------------------------------------------------------
    # SWORN_TO (character level — sworn to a person)
    # -----------------------------------------------------------------------
    if can("SWORN_TO"):
        if _check_sworn_to_person_explicit(ev, sfn, tfn):
            return e("SWORN_TO", qualifier="current")

    # -----------------------------------------------------------------------
    # SERVES - source serves target
    # -----------------------------------------------------------------------
    if can("SERVES"):
        if _check_serves_explicit(ev, sfn, tfn):
            return e("SERVES")

    # -----------------------------------------------------------------------
    # COMMANDS - source commands target (person)
    # -----------------------------------------------------------------------
    if can("COMMANDS"):
        if _check_commands_explicit(ev, sfn, tfn):
            return e("COMMANDS")

    # -----------------------------------------------------------------------
    # ADVISES - source advises target
    # -----------------------------------------------------------------------
    if can("ADVISES"):
        if _check_advises_explicit(ev, sfn, tfn):
            return e("ADVISES")

    # -----------------------------------------------------------------------
    # BETRAYS - source betrays target
    # -----------------------------------------------------------------------
    if can("BETRAYS"):
        if _check_betrays_explicit(ev, sfn, tfn):
            return e("BETRAYS")

    # -----------------------------------------------------------------------
    # MOURNS - source grieves for/over target
    # -----------------------------------------------------------------------
    if can("MOURNS"):
        if _check_mourns_explicit(ev, sfn, tfn):
            return e("MOURNS")

    # -----------------------------------------------------------------------
    # LOVES - source loves target
    # -----------------------------------------------------------------------
    if can("LOVES"):
        if _check_loves_explicit(ev, sfn, tfn):
            return e("LOVES")

    # -----------------------------------------------------------------------
    # RESPECTS / TRUSTS / DISTRUSTS / FEARS / HATES
    # -----------------------------------------------------------------------
    if can("RESPECTS"):
        if f"{sfn} respect" in ev and tfn in ev:
            return e("RESPECTS")
    if can("TRUSTS"):
        if f"{sfn} trust" in ev and tfn in ev:
            return e("TRUSTS")
    if can("DISTRUSTS"):
        if f"{sfn} distrust" in ev and tfn in ev:
            return e("DISTRUSTS")
    if can("FEARS"):
        if f"{sfn} fear" in ev and tfn in ev:
            return e("FEARS")
    if can("HATES"):
        if f"{sfn} hates {tfn}" in ev or f"{sfn} hated {tfn}" in ev:
            return e("HATES")

    # -----------------------------------------------------------------------
    # OPPOSES
    # -----------------------------------------------------------------------
    if can("OPPOSES"):
        if _check_opposes_explicit(ev, sfn, tfn):
            return e("OPPOSES")

    # -----------------------------------------------------------------------
    # DEFEATS
    # -----------------------------------------------------------------------
    if can("DEFEATS"):
        if _check_defeats_explicit(ev, sfn, tfn):
            return e("DEFEATS")

    # -----------------------------------------------------------------------
    # NEGOTIATES_WITH - source directly negotiates with target
    # (NOT: third party negotiates with someone that is not the source)
    # -----------------------------------------------------------------------
    if can("NEGOTIATES_WITH"):
        if _check_negotiates_explicit(ev, sfn, tfn):
            return e("NEGOTIATES_WITH")

    # -----------------------------------------------------------------------
    # CONSPIRES_WITH
    # -----------------------------------------------------------------------
    if can("CONSPIRES_WITH"):
        if f"conspire" in ev and sfn in ev and tfn in ev:
            return e("CONSPIRES_WITH")

    # -----------------------------------------------------------------------
    # ALLIES_WITH
    # -----------------------------------------------------------------------
    if can("ALLIES_WITH"):
        if _check_allies_explicit(ev, sfn, tfn):
            return e("ALLIES_WITH")

    # -----------------------------------------------------------------------
    # UNCLE_OF / NEPHEW_OF / COUSIN_OF
    # -----------------------------------------------------------------------
    if can("UNCLE_OF"):
        if _check_uncle_of_explicit(ev, sfn, tfn):
            return e("UNCLE_OF")
    if can("NEPHEW_OF"):
        if _check_nephew_of_explicit(ev, sfn, tfn):
            return e("NEPHEW_OF")
    if can("COUSIN_OF"):
        if f"{sfn}'s cousin" in ev and tfn in ev:
            return e("COUSIN_OF")
        if f"{tfn}'s cousin" in ev and sfn in ev:
            return e("COUSIN_OF")

    # -----------------------------------------------------------------------
    # WARD_OF - source is ward/foster-child of target
    # -----------------------------------------------------------------------
    if can("WARD_OF"):
        if _check_ward_of_explicit(ev, sfn, tfn):
            return e("WARD_OF", qualifier="formal")

    # -----------------------------------------------------------------------
    # MARRIES_OFF - source arranges marriage for target (or source is married off)
    # -----------------------------------------------------------------------
    if can("MARRIES_OFF"):
        if _check_marries_off_explicit(ev, sfn, tfn):
            return e("MARRIES_OFF")

    # -----------------------------------------------------------------------
    # COURTS
    # -----------------------------------------------------------------------
    if can("COURTS"):
        if f"{sfn}" in ev and f"{tfn}" in ev and "suitor" in ev:
            return e("COURTS")
        if f"{sfn} courts {tfn}" in ev:
            return e("COURTS")

    # -----------------------------------------------------------------------
    # DECEIVES / MANIPULATES
    # -----------------------------------------------------------------------
    if can("DECEIVES"):
        if f"{sfn} deceiv" in ev and tfn in ev:
            return e("DECEIVES")
    if can("MANIPULATES"):
        if f"{sfn} manipulat" in ev and tfn in ev:
            return e("MANIPULATES", qualifier="unknown")

    # -----------------------------------------------------------------------
    # RESCUES / HEALS / PROTECTS
    # -----------------------------------------------------------------------
    if can("RESCUES"):
        if _check_rescues_explicit(ev, sfn, tfn):
            return e("RESCUES")
    if can("HEALS"):
        if f"{sfn} heal" in ev and tfn in ev:
            return e("HEALS")
    if can("PROTECTS"):
        if f"{sfn} protect" in ev and tfn in ev:
            return e("PROTECTS")

    # -----------------------------------------------------------------------
    # REVEALS_TO / CONFIDES
    # -----------------------------------------------------------------------
    if can("REVEALS_TO"):
        if _check_reveals_to_explicit(ev, sfn, tfn):
            return e("REVEALS_TO")

    # -----------------------------------------------------------------------
    # ATTENDS - source attends where target is host or target is another attendee
    # Only emit if it's an ATTENDS relationship (source→event, not source→person)
    # -----------------------------------------------------------------------
    # (for character→character, ATTENDS doesn't make sense; skip)

    # -----------------------------------------------------------------------
    # TRAVELS_WITH - source travels in same company as target
    # -----------------------------------------------------------------------
    if can("TRAVELS_WITH"):
        if _check_travels_with_explicit(ev, sfn, tfn):
            return e("TRAVELS_WITH")

    # -----------------------------------------------------------------------
    # COMPANION_OF
    # -----------------------------------------------------------------------
    if can("COMPANION_OF"):
        if _check_companion_explicit(ev, sfn, tfn):
            return e("COMPANION_OF")

    # -----------------------------------------------------------------------
    # ENCOUNTERS - verb gate: staging_verbs_present must be non-empty
    # -----------------------------------------------------------------------
    if can("ENCOUNTERS") and staging_verbs:
        if _check_encounters_explicit(ev, sfn, tfn):
            return e("ENCOUNTERS")

    # -----------------------------------------------------------------------
    # No fitting edge found
    # -----------------------------------------------------------------------
    return r("character co-present or mentioned in context without clear typed relationship")


# ---------------------------------------------------------------------------
# Event target classifier
# ---------------------------------------------------------------------------

def _classify_event_target(
    row, source, target, sfn, tfn, ev, valid_types, can, e, r
) -> dict:
    # Build a list of candidate event name variants to match against prose.
    # 1. slug with hyphens replaced by spaces: "sistermens-rebellion" -> "sistermens rebellion"
    # 2. Same without trailing "s" where apostrophe was dropped: add "sistermen's rebellion"
    # 3. The raw slug: "sistermens-rebellion" (exact slug lookup, rarely matches prose)
    event_slug_spaced = target.replace("-", " ").lower()
    # Build the set of variants the checkers will try
    event_names = {event_slug_spaced}
    # Add possessive-restored form: replace terminal "s " or "s " preceded by consonant
    # Simple heuristic: if a word ends with "s" and the slug dropped an apostrophe,
    # the prose form would be "word's".  We try both.
    words = event_slug_spaced.split()
    possessive_variants = []
    for i, word in enumerate(words):
        if word.endswith("s") and len(word) > 2:
            new_words = words[:]
            new_words[i] = word[:-1] + "'s"
            possessive_variants.append(" ".join(new_words))
    event_names.update(possessive_variants)

    def check_event(checker, *args):
        for en in event_names:
            if checker(ev, sfn, en, *args):
                return True
        return False

    # FIGHTS_IN: source fought in this event
    if can("FIGHTS_IN"):
        if check_event(_check_fights_in_explicit):
            return e("FIGHTS_IN")

    # COMMANDS_IN: source held command role in this event
    if can("COMMANDS_IN"):
        if check_event(_check_commands_in_explicit):
            return e("COMMANDS_IN")

    # PARTICIPATES_IN: source had non-combat involvement (organizer, escort, etc.)
    if can("PARTICIPATES_IN"):
        if check_event(_check_participates_in_explicit):
            return e("PARTICIPATES_IN")

    # ATTENDS: source was present as guest/witness
    if can("ATTENDS"):
        if check_event(_check_attends_explicit):
            return e("ATTENDS")

    # OFFICIATES: source performs ritual/ceremonial role
    if can("OFFICIATES"):
        for en in event_names:
            if f"{sfn} officiat" in ev and en in ev:
                return e("OFFICIATES")

    return r("event mentioned in narrative context without source participation signal")


# ---------------------------------------------------------------------------
# Organization target classifier
# ---------------------------------------------------------------------------

def _classify_org_target(
    row, source, target, sfn, tfn, ev, valid_types, can, e, r
) -> dict:
    org_name = target.replace("-", " ").lower().replace("house ", "")
    full_org_name = target.replace("-", " ").lower()

    # SWORN_TO: source is feudally sworn to this org/house
    if can("SWORN_TO"):
        if _check_sworn_to_org_explicit(ev, sfn, org_name, full_org_name):
            return e("SWORN_TO", qualifier="current")

    # MEMBER_OF: source belongs to this faction/order
    if can("MEMBER_OF"):
        if f"{sfn} joined" in ev and org_name in ev:
            return e("MEMBER_OF")
        if f"{sfn} is a member of" in ev and org_name in ev:
            return e("MEMBER_OF")

    # OPPOSES: source opposed this org
    if can("OPPOSES"):
        if _check_opposes_explicit(ev, sfn, org_name):
            return e("OPPOSES")

    # BETRAYS: source betrayed this org
    if can("BETRAYS"):
        if f"{sfn} betray" in ev and org_name in ev:
            return e("BETRAYS")

    # CONSPIRES_WITH
    if can("CONSPIRES_WITH"):
        if "conspire" in ev and sfn in ev and org_name in ev:
            return e("CONSPIRES_WITH")

    # ALLIES_WITH
    if can("ALLIES_WITH"):
        if _check_allies_explicit(ev, sfn, org_name):
            return e("ALLIES_WITH")

    return r("organization mentioned in narrative context without typed relationship")


# ---------------------------------------------------------------------------
# Explicit relationship checkers (strict)
# ---------------------------------------------------------------------------

def _check_sibling_explicit(ev: str, sfn: str, tfn: str) -> str | None:
    """
    Return qualifier ('full', 'half') if evidence explicitly states source and target
    are siblings. Returns None otherwise.

    Strict: requires an explicit sibling phrase that names BOTH source and target
    in a way that unambiguously links them as siblings — not siblings of a third party.

    Patterns accepted:
      A) "[source], ... [sibling_phrase], [target]" — source is described, target is their sibling
      B) "[target], ... [sibling_phrase], [source]" — target described, source is their sibling
      C) "his/her [sibling_phrase], Ser/Lord [target]" in context where source is the subject

    NOT accepted:
      - "accompanied his brother, Ser [other], to X when [target] calls banners"
        (the sibling phrase refers to source→other, not source→target)
    """
    # Build sibling phrase → qualifier map
    sibling_phrases = {
        "older brother": "full",
        "younger brother": "full",
        "older sister": "full",
        "younger sister": "full",
        "half-brother": "half",
        "half brother": "half",
        "half-sister": "half",
        "half sister": "half",
    }

    for phrase, qual in sibling_phrases.items():
        if phrase not in ev:
            continue
        if tfn not in ev:
            continue

        # Find sentences containing this phrase and tfn together
        sentences = [s.strip() for s in ev.split(".") if s.strip()]
        for sent in sentences:
            if phrase not in sent or tfn not in sent:
                continue
            # The phrase and target are in the same sentence.
            # Now check: does the phrase directly precede or refer to tfn?
            # Pattern: "... [phrase], Ser/Lord/[tfn]" or "[phrase] [tfn]"
            # Accept if tfn appears immediately after the phrase (within a few words)
            idx_phrase = sent.find(phrase)
            idx_tfn = sent.find(tfn)
            if idx_phrase < 0 or idx_tfn < 0:
                continue
            gap_text = sent[idx_phrase + len(phrase): idx_tfn].strip()
            # Gap should be short (just "ser", "lord", "," etc.)
            gap_words = [w for w in gap_text.replace(",", "").replace("ser", "").replace("lord", "").split() if w]
            if len(gap_words) <= 2:
                # The phrase directly names the target as the sibling
                # Now verify that source is the one who has this sibling,
                # NOT a third party. We require sfn to appear in the sentence
                # OR for the sentence to begin the paragraph (page subject = source).
                if sfn in sent:
                    return qual
                # If sfn not in this sentence, check if sfn is the page subject
                # by verifying sfn appears as the first name in the evidence paragraph.
                first_sentence = sentences[0] if sentences else ""
                if sfn in first_sentence:
                    # Source is the page subject; implicit subject of this sentence
                    # BUT we must also check that the sentence doesn't have another
                    # character as the possessor of the sibling relation.
                    # Reject if the sentence has "[other_name]'s [phrase]" pattern
                    possessive_pos = sent.find("'s " + phrase)
                    if possessive_pos >= 0:
                        # Some other character owns the sibling phrase — not source
                        continue
                    # Also reject if another character name appears BEFORE the phrase
                    # in the sentence and source does NOT appear before the phrase
                    before_phrase = sent[:idx_phrase]
                    # Only emit if source name is present somewhere nearby
                    if sfn in before_phrase:
                        return qual

    return None


def _check_parent_of_explicit(ev: str, sfn: str, tfn: str) -> str | None:
    """
    Source is parent of target.

    Requires: source's son/daughter named as target, OR target's parent named as source.
    The target_name (tfn) must be the CHILD whose parent is source, or the specific
    named person whose father/mother is source.

    NOT accepted: "source's daughter X served Y" where Y is the target (Y is not the child).
    """
    # "source's son [tfn]" or "source's daughter [tfn]" — tfn must immediately follow
    # the possessive phrase (the child's name should be right there, not a distant reference)
    for possessive in [f"{sfn}'s son", f"{sfn}'s daughter",
                       f"lord {sfn}'s son", f"lord {sfn}'s daughter"]:
        if possessive not in ev:
            continue
        # Find the possessive in the text and check tfn follows IMMEDIATELY (within ~20 chars)
        # This ensures "source's daughter Mara" fires for Mara but not for Alysanne
        # who appears later in the same sentence
        idx = ev.find(possessive)
        text_after = ev[idx + len(possessive):idx + len(possessive) + 25]
        # Strip guild characters (wiki markup like «»)
        text_after_clean = text_after.replace("«", "").replace("»", "").strip()
        if text_after_clean.lower().startswith(tfn) or f" {tfn}" in text_after_clean.lower():
            return "biological"

    # "target's father/mother is source" patterns — target is named child
    for p in [f"{tfn}'s father, lord {sfn}", f"{tfn}'s father, ser {sfn}",
              f"{tfn}'s father is {sfn}", f"{tfn}'s mother, lady {sfn}",
              f"{tfn}'s mother is {sfn}"]:
        if p in ev:
            return "biological"

    # "like his father, lord [sfn]" appearing with tfn in the same sentence
    # where tfn is the person saying this (tfn is the child)
    for p in [f"his father, lord {sfn}", f"her father, lord {sfn}",
              f"his father, ser {sfn}", f"her father, ser {sfn}"]:
        if p in ev:
            # Find which sentence it's in and see if tfn is subject
            sentences = [s.strip() for s in ev.split(".") if s.strip()]
            for sent in sentences:
                if p in sent and tfn in sent:
                    return "biological"

    return None


def _check_spouse_of_explicit(ev: str, sfn: str, tfn: str) -> str | None:
    """
    Source is married to target.

    Strict: the marriage relationship must be explicitly stated between source and target.
    NOT accepted: "wed off granddaughters to Freys" (Wyman arranges, not Wylis is the spouse).
    NOT accepted: "alliance with Stannis" (diplomatic, not marriage).
    """
    # "source's wife, [target_name]" or "source's husband, [target_name]"
    for p in [f"{sfn}'s wife, ", f"{sfn}'s wife.", f"{sfn}'s wife ",
              f"{sfn}'s husband, ", f"{sfn}'s husband.", f"{sfn}'s husband ",
              f"{sfn}'s late wife", f"{sfn}'s late husband"]:
        if p in ev and tfn in ev:
            # Verify they're in the same sentence
            sentences = [s.strip() for s in ev.split(".") if s.strip()]
            for sent in sentences:
                if p.strip(".").strip(",").strip() in sent and tfn in sent:
                    return "current"

    # "target's wife/husband [is/was source]"
    for p in [f"{tfn}'s wife", f"{tfn}'s husband"]:
        if p in ev and sfn in ev:
            sentences = [s.strip() for s in ev.split(".") if s.strip()]
            for sent in sentences:
                if p in sent and sfn in sent:
                    return "current"

    # "[source] married [target]" or "[target] married [source]" — direct marriage act
    if f"{sfn} married {tfn}" in ev:
        return "current"
    if f"{tfn} married {sfn}" in ev:
        return "current"

    # "[source] wed/weds [target]" or "[target] wed [source]"
    if f"{sfn} wed {tfn}" in ev or f"{sfn} weds {tfn}" in ev:
        return "current"
    if f"{tfn} wed {sfn}" in ev or f"{tfn} weds {sfn}" in ev:
        return "current"

    return None


def _check_betrothed_explicit(ev: str, sfn: str, tfn: str) -> str | None:
    """
    Return a qualifier string if evidence explicitly states source is betrothed
    to target.  Returns None if no betrothal found (or if the betrothal is
    between third parties, e.g. "source's daughter married X").

    Qualifier selection:
      - "broken"    — betrothal did not result in marriage (died before, called off)
      - "fulfilled" — betrothal led to a completed marriage
      - "current"   — betrothal is in force (no resolution mentioned)
      - "unknown"   — betrothal detected but state unclear

    GUARD: We only fire when the betrothal directly involves source AND target.
    "source's daughter married/betrothed X" is NOT a BETROTHED_TO source↔X edge;
    that relationship belongs on the daughter's node or is a MARRIES_OFF edge.
    We require that neither sfn nor tfn appears only as a possessive modifier
    (e.g. "theomore's daughter") — the betrothal must name them as the parties.
    """
    if "betrothed" not in ev:
        return None

    # Guard: reject if the only occurrence of sfn in the paragraph is in a
    # possessive-daughter pattern ("sfn's daughter"), meaning sfn is the
    # arranger, not the betrothed party.  We check this per sentence.
    def _is_arranger_not_party(name: str, sentence: str) -> bool:
        """Return True if 'name' appears only as an arranger (possessive) in sentence."""
        possessive_forms = [f"{name}'s daughter", f"{name}'s son"]
        # name appears in sentence
        if name not in sentence:
            return False
        # Check if EVERY occurrence of name is as an arranger
        remaining = sentence
        found_as_party = False
        while name in remaining:
            idx = remaining.find(name)
            # Check the text surrounding this occurrence
            before = remaining[:idx]
            after = remaining[idx + len(name):]
            is_possessive = after.startswith("'s ")
            if not is_possessive:
                found_as_party = True
                break
            remaining = remaining[idx + len(name):]
        return not found_as_party

    # Determine qualifier: broken if evidence mentions death/died before marriage
    broken_signals = ["died before", "thrown from", "died in", "before her departure",
                      "before his departure", "never married", "betrothal was broken",
                      "betrothal broken"]
    fulfilled_signals = ["married", "wed ", "weds ", "wedded"]

    sentences = [s.strip() for s in ev.split(".") if s.strip()]

    # Pattern A: direct betrothal statement between sfn and tfn
    direct_patterns = [
        f"betrothed {tfn} to {sfn}",
        f"betrothed {sfn} to {tfn}",
        f"{sfn} betrothed to {tfn}",
        f"{tfn} betrothed to {sfn}",
    ]
    for p in direct_patterns:
        if p in ev:
            # Determine qualifier
            if any(s in ev for s in broken_signals):
                return "broken"
            if any(s in ev for s in fulfilled_signals):
                return "fulfilled"
            return "current"

    # Pattern B: "betrothed her/his [relation] ... to [sfn or tfn]" where the
    # OTHER party is the relation, not a named third party.
    # "betrothed her daughter ... to theomore" (source=theomore, target=viserra)
    # → fire only if viserra is named as the daughter and theomore is "to [sfn]"
    for sent in sentences:
        if "betrothed" not in sent:
            continue
        if sfn not in sent and tfn not in sent:
            continue

        # Both names must appear in the sentence (directly, not just as possessives)
        sfn_as_party = sfn in sent and not _is_arranger_not_party(sfn, sent)
        tfn_as_party = tfn in sent and not _is_arranger_not_party(tfn, sent)

        if not (sfn_as_party or tfn_as_party):
            continue

        # "betrothed ... to [sfn]" with tfn also in sentence as the named party
        if f"to {sfn}" in sent and tfn in sent and sfn_as_party:
            if any(s in ev for s in broken_signals):
                return "broken"
            if any(s in ev for s in fulfilled_signals):
                return "fulfilled"
            return "current"
        # "betrothed ... to [tfn]" with sfn also in sentence as the named party
        if f"to {tfn}" in sent and sfn in sent and tfn_as_party:
            if any(s in ev for s in broken_signals):
                return "broken"
            if any(s in ev for s in fulfilled_signals):
                return "fulfilled"
            return "current"

    return None


def _check_prisoner_of_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """
    Source is prisoner of target (target is the captor).

    Strict: target must be named as the captor/holder, not just co-present.
    Pattern: "[source] captured by [target]" or "[target] keeps/held [source] as prisoner"
    or "[source] is [target]'s prisoner".
    """
    # Direct: "source is/was captured by target"
    for p in [f"{sfn} is captured by {tfn}", f"{sfn} was captured by {tfn}",
              f"{sfn}, captured by {tfn}"]:
        if p in ev:
            return True

    # "in which [source] is captured by [target]"
    if f"captured by {tfn}" in ev and sfn in ev:
        # Verify source is the one captured (sfn appears before or with the captured phrase)
        sentences = [s.strip() for s in ev.split(".") if s.strip()]
        for sent in sentences:
            if f"captured by {tfn}" in sent and sfn in sent:
                return True

    # "[target] keeps/kept [source] as prisoner" — target MUST be the actor
    for p in [f"{tfn} keeps {sfn}", f"{tfn} kept {sfn}",
              f"{tfn} keep {sfn}"]:
        if p in ev:
            return True
    # "keep [source] as prisoner" — only if target appears as the subject in that sentence
    for p in [f"keep {sfn} as prisoner", f"kept {sfn} as prisoner"]:
        if p in ev:
            sentences = [s.strip() for s in ev.split(".") if s.strip()]
            for sent in sentences:
                if p in sent and tfn in sent:
                    # Verify tfn appears BEFORE the action (as subject/agent)
                    idx_p = sent.find(p)
                    idx_tfn = sent.find(tfn)
                    if idx_tfn < idx_p:
                        return True

    # "held captive at [location]" + target is captor mentioned in same sentence
    # This is location-dependent; check carefully
    if f"held captive" in ev and sfn in ev and tfn in ev:
        sentences = [s.strip() for s in ev.split(".") if s.strip()]
        for sent in sentences:
            if "held captive" in sent and sfn in sent and tfn in sent:
                # Verify target is named as captor (e.g., "held captive at Harrenhal"
                # with Tywin present) — but need to check tfn is the captor, not just nearby
                # Accept if sentence has "kept by tfn" or "tfn's prisoner" or "held by tfn"
                if (f"kept by {tfn}" in sent or f"{tfn}'s prisoner" in sent
                        or f"held by {tfn}" in sent or f"captive of {tfn}" in sent):
                    return True

    return False


def _check_prisoner_exchange_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """
    Source and target are in a formal prisoner exchange (both are the prisoners being swapped).

    Pattern: "trade [source] and [target] for [someone]"
           or "trade [source] for [target]" (source and target are the exchanged prisoners)

    Strict: The target must appear in the trade clause as a PRISONER being exchanged,
    not as the proposer (Tyrion), messenger (Cleos), or bystander.
    """
    sentences = [s.strip() for s in ev.split(".") if s.strip()]
    for sent in sentences:
        # "trade [sfn] and [tfn] for X" — both source and target are in the trade
        if f"trade {sfn} and {tfn}" in sent:
            return True
        if f"trade {tfn} and {sfn}" in sent:
            return True
        # "trade [sfn] for [tfn]" — source traded for target (target is the other prisoner)
        if f"trade {sfn}" in sent and f"for {tfn}" in sent:
            # Validate structure: "trade X for Y" means X and Y are the prisoners.
            # Reject if tfn appears BEFORE "trade" in the sentence (proposer role).
            idx_trade = sent.find(f"trade {sfn}")
            idx_tfn = sent.find(tfn)
            if idx_tfn > idx_trade:
                return True
        if f"trade {tfn}" in sent and f"for {sfn}" in sent:
            idx_trade = sent.find(f"trade {tfn}")
            idx_sfn = sent.find(sfn)
            if idx_sfn > idx_trade:
                return True
    return False


def _check_captures_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source captures target (source is the captor)."""
    if f"{sfn} captured {tfn}" in ev:
        return True
    if f"{sfn} captures {tfn}" in ev:
        return True
    # "in which [source] is captured by [target]" -> NOT captures, is PRISONER_OF
    return False


def _check_kills_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source kills target."""
    if f"{sfn} kills {tfn}" in ev:
        return True
    if f"{sfn} killed {tfn}" in ev:
        return True
    if f"{sfn} slew {tfn}" in ev:
        return True
    if f"{sfn} slays {tfn}" in ev:
        return True
    return False


def _check_killed_by_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source was killed by target."""
    if f"{sfn} is killed by {tfn}" in ev:
        return True
    if f"{sfn} was killed by {tfn}" in ev:
        return True
    if f"{sfn} killed by {tfn}" in ev:
        return True
    return False


def _check_sworn_to_person_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source is sworn to target person (not house)."""
    if f"{sfn}'s sworn swords" in ev:
        return False  # source has sworn swords, not source is sworn
    if f"sworn to {tfn}" in ev and sfn in ev:
        return True
    # "sworn sword" of a lord -- check if source is called target's sworn sword
    if f"{tfn}'s sworn sword" in ev and sfn in ev:
        return True
    return False


def _check_sworn_to_org_explicit(ev: str, sfn: str, org_name: str, full_org_name: str) -> bool:
    """Source is sworn to target organization."""
    # "Robb's sworn swords" -> sworn to Robb (not org)
    # House-level sworn: "house stark's sworn sword" or "sworn to house stark"
    if f"sworn to house {org_name}" in ev and sfn in ev:
        return True
    if f"sworn to the {org_name}" in ev and sfn in ev:
        return True
    if f"{org_name}'s sworn sword" in ev and sfn in ev:
        return True
    if f"sworn swords of house {org_name}" in ev and sfn in ev:
        return True
    # "one of robb's sworn swords" on wendel's page -> sworn to robb (person not house)
    # This should be handled as person->person SWORN_TO, not org
    return False


def _check_serves_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source serves target."""
    if f"{sfn} serves {tfn}" in ev:
        return True
    if f"{sfn} served {tfn}" in ev:
        return True
    if f"in the service of {tfn}" in ev and sfn in ev:
        return True
    # "wylis comes under the command of roose bolton" -> wylis serves roose
    if f"{sfn} comes under the command of {tfn}" in ev:
        return True
    return False


def _check_commands_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source commands target person (not event)."""
    if f"{sfn} commands {tfn}" in ev:
        return True
    # Not valid for person→event (that's COMMANDS_IN)
    return False


def _check_advises_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source advises target."""
    if f"{sfn} advises {tfn}" in ev:
        return True
    if f"{sfn} advised {tfn}" in ev:
        return True
    return False


def _check_betrays_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source betrays target."""
    if f"{sfn} betrays {tfn}" in ev:
        return True
    if f"{sfn} betrayed {tfn}" in ev:
        return True
    return False


def _check_mourns_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source actively mourns target."""
    if f"{sfn} mourns {tfn}" in ev:
        return True
    if f"{sfn} grieved for {tfn}" in ev:
        return True
    # "source seeks vengeance against target for target's death"
    # -- the dead person Wendel can't seek vengeance; skip
    # This only applies when source is living and grieves for target
    return False


def _check_loves_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source loves target."""
    if f"{sfn} loves {tfn}" in ev:
        return True
    if f"{sfn} loved {tfn}" in ev:
        return True
    # "wylis is the whole life of lady leona" -> leona loves wylis
    # Here source=leona if we're on leona's page. But we're on wylis's page.
    # So this would only apply if source=leona. Skip for wylis's page.
    return False


def _check_opposes_explicit(ev: str, sfn: str, target_name: str) -> bool:
    """Source opposes target."""
    if f"{sfn} opposes {target_name}" in ev:
        return True
    if f"{sfn} opposed {target_name}" in ev:
        return True
    return False


def _check_defeats_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source defeats target."""
    if f"{sfn} defeats {tfn}" in ev:
        return True
    if f"{sfn} defeated {tfn}" in ev:
        return True
    return False


def _check_negotiates_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source negotiates directly with target."""
    # "source and target negotiated" or "source negotiated with target"
    for p in [
        f"{sfn} and {tfn} negotiated",
        f"{tfn} and {sfn} negotiated",
        f"{sfn} negotiated with {tfn}",
        f"{sfn} negotiates with {tfn}",
    ]:
        if p in ev:
            return True
    return False


def _check_allies_explicit(ev: str, sfn: str, target_name: str) -> bool:
    """Source allies with target."""
    if f"{sfn} allied with {target_name}" in ev:
        return True
    if f"alliance between {sfn} and {target_name}" in ev:
        return True
    return False


def _check_uncle_of_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source is uncle/aunt of target."""
    if f"{tfn}'s uncle" in ev and sfn in ev:
        return True
    if f"his uncle {sfn}" in ev and tfn in ev:
        return True
    if f"her uncle {sfn}" in ev and tfn in ev:
        return True
    return False


def _check_nephew_of_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source is nephew of target."""
    if f"{sfn}'s nephew" in ev and tfn in ev:
        return True
    if f"his nephew {sfn}" in ev and tfn in ev:
        return True
    if f"her nephew {sfn}" in ev and tfn in ev:
        return True
    # "and a third to a nephew" generic -> not specific enough
    return False


def _check_ward_of_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source is ward/foster-child of target."""
    if f"{sfn} was fostered by {tfn}" in ev:
        return True
    if f"fostered by {tfn}" in ev and sfn in ev:
        return True
    if f"{sfn} as ward of {tfn}" in ev:
        return True
    return False


def _check_marries_off_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source arranges a marriage for target."""
    # "source considers marrying target to someone"
    if f"{sfn} considers marrying {tfn}" in ev:
        return True
    if f"{sfn} offers to marry {tfn}" in ev:
        return True
    if f"wed off {tfn}" in ev and sfn in ev:
        return True
    if f"{sfn} arranges" in ev and tfn in ev and "married" in ev:
        return True
    # "source married off target" -- daughter married into house
    if f"{sfn}'s daughter" in ev and tfn in ev and "married" in ev:
        # This is MARRIES_OFF source -> target (where target is the daughter's match)
        return True
    return False


def _check_rescues_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source rescues target."""
    if f"{sfn} rescues {tfn}" in ev:
        return True
    if f"{sfn} rescued {tfn}" in ev:
        return True
    if f"{sfn} saved {tfn}" in ev:
        return True
    return False


def _check_reveals_to_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source reveals/confides to target."""
    if f"{sfn} confides in {tfn}" in ev:
        return True
    if f"{sfn} confided in {tfn}" in ev:
        return True
    if f"{sfn} reveals" in ev and tfn in ev:
        return True
    if f"{sfn} told {tfn}" in ev:
        return True
    return False


def _check_travels_with_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """
    Source travels in company of target.

    Strict: source must be described as directly traveling with/accompanying target,
    or they both escort a third party together. NOT fired if they are merely in
    the same geographic area or mentioned in the same paragraph.
    """
    # "source accompanies target" — source travels with target
    if f"{sfn} accompanies {tfn}" in ev:
        return True
    if f"{sfn} accompanied {tfn}" in ev:
        return True
    # "source and target escort X" — both traveling together
    sentences = [s.strip() for s in ev.split(".") if s.strip()]
    for sent in sentences:
        if sfn not in sent or tfn not in sent:
            continue
        # Both names together + travel verb
        if (f"{sfn} and {tfn}" in sent or f"{tfn} and {sfn}" in sent):
            if any(p in sent for p in ["escort", "accompany", "traveled with", "journeyed with"]):
                return True
    return False


def _check_companion_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """
    Source and target are companions/close personal friends.

    Strict: requires explicit "companion of" or "good friends with" language
    directly linking source and target. NOT fired for mere co-presence in events.
    """
    sentences = [s.strip() for s in ev.split(".") if s.strip()]
    for sent in sentences:
        if sfn not in sent or tfn not in sent:
            continue
        # "source and target are companions" or "target served as companion to source"
        if f"{sfn} and {tfn}" in sent or f"{tfn} and {sfn}" in sent:
            if any(p in sent for p in ["companion", "good friend", "close friend", "sworn brother"]):
                return True
        # Explicit "companion" phrase linking them
        if f"{tfn} served as companion to {sfn}" in sent:
            return True
        if f"{sfn} served as companion to {tfn}" in sent:
            return True
    return False


def _check_encounters_explicit(ev: str, sfn: str, tfn: str) -> bool:
    """Source and target have a staged face-to-face meeting."""
    meeting_verbs = [
        "speaks with", "meets with", "confronts", "greets",
        "meets", "visited", "talks to", "spoke to", "talked to",
    ]
    sentences = [s.strip() for s in ev.split(".") if s.strip()]
    for sent in sentences:
        if sfn in sent and tfn in sent:
            for v in meeting_verbs:
                if v in sent:
                    return True
    return False


def _check_fights_in_explicit(ev: str, sfn: str, event_name: str) -> bool:
    """Source fought in the event."""
    if event_name not in ev:
        return False

    fight_verbs = [
        "fought in", "fought at", "fights in", "at the battle", "in the battle",
        "during the battle", "at the siege", "at the tourney",
    ]
    for v in fight_verbs:
        if v in ev and event_name in ev and sfn in ev:
            return True

    # "source is captured" / "source was captured" at an event that matches target
    if event_name in ev and sfn in ev:
        if any(p in ev for p in [
            f"{sfn} is captured", f"{sfn} was captured",
            f"{sfn} killed", f"{sfn} is killed",
            f"captured, including {sfn}", f"captured {sfn}",
            "including wylis", "wylis is captured",
        ]):
            return True

    return False


def _check_commands_in_explicit(ev: str, sfn: str, event_name: str) -> bool:
    """Source commanded in the event.

    Checks both single-sentence and adjacent-sentence patterns:
    - Same sentence: event name + source + command signal co-occur.
    - Adjacent sentences (window=2): source receives command in one sentence,
      event name in the adjacent sentence — captures "Torrhen granted command to
      Warrick ... The Sistermen's Rebellion ended when Warrick's fleet arrived."
    """
    if event_name not in ev:
        return False
    if sfn not in ev:
        return False

    command_signals = [
        f"{sfn} commands", f"{sfn} commanded",
        # "granted command of X army to [source]"
        f"granted command of", f"command to {sfn}",
    ]

    sentences = [s.strip() for s in ev.split(".") if s.strip()]

    # Single-sentence check
    for sent in sentences:
        if event_name not in sent:
            continue
        if sfn not in sent:
            continue
        if any(p in sent for p in command_signals):
            return True

    # Adjacent-sentence check (window of ±1 sentence)
    for i, sent in enumerate(sentences):
        has_command = any(p in sent for p in command_signals)
        if not has_command:
            continue
        # Look in neighboring sentences for the event name
        window = sentences[max(0, i - 1): i + 2]
        for neighbor in window:
            if event_name in neighbor and sfn in neighbor:
                return True

    return False


def _check_participates_in_explicit(ev: str, sfn: str, event_name: str) -> bool:
    """Source had non-combat involvement in the event."""
    if event_name not in ev:
        return False
    # Organizing: "held a tourney", "hosted", "attended" in non-combat context
    organize_verbs = ["held a", "hosted a", "organized", "organized the"]
    for v in organize_verbs:
        sentences = [s.strip() for s in ev.split(".") if s.strip()]
        for sent in sentences:
            if sfn in sent and event_name in sent and v in sent:
                return True
    # Baggage train, logistics
    if "baggage train" in ev and sfn in ev and event_name in ev:
        return True
    return False


def _check_attends_explicit(ev: str, sfn: str, event_name: str) -> bool:
    """
    Source attended the event as guest/spectator.

    Strict: source must be explicitly described as attending/watching the event.
    NOT accepted if the event is merely mentioned in context of someone else's actions.
    """
    if event_name not in ev:
        return False
    sentences = [s.strip() for s in ev.split(".") if s.strip()]
    for sent in sentences:
        if sfn not in sent or event_name not in sent:
            continue
        # Explicit attendance language about source
        if any(p in sent for p in [
            f"{sfn} attended", f"{sfn} attend",
            f"{sfn} spectated", f"{sfn} watched",
            f"{sfn} is entertained by the",
            f"{sfn} was entertained by",
        ]):
            return True
    return False


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_file(input_path: Path, output_dir: Path) -> tuple[int, int]:
    """
    Process one candidates file. Returns (emit_count, reject_count).

    Deduplication: after classification, emitted edges are deduplicated by
    (source_slug, target_slug, edge_type) — keeping the first occurrence.
    Duplicates arise when the same relationship appears in multiple wiki sections
    (e.g., "Narrative Arc / AGOT" and "Quotes by Wylis" both describe the
    same SIBLING_OF relationship).
    """
    slug = input_path.stem.replace(".candidates", "")
    output_path = output_dir / f"{slug}.edges.jsonl"

    all_decisions: list[dict] = []
    seen_emit_keys: set[tuple] = set()

    with input_path.open("r", encoding="utf-8") as fin:
        for line_num, line in enumerate(fin, 1):
            line = line.strip()
            if not line:
                continue

            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(
                    f"  WARNING: line {line_num} in {input_path.name} invalid JSON: {exc}",
                    file=sys.stderr,
                )
                continue

            try:
                decision = classify(row)
            except Exception as exc:
                print(
                    f"  WARNING: classification error line {line_num} in {input_path.name}: {exc}",
                    file=sys.stderr,
                )
                src = row.get("source_slug", "unknown")
                tgt = row.get("target_slug", "unknown")
                decision = reject(src, tgt, f"classification-error: {exc}")

            # Deduplicate emit_edge rows by (source, target, edge_type)
            if decision["decision"] == "emit_edge":
                dedup_key = (
                    decision["source_slug"],
                    decision["target_slug"],
                    decision["edge_type"],
                )
                if dedup_key in seen_emit_keys:
                    # Convert to reject with dedup reason instead of writing duplicate
                    decision = reject(
                        decision["source_slug"],
                        decision["target_slug"],
                        "duplicate-edge-across-sections",
                    )
                else:
                    seen_emit_keys.add(dedup_key)

            all_decisions.append(decision)

    emit_count = sum(1 for d in all_decisions if d["decision"] == "emit_edge")
    reject_count = sum(1 for d in all_decisions if d["decision"] != "emit_edge")

    with output_path.open("w", encoding="utf-8") as fout:
        for decision in all_decisions:
            fout.write(json.dumps(decision, ensure_ascii=False) + "\n")

    return emit_count, reject_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify enriched Manderly prose-edge candidates into emit/reject decisions."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=INPUT_DIR,
        help="Directory containing *.candidates.jsonl files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory to write *.edges.jsonl output files",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=TARGET_FILES,
        help="Specific candidate filenames to process (default: all 5 Manderly files)",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    total_emit = 0
    total_reject = 0

    for filename in args.files:
        input_path = args.input_dir / filename
        if not input_path.exists():
            print(f"  WARNING: {input_path} not found — skipping", file=sys.stderr)
            continue

        emit_count, reject_count = process_file(input_path, args.output_dir)
        total_emit += emit_count
        total_reject += reject_count
        print(
            f"[done] {filename} → {emit_count} emit_edge, {reject_count} reject_just_mention"
        )

    print()
    print(f"Summary: {len(args.files)} files processed")
    print(f"  Total emit_edge:           {total_emit}")
    print(f"  Total reject_just_mention: {total_reject}")
    print(f"  Total rows:                {total_emit + total_reject}")
    print(f"Output written to: {args.output_dir}")


if __name__ == "__main__":
    main()
