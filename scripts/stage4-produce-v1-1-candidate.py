#!/usr/bin/env python3
"""stage4-produce-v1-1-candidate.py — Deterministic v1.1 edge refinement candidate.

Reads graph/edges/edges.jsonl (3,842 rows, READ-ONLY).
NEVER writes to graph/edges/ or modifies the input.

Produces:
  working/wiki/pass2-buckets/pass1-derived/_v1-refine/edges-v1.1-candidate.jsonl
  working/wiki/pass2-buckets/pass1-derived/_v1-refine/v1.1-dropped.jsonl
  working/wiki/data/pass1-derived-v1.1-applied.md

Two-bucket approach:
  SURE: apply immediately (drops + retypes + evidence annotations)
  NODE-DEPENDENT: flag only (add _needs_node_decision + _proposed_fix, endpoints unchanged)

Transformation order (per-row):
  1. SURE-DROP: 4 exact edges dropped to v1.1-dropped.jsonl (NOT the contract-dropped file)
  2. TYPE-CONTRACT (via stage4-type-contract-validator.py):
       RULES→char => RETYPE to COMMANDS
       kinship non-char => FLAG or DROP
       COMMANDS non-char target => DROP
       MOTIVATES char source => DROP
       empty evidence_quote => DROP
       etc.
  3. SURE-RETYPE: any remaining RULES→char edges (belt-and-suspenders after contract pass)
  4. ECHOES char↔char: KEPT (contract removed); add _evidence_weak:true to
       robb-stark ECHOES eddard-stark (quote doesn't evidence the echo).
  5. NODE-DEPENDENT FLAGS: add _needs_node_decision + _proposed_fix to 3 specific edges
  6. QR SOFT-FLAG: non-destructive _qr_warning/_qr_reason from quote-relevance filter

Usage:
    python3 scripts/stage4-produce-v1-1-candidate.py          # dry-run (no writes)
    python3 scripts/stage4-produce-v1-1-candidate.py --apply  # write outputs
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
_EDGES_V1    = _REPO / "graph" / "edges" / "edges.jsonl"
_SCRATCH_DIR = (
    _REPO / "working" / "wiki" / "pass2-buckets" / "pass1-derived" / "_v1-refine"
)
_CANDIDATE_PATH = _SCRATCH_DIR / "edges-v1.1-candidate.jsonl"
_DROPPED_PATH   = _SCRATCH_DIR / "v1.1-dropped.jsonl"
_REPORT_PATH    = _REPO / "working" / "wiki" / "data" / "pass1-derived-v1.1-applied.md"

# ---------------------------------------------------------------------------
# SURE-DROP set — 4 exact (source_slug, edge_type, target_slug) triples
# ---------------------------------------------------------------------------

_SURE_DROPS: frozenset[tuple[str, str, str]] = frozenset({
    ("theon-greyjoy",    "UNCLE_OF",   "greyjoy-rebellion"),
    ("black-walder-frey","LOVER_OF",   "fair-isle"),
    ("missandei",        "SIBLING_OF", "three-sisters"),
    ("gilly",            "PARENT_OF",  "her-little-flower"),
})

# ---------------------------------------------------------------------------
# ECHOES evidence-weak set — add _evidence_weak:true
# ---------------------------------------------------------------------------

_ECHOES_EVIDENCE_WEAK: frozenset[tuple[str, str, str]] = frozenset({
    ("robb-stark", "ECHOES", "eddard-stark"),
})

# ---------------------------------------------------------------------------
# NODE-DEPENDENT flags — (source_slug, edge_type, target_slug) -> proposed_fix
# ---------------------------------------------------------------------------

_NODE_DEPENDENT_FLAGS: dict[tuple[str, str, str], str] = {
    ("nestor-royce", "COUSIN_OF",  "bronze"):
        "retarget target bronze->yohn-royce (alias)",
    ("robb-stark",   "HEIR_TO",    "winterfell"):
        "retarget target winterfell->lord-of-winterfell (title node)",
    ("queen-cersei", "SPOUSE_OF",  "robert-i-baratheon"):
        "alias queen-cersei->cersei-lannister",
}
# Also flag ALL queen-cersei-source edges
_QUEEN_CERSEI_SOURCE_FIX = "alias queen-cersei->cersei-lannister"

# ---------------------------------------------------------------------------
# Load sibling scripts via importlib (hyphenated filenames)
# ---------------------------------------------------------------------------

def _load_module(filename: str):
    mod_path = _REPO / "scripts" / filename
    mod_name = filename.replace("-", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod

# ---------------------------------------------------------------------------
# JSONL helpers
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
# Core pipeline
# ---------------------------------------------------------------------------

def produce_v1_1_candidate(
    rows: list[dict],
    *,
    tcv_module,
    qrf_module,
    nodes_dir: Path,
) -> tuple[list[dict], list[dict], dict]:
    """Apply all v1.1 refinements.

    Returns:
        (candidate_rows, dropped_rows, stats_dict)
    """
    # Build character slugs and slug category index for the validator
    character_slugs = tcv_module.build_character_slugs(nodes_dir)
    slug_cat_index  = tcv_module.build_slug_category_index(nodes_dir)

    # QR filter resources
    stoplist         = qrf_module.build_stoplist()
    all_slugs        = list({
        s for row in rows
        for s in (row.get("source_slug",""), row.get("target_slug",""))
        if s
    })
    slug_token_index = qrf_module.build_slug_token_index(all_slugs, stoplist=stoplist)

    candidate_rows: list[dict] = []
    dropped_rows:   list[dict] = []

    # Tracking for report
    sure_dropped_found: set[tuple[str,str,str]] = set()
    sure_dropped_rows:  list[tuple[str,str,str]] = []
    contract_dropped:   list[dict] = []
    contract_retyped:   list[dict] = []
    contract_flagged:   list[dict] = []
    echoes_kept:        list[dict] = []
    echoes_evidence_weak_applied: list[dict] = []
    node_dep_flagged:   list[dict] = []
    qr_flagged:         list[dict] = []
    qr_reason_counts:   Counter    = Counter()
    not_found_sure_drops: list[tuple[str,str,str]] = []
    not_found_node_deps:  list[tuple[str,str,str]] = []

    for row in rows:
        src = row.get("source_slug", "")
        et  = row.get("edge_type",   "")
        tgt = row.get("target_slug", "")
        key = (src, et, tgt)

        # ---- Step 1: SURE-DROP ----
        if key in _SURE_DROPS:
            annotated = dict(row)
            annotated["_v1_1_drop_reason"] = "sure-drop: genuinely wrong target (not a person)"
            dropped_rows.append(annotated)
            sure_dropped_found.add(key)
            sure_dropped_rows.append(key)
            continue

        # ---- Step 2: Type-contract validator ----
        tc_disp, tc_reason = tcv_module.type_contract_pass(row, character_slugs, slug_cat_index)

        if tc_disp == "drop":
            annotated = dict(row)
            annotated["_contract_reason"] = tc_reason
            dropped_rows.append(annotated)
            contract_dropped.append(annotated)
            continue

        working_row = dict(row)

        if tc_disp == "flip":
            orig_src = working_row.get("source_slug", "")
            orig_tgt = working_row.get("target_slug", "")
            working_row["source_slug"]          = orig_tgt
            working_row["target_slug"]          = orig_src
            working_row["_flipped"]             = True
            working_row["_flip_reason"]         = tc_reason
            working_row["_flipped_from_source"] = orig_src
            working_row["_flipped_from_target"] = orig_tgt
            contract_flagged.append(working_row)

        elif tc_disp == "flag":
            working_row["_contract_warning"] = True
            working_row["_contract_reason"]  = tc_reason
            contract_flagged.append(working_row)

        elif tc_disp == "retype":
            orig_et = (working_row.get("edge_type") or "").strip()
            new_et  = tcv_module._RULES_RETYPE_TARGET_TYPE
            if "retype_to=" in tc_reason:
                new_et = tc_reason.split("retype_to=")[-1].strip().rstrip(")")
            working_row["edge_type"]      = new_et
            working_row["_retyped_from"]  = orig_et
            working_row["_retype_reason"] = tc_reason
            contract_retyped.append(working_row)

        # ---- Step 3: ECHOES char↔char — KEPT; add _evidence_weak if applicable ----
        src2 = working_row.get("source_slug", "")
        et2  = working_row.get("edge_type",   "")
        tgt2 = working_row.get("target_slug", "")

        if et2 == "ECHOES":
            src_is_char = src2 in character_slugs
            tgt_is_char = tgt2 in character_slugs
            if src_is_char and tgt_is_char:
                echoes_kept.append(working_row)
                if (src2, et2, tgt2) in _ECHOES_EVIDENCE_WEAK:
                    working_row["_evidence_weak"] = True
                    echoes_evidence_weak_applied.append(working_row)

        # ---- Step 4: NODE-DEPENDENT flags ----
        key2 = (src2, et2, tgt2)
        if key2 in _NODE_DEPENDENT_FLAGS:
            working_row["_needs_node_decision"] = True
            working_row["_proposed_fix"]        = _NODE_DEPENDENT_FLAGS[key2]
            node_dep_flagged.append(working_row)
        elif src2 == "queen-cersei":
            # Flag ALL remaining queen-cersei-source edges (beyond the SPOUSE_OF already above)
            working_row["_needs_node_decision"] = True
            working_row["_proposed_fix"]        = _QUEEN_CERSEI_SOURCE_FIX
            node_dep_flagged.append(working_row)

        # ---- Step 5: QR soft-flag ----
        passed_qr, qr_reason = qrf_module.quote_relevance_pass(
            working_row, slug_token_index, stoplist
        )
        if not passed_qr:
            # Map reason to short label (same logic as stage4-refine-v1-edges.py)
            r = qr_reason.upper()
            if "UNMATCHABLE" in r:
                short = "unmatchable"
            elif "NO_QUOTE" in r:
                short = "no_quote"
            elif "MISSING_ENDPOINT" in r:
                short = "missing_endpoint"
            elif "UNMATCHED_BOTH" in r:
                short = "both"
            elif "UNMATCHED_SOURCE" in r:
                short = "unmatched_source"
            elif "UNMATCHED_TARGET" in r:
                short = "unmatched_target"
            else:
                short = "other"
            working_row["_qr_warning"] = True
            working_row["_qr_reason"]  = short
            qr_flagged.append(working_row)
            qr_reason_counts[short] += 1

        candidate_rows.append(working_row)

    # Check for any sure-drop targets not found in input
    for key in sorted(_SURE_DROPS):
        if key not in sure_dropped_found:
            not_found_sure_drops.append(key)

    # Check for any node-dependent targets not found in candidate
    for key in sorted(_NODE_DEPENDENT_FLAGS.keys()):
        found = any(
            r.get("source_slug")==key[0]
            and r.get("edge_type")==key[1]
            and r.get("target_slug")==key[2]
            for r in candidate_rows
        )
        if not found:
            not_found_node_deps.append(key)

    # RULES→char retyped summary (from contract_retyped)
    rules_retyped = [
        r for r in contract_retyped
        if r.get("_retyped_from") == "RULES"
    ]

    stats = {
        "total_in":                 len(rows),
        "sure_dropped":             len(sure_dropped_rows),
        "sure_dropped_keys":        sure_dropped_rows,
        "contract_dropped":         len(contract_dropped),
        "contract_retyped":         contract_retyped,
        "rules_retyped":            rules_retyped,
        "contract_flagged":         contract_flagged,
        "echoes_kept":              echoes_kept,
        "echoes_evidence_weak":     echoes_evidence_weak_applied,
        "node_dep_flagged":         node_dep_flagged,
        "qr_flagged_count":         len(qr_flagged),
        "qr_reason_counts":         qr_reason_counts,
        "total_out":                len(candidate_rows),
        "total_dropped":            len(dropped_rows),
        "not_found_sure_drops":     not_found_sure_drops,
        "not_found_node_deps":      not_found_node_deps,
    }

    return candidate_rows, dropped_rows, stats

# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def _build_report(stats: dict, input_path: Path) -> str:
    lines: list[str] = [
        "# Pass-1-Derived v1.1 Refinement — Applied Report",
        "",
        f"**Input:** `{input_path}` (READ-ONLY — not modified)",
        f"**Total in:** {stats['total_in']}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Operation | Count |",
        f"|-----------|-------|",
        f"| Input rows | {stats['total_in']} |",
        f"| SURE-DROP (genuinely wrong target) | {stats['sure_dropped']} |",
        f"| Type-contract DROP | {stats['contract_dropped']} |",
        f"| **Total dropped** | **{stats['total_dropped']}** |",
        f"| RULES→COMMANDS retype | {len(stats['rules_retyped'])} |",
        f"| Contract FLAG/FLIP | {len(stats['contract_flagged'])} |",
        f"| ECHOES char↔char KEPT | {len(stats['echoes_kept'])} |",
        f"| ECHOES _evidence_weak:true applied | {len(stats['echoes_evidence_weak'])} |",
        f"| NODE-DEPENDENT flagged | {len(stats['node_dep_flagged'])} |",
        f"| QR soft-flagged | {stats['qr_flagged_count']} |",
        f"| **Final candidate rows** | **{stats['total_out']}** |",
        "",
        "---",
        "",
        "## SURE-DROP List (4 targeted + any contract drops)",
        "",
        "### Targeted drops (genuinely wrong target — not a person):",
        "",
    ]

    for key in stats["sure_dropped_keys"]:
        lines.append(f"- `{key[0]} {key[1]} {key[2]}`")

    if stats["not_found_sure_drops"]:
        lines += ["", "### WARNING: Expected sure-drop edges NOT found in input:", ""]
        for key in stats["not_found_sure_drops"]:
            lines.append(f"- NOT FOUND: `{key[0]} {key[1]} {key[2]}`")
    else:
        lines += ["", "_All 4 sure-drop targets found and dropped._"]

    lines += [
        "",
        "---",
        "",
        "## RULES→COMMANDS Retype List",
        "",
        "Architecture: RULES = Ruler→Location; COMMANDS = Commander→Subordinate.",
        "These edges had a character target — correct type is COMMANDS.",
        "",
    ]
    for r in stats["rules_retyped"]:
        src = r.get("source_slug","?")
        tgt = r.get("target_slug","?")
        lines.append(f"- `{src} RULES→COMMANDS {tgt}`")

    if not stats["rules_retyped"]:
        lines.append("_No RULES→COMMANDS retypes._")

    lines += [
        "",
        "---",
        "",
        "## ECHOES char↔char — KEPT",
        "",
        "Contract was removed per architecture: ECHOES is valid for character↔character.",
        "",
    ]
    for r in stats["echoes_kept"]:
        src = r.get("source_slug","?")
        tgt = r.get("target_slug","?")
        ev_weak = " [_evidence_weak:true]" if r.get("_evidence_weak") else ""
        lines.append(f"- `{src} ECHOES {tgt}`{ev_weak}")

    if not stats["echoes_kept"]:
        lines.append("_No ECHOES char↔char edges._")

    lines += [
        "",
        "---",
        "",
        "## NODE-DEPENDENT Flags (endpoints unchanged, awaiting node decision)",
        "",
        "Format: `src EDGE tgt` → `_proposed_fix`",
        "",
    ]
    for r in stats["node_dep_flagged"]:
        src  = r.get("source_slug","?")
        et   = r.get("edge_type","?")
        tgt  = r.get("target_slug","?")
        fix  = r.get("_proposed_fix","?")
        lines.append(f"- `{src} {et} {tgt}` → `{fix}`")

    if stats["not_found_node_deps"]:
        lines += ["", "### WARNING: Expected node-dep edges NOT found in candidate:", ""]
        for key in stats["not_found_node_deps"]:
            lines.append(f"- NOT FOUND: `{key[0]} {key[1]} {key[2]}`")

    if not stats["node_dep_flagged"]:
        lines.append("_No node-dependent flags._")

    lines += [
        "",
        "---",
        "",
        "## QR Soft-Flag Summary",
        "",
        f"Total QR-flagged rows: **{stats['qr_flagged_count']}**",
        "(Kept in candidate, not dropped — soft annotation only)",
        "",
        "| Reason | Count |",
        "|--------|-------|",
    ]
    for reason, count in sorted(stats["qr_reason_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| {reason} | {count} |")

    if not stats["qr_reason_counts"]:
        lines.append("_No QR flags._")

    lines += [
        "",
        "---",
        "",
        "## Input Integrity Check",
        "",
        f"`graph/edges/edges.jsonl` is READ-ONLY. Total rows in: {stats['total_in']}.",
        "This script NEVER writes to `graph/edges/`.",
        "",
        "Total candidate rows out: " + str(stats["total_out"]),
        "Total dropped rows: " + str(stats["total_dropped"]),
        f"Expected: {stats['total_in']} = {stats['total_out']} + {stats['total_dropped']}",
        "Check: " + (
            "PASS"
            if stats["total_in"] == stats["total_out"] + stats["total_dropped"]
            else "FAIL — row count mismatch!"
        ),
    ]

    return "\n".join(lines) + "\n"

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Produce v1.1 edge refinement candidate (deterministic, zero LLM).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Write output files (default is dry-run — prints stats only).",
    )
    parser.add_argument(
        "--input", default=str(_EDGES_V1),
        help=f"Input edges JSONL (default: {_EDGES_V1})",
    )
    parser.add_argument(
        "--candidate", default=str(_CANDIDATE_PATH),
        help=f"Output candidate path (default: {_CANDIDATE_PATH})",
    )
    parser.add_argument(
        "--dropped", default=str(_DROPPED_PATH),
        help=f"Output dropped path (default: {_DROPPED_PATH})",
    )
    parser.add_argument(
        "--report", default=str(_REPORT_PATH),
        help=f"Output report path (default: {_REPORT_PATH})",
    )
    parser.add_argument(
        "--graph-nodes", default=str(_REPO / "graph" / "nodes"),
        help="Path to graph/nodes dir",
    )
    args = parser.parse_args(argv)

    input_path     = Path(args.input)
    candidate_path = Path(args.candidate)
    dropped_path   = Path(args.dropped)
    report_path    = Path(args.report)
    nodes_dir      = Path(args.graph_nodes)

    # Safety: never write to graph/edges/
    _REPO_EDGES = _REPO / "graph" / "edges"
    for out_p in [candidate_path, dropped_path, report_path]:
        try:
            out_p.resolve().relative_to(_REPO_EDGES)
            sys.exit(f"ERROR: output path must not be inside graph/edges/: {out_p}")
        except ValueError:
            pass
        if out_p.resolve() == input_path.resolve():
            sys.exit(f"ERROR: output path must not be the same as --input: {out_p}")

    print("Loading sibling modules…", file=sys.stderr)
    tcv_module = _load_module("stage4-type-contract-validator.py")
    qrf_module = _load_module("stage4-quote-relevance-filter.py")

    print(f"Reading {input_path}…", file=sys.stderr)
    rows = _read_jsonl(input_path)
    print(f"  {len(rows)} rows loaded", file=sys.stderr)

    print("Building character slugs and slug category index…", file=sys.stderr)

    print("Running v1.1 refinement pipeline…", file=sys.stderr)
    candidate_rows, dropped_rows, stats = produce_v1_1_candidate(
        rows,
        tcv_module=tcv_module,
        qrf_module=qrf_module,
        nodes_dir=nodes_dir,
    )

    # Integrity check
    assert len(rows) == len(candidate_rows) + len(dropped_rows), (
        f"Row count mismatch: {len(rows)} in != {len(candidate_rows)} candidate "
        f"+ {len(dropped_rows)} dropped"
    )

    print("\n=== v1.1 Refinement Summary ===", file=sys.stderr)
    print(f"  Input rows:              {stats['total_in']}", file=sys.stderr)
    print(f"  SURE-DROP (targeted):    {stats['sure_dropped']}", file=sys.stderr)
    print(f"  Contract DROP:           {stats['contract_dropped']}", file=sys.stderr)
    print(f"  Total dropped:           {stats['total_dropped']}", file=sys.stderr)
    print(f"  RULES→COMMANDS retyped:  {len(stats['rules_retyped'])}", file=sys.stderr)
    print(f"  Contract FLAG/FLIP:      {len(stats['contract_flagged'])}", file=sys.stderr)
    print(f"  ECHOES char↔char kept:   {len(stats['echoes_kept'])}", file=sys.stderr)
    print(f"  ECHOES _evidence_weak:   {len(stats['echoes_evidence_weak'])}", file=sys.stderr)
    print(f"  NODE-DEPENDENT flagged:  {len(stats['node_dep_flagged'])}", file=sys.stderr)
    print(f"  QR soft-flagged:         {stats['qr_flagged_count']}", file=sys.stderr)
    print(f"  Final candidate rows:    {stats['total_out']}", file=sys.stderr)

    if stats["not_found_sure_drops"]:
        print("\n[WARN] Sure-drop targets NOT found in input:", file=sys.stderr)
        for key in stats["not_found_sure_drops"]:
            print(f"  NOT FOUND: {key[0]} {key[1]} {key[2]}", file=sys.stderr)

    if stats["not_found_node_deps"]:
        print("\n[WARN] Node-dep targets NOT found in candidate:", file=sys.stderr)
        for key in stats["not_found_node_deps"]:
            print(f"  NOT FOUND: {key[0]} {key[1]} {key[2]}", file=sys.stderr)

    print("\n--- SURE-DROP list ---", file=sys.stderr)
    for key in stats["sure_dropped_keys"]:
        print(f"  DROPPED: {key[0]} {key[1]} {key[2]}", file=sys.stderr)

    print("\n--- RULES→COMMANDS retype list ---", file=sys.stderr)
    for r in stats["rules_retyped"]:
        print(f"  RETYPED: {r['source_slug']} RULES→COMMANDS {r['target_slug']}", file=sys.stderr)

    print("\n--- ECHOES char↔char kept ---", file=sys.stderr)
    for r in stats["echoes_kept"]:
        ev = " [_evidence_weak:true]" if r.get("_evidence_weak") else ""
        print(f"  KEPT: {r['source_slug']} ECHOES {r['target_slug']}{ev}", file=sys.stderr)

    print("\n--- NODE-DEPENDENT flags ---", file=sys.stderr)
    for r in stats["node_dep_flagged"]:
        print(f"  FLAGGED: {r['source_slug']} {r['edge_type']} {r['target_slug']}"
              f" -> {r['_proposed_fix']}", file=sys.stderr)

    print("\n--- QR soft-flag counts ---", file=sys.stderr)
    for reason, count in sorted(stats["qr_reason_counts"].items(), key=lambda x: -x[1]):
        print(f"  {reason}: {count}", file=sys.stderr)

    if not args.apply:
        print(
            "\n(Dry-run mode — no files written.  Use --apply to write.)",
            file=sys.stderr,
        )
        return

    # Write outputs
    _write_jsonl(candidate_rows, candidate_path)
    print(f"\nCandidate written -> {candidate_path} ({len(candidate_rows)} rows)", file=sys.stderr)

    _write_jsonl(dropped_rows, dropped_path)
    print(f"Dropped written   -> {dropped_path} ({len(dropped_rows)} rows)", file=sys.stderr)

    report_md = _build_report(stats, input_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")
    print(f"Report written    -> {report_path}", file=sys.stderr)

    print(f"\ngraph/edges/edges.jsonl: unchanged (read-only — {stats['total_in']} rows)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
