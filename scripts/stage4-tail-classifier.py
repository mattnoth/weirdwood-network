#!/usr/bin/env python3
"""stage4-tail-classifier.py — LLM tail classifier for the Stage 4 Pass-1-derived edge pipeline.

The deterministic spine (stage4-pass1-edge-candidates.py) emitted 2,834 typed
edges.  Rows it resolved to a node pair but could NOT type were written to
_tail/{book}/*.tail.jsonl with decision=needs_type.  This script asks an LLM
to assign ONE locked-vocab edge type per row (or REJECT).

Architecture:
  - Every claude invocation uses `claude -p` subprocess, cwd=/tmp, so it does
    NOT load this repo's CLAUDE.md (~28 k token cold-load avoided).
  - Rows are batched (default 40 per call) to amortise per-call overhead.
  - Each row in the batch gets an explicit `idx` integer; the model MUST echo
    it in each output object.  Missing/extra/duplicate idx → classify_failed.
  - Returned edge_type is conformed against the locked vocab from
    architecture.md.  Not-in-vocab and not-REJECT → classify_failed.
    REJECT → rejected.jsonl.  Tier-1 type with no qualifier → needs-qualifier.
  - Accepted edges are written in the EXACT same schema as the deterministic
    edges (pass1-derived/{book}/*.edges.jsonl) with typed_by="sonnet".

Input (default):
  working/wiki/pass2-buckets/pass1-derived/_tail/{book}/*.tail.jsonl
  (books: agot acok asos affc adwd)

Input (--input-dir):
  Any directory tree of JSONL files containing candidate rows with edge_type==null.
  Filtered by --candidate-kinds if specified (comma-separated list of candidate_kind
  values, e.g. pass1_dialogue,pass1_events,pass1_info,pass1_food).

Output (--apply only):
  working/wiki/pass2-buckets/pass1-derived/_tail-typed/{book}/*.edges.jsonl
  working/wiki/pass2-buckets/pass1-derived/_tail-typed/{book}/*.rejected.jsonl
  working/wiki/pass2-buckets/pass1-derived/_tail-needs-qualifier/{book}/*.needs-qualifier.jsonl
  working/wiki/pass2-buckets/pass1-derived/_tail-typed/run-summary.json

Usage:
  python3 scripts/stage4-tail-classifier.py                   # dry-run (default)
  python3 scripts/stage4-tail-classifier.py --dry-run         # explicit dry-run
  python3 scripts/stage4-tail-classifier.py --apply           # run for real
  python3 scripts/stage4-tail-classifier.py --apply --book affc
  python3 scripts/stage4-tail-classifier.py --apply --smoke 3
  python3 scripts/stage4-tail-classifier.py --apply --smoke 50 --book agot
  python3 scripts/stage4-tail-classifier.py --apply --skip-existing
  python3 scripts/stage4-tail-classifier.py --apply --model claude-haiku-4-5
  python3 scripts/stage4-tail-classifier.py --dry-run --chunk-size 20
  # Extra-tables smoke run (stratified 200-row sample):
  python3 scripts/stage4-tail-classifier.py --dry-run \\
      --input-dir working/wiki/pass2-buckets/pass1-derived/_extra-tables \\
      --candidate-kinds pass1_dialogue,pass1_events,pass1_info,pass1_food \\
      --sample-n 200
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
TAIL_DIR = REPO / "working/wiki/pass2-buckets/pass1-derived/_tail"
EXTRA_TABLES_DIR = REPO / "working/wiki/pass2-buckets/pass1-derived/_extra-tables"
OUT_BASE = REPO / "working/wiki/pass2-buckets/pass1-derived/_tail-typed"
OUT_NEEDS_QUAL_DIR = REPO / "working/wiki/pass2-buckets/pass1-derived/_tail-needs-qualifier"
ARCH_MD = REPO / "reference/architecture.md"
QUAL_VOCAB_MD = REPO / "reference/edge-qualifier-vocab.md"
GRAPH_NODES_DIR = REPO / "graph/nodes"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_CHUNK_SIZE = 40

# ---------------------------------------------------------------------------
# Dynamic imports (hyphenated filenames)
# ---------------------------------------------------------------------------

def _load_module(filename: str, mod_name: str):
    """Load a script from scripts/ by filename via importlib."""
    path = Path(__file__).parent / filename
    if not path.exists():
        sys.exit(f"ERROR: Required module not found: {path}")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_resolver():
    """Load stage4_name_resolver (underscore filename — importable directly)."""
    path = Path(__file__).parent / "stage4_name_resolver.py"
    if not path.exists():
        sys.exit(f"ERROR: stage4_name_resolver.py not found: {path}")
    spec = importlib.util.spec_from_file_location("stage4_name_resolver", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["stage4_name_resolver"] = mod
    spec.loader.exec_module(mod)
    return mod


_resolver = _load_resolver()
load_node_display_names = _resolver.load_node_display_names


# ---------------------------------------------------------------------------
# Locked vocab + Tier-1 set  (reuse same logic as stage4-pass1-edge-candidates.py)
# ---------------------------------------------------------------------------

def load_locked_vocab(arch_path: Path) -> frozenset[str]:
    """Extract the canonical active edge type set from architecture.md.

    Uses the same scoped table-row extraction as build-edge-type-counts.py
    (extract_canonical_types): only matches rows of the form
    ``| `EDGE_TYPE` | ...`` that appear inside the
    ``## Edge Types (Relationship Categories)`` section, which correctly
    excludes prose mentions, history notes, deprecated aliases, and book-code
    tokens (KNOWS, LOCATED_IN, ACCOMPANIES, FIELD_EDGE_MAP, etc.).
    """
    # Load build-edge-type-counts.py via importlib (hyphenated filename).
    _build_mod = _load_module("build-edge-type-counts.py", "build_edge_type_counts")
    type_to_category, _ = _build_mod.extract_canonical_types(arch_path)
    return frozenset(type_to_category.keys())


def load_tier1_edge_types(qual_vocab_path: Path) -> frozenset[str]:
    """Parse reference/edge-qualifier-vocab.md and return the set of Tier-1 edge types."""
    try:
        text = qual_vocab_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"WARNING: Cannot read qualifier vocab {qual_vocab_path}: {exc}", file=sys.stderr)
        return frozenset()

    tier1_types: set[str] = set()
    in_tier1 = False

    for line in text.splitlines():
        if line.startswith("## Tier 1"):
            in_tier1 = True
            continue
        if in_tier1 and line.startswith("## "):
            in_tier1 = False
            continue
        if not in_tier1:
            continue
        m = re.search(r"`([A-Z][A-Z_]+)`", line)
        if m:
            tier1_types.add(m.group(1))

    return frozenset(tier1_types)


# ---------------------------------------------------------------------------
# Display name resolution
# ---------------------------------------------------------------------------

def build_display_name_map(locked_vocab: frozenset[str]) -> dict[str, str]:
    """Build slug → display name map from graph/nodes/."""
    # Collect all slugs from node files
    node_slugs: set[str] = set()
    skip_dirs = {"_conflicts", "_unclassified", "_stage3-preview"}
    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if any(p in skip_dirs for p in parts):
            continue
        slug = node_file.name[: -len(".node.md")]
        node_slugs.add(slug)

    return load_node_display_names(node_slugs, GRAPH_NODES_DIR)


_CACHED_DISPLAY_NAMES: dict[str, str] | None = None


def get_display_name(slug: str) -> str:
    """Get display name for a slug, falling back to de-kebabbed form."""
    global _CACHED_DISPLAY_NAMES
    if _CACHED_DISPLAY_NAMES is None:
        _CACHED_DISPLAY_NAMES = build_display_name_map(frozenset())
    name = _CACHED_DISPLAY_NAMES.get(slug)
    if name:
        return name
    # De-kebab fallback: "brienne-tarth" → "Brienne Tarth"
    return " ".join(part.capitalize() for part in slug.split("-"))


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------

# Concise type contracts for the classify prompt (inline summary — full vocab
# is injected from architecture.md).  This preamble orients the model quickly.
_PROMPT_PREAMBLE = """\
You are a relationship classifier for the Weirwood Network ASOIAF knowledge graph.
Classify each relationship row as exactly ONE edge type from the LOCKED VOCABULARY below, or REJECT.

