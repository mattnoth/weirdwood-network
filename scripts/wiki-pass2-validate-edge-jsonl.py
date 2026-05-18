#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier output validator.

Loads every output file produced by a Stage 4 batch (per the batch-manifest entry),
checks each row against the required-fields contract from
`.claude/agents/prose-edge-classifier.md`'s "Required fields per decision" table,
plus the field-shape rules.

Exits 0 if all rows pass; exits non-zero with a per-row violation report otherwise.

Usage:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \
        --batch-id batch-0012 \
        --mission working/missions/2026-05-14-stage4-v1-bulk-sonnet

    # Or validate a single output file directly:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \
        --file working/wiki/pass2-buckets/<bucket>/prose-edges/<slug>.edges.jsonl

    # Or validate the questions-for-matt.jsonl rows filed during a batch:
    python3 scripts/wiki-pass2-validate-edge-jsonl.py \
        --questions working/wiki/pass2-buckets/questions-for-matt.jsonl \
        --filed-after 2026-05-15T14:32:00Z
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

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
# Vocabulary loader (canonical edge_type list from architecture.md)
# ---------------------------------------------------------------------------

def load_canonical_vocab(arch_path: Path = Path("reference/architecture.md")) -> set[str]:
    """Parse architecture.md and return the set of canonical edge_type names.

    Looks for backticked all-caps identifiers in the Edge Types section's tables.
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

    # Extract `BACKTICKED_NAMES` that look like edge types: all-caps + underscores
    candidates = re.findall(r"`([A-Z][A-Z_]+)`", section)
    # Filter out non-edge-type backticked tokens (e.g., examples that aren't edges)
    # Heuristic: edge types are 4+ chars and don't include common non-edge tokens
    nonedges = {"AGOT", "ACOK", "ASOS", "AFFC", "ADWD", "POV", "JSONL", "JSON",
                "TWOIAF", "TWOTNW", "ASOIAF", "URL", "ID", "UTC"}
    return {c for c in candidates if len(c) >= 4 and c not in nonedges}


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


def validate_edge_row(row: dict, file: str, line_no: int, vocab: set[str]) -> list[Violation]:
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
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if not (args.batch_id or args.file or args.questions):
        parser.error("Must supply --batch-id, --file, or --questions")

    try:
        vocab = load_canonical_vocab(Path(args.arch))
    except Exception as e:
        print(f"WARNING: could not load canonical vocabulary ({e}); skipping edge_type-in-vocab checks", file=sys.stderr)
        vocab = set()

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
            all_violations.extend(validate_edge_row(row, f, line_no, vocab))

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

    # Report
    print(f"Validator summary: files_checked={files_checked}, files_missing={files_missing}, rows_checked={rows_checked}, violations={len(all_violations)}")
    if all_violations:
        print("\nViolations:")
        for v in all_violations:
            print(v)
        return 1
    print("CLEAN ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
