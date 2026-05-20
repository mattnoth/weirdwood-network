#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier output validator.

Loads every output file produced by a Stage 4 batch (per the batch-manifest entry),
checks each row against the required-fields contract from
`.claude/agents/prose-edge-classifier.md`'s "Required fields per decision" table,
plus the field-shape rules.

Exits 0 if all rows pass; exits non-zero with a per-row violation report otherwise.

Three extended check classes (HAIKU-CUTOVER STEP 3, added 2026-05-18):

  1. TYPE CONTRACTS — per-edge-type target-type constraints.
     Transcribed from `.claude/agents/prose-edge-classifier.md` § "Type contracts".
     Requires --graph-nodes path to resolve target slugs to their `type:` field.
     When a target slug is not found in the node index the check is SKIPPED (warn only).
     Violation kind: `type-contract-violation`.

  2. QUALIFIER ENUMS — loads `reference/edge-qualifier-vocab.md`.
     Tier 1 (REQUIRED): rejects missing qualifier or out-of-enum value.
     Tier 2 (OPTIONAL): accepts absent qualifier; rejects present-but-out-of-enum.
     Tier 3 (default): rejects any `qualifier` field present.
     Violation kinds: `qualifier-required-missing`, `qualifier-not-in-enum`,
                      `qualifier-tier3-not-allowed`.

  3. NOTES-REJECTION — rejects any row (any decision type) carrying a `notes` field.
     The `notes` field was deleted from the schema entirely 2026-05-18 (Session 57).
     Violation kind: `notes-field-present`.

Self-test command (catches old 14-violation batch + new extended-check violations):

    # Old violations (14) from archived broken batch-0012:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \\
        --graph-nodes graph/nodes \\
        --arch reference/architecture.md \\
        --qualifier-vocab reference/edge-qualifier-vocab.md \\
        $(find working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15 \\
              -name '*.jsonl' | sed 's/^/--file /') \\
        2>&1 | grep -E '^Validator|\\[invalid-candidate'

    # Notes violations from the 21 freeform-control-arm Sonnet batches:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \\
        --graph-nodes graph/nodes \\
        --arch reference/architecture.md \\
        --qualifier-vocab reference/edge-qualifier-vocab.md \\
        $(find working/wiki/pass2-buckets -name '*.edges.jsonl' \\
              --not -path '*/_archive/*' | sed 's/^/--file /') \\
        2>&1 | grep notes-field-present | wc -l

Usage:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \\
        --batch-id batch-0012 \\
        --mission working/missions/2026-05-14-stage4-v1-bulk-sonnet \\
        --graph-nodes graph/nodes \\
        --qualifier-vocab reference/edge-qualifier-vocab.md

    # Or validate a single output file directly:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \\
        --file working/wiki/pass2-buckets/<bucket>/prose-edges/<slug>.edges.jsonl \\
        --graph-nodes graph/nodes \\
        --qualifier-vocab reference/edge-qualifier-vocab.md

    # Or validate the questions-for-matt.jsonl rows filed during a batch:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \\
        --questions working/wiki/pass2-buckets/questions-for-matt.jsonl \\
        --filed-after 2026-05-15T14:32:00Z
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Repo root (used for normalizer import path resolution)
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Helpers for --unresolved-log append mode (STEP 4 of no-silent-drop pipeline)
# Reuses load_existing_log_keys() and append_unresolved_log() from the
# normalizer script rather than re-implementing them.
# ---------------------------------------------------------------------------