RULES:
1. Return STRICT JSON only — a single JSON array, one object per input row, in idx order.
2. Each object: {"idx": <integer>, "edge_type": "<TYPE_FROM_VOCAB_OR_REJECT>", "qualifier": "<only if Tier-1 type>"}
3. Use EXACTLY the spelling from the locked vocab list. No variations, no prose.
4. REJECT if hint+evidence does not clearly support any vocab type.
5. Direction is FIXED: edge runs source → target (do NOT reverse).
6. Rule 6: ENCOUNTERS requires explicit staging verb — NEVER emit for co-presence.
   ENCOUNTERS records a plot-significant face-to-face meeting anchored by EXPLICIT PROSE STAGING.
   It is NOT a fallback for two entities appearing in the same scene, battle, court, or passage.
   - Use ENCOUNTERS ONLY when the hint or evidence_quote contains a past-tense staging verb
     from this whitelist: met, meets, meeting, came face to face, confronted, encountered.
   - The infinitive "to meet" is NOT a staging verb — it expresses intent, not a consummated
     encounter. If you see only "to meet" or "planned to meet": REJECT or pick another type.
   - If no whitelisted staging verb is present: ENCOUNTERS is IMPOSSIBLE — pick a different
     type or REJECT. Do not argue around the absence.
   - Even if a staging verb is present, verify it actually stages a meeting between the
     specific source and target in this row (not between two other characters in the passage).
   - ENCOUNTERS also requires both source AND target to be characters, never places/events/objects.
7. Tier-1 types (REQUIRE qualifier field): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,\
 HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO
   - For Tier-1, qualifier MUST be from the documented enum (see below).
   - For all other types, omit qualifier entirely.
8. No prose explanation. JSON array only.
9. GATED TYPES — these five types have narrow, strict definitions. Read carefully before using:
   - INFORMS: ONLY a spy or agent reporting to a handler in an ONGOING INTELLIGENCE RELATIONSHIP.
     DO NOT use INFORMS for generic "X told Y something" — use REVEALS_TO for one-time disclosures.
   - ADVISES: ONLY genuine counsel from an institutional advisor role (maester, Hand, councillor).
     DO NOT use ADVISES for rebukes, arguments, objections, or casual opinion-giving.
   - MANIPULATES: The target MUST be UNAWARE they are being used or deceived.
     DO NOT use MANIPULATES for overt threats, coercion, or open provocation.
   - SUPPORTS: ONLY evidentiary or theory-layer support (a theory supported by evidence).
     DO NOT use SUPPORTS for interpersonal backing, political alliances, or emotional support.
   - ALIAS_OF: ONLY for true identity aliases (alternate names for the same person).
     DO NOT use ALIAS_OF for titular forms of address such as "King Robert", "Ser X", "Lord Y",
     "Maester Z" — these are titles, NOT aliases.
   When in doubt about a gated type, REJECT or pick a clearly-correct alternative type.
10. TIER ASSIGNMENT — do NOT default every row to Tier-1:
    - Tier-1: ONLY for explicit prose statements of the relationship ("his uncle X", "Eddard's wife Y",
      direct speech attributing a clear relationship).
    - Tier-2: implied-but-clear from context (their behavior, roles, or narrative framing strongly
      implies the relationship even without an explicit statement).
    - Tier-3: inferred — the relationship is plausible given the evidence but not directly stated.
    Emit the confidence_tier field as an integer (1, 2, or 3) in each output object.
11. ANTI-PATTERN TYPE GATES — these five types have specific misuse patterns that appear frequently.
    Read before classifying any row involving two characters in the same scene or chapter:
    - CONTEMPORARY_WITH: CONTEMPORARY_WITH is for two distinct EVENTS that overlap in time — NOT for
      two characters who merely appear in the same scene or chapter. If two PEOPLE are simply co-present,
      do not emit CONTEMPORARY_WITH; pick the actual relationship if one is evidenced, otherwise REJECT.
      Two people being in the same room is not a graph edge.
    - COMPANION_OF: COMPANION_OF requires prose that EXPLICITLY names a friendship, sworn-brotherhood,
      or sustained personal bond ('fast friends', 'sworn brothers', 'his closest companion'). Sharing a
      single scene, meal, journey, or battle does NOT qualify. If there is no explicit friendship/bond
      language in the evidence, use TRAVELS_WITH (if they travel together) or REJECT. Do not infer
      companionship from co-presence.
    - CITED_BY and CONTRADICTS: CITED_BY and CONTRADICTS are THEORY-SUPPORT edges connecting a theory
      to its evidence or theorist — they are NEVER interpersonal relationships. Do not use CITED_BY for
      dreams, songs, or one character mentioning another. Do not use CONTRADICTS for interpersonal
      disagreements, arguments, or reassurances (use OPPOSES or REVEALS_TO if a real relationship is
      evidenced, else REJECT). A character dreaming of another is DREAMS_OF, not CITED_BY.
    - ASSAULTS: ASSAULTS is sexual violence specifically. Non-sexual physical violence (grabbing, shoving,
      striking) is ATTACKS. Threatening to throw someone to their death is ATTACKS or IMPRISONS,
      not ASSAULTS.
    - NURSED_BY: NURSED_BY is wet-nursing specifically. A maester giving medicine or treating a patient
      is HEALS, not NURSED_BY.

