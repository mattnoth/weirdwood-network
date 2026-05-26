#!/usr/bin/env python3
"""stage4-refine-v1-edges.py — Read-only v1.1 refinement candidate producer.

Reads graph/edges/edges.jsonl (v1, 3,842 rows, READ-ONLY) and produces a
scratch candidate at:

  working/wiki/pass2-buckets/pass1-derived/_v1-refine/edges-v1.1-candidate.jsonl
  working/wiki/pass2-buckets/pass1-derived/_v1-refine/v1.1-type-contract-dropped.jsonl

Two operations (deterministic, zero LLM calls):

  1. TYPE-CONTRACT HARD DROP
     Calls type_contract_pass() from stage4-type-contract-validator.py.
     Rows that fail are removed from the output and written to the dropped file
     with a '_contract_reason' field.

  2. QUOTE-RELEVANCE SOFT FLAG
     Calls quote_relevance_pass() from stage4-quote-relevance-filter.py on the
     survivors.  Rows that fail are NOT dropped; instead two fields are added:
       _qr_warning: true
       _qr_reason:  one of "unmatched_source" | "unmatched_target" | "both" |
                    "unmatchable" | "no_quote" | "missing_endpoint"

Passing rows are written unannotated (no extra fields).

NEVER writes to graph/edges/ or modifies the input file.

Usage:
    python3 scripts/stage4-refine-v1-edges.py [--dry-run]
    python3 scripts/stage4-refine-v1-edges.py --apply

Options:
    --dry-run   (default) Print stats only.  No files written.
    --apply     Write the scratch candidate files.

Importable:
    from scripts.stage4_refine_v1_edges import (
        classify_qr_reason, refine_edges
    )
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo paths
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_EDGES_V1 = _REPO / "graph" / "edges" / "edges.jsonl"
_SCRATCH_DIR = (
    _REPO
    / "working"
    / "wiki"
    / "pass2-buckets"
    / "pass1-derived"
    / "_v1-refine"
)
_CANDIDATE_PATH = _SCRATCH_DIR / "edges-v1.1-candidate.jsonl"
_DROPPED_PATH   = _SCRATCH_DIR / "v1.1-type-contract-dropped.jsonl"

# ---------------------------------------------------------------------------
# Import sibling scripts via importlib (hyphenated filenames)
# ---------------------------------------------------------------------------

def _load_module(filename: str):
    """Load a script from scripts/ by filename (handles hyphenated names)."""
    mod_path = _REPO / "scripts" / filename
    mod_name = filename.replace("-", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_type_contract_validator():
    return _load_module("stage4-type-contract-validator.py")


def _load_quote_relevance_filter():
    return _load_module("stage4-quote-relevance-filter.py")


# ---------------------------------------------------------------------------
# QR reason classifier
# ---------------------------------------------------------------------------

def classify_qr_reason(qr_fail_reason: str) -> str:
    """Map a raw quote_relevance_pass reason string to a short reason label.

    Returns one of:
      "unmatched_source"
      "unmatched_target"
      "both"
      "unmatchable"
      "no_quote"
      "missing_endpoint"
    """
    r = qr_fail_reason.upper()
    if "UNMATCHABLE" in r:
        return "unmatchable"
    if "NO_QUOTE" in r:
        return "no_quote"
    if "MISSING_ENDPOINT" in r:
        return "missing_endpoint"
    if "UNMATCHED_BOTH" in r:
        return "both"
    if "UNMATCHED_SOURCE" in r:
        return "unmatched_source"
    if "UNMATCHED_TARGET" in r:
        return "unmatched_target"
    # Fallback — should not normally occur
    return "other"


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def refine_edges(
    rows: list[dict],
    character_slugs: frozenset[str],
    slug_token_index: dict[str, frozenset[str]],
    stoplist: frozenset[str],
    *,
    tcv_module,
    qrf_module,
) -> tuple[list[dict], list[dict]]:
    """Apply type-contract drop then quote-relevance soft-flag.

    Args:
        rows:              Input edge rows.
        character_slugs:   Frozenset of character slugs (filesystem-derived).
        slug_token_index:  Token index for QR filter.
        stoplist:          Token stoplist for QR filter.
        tcv_module:        Loaded stage4-type-contract-validator module.
        qrf_module:        Loaded stage4-quote-relevance-filter module.

    Returns:
        (output_rows, dropped_rows)
        output_rows:  Survivors after hard drop, soft-flagged where QR fails.
        dropped_rows: Rows removed by type-contract; include '_contract_reason'.
    """
    output_rows: list[dict] = []
    dropped_rows: list[dict] = []

    for row in rows:
        # ---- Pass 1: type-contract gate (drop / flip / flag / retype / keep) ----
        tc_disp, tc_reason = tcv_module.type_contract_pass(row, character_slugs)

        if tc_disp == "drop":
            annotated = dict(row)
            annotated["_contract_reason"] = tc_reason
            dropped_rows.append(annotated)
            continue

        if tc_disp == "flip":
            # Swap source/target; annotate.
            orig_src = row.get("source_slug", "")
            orig_tgt = row.get("target_slug", "")
            row = dict(row)
            row["source_slug"]          = orig_tgt
            row["target_slug"]          = orig_src
            row["_flipped"]             = True
            row["_flip_reason"]         = tc_reason
            row["_flipped_from_source"] = orig_src
            row["_flipped_from_target"] = orig_tgt

        elif tc_disp == "flag":
            row = dict(row)
            row["_contract_warning"] = True
            row["_contract_reason"]  = tc_reason

        elif tc_disp == "retype":
            # Rewrite edge_type; annotate with retype metadata.
            orig_et = (row.get("edge_type") or "").strip()
            row = dict(row)
            # Extract new type from reason string: "retype_to=COMMANDS"
            new_et = tcv_module._RULES_RETYPE_TARGET_TYPE  # default for RULES→char
            if "retype_to=" in tc_reason:
                new_et = tc_reason.split("retype_to=")[-1].strip().rstrip(")")
            row["edge_type"]      = new_et
            row["_retyped_from"]  = orig_et
            row["_retype_reason"] = tc_reason

        # ---- Pass 2: quote-relevance soft flag ----
        passed_qr, qr_reason = qrf_module.quote_relevance_pass(
            row, slug_token_index, stoplist
        )
        if not passed_qr:
            annotated = dict(row)
            annotated["_qr_warning"] = True
            annotated["_qr_reason"] = classify_qr_reason(qr_reason)
            output_rows.append(annotated)
        else:
            output_rows.append(dict(row))

    return output_rows, dropped_rows


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
                print(
                    f"[warn] {path}:{lineno}: JSON parse error: {exc}",
                    file=sys.stderr,
                )
    return rows


def _write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Stats helpers
# ---------------------------------------------------------------------------

def _build_stats(
    total: int,
    dropped_rows: list[dict],
    output_rows: list[dict],
) -> dict:
    """Return a stats dict used both for printing and for the proposal report."""
    qr_flagged  = [r for r in output_rows if r.get("_qr_warning")]
    qr_clean    = [r for r in output_rows if not r.get("_qr_warning")]
    n_dropped   = len(dropped_rows)
    n_survivors = len(output_rows)
    n_flagged   = len(qr_flagged)

    # Breakdown of dropped by contract
    drop_by_contract: Counter = Counter()
    for row in dropped_rows:
        reason = row.get("_contract_reason", "?")
        et = (row.get("edge_type") or "?").strip()
        drop_by_contract[f"{et}"] += 1

    # QR flag breakdown by reason
    qr_by_reason: Counter = Counter(r.get("_qr_reason", "?") for r in qr_flagged)

    # QR flag breakdown by edge_type
    qr_by_edge_type: Counter = Counter(
        (r.get("edge_type") or "?") for r in qr_flagged
    )

    return {
        "total":           total,
        "dropped":         n_dropped,
        "survivors":       n_survivors,
        "qr_flagged":      n_flagged,
        "qr_clean":        len(qr_clean),
        "drop_by_contract": drop_by_contract,
        "qr_by_reason":    qr_by_reason,
        "qr_by_edge_type": qr_by_edge_type,
        "dropped_rows":    dropped_rows,
        "qr_flagged_rows": qr_flagged,
    }


def _print_stats(stats: dict) -> None:
    total      = stats["total"]
    dropped    = stats["dropped"]
    survivors  = stats["survivors"]
    qr_flagged = stats["qr_flagged"]

    print()
    print("=== Stage 4 v1.1 Refine — Summary ===")
    print(f"  Input (v1):              {total:,} edges")
    print(f"  Hard-dropped (contract): {dropped:,}")
    print(f"  Survivors:               {survivors:,}")
    print(f"  Soft-flagged (QR):       {qr_flagged:,}  (kept, not removed)")
    print(f"  Clean (no flag):         {stats['qr_clean']:,}")
    print()

    if stats["drop_by_contract"]:
        print("  Hard-dropped by edge_type:")
        for et, cnt in sorted(
            stats["drop_by_contract"].items(), key=lambda x: -x[1]
        ):
            print(f"    {et}: {cnt}")
        print()

    if stats["qr_by_reason"]:
        print("  QR-flagged by reason:")
        for reason, cnt in sorted(
            stats["qr_by_reason"].items(), key=lambda x: -x[1]
        ):
            print(f"    {reason}: {cnt}")
        print()

    if stats["qr_by_edge_type"]:
        print("  QR-flagged by edge_type (top 15):")
        for et, cnt in stats["qr_by_edge_type"].most_common(15):
            print(f"    {et}: {cnt}")
        print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Produce v1.1 refinement candidate for graph/edges/edges.jsonl.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=True,
        help="(default) Print stats only.  No files written.",
    )
    mode_group.add_argument(
        "--apply",
        dest="dry_run",
        action="store_false",
        help="Write scratch candidate files.",
    )
    parser.add_argument(
        "--input",
        default=str(_EDGES_V1),
        help=f"Input JSONL file (default: {_EDGES_V1})",
    )
    parser.add_argument(
        "--graph-nodes",
        default=str(_REPO / "graph" / "nodes"),
        help="Path to graph/nodes dir (for character slug detection)",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input).resolve()
    nodes_dir  = Path(args.graph_nodes)

    # Safety: never touch graph/edges/
    _REPO_EDGES = _REPO / "graph" / "edges"
    if input_path.parent.resolve() == _REPO_EDGES.resolve():
        # READ is fine; we just must not write there
        pass  # writing guard is below

    # Load sibling modules
    print("Loading sibling modules…", file=sys.stderr)
    tcv = _load_type_contract_validator()
    qrf = _load_quote_relevance_filter()

    # Build character slug set
    print("Building character slug set…", file=sys.stderr)
    character_slugs = tcv.build_character_slugs(nodes_dir)
    print(f"  {len(character_slugs):,} character slugs", file=sys.stderr)

    # Read input
    print(f"Reading {input_path}…", file=sys.stderr)
    rows = _read_jsonl(input_path)
    print(f"  {len(rows):,} rows loaded", file=sys.stderr)

    # Build QR token index from all slugs seen in the data
    print("Building slug-token index for QR filter…", file=sys.stderr)
    stoplist = qrf.build_stoplist()
    all_slugs = list(
        {r.get("source_slug", "") for r in rows}
        | {r.get("target_slug", "") for r in rows}
    )
    slug_token_index = qrf.build_slug_token_index(
        slugs=all_slugs, stoplist=stoplist
    )
    print(f"  Index covers {len(slug_token_index):,} slugs", file=sys.stderr)

    # Run the pipeline
    print("Running refine pipeline…", file=sys.stderr)
    output_rows, dropped_rows = refine_edges(
        rows,
        character_slugs,
        slug_token_index,
        stoplist,
        tcv_module=tcv,
        qrf_module=qrf,
    )

    stats = _build_stats(len(rows), dropped_rows, output_rows)
    _print_stats(stats)

    if args.dry_run:
        print("(Dry-run mode — no files written.  Use --apply to write.)")
        return

    # Write scratch outputs (never to graph/edges/)
    for out_path in (_CANDIDATE_PATH, _DROPPED_PATH):
        if out_path.resolve().is_relative_to(_REPO_EDGES.resolve()):
            sys.exit(
                f"ERROR: output path must not be inside graph/edges/: {out_path}"
            )

    print(f"Writing candidate -> {_CANDIDATE_PATH}", file=sys.stderr)
    _write_jsonl(output_rows, _CANDIDATE_PATH)

    print(f"Writing dropped   -> {_DROPPED_PATH}", file=sys.stderr)
    _write_jsonl(dropped_rows, _DROPPED_PATH)

    n = stats["total"]
    d = stats["dropped"]
    f = stats["qr_flagged"]
    print(
        f"\nDone.  v1 {n:,} -> after hard-drop {n - d:,} "
        f"(dropped {d}), of which {f} carry _qr_warning."
    )
    print(f"Candidate: {_CANDIDATE_PATH}")
    print(f"Dropped:   {_DROPPED_PATH}")


if __name__ == "__main__":
    main()
