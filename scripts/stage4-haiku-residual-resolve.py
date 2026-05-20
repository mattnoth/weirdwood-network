#!/usr/bin/env python3
"""
Stage 4 Haiku — residual-resolution pass (STEP 2 of the no-silent-drop pipeline).

Takes every `stage=normalizer-residual` row from the unresolved-edges-log and gets
a second Haiku pass to either map it to a canonical edge type or reject it. Then
deterministically applies the result to the .edges.jsonl files.

Three phases:
  Phase 1 — gather (pure Python): read the log, locate matching rows in .edges.jsonl files.
  Phase 2 — classify (one Haiku call): inline the locked 164-type vocab + residual rows;
             Haiku returns map/reject/escalate per row.
  Phase 3 — apply (pure Python, atomic): rewrite .edges.jsonl files; append escalations
             to the unresolved log.

HARD CONSTRAINTS:
  - Touches ONLY prose-edges-haiku/ files and the Haiku mission dir.
  - NEVER reads or writes the Sonnet mission dir or prose-edges/ (non-haiku) directories.

Usage:
    # Dry run — gather + render prompt, print what WOULD happen, no Haiku call, no writes:
    python3 scripts/stage4-haiku-residual-resolve.py --dry-run

    # Live run (requires explicit authorization):
    python3 scripts/stage4-haiku-residual-resolve.py

    # Custom log path:
    python3 scripts/stage4-haiku-residual-resolve.py \\
        --log working/missions/2026-05-19-stage4-haiku/unresolved-edges-log.jsonl

    # Custom model:
    python3 scripts/stage4-haiku-residual-resolve.py --model claude-haiku-4-5
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent

HAIKU_MISSION = REPO / "working/missions/2026-05-19-stage4-haiku"
DEFAULT_LOG = HAIKU_MISSION / "unresolved-edges-log.jsonl"
LOCKED_VOCAB = HAIKU_MISSION / "locked-edge-vocab-159.md"
ARCH_PATH = REPO / "reference/architecture.md"

# Output files written by this script (all within the Haiku mission dir)
HAIKU_DECISIONS_FILE = HAIKU_MISSION / "residual-haiku-decisions.jsonl"
RESOLUTIONS_AUDIT = HAIKU_MISSION / "residual-resolutions.jsonl"
RESIDUAL_RUN_LOG = HAIKU_MISSION / "run-logs"

# Forbidden path substrings — never touch these
FORBIDDEN_PATH_SUBSTRS = [
    "2026-05-14-stage4-v1-bulk-sonnet",
    "/prose-edges/",    # non-haiku Sonnet output dirs
]

# Only the normalizer-residual stage rows are our input
TARGET_STAGE = "normalizer-residual"

# The stage name we append when escalating from THIS script
OUTPUT_ESCALATE_STAGE = "haiku-residual"

# ---------------------------------------------------------------------------
# Safety guard
# ---------------------------------------------------------------------------

def _is_forbidden(path: str) -> bool:
    """Return True if the path touches a forbidden location."""
    for substr in FORBIDDEN_PATH_SUBSTRS:
        if substr in path:
            # Exception: /prose-edges-haiku/ is allowed
            if substr == "/prose-edges/" and "/prose-edges-haiku/" in path:
                continue
            return True
    return False


def _assert_safe(path: str, context: str = "") -> None:
    """Raise RuntimeError if path is forbidden."""
    if _is_forbidden(path):
        raise RuntimeError(
            f"SAFETY VIOLATION{' (' + context + ')' if context else ''}: "
            f"would touch forbidden path: {path}"
        )


# ---------------------------------------------------------------------------
# Import normalizer helpers (importlib — filename has hyphens)
# ---------------------------------------------------------------------------

def _load_normalizer_module():
    """Load stage4-haiku-normalize-edge-types.py via importlib."""
    norm_path = REPO / "scripts" / "stage4-haiku-normalize-edge-types.py"
    spec = importlib.util.spec_from_file_location(
        "stage4_haiku_normalize_edge_types", norm_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_validator_module():
    """Load wiki-pass2-validate-edge-jsonl.py via importlib."""
    validator_path = REPO / "scripts" / "wiki-pass2-validate-edge-jsonl.py"
    spec = importlib.util.spec_from_file_location(
        "wiki_pass2_validate_edge_jsonl", validator_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Canonical vocab loader
# ---------------------------------------------------------------------------

def load_canonical_vocab() -> frozenset[str]:
    """Load the 164 canonical edge types from architecture.md via the validator."""
    validator = _load_validator_module()
    return frozenset(validator.load_canonical_vocab(ARCH_PATH))


# ---------------------------------------------------------------------------
# Locked vocab body (for inlining into the Haiku prompt)
# ---------------------------------------------------------------------------

def load_locked_vocab_body() -> str:
    """Read locked-edge-vocab-159.md, strip the admin header, return the entry list."""
    if not LOCKED_VOCAB.exists():
        sys.exit(
            f"ERROR: locked vocab file not found: {LOCKED_VOCAB}\n"
            "Regenerate: python3 scripts/stage4-haiku-normalize-edge-types.py "
            f"--dump-vocab {LOCKED_VOCAB}"
        )
    text = LOCKED_VOCAB.read_text(encoding="utf-8")
    # Drop everything up to and including the first horizontal rule (---),
    # matching the same stripping logic in stage4-haiku-run.py load_locked_vocab().
    body = text.split("\n---\n", 1)[-1].strip()
    return body


# ---------------------------------------------------------------------------
# Phase 1 — gather
# ---------------------------------------------------------------------------

def read_log(log_path: Path) -> list[dict]:
    """Read the unresolved-edges-log and return all rows."""
    if not log_path.exists():
        return []
    rows = []
    with log_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def select_residual_rows(log_rows: list[dict]) -> list[dict]:
    """Select normalizer-residual rows, deduped on the 5-tuple key."""
    seen: set[tuple] = set()
    out: list[dict] = []
    for row in log_rows:
        if row.get("stage") != TARGET_STAGE:
            continue
        key = (
            row.get("file", ""),
            row.get("source_slug", ""),
            row.get("target_slug", ""),
            row.get("raw_edge_type", ""),
            row.get("stage", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def locate_edge_row(
    file_path: Path,
    source_slug: str,
    target_slug: str,
    raw_edge_type: str,
    is_missing_field: bool,
) -> Optional[tuple[int, dict]]:
    """Find the matching emit_edge row in the .edges.jsonl file.

    For is_missing_field=True: match on slugs only, require edge_type ABSENT.
    For is_missing_field=False: match on slugs AND edge_type == raw_edge_type.

    Returns (line_number, row_dict) on success, None if not found.
    """
    if not file_path.exists():
        return None

    with file_path.open(encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, 1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue

            if row.get("decision") != "emit_edge":
                continue
            if row.get("source_slug") != source_slug:
                continue
            if row.get("target_slug") != target_slug:
                continue

            if is_missing_field:
                # Match: edge_type must be absent
                if "edge_type" not in row:
                    return (line_no, row)
            else:
                # Match: edge_type must equal raw_edge_type
                if row.get("edge_type") == raw_edge_type:
                    return (line_no, row)

    return None


class GatheredResidual:
    """One gathered residual row + its located edge row."""
    def __init__(
        self,
        log_row: dict,
        idx: int,
        located_line_no: int,
        located_row: dict,
        is_missing_field: bool,
    ):
        self.log_row = log_row
        self.idx = idx                          # 1-based index for Haiku prompt
        self.located_line_no = located_line_no
        self.located_row = located_row
        self.is_missing_field = is_missing_field

    @property
    def file_path(self) -> Path:
        return Path(self.log_row["file"])

    @property
    def source_slug(self) -> str:
        return self.log_row.get("source_slug", "")

    @property
    def target_slug(self) -> str:
        return self.log_row.get("target_slug", "")

    @property
    def raw_edge_type(self) -> str:
        return self.log_row.get("raw_edge_type", "")

    @property
    def evidence_snippet(self) -> str:
        return self.log_row.get("evidence_snippet", "")

    @property
    def log_reason(self) -> str:
        return self.log_row.get("reason", "")


def gather_residuals(
    residual_log_rows: list[dict],
    canonical: frozenset[str],
) -> tuple[list[GatheredResidual], list[dict]]:
    """Phase 1: locate each residual row in its .edges.jsonl file.

    Returns (gathered_list, skipped_list).
    skipped_list entries have keys: log_row, reason ('not-found' | 'already-resolved' | 'forbidden-path').
    """
    gathered: list[GatheredResidual] = []
    skipped: list[dict] = []
    idx = 1

    for log_row in residual_log_rows:
        file_str = log_row.get("file", "")
        source_slug = log_row.get("source_slug", "")
        target_slug = log_row.get("target_slug", "")
        raw_edge_type = log_row.get("raw_edge_type", "")
        log_reason = log_row.get("reason", "")

        # Safety: never touch forbidden paths
        if _is_forbidden(file_str):
            print(
                f"  WARNING: skipping forbidden path: {file_str}",
                file=sys.stderr,
            )
            skipped.append({"log_row": log_row, "reason": "forbidden-path"})
            continue

        file_path = Path(file_str)
        is_missing_field = (raw_edge_type == "<missing>" or log_reason == "missing-edge-type-field")

        result = locate_edge_row(
            file_path, source_slug, target_slug, raw_edge_type, is_missing_field
        )

        if result is None:
            # No matching row found — either already resolved or file changed
            skipped.append({"log_row": log_row, "reason": "not-found"})
            continue

        line_no, row = result

        # Staleness/idempotency guard: if row already has a canonical edge_type, skip
        if not is_missing_field:
            current_et = row.get("edge_type", "")
            if current_et in canonical:
                skipped.append({"log_row": log_row, "reason": "already-resolved"})
                continue

        gathered.append(GatheredResidual(
            log_row=log_row,
            idx=idx,
            located_line_no=line_no,
            located_row=row,
            is_missing_field=is_missing_field,
        ))
        idx += 1

    return gathered, skipped


# ---------------------------------------------------------------------------
# Phase 2 — classify (Haiku)
# ---------------------------------------------------------------------------

DIRECTION_GUIDANCE = """
## Direction-Guidance for Edge Orientation

