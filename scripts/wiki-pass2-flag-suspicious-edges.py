#!/usr/bin/env python3
"""
Stage 4 prose-edge soft-fallback flagger.

Walks all `emit_edge` rows produced by completed Stage 4 batches and tags rows
matching known soft-fallback / semantic-suspicious patterns. Does NOT block or
modify them — only flags for a later Opus audit pass.

Pattern classes (per Session 54 plan):
  1. knows_as_fallback
       edge_type == KNOWS  AND  evidence_snippet contains no knowing-verb
       ("knew", "knows", "know", "known", "learning", "informed", "told",
        "aware of", "told that", "acquainted", etc.)
  2. attends_non_event
       edge_type == ATTENDS  AND  target_type is not event.*
  3. fights_in_non_event
       edge_type == FIGHTS_IN  AND  target_type is not event.*
       (classic pattern: FIGHTS_IN aenys-frey → stannis-baratheon)
  4. killed_by_non_person
       edge_type == KILLED_BY  AND  source_type is not character.* AND not
       creature.* AND not object.weapon
       (e.g., a place listed as the KILLED_BY source)
  5. tier3_weak_evidence
       confidence_tier == 3  AND  (evidence_snippet is empty OR
       len(evidence_snippet.strip()) < 20)
  6. contemporary_with_char_pair
       edge_type == CONTEMPORARY_WITH  AND  both source AND target are
       character.*  (soft-fallback when classifier couldn't pick a more
       specific edge type)

Output:
  working/wiki/data/stage4-suspicious-edges.jsonl   — one row per flagged edge

Row format (flat):
  {
    "source_slug": "...",
    "edge_type": "...",
    "target_slug": "...",
    "qualifier": "..." | null,
    "confidence_tier": N | null,
    "evidence_snippet": "...",
    "evidence_kind": "...",
    "source_batch": "<batch-id>",
    "source_file": "<path to .edges.jsonl>",
    "flag_reasons": ["knows_as_fallback", ...]
  }

Multiple flag_reasons may fire on the same edge row.

Usage:
    python3 scripts/wiki-pass2-flag-suspicious-edges.py
    python3 scripts/wiki-pass2-flag-suspicious-edges.py --dry-run
    python3 scripts/wiki-pass2-flag-suspicious-edges.py --sample 5
    python3 scripts/wiki-pass2-flag-suspicious-edges.py --batch-id batch-0020
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import shutil
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Knowing-verb regex for pattern 1 (KNOWS as fallback)
# ---------------------------------------------------------------------------

KNOWS_PROSE_RE = re.compile(
    r"\b(knew|know|known|knows|knowing|learned of|learnt of|learn(?:ed|s|ing)\b|"
    r"informed|informs|informing|told|tells|telling|"
    r"acquainted|familiar with|recogni[sz]e[sd]?|recogni[sz]ing|"
    r"aware of|met\b|meets|meeting|heard of|hears of|discovers?)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Slug → type-family index from graph/nodes/
# ---------------------------------------------------------------------------

# Map node directory name → type-family prefix for contract checks.
# "characters" → "character", "events" → "event", etc.
DIR_TO_TYPE_FAMILY: dict[str, str] = {
    "characters": "character",
    "events":     "event",
    "locations":  "place",
    "artifacts":  "object.artifact",
    "factions":   "organization",
    "houses":     "organization",
    "religions":  "organization",
    "species":    "creature",
    "titles":     "title",
    "concepts":   "concept",
    "texts":      "text",
    "theories":   "theory",
    "prophecies": "prophecy",
    "foods":      "object.food",
    "materials":  "object.material",
    "customs":    "concept.custom",
    "languages":  "concept.language",
    "medical":    "concept.medical",
    "chapters":   "chapter",
}


def build_slug_index(nodes_root: Path) -> dict[str, str]:
    """Return {slug: type_family} for every node file under nodes_root.

    Cheap: uses the parent directory name; no frontmatter parsing needed.
    Slugs are derived from filenames (<slug>.node.md).
    First-write wins across directories; collisions are graph-cleanup issues.
    """
    index: dict[str, str] = {}
    if not nodes_root.is_dir():
        return index
    for dir_path in nodes_root.iterdir():
        if not dir_path.is_dir():
            continue
        dir_name = dir_path.name
        if dir_name.startswith("_"):
            continue
        family = DIR_TO_TYPE_FAMILY.get(dir_name, dir_name)
        for node_file in dir_path.glob("*.node.md"):
            slug = node_file.stem  # removes .node.md suffix
            if slug.endswith(".node"):
                slug = slug[: -len(".node")]
            index.setdefault(slug, family)
    return index


# ---------------------------------------------------------------------------
# Schema-normalisation helpers (old vs new emit_edge formats coexist)
# ---------------------------------------------------------------------------

def get_source_slug(row: dict) -> str | None:
    return row.get("source_slug") or row.get("source") or None


def get_target_slug(row: dict) -> str | None:
    return row.get("target_slug") or row.get("target") or None


def get_confidence_tier(row: dict) -> int | None:
    """Normalise confidence_tier to int (1/2/3) or None."""
    ct = row.get("confidence_tier")
    if isinstance(ct, int):
        return ct
    # Old schema: "tier-1" / "tier-2" / "tier-3"
    if isinstance(ct, str) and ct.startswith("tier-"):
        try:
            return int(ct.split("-")[1])
        except (IndexError, ValueError):
            pass
    # Some old rows use "confidence" instead of "confidence_tier"
    c = row.get("confidence")
    if isinstance(c, str) and c.startswith("tier-"):
        try:
            return int(c.split("-")[1])
        except (IndexError, ValueError):
            pass
    if isinstance(c, int):
        return c
    return None


# ---------------------------------------------------------------------------
# Pattern checks — return list of flag-reason strings
# ---------------------------------------------------------------------------

def check_patterns(
    row: dict,
    slug_type: dict[str, str],
) -> list[str]:
    """Return list of flag-reason strings; empty = no flags."""
    if row.get("decision") != "emit_edge":
        return []

    edge_type   = row.get("edge_type") or ""
    source_slug = get_source_slug(row) or ""
    target_slug = get_target_slug(row) or ""
    snippet     = row.get("evidence_snippet") or ""
    confidence  = get_confidence_tier(row)

    source_family = slug_type.get(source_slug) if source_slug else None
    target_family = slug_type.get(target_slug) if target_slug else None

    flags: list[str] = []

    # --- Pattern 1: KNOWS as fallback ---
    if edge_type == "KNOWS" and not KNOWS_PROSE_RE.search(snippet):
        flags.append("knows_as_fallback")

    # --- Pattern 2: ATTENDS with non-event target ---
    if edge_type == "ATTENDS":
        if target_family is not None and not target_family.startswith("event"):
            flags.append("attends_non_event")
        elif target_family is None and target_slug:
            # Target slug exists in data but not in slug index — flag it
            flags.append("attends_non_event")

    # --- Pattern 3: FIGHTS_IN with non-event target ---
    if edge_type == "FIGHTS_IN":
        if target_family is not None and not target_family.startswith("event"):
            flags.append("fights_in_non_event")
        elif target_family is None and target_slug:
            flags.append("fights_in_non_event")

    # --- Pattern 4: KILLED_BY with non-person source ---
    if edge_type == "KILLED_BY":
        if source_family is not None:
            is_ok = (
                source_family.startswith("character")
                or source_family.startswith("creature")
                or source_family == "object.artifact"  # weapons
            )
            if not is_ok:
                flags.append("killed_by_non_person")
        elif source_family is None and source_slug:
            # Source not in index but slug present — flag conservatively
            flags.append("killed_by_non_person")

    # --- Pattern 5: Tier-3 with weak/absent evidence snippet ---
    if confidence == 3:
        stripped = snippet.strip()
        if len(stripped) < 20:
            flags.append("tier3_weak_evidence")

    # --- Pattern 6: CONTEMPORARY_WITH on character pair ---
    if edge_type == "CONTEMPORARY_WITH":
        if (source_family is not None and source_family.startswith("character")
                and target_family is not None and target_family.startswith("character")):
            flags.append("contemporary_with_char_pair")

    return flags


# ---------------------------------------------------------------------------
# Batch enumeration via mission manifest
# ---------------------------------------------------------------------------

def derive_output_path(input_path: str) -> str:
    """Convert a candidate input path to the corresponding .edges.jsonl path."""
    if "/prose-edge-candidates/" in input_path:
        return (
            input_path
            .replace("/prose-edge-candidates/", "/prose-edges/")
            .replace(".candidates.jsonl", ".edges.jsonl")
        )
    if "/comention-candidates/" in input_path:
        return (
            input_path
            .replace("/comention-candidates/", "/prose-edges/")
            .replace(".candidates.jsonl", ".comention-edges.jsonl")
        )
    if "/extractions-pass1/" in input_path:
        parts = input_path.rsplit("/", 1)
        base, fname = parts[0], parts[1] if len(parts) > 1 else ""
        return f"{base}/prose-edges/{fname.replace('.candidates.jsonl', '.pass1-edges.jsonl')}"
    return input_path.replace(".candidates.jsonl", ".edges.jsonl")


def iter_done_batches(
    manifest_path: Path,
    repo_root: Path,
    batch_id_filter: str | None = None,
):
    """Yield (batch_id, [absolute Path to output .edges.jsonl]) for each done batch."""
    with manifest_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("status") != "done":
                continue
            bid = r.get("batch_id", "")
            if batch_id_filter and bid != batch_id_filter:
                continue
            out_paths = [
                repo_root / derive_output_path(fp)
                for fp in r.get("files", [])
            ]
            yield bid, out_paths


def load_jsonl(path: Path):
    """Yield parsed rows from a JSONL file; skip blank lines and parse errors."""
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--mission",
        default="working/missions/2026-05-14-stage4-v1-bulk-sonnet",
        help="Mission directory containing batch-manifest.jsonl",
    )
    ap.add_argument(
        "--repo-root",
        default=".",
        help="Repository root (default: current directory)",
    )
    ap.add_argument(
        "--batch-id",
        help="Process only this single batch (default: all done batches)",
    )
    ap.add_argument(
        "--nodes-root",
        default="graph/nodes",
        help="Root of typed-node directories for slug→type index",
    )
    ap.add_argument(
        "--out-dir",
        default="working/wiki/data",
        help="Output directory for stage4-suspicious-edges.jsonl",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report counts but do NOT write output file",
    )
    ap.add_argument(
        "--sample",
        type=int,
        metavar="N",
        help="Process at most N batches (for quick testing)",
    )
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    repo_root   = Path(args.repo_root).resolve()
    mission_dir = repo_root / args.mission
    nodes_root  = repo_root / args.nodes_root
    out_dir     = repo_root / args.out_dir
    manifest    = mission_dir / "batch-manifest.jsonl"

    if not manifest.exists():
        print(f"ERROR: manifest not found at {manifest}", file=sys.stderr)
        return 1

    # --- Build slug→type index ---
    print(f"Building slug→type index from {nodes_root} ...", file=sys.stderr)
    slug_type = build_slug_index(nodes_root)
    print(f"  {len(slug_type):,} slugs indexed", file=sys.stderr)

    # --- Counters ---
    pattern_counts:   Counter[str]              = Counter()
    bucket_counts:    Counter[str]              = Counter()
    pattern_samples:  dict[str, list[dict]]     = defaultdict(list)
    batches_seen  = 0
    files_seen    = 0
    files_missing = 0
    rows_scanned  = 0
    emits_scanned = 0
    flagged_count = 0

    # --- Write to temp file, then atomically rename ---
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "stage4-suspicious-edges.jsonl"
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        dir=out_dir, prefix=".stage4-suspicious-edges.tmp-"
    )

    try:
        with open(tmp_fd, "w", encoding="utf-8") as out_f:
            for batch_id, out_files in iter_done_batches(manifest, repo_root, args.batch_id):
                batches_seen += 1
                if args.sample and batches_seen > args.sample:
                    break
                if args.verbose:
                    print(f"  batch={batch_id}  files={len(out_files)}", file=sys.stderr)

                for fpath in out_files:
                    if not fpath.exists():
                        files_missing += 1
                        continue
                    files_seen += 1

                    for row in load_jsonl(fpath):
                        rows_scanned += 1
                        if row.get("decision") != "emit_edge":
                            continue
                        emits_scanned += 1

                        flags = check_patterns(row, slug_type)
                        if not flags:
                            continue

                        flagged_count += 1
                        source_slug = get_source_slug(row) or ""
                        target_slug = get_target_slug(row) or ""

                        out_row = {
                            "source_slug":     source_slug,
                            "edge_type":       row.get("edge_type") or "",
                            "target_slug":     target_slug,
                            "qualifier":       row.get("qualifier"),
                            "confidence_tier": get_confidence_tier(row),
                            "evidence_snippet": row.get("evidence_snippet") or "",
                            "evidence_kind":   row.get("evidence_kind") or "",
                            "source_batch":    batch_id,
                            "source_file":     str(fpath),
                            "flag_reasons":    flags,
                        }

                        for pat in flags:
                            pattern_counts[pat] += 1
                            bucket_counts[batch_id] += 1
                            if len(pattern_samples[pat]) < 5:
                                pattern_samples[pat].append(out_row)

                        if not args.dry_run:
                            out_f.write(json.dumps(out_row) + "\n")

        if args.dry_run:
            Path(tmp_path_str).unlink(missing_ok=True)
        else:
            shutil.move(tmp_path_str, out_path)

    except Exception:
        Path(tmp_path_str).unlink(missing_ok=True)
        raise

    # --- Stdout summary ---
    print()
    print("=" * 60)
    print("Stage 4 Suspicious-Edges Flagger — Summary")
    print("=" * 60)
    print(f"Batches scanned (done):   {batches_seen}")
    print(f"Output files found:       {files_seen}  (missing: {files_missing})")
    print(f"Total rows scanned:       {rows_scanned:,}")
    print(f"  of which emit_edge:     {emits_scanned:,}")
    print(f"Flagged edges:            {flagged_count:,}", end="")
    if emits_scanned:
        print(f"  ({flagged_count / emits_scanned * 100:.1f}% of emits)", end="")
    print()
    if args.dry_run:
        print("[DRY RUN — no output file written]")
    elif args.sample:
        print(f"[SAMPLE MODE — processed first {args.sample} batches only]")
    print()

    print("Per-pattern flag counts:")
    for pat, cnt in pattern_counts.most_common():
        print(f"  {pat:<35}  {cnt:>5}")

    if pattern_counts:
        print()
        print("Top 5 most-flagged batches:")
        for bid, cnt in bucket_counts.most_common(5):
            print(f"  {bid}:  {cnt}")

    print()
    print("Sample flagged edges per pattern:")
    for pat, _ in pattern_counts.most_common():
        print(f"\n  [{pat}]")
        for s in pattern_samples[pat][:3]:
            print(
                f"    {s['source_slug']} --{s['edge_type']}--> {s['target_slug']}"
                f"  tier={s['confidence_tier']}  batch={s['source_batch']}"
            )
            snip = (s["evidence_snippet"] or "").replace("\n", " ").strip()
            if snip:
                print(f"      snippet: {snip[:100]}")

    print()
    if not args.dry_run and not args.sample:
        print(f"Output: {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
