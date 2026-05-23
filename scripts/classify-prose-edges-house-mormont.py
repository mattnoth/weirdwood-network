#!/usr/bin/env python3
"""
classify-prose-edges-house-mormont.py

Deterministic rule-based edge classifier for House Mormont characters.

Reads enriched prose-edge-candidate files for:
  dacey-mormont, jeor-mormont, jorah-mormont, jorelle-mormont,
  lady-mormont-wife-of-alaric-stark

Classifies each candidate into one of:
  - emit_edge              (typed edge with evidence)
  - reject_just_mention    (co-mention only, no typed relationship)
  - escalate_cross_identity (candidate requires identity resolution)

Output: one JSONL file per character in prose-edges-haiku/.

Usage:
    python3 scripts/classify-prose-edges-house-mormont.py
    python3 scripts/classify-prose-edges-house-mormont.py --dry-run
    python3 scripts/classify-prose-edges-house-mormont.py --character jorah-mormont
"""

import argparse
import json
import sys
from pathlib import Path

BUCKET_DIR = Path(
    "/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets"
    "/characters-house-mormont"
)
INPUT_DIR = BUCKET_DIR / "prose-edge-candidates-enriched"
OUTPUT_DIR = BUCKET_DIR / "prose-edges-haiku"

# Files to process (5 named files as specified)
CHARACTERS = [
    "dacey-mormont",
    "jeor-mormont",
    "jorah-mormont",
    "jorelle-mormont",
    "lady-mormont-wife-of-alaric-stark",
]


# ---------------------------------------------------------------------------
# Decision row constructors
# ---------------------------------------------------------------------------

def emit_edge(source_slug, target_slug, candidate_kind, edge_type,
              snippet, section, confidence_tier=1, qualifier=None):
    """Build an emit_edge decision row."""
    row = {
        "decision": "emit_edge",
        "candidate_kind": candidate_kind,
        "evidence_kind": "wiki-entity",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "edge_type": edge_type,
    }
    if qualifier is not None:
        row["qualifier"] = qualifier
    row["evidence_snippet"] = snippet[:200]
    row["evidence_section"] = section
    row["confidence_tier"] = confidence_tier
    return row


def reject(source_slug, target_slug, candidate_kind, reason):
    """Build a reject_just_mention decision row."""
    return {
        "decision": "reject_just_mention",
        "candidate_kind": candidate_kind,
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": reason,
    }


def escalate_cross_identity(source_slug, target_slug, candidate_kind, reason):
    """Build an escalate_cross_identity decision row."""
    return {
        "decision": "escalate_cross_identity",
        "candidate_kind": candidate_kind,
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# Snippet extraction helper
# ---------------------------------------------------------------------------

def extract_snippet(para, keyword=None, max_len=200):
    """Extract a representative snippet from the evidence paragraph.

    If keyword is provided, center the snippet around the first occurrence.
    Falls back to the first max_len characters.
    """
    if not para:
        return ""
    para = para.strip()
    if keyword:
        idx = para.lower().find(keyword.lower())
        if idx != -1:
            start = max(0, idx - 40)
            end = min(len(para), start + max_len)
            return para[start:end]
    return para[:max_len]


# ---------------------------------------------------------------------------
# Per-character classification functions
# ---------------------------------------------------------------------------

def classify_dacey(c):
    """Classify a single candidate for dacey-mormont."""
    slug = c["target_slug"]
    section = c.get("source_section", "")
    para = c.get("evidence_paragraph", "")
    kind = c.get("candidate_kind", "source_target")
    source = "dacey-mormont"

    # =========================================================
    # Narrative Arc / A Dance with Dragons
    # =========================================================
    if "A Dance with Dragons" in section:
        if slug == "alysane-mormont":
            # "Alysane Mormont speaks of her sister's murder" — Dacey is the sister
            return emit_edge(source, slug, kind, "SIBLING_OF",
                             extract_snippet(para, "sister"),
                             section, confidence_tier=1, qualifier="full")
        if slug == "asha-greyjoy":
            # Alysane tells Asha about Dacey's murder — co-mention, not a direct
            # Dacey→Asha relationship
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")

    # =========================================================
    # Narrative Arc / A Game of Thrones
    # =========================================================
    if "A Game of Thrones" in section:
        if slug == "battle-in-the-whispering-wood":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "battle"),
                             section, confidence_tier=1)
        if slug == "house-lannister":
            return emit_edge(source, slug, kind, "OPPOSES",
                             extract_snippet(para, "Lannisters"),
                             section, confidence_tier=2)
        if slug == "robb-stark":
            # Co-presence as sworn guard — not a kinship or deep relational edge;
            # the SERVES edge belongs to the infobox extraction layer
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")

    # =========================================================
    # Narrative Arc / A Storm of Swords
    # =========================================================
    if "A Storm of Swords" in section:
        if slug == "benfrey-frey":
            # Evidence: Dacey is attacked and killed at the Red Wedding;
            # Benfrey Frey is the killer (who smashed a flagon on her arm)
            return emit_edge(source, slug, kind, "ATTACKS",
                             extract_snippet(para, "flagon"),
                             section, confidence_tier=1)
        if slug == "catelyn-stark":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "edmure-tully":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "edwyn-frey":
            # Edwyn refuses to dance — early warning sign of the massacre,
            # but this is a social slight, not a combat attack
            return emit_edge(source, slug, kind, "ATTACKS",
                             extract_snippet(para, "Edwyn"),
                             section, confidence_tier=1)
        if slug == "house-frey":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "ironborn":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "lynesse-hightower":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "moat-cailin":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Moat Cailin"),
                             section, confidence_tier=1)
        if slug == "mormont-keep":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Mormont"),
                             section, confidence_tier=1)
        if slug == "red-wedding":
            # Dacey attends the Red Wedding as a guard/guest
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "wedding feast"),
                             section, confidence_tier=1)
        if slug == "roslin-frey":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "ryman-frey":
            # Ryman Frey is the one who kills Dacey at the Red Wedding
            return emit_edge(source, slug, kind, "KILLED_BY",
                             extract_snippet(para, "killed"),
                             section, confidence_tier=1)
        if slug == "wine":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")

    # =========================================================
    # Quotes section
    # =========================================================
    if "Quotes" in section:
        if slug == "catelyn-stark":
            # Direct quote by Dacey to Catelyn — real exchange
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "robb-stark":
            # Robb mentioned in quote ("Young Wolf") — co-mention
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")

    return reject(source, slug, kind, "no-fitting-type-vocab-locked")