The canonical vocabulary's *Source → Target* annotation tells you which entity goes
on which side. When mapping a raw invented type, you MUST pick `swap` correctly:

- **`WARD_OF`**: *Ward → Guardian* (the ward is the source, the guardian is the target).
  - Haiku emitted `FOSTERED_BY` (Guardian → Ward direction) → map to `WARD_OF` with `swap: true`
    so the guardian becomes the target and the ward becomes the source.
  - Haiku emitted `FOSTERED_BY_INVERSE` (Ward → Guardian? or the inverse of FOSTERED_BY)
    → evaluate carefully; if source is the ward and target is the guardian, map to `WARD_OF`
    with `swap: false`; otherwise `swap: true`.

For every row: restate the edge as a plain English sentence first
(e.g. "Rorge raised Biter"), then check whether the canonical direction matches.
Set `swap: true` if the sentence runs opposite to the canonical *Source → Target* shown
in the vocab entry.

If no canonical type fits, use `reject`. If genuinely uncertain, use `escalate`.
"""


def build_haiku_prompt(
    gathered: list[GatheredResidual],
    vocab_body: str,
) -> str:
    """Build the full Haiku prompt for the residual-resolution pass."""
    rows_text_parts = []
    for g in gathered:
        missing_note = " [MISSING EDGE_TYPE FIELD — row has no edge_type key]" if g.is_missing_field else ""
        rows_text_parts.append(
            f"Row {g.idx}:\n"
            f"  source_slug: {g.source_slug}\n"
            f"  target_slug: {g.target_slug}\n"
            f"  raw_edge_type: {g.raw_edge_type}{missing_note}\n"
            f"  evidence_snippet: {g.evidence_snippet!r}\n"
            f"  log_reason: {g.log_reason}"
        )

    rows_block = "\n\n".join(rows_text_parts)

    prompt = f"""You are a graph-edge type classifier for an ASOIAF knowledge graph.