TIER-1 QUALIFIER ENUMS (required when using these types):
  SIBLING_OF: full | half | step | milk | unknown
  SPOUSE_OF: current | former | annulled | widowed | salt_wife | unknown
  PARENT_OF: biological | adopted | claimed | rumored | disputed | unknown
  WARD_OF: formal | informal | hostage | unknown
  HOLDS_TITLE: current | former | claimed | contested | historical | unknown
  VOWS_TO: active | kept | broken | fulfilled | unknown
  MANIPULATES: via_bribe | via_flattery | via_false_information | via_threat | via_seduction | unknown
  SWORN_TO: current | former | deserted | by_marriage | claimed | unknown

LOCKED EDGE VOCABULARY (use EXACTLY one of these, or REJECT):
"""

# The five gated types and their anti-pattern descriptions.
# This list is also used for --gate-vocab CLI default and the prompt injection.
DEFAULT_GATED_TYPES: tuple[str, ...] = (
    "INFORMS",
    "ADVISES",
    "MANIPULATES",
    "SUPPORTS",
    "ALIAS_OF",
)


def build_vocab_block(
    locked_vocab: frozenset[str],
    gated_types: tuple[str, ...] | None = None,
) -> str:
    """Return a sorted, newline-separated list of vocab types for the prompt.

    Gated types are included in the vocabulary (NOT removed — the blocklist keeps
    the ~150 other types fully available) but annotated with a [GATED] marker so
    the model knows to apply the strict anti-pattern checks from Rule 9.
    """
    gated_set: frozenset[str] = frozenset(gated_types) if gated_types else frozenset()
    lines: list[str] = []
    for t in sorted(locked_vocab):
        if t in gated_set:
            lines.append(f"  {t}  [GATED — see Rule 9 before using]")
        else:
            lines.append(f"  {t}")
    return "\n".join(lines)


def render_classify_prompt(
    rows: list[dict],
    locked_vocab: frozenset[str],
    gated_types: tuple[str, ...] | None = None,
) -> str:
    """Render the classify prompt for a batch of tail rows.

    Each row gets an explicit idx injected.  The model must echo idx in output.
    gated_types: tuple of edge type strings to annotate as [GATED] in the vocab
    block (blocklist approach — types remain available but carry strict Rule 9
    anti-pattern guidance).
    """
    vocab_block = build_vocab_block(locked_vocab, gated_types=gated_types)

    lines = [_PROMPT_PREAMBLE + vocab_block, "", "ROWS TO CLASSIFY:"]

    for i, row in enumerate(rows):
        src_display = get_display_name(row["source_slug"])
        tgt_display = get_display_name(row["target_slug"])
        chapter = row.get("evidence_chapter", "")
        hint = row.get("hint_raw", "")
        quote = row.get("evidence_quote", "")

        lines.append(
            f'\n[{{"idx": {i}, '
            f'"source": "{src_display}", '
            f'"target": "{tgt_display}", '
            f'"hint": "{hint}", '
            f'"evidence_chapter": "{chapter}", '
            f'"evidence_quote": {json.dumps(quote)}}}]'
        )

    lines.append(
        "\nReturn a JSON array with exactly one object per row above. "
        "Each object must have 'idx' (integer matching the row), 'edge_type' "
        "(exactly from vocab or REJECT), 'qualifier' (only for Tier-1 types), "
        "and 'confidence_tier' (integer 1, 2, or 3 — see Rule 10)."
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# claude -p subprocess invocation (cwd=/tmp to avoid CLAUDE.md load)
# ---------------------------------------------------------------------------

def invoke_claude(prompt: str, model: str) -> dict:
    """Call `claude -p` from /tmp (avoids repo CLAUDE.md cold-load).

    Returns dict with keys: returncode, raw_output, result_json,
    total_cost_usd, error_message.
    """
    cmd = [
        "claude",
        "-p",
        "--dangerously-skip-permissions",
        "--model", model,
        "--output-format", "json",
        prompt,
    ]

    t_start = time.monotonic()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd="/tmp",   # CRITICAL: avoids loading this repo's CLAUDE.md
    )
    duration_s = round(time.monotonic() - t_start, 2)

    raw_output = result.stdout.strip()
    error_message = result.stderr.strip()[:500] if result.stderr.strip() else None

    # Parse the outer claude JSON envelope
    result_json: dict | None = None
    total_cost_usd = 0.0
    try:
        outer = json.loads(raw_output)
        total_cost_usd = outer.get("total_cost_usd", 0.0)
        result_json = outer
    except (json.JSONDecodeError, ValueError):
        pass

    return {
        "returncode": result.returncode,
        "raw_output": raw_output,
        "result_json": result_json,
        "total_cost_usd": total_cost_usd,
        "error_message": error_message,
        "duration_s": duration_s,
    }


# ---------------------------------------------------------------------------
# Parse and align the model's batch response
# ---------------------------------------------------------------------------

def parse_batch_response(raw_output: str, expected_count: int) -> tuple[list[dict], str | None]:
    """Extract the JSON array from the claude -p result envelope.

    Returns (parsed_objects, error_message).
    parsed_objects may be [] on parse failure.
    """
    # claude --output-format json wraps the model's text in an envelope:
    # {"result": "<model text>", "total_cost_usd": ..., ...}
    # Alternatively, raw_output may already be a JSON array (fallback path).
    model_text = None
    try:
        outer = json.loads(raw_output)
        if isinstance(outer, list):
            # raw_output IS the JSON array directly
            return outer, None
        elif isinstance(outer, dict):
            model_text = outer.get("result", "")
        else:
            model_text = raw_output
    except (json.JSONDecodeError, ValueError):
        # raw_output is not valid JSON at all — treat as raw model text
        model_text = raw_output

    if not model_text:
        return [], "Empty model response"

    # Strip markdown code fences if present
    stripped = model_text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        # Remove first and last fence lines
        inner_lines = []
        in_fence = False
        for ln in lines:
            if ln.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or (not inner_lines and not in_fence):
                inner_lines.append(ln)
        stripped = "\n".join(inner_lines).strip()
        if not stripped:
            stripped = "\n".join(lines[1:-1]).strip()

    # Try parsing as JSON array
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, list):
            return parsed, None
        # Wrapped in another envelope? Try to extract result field
        if isinstance(parsed, dict) and "result" in parsed:
            inner_text = parsed["result"]
            if isinstance(inner_text, str):
                inner = json.loads(inner_text)
                if isinstance(inner, list):
                    return inner, None
        return [], f"Model returned non-list JSON: {type(parsed).__name__}"
    except json.JSONDecodeError as exc:
        return [], f"JSON parse error: {exc}"


def align_batch_output(
    parsed_objects: list[dict],
    input_rows: list[dict],
) -> dict[int, dict]:
    """Align model outputs back to input rows by idx.

    Returns {idx: obj} for all valid idx values.  Duplicate or out-of-range
    idx values are logged but not included (the calling code marks those rows
    as classify_failed).
    """
    aligned: dict[int, dict] = {}
    n = len(input_rows)
    seen_idx: set[int] = set()

    for obj in parsed_objects:
        if not isinstance(obj, dict):
            continue
        raw_idx = obj.get("idx")
        if raw_idx is None or not isinstance(raw_idx, int):
            continue
        idx = raw_idx
        if idx < 0 or idx >= n:
            # Out-of-range idx — ignore
            continue
        if idx in seen_idx:
            # Duplicate idx — mark as conflict; don't include
            aligned.pop(idx, None)
            seen_idx.discard(idx)  # remove so we don't accidentally include it
            seen_idx.add(-idx - 1)  # sentinel to track "was duplicated"
            continue
        seen_idx.add(idx)
        aligned[idx] = obj

    return aligned


# ---------------------------------------------------------------------------
# Conform: validate edge_type against locked vocab
# ---------------------------------------------------------------------------

def conform_edge_type(
    edge_type: str,
    locked_vocab: frozenset[str],
    tier1_types: frozenset[str],
    qualifier: str | None,
) -> tuple[str, str | None]:
    """Validate and normalize a model-returned edge_type.

    Returns (decision, conform_error_or_none):
      - ("emit_edge", None)         — valid type, qualifier ok
      - ("rejected", None)          — REJECT
      - ("classify_failed", reason) — invalid type
      - ("needs_qualifier", None)   — Tier-1 type missing qualifier
    """
    if edge_type == "REJECT":
        return "rejected", None

    if edge_type not in locked_vocab:
        return "classify_failed", f"edge_type={edge_type!r} not in locked vocab"

    # Tier-1 check: qualifier required
    if edge_type in tier1_types:
        if not qualifier:
            return "needs_qualifier", None

    return "emit_edge", None


# ---------------------------------------------------------------------------
# Schema: build output rows matching the deterministic edge schema
# ---------------------------------------------------------------------------

def derive_typed_by(model: str) -> str:
    """Map a claude model identifier to a short typed_by label.

    Examples:
      "claude-haiku-4-5"   → "haiku"
      "claude-sonnet-4-6"  → "sonnet"
      "claude-opus-4"      → "opus"
    Falls back to the raw model string if no pattern matches.
    """
    m_lower = model.lower()
    if "haiku" in m_lower:
        return "haiku"
    if "sonnet" in m_lower:
        return "sonnet"
    if "opus" in m_lower:
        return "opus"
    # Unknown model: use model name as-is (truncate for safety)
    return m_lower[:32]


def build_emit_edge_row(
    tail_row: dict,
    edge_type: str,
    qualifier: str | None,
    model: str,
    run_id: str,
    model_confidence_tier: int | None = None,
) -> dict:
    """Build an emit_edge row matching the deterministic edge schema exactly.

    Fields from the deterministic schema:
      decision, candidate_kind, edge_type, source_slug, source_resolution_status,
      target_slug, target_resolution_status, evidence_kind, evidence_book,
      evidence_chapter, evidence_section, evidence_quote, evidence_ref,
      asserted_relation, hint_raw, extraction_file, confidence_tier, typed_by,
      corroborates_known_edge, wiki_edge_type, locate_status, run_id,
      schema_version, produced_at

    Tail rows lack: source_resolution_status, target_resolution_status,
    evidence_book, asserted_relation, extraction_file, confidence_tier.
    We carry "tail-llm" for resolution_status, derive evidence_book from
    evidence_chapter, and set confidence_tier from the model's emitted tier
    (or fall back to 1 if the model did not emit a tier).

    candidate_kind is preserved from the INPUT row's actual candidate_kind
    (e.g. pass1_dialogue, pass1_events, pass1_info, pass1_food,
    pass1_relationship) rather than being hardcoded.

    typed_by is derived from the --model argument (e.g. "haiku", "sonnet",
    "opus") rather than being hardcoded, so Haiku runs are labeled correctly.
    """
    chapter = tail_row.get("evidence_chapter", "")
    # Derive evidence_book from chapter slug prefix (e.g. "affc-brienne-03" → "affc")
    evidence_book = chapter.split("-")[0] if chapter else ""

    # Preserve the source row's candidate_kind (varies across table types)
    candidate_kind = tail_row.get("candidate_kind", "pass1_relationship")

    # Derive typed_by from the actual model used (critical: Haiku ≠ "sonnet")
    typed_by = derive_typed_by(model)

    # confidence_tier: use the model-emitted tier if provided, else fall back to 1
    confidence_tier = model_confidence_tier if model_confidence_tier in (1, 2, 3) else 1

    row: dict = {
        "decision": "emit_edge",
        "candidate_kind": candidate_kind,
        "edge_type": edge_type,
        "source_slug": tail_row["source_slug"],
        "source_resolution_status": "tail-llm",
        "target_slug": tail_row["target_slug"],
        "target_resolution_status": "tail-llm",
        "evidence_kind": tail_row.get("evidence_kind", "book-pass1"),
        "evidence_book": evidence_book,
        "evidence_chapter": chapter,
        "evidence_section": tail_row.get("evidence_section", "Relationships Observed"),
        "evidence_quote": tail_row.get("evidence_quote", ""),
        "evidence_ref": tail_row.get("evidence_ref", ""),
        "asserted_relation": tail_row.get("hint_raw", ""),
        "hint_raw": tail_row.get("hint_raw", ""),
        "extraction_file": f"extractions/mechanical/{evidence_book}/{chapter}.extraction.md" if evidence_book and chapter else "",
        "confidence_tier": confidence_tier,
        "typed_by": typed_by,
        "corroborates_known_edge": tail_row.get("corroborates_known_edge", False),
        "wiki_edge_type": tail_row.get("wiki_edge_type"),
        "locate_status": tail_row.get("locate_status", "verbatim"),
        "run_id": run_id,
        "schema_version": "pass1-derived-v1",
        "produced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if qualifier:
        row["qualifier"] = qualifier
    return row


def build_rejected_row(tail_row: dict, run_id: str) -> dict:
    """Build a rejected row carrying the original tail data."""
    return {
        "decision": "rejected",
        "source_slug": tail_row["source_slug"],
        "target_slug": tail_row["target_slug"],
        "hint_raw": tail_row.get("hint_raw", ""),
        "evidence_chapter": tail_row.get("evidence_chapter", ""),
        "evidence_quote": tail_row.get("evidence_quote", ""),
        "run_id": run_id,
        "schema_version": "pass1-derived-v1",
        "produced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def build_needs_qualifier_row(
    tail_row: dict,
    edge_type: str,
    run_id: str,
) -> dict:
    """Build a needs-qualifier row for Tier-1 types missing a qualifier."""
    return {
        "decision": "needs_qualifier",
        "edge_type": edge_type,
        "source_slug": tail_row["source_slug"],
        "target_slug": tail_row["target_slug"],
        "hint_raw": tail_row.get("hint_raw", ""),
        "evidence_chapter": tail_row.get("evidence_chapter", ""),
        "evidence_quote": tail_row.get("evidence_quote", ""),
        "run_id": run_id,
        "schema_version": "pass1-derived-v1",
        "produced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def build_classify_failed_row(
    tail_row: dict,
    reason: str,
    run_id: str,
) -> dict:
    """Build a classify_failed row."""
    return {
        "decision": "classify_failed",
        "source_slug": tail_row["source_slug"],
        "target_slug": tail_row["target_slug"],
        "hint_raw": tail_row.get("hint_raw", ""),
        "evidence_chapter": tail_row.get("evidence_chapter", ""),
        "reason": reason,
        "run_id": run_id,
        "schema_version": "pass1-derived-v1",
        "produced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------------------
# Per-chapter file output key (for skip-existing)
# ---------------------------------------------------------------------------

def row_skip_key(row: dict) -> tuple[str, str, str]:
    """Return (source_slug, target_slug, evidence_chapter) as dedup key."""
    return (row["source_slug"], row["target_slug"], row.get("evidence_chapter", ""))


# ---------------------------------------------------------------------------
# Load tail rows
# ---------------------------------------------------------------------------

def load_tail_rows(
    books: list[str],
    smoke: int | None = None,
) -> list[dict]:
    """Load all tail rows from _tail/{book}/*.tail.jsonl.

    Each row is augmented with its originating book (field 'tail_book').
    If smoke is set, return only the first N rows across all books.
    """
    rows: list[dict] = []
    for book in books:
        book_dir = TAIL_DIR / book
        if not book_dir.exists():
            print(f"  WARNING: tail dir not found: {book_dir}", file=sys.stderr)
            continue
        for tail_file in sorted(book_dir.glob("*.tail.jsonl")):
            for line in tail_file.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    row["_tail_book"] = book
                    row["_tail_file"] = str(tail_file.relative_to(REPO))
                    rows.append(row)
                except json.JSONDecodeError as exc:
                    print(f"  WARNING: JSON parse error in {tail_file}: {exc}", file=sys.stderr)
            if smoke is not None and len(rows) >= smoke:
                return rows[:smoke]
    if smoke is not None:
        return rows[:smoke]
    return rows


# ---------------------------------------------------------------------------
# Load from _extra-tables/ directory (Task 3)
# ---------------------------------------------------------------------------

def load_extra_tables_rows(
    input_dir: Path,
    books: list[str],
    candidate_kinds: list[str] | None = None,
) -> list[dict]:
    """Load untyped candidate rows from an _extra-tables/-style directory.

    Reads all *.extra-tables.jsonl files under input_dir/{book}/.
    Filters to rows where edge_type is None (untyped candidates).
    If candidate_kinds is non-empty, further filters to matching candidate_kind values.

    Each row is augmented with '_tail_book' and '_tail_file' for consistency
    with the existing load_tail_rows() schema.

    Returns list of row dicts.
    """
    rows: list[dict] = []
    kinds_set: set[str] | None = set(candidate_kinds) if candidate_kinds else None

    for book in books:
        book_dir = input_dir / book
        if not book_dir.exists():
            continue
        for jsonl_file in sorted(book_dir.glob("*.extra-tables.jsonl")):
            for line in jsonl_file.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    print(f"  WARNING: JSON parse error in {jsonl_file}: {exc}", file=sys.stderr)
                    continue
                # Only include untyped candidates (edge_type is null/None)
                if row.get("edge_type") is not None:
                    continue
                # Filter by candidate_kinds if specified
                if kinds_set is not None:
                    if row.get("candidate_kind") not in kinds_set:
                        continue
                row["_tail_book"] = book
                try:
                    row["_tail_file"] = str(jsonl_file.relative_to(REPO))
                except ValueError:
                    row["_tail_file"] = str(jsonl_file)
                # Normalize field names for the classifier prompt:
                # extra-tables rows use evidence_chapter directly (same as tail rows)
                rows.append(row)

    return rows


def stratified_sample(
    rows: list[dict],
    n: int,
    strat_keys: tuple[str, ...] = ("_tail_book", "candidate_kind"),
    seed: int = 42,
) -> list[dict]:
    """Return a stratified random sample of at most n rows.

    Stratification is by the combination of strat_keys (e.g. book + candidate_kind).
    Allocation is proportional: each stratum gets floor(n * stratum_size / total) rows,
    with remainders filled by the largest strata until n is reached.

    If total rows <= n, returns all rows (shuffled).
    """
    if len(rows) <= n:
        rng = random.Random(seed)
        result = list(rows)
        rng.shuffle(result)
        return result

    rng = random.Random(seed)

    # Group rows by stratum key
    strata: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(k, "") for k in strat_keys)
        strata[key].append(row)

    total = len(rows)
    # Compute allocation per stratum
    allocations: dict[tuple, int] = {}
    remainders: list[tuple[float, tuple]] = []
    allocated_total = 0
    for key, stratum_rows in strata.items():
        exact = n * len(stratum_rows) / total
        floor_val = int(exact)
        allocations[key] = floor_val
        allocated_total += floor_val
        remainders.append((exact - floor_val, key))

    # Distribute remaining slots to strata with largest fractional parts
    remainder_needed = n - allocated_total
    remainders.sort(key=lambda x: -x[0])
    for i in range(remainder_needed):
        allocations[remainders[i][1]] += 1

    # Sample from each stratum
    result: list[dict] = []
    for key, count in allocations.items():
        stratum = list(strata[key])
        rng.shuffle(stratum)
        result.extend(stratum[:count])

    rng.shuffle(result)
    return result


# ---------------------------------------------------------------------------
# Load already-typed keys (for --skip-existing)
# ---------------------------------------------------------------------------

def load_existing_keys(books: list[str]) -> set[tuple[str, str, str]]:
    """Return the set of (source_slug, target_slug, evidence_chapter) already in _tail-typed/."""
    existing: set[tuple[str, str, str]] = set()
    for book in books:
        book_out_dir = OUT_BASE / book
        if not book_out_dir.exists():
            continue
        for edges_file in book_out_dir.glob("*.edges.jsonl"):
            for line in edges_file.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    key = (
                        row.get("source_slug", ""),
                        row.get("target_slug", ""),
                        row.get("evidence_chapter", ""),
                    )
                    existing.add(key)
                except json.JSONDecodeError:
                    pass
        for rejected_file in book_out_dir.glob("*.rejected.jsonl"):
            for line in rejected_file.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    key = (
                        row.get("source_slug", ""),
                        row.get("target_slug", ""),
                        row.get("evidence_chapter", ""),
                    )
                    existing.add(key)
                except json.JSONDecodeError:
                    pass
    return existing


# ---------------------------------------------------------------------------
# Process one batch of rows
# ---------------------------------------------------------------------------

def process_batch(
    batch: list[dict],
    batch_idx: int,
    locked_vocab: frozenset[str],
    tier1_types: frozenset[str],
    model: str,
    run_id: str,
    apply: bool,
    gated_types: tuple[str, ...] | None = None,
) -> dict:
    """Classify one batch via claude -p.  Returns a results dict.

    In dry-run mode (apply=False), skips the actual API call and returns
    a mock result.

    Result keys: typed, rejected, classify_failed, needs_qualifier,
    total_cost_usd, conform_violations, rows_in.

    gated_types: optional tuple of edge types to annotate as [GATED] in the
    vocab block (Rule 9 anti-pattern gate).
    """
    prompt = render_classify_prompt(batch, locked_vocab, gated_types=gated_types)
    rows_in = len(batch)

    if not apply:
        return {
            "batch_idx": batch_idx,
            "rows_in": rows_in,
            "typed": 0,
            "rejected": 0,
            "classify_failed": 0,
            "needs_qualifier": 0,
            "conform_violations": 0,
            "total_cost_usd": 0.0,
            "prompt": prompt,  # include prompt for dry-run inspection
            "emit_rows": [],
            "rejected_rows": [],
            "failed_rows": [],
            "needs_qualifier_rows": [],
        }

    result = invoke_claude(prompt, model)
    total_cost_usd = result["total_cost_usd"]

    parsed_objects, parse_error = parse_batch_response(
        result["raw_output"], rows_in
    )

    emit_rows: list[dict] = []
    rejected_rows: list[dict] = []
    failed_rows: list[dict] = []
    needs_qualifier_rows: list[dict] = []
    conform_violations = 0

    if parse_error:
        # Entire batch failed
        print(f"  [batch {batch_idx}] Parse error: {parse_error}", file=sys.stderr)
        for tail_row in batch:
            failed_rows.append(build_classify_failed_row(tail_row, f"parse_error: {parse_error}", run_id))
    else:
        aligned = align_batch_output(parsed_objects, batch)

        for row_idx, tail_row in enumerate(batch):
            obj = aligned.get(row_idx)
            if obj is None:
                # idx missing or duplicated → classify_failed
                reason = "idx missing or duplicated in model output"
                failed_rows.append(build_classify_failed_row(tail_row, reason, run_id))
                conform_violations += 1
                continue

            edge_type = str(obj.get("edge_type", "")).strip()
            qualifier = obj.get("qualifier")
            if qualifier is not None:
                qualifier = str(qualifier).strip() or None

            # Extract confidence_tier from model output (Rule 10)
            raw_tier = obj.get("confidence_tier")
            model_confidence_tier: int | None = None
            if isinstance(raw_tier, int) and raw_tier in (1, 2, 3):
                model_confidence_tier = raw_tier
            elif isinstance(raw_tier, str):
                try:
                    t = int(raw_tier)
                    if t in (1, 2, 3):
                        model_confidence_tier = t
                except ValueError:
                    pass

            decision, conform_error = conform_edge_type(
                edge_type, locked_vocab, tier1_types, qualifier
            )

            if decision == "rejected":
                rejected_rows.append(build_rejected_row(tail_row, run_id))

            elif decision == "classify_failed":
                conform_violations += 1
                failed_rows.append(build_classify_failed_row(
                    tail_row, conform_error or "conform failed", run_id
                ))

            elif decision == "needs_qualifier":
                needs_qualifier_rows.append(build_needs_qualifier_row(
                    tail_row, edge_type, run_id
                ))

            else:  # emit_edge
                emit_rows.append(build_emit_edge_row(
                    tail_row, edge_type, qualifier, model, run_id,
                    model_confidence_tier=model_confidence_tier,
                ))

    return {
        "batch_idx": batch_idx,
        "rows_in": rows_in,
        "typed": len(emit_rows),
        "rejected": len(rejected_rows),
        "classify_failed": len(failed_rows),
        "needs_qualifier": len(needs_qualifier_rows),
        "conform_violations": conform_violations,
        "total_cost_usd": total_cost_usd,
        "emit_rows": emit_rows,
        "rejected_rows": rejected_rows,
        "failed_rows": failed_rows,
        "needs_qualifier_rows": needs_qualifier_rows,
    }


# ---------------------------------------------------------------------------
# Output writing
# ---------------------------------------------------------------------------

def write_output_rows(
    emit_rows: list[dict],
    rejected_rows: list[dict],
    failed_rows: list[dict],
    needs_qualifier_rows: list[dict],
    books: list[str],
) -> None:
    """Write classified rows to _tail-typed/{book}/ and _tail-needs-qualifier/{book}/."""

    def _book_from_chapter(chapter: str) -> str:
        return chapter.split("-")[0] if chapter else "unknown"

    # Group rows by book
    def _group_by_book(rows: list[dict], chapter_field: str = "evidence_chapter") -> dict[str, list[dict]]:
        grouped: dict[str, list[dict]] = {}
        for row in rows:
            book = _book_from_chapter(row.get(chapter_field, ""))
            grouped.setdefault(book, []).append(row)
        return grouped

    emit_by_book = _group_by_book(emit_rows)
    rejected_by_book = _group_by_book(rejected_rows)
    failed_by_book = _group_by_book(failed_rows)
    needs_qual_by_book = _group_by_book(needs_qualifier_rows)

    # Write emit_edge rows
    for book, rows in emit_by_book.items():
        out_dir = OUT_BASE / book
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{book}-tail.edges.jsonl"
        with open(out_file, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Write rejected rows
    for book, rows in rejected_by_book.items():
        out_dir = OUT_BASE / book
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{book}-tail.rejected.jsonl"
        with open(out_file, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Write classify_failed rows (alongside the edges files)
    for book, rows in failed_by_book.items():
        out_dir = OUT_BASE / book
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{book}-tail.classify_failed.jsonl"
        with open(out_file, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Write needs-qualifier rows to separate dir
    for book, rows in needs_qual_by_book.items():
        out_dir = OUT_NEEDS_QUAL_DIR / book
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{book}-tail.needs-qualifier.jsonl"
        with open(out_file, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="LLM tail classifier for Stage 4 Pass-1-derived edges.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Render plan + first batch prompt; spend $0 (default when no --apply)",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Call claude -p and write output files",
    )
    parser.add_argument(
        "--book",
        choices=BOOKS,
        default=None,
        metavar="BOOK",
        help="Process only one book (agot|acok|asos|affc|adwd)",
    )
    parser.add_argument(
        "--smoke",
        type=int,
        default=None,
        metavar="N",
        help="Process only first N tail rows across all books (sequential, not stratified)",
    )
    parser.add_argument(
        "--sample-n",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Select a stratified random sample of N rows (across books AND candidate_kinds) "
            "before classifying. Use this for smoke runs over --input-dir, e.g. --sample-n 200. "
            "Mutually exclusive with --smoke in effect (if both given, --sample-n runs first)."
        ),
    )
    parser.add_argument(
        "--input-dir",
        default=None,
        metavar="DIR",
        help=(
            "Read candidate rows from this directory tree instead of the default _tail/ dir. "
            "Expected layout: DIR/{book}/*.jsonl. "
            "Only rows with edge_type==null are loaded. "
            f"Default: {TAIL_DIR.relative_to(REPO)}"
        ),
    )
    parser.add_argument(
        "--candidate-kinds",
        default=None,
        metavar="KINDS",
        help=(
            "Comma-separated list of candidate_kind values to include when reading from "
            "--input-dir (e.g. pass1_dialogue,pass1_events,pass1_info,pass1_food). "
            "If omitted, all untyped rows from --input-dir are included."
        ),
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        metavar="MODEL",
        help=f"claude -p model (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        metavar="N",
        help=f"Rows per claude -p call (default: {DEFAULT_CHUNK_SIZE})",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip rows whose (source, target, chapter) is already in _tail-typed/",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        metavar="DIR",
        help=(
            "Write typed edges / rejected / classify_failed / run-summary to this dir "
            "instead of the canonical _tail-typed/. needs-qualifier rows go to "
            "DIR/_needs-qualifier/. Use this for SMOKE runs so they never touch the "
            f"canonical typed-tail set. Default: {OUT_BASE.relative_to(REPO)}"
        ),
    )
    parser.add_argument(
        "--gate-vocab",
        default=",".join(DEFAULT_GATED_TYPES),
        metavar="TYPES",
        help=(
            "Comma-separated list of edge types to gate with Rule 9 anti-pattern guidance. "
            "Gated types remain available in the vocabulary (blocklist, NOT narrow allow-list) "
            "but are annotated [GATED] in the prompt to trigger strict usage checks. "
            f"Default: {','.join(DEFAULT_GATED_TYPES)}"
        ),
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()

    # Bare invocation = dry-run
    apply = args.apply

    # --output-dir: redirect ALL writes away from the canonical _tail-typed/.
    # Reassign module globals; write_output_rows + run-summary + mkdir look these
    # up at call time, so this covers every write path. Used for smoke runs.
    global OUT_BASE, OUT_NEEDS_QUAL_DIR
    if args.output_dir:
        OUT_BASE = Path(args.output_dir).resolve()
        OUT_NEEDS_QUAL_DIR = OUT_BASE / "_needs-qualifier"
        print(f"  Output dir: {OUT_BASE} (redirected from canonical _tail-typed/)")

    print("Weirwood Network — Stage 4 Tail Classifier")
    print(f"  Model:      {args.model}")
    print(f"  Chunk size: {args.chunk_size}")
    print(f"  Mode:       {'--apply' if apply else '--dry-run'}")
    if args.book:
        print(f"  Book:       {args.book}")
    if args.smoke is not None:
        print(f"  Smoke:      {args.smoke} rows (sequential)")
    if args.sample_n is not None:
        print(f"  Sample-N:   {args.sample_n} rows (stratified)")
    if args.input_dir:
        print(f"  Input dir:  {args.input_dir}")
    if args.candidate_kinds:
        print(f"  Kinds:      {args.candidate_kinds}")

    # Parse --gate-vocab
    gated_types: tuple[str, ...] = tuple(
        t.strip().upper() for t in args.gate_vocab.split(",") if t.strip()
    ) if args.gate_vocab else ()
    if gated_types:
        print(f"  Gate-vocab: {', '.join(gated_types)}")
    print()

    # Load vocab
    print("Loading locked vocab + Tier-1 set...")
    locked_vocab = load_locked_vocab(ARCH_MD)
    tier1_types = load_tier1_edge_types(QUAL_VOCAB_MD)
    print(f"  Locked vocab: {len(locked_vocab)} edge types")
    print(f"  Tier-1 types: {len(tier1_types)}: {sorted(tier1_types)}")
    print()

    # Pre-warm display name cache
    print("Building display name cache from graph/nodes/...")
    global _CACHED_DISPLAY_NAMES
    _CACHED_DISPLAY_NAMES = build_display_name_map(locked_vocab)
    print(f"  {len(_CACHED_DISPLAY_NAMES)} slug → display name entries")
    print()

    # Load tail rows — from default _tail/ or from --input-dir
    books = [args.book] if args.book else BOOKS

    if args.input_dir:
        input_dir = Path(args.input_dir)
        candidate_kinds = (
            [k.strip() for k in args.candidate_kinds.split(",") if k.strip()]
            if args.candidate_kinds
            else None
        )
        print(f"Loading extra-tables rows from {input_dir} ...")
        all_rows = load_extra_tables_rows(input_dir, books, candidate_kinds=candidate_kinds)
        print(f"  {len(all_rows)} untyped rows loaded")
    else:
        print(f"Loading tail rows from {TAIL_DIR} ...")
        all_rows = load_tail_rows(books, smoke=args.smoke)
        print(f"  {len(all_rows)} rows loaded")

    # --sample-n: stratified sample (runs before --smoke sequential truncation)
    if args.sample_n is not None and len(all_rows) > args.sample_n:
        print(f"Stratified sampling: {args.sample_n} rows from {len(all_rows)} ...")
        all_rows = stratified_sample(all_rows, args.sample_n)
        print(f"  {len(all_rows)} rows after stratified sample")

    # --smoke (sequential truncation, for backward compat with existing usage)
    if args.smoke is not None and args.input_dir is None:
        # Already handled by load_tail_rows; no-op here
        pass

    # Skip-existing filter
    if args.skip_existing and all_rows:
        print("Checking for existing output (--skip-existing)...")
        existing_keys = load_existing_keys(books)
        before = len(all_rows)
        all_rows = [r for r in all_rows if row_skip_key(r) not in existing_keys]
        skipped = before - len(all_rows)
        print(f"  Skipped {skipped} already-typed rows; {len(all_rows)} remaining")
    print()

    if not all_rows:
        print("No rows to process. Done.")
        return 0

    # Chunk plan
    chunk_size = args.chunk_size
    chunks = [all_rows[i : i + chunk_size] for i in range(0, len(all_rows), chunk_size)]
    print(f"Batch plan: {len(all_rows)} rows → {len(chunks)} batches of ≤{chunk_size}")
    print()

    if not apply:
        # Dry-run: print first batch prompt
        print("=== DRY-RUN PLAN ===")
        print(f"  rows_in:      {len(all_rows)}")
        print(f"  batch_count:  {len(chunks)}")
        print(f"  chunk_size:   {chunk_size}")
        print(f"  model:        {args.model}")
        print()
        if chunks:
            print(f"--- First batch prompt ({len(chunks[0])} rows) ---")
            prompt = render_classify_prompt(chunks[0], locked_vocab, gated_types=gated_types)
            print(prompt)
            print("--- End of first batch prompt ---")
        return 0

    # === APPLY MODE ===
    run_id = f"tail-llm-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    print(f"Run ID: {run_id}")
    print()

    # Create output dirs
    for book in books:
        (OUT_BASE / book).mkdir(parents=True, exist_ok=True)
        (OUT_NEEDS_QUAL_DIR / book).mkdir(parents=True, exist_ok=True)

    total_typed = 0
    total_rejected = 0
    total_classify_failed = 0
    total_needs_qualifier = 0
    total_conform_violations = 0
    total_cost_usd = 0.0

    all_emit_rows: list[dict] = []
    all_rejected_rows: list[dict] = []
    all_failed_rows: list[dict] = []
    all_needs_qualifier_rows: list[dict] = []

    for batch_idx, batch in enumerate(chunks):
        print(f"  Batch {batch_idx + 1}/{len(chunks)} ({len(batch)} rows)...", end=" ", flush=True)
        t0 = time.monotonic()

        result = process_batch(
            batch=batch,
            batch_idx=batch_idx,
            locked_vocab=locked_vocab,
            tier1_types=tier1_types,
            model=args.model,
            run_id=run_id,
            apply=True,
            gated_types=gated_types,
        )

        elapsed = round(time.monotonic() - t0, 1)
        print(
            f"typed={result['typed']} rejected={result['rejected']} "
            f"failed={result['classify_failed']} nq={result['needs_qualifier']} "
            f"cost=${result['total_cost_usd']:.4f} ({elapsed}s)"
        )

        total_typed += result["typed"]
        total_rejected += result["rejected"]
        total_classify_failed += result["classify_failed"]
        total_needs_qualifier += result["needs_qualifier"]
        total_conform_violations += result["conform_violations"]
        total_cost_usd += result["total_cost_usd"]

        all_emit_rows.extend(result["emit_rows"])
        all_rejected_rows.extend(result["rejected_rows"])
        all_failed_rows.extend(result["failed_rows"])
        all_needs_qualifier_rows.extend(result["needs_qualifier_rows"])

    # Write output files
    print()
    print("Writing output files...")
    write_output_rows(
        all_emit_rows,
        all_rejected_rows,
        all_failed_rows,
        all_needs_qualifier_rows,
        books,
    )

    # Write run-summary
    summary = {
        "run_id": run_id,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": args.model,
        "chunk_size": chunk_size,
        "books": books,
        "smoke": args.smoke,
        "rows_in": len(all_rows),
        "batches": len(chunks),
        "typed": total_typed,
        "rejected": total_rejected,
        "classify_failed": total_classify_failed,
        "needs_qualifier": total_needs_qualifier,
        "conform_violations": total_conform_violations,
        "total_cost_usd": round(total_cost_usd, 6),
    }
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    summary_path = OUT_BASE / "run-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    print()
    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"  rows_in:           {len(all_rows)}")
    print(f"  typed (emit_edge): {total_typed}")
    print(f"  rejected:          {total_rejected}")
    print(f"  classify_failed:   {total_classify_failed}")
    print(f"  needs_qualifier:   {total_needs_qualifier}")
    print(f"  conform_violations:{total_conform_violations}")
    print(f"  total_cost_usd:    ${total_cost_usd:.4f}")
    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO))
        except ValueError:
            return str(p)
    print(f"  output dir:        {_rel(OUT_BASE)}")
    print(f"  needs-qual dir:    {_rel(OUT_NEEDS_QUAL_DIR)}")
    print(f"  run summary:       {_rel(summary_path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