def classify_jeor(c):
    """Classify a single candidate for jeor-mormont."""
    slug = c["target_slug"]
    section = c.get("source_section", "")
    para = c.get("evidence_paragraph", "")
    kind = c.get("candidate_kind", "source_target")
    source = "jeor-mormont"

    # =========================================================
    # Appearances & Description
    # =========================================================
    if "Appearances & Description" in section:
        if slug == "bear":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "beer":
            return reject(source, slug, kind, "incidental personal-habit detail — no typed edge")
        if slug == "castle-black":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Castle Black"),
                             section, confidence_tier=1)
        if slug == "denys-mallister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "gold":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "lemon":
            return reject(source, slug, kind, "incidental personal-habit detail — no typed edge")
        if slug == "longclaw":
            return emit_edge(source, slug, kind, "WIELDS",
                             extract_snippet(para, "Longclaw"),
                             section, confidence_tier=1)
        if slug == "lord-commanders-tower":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "tower"),
                             section, confidence_tier=1)
        if slug == "mormonts-raven":
            return emit_edge(source, slug, kind, "OWNS",
                             extract_snippet(para, "raven"),
                             section, confidence_tier=1)
        if slug == "samwell-tarly":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "steel":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "valyrian-steel":
            # valyrian-steel appears as the type of Longclaw — material context
            return reject(source, slug, kind,
                          "valyrian-steel is material of Longclaw; WIELDS edge targets "
                          "the artifact (longclaw), not the material")
        if slug == "wine":
            return reject(source, slug, kind, "incidental personal-habit detail — no typed edge")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Origins
    # =========================================================
    if section == "## Origins" or section.startswith("## Origins"):
        if slug == "benjen-stark":
            return emit_edge(source, slug, kind, "ADVISES",
                             extract_snippet(para, "advice"),
                             section, confidence_tier=1)
        if slug == "beyond-the-wall":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "beyond the Wall"),
                             section, confidence_tier=2)
        if slug == "cotter-pyke":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "denys-mallister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "eddard-stark":
            # Eddard is mentioned as the lord from whom Jorah fled, giving Jeor
            # back Longclaw — not Jeor's sibling; reject as context mention
            return reject(source, slug, kind,
                          "Eddard Stark is context for Jorah's exile, not Jeor's sibling — "
                          "temporal-cooccurrence-not-relational")
        if slug == "first-ranger":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "free-cities":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "house-mallister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "ironborn":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "longclaw":
            return emit_edge(source, slug, kind, "WIELDS",
                             extract_snippet(para, "Longclaw"),
                             section, confidence_tier=1)
        if slug == "lord-commander-qorgyle":
            return emit_edge(source, slug, kind, "SUCCEEDS",
                             extract_snippet(para, "Lord Commander"),
                             section, confidence_tier=1)
        if slug == "maege-mormont":
            return emit_edge(source, slug, kind, "SIBLING_OF",
                             extract_snippet(para, "sister"),
                             section, confidence_tier=1, qualifier="full")
        if slug == "roberts-rebellion":
            return reject(source, slug, kind,
                          "Robert's Rebellion mentioned as prior context — "
                          "Jeor's NW entry predates it; temporal-cooccurrence-not-relational")
        if slug == "valyrian-steel":
            return reject(source, slug, kind,
                          "valyrian-steel is material of Longclaw — "
                          "WIELDS edge targets artifact; no-fitting-type-vocab-locked")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Game of Thrones
    # =========================================================
    if "A Game of Thrones" in section:
        if slug == "aemon-targaryen-son-of-maekar-i":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "alliser-thorne":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "arrest-of-eddard-stark":
            return reject(source, slug, kind,
                          "arrest-of-eddard-stark is background political context — "
                          "Jeor not a participant; temporal-cooccurrence-not-relational")
        if slug == "benjen-stark":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Benjen"),
                             section, confidence_tier=1)
        if slug == "beyond-the-wall":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "beyond the Wall"),
                             section, confidence_tier=2)
        if slug == "castle-black":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Castle Black"),
                             section, confidence_tier=1)
        if slug == "direwolf":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "eddard-stark":
            return reject(source, slug, kind,
                          "Eddard Stark mentioned as the lord from whom Jorah fled — "
                          "Jeor regained Longclaw after Jorah's flight; "
                          "temporal-cooccurrence-not-relational")
        if slug == "first-ranger":
            return reject(source, slug, kind, "title context only — no-fitting-type-vocab-locked")
        if slug == "ghost":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "house-lannister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "jafer-flowers":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "jaime-lannister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "jaremy-rykker":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "joffrey-baratheon":
            return reject(source, slug, kind,
                          "Joffrey mentioned as the king whose support Jeor sought — "
                          "political context; temporal-cooccurrence-not-relational")
        if slug == "jon-snow":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Jon"),
                             section, confidence_tier=1)
        if slug == "kings-landing":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "King's Landing"),
                             section, confidence_tier=2)
        if slug == "kings-tower":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "King's Tower"),
                             section, confidence_tier=1)
        if slug == "knight":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "longclaw":
            return emit_edge(source, slug, kind, "WIELDS",
                             extract_snippet(para, "Longclaw"),
                             section, confidence_tier=1)
        if slug == "lord-commanders-tower":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "tower"),
                             section, confidence_tier=1)
        if slug == "mance-rayder":
            return reject(source, slug, kind,
                          "Mance Rayder mentioned in Jon's desertion context — "
                          "temporal-cooccurrence-not-relational")
        if slug == "others":
            return reject(source, slug, kind,
                          "Others mentioned as external threat — "
                          "no direct Jeor→Others relationship in this section")
        if slug == "othor":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "pycelle":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "rangers":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "red-keep":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Red Keep"),
                             section, confidence_tier=2)
        if slug == "robb-stark":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "robert-i-baratheon":
            return reject(source, slug, kind,
                          "Robert mentioned as king Tyrion informed — "
                          "political context; temporal-cooccurrence-not-relational")
        if slug == "samwell-tarly":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Sam"),
                             section, confidence_tier=1)
        if slug == "steward":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "tyrion-lannister":
            return emit_edge(source, slug, kind, "ENCOUNTERS",
                             extract_snippet(para, "host"),
                             section, confidence_tier=1)
        if slug == "tywin-lannister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "valyrian-steel":
            return reject(source, slug, kind,
                          "valyrian-steel is material of Longclaw — "
                          "WIELDS edge targets artifact; no-fitting-type-vocab-locked")
        if slug == "wall":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Wall"),
                             section, confidence_tier=1)
        if slug == "waymar-royce":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Waymar"),
                             section, confidence_tier=1)
        if slug == "weirwood":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Clash of Kings
    # =========================================================
    if "A Clash of Kings" in section:
        if slug == "aemon-targaryen-son-of-maekar-i":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "arnell":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "envoy"),
                             section, confidence_tier=1)
        if slug == "castle-black":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Castle Black"),
                             section, confidence_tier=1)
        if slug == "craster":
            # Jeor visits Craster's Keep; infobox row — reject infobox-structured evidence
            if para.startswith("-"):
                return reject(source, slug, kind,
                              "infobox-structured evidence row — relationship already in "
                              "skeleton; temporal-cooccurrence-not-relational")
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "crasters-sons":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dragonglass":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "fist-of-the-first-men":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Fist"),
                             section, confidence_tier=1)
        if slug == "frostfangs":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Frostfangs"),
                             section, confidence_tier=1)
        if slug == "giants-stair":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "great-ranging":
            return emit_edge(source, slug, kind, "COMMANDS_IN",
                             extract_snippet(para, "great ranging"),
                             section, confidence_tier=1)
        if slug == "house-targaryen":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "iron-throne":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "king-in-the-north":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "lord-of-bones":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "milkwater":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "others":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "qhorin-halfhand":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Qhorin"),
                             section, confidence_tier=1)
        if slug == "rangers":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "renly-baratheon":
            return reject(source, slug, kind,
                          "Renly mentioned as one of the claimants Jeor sent an envoy to — "
                          "political outreach; temporal-cooccurrence-not-relational")
        if slug == "samwell-tarly":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Sam"),
                             section, confidence_tier=1)
        if slug == "shadow-tower":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "skirling-pass":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "wall":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Wall"),
                             section, confidence_tier=1)
        if slug == "war-of-the-five-kings":
            return reject(source, slug, kind,
                          "War of the Five Kings as political background context — "
                          "temporal-cooccurrence-not-relational")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Storm of Swords
    # =========================================================
    if "A Storm of Swords" in section:
        if slug == "bannen":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "battle-beneath-the-wall":
            return reject(source, slug, kind,
                          "battle-beneath-the-wall occurs after Jeor's death at Craster's Keep — "
                          "temporal-cooccurrence-not-relational")
        if slug == "bowen-marsh":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "castellan"),
                             section, confidence_tier=1)
        if slug == "castle-black":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Castle Black"),
                             section, confidence_tier=1)
        if slug == "chett":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "crasters-wives":
            # At the mutiny, Jeor is killed — crasters-wives are co-present
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "denys-mallister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dirk":
            # Dirk kills Craster, then Jeor is stabbed — Dirk is a mutineer
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "fight-at-the-fist":
            return emit_edge(source, slug, kind, "COMMANDS_IN",
                             extract_snippet(para, "Fist"),
                             section, confidence_tier=1)
        if slug == "fist-of-the-first-men":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Fist"),
                             section, confidence_tier=1)
        if slug == "garth-of-greenaway":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "gilly":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "jon-snow":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Jon"),
                             section, confidence_tier=1)
        if slug == "kings-tower":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "King's Tower"),
                             section, confidence_tier=1)
        if slug == "monster":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "mormonts-raven":
            return emit_edge(source, slug, kind, "OWNS",
                             extract_snippet(para, "raven"),
                             section, confidence_tier=1)
        if slug == "mutiny-at-crasters-keep":
            # Jeor is present and dies at the mutiny
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "mutiny"),
                             section, confidence_tier=1)
        if slug == "ollo-lophand":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "raven":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "samwell-tarly":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Sam"),
                             section, confidence_tier=1)
        if slug == "small-paul":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "softfoot":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "stannis-baratheon":
            return reject(source, slug, kind,
                          "Stannis arrives after Jeor's death — "
                          "temporal-cooccurrence-not-relational")
        if slug == "wights":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Quotes sections
    # =========================================================
    if "Quotes" in section:
        if slug == "bear":
            if para.startswith("-"):
                return reject(source, slug, kind,
                              "infobox-structured evidence row — no-fitting-type-vocab-locked")
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "bowen-marsh":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "cotter-pyke":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "denys-mallister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "donal-noye":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "jon-snow":
            return emit_edge(source, slug, kind, "COMMANDS",
                             extract_snippet(para, "Jon"),
                             section, confidence_tier=1)
        if slug == "mormonts-raven":
            return emit_edge(source, slug, kind, "OWNS",
                             extract_snippet(para, "raven"),
                             section, confidence_tier=1)
        if slug == "othell-yarwyck":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "robert-i-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "samwell-tarly":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "squire":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "stannis-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "tyrion-lannister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "wall":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "wine":
            return reject(source, slug, kind,
                          "incidental food/drink mention — no typed edge")
        # Quotes by Jeor — handle specific addresses
        if slug == "aemon-targaryen-son-of-maekar-i":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dragonglass":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "eddard-stark":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "fight-at-the-fist":
            return reject(source, slug, kind,
                          "duplicate of narrative-arc COMMANDS_IN edge already captured; "
                          "temporal-cooccurrence-not-relational")
        if slug == "free-folk":
            return reject(source, slug, kind,
                          "free-folk mentioned as the threat Jeor warns about — "
                          "no direct Jeor→free-folk typed edge; "
                          "temporal-cooccurrence-not-relational")
        if slug == "iron-throne":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "kingsroad":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "known-world":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "mutiny-at-crasters-keep":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "mutiny"),
                             section, confidence_tier=1)
        if slug == "others":
            return reject(source, slug, kind,
                          "Others mentioned as the threat — "
                          "no direct Jeor→Others relationship; "
                          "temporal-cooccurrence-not-relational")
        return reject(source, slug, kind, "temporal-cooccurrence-not-relational")

    return reject(source, slug, kind, "no-fitting-type-vocab-locked")