Your task: classify each of the {len(gathered)} residual edge rows below.
Each row was flagged by a prior normalizer pass because its edge_type is either
semantically distinct from all canonical types, or missing entirely.

## Canonical Edge-Type Vocabulary (164 types)

{vocab_body}

{DIRECTION_GUIDANCE}

## Your task

For each numbered row, choose exactly one decision:
- `map` — a canonical type from the 164-list fits the relationship. Provide:
    - `edge_type`: exact canonical spelling (UPPER_CASE_WITH_UNDERSCORES)
    - `swap`: true if source_slug and target_slug must be swapped to match the canonical
              *Source → Target* direction; false if the current order is already correct.
    - `confidence_tier`: 1 (explicit in text), 2 (strongly implied), or 3 (inferred)
    - `rationale`: brief explanation (1 sentence)
- `reject` — no canonical type fits the relationship described. Provide:
    - `rationale`: why no type fits
- `escalate` — genuinely unsure; defer to human/Opus review. Provide:
    - `rationale`: what makes this ambiguous

## Output format

Write one JSON object per row to {HAIKU_DECISIONS_FILE.name}, one per line:

{{"idx": 1, "decision": "map", "edge_type": "WARD_OF", "swap": true, "confidence_tier": 1, "rationale": "Rorge raised Biter as a ward; WARD_OF Ward→Guardian direction requires swap."}}
{{"idx": 2, "decision": "reject", "rationale": "GRANDCHILD_OF has no canonical equivalent in the vocabulary."}}
{{"idx": 3, "decision": "escalate", "rationale": "Unclear whether this is KNOWS or CONTEMPORARY_WITH."}}

