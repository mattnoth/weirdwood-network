#!/usr/bin/env python3
"""
Stage 4 prose-edge soft-fallback flagger.

Walks all `emit_edge` rows produced by completed Stage 4 batches and tags rows
matching known soft-fallback patterns (KNOWS-as-default, type-contract
violations, low-confidence emissions, etc.). Does NOT block or modify them —
only flags for a later Opus audit pass.

Pattern checks (per session-54 plan):
  1. KNOWS  with no knowing-prose in snippet (no knew/known/learned/informed/told)
  2. ATTENDS  with target type not starting with `event.*`
  3. FIGHTS_IN  with target type not `event.*` or `organization.*`
  4. TRAVELS_TO / LOCATED_AT / BORN_AT / DIED_AT  with target type not `place.*`
  5. SPOUSE_OF  with target type not `character.*`
  6. WIELDS  with target type not `object.artifact`
  7. confidence_tier == 3  (model self-flagged low)
  8. CONTEMPORARY_WITH  with target type `character.*` (per patched prompt)

Outputs:
  working/wiki/data/stage4-suspicious-edges.jsonl       — full flagged rows
  working/wiki/data/stage4-suspicious-edges-summary.md  — counts + samples

Usage:
    python3 scripts/wiki-pass2-flag-suspicious-edges.py
    python3 scripts/wiki-pass2-flag-suspicious-edges.py --mission <dir>
    python3 scripts/wiki-pass2-flag-suspicious-edges.py --batch-id batch-0020
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

KNOWS_PROSE_RE = re.compile(
    r"\b(knew|known|knows|knowing|learned of|learnt of|informed|told|"
    r"acquainted|familiar with|recognize[sd]?|aware of|met|meets|meeting)\b",
    re.IGNORECASE,
)

# Map node directory name -> normalized "type family" prefix used in contracts.
# Directories below `graph/nodes/` whose name maps to a family. Anything not
# listed is left as the raw dir name (e.g. "concepts", "titles") and will not
# match the strict family checks below — those rows simply won't be flagged
# for type-contract violations (they may still be flagged on other patterns).
DIR_TO_TYPE_FAMILY = {
    "characters": "character",
    "events":     "event",
    "locations":  "place",
    "artifacts":  "object.artifact",
    "factions":   "organization",
    "houses":     "organization",
    "religions":  "organization",
}

# edge_type -> required target-type family (or set of acceptable families).
# Used by the type-contract pattern checks below.
EDGE_TYPE_TARGET_CONTRACT = {
    "ATTENDS":          {"event"},
    "FIGHTS_IN":        {"event", "organization"},
    "TRAVELS_TO":       {"place"},
    "LOCATED_AT":       {"place"},
    "BORN_AT":          {"place"},
    "DIED_AT":          {"place"},
    "SPOUSE_OF":        {"character"},
    "WIELDS":           {"object.artifact"},
}


# ---------------------------------------------------------------------------
# Slug -> type index (built by walking graph/nodes/)
# ---------------------------------------------------------------------------

def build_slug_index(nodes_root: Path) -> dict[str, str]:
    """Return {slug: type_family} for every node file under nodes_root.

    Cheap: uses the parent directory name; no frontmatter parsing required for
    the family check. Slugs are derived from filenames (`<slug>.node.md`).
    """
    index: dict[str, str] = {}
    if not nodes_root.is_dir():
        return index
    for dir_path in nodes_root.iterdir():
        if not dir_path.is_dir():
            continue
        dir_name = dir_path.name
        if dir_name.startswith("_"):  # _conflicts, _unclassified — skip
            continue
        family = DIR_TO_TYPE_FAMILY.get(dir_name, dir_name)
        for node_file in dir_path.glob("*.node.md"):
            slug = node_file.name[:-len(".node.md")]
            # First-write wins; collisions across dirs are graph-cleanup issues,
            # not our concern.
            index.setdefault(slug, family)
    return index


# ---------------------------------------------------------------------------
# Pattern checks
# ---------------------------------------------------------------------------

def check_patterns(row: dict, slug_type: dict[str, str]) -> list[str]:
    """Return list of pattern names this row matches; empty list = clean."""
    matched: list[str] = []

    if row.get("decision") != "emit_edge":
        return matched

    edge_type = row.get("edge_type")
    target_slug = row.get("target_slug")
    target_family = slug_type.get(target_slug) if target_slug else None
    snippet = row.get("evidence_snippet", "") or ""
    confidence_tier = row.get("confidence_tier")

    # Pattern 1: KNOWS soft-fallback
    if edge_type == "KNOWS" and not KNOWS_PROSE_RE.search(snippet):
        matched.append("knows-without-knowing-prose")

    # Patterns 2-6 + 8: type-contract violations
    contract = EDGE_TYPE_TARGET_CONTRACT.get(edge_type)
    if contract and target_family is not None and target_family not in contract:
        matched.append(f"target-type-mismatch-{edge_type.lower()}")

    # Pattern 8: CONTEMPORARY_WITH with character target
    if edge_type == "CONTEMPORARY_WITH" and target_family == "character":
        matched.append("contemporary-with-character-target")

    # Pattern 7: model self-flagged low-confidence
    if isinstance(confidence_tier, int) and confidence_tier == 3:
        matched.append("confidence-tier-3")

    return matched


# ---------------------------------------------------------------------------
# Batch + file enumeration (mirrors validator's logic)
# ---------------------------------------------------------------------------

def derive_output_paths_from_input(input_paths: list[str]) -> list[str]:
    out: list[str] = []
    for p in input_paths:
        if "/prose-edge-candidates/" in p:
            out.append(
                p.replace("/prose-edge-candidates/", "/prose-edges/")
                 .replace(".candidates.jsonl", ".edges.jsonl")
            )
        elif "/comention-candidates/" in p:
            out.append(
                p.replace("/comention-candidates/", "/prose-edges/")
                 .replace(".candidates.jsonl", ".comention-edges.jsonl")
            )
        elif "/extractions-pass1/" in p:
            parts = p.split("/")
            slug_with_ext = parts[-1]
            base = "/".join(parts[:-1])
            out.append(
                f"{base}/prose-edges/"
                f"{slug_with_ext.replace('.candidates.jsonl', '.pass1-edges.jsonl')}"
            )
        else:
            out.append(p.replace(".candidates.jsonl", ".edges.jsonl"))
    return out


def iter_done_batches(mission_dir: Path, batch_id_filter: str | None = None):
    """Yield (batch_id, [output_file_paths]) for each `done` batch."""
    manifest = mission_dir / "batch-manifest.jsonl"
    if not manifest.exists():
        raise FileNotFoundError(f"No batch-manifest.jsonl at {manifest}")
    with manifest.open() as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("status") != "done":
                continue
            bid = r.get("batch_id")
            if batch_id_filter and bid != batch_id_filter:
                continue
            yield bid, derive_output_paths_from_input(r.get("files", []))


def load_jsonl(path: Path):
    """Yield (line_no, parsed_row) for each non-blank line. Skips parse errors."""
    with path.open() as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                yield i, json.loads(line)
            except json.JSONDecodeError:
                continue


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--mission",
        default="working/missions/2026-05-14-stage4-v1-bulk-sonnet",
        help="Mission directory containing batch-manifest.jsonl",
    )
    p.add_argument(
        "--batch-id",
        help="Process only this batch (default: all done batches)",
    )
    p.add_argument(
        "--nodes-root",
        default="graph/nodes",
        help="Root of typed-node directories",
    )
    p.add_argument(
        "--out-dir",
        default="working/wiki/data",
        help="Output directory for suspicious-edges.jsonl + summary.md",
    )
    p.add_argument(
        "--samples-per-pattern",
        type=int,
        default=5,
        help="How many sample rows to include per pattern in the summary",
    )
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    mission_dir = Path(args.mission)
    nodes_root = Path(args.nodes_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_jsonl = out_dir / "stage4-suspicious-edges.jsonl"
    out_md = out_dir / "stage4-suspicious-edges-summary.md"

    print(f"Building slug→type index from {nodes_root} ...", file=sys.stderr)
    slug_type = build_slug_index(nodes_root)
    print(f"  {len(slug_type):,} slugs indexed", file=sys.stderr)

    pattern_counts: Counter[str] = Counter()
    pattern_samples: dict[str, list[dict]] = defaultdict(list)
    edge_type_by_pattern: dict[str, Counter[str]] = defaultdict(Counter)
    batches_seen = 0
    files_seen = 0
    files_missing = 0
    rows_seen = 0
    flagged_count = 0

    with out_jsonl.open("w") as out_f:
        for batch_id, out_files in iter_done_batches(mission_dir, args.batch_id):
            batches_seen += 1
            if args.verbose:
                print(f"batch={batch_id} files={len(out_files)}", file=sys.stderr)
            for fp in out_files:
                path = Path(fp)
                if not path.exists():
                    files_missing += 1
                    continue
                files_seen += 1
                for line_no, row in load_jsonl(path):
                    rows_seen += 1
                    matched = check_patterns(row, slug_type)
                    if not matched:
                        continue
                    flagged_count += 1
                    enriched = {
                        "batch_id": batch_id,
                        "file": fp,
                        "line_no": line_no,
                        "matched_patterns": matched,
                        "target_type_family": slug_type.get(
                            row.get("target_slug", ""), None
                        ),
                        "row": row,
                    }
                    out_f.write(json.dumps(enriched) + "\n")
                    for pat in matched:
                        pattern_counts[pat] += 1
                        edge_type_by_pattern[pat][row.get("edge_type", "?")] += 1
                        if len(pattern_samples[pat]) < args.samples_per_pattern:
                            pattern_samples[pat].append(enriched)

    # ---------------- summary markdown ----------------
    lines: list[str] = []
    lines.append("# Stage 4 Suspicious Edges — Summary")
    lines.append("")
    lines.append(
        f"Generated by `scripts/wiki-pass2-flag-suspicious-edges.py`. "
        f"This is a flagger, not a blocker — each row below was emitted by "
        f"the Stage 4 classifier and stored to the bucket. A later "
        f"Opus-audit pass will confirm or retract."
    )
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- Mission: `{mission_dir}`")
    if args.batch_id:
        lines.append(f"- Batch filter: `{args.batch_id}`")
    lines.append(f"- Batches scanned (done): {batches_seen}")
    lines.append(f"- Output files scanned: {files_seen} (missing: {files_missing})")
    lines.append(f"- Rows scanned: {rows_seen:,}")
    lines.append(f"- Rows flagged: {flagged_count:,}")
    if rows_seen:
        pct = (flagged_count / rows_seen) * 100
        lines.append(f"- Flag rate: {pct:.2f}%")
    lines.append("")
    lines.append("## Counts by pattern")
    lines.append("")
    lines.append("| Pattern | Count | Top edge_types |")
    lines.append("|---|---:|---|")
    for pat, cnt in pattern_counts.most_common():
        top = ", ".join(
            f"`{et}` ({n})"
            for et, n in edge_type_by_pattern[pat].most_common(5)
        )
        lines.append(f"| `{pat}` | {cnt} | {top} |")
    lines.append("")
    lines.append("## Sample rows per pattern")
    lines.append("")
    for pat, _ in pattern_counts.most_common():
        lines.append(f"### `{pat}`")
        lines.append("")
        for sample in pattern_samples[pat]:
            r = sample["row"]
            src = r.get("source_slug") or r.get("pair_a") or "?"
            tgt = r.get("target_slug") or r.get("pair_b") or "?"
            et = r.get("edge_type", "?")
            ct = r.get("confidence_tier", "?")
            tfam = sample.get("target_type_family") or "—"
            snip = (r.get("evidence_snippet") or "").replace("\n", " ").strip()
            if len(snip) > 200:
                snip = snip[:200] + "…"
            lines.append(
                f"- **{src} → {tgt}** `{et}` tier={ct} "
                f"target_family=`{tfam}` (batch `{sample['batch_id']}`)"
            )
            if snip:
                lines.append(f"  > {snip}")
        lines.append("")

    out_md.write_text("\n".join(lines))

    # ---------------- console report ----------------
    print()
    print(f"Scanned {batches_seen} batches, {files_seen} files, {rows_seen:,} rows")
    print(f"Flagged {flagged_count:,} rows ({len(pattern_counts)} distinct patterns)")
    for pat, cnt in pattern_counts.most_common():
        print(f"  {pat}: {cnt}")
    print()
    print(f"Wrote {out_jsonl}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