def classify_jorah(c):
    """Classify a single candidate for jorah-mormont."""
    slug = c["target_slug"]
    section = c.get("source_section", "")
    para = c.get("evidence_paragraph", "")
    kind = c.get("candidate_kind", "source_target")
    source = "jorah-mormont"

    # =========================================================
    # Appearances & Description
    # =========================================================
    if "Appearances & Description" in section:
        if slug == "barristan-selmy":
            # Described as shorter/more muscular than Barristan — comparison, not relationship
            return reject(source, slug, kind, "description comparison — no typed edge")
        if slug == "bear":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "daenerys-targaryen":
            # Daenerys considers Jorah not handsome — perception context
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dothraki":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "drogo":
            return reject(source, slug, kind, "equipment context — no typed edge")
        if slug == "eddard-stark":
            # "Jorah hates Lord Eddard Stark" — direct HATES edge
            return emit_edge(source, slug, kind, "HATES",
                             extract_snippet(para, "hates"),
                             section, confidence_tier=1)
        if slug == "essos":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "longsword":
            return emit_edge(source, slug, kind, "WIELDS",
                             extract_snippet(para, "longsword"),
                             section, confidence_tier=1)
        if slug == "moqorro":
            return reject(source, slug, kind, "description comparison — no typed edge")
        if slug == "steel":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Game of Thrones
    # =========================================================
    if "A Game of Thrones" in section:
        # Infobox-structured evidence — skip
        if para.startswith("-"):
            return reject(source, slug, kind,
                          "infobox-structured evidence row — already in skeleton; "
                          "temporal-cooccurrence-not-relational")
        if slug == "arakh":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "asshai":
            return reject(source, slug, kind, "travel destination mentioned — temporal context")
        if slug == "bloodrider":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "common-tongue":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "daenerys-targaryen":
            return emit_edge(source, slug, kind, "SERVES",
                             extract_snippet(para, "service"),
                             section, confidence_tier=1)
        if slug == "dosh-khaleen":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dothraki":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dragon":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "dragon-egg":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "drogo":
            return emit_edge(source, slug, kind, "SERVES",
                             extract_snippet(para, "khal"),
                             section, confidence_tier=1)
        if slug == "drogos-manse":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "manse"),
                             section, confidence_tier=1)
        if slug == "drogos-stallion":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "illyrio-mopatis":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "jade-sea":
            return reject(source, slug, kind, "travel destination — temporal context")
        if slug == "khal":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "kings-landing":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "King's Landing"),
                             section, confidence_tier=1)
        if slug == "lhazar":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Lhazar"),
                             section, confidence_tier=1)
        if slug == "lhazareen":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "lord":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "maegi":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "master-of-whisperers":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "mirri-maz-duur":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "ogo":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "pentos":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Pentos"),
                             section, confidence_tier=1)
        if slug == "qarth":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Qarth"),
                             section, confidence_tier=1)
        if slug == "qotho":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "rakharo":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "rhaego":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "robert-i-baratheon":
            # Jorah was secretly spying for Robert — SPIES_ON is inbound from Jorah
            return emit_edge(source, slug, kind, "INFORMS",
                             extract_snippet(para, "employment"),
                             section, confidence_tier=1)
        if slug == "seven-kingdoms":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Seven Kingdoms"),
                             section, confidence_tier=1)
        if slug == "silver-mare":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "stallion-heart":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "vaes-dothrak":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Vaes Dothrak"),
                             section, confidence_tier=1)
        if slug == "valyrian-steel":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "varys":
            return emit_edge(source, slug, kind, "INFORMS",
                             extract_snippet(para, "Varys"),
                             section, confidence_tier=1)
        if slug == "viserys-targaryen":
            return emit_edge(source, slug, kind, "SERVES",
                             extract_snippet(para, "service"),
                             section, confidence_tier=1)
        if slug == "wedding-of-drogo-and-daenerys-targaryen":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "feast"),
                             section, confidence_tier=1)
        if slug == "westeros":
            return reject(source, slug, kind,
                          "Westeros as Jorah's hoped-for destination — "
                          "motivational context; temporal-cooccurrence-not-relational")
        if slug == "wine":
            return reject(source, slug, kind, "incidental mention — no typed edge")
        if slug == "yi-ti":
            return reject(source, slug, kind, "travel destination — temporal context")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Clash of Kings
    # =========================================================
    if "A Clash of Kings" in section:
        if para.startswith("-"):
            return reject(source, slug, kind,
                          "infobox-structured evidence row — already in skeleton; "
                          "temporal-cooccurrence-not-relational")
        if slug == "asshai":
            return reject(source, slug, kind, "travel destination — temporal context")
        if slug == "barristan-selmy":
            return reject(source, slug, kind, "description comparison — temporal-cooccurrence-not-relational")
        if slug == "belwas":
            return emit_edge(source, slug, kind, "ENCOUNTERS",
                             extract_snippet(para, "met"),
                             section, confidence_tier=1)
        if slug == "cinnamon-wind":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "drogon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "further-east":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "great-houses":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "house-glover":
            # house-glover appears only in the infobox-structured row
            return reject(source, slug, kind,
                          "infobox-structured evidence row — already in skeleton; "
                          "temporal-cooccurrence-not-relational")
        if slug == "house-of-the-undying":
            return emit_edge(source, slug, kind, "ENCOUNTERS",
                             extract_snippet(para, "meeting"),
                             section, confidence_tier=1)
        if slug == "illyrio-mopatis":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug in ("iron-throne", "iron-throne"):
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "joffrey-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "mirri-maz-duur":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "pentos":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Pentos"),
                             section, confidence_tier=1)
        if slug == "port-of-qarth":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Qarth"),
                             section, confidence_tier=1)
        if slug == "pureborn":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "pyat-pree":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "qarth":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Qarth"),
                             section, confidence_tier=1)
        if slug == "quaithe":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "quhuru-mo":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "renly-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "rhaegal":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "robert-i-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "seven-kingdoms":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Seven Kingdoms"),
                             section, confidence_tier=1)
        if slug == "stannis-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "tourney-at-lannisport":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "tourney"),
                             section, confidence_tier=1)
        if slug == "undying-ones":
            return emit_edge(source, slug, kind, "ENCOUNTERS",
                             extract_snippet(para, "meeting"),
                             section, confidence_tier=1)
        if slug == "vaes-tolorro":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Vaes Tolorro"),
                             section, confidence_tier=1)
        if slug == "viserion":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "xaro-xhoan-daxos":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Storm of Swords
    # =========================================================
    if "A Storm of Swords" in section:
        if slug == "aegons-conquest":
            return reject(source, slug, kind, "historical context mention — temporal-cooccurrence-not-relational")
        if slug == "astapor":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Astapor"),
                             section, confidence_tier=1)
        if slug == "barristan-selmy":
            return emit_edge(source, slug, kind, "DISTRUSTS",
                             extract_snippet(para, "distrust"),
                             section, confidence_tier=1)
        if slug == "battle-near-yunkai":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "Yunkai"),
                             section, confidence_tier=1)
        if slug == "daario-naharis":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "dragon":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "drogo":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "fall-of-astapor":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "Astapor"),
                             section, confidence_tier=1)
        if slug == "good-masters":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "grey-worm":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "illyrio-mopatis":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "lord-commander-of-the-kingsguard":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "lord-commander-of-the-nights-watch":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "meereen":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Meereen"),
                             section, confidence_tier=1)
        if slug == "mero":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "mutiny-at-crasters-keep":
            # Jeor's dying wish mentioned; Jorah not present at the mutiny
            return reject(source, slug, kind,
                          "mutiny is context for Jeor's dying message — "
                          "Jorah not present; temporal-cooccurrence-not-relational")
        if slug == "nights-watch":
            return reject(source, slug, kind,
                          "Night's Watch mentioned as institution Jorah's father joined — "
                          "Jeor's membership; temporal-cooccurrence-not-relational")
        if slug == "pentos":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Pentos"),
                             section, confidence_tier=1)
        if slug == "plaza-of-pride":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Plaza"),
                             section, confidence_tier=1)
        if slug == "rhaegar-targaryen":
            return reject(source, slug, kind,
                          "Rhaegar mentioned in historical context Arstan discusses — "
                          "temporal-cooccurrence-not-relational")
        if slug == "robert-i-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "sack-of-kings-landing":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "Sack"),
                             section, confidence_tier=1)
        if slug == "samwell-tarly":
            return reject(source, slug, kind,
                          "Samwell mentioned as messenger of Jeor's dying wish — "
                          "temporal-cooccurrence-not-relational")
        if slug == "siege-of-meereen":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "siege"),
                             section, confidence_tier=1)
        if slug == "slavers-bay":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Bay"),
                             section, confidence_tier=1)
        if slug == "stormcrows":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "three-thousand-of-qohor":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "tourney-at-lannisport":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "tourney"),
                             section, confidence_tier=1)
        if slug == "unsullied":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "viserys-targaryen":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "wise-masters":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "yunkai":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Yunkai"),
                             section, confidence_tier=1)
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / A Dance with Dragons
    # =========================================================
    if "A Dance with Dragons" in section:
        if slug == "ben-plumm":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "benerro":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "daenerys-targaryen":
            return emit_edge(source, slug, kind, "SERVES",
                             extract_snippet(para, "Daenerys"),
                             section, confidence_tier=1)
        if slug == "daznaks-pit":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Pit"),
                             section, confidence_tier=1)
        if slug == "dothraki-sea":
            return reject(source, slug, kind, "vision context — temporal-cooccurrence-not-relational")
        if slug == "drogon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "hizdahr-zo-loraq":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "knight":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "meereen":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Meereen"),
                             section, confidence_tier=1)
        if slug == "merchants-house":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "house"),
                             section, confidence_tier=1)
        if slug == "nurse":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "oppo":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "penny":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "pentos":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Pentos"),
                             section, confidence_tier=1)
        if slug == "pretty-pig":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "qarth":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Qarth"),
                             section, confidence_tier=1)
        if slug == "red-priest":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "second-siege-of-meereen":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "siege"),
                             section, confidence_tier=2)
        if slug == "selaesori-qhoran":
            return emit_edge(source, slug, kind, "TRAVELS_WITH",
                             extract_snippet(para, "cabin"),
                             section, confidence_tier=3)
        if slug == "selhorys":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Selhorys"),
                             section, confidence_tier=1)
        if slug == "silver-haired-whore":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "the-bear-and-the-maiden-fair":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "tyrion-lannister":
            return emit_edge(source, slug, kind, "TRAVELS_WITH",
                             extract_snippet(para, "captive"),
                             section, confidence_tier=3)
        if slug == "undying-ones":
            return emit_edge(source, slug, kind, "ENCOUNTERS",
                             extract_snippet(para, "meeting"),
                             section, confidence_tier=1)
        if slug == "varys":
            return emit_edge(source, slug, kind, "INFORMS",
                             extract_snippet(para, "Varys"),
                             section, confidence_tier=1)
        if slug == "volantis":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Volantis"),
                             section, confidence_tier=1)
        if slug == "widow-of-the-waterfront":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "yezzan-zo-qaggaz":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Narrative Arc / The Winds of Winter (preview chapter)
    # =========================================================
    if "Winds of Winter" in section:
        if slug == "barristan-selmy":
            return reject(source, slug, kind, "description comparison — no typed edge")
        if slug == "ben-plumm":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "daenerys-targaryen":
            return emit_edge(source, slug, kind, "SERVES",
                             extract_snippet(para, "Daenerys"),
                             section, confidence_tier=1)
        if slug == "meereen":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Meereen"),
                             section, confidence_tier=1)
        if slug == "morghaz-zo-zherzyn":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "unsullied":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    # =========================================================
    # Quotes section (Quotes about Jorah / Quotes by Jorah)
    # =========================================================
    if "Quotes" in section:
        # Quotes about Jorah — these paragraphs repeat narrative evidence
        # already classified in narrative-arc sections, or are quotes from
        # other characters' POVs. Reject all as duplicates/co-mentions.
        if slug == "daenerys-targaryen":
            # Daenerys speaks of Jorah in quotes — co-mention
            return reject(source, slug, kind,
                          "quote-section co-mention — Daenerys's perception of Jorah; "
                          "temporal-cooccurrence-not-relational")
        if slug == "eddard-stark":
            return reject(source, slug, kind,
                          "quote-section co-mention — Eddard as context for Jorah's exile; "
                          "temporal-cooccurrence-not-relational")
        if slug == "hizdahr-zo-loraq":
            return reject(source, slug, kind,
                          "quote-section co-mention — temporal-cooccurrence-not-relational")
        if slug == "robert-i-baratheon":
            return reject(source, slug, kind,
                          "quote-section co-mention — temporal-cooccurrence-not-relational")
        if slug == "sellsword":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "tyrion-lannister":
            return reject(source, slug, kind,
                          "quote-section — Tyrion speaks about Jorah; "
                          "temporal-cooccurrence-not-relational")
        if slug == "viserys-targaryen":
            return reject(source, slug, kind,
                          "quote-section co-mention — temporal-cooccurrence-not-relational")
        if slug == "yezzan-zo-qaggaz":
            return reject(source, slug, kind,
                          "quote-section co-mention — temporal-cooccurrence-not-relational")
        if slug == "zahrina":
            return reject(source, slug, kind,
                          "Zahrina is mentioned in a quote about Jorah being broken — "
                          "no direct Jorah→Zahrina edge; temporal-cooccurrence-not-relational")
        # Quotes by Jorah
        if slug == "currency":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "qarth":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Qarth"),
                             section, confidence_tier=1)
        if slug == "qotho":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "red-waste":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "smallfolk":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "vaes-tolorro":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Vaes Tolorro"),
                             section, confidence_tier=1)
        if slug == "widow-of-the-waterfront":
            return reject(source, slug, kind,
                          "widow-of-the-waterfront mentioned in Volantis travel — "
                          "temporal-cooccurrence-not-relational")
        # Remaining quote co-mentions — narrative paragraphs already handled above
        return reject(source, slug, kind,
                      "quote-section co-mention or repeated narrative paragraph — "
                      "temporal-cooccurrence-not-relational")

    # =========================================================
    # Catch all remaining sections (Origins subsections + Quotes)
    # =========================================================
    if "Origins" in section or section.startswith("## Origins"):
        # ---- Origins / Youth ----
        if slug == "283-ac":
            return reject(source, slug, kind, "year-date node — no typed edge; temporal context")
        if slug == "battle-of-the-trident":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "Trident"),
                             section, confidence_tier=1)
        if slug == "house-glover":
            # First wife came from House Glover
            return emit_edge(source, slug, kind, "IN_LAW_OF",
                             extract_snippet(para, "House Glover"),
                             section, confidence_tier=1,
                             qualifier="wifes_house")
        if slug == "nights-watch":
            return reject(source, slug, kind,
                          "Night's Watch as institution Jeor joined — "
                          "Jeor's membership, not Jorah's; temporal-cooccurrence-not-relational")
        if slug == "roberts-rebellion":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "Robert's Rebellion"),
                             section, confidence_tier=1)
        if slug == "sack-of-kings-landing":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "Sack"),
                             section, confidence_tier=1)
        # ---- Origins / Greyjoy's Rebellion ----
        if slug == "balon-greyjoy":
            return reject(source, slug, kind,
                          "Balon Greyjoy mentioned as the rebel whose rebellion "
                          "Jorah fought in — temporal-cooccurrence-not-relational")
        if slug == "greyjoys-rebellion":
            return emit_edge(source, slug, kind, "FIGHTS_IN",
                             extract_snippet(para, "Greyjoy"),
                             section, confidence_tier=1)
        if slug == "high-septon":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "illyrio-mopatis":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "knight":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "lord-of-the-iron-islands":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "pyke":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "religion":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "robert-i-baratheon":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        # ---- Origins / Marriage to Lynesse ----
        if slug == "braavos":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Braavos"),
                             section, confidence_tier=1)
        if slug == "house-greyjoy":
            return reject(source, slug, kind,
                          "House Greyjoy mentioned as the rebels at the tourney context — "
                          "temporal-cooccurrence-not-relational")
        if slug == "house-hightower":
            return emit_edge(source, slug, kind, "IN_LAW_OF",
                             extract_snippet(para, "Hightower"),
                             section, confidence_tier=1,
                             qualifier="wifes_house")
        if slug == "jaime-lannister":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "lannisport":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Lannisport"),
                             section, confidence_tier=1)
        if slug == "leyton-hightower":
            return emit_edge(source, slug, kind, "IN_LAW_OF",
                             extract_snippet(para, "Leyton"),
                             section, confidence_tier=1,
                             qualifier="father_in_law")
        if slug == "lynesse-hightower":
            # Lynesse left Jorah and became a concubine in Lys — former marriage
            return emit_edge(source, slug, kind, "SPOUSE_OF",
                             extract_snippet(para, "married"),
                             section, confidence_tier=1, qualifier="former")
        if slug == "marriage":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "oldtown":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "queen-of-love-and-beauty":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "tourney-at-lannisport":
            return emit_edge(source, slug, kind, "ATTENDS",
                             extract_snippet(para, "tourney"),
                             section, confidence_tier=1)
        # ---- Origins / Exile ----
        if slug == "ben-plumm":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug in ("castle-black", "seven-kingdoms", "tyrosh"):
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, slug.replace("-", " ")),
                             section, confidence_tier=1)
        if slug == "dothraki":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "eddard-stark":
            return reject(source, slug, kind,
                          "Eddard Stark is context for Jorah's exile and Jeor's reclaiming "
                          "of Longclaw — temporal-cooccurrence-not-relational")
        if slug == "free-cities":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Free Cities"),
                             section, confidence_tier=1)
        if slug == "longclaw":
            return reject(source, slug, kind,
                          "Longclaw is the sword Jorah left behind; Jeor later gave it to "
                          "Jon Snow — Jorah no longer holds it in exile; "
                          "temporal-cooccurrence-not-relational")
        if slug == "lys":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Lys"),
                             section, confidence_tier=1)
        if slug == "maege-mormont":
            return reject(source, slug, kind,
                          "Maege becomes Lady of Bear Island after Jorah's exile — "
                          "no direct Jorah→Maege edge here; temporal-cooccurrence-not-relational")
        if slug == "master-of-whisperers":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "mercenary":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "red-waste":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "rhoyne":
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, "Rhoyne"),
                             section, confidence_tier=1)
        if slug == "small-council":
            return reject(source, slug, kind, "temporal-cooccurrence-not-relational")
        if slug == "tregar-ormollen":
            return reject(source, slug, kind,
                          "Tregar Ormollen is the merchant prince Lynesse left Jorah for — "
                          "no direct Jorah→Tregar edge; temporal-cooccurrence-not-relational")
        if slug in ("vaes-dothrak", "volantis"):
            return emit_edge(source, slug, kind, "LOCATED_AT",
                             extract_snippet(para, slug.replace("-", " ")),
                             section, confidence_tier=1)
        if slug == "valyrian-steel":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        if slug == "varys":
            return emit_edge(source, slug, kind, "INFORMS",
                             extract_snippet(para, "Varys"),
                             section, confidence_tier=1)
        if slug == "warden-of-the-north":
            return reject(source, slug, kind, "no-fitting-type-vocab-locked")
        return reject(source, slug, kind, "no-fitting-type-vocab-locked")

    return reject(source, slug, kind, "no-fitting-type-vocab-locked")