Rules:
1. Output ONLY the JSON objects — no preamble, no commentary.
2. Every row must have an entry (1 through {len(gathered)}) — no omissions.
3. For `map` decisions: edge_type MUST be spelled exactly as in the vocab above.
4. For `reject`/`escalate`: omit `edge_type`, `swap`, `confidence_tier`.
5. Do NOT read any files from the repository. Everything you need is inlined above.

## Residual rows to classify

{rows_block}

Write your decisions (one JSON per line) to:
{HAIKU_DECISIONS_FILE}
"""
    return prompt


def invoke_haiku(prompt: str, model: str, log_path: Path) -> dict:
    """Call claude -p with the rendered prompt. Returns cost/status dict.

    Copied from stage4-haiku-run.py's invoke_haiku() — same invocation pattern.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "claude",
        "-p",
        "--dangerously-skip-permissions",
        "--model", model,
        "--verbose",
        "--output-format", "stream-json",
        prompt,
    ]

    total_cost_usd = 0.0
    error_message = None
    t_start = time.monotonic()

    with open(log_path, "w", encoding="utf-8") as log_fh:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for line in proc.stdout:
            log_fh.write(line)
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("type") == "result":
                    total_cost_usd = event.get("total_cost_usd", 0.0)
            except json.JSONDecodeError:
                pass

        stderr_text = proc.stderr.read()
        proc.wait()

        if proc.returncode != 0:
            error_message = (
                stderr_text.strip()[:500] if stderr_text.strip()
                else f"exit code {proc.returncode}"
            )

    duration_s = time.monotonic() - t_start

    return {
        "returncode": proc.returncode,
        "total_cost_usd": total_cost_usd,
        "error_message": error_message,
        "duration_s": round(duration_s, 2),
    }


def read_haiku_decisions(
    decisions_path: Path,
    count: int,
    run_log_path: Path | None = None,
) -> dict[int, dict]:
    """Read Haiku's output file and return {idx: decision_row}.

    If the decisions file is missing/empty or yields zero parseable rows,
    fall back to parsing the run-log's `result` event text — Haiku often
    returns the JSONL inline (in a ```json ... ``` fenced block or raw)
    rather than calling the Write tool, even when the prompt asks it to.
    """
    decisions: dict[int, dict] = {}

    def _consume_lines(text: str) -> None:
        for raw in text.splitlines():
            raw = raw.strip()
            if not raw or not raw.startswith("{"):
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            idx = row.get("idx")
            if isinstance(idx, int) and 1 <= idx <= count:
                decisions[idx] = row

    if decisions_path.exists():
        _consume_lines(decisions_path.read_text(encoding="utf-8"))

    if decisions or run_log_path is None or not run_log_path.exists():
        return decisions

    # Fallback: extract the assistant's final text from the run-log's `result`
    # event and try to parse JSONL out of it.
    result_text = ""
    with run_log_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                result_text = event.get("result") or ""
                break

    if not result_text:
        return decisions

    # Prefer a ```json fenced block if one is present.
    fence_match = re.search(r"```(?:json|jsonl)?\s*\n(.*?)```", result_text, re.DOTALL)
    if fence_match:
        _consume_lines(fence_match.group(1))
    else:
        _consume_lines(result_text)

    return decisions


# ---------------------------------------------------------------------------
# Phase 3 — apply
# ---------------------------------------------------------------------------