def _load_normalizer_module() -> object:
    """Load stage4-haiku-normalize-edge-types.py via importlib (filename has hyphens)."""
    normalizer_path = _REPO / "scripts" / "stage4-haiku-normalize-edge-types.py"
    spec = importlib.util.spec_from_file_location(
        "stage4_haiku_normalize_edge_types", normalizer_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _derive_batch_id_for_validator(file_path: Path) -> Optional[str]:
    """Best-effort: derive a batch_id from an edges file path.

    Handles both Haiku paths (.../prose-edges-haiku/<slug>.edges.jsonl) and
    Sonnet paths (.../prose-edges/<slug>.edges.jsonl) — returns the bucket
    directory name in either case.  Returns None if unrecognisable.
    """
    parts = file_path.parts
    for i, part in enumerate(parts):
        if part in ("prose-edges-haiku", "prose-edges") and i >= 1:
            return parts[i - 1]
    return None


# ---------------------------------------------------------------------------
# Required-fields contract (mirrors prose-edge-classifier.md)
# ---------------------------------------------------------------------------

REQUIRED_FIELDS_BY_DECISION = {
    ("emit_edge", "source_target"): {
        "decision", "candidate_kind", "evidence_kind",
        "source_slug", "target_slug", "edge_type",
        "evidence_snippet", "evidence_section", "confidence_tier",
    },
    ("emit_edge", "comention"): {
        "decision", "candidate_kind", "evidence_kind",
        "source_slug", "target_slug", "direction", "edge_type",
        "evidence_chapter", "evidence_snippet", "evidence_section",
        "confidence_tier",
    },
    ("emit_edge", "pass1_relationship"): {
        "decision", "candidate_kind", "evidence_kind",
        "source_slug", "target_slug", "edge_type",
        "evidence_chapter", "evidence_book", "evidence_quote",
        "asserted_relation", "extraction_file", "confidence_tier",
    },
    ("reject_just_mention", "source_target"): {
        "decision", "candidate_kind", "source_slug", "target_slug", "reason",
    },
    ("reject_just_mention", "comention"): {
        "decision", "candidate_kind", "pair_a", "pair_b",
        "evidence_chapter", "reason",
    },
    ("reject_just_mention", "pass1_relationship"): {
        "decision", "candidate_kind", "source_slug", "target_slug",
        "evidence_chapter", "asserted_relation", "reason",
    },
    ("escalate_cross_identity", "source_target"): {
        "decision", "candidate_kind", "source_slug", "target_slug",
        "evidence_snippet", "evidence_section", "rationale",
    },
    ("escalate_cross_identity", "comention"): {
        "decision", "candidate_kind", "pair_a", "pair_b",
        "evidence_chapter", "evidence_snippet", "evidence_section", "rationale",
    },
    ("escalate_disambiguation", "source_target"): {
        "decision", "candidate_kind", "source_slug", "target_candidates",
        "evidence_snippet", "evidence_section", "anchor_text",
    },
    ("escalate_disambiguation", "pass1_relationship"): {
        "decision", "candidate_kind", "source_slug", "target_candidates",
        "evidence_quote", "asserted_relation", "extraction_file", "anchor_text",
    },
}

EVIDENCE_KIND_BY_CANDIDATE_KIND = {
    "source_target": "wiki-entity",
    "comention": "wiki-chapter-summary",
    "pass1_relationship": "book-pass1",
}

VALID_DECISIONS = {
    "emit_edge", "reject_just_mention",
    "escalate_cross_identity", "escalate_disambiguation",
}

# Vocab-gap question required fields
VOCAB_GAP_REQUIRED = {
    "question_id", "bucket_id", "agent", "type",
    "proposed_edge_type", "evidence_snippet", "text", "asked_at",
}

# Section header pattern (e.g., "## Appearances", "## Origins", "## Quotes")
SECTION_HEADER_RE = re.compile(r"^## \S")

# What evidence_snippet must NOT be (just a section header, with or without ##)
SECTION_HEADER_AS_SNIPPET = {
    "## appearances", "## origins", "## quotes", "## history",
    "## biography", "## narrative arc", "## description",
    "appearances", "origins", "quotes", "history", "biography",
}

# ---------------------------------------------------------------------------
# Type-contract table (transcribed from .claude/agents/prose-edge-classifier.md
# § "Type contracts on common-failure edge types", 2026-05-18)
#
# Format: edge_type -> (source_pattern | None, target_pattern | None)
# Patterns are prefix-match strings: "place." matches "place.location" and "place.region".
# None means "any type is acceptable".
# Multiple target patterns are stored as a tuple; any match passes.
# ---------------------------------------------------------------------------

# Each value is (source_pattern_or_None, tuple_of_acceptable_target_patterns)
TYPE_CONTRACTS: dict[str, tuple[Optional[str], tuple[str, ...]]] = {
    "LOCATED_AT":          (None,              ("place.location", "place.region")),
    "REGION_OF":           ("place.location",  ("place.region",)),
    "SEAT_OF":             ("place.location",  ("organization.house", "organization.faction")),
    "WIELDS":              ("character.",      ("object.artifact",)),
    "FORGED_BY":           ("object.artifact", ("character.", "concept.culture")),
    "MADE_OF":             ("object.artifact", ("object.material",)),
    "LOOTED_BY":           ("object.artifact", ("character.", "organization.")),
    "GIFTED_TO":           ("object.artifact", ("character.", "organization.")),
    "INHERITED_BY":        ("object.artifact", ("character.", "organization.")),
    "REFORGED_INTO":       ("object.artifact", ("object.artifact",)),
    "WIELDED_IN":          ("object.artifact", ("event.",)),
    "EXECUTED_WITH":       ("character.",      ("object.artifact",)),
    "KILLED_WITH":         ("character.",      ("object.artifact",)),
    "CULTURE_OF":          ("character.",      ("concept.culture",)),
    "WORSHIPS":            ("character.",      ("organization.religion",)),
    "CLERGY_OF":           ("character.",      ("organization.religion",)),
    "MEMBER_OF":           ("character.",      ("organization.",)),
    "HOLDS_TITLE":         ("character.",      ("title",)),
    "ANCESTRAL_WEAPON_OF": ("object.artifact", ("organization.house",)),
    "BORN_AT":             ("character.",      ("place.location",)),
    "DIED_AT":             ("character.",      ("place.location",)),
    "BURIED_AT":           ("character.",      ("place.location",)),
    # Event-target contracts (must NOT be a person)
    "FIGHTS_IN":           (None,              ("event.", "organization.")),
    "ATTENDS":             (None,              ("event.",)),
    "WIELDED_IN":          ("object.artifact", ("event.",)),
    # Session 61 vocab additions (2026-05-19)
    "IMPRISONED_AT":       ("character.",      ("place.location",)),
    "TRAVELS_WITH":        ("character.",      ("character.",)),
    "PRISONER_EXCHANGE_FOR": ("character.",    ("character.",)),
    "GUARDS":              ("character.",      ("character.",)),
    "ENCOUNTERS":          ("character.",      ("character.",)),
}


# ---------------------------------------------------------------------------
# Verb-gate config — Session 61 (2026-05-19)
#
# Certain edge types require a whitelisted verb in the evidence text to be
# valid emissions. Mirrors the CRITICAL RULES verb-gate pattern in the classify
# prompt (Rule 2 KNOWS-STOP, Rule 6 ENCOUNTERS) — promotes the prompt-text
# behavioral constraint to schema enforcement.
#
# Adding KNOWS to this gate is a known follow-up; deferred until an audit
# of existing KNOWS rows determines whether retroactive enforcement would
# raise false-positive violations on already-shipped data.
#
# Match is case-insensitive substring against evidence_snippet (wiki-derived
# shapes) or evidence_quote (pass1_relationship).
# ---------------------------------------------------------------------------
VERB_GATE: dict[str, tuple[str, ...]] = {
    "ENCOUNTERS": (
        "met ",
        "meets ",
        "meeting ",
        "came face to face",
        "face-to-face",
        "face to face",
        "confronted",
        "found himself before",
        "found herself before",
        "stood before",
        "appeared before",
        "encountered",
        "encounter ",
    ),
}


def _type_matches(actual_type: str, patterns: tuple[str, ...]) -> bool:
    """Return True if actual_type starts with any of the given patterns."""
    return any(actual_type.startswith(p) for p in patterns)


# ---------------------------------------------------------------------------
# Qualifier-enum loader (from reference/edge-qualifier-vocab.md)
# ---------------------------------------------------------------------------

# QUALIFIER_ENUM: {edge_type: (tier, frozenset(allowed_values))}
# tier = 1 (REQUIRED) or 2 (OPTIONAL)
QUALIFIER_ENUM: dict[str, tuple[int, frozenset]] = {}


def load_qualifier_vocab(vocab_path: Path) -> dict[str, tuple[int, frozenset]]:
    """Parse reference/edge-qualifier-vocab.md and return the QUALIFIER_ENUM lookup.

    Returns {edge_type: (tier, frozenset(allowed_values))}.
    """
    text = vocab_path.read_text()

    tier1_start = text.find("## Tier 1")
    tier2_start = text.find("## Tier 2")
    tier3_start = text.find("## Tier 3")

    if tier1_start < 0 or tier2_start < 0:
        raise RuntimeError(f"Could not find Tier 1 / Tier 2 sections in {vocab_path}")

    tier1_section = text[tier1_start:tier2_start]
    tier2_section = text[tier2_start:(tier3_start if tier3_start >= 0 else len(text))]

    result: dict[str, tuple[int, frozenset]] = {}

    def parse_section(section: str, tier: int) -> None:
        # Match table rows: | `EDGE_TYPE` | `val1`, `val2`, ... | ...
        for m in re.finditer(r"\| `([A-Z_]+)` \| (.+?) \|", section):
            edge_type = m.group(1)
            vals_raw = m.group(2)
            # Extract backtick-quoted lowercase values
            vals = frozenset(re.findall(r"`([a-z_A-Z]+)`", vals_raw))
            if vals:
                result[edge_type] = (tier, vals)

    parse_section(tier1_section, 1)
    parse_section(tier2_section, 2)
    return result


# ---------------------------------------------------------------------------
# Node-type index (slug -> type string) for type-contract checks
# ---------------------------------------------------------------------------

NODE_TYPE_INDEX: dict[str, str] = {}


def build_node_type_index(nodes_dir: Path) -> dict[str, str]:
    """Walk graph/nodes/ and build a slug→type lookup from frontmatter."""
    index: dict[str, str] = {}
    slug_re = re.compile(r"^slug:\s*(.+)$", re.MULTILINE)
    type_re = re.compile(r"^type:\s*(.+)$", re.MULTILINE)

    for p in nodes_dir.rglob("*.node.md"):
        try:
            text = p.read_text(errors="replace")
            # Only read the frontmatter block (up to second ---)
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            fm = parts[1]
            slug_m = slug_re.search(fm)
            type_m = type_re.search(fm)
            if slug_m and type_m:
                slug = slug_m.group(1).strip()
                node_type = type_m.group(1).strip()
                index[slug] = node_type
        except Exception:
            pass
    return index


# ---------------------------------------------------------------------------
# Vocabulary loader (canonical edge_type list from architecture.md)
# ---------------------------------------------------------------------------

def load_canonical_vocab(arch_path: Path = Path("reference/architecture.md")) -> set[str]:
    """Parse architecture.md and return the set of canonical edge_type names.

    Counts a token as canonical ONLY when it appears as the first backticked token
    of a markdown table row (i.e. ``| `TOKEN` | ...``).  Tokens that appear only
    inside description cells (e.g. deprecated synonyms, permitted reverse-direction
    labels mentioned in prose) are intentionally excluded.

    This ensures the count matches the 159 true canonical types:
      - LOCATED_IN is excluded — it is a deprecated synonym noted in the LOCATED_AT
        row's description cell ("Deprecated synonym `LOCATED_IN` was emitted by an
        early parser variant; normalize on read."), NOT a canonical type.
      - FOSTERED_BY is excluded — it is listed in the WARD_OF row's description as
        "Reverse-direction `FOSTERED_BY` ... is permitted and semantically equivalent",
        NOT as a separate canonical edge type.
    """
    text = arch_path.read_text()
    # Find the Edge Types section
    start = text.find("## Edge Types")
    if start < 0:
        raise RuntimeError("Could not find ## Edge Types section in architecture.md")
    # Find the next H2 (## ) at start-of-line — must NOT match ### subsections
    end_match = re.search(r"\n## [^#]", text[start + 5:])
    end = (start + 5 + end_match.start()) if end_match else len(text)
    section = text[start:end]

    # Only match the first backticked ALL-CAPS token of a table row.
    # Pattern: line starts with "| `TOKEN` |" — captures TOKEN.
    # This excludes tokens mentioned only in description cells.
    table_row_keys = re.findall(r"^\| `([A-Z][A-Z_]+)`", section, re.MULTILINE)
    return set(table_row_keys)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class Violation:
    def __init__(self, file: str, line_no: int, kind: str, detail: str, row: dict | None = None):
        self.file = file
        self.line_no = line_no
        self.kind = kind
        self.detail = detail
        self.row = row

    def __str__(self) -> str:
        loc = f"{self.file}:{self.line_no}"
        slug_hint = ""
        if self.row:
            s = self.row.get("source_slug") or self.row.get("pair_a") or "?"
            t = self.row.get("target_slug") or self.row.get("pair_b") or "?"
            et = self.row.get("edge_type", "?")
            slug_hint = f" [{s} -> {t} : {et}]"
        return f"  {loc} [{self.kind}]{slug_hint} — {self.detail}"


def validate_edge_row(
    row: dict,
    file: str,
    line_no: int,
    vocab: set[str],
    qualifier_enum: Optional[dict] = None,
    node_type_index: Optional[dict] = None,
    unresolved_slugs: Optional[set] = None,
) -> list[Violation]:
    """Validate a single decision row from a prose-edges JSONL output."""
    out: list[Violation] = []
    decision = row.get("decision")
    candidate_kind = row.get("candidate_kind")

    if decision not in VALID_DECISIONS:
        out.append(Violation(file, line_no, "invalid-decision",
                             f"`decision` is {decision!r}, must be one of {sorted(VALID_DECISIONS)}", row))
        return out

    if candidate_kind not in EVIDENCE_KIND_BY_CANDIDATE_KIND:
        out.append(Violation(file, line_no, "invalid-candidate-kind",
                             f"`candidate_kind` is {candidate_kind!r}, must be source_target/comention/pass1_relationship", row))
        return out

    key = (decision, candidate_kind)
    required = REQUIRED_FIELDS_BY_DECISION.get(key)
    if required is None:
        out.append(Violation(file, line_no, "unsupported-shape",
                             f"No required-fields contract for ({decision}, {candidate_kind})", row))
        return out

    missing = required - set(row.keys())
    if missing:
        out.append(Violation(file, line_no, "missing-required-fields",
                             f"Missing fields: {sorted(missing)}", row))

    # Field-shape checks for emit_edge rows
    if decision == "emit_edge":
        # confidence_tier: int 1, 2, or 3
        ct = row.get("confidence_tier")
        if not (isinstance(ct, int) and ct in (1, 2, 3)):
            out.append(Violation(file, line_no, "bad-confidence-tier",
                                 f"`confidence_tier` is {ct!r}, must be int 1/2/3", row))

        # evidence_kind matches candidate_kind
        ek = row.get("evidence_kind")
        expected_ek = EVIDENCE_KIND_BY_CANDIDATE_KIND[candidate_kind]
        if ek != expected_ek:
            out.append(Violation(file, line_no, "bad-evidence-kind",
                                 f"`evidence_kind` is {ek!r}, expected {expected_ek!r} for candidate_kind {candidate_kind!r}", row))

        # edge_type in canonical vocab
        et = row.get("edge_type")
        if et and vocab and et not in vocab:
            out.append(Violation(file, line_no, "edge-type-not-canonical",
                                 f"`edge_type` {et!r} not in canonical vocabulary (architecture.md)", row))

        # Verb gate — Session 61 (2026-05-19)
        # Mechanical enforcement of classify-prompt Rule 6 (and precedent Rule 2):
        # certain edge types require a whitelisted staging verb in evidence text.
        if et and et in VERB_GATE:
            if candidate_kind == "pass1_relationship":
                evidence_text = row.get("evidence_quote", "") or ""
            else:
                evidence_text = row.get("evidence_snippet", "") or ""
            evidence_lower = evidence_text.lower() if isinstance(evidence_text, str) else ""
            verbs = VERB_GATE[et]
            if not any(v in evidence_lower for v in verbs):
                out.append(Violation(file, line_no, "verb-gate-failure",
                                     f"Edge `{et}` requires a whitelisted staging verb in evidence text; "
                                     f"none of {list(verbs)} present", row))

        # evidence_snippet for wiki-derived shapes: not just a section header
        if candidate_kind in ("source_target", "comention"):
            snippet = row.get("evidence_snippet", "")
            if not isinstance(snippet, str):
                out.append(Violation(file, line_no, "bad-evidence-snippet",
                                     f"`evidence_snippet` is not a string", row))
            elif snippet.strip().lower() in SECTION_HEADER_AS_SNIPPET:
                out.append(Violation(file, line_no, "snippet-is-section-header",
                                     f"`evidence_snippet` is a section header ({snippet!r}), not actual prose evidence", row))
            elif len(snippet.strip()) < 10:
                out.append(Violation(file, line_no, "snippet-too-short",
                                     f"`evidence_snippet` length {len(snippet.strip())} chars; must be ≥10", row))
            elif len(snippet) > 500:
                out.append(Violation(file, line_no, "snippet-too-long",
                                     f"`evidence_snippet` length {len(snippet)} chars; must be ≤500 (target ≤200)", row))

            section = row.get("evidence_section", "")
            if isinstance(section, str) and not SECTION_HEADER_RE.match(section):
                out.append(Violation(file, line_no, "bad-evidence-section",
                                     f"`evidence_section` is {section!r}, must start with '## '", row))

        # evidence_quote for pass1_relationship: must be string, ≥5 chars
        if candidate_kind == "pass1_relationship":
            quote = row.get("evidence_quote", "")
            if not isinstance(quote, str) or len(quote.strip()) < 5:
                out.append(Violation(file, line_no, "bad-evidence-quote",
                                     f"`evidence_quote` is missing or too short", row))

        # ---------------------------------------------------------------
        # NEW CHECK 1: Qualifier enums (HAIKU-CUTOVER STEP 3)
        # Loads from QUALIFIER_ENUM (populated by load_qualifier_vocab).
        # Tier 1 (REQUIRED): qualifier must be present and in enum.
        # Tier 2 (OPTIONAL): if present, must be in enum; absent is fine.
        # Tier 3 (default): qualifier field must not be present at all.
        # ---------------------------------------------------------------
        if qualifier_enum is not None and et:
            qual = row.get("qualifier")
            if et in qualifier_enum:
                tier, allowed = qualifier_enum[et]
                if tier == 1:
                    if qual is None or qual == "":
                        out.append(Violation(file, line_no, "qualifier-required-missing",
                                             f"Tier-1 edge `{et}` requires `qualifier` from {sorted(allowed)}; field absent or empty", row))
                    elif qual not in allowed:
                        out.append(Violation(file, line_no, "qualifier-not-in-enum",
                                             f"Tier-1 edge `{et}` qualifier {qual!r} not in allowed set {sorted(allowed)}", row))
                elif tier == 2:
                    if qual is not None and qual != "" and qual not in allowed:
                        out.append(Violation(file, line_no, "qualifier-not-in-enum",
                                             f"Tier-2 edge `{et}` qualifier {qual!r} not in allowed set {sorted(allowed)}", row))
            else:
                # Tier 3: qualifier must not be present
                if qual is not None and qual != "":
                    out.append(Violation(file, line_no, "qualifier-tier3-not-allowed",
                                         f"Tier-3 edge `{et}` must not have a `qualifier` field; got {qual!r}", row))

        # ---------------------------------------------------------------
        # NEW CHECK 2: Type contracts (HAIKU-CUTOVER STEP 3)
        # For edges with known target-type constraints, resolve target_slug
        # to its node type and verify the contract is satisfied.
        # If slug not in node index: skip check, record unresolved slug.
        # ---------------------------------------------------------------
        if node_type_index is not None and et and et in TYPE_CONTRACTS:
            target_slug = row.get("target_slug", "")
            _, target_patterns = TYPE_CONTRACTS[et]
            if target_slug:
                if target_slug in node_type_index:
                    actual_type = node_type_index[target_slug]
                    if not _type_matches(actual_type, target_patterns):
                        out.append(Violation(file, line_no, "type-contract-violation",
                                             f"`{et}` type contract: target `{target_slug}` has type `{actual_type}`, "
                                             f"expected one of {target_patterns}", row))
                else:
                    # Slug not found — skip the check but record it for summary
                    if unresolved_slugs is not None:
                        unresolved_slugs.add(target_slug)

    # ---------------------------------------------------------------
    # NEW CHECK 3: Notes-rejection (HAIKU-CUTOVER STEP 3)
    # The `notes` field was deleted from the schema entirely 2026-05-18.
    # Reject any row (any decision type) that carries a `notes` field.
    # ---------------------------------------------------------------
    if "notes" in row:
        out.append(Violation(file, line_no, "notes-field-present",
                             f"`notes` field present on {decision!r} row; field deleted from schema 2026-05-18 (Session 57)", row))

    return out


def validate_vocab_gap_question(row: dict, file: str, line_no: int) -> list[Violation]:
    """Validate a single vocab-gap question row."""
    out: list[Violation] = []
    if row.get("type") != "vocabulary-gap" and row.get("kind") != "vocab-gap" and row.get("question_type") != "vocab_gap":
        # Not a vocab-gap question; skip
        return out

    # Detect the abbreviated/wrong schema
    if "question_type" in row or "pattern" in row or "frequency" in row:
        out.append(Violation(file, line_no, "vocab-gap-wrong-schema",
                             "Vocab-gap question uses abbreviated schema (`question_type`/`pattern`/`frequency`); use full schema with `question_id`, `bucket_id`, `agent`, `type: vocabulary-gap`, `proposed_edge_type`, `evidence_snippet`, `text`, `asked_at`",
                             row))
        return out

    missing = VOCAB_GAP_REQUIRED - set(row.keys())
    if missing:
        out.append(Violation(file, line_no, "vocab-gap-missing-fields",
                             f"Missing fields: {sorted(missing)}", row))

    # evidence_snippet shape check
    snippet = row.get("evidence_snippet", "")
    if isinstance(snippet, str) and snippet.strip().lower() in SECTION_HEADER_AS_SNIPPET:
        out.append(Violation(file, line_no, "vocab-gap-snippet-is-section-header",
                             f"`evidence_snippet` is a section header, not actual prose", row))

    return out


def load_jsonl(path: str) -> list[tuple[int, dict]]:
    """Return list of (line_no, parsed_row) tuples; skip blank lines."""
    rows = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append((i, json.loads(line)))
            except json.JSONDecodeError as e:
                rows.append((i, {"_parse_error": str(e), "_raw": line.rstrip()}))
    return rows


def get_batch_output_files(mission_dir: str, batch_id: str) -> list[str]:
    """Find every output edge JSONL for the given batch by reading the batch-results JSON."""
    results_path = os.path.join(mission_dir, "results", f"{batch_id}.json")
    if not os.path.exists(results_path):
        # Try the batch-manifest entry instead
        manifest_path = os.path.join(mission_dir, "batch-manifest.jsonl")
        with open(manifest_path) as f:
            for line in f:
                if not line.strip(): continue
                r = json.loads(line)
                if r.get("batch_id") == batch_id:
                    return _derive_output_paths_from_input(r.get("files", []), r.get("shape"))
        raise FileNotFoundError(f"Could not find {results_path} or batch-{batch_id} entry in manifest")

    data = json.load(open(results_path))
    files = data.get("output_files")
    if files:
        return files
    # Some result schemas have files as a list of dicts
    if isinstance(data.get("files"), list):
        return _derive_output_paths_from_results_files(data["files"])
    raise RuntimeError(f"Could not extract output file list from {results_path}")


def _derive_output_paths_from_input(input_paths: list[str], shape: str | None) -> list[str]:
    """Given input candidate file paths, derive the corresponding output edge file paths."""
    out = []
    for p in input_paths:
        # source_target inputs:
        # working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/<slug>.candidates.jsonl
        # → working/wiki/pass2-buckets/<bucket>/prose-edges/<slug>.edges.jsonl
        if "/prose-edge-candidates/" in p:
            out.append(p.replace("/prose-edge-candidates/", "/prose-edges/")
                        .replace(".candidates.jsonl", ".edges.jsonl"))
        elif "/comention-candidates/" in p:
            out.append(p.replace("/comention-candidates/", "/prose-edges/")
                        .replace(".candidates.jsonl", ".comention-edges.jsonl"))
        elif "/extractions-pass1/" in p:
            # working/wiki/pass2-buckets/extractions-pass1/<book>/<slug>.candidates.jsonl
            # → working/wiki/pass2-buckets/extractions-pass1/<book>/prose-edges/<slug>.pass1-edges.jsonl
            parts = p.split("/")
            # Insert "prose-edges" before the slug filename
            slug_with_ext = parts[-1]
            book = parts[-2]
            base = "/".join(parts[:-1])
            out.append(f"{base}/prose-edges/{slug_with_ext.replace('.candidates.jsonl', '.pass1-edges.jsonl')}")
        else:
            # Fall back: assume same path with .candidates → .edges
            out.append(p.replace(".candidates.jsonl", ".edges.jsonl"))
    return out


def _derive_output_paths_from_results_files(files_list: list[dict]) -> list[str]:
    out = []
    for r in files_list:
        slug = r.get("source_slug")
        bucket = r.get("bucket")
        if slug and bucket:
            out.append(f"working/wiki/pass2-buckets/{bucket}/prose-edges/{slug}.edges.jsonl")
    return out


# ---------------------------------------------------------------------------
# Unresolved-log append (--unresolved-log mode)
# ---------------------------------------------------------------------------

def _append_violations_to_log(violations: list["Violation"], log_path: Path) -> None:
    """Append one log row per violation to log_path with stage='validator'.

    Imports load_existing_log_keys() and append_unresolved_log() from the
    normalizer script to reuse its atomic-write and dedup machinery.

    Prints a one-line summary: appended N / already-present M.
    """
    try:
        norm = _load_normalizer_module()
    except Exception as e:
        print(f"WARNING: could not load normalizer module for --unresolved-log: {e}",
              file=sys.stderr)
        return

    load_existing_log_keys = norm.load_existing_log_keys
    append_unresolved_log = norm.append_unresolved_log

    # Load existing keys so we can dedup
    existing_keys: set[tuple] = load_existing_log_keys(log_path)
    already_present = len(existing_keys)

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stage = "validator"

    new_rows: list[dict] = []
    seen_new: set[tuple] = set()

    for v in violations:
        file_str = v.file
        row = v.row or {}
        source_slug = (row.get("source_slug")
                       or row.get("pair_a")
                       or "")
        target_slug = (row.get("target_slug")
                       or row.get("pair_b")
                       or "")
        raw_edge_type = row.get("edge_type") or "<missing>"

        # evidence_snippet: prefer the row's field; truncate to ~200 chars
        snippet = row.get("evidence_snippet") or row.get("evidence_quote") or ""
        if isinstance(snippet, str) and len(snippet) > 200:
            snippet = snippet[:200] + "..."

        reason = v.kind  # violation kind is already a stable, descriptive string

        # Dedup key: (file, source_slug, target_slug, raw_edge_type, stage)
        key = (file_str, source_slug, target_slug, raw_edge_type, stage)
        if key in existing_keys or key in seen_new:
            continue
        seen_new.add(key)

        batch_id = _derive_batch_id_for_validator(Path(file_str))
        new_rows.append({
            "timestamp": ts,
            "stage": stage,
            "batch_id": batch_id,
            "file": file_str,
            "source_slug": source_slug,
            "target_slug": target_slug,
            "raw_edge_type": raw_edge_type,
            "evidence_snippet": snippet,
            "reason": reason,
        })

    appended = append_unresolved_log(log_path, new_rows, dry_run=False)
    skipped = len(violations) - appended  # violations that deduped against existing or in-run dups
    print(f"Unresolved-log: appended {appended} validator row(s), "
          f"{already_present} already in log, "
          f"{skipped} violation(s) deduplicated/skipped "
          f"({log_path})")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", help="Validate all output files for this batch")
    parser.add_argument("--mission", default="working/missions/2026-05-14-stage4-v1-bulk-sonnet",
                        help="Mission directory (for batch-id lookup)")
    parser.add_argument("--file", action="append", default=[],
                        help="Validate specific edge JSONL file(s) — repeat for multiple")
    parser.add_argument("--questions", help="Validate vocab-gap questions in this JSONL file")
    parser.add_argument("--filed-after", help="When validating questions, only check rows with asked_at/filed_at >= this UTC ISO8601 timestamp")
    parser.add_argument("--arch", default="reference/architecture.md",
                        help="Path to architecture.md for vocab loading")
    parser.add_argument("--qualifier-vocab", default="reference/edge-qualifier-vocab.md",
                        help="Path to edge-qualifier-vocab.md for qualifier-enum enforcement")
    parser.add_argument("--graph-nodes", default="graph/nodes",
                        help="Path to graph/nodes/ directory for type-contract resolution")
    parser.add_argument("--skip-type-contracts", action="store_true",
                        help="Disable type-contract checks (e.g., if graph/nodes not available)")
    parser.add_argument("--skip-qualifier-enums", action="store_true",
                        help="Disable qualifier-enum checks (e.g., if edge-qualifier-vocab.md not available)")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument(
        "--unresolved-log",
        metavar="PATH",
        help="(Optional) Append one log row per violation to this persistent "
             "unresolved-edges-log.jsonl file, with stage='validator'. "
             "Deduplicates against existing rows; atomic write. "
             "When omitted the validator behaves exactly as before — additive only.",
    )
    args = parser.parse_args()

    if not (args.batch_id or args.file or args.questions):
        parser.error("Must supply --batch-id, --file, or --questions")

    try:
        vocab = load_canonical_vocab(Path(args.arch))
    except Exception as e:
        print(f"WARNING: could not load canonical vocabulary ({e}); skipping edge_type-in-vocab checks", file=sys.stderr)
        vocab = set()

    # Load qualifier vocab (new check 1)
    qualifier_enum: Optional[dict] = None
    if not args.skip_qualifier_enums:
        vocab_path = Path(args.qualifier_vocab)
        if vocab_path.exists():
            try:
                qualifier_enum = load_qualifier_vocab(vocab_path)
                if args.verbose:
                    print(f"Loaded qualifier vocab: {len(qualifier_enum)} edge types "
                          f"({sum(1 for t,_ in qualifier_enum.values() if t==1)} Tier-1, "
                          f"{sum(1 for t,_ in qualifier_enum.values() if t==2)} Tier-2)", file=sys.stderr)
            except Exception as e:
                print(f"WARNING: could not load qualifier vocab ({e}); skipping qualifier-enum checks", file=sys.stderr)
        else:
            print(f"WARNING: qualifier-vocab file not found at {vocab_path}; skipping qualifier-enum checks", file=sys.stderr)

    # Load node type index (new check 2)
    node_type_index: Optional[dict] = None
    unresolved_slugs: set = set()
    if not args.skip_type_contracts:
        nodes_dir = Path(args.graph_nodes)
        if nodes_dir.exists():
            try:
                node_type_index = build_node_type_index(nodes_dir)
                if args.verbose:
                    print(f"Indexed {len(node_type_index)} node slugs for type-contract checks", file=sys.stderr)
            except Exception as e:
                print(f"WARNING: could not build node type index ({e}); skipping type-contract checks", file=sys.stderr)
        else:
            print(f"WARNING: graph/nodes dir not found at {nodes_dir}; skipping type-contract checks", file=sys.stderr)

    files_to_check: list[str] = list(args.file)
    if args.batch_id:
        try:
            batch_files = get_batch_output_files(args.mission, args.batch_id)
            files_to_check.extend(batch_files)
        except Exception as e:
            print(f"ERROR: could not enumerate batch {args.batch_id} files: {e}", file=sys.stderr)
            return 2

    all_violations: list[Violation] = []
    files_checked = 0
    files_missing = 0
    rows_checked = 0

    for f in files_to_check:
        if not os.path.exists(f):
            files_missing += 1
            if args.verbose:
                print(f"  SKIP (missing): {f}", file=sys.stderr)
            continue
        files_checked += 1
        rows = load_jsonl(f)
        for line_no, row in rows:
            rows_checked += 1
            if "_parse_error" in row:
                all_violations.append(Violation(f, line_no, "json-parse-error",
                                                row["_parse_error"]))
                continue
            all_violations.extend(validate_edge_row(
                row, f, line_no, vocab,
                qualifier_enum=qualifier_enum,
                node_type_index=node_type_index,
                unresolved_slugs=unresolved_slugs,
            ))

    if args.questions:
        if not os.path.exists(args.questions):
            print(f"ERROR: questions file not found: {args.questions}", file=sys.stderr)
            return 2
        rows = load_jsonl(args.questions)
        for line_no, row in rows:
            if "_parse_error" in row:
                all_violations.append(Violation(args.questions, line_no, "json-parse-error",
                                                row["_parse_error"]))
                continue
            if args.filed_after:
                ts = row.get("asked_at") or row.get("filed_at") or ""
                if ts < args.filed_after:
                    continue
            rows_checked += 1
            all_violations.extend(validate_vocab_gap_question(row, args.questions, line_no))

    # Violation breakdown by kind (new extended checks get their own counts)
    violation_kinds: dict[str, int] = {}
    for v in all_violations:
        violation_kinds[v.kind] = violation_kinds.get(v.kind, 0) + 1

    # Report
    print(f"Validator summary: files_checked={files_checked}, files_missing={files_missing}, "
          f"rows_checked={rows_checked}, violations={len(all_violations)}")
    if unresolved_slugs and args.verbose:
        print(f"  Type-contract: {len(unresolved_slugs)} target slug(s) not found in node index (checks skipped for those rows)", file=sys.stderr)
    if unresolved_slugs and not args.verbose and node_type_index is not None:
        print(f"  NOTE: {len(unresolved_slugs)} target slug(s) unresolvable in graph/nodes (type-contract checks skipped for those); use --verbose to list", file=sys.stderr)
    if all_violations:
        print("\nViolations by kind:")
        for kind, count in sorted(violation_kinds.items()):
            print(f"  {kind}: {count}")
        print("\nViolation detail:")
        for v in all_violations:
            print(v)

    # ------------------------------------------------------------------
    # --unresolved-log append mode (STEP 4 of no-silent-drop pipeline)
    # Purely additive: only runs when --unresolved-log is supplied.
    # When omitted this block is entirely skipped — no behaviour change.
    # ------------------------------------------------------------------
    if args.unresolved_log:
        _append_violations_to_log(all_violations, Path(args.unresolved_log))

    if all_violations:
        return 1
    print("CLEAN ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