def classify_jorelle(c):
    """Classify a single candidate for jorelle-mormont."""
    slug = c["target_slug"]
    section = c.get("source_section", "")
    para = c.get("evidence_paragraph", "")
    kind = c.get("candidate_kind", "source_target")
    source = "jorelle-mormont"

    # Jorelle has 2 rows, both from the same evidence paragraph:
    # "Alysane Mormont tells Asha Greyjoy that her sister, affectionately called Jory,
    #  is currently with their mother, Maege Mormont."
    if slug == "alysane-mormont":
        # Jorelle's sister Alysane speaks about her — SIBLING_OF
        return emit_edge(source, slug, kind, "SIBLING_OF",
                         extract_snippet(para, "sister"),
                         section, confidence_tier=1, qualifier="full")
    if slug == "asha-greyjoy":
        # Asha hears about Jorelle — no direct Jorelle→Asha relationship
        return reject(source, slug, kind, "temporal-cooccurrence-not-relational")

    return reject(source, slug, kind, "no-fitting-type-vocab-locked")


def classify_lady_mormont(c):
    """Classify a single candidate for lady-mormont-wife-of-alaric-stark."""
    slug = c["target_slug"]
    section = c.get("source_section", "")
    para = c.get("evidence_paragraph", "")
    kind = c.get("candidate_kind", "source_target")
    source = "lady-mormont-wife-of-alaric-stark"

    if slug == "brandon-stark-father-of-walton":
        # "she married Alaric Stark, the second son of Lord Brandon Stark"
        # — Brandon Stark is her father-in-law
        return emit_edge(source, slug, kind, "IN_LAW_OF",
                         extract_snippet(para, "Brandon"),
                         section, confidence_tier=1,
                         qualifier="father_in_law")
    if slug == "walton-stark-son-of-brandon":
        # "she became the Lady of Winterfell after the death of her brother-in-law, Lord Walton Stark"
        return emit_edge(source, slug, kind, "IN_LAW_OF",
                         extract_snippet(para, "brother-in-law"),
                         section, confidence_tier=1,
                         qualifier="brother_in_law")

    return reject(source, slug, kind, "no-fitting-type-vocab-locked")


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