def _write_atomic(path: Path, lines: list[str]) -> None:
    """Write lines to path atomically (temp file + os.replace)."""
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, prefix=".tmp-residual-", suffix=".jsonl"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.writelines(lines)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _rewrite_file_for_residual(
    file_path: Path,
    rewrites: list[dict],
) -> None:
    """Apply a list of rewrite operations to a .edges.jsonl file atomically.

    Each rewrite: {line_no: int, new_row: dict}
    """
    lines_in = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    lines_out = list(lines_in)  # copy

    rewrite_by_lineno = {r["line_no"]: r["new_row"] for r in rewrites}

    for line_no_1based, new_row in rewrite_by_lineno.items():
        idx = line_no_1based - 1  # 0-based
        if 0 <= idx < len(lines_out):
            lines_out[idx] = json.dumps(new_row, ensure_ascii=False) + "\n"

    _write_atomic(file_path, lines_out)


def build_reject_row(original_row: dict, reason: str) -> dict:
    """Convert an emit_edge row to a reject_just_mention row.

    Required fields for (reject_just_mention, source_target) per validator:
      decision, candidate_kind, source_slug, target_slug, reason

    We preserve additional fields that are harmless and provide audit context:
      evidence_kind, evidence_snippet, evidence_section (optional extras, not required).
    We DROP: edge_type, confidence_tier, qualifier, evidence_paragraph_index.

    The validator only checks for REQUIRED fields being present; it does not
    reject extra fields on reject_just_mention rows (confirmed from validator source).
    We keep evidence_snippet to preserve the audit trail.
    """
    new_row: dict = {
        "decision": "reject_just_mention",
        "candidate_kind": original_row.get("candidate_kind", "source_target"),
        "source_slug": original_row.get("source_slug", ""),
        "target_slug": original_row.get("target_slug", ""),
        "reason": reason,
    }
    # Preserve optional evidence fields for audit traceability
    for field in ("evidence_kind", "evidence_snippet", "evidence_section"):
        if field in original_row:
            new_row[field] = original_row[field]
    return new_row


