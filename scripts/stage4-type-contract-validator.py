#!/usr/bin/env python3
"""stage4-type-contract-validator.py — Deterministic endpoint-type contract validator.

Enforces per-edge-type endpoint contracts.  Contracts now have four dispositions:

  DROP   — the edge is genuinely wrong (wrong type, wrong direction, wrong target type).
           The row is written to --dropped and NOT to --kept.

  FLIP   — the edge is true but direction-reversed and recoverable.
           The source/target are swapped in the emitted row; the row carries
           _flipped=True and _flip_reason.  Emitted to --kept.

  FLAG   — the edge is true but malformed (e.g. target should be retargeted to
           a different node type).  The row is kept as-is with _contract_warning=True
           and _contract_reason.  Emitted to --kept.

  RETYPE — the edge is true but the edge_type is wrong and can be deterministically
           corrected.  The edge_type field is rewritten in the emitted row; the row
           carries _retyped_from (original type) and _retype_reason.
           Emitted to --kept.

  KEEP   — no contract violation detected.

The character-vs-not distinction is derived purely from the filesystem:
  graph/nodes/characters/<slug>.node.md exists => character.
Endpoint categories for richer contracts use build_slug_category_index().

Contracts enforced (conservative / high-confidence only):

  ECHOES
    Architecture (reference/architecture.md, Narrative section):
      PARALLELS = "Event/character A mirrors character B thematically"
      ECHOES    = "Weaker than PARALLELS — structural or verbal similarity"
    Both types are literary/narrative and explicitly apply to characters.
    ECHOES char<->char is VALID — no contract fired.

  RULES → character target (RETYPE to COMMANDS)
    Architecture: RULES = "Holds authority over a location or domain" (Ruler→Location)
                  COMMANDS = "Military or organizational command" (Commander→Subordinate)
    When a RULES edge's target is a character, the model confused interpersonal
    authority with territorial rule.  The correct type is COMMANDS (same direction).
    => RETYPE edge_type to "COMMANDS" when target IS a character.
       Preserve source/target; add _retyped_from="RULES" + _retype_reason.
    (RULES → non-character: KEEP — no contract fired.)

  Kinship edges (SIBLING_OF, PARENT_OF, CHILD_OF, SPOUSE_OF,
                 STEP_PARENT_OF, STEP_CHILD_OF, BETROTHED_TO,
                 LOVER_OF, ANCESTOR_OF, HEIR_TO,
                 UNCLE_OF, NEPHEW_OF, COUSIN_OF,
                 MILK_BROTHER_OF, NURSED_BY, WET_NURSE_OF)
    Require char<->char  (kinship relationships only apply between characters)
    => FLAG if EITHER endpoint is not a character but the OTHER endpoint IS
       (true relationship with a slug-alias problem — e.g. "queen-cersei"
       instead of "cersei-lannister").
    => DROP if NEITHER endpoint is a character (both non-char: genuinely wrong).

  HOLDS_TITLE, SEAT_OF
    Target should be a place/house/title — NOT a character
    => DROP if target IS a character.
    (GUEST_OF excluded: "Guest -> Host" — the host is frequently a named character.)
    (RULES excluded: handled by the RETYPE contract above.)

  CONTEMPORARY_WITH
    Should connect two events (not two characters who are merely co-present).
    => DROP if BOTH endpoints are characters.

  COMMANDS
    Target must be the person being commanded — a CHARACTER, not a place/faction/group.
    "A orders B to act on C" is at most A→B COMMANDS; A→C is a two-hop collapse.
    => DROP if target is NOT a character.

  MOTIVATES
    Per architecture: MOTIVATES = Event/condition → Actor.  The SOURCE must be an
    event or condition, never a person.  Person→person MOTIVATES is a direction error.
    => DROP if source IS a character.

  CONTRACTED_WITH (+ similar person/org-only contractual types) target-not-object:
    Contractual edges bind persons/orgs, not physical objects (ships, swords, etc.).
    => DROP if target resolves to an object-ish category (artifacts, foods, materials).
    => Soft-flag (no drop) if target category is unknown (slug has no node).

  MEMBER_OF direction:
    MEMBER_OF is person→faction/house.  A faction/house as SOURCE pointing at a
    character TARGET is a reversed direction error.
    => FLIP when source resolves to faction/house AND target resolves to characters
       (conservative: both endpoints must resolve; unknown endpoint → do NOT flip).

  HOLDS_TITLE target-not-place (extended):
    HOLDS_TITLE target should be a title/house, never a location/region.
    The relationship is TRUE (e.g. "robb HOLDS_TITLE north" = King in the North)
    but the target needs retargeting to a title node.
    => FLAG if target resolves to a locations category (keep + annotate).
    (Extends the existing "target must not be a character" check above.)

  Empty evidence_quote
    Any emit whose evidence_quote is empty or whitespace carries no textual support.
    => DROP unconditionally.

CLI usage:
    python3 scripts/stage4-type-contract-validator.py \\
        --input path/to/edges.jsonl \\
        [--kept   path/to/kept.jsonl] \\
        [--dropped path/to/dropped.jsonl] \\
        [--report  path/to/report.md] \\
        [--graph-nodes PATH]   # default: graph/nodes/

NEVER writes to graph/edges/ or to --input.

Importable:
    from scripts.stage4_type_contract_validator import (
        build_character_slugs, build_slug_category_index, type_contract_pass
    )

type_contract_pass return value:
    (disposition, reason)
    disposition is one of: "keep", "drop", "flip", "flag", "retype"
    For "flip"   the caller should swap source_slug/target_slug in the emitted row
                 and add _flipped=True, _flip_reason=reason.
    For "flag"   the caller should add _contract_warning=True, _contract_reason=reason.
    For "retype" the caller should rewrite edge_type to the new type encoded in reason,
                 and add _retyped_from=<original_type>, _retype_reason=reason.
    For "drop"   the caller should add _contract_reason=reason and not emit to kept set.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo path
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_DEFAULT_NODES_DIR = _REPO / "graph" / "nodes"

# ---------------------------------------------------------------------------
# Character set builder
# ---------------------------------------------------------------------------

def build_character_slugs(nodes_dir: Path) -> frozenset[str]:
    """Return the set of all character slugs.

    Mirrors stage4-formalize-edges.py: a slug is a character iff
    graph/nodes/characters/<slug>.node.md exists.  Pure filesystem check.
    """
    chars_dir = nodes_dir / "characters"
    if not chars_dir.is_dir():
        print(f"[warn] characters dir missing: {chars_dir}", file=sys.stderr)
        return frozenset()
    return frozenset(
        p.stem.replace(".node", "")
        for p in chars_dir.glob("*.node.md")
    )


# Cache for slug→category index (populated on first call)
_slug_category_cache: dict[str, str] | None = None
_slug_category_nodes_dir_used: Path | None = None


def build_slug_category_index(nodes_dir: Path) -> dict[str, str]:
    """Return a dict mapping slug → category string.

    Category is the name of the subdirectory under graph/nodes/ that contains
    the slug's .node.md file.  For example:
        "summer-sun" → "artifacts"
        "north"      → "locations"
        "jon-snow"   → "characters"

    Result is cached; repeated calls with the same nodes_dir return the same
    object without re-scanning.  If nodes_dir does not exist, returns {}.

    Directories that start with '_' are skipped (e.g. _conflicts, _unclassified).
    """
    global _slug_category_cache, _slug_category_nodes_dir_used
    if _slug_category_cache is not None and _slug_category_nodes_dir_used == nodes_dir:
        return _slug_category_cache

    index: dict[str, str] = {}
    if not nodes_dir.is_dir():
        print(f"[warn] nodes dir missing: {nodes_dir}", file=sys.stderr)
        _slug_category_cache = index
        _slug_category_nodes_dir_used = nodes_dir
        return index

    for category_dir in nodes_dir.iterdir():
        if not category_dir.is_dir():
            continue
        if category_dir.name.startswith("_"):
            continue  # skip _conflicts, _unclassified, etc.
        for node_file in category_dir.glob("*.node.md"):
            slug = node_file.stem.replace(".node", "")
            index[slug] = category_dir.name

    _slug_category_cache = index
    _slug_category_nodes_dir_used = nodes_dir
    return index


# ---------------------------------------------------------------------------
# Contract definitions
# ---------------------------------------------------------------------------

# Kinship types that require BOTH endpoints to be characters
_KINSHIP_TYPES: frozenset[str] = frozenset({
    "SIBLING_OF",
    "PARENT_OF",
    "CHILD_OF",
    "SPOUSE_OF",
    "STEP_PARENT_OF",
    "STEP_CHILD_OF",
    "BETROTHED_TO",
    "LOVER_OF",
    "ANCESTOR_OF",
    "HEIR_TO",
    "UNCLE_OF",
    "NEPHEW_OF",
    "COUSIN_OF",
    "MILK_BROTHER_OF",
    "NURSED_BY",
    "WET_NURSE_OF",
    "IN_LAW_OF",
})

# Types where the TARGET must NOT be a character.
# GUEST_OF is intentionally excluded: "Guest → Host" — the host is often a person.
# RULES is intentionally excluded: when RULES target IS a character, it is a
# type error (should be COMMANDS), handled by the RETYPE contract below, not DROP.
_NON_CHAR_TARGET_TYPES: frozenset[str] = frozenset({
    "HOLDS_TITLE",
    "SEAT_OF",
    # Vessel captaincy/crew: target MUST be a vessel (object.artifact), never a
    # person (architecture.md).  Backstops the ship-named-after-a-person class
    # (e.g. "Lady Marya" the ship) that the resolver's title-person rung may
    # redirect to the character — you cannot captain/crew a person.
    "CAPTAIN_OF",
    "CREW_OF",
})

# RULES → character RETYPE contract.
# Architecture: RULES = Ruler→Location; COMMANDS = Commander→Subordinate (character).
# When RULES has a character target, the correct edge is COMMANDS (same direction).
# RETYPE: rewrite edge_type to "COMMANDS", preserve source/target/evidence,
# add _retyped_from="RULES" and _retype_reason.
# NOTE: the retyped edge has a character target, which satisfies Contract 4
# (Contract 4 accepts character targets — and also commandable units; see Contract 4).
_RULES_RETYPE_TARGET_TYPE: str = "COMMANDS"

# Types where BOTH endpoints being characters is wrong.
# NOTE: ECHOES is intentionally NOT included here.
# Architecture (Narrative section): PARALLELS = "Event/character A mirrors character B
# thematically"; ECHOES = "Weaker than PARALLELS — structural or verbal similarity."
# Both apply to characters.  ECHOES char<->char is valid and must not be dropped.
_NOT_CHAR_CHAR_TYPES: frozenset[str] = frozenset({
    "CONTEMPORARY_WITH",
})

# COMMANDS target sanity.  COMMANDS = Commander → Subordinate.  A valid target is a
# character (the person commanded) OR a commandable unit/organization (faction/house —
# clan, sellsword company, levy, military order; e.g. gunthor COMMANDS stone-crows,
# victarion COMMANDS iron-fleet, beric COMMANDS brotherhood-without-banners).
# A PLACE target is a two-hop collapse ("A orders B to act on place C"); an object
# target cannot be commanded — both DROP.  Unknown target (no node) → soft-flag.
_COMMANDS_TYPES: frozenset[str] = frozenset({
    "COMMANDS",
})

# Organizational/unit categories that ARE valid COMMANDS targets.  You command a
# faction (clan/company/order) or a house's levies — not just an individual person.
_COMMANDABLE_ORG_CATEGORIES: frozenset[str] = frozenset({
    "factions",
    "houses",
})

# MOTIVATES source-type guard: source must NOT be a character.
# Architecture: MOTIVATES = Event/condition → Actor.  Person as source is a direction error.
_MOTIVATES_TYPES: frozenset[str] = frozenset({
    "MOTIVATES",
})

# CONTRACTED_WITH (and similar person/org-only contractual types): target must not be
# an object-ish node (artifact, food, material).  A ship or sword cannot be a contracting
# party.  Conservative: only drop when the target resolves to a known object category;
# unknown slugs are soft-flagged, not dropped.
_CONTRACTUAL_TYPES: frozenset[str] = frozenset({
    "CONTRACTED_WITH",
})

# Object-ish node categories.  A target in one of these categories is NOT a contracting
# party and indicates a model direction/type error.
_OBJECT_CATEGORIES: frozenset[str] = frozenset({
    "artifacts",
    "foods",
    "materials",
})

# MEMBER_OF direction guard: MEMBER_OF is person→faction/house/org.
# A faction/house source pointing at a character target is a reversed direction error.
# Conservative: both endpoints must resolve to known categories before we flip.
_MEMBER_OF_TYPES: frozenset[str] = frozenset({
    "MEMBER_OF",
})

# Source categories that indicate a reversed MEMBER_OF (faction as source is wrong).
_ORG_SOURCE_CATEGORIES: frozenset[str] = frozenset({
    "factions",
    "houses",
})

# HOLDS_TITLE target-not-place: HOLDS_TITLE target should be a title/house, not a
# location/region.  The existing contract already drops char targets; this extension
# FLAGS (not drops) location targets because the relationship is TRUE but needs
# retargeting to a proper title node.
_HOLDS_TITLE_TYPES: frozenset[str] = frozenset({
    "HOLDS_TITLE",
})

# Location-family categories that are invalid HOLDS_TITLE targets (should be flagged).
_LOCATION_CATEGORIES: frozenset[str] = frozenset({
    "locations",
})

# AGENT_IN / VICTIM_IN target-type contract.
# Architecture: AGENT_IN = executor of an event; VICTIM_IN = patient of an event.
# Both are reification role edges — source is a person or house, target MUST be
# an event node (event.*).  Any non-event target is a model error.
#   DROP  — if target resolves to a known non-event category.
#   FLAG  — if target has no node (alias/unpromoted; keep + annotate).
#   KEEP  — if target resolves to the "events" category.
_ROLE_EVENT_TYPES: frozenset[str] = frozenset({
    "AGENT_IN",
    "VICTIM_IN",
})

# Valid source categories for AGENT_IN / VICTIM_IN.
_ROLE_EVENT_VALID_SOURCE_CATEGORIES: frozenset[str] = frozenset({
    "characters",
    "houses",
})

# The single valid target category for AGENT_IN / VICTIM_IN.
_ROLE_EVENT_TARGET_CATEGORY: str = "events"


# ---------------------------------------------------------------------------
# Core predicate
# ---------------------------------------------------------------------------

def type_contract_pass(
    row: dict,
    character_slugs: frozenset[str],
    slug_category_index: dict[str, str] | None = None,
) -> tuple[str, str]:
    """Test whether an edge row passes its type contract.

    Args:
        row: edge dict (source_slug, target_slug, edge_type, evidence_quote, …)
        character_slugs: frozenset of known character slugs (from build_character_slugs)
        slug_category_index: optional dict slug→category from build_slug_category_index.
            Required for the richer category-based contracts (CONTRACTED_WITH,
            MEMBER_OF direction, HOLDS_TITLE target-not-place).  If None, those
            contracts are skipped.

    Returns:
        (disposition, reason)
        disposition is one of:
            "keep"   — no contract violation
            "drop"   — edge is genuinely wrong; do not keep
            "flip"   — edge is true but direction-reversed; caller should swap
                       source_slug/target_slug and annotate _flipped=True
            "flag"   — edge is true but malformed target/slug; keep with
                       _contract_warning=True annotation
            "retype" — edge is true but edge_type is wrong; caller should rewrite
                       edge_type to the new type encoded in reason, and annotate
                       _retyped_from=<original_type>, _retype_reason=reason
    """
    et  = (row.get("edge_type") or "").strip()
    src = (row.get("source_slug") or "").strip()
    tgt = (row.get("target_slug") or "").strip()

    if not et:
        return "keep", "NO_TYPE: no contract to enforce"

    src_is_char = src in character_slugs
    tgt_is_char = tgt in character_slugs

    # Contract 1: not-char<->char types (ECHOES, CONTEMPORARY_WITH)
    # Both endpoints being characters is a genuinely wrong relationship type.
    if et in _NOT_CHAR_CHAR_TYPES:
        if src_is_char and tgt_is_char:
            return "drop", (
                f"CONTRACT_VIOLATED: {et} must not connect two characters "
                f"(src={src!r} tgt={tgt!r})"
            )

    # Contract 2: kinship — both must be characters.
    # If one endpoint is a character and the other is not, this is most likely a
    # slug-alias problem (e.g. "queen-cersei" instead of "cersei-lannister") where
    # the true relationship is real — FLAG rather than DROP so it can be corrected.
    # If neither endpoint is a character, the edge is genuinely wrong — DROP.
    if et in _KINSHIP_TYPES:
        if not src_is_char and not tgt_is_char:
            # Both non-char: genuinely wrong — DROP.
            return "drop", (
                f"CONTRACT_VIOLATED: {et} requires char<->char, "
                f"but neither endpoint is a character "
                f"(src={src!r}, tgt={tgt!r})"
            )
        if not src_is_char:
            # Source is not a character but target is — likely slug-alias issue.
            return "flag", (
                f"CONTRACT_WARNING: {et} requires char<->char, "
                f"but source {src!r} is not a recognized character slug "
                f"(target {tgt!r} IS a character — probable alias/slug mismatch)"
            )
        if not tgt_is_char:
            # Target is not a character but source is — likely slug-alias issue.
            return "flag", (
                f"CONTRACT_WARNING: {et} requires char<->char, "
                f"but target {tgt!r} is not a recognized character slug "
                f"(source {src!r} IS a character — probable alias/slug mismatch)"
            )

    # Contract 2b: RULES → character target ⇒ RETYPE to COMMANDS.
    # Architecture: RULES = "Holds authority over a location or domain" (Ruler→Location).
    #               COMMANDS = "Military or organizational command" (Commander→Subordinate).
    # When the target is a character, the model confused interpersonal command authority
    # with territorial rule.  The correct edge type is COMMANDS (same source→target direction).
    # RETYPE: rewrite edge_type; preserve all other fields.
    if et == "RULES" and tgt_is_char:
        return "retype", (
            f"CONTRACT_RETYPE: RULES target {tgt!r} is a character — "
            f"architecture defines RULES as Ruler→Location; "
            f"interpersonal command authority uses COMMANDS (Commander→Subordinate). "
            f"Retyping edge_type RULES → COMMANDS. "
            f"(retype_to=COMMANDS)"
        )

    # Contract 3: non-character target types
    # HOLDS_TITLE/SEAT_OF → character target is a genuinely wrong edge.
    if et in _NON_CHAR_TARGET_TYPES:
        if tgt_is_char:
            return "drop", (
                f"CONTRACT_VIOLATED: {et} target must not be a character, "
                f"but target {tgt!r} is a character"
            )

    # Contract 4: COMMANDS target sanity.
    # COMMANDS = Commander → Subordinate.  Valid targets: a character (person commanded)
    # OR a commandable unit/organization (faction/house — clan, company, levy, order).
    #   keep → target is a character, or resolves to factions/houses
    #   drop → target is a PLACE (two-hop collapse: "A orders B to act on place C")
    #   drop → target is an object (artifact/food/material — cannot be commanded)
    #   drop → target resolves to another non-commandable known category
    #   flag → target has no node (relationship may be real — alias/unpromoted; annotate)
    # (Was previously a char-target-only DROP, which false-dropped real unit-command
    #  edges like gunthor→stone-crows once factions became first-class nodes.)
    if et in _COMMANDS_TYPES and not tgt_is_char:
        tgt_cat = slug_category_index.get(tgt) if slug_category_index else None
        if tgt_cat in _COMMANDABLE_ORG_CATEGORIES:
            pass  # valid: commanding a unit/organization (e.g. gunthor → stone-crows)
        elif tgt_cat in _LOCATION_CATEGORIES:
            return "drop", (
                f"CONTRACT_VIOLATED: {et} target {tgt!r} is a place "
                f"(category {tgt_cat!r}) — two-hop collapse "
                f"('A orders B to act on place C'); COMMANDS targets a person or unit"
            )
        elif tgt_cat in _OBJECT_CATEGORIES:
            return "drop", (
                f"CONTRACT_VIOLATED: {et} target {tgt!r} resolves to object category "
                f"{tgt_cat!r} — an object cannot be commanded"
            )
        elif tgt_cat is None:
            return "flag", (
                f"CONTRACT_WARNING: {et} target {tgt!r} has no node — the command "
                f"relationship may be real (alias/unpromoted target); keep + annotate"
            )
        else:
            return "drop", (
                f"CONTRACT_VIOLATED: {et} target {tgt!r} resolves to category "
                f"{tgt_cat!r}, which is not a commandable person or unit"
            )

    # Contract 5: MOTIVATES source-type guard — source must NOT be a character.
    # Architecture: MOTIVATES = Event/condition → Actor.  Person as source is a direction error.
    if et in _MOTIVATES_TYPES:
        if src_is_char:
            return "drop", (
                f"CONTRACT_VIOLATED: {et} source must be an event/condition, "
                f"not a character — person-as-source is a direction error "
                f"(src={src!r})"
            )

    # Contract 6: empty evidence_quote — no textual support, drop unconditionally.
    evidence_quote = (row.get("evidence_quote") or "").strip()
    if not evidence_quote:
        return "drop", (
            f"CONTRACT_VIOLATED: evidence_quote is empty — no textual support "
            f"for {et} edge ({src!r} -> {tgt!r})"
        )

    # -----------------------------------------------------------------------
    # Category-based contracts (require slug_category_index; skipped if None)
    # -----------------------------------------------------------------------
    if slug_category_index is not None:
        src_cat = slug_category_index.get(src)  # None if slug has no node
        tgt_cat = slug_category_index.get(tgt)

        # Contract 7: CONTRACTED_WITH target-not-object.
        # Contractual edges bind persons/orgs.  A ship or food item cannot be a
        # contracting party.  Conservative: only drop if target category is
        # positively known to be object-ish; unknown tgt_cat → soft-flag, no drop.
        if et in _CONTRACTUAL_TYPES:
            if tgt_cat in _OBJECT_CATEGORIES:
                return "drop", (
                    f"CONTRACT_VIOLATED: {et} target must be a person/org, "
                    f"but target {tgt!r} resolves to object category {tgt_cat!r}"
                )
            # Soft-flag (no drop) if target has no node — conservative, don't drop unknown.

        # Contract 8: MEMBER_OF direction guard.
        # MEMBER_OF is person→faction/house.  Faction/house source → character target
        # is a reversed direction error — but the underlying relationship is TRUE
        # (person IS a member of the org).  FLIP: emit target→source instead.
        # Conservative: both endpoints must resolve before we flip.
        if et in _MEMBER_OF_TYPES:
            if src_cat in _ORG_SOURCE_CATEGORIES and tgt_cat == "characters":
                return "flip", (
                    f"CONTRACT_FLIP: {et} direction reversed — source {src!r} "
                    f"is a {src_cat!r} (org/faction) pointing at character target "
                    f"{tgt!r}; MEMBER_OF runs person→faction, not faction→person. "
                    f"Reversed to: {tgt!r} MEMBER_OF {src!r}"
                )

        # Contract 9: HOLDS_TITLE target-not-place.
        # A location/region cannot be a title node, but the underlying relationship
        # is TRUE (e.g. "robb HOLDS_TITLE north" = King in the North).
        # FLAG rather than DROP — keep the edge, annotate for retargeting.
        # The existing Contract 3 already drops char targets; this extension flags
        # location targets.
        if et in _HOLDS_TITLE_TYPES:
            if tgt_cat in _LOCATION_CATEGORIES:
                return "flag", (
                    f"CONTRACT_WARNING: {et} target {tgt!r} resolves to location "
                    f"category {tgt_cat!r} — the relationship is TRUE but the target "
                    f"should be retargeted to a title node "
                    f"(holds_title_target_is_place_should_retarget_to_title)"
                )

        # Contract 10: AGENT_IN / VICTIM_IN target-type contract.
        # Both are reification role edges: source = person/house, target MUST be event.*.
        # Architecture: "Person/House → Event (event.*)" (added Session 83, 2026-06-05).
        #   DROP  — target resolves to a known non-event category.
        #   FLAG  — target has no node (alias/unpromoted event node; keep + annotate).
        #   KEEP  — target resolves to "events".
        if et in _ROLE_EVENT_TYPES:
            if tgt_cat == _ROLE_EVENT_TARGET_CATEGORY:
                pass  # valid: role edge correctly points at an event node
            elif tgt_cat is None:
                return "flag", (
                    f"CONTRACT_WARNING: {et} target {tgt!r} has no node — expected "
                    f"an event.* node; the event may be unminted or the slug is an alias. "
                    f"Keep + annotate for retargeting once the event node exists."
                )
            else:
                return "drop", (
                    f"CONTRACT_VIOLATED: {et} target must be an event node (event.*), "
                    f"but target {tgt!r} resolves to category {tgt_cat!r}. "
                    f"AGENT_IN and VICTIM_IN are reification role edges — source is a "
                    f"person/house and target MUST be an event hub."
                )

    return "keep", "PASS"


# ---------------------------------------------------------------------------
# JSONL I/O helpers
# ---------------------------------------------------------------------------

def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                print(f"[warn] {path}:{lineno}: JSON parse error: {exc}", file=sys.stderr)
    return rows


def _write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------

def _build_report(
    input_path: Path,
    total: int,
    kept_rows: list[dict],
    dropped_rows: list[dict],
    flipped_rows: list[dict],
    flagged_rows: list[dict],
    retyped_rows: list[dict],
    contract_fire_counts: Counter,
) -> str:
    retyped  = len(retyped_rows)
    kept_clean = len(kept_rows) - len(flipped_rows) - len(flagged_rows) - retyped
    dropped  = len(dropped_rows)
    flipped  = len(flipped_rows)
    flagged  = len(flagged_rows)
    drop_rate = (dropped / total * 100) if total else 0.0
    recovered = flipped + flagged + retyped

    lines: list[str] = [
        "# Type-Contract Validator Report",
        "",
        f"**Input:** `{input_path}`  ",
        f"**Total:** {total}  "
        f"**Kept (clean):** {kept_clean}  "
        f"**Flipped:** {flipped}  "
        f"**Flagged:** {flagged}  "
        f"**Retyped:** {retyped}  "
        f"**Dropped:** {dropped}  "
        f"**Drop rate:** {drop_rate:.1f}%  "
        f"**True edges recovered (flip+flag+retype):** {recovered}",
        "",
        "---",
        "",
        "## Contract Fire Counts",
        "",
    ]

    if contract_fire_counts:
        for contract, cnt in sorted(contract_fire_counts.items(), key=lambda x: -x[1]):
            lines.append(f"- `{contract}`: {cnt} rows")
    else:
        lines.append("_No contracts fired._")

    lines += ["", "---", "", "## Dropped Rows", ""]

    if not dropped_rows:
        lines.append("_No rows dropped._")
    else:
        lines.append("Format: `src --EDGE--> tgt | reason`")
        lines.append("")
        for row in dropped_rows:
            src    = row.get("source_slug", "?")
            tgt    = row.get("target_slug", "?")
            et     = row.get("edge_type", "?")
            reason = row.get("_contract_reason", "?")
            lines.append(f"- `{src} --{et}--> {tgt}` | {reason}")

    lines += ["", "---", "", "## Flipped Rows (reversed direction, kept)", ""]

    if not flipped_rows:
        lines.append("_No rows flipped._")
    else:
        lines.append("Format: `new_src --EDGE--> new_tgt (was: orig_src -> orig_tgt) | reason`")
        lines.append("")
        for row in flipped_rows:
            src    = row.get("source_slug", "?")
            tgt    = row.get("target_slug", "?")
            et     = row.get("edge_type", "?")
            reason = row.get("_flip_reason", "?")
            orig_src = row.get("_flipped_from_source", "?")
            orig_tgt = row.get("_flipped_from_target", "?")
            lines.append(f"- `{src} --{et}--> {tgt}` (was: {orig_src!r} -> {orig_tgt!r}) | {reason}")

    lines += ["", "---", "", "## Flagged Rows (kept, annotated for review)", ""]

    if not flagged_rows:
        lines.append("_No rows flagged._")
    else:
        lines.append("Format: `src --EDGE--> tgt | warning`")
        lines.append("")
        for row in flagged_rows:
            src    = row.get("source_slug", "?")
            tgt    = row.get("target_slug", "?")
            et     = row.get("edge_type", "?")
            reason = row.get("_contract_reason", "?")
            lines.append(f"- `{src} --{et}--> {tgt}` | {reason}")

    lines += ["", "---", "", "## Retyped Rows (kept, edge_type corrected)", ""]

    if not retyped_rows:
        lines.append("_No rows retyped._")
    else:
        lines.append("Format: `src --NEW_EDGE--> tgt (was: OLD_EDGE) | reason`")
        lines.append("")
        for row in retyped_rows:
            src      = row.get("source_slug", "?")
            tgt      = row.get("target_slug", "?")
            new_et   = row.get("edge_type", "?")
            orig_et  = row.get("_retyped_from", "?")
            reason   = row.get("_retype_reason", "?")
            lines.append(f"- `{src} --{new_et}--> {tgt}` (was: {orig_et}) | {reason}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Type-contract validator for Stage 4 edges.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input",       required=True, help="Input JSONL file (read-only)")
    parser.add_argument("--kept",        default=None,  help="Write kept rows here (includes flipped + flagged)")
    parser.add_argument("--dropped",     default=None,  help="Write dropped rows here")
    parser.add_argument("--report",      default=None,  help="Write markdown report here")
    parser.add_argument("--graph-nodes", default=str(_DEFAULT_NODES_DIR),
                        help=f"Path to graph/nodes dir (default: {_DEFAULT_NODES_DIR})")
    args = parser.parse_args(argv)

    input_path  = Path(args.input)
    nodes_dir   = Path(args.graph_nodes)

    # Safety: never write to graph/edges/ or overwrite input
    _REPO_EDGES = _REPO / "graph" / "edges"
    for out_path_str in [args.kept, args.dropped, args.report]:
        if out_path_str is None:
            continue
        out_p = Path(out_path_str).resolve()
        if out_p == input_path.resolve():
            sys.exit(f"ERROR: output path must not be the same as --input: {out_p}")
        try:
            out_p.relative_to(_REPO_EDGES)
            sys.exit(f"ERROR: output path must not be inside graph/edges/: {out_p}")
        except ValueError:
            pass

    # Build character set and category index
    print("Building character slug set…", file=sys.stderr)
    character_slugs = build_character_slugs(nodes_dir)
    print(f"  {len(character_slugs)} character slugs loaded", file=sys.stderr)

    print("Building slug→category index…", file=sys.stderr)
    slug_category_index = build_slug_category_index(nodes_dir)
    print(f"  {len(slug_category_index)} slugs indexed", file=sys.stderr)

    # Filter
    rows         = _read_jsonl(input_path)
    kept_rows:    list[dict] = []
    dropped_rows: list[dict] = []
    flipped_rows: list[dict] = []
    flagged_rows: list[dict] = []
    retyped_rows: list[dict] = []
    contract_fire_counts: Counter = Counter()

    for row in rows:
        disposition, reason = type_contract_pass(row, character_slugs, slug_category_index)

        if disposition == "keep":
            kept_rows.append(row)

        elif disposition == "drop":
            annotated = dict(row)
            annotated["_contract_reason"] = reason
            dropped_rows.append(annotated)
            # Track which contract fired
            et = (row.get("edge_type") or "?").strip()
            if "evidence_quote is empty" in reason:
                contract_fire_counts["EMPTY_EVIDENCE_QUOTE"] += 1
            elif et in _NOT_CHAR_CHAR_TYPES:
                contract_fire_counts[f"{et}_char_char"] += 1
            elif et in _KINSHIP_TYPES:
                contract_fire_counts[f"{et}_non_char_endpoint_drop"] += 1
            elif et in _NON_CHAR_TARGET_TYPES:
                contract_fire_counts[f"{et}_char_target"] += 1
            elif et in _COMMANDS_CHAR_TARGET_TYPES:
                contract_fire_counts["COMMANDS_non_char_target"] += 1
            elif et in _MOTIVATES_TYPES:
                contract_fire_counts["MOTIVATES_char_source"] += 1
            elif et in _CONTRACTUAL_TYPES:
                contract_fire_counts["CONTRACTED_WITH_object_target"] += 1
            else:
                contract_fire_counts["other_drop"] += 1

        elif disposition == "flip":
            # Swap source and target; annotate with flip metadata.
            orig_src = row.get("source_slug", "")
            orig_tgt = row.get("target_slug", "")
            flipped = dict(row)
            flipped["source_slug"]          = orig_tgt
            flipped["target_slug"]          = orig_src
            flipped["_flipped"]             = True
            flipped["_flip_reason"]         = reason
            flipped["_flipped_from_source"] = orig_src
            flipped["_flipped_from_target"] = orig_tgt
            kept_rows.append(flipped)
            flipped_rows.append(flipped)
            et = (row.get("edge_type") or "?").strip()
            contract_fire_counts[f"{et}_direction_flipped"] += 1

        elif disposition == "flag":
            # Keep the row as-is; annotate with warning.
            flagged = dict(row)
            flagged["_contract_warning"] = True
            flagged["_contract_reason"]  = reason
            kept_rows.append(flagged)
            flagged_rows.append(flagged)
            et = (row.get("edge_type") or "?").strip()
            if et in _KINSHIP_TYPES:
                contract_fire_counts[f"{et}_non_char_endpoint_flag"] += 1
            elif et in _HOLDS_TITLE_TYPES:
                contract_fire_counts["HOLDS_TITLE_location_target_flagged"] += 1
            else:
                contract_fire_counts["other_flag"] += 1

        elif disposition == "retype":
            # Rewrite edge_type to the new type; annotate with retype metadata.
            # The new type is encoded in reason as "retype_to=<TYPE>".
            orig_et = (row.get("edge_type") or "").strip()
            retyped = dict(row)
            # Extract new type from reason string: "retype_to=COMMANDS"
            new_et = _RULES_RETYPE_TARGET_TYPE  # default for RULES→character case
            if "retype_to=" in reason:
                new_et = reason.split("retype_to=")[-1].strip().rstrip(")")
            retyped["edge_type"]       = new_et
            retyped["_retyped_from"]   = orig_et
            retyped["_retype_reason"]  = reason
            kept_rows.append(retyped)
            retyped_rows.append(retyped)
            contract_fire_counts[f"{orig_et}_retyped_to_{new_et}"] += 1

    total     = len(rows)
    kept      = len(kept_rows)
    dropped   = len(dropped_rows)
    flipped_n = len(flipped_rows)
    flagged_n = len(flagged_rows)
    retyped_n = len(retyped_rows)
    drop_rate = (dropped / total * 100) if total else 0.0
    recovered = flipped_n + flagged_n + retyped_n

    # Write outputs
    if args.kept:
        _write_jsonl(kept_rows, Path(args.kept))
        print(f"Kept rows    -> {args.kept}", file=sys.stderr)

    if args.dropped:
        _write_jsonl(dropped_rows, Path(args.dropped))
        print(f"Dropped rows -> {args.dropped}", file=sys.stderr)

    if args.report:
        report_md = _build_report(
            input_path, total, kept_rows, dropped_rows,
            flipped_rows, flagged_rows, retyped_rows, contract_fire_counts,
        )
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report_md, encoding="utf-8")
        print(f"Report       -> {args.report}", file=sys.stderr)

    # Summary
    print(f"\nType-contract validator summary")
    print(f"  Input:     {input_path} ({total} rows)")
    print(f"  Kept:      {kept} ({kept - flipped_n - flagged_n - retyped_n} clean + "
          f"{flipped_n} flipped + {flagged_n} flagged + {retyped_n} retyped)")
    print(f"  Dropped:   {dropped}  ({drop_rate:.1f}%)")
    print(f"  True edges recovered (flip+flag+retype): {recovered}")
    if contract_fire_counts:
        print("  Contracts fired:")
        for contract, cnt in sorted(contract_fire_counts.items(), key=lambda x: -x[1]):
            print(f"    {contract}: {cnt}")


if __name__ == "__main__":
    main()