CLASSIFIERS = {
    "dacey-mormont": classify_dacey,
    "jeor-mormont": classify_jeor,
    "jorah-mormont": classify_jorah,
    "jorelle-mormont": classify_jorelle,
    "lady-mormont-wife-of-alaric-stark": classify_lady_mormont,
}


# Tier-1 edge types that REQUIRE a qualifier field (from reference/edge-qualifier-vocab.md)
TIER1_QUALIFIER_REQUIRED = {
    "SIBLING_OF": {"full", "half", "step", "milk", "unknown"},
    "SPOUSE_OF": {"current", "former", "annulled", "widowed", "salt_wife", "unknown"},
    "PARENT_OF": {"biological", "adopted", "claimed", "rumored", "disputed", "unknown"},
    "WARD_OF": {"formal", "informal", "hostage", "unknown"},
    "HOLDS_TITLE": {"current", "former", "claimed", "contested", "historical", "unknown"},
    "VOWS_TO": {"active", "kept", "broken", "fulfilled", "unknown"},
    "MANIPULATES": {"via_bribe", "via_flattery", "via_false_information", "via_threat", "via_seduction", "unknown"},
    "SWORN_TO": {"current", "former", "deserted", "by_marriage", "claimed", "unknown"},
}


def validate_edge_type(row, valid_edge_types):
    """Warn if the emitted edge type is not in valid_edge_types, and enforce
    Tier-1 qualifier requirements.

    Returns the row unchanged — validation is advisory, not fatal, because
    some master-vocab types (FIGHTS_IN, ATTENDS, LOCATED_AT) may be absent
    from the per-row valid_edge_types list due to pipeline version skew.
    However, missing Tier-1 qualifiers are always flagged as errors.
    """
    if row.get("decision") != "emit_edge":
        return row
    edge_type = row.get("edge_type", "")
    source = row.get("source_slug", "?")
    target = row.get("target_slug", "?")
    if valid_edge_types and edge_type not in valid_edge_types:
        print(
            f"  WARNING: {edge_type} not in valid_edge_types for "
            f"{source} -> {target}",
            file=sys.stderr,
        )
    # Enforce Tier-1 qualifier requirement
    if edge_type in TIER1_QUALIFIER_REQUIRED:
        qualifier = row.get("qualifier")
        allowed = TIER1_QUALIFIER_REQUIRED[edge_type]
        if qualifier is None:
            print(
                f"  ERROR: Tier-1 edge {edge_type} is missing required 'qualifier' field "
                f"for {source} -> {target}. Allowed: {sorted(allowed)}",
                file=sys.stderr,
            )
        elif qualifier not in allowed:
            print(
                f"  ERROR: Tier-1 edge {edge_type} has out-of-enum qualifier "
                f"'{qualifier}' for {source} -> {target}. Allowed: {sorted(allowed)}",
                file=sys.stderr,
            )
    return row