def apply_results(
    gathered: list[GatheredResidual],
    decisions: dict[int, dict],
    canonical: frozenset[str],
    dry_run: bool,
    log_path: Path,
    normalizer_mod,
) -> dict:
    """Phase 3: apply Haiku's decisions to the .edges.jsonl files.

    Returns a summary dict with counts and a list of per-residual audit rows.
    """
    counts = {
        "mapped": 0,
        "rejected": 0,
        "escalated": 0,
        "already_resolved": 0,
        "parse_failed": 0,
    }
    audit_rows: list[dict] = []

    # Group rewrites by file so we can do one atomic write per file
    # {file_path: [{"line_no": N, "new_row": {...}}]}
    file_rewrites: dict[Path, list[dict]] = {}

    # Escalation log rows to append
    new_log_rows: list[dict] = []
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for g in gathered:
        idx = g.idx
        decision_row = decisions.get(idx)

        # Defaults — will be overwritten per branch below
        applied: str = "escalate"
        final_reason: str = "haiku-output-unparseable"
        haiku_rationale: str = ""
        audit_canonical_et: Optional[str] = None
        audit_swap: bool = False

        if decision_row is None:
            # Haiku produced no parseable decision for this row
            haiku_rationale = "No parseable decision found in Haiku output file."
            counts["parse_failed"] += 1
        else:
            raw_decision = decision_row.get("decision", "")
            haiku_rationale = decision_row.get("rationale", "")

            if raw_decision == "map":
                proposed_et = decision_row.get("edge_type", "")

                # Validate: must be in canonical set
                if proposed_et not in canonical:
                    # Haiku invented again — downgrade to escalate
                    applied = "escalate"
                    final_reason = f"haiku-map-still-invalid-type:{proposed_et!r}"
                    haiku_rationale = (
                        haiku_rationale
                        + f" [DOWNGRADED: proposed type {proposed_et!r} not in canonical set]"
                    )
                    counts["escalated"] += 1
                    print(
                        f"  [{idx}] DOWNGRADE: {g.source_slug} --{g.raw_edge_type}--> {g.target_slug}"
                        f" | Haiku proposed {proposed_et!r} (not canonical) → escalate",
                        file=sys.stderr,
                    )
                else:
                    applied = "map"
                    final_reason = ""  # not used for map
                    swap = decision_row.get("swap", False)
                    confidence_tier = decision_row.get("confidence_tier", 2)
                    audit_canonical_et = proposed_et
                    audit_swap = swap

                    # Build the rewritten row
                    new_row = dict(g.located_row)
                    new_row["edge_type"] = proposed_et
                    new_row["confidence_tier"] = confidence_tier
                    if swap:
                        # Swap source and target slugs
                        new_row["source_slug"] = g.target_slug
                        new_row["target_slug"] = g.source_slug

                    # Queue the rewrite
                    fp = g.file_path
                    if fp not in file_rewrites:
                        file_rewrites[fp] = []
                    file_rewrites[fp].append({
                        "line_no": g.located_line_no,
                        "new_row": new_row,
                    })

                    counts["mapped"] += 1
                    swap_note = f" (swap: {g.source_slug}↔{g.target_slug})" if swap else ""
                    print(
                        f"  [{idx}] MAP: {g.source_slug} --{g.raw_edge_type}--> {g.target_slug}"
                        f" → {proposed_et}{swap_note}",
                        file=sys.stderr,
                    )

            elif raw_decision == "reject":
                applied = "reject"
                final_reason = "no-fitting-type-vocab-locked"

                # Build the reject_just_mention row
                new_row = build_reject_row(g.located_row, final_reason)

                # Queue the rewrite
                fp = g.file_path
                if fp not in file_rewrites:
                    file_rewrites[fp] = []
                file_rewrites[fp].append({
                    "line_no": g.located_line_no,
                    "new_row": new_row,
                })

                counts["rejected"] += 1
                print(
                    f"  [{idx}] REJECT: {g.source_slug} --{g.raw_edge_type}--> {g.target_slug}",
                    file=sys.stderr,
                )

            elif raw_decision == "escalate":
                applied = "escalate"
                final_reason = "haiku-escalated"
                counts["escalated"] += 1
                print(
                    f"  [{idx}] ESCALATE: {g.source_slug} --{g.raw_edge_type}--> {g.target_slug}",
                    file=sys.stderr,
                )
            else:
                # Unrecognised decision value
                applied = "escalate"
                final_reason = "haiku-output-unparseable"
                haiku_rationale = f"Unknown decision value: {raw_decision!r}"
                counts["parse_failed"] += 1

        # Build escalation log row (for escalations only)
        if applied == "escalate":
            log_row = {
                "timestamp": ts,
                "stage": OUTPUT_ESCALATE_STAGE,
                "batch_id": g.log_row.get("batch_id", ""),
                "file": str(g.file_path),
                "source_slug": g.source_slug,
                "target_slug": g.target_slug,
                "raw_edge_type": g.raw_edge_type,
                "evidence_snippet": g.evidence_snippet,
                "reason": final_reason,
                "haiku_rationale": haiku_rationale,
            }
            new_log_rows.append(log_row)

        # Build audit row
        audit_entry: dict = {
            "idx": idx,
            "source_slug": g.source_slug,
            "target_slug": g.target_slug,
            "raw_edge_type": g.raw_edge_type,
            "file": str(g.file_path),
            "applied": applied,
            "haiku_rationale": haiku_rationale,
        }
        if applied == "map" and audit_canonical_et is not None:
            audit_entry["canonical_edge_type"] = audit_canonical_et
            audit_entry["swap"] = audit_swap
        if applied in ("reject", "escalate"):
            audit_entry["reason"] = final_reason
        audit_rows.append(audit_entry)

    # -----------------------------------------------------------------------
    # Apply file rewrites (atomic, one write per file)
    # -----------------------------------------------------------------------
    if not dry_run:
        for fp, rewrites in file_rewrites.items():
            _assert_safe(str(fp), "file rewrite")
            print(f"  Writing {fp.name} ({len(rewrites)} rewrite(s))...", file=sys.stderr)
            _rewrite_file_for_residual(fp, rewrites)

        # Append escalation rows to the unresolved-edges-log
        if new_log_rows:
            existing_keys = normalizer_mod.load_existing_log_keys(log_path)
            # Filter to only truly new keys
            truly_new = []
            seen_new: set[tuple] = set()
            for row in new_log_rows:
                key = (
                    row.get("file", ""),
                    row.get("source_slug", ""),
                    row.get("target_slug", ""),
                    row.get("raw_edge_type", ""),
                    row.get("stage", ""),
                )
                if key not in existing_keys and key not in seen_new:
                    seen_new.add(key)
                    truly_new.append(row)
            appended = normalizer_mod.append_unresolved_log(log_path, truly_new, dry_run=False)
            print(f"  Appended {appended} escalation row(s) to unresolved log.", file=sys.stderr)

        # Write audit trail
        RESOLUTIONS_AUDIT.parent.mkdir(parents=True, exist_ok=True)
        with RESOLUTIONS_AUDIT.open("w", encoding="utf-8") as f:
            for row in audit_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  Audit trail written: {RESOLUTIONS_AUDIT.relative_to(REPO)}", file=sys.stderr)
    else:
        # Dry run: show what would happen
        print("\n[dry-run] Would apply the following rewrites:", file=sys.stderr)
        for fp, rewrites in file_rewrites.items():
            print(f"  {fp.relative_to(REPO)}: {len(rewrites)} rewrite(s)", file=sys.stderr)
        if new_log_rows:
            print(f"  Would append {len(new_log_rows)} escalation row(s) to unresolved log.",
                  file=sys.stderr)

    return {
        "counts": counts,
        "audit_rows": audit_rows,
        "file_rewrites_count": sum(len(v) for v in file_rewrites.values()),
        "escalation_log_rows": len(new_log_rows),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--log",
        default=str(DEFAULT_LOG),
        metavar="PATH",
        help=(
            "Path to the unresolved-edges-log.jsonl "
            f"(default: {DEFAULT_LOG.relative_to(REPO)})"
        ),
    )
    parser.add_argument(
        "--model",
        default="claude-haiku-4-5",
        metavar="MODEL",
        help="Model to invoke for residual classification (default: claude-haiku-4-5)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Phases 1 only: gather residuals, render prompt, print what WOULD be applied. "
            "Do NOT invoke Haiku. Do NOT write anything."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    log_path = Path(args.log)
    if not log_path.is_absolute():
        log_path = REPO / log_path

    print("Weirwood Network — Stage 4 Haiku Residual-Resolution Pass")
    print(f"  Log: {log_path}")
    print(f"  Model: {args.model}")
    print(f"  Dry-run: {args.dry_run}")
    print()

    # ── Load modules ──────────────────────────────────────────────────────────
    try:
        normalizer_mod = _load_normalizer_module()
    except Exception as e:
        print(f"ERROR: could not load normalizer module: {e}", file=sys.stderr)
        return 2

    try:
        canonical = load_canonical_vocab()
    except Exception as e:
        print(f"ERROR: could not load canonical vocab: {e}", file=sys.stderr)
        return 2
    print(f"Canonical vocab: {len(canonical)} types")

    # ── Phase 1: gather ───────────────────────────────────────────────────────
    print("\nPhase 1 — gather")
    all_log_rows = read_log(log_path)
    print(f"  Total log rows: {len(all_log_rows)}")

    residual_rows = select_residual_rows(all_log_rows)
    print(f"  Rows with stage={TARGET_STAGE!r}: {len(residual_rows)}")

    gathered, skipped = gather_residuals(residual_rows, canonical)
    print(f"  Located in .edges.jsonl files: {len(gathered)}")
    print(f"  Skipped (not-found / already-resolved / forbidden): {len(skipped)}")

    # Report skipped breakdown
    skip_counts: dict[str, int] = {}
    for s in skipped:
        r = s.get("reason", "unknown")
        skip_counts[r] = skip_counts.get(r, 0) + 1
    for reason, count in sorted(skip_counts.items()):
        print(f"    {reason}: {count}")

    if not gathered:
        print("\nNo residuals to resolve. Nothing to do.")
        return 0

    # ── Load locked vocab body ────────────────────────────────────────────────
    vocab_body = load_locked_vocab_body()

    # ── Build prompt ──────────────────────────────────────────────────────────
    prompt = build_haiku_prompt(gathered, vocab_body)

    if args.dry_run:
        print("\n[dry-run] Gathered residuals (no Haiku call will be made):")
        for g in gathered:
            missing_note = " [MISSING FIELD]" if g.is_missing_field else ""
            print(
                f"  [{g.idx}] {g.source_slug} --{g.raw_edge_type!r}{missing_note}--> {g.target_slug}"
                f"\n        file: {g.file_path.relative_to(REPO)}"
                f"\n        evidence: {g.evidence_snippet[:80]!r}"
            )

        print(f"\n[dry-run] Rendered prompt ({len(prompt)} chars, {len(prompt.splitlines())} lines):")
        print("  " + "-" * 72)
        # Print a truncated version — first 60 lines, then skip to last 30
        prompt_lines = prompt.splitlines()
        if len(prompt_lines) > 90:
            for line in prompt_lines[:60]:
                print(f"  {line}")
            print(f"  ... [{len(prompt_lines) - 90} lines omitted] ...")
            for line in prompt_lines[-30:]:
                print(f"  {line}")
        else:
            for line in prompt_lines:
                print(f"  {line}")
        print("  " + "-" * 72)

        print("\n[dry-run] Summary:")
        print(f"  Residuals gathered: {len(gathered)}")
        print(f"  Skipped: {len(skipped)}")
        for reason, count in sorted(skip_counts.items()):
            print(f"    {reason}: {count}")
        print("\nNo files were written. No Haiku call was made.")
        return 0

    # ── Phase 2: classify (live) ──────────────────────────────────────────────
    print("\nPhase 2 — classify (Haiku)")
    HAIKU_MISSION.mkdir(parents=True, exist_ok=True)
    RESIDUAL_RUN_LOG.mkdir(parents=True, exist_ok=True)

    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    log_out_path = RESIDUAL_RUN_LOG / f"residual-resolve-{run_ts}.jsonl"

    print(f"  Invoking {args.model}...")
    print(f"  Run log: {log_out_path.relative_to(REPO)}")
    print(f"  Decisions output: {HAIKU_DECISIONS_FILE.relative_to(REPO)}")

    invoke_result = invoke_haiku(prompt, args.model, log_out_path)
    print(f"  Done. Exit code: {invoke_result['returncode']}, "
          f"cost: ${invoke_result['total_cost_usd']:.4f}, "
          f"duration: {invoke_result['duration_s']:.1f}s")

    if invoke_result["returncode"] != 0:
        print(
            f"  WARNING: Haiku exited non-zero: {invoke_result['error_message']}",
            file=sys.stderr,
        )

    # Read decisions — fall back to parsing the run-log's result text if Haiku
    # returned JSON inline instead of writing the decisions file (common; the
    # Write tool is not always invoked even when the prompt requests it).
    decisions = read_haiku_decisions(
        HAIKU_DECISIONS_FILE, len(gathered), run_log_path=log_out_path
    )
    print(f"  Parsed {len(decisions)}/{len(gathered)} decision rows")

    # ── Phase 3: apply ────────────────────────────────────────────────────────
    print("\nPhase 3 — apply")
    result = apply_results(
        gathered=gathered,
        decisions=decisions,
        canonical=canonical,
        dry_run=False,
        log_path=log_path,
        normalizer_mod=normalizer_mod,
    )

    counts = result["counts"]

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("RESIDUAL-RESOLUTION RUN SUMMARY")
    print("=" * 60)
    print(f"  Residuals gathered:    {len(gathered)}")
    print(f"  Skipped (not-found):   {skip_counts.get('not-found', 0)}")
    print(f"  Skipped (already-res): {skip_counts.get('already-resolved', 0)}")
    print(f"  Skipped (forbidden):   {skip_counts.get('forbidden-path', 0)}")
    print()
    print(f"  Mapped to canonical:   {counts['mapped']}")
    print(f"  Rejected (no type):    {counts['rejected']}")
    print(f"  Escalated:             {counts['escalated']}")
    print(f"  Parse-failed:          {counts['parse_failed']}")
    print()
    print(f"  File rewrites applied: {result['file_rewrites_count']}")
    print(f"  Log rows appended:     {result['escalation_log_rows']}")
    print(f"  Audit trail:           {RESOLUTIONS_AUDIT.relative_to(REPO)}")
    print(f"  Unresolved log:        {log_path}")
    print()
    total_in = len(gathered)
    total_out = counts["mapped"] + counts["rejected"] + counts["escalated"] + counts["parse_failed"]
    if total_in != total_out:
        print(
            f"  WARNING: accounting mismatch — {total_in} gathered, {total_out} accounted for",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