def process_character(character, dry_run=False):
    """Read, classify, and write edges for one character. Returns stats dict."""
    input_path = INPUT_DIR / f"{character}.candidates.jsonl"
    output_path = OUTPUT_DIR / f"{character}.edges.jsonl"
    classifier = CLASSIFIERS[character]

    if not input_path.exists():
        print(f"  ERROR: Input not found: {input_path}", file=sys.stderr)
        return None

    # Read candidates
    candidates = []
    with input_path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(
                    f"  WARNING: Skipping malformed line {line_num} in "
                    f"{input_path.name}: {e}",
                    file=sys.stderr,
                )

    # Classify
    decisions = []
    for c in candidates:
        valid_edge_types = c.get("valid_edge_types", [])
        row = classifier(c)
        validate_edge_type(row, valid_edge_types)
        decisions.append(row)

    # Stats
    emit_count = sum(1 for d in decisions if d["decision"] == "emit_edge")
    reject_count = sum(1 for d in decisions if d["decision"] == "reject_just_mention")
    escalate_ci = sum(1 for d in decisions if d["decision"] == "escalate_cross_identity")

    edge_types: dict[str, int] = {}
    for d in decisions:
        if d["decision"] == "emit_edge":
            et = d.get("edge_type", "unknown")
            edge_types[et] = edge_types.get(et, 0) + 1

    # Write or print
    if dry_run:
        print(f"\n--- {character} (dry-run) ---")
        for row in decisions:
            print(json.dumps(row, ensure_ascii=False))
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            for row in decisions:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {
        "character": character,
        "total": len(decisions),
        "emit_edge": emit_count,
        "reject_just_mention": reject_count,
        "escalate_cross_identity": escalate_ci,
        "edge_types": edge_types,
        "output_path": output_path,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic rule-based edge classifier for House Mormont characters. "
            "Reads enriched prose-edge-candidate files and emits typed JSONL edges."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results to stdout instead of writing to output files.",
    )
    parser.add_argument(
        "--character",
        choices=CHARACTERS,
        metavar="CHARACTER",
        help=(
            "Process only this character. "
            f"Choices: {', '.join(CHARACTERS)}"
        ),
    )
    args = parser.parse_args()

    targets = [args.character] if args.character else CHARACTERS

    print(f"Processing {len(targets)} character(s)...")
    print(f"Input dir:  {INPUT_DIR}")
    if not args.dry_run:
        print(f"Output dir: {OUTPUT_DIR}")
    print()

    all_stats = []
    for character in targets:
        print(f"  [{character}]")
        stats = process_character(character, dry_run=args.dry_run)
        if stats is None:
            continue
        all_stats.append(stats)
        if not args.dry_run:
            print(f"    Wrote {stats['total']} rows -> {stats['output_path'].name}")
        print(
            f"    emit_edge={stats['emit_edge']}  "
            f"reject={stats['reject_just_mention']}  "
            f"escalate_ci={stats['escalate_cross_identity']}"
        )
        if stats["edge_types"]:
            for et, ct in sorted(stats["edge_types"].items()):
                print(f"      {et}: {ct}")

    # Summary table
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_rows = sum(s["total"] for s in all_stats)
    total_emit = sum(s["emit_edge"] for s in all_stats)
    total_reject = sum(s["reject_just_mention"] for s in all_stats)
    total_esc = sum(s["escalate_cross_identity"] for s in all_stats)

    print(f"{'Character':<45} {'Total':>5} {'Emit':>5} {'Reject':>7} {'EscCI':>6}")
    print("-" * 60)
    for s in all_stats:
        print(
            f"{s['character']:<45} "
            f"{s['total']:>5} "
            f"{s['emit_edge']:>5} "
            f"{s['reject_just_mention']:>7} "
            f"{s['escalate_cross_identity']:>6}"
        )
    print("-" * 60)
    print(
        f"{'TOTAL':<45} "
        f"{total_rows:>5} "
        f"{total_emit:>5} "
        f"{total_reject:>7} "
        f"{total_esc:>6}"
    )
    print()

    # Combined edge-type breakdown
    combined_types: dict[str, int] = {}
    for s in all_stats:
        for et, ct in s["edge_types"].items():
            combined_types[et] = combined_types.get(et, 0) + ct
    if combined_types:
        print("Edge types emitted (all characters):")
        for et, ct in sorted(combined_types.items(), key=lambda x: -x[1]):
            print(f"  {et}: {ct}")

    if not args.dry_run and all_stats:
        print()
        print(f"Output files written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
