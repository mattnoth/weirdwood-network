#!/usr/bin/env python3
"""Stage 3 promotion: concatenate skeleton + prose artifacts into final graph nodes.

Reads skeleton/<slug>.node.md and (optionally) prose/<slug>.prose.md from each
secondary-tier bucket, concatenates them, and atomic-renames the result into
graph/nodes/<type>/<slug>.node.md.

Concatenation rule:
  - If prose file exists and is non-empty:   final = skeleton_bytes + b"\\n" + prose_bytes
  - If prose file is absent or empty (0 bytes): final = skeleton_bytes verbatim

This produces a single blank line between ## Edges (skeleton's last section) and
## Origins (prose's first heading), because skeletons end with exactly one "\\n".

Conflict detection (per-page):
  1. If dest doesn't exist → atomic write.
  2. If dest exists and bytes match → skip silently (idempotent re-run).
  3. If dest exists and bytes differ → write to graph/nodes/_conflicts/, log to
     working/wiki/pass2-buckets/conflicts.jsonl.

Only secondary-tier buckets are processed. Core buckets (already promoted via
Stage 1 / the agent path in wiki-pass2.sh) are skipped.

Type routing uses TYPE_DIR_MAP below — replicates wiki-pass2.sh's TYPE_DIR_MAP
with the full leaf-type coverage from wiki-pass2-emit-deterministic.py.
Unknown types go to graph/nodes/_unclassified/.

Usage:
  python3 scripts/wiki-pass2-promote.py                          # dry-run
  python3 scripts/wiki-pass2-promote.py --apply                  # write nodes
  python3 scripts/wiki-pass2-promote.py --bucket houses-other-h-w
  python3 scripts/wiki-pass2-promote.py --bucket houses-other-h-w --apply
  python3 scripts/wiki-pass2-promote.py -v                       # verbose per-page
"""

import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
CONFLICTS_JSONL = WIKI_PASS2_DIR / "conflicts.jsonl"
SUMMARY_FILE = PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "stage3-promote-summary.json"

# ---------------------------------------------------------------------------
# Type → directory mapping
# Replicates wiki-pass2.sh TYPE_DIR_MAP with leaf-type coverage from
# wiki-pass2-emit-deterministic.py.  Most-specific match wins; falls back to
# parent prefix (e.g. "character.human" → "characters" via leaf; then
# "character" → "characters" via parent prefix).
# ---------------------------------------------------------------------------
TYPE_DIR_MAP: dict[str, str] = {
    # Character leaves
    "character.human": "characters",
    "character.direwolf": "characters",
    "character.dragon": "characters",
    "character.giant": "characters",
    "character.cotf": "characters",
    "character.other": "characters",
    # Character parent
    "character": "characters",
    # Organization leaves
    "organization.house": "houses",
    "organization.faction": "factions",
    "organization.cult": "factions",
    "organization.religion": "religions",
    # Organization parent
    "organization": "factions",
    # Place leaves
    "place.location": "locations",
    "place.region": "locations",
    "place.castle": "locations",
    "place.city": "locations",
    # Place parent
    "place": "locations",
    # Artifact leaves
    "artifact": "artifacts",
    "artifact.weapon": "artifacts",
    "artifact.armor": "artifacts",
    # Object (alternate spelling in some pages)
    "object": "artifacts",
    "object.artifact": "artifacts",
    "object.text": "texts",
    "object.food": "foods",
    "object.material": "materials",
    # Event leaves
    "event.battle": "events",
    "event.tournament": "events",
    "event.war": "events",
    # Event parent (shell script has "battle" and "war" as top-level too)
    "event": "events",
    "battle": "events",
    "war": "events",
    # Concept
    "concept": "concepts",
    "concept.culture": "concepts",
    "concept.magic": "concepts",
    "concept.prophecy": "prophecies",
    "concept.theory": "theories",
    "concept.language": "languages",
    "concept.medical": "medical",
    "concept.custom": "customs",
    # Top-level
    "species": "species",
    "title": "titles",
    "prophecy": "prophecies",
    "theory": "theories",
    "text": "texts",
    # Meta (out-of-universe)
    "meta.chapter": "chapters",
    "meta": "chapters",
}


def resolve_type_dir(entity_type: str) -> str | None:
    """Map entity_type string to a graph/nodes/ subdirectory name.

    Returns None if the type is unrecognised (caller routes to _unclassified).
    """
    # Exact match first
    if entity_type in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[entity_type]
    # Parent-prefix fallback: "character.human" → "character"
    parent = entity_type.split(".")[0]
    if parent in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[parent]
    return None


# ---------------------------------------------------------------------------
# Core-bucket detection (mirrors wiki-pass2-emit-deterministic.py)
# ---------------------------------------------------------------------------
_SPLIT_SUFFIX = r"(-[a-z]([0-9]+)?(-[a-z]([0-9]+)?)?)?$"
CORE_TIER_PATTERNS = [
    re.compile(r"^direwolves" + _SPLIT_SUFFIX),
    re.compile(
        r"^characters-house-(stark|lannister|targaryen|baratheon|"
        r"greyjoy|tully|arryn|tyrell|martell)" + _SPLIT_SUFFIX
    ),
    re.compile(
        r"^houses-(north|westerlands|crownlands|riverlands|vale|"
        r"reach|stormlands|dorne|iron-islands)" + _SPLIT_SUFFIX
    ),
    re.compile(
        r"^(north|westerlands|crownlands|riverlands|vale|reach|"
        r"stormlands|dorne|iron-islands)-locations" + _SPLIT_SUFFIX
    ),
]


def is_core_bucket(bucket_id: str) -> bool:
    """Return True if this bucket is a core (Stage 1) bucket that should be skipped."""
    for pat in CORE_TIER_PATTERNS:
        if pat.match(bucket_id):
            return True
    return False


# ---------------------------------------------------------------------------
# Frontmatter parser — extract `type:` field from YAML block
# ---------------------------------------------------------------------------

def read_entity_type(skeleton_bytes: bytes) -> str:
    """Parse `type:` from the YAML frontmatter of a skeleton node.

    Returns the raw value string (e.g. "organization.faction") or "unknown"
    if not found.
    """
    # Frontmatter is between the first two `---` lines
    text = skeleton_bytes.decode("utf-8", errors="replace")
    # Quick regex scan — frontmatter is always at the top
    m = re.search(r"^type:\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "unknown"


# ---------------------------------------------------------------------------
# Atomic write helper
# ---------------------------------------------------------------------------

def atomic_write(dest_path: Path, data: bytes) -> None:
    """Write data to dest_path atomically via a temp file in the same directory.

    Uses a staging temp file named .staging-<slug>.tmp in the same directory
    so that os.rename is on the same filesystem (atomic on POSIX).
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    staging = dest_path.parent / f".staging-{dest_path.name}.tmp"
    try:
        staging.write_bytes(data)
        os.rename(staging, dest_path)
    except Exception:
        # Best-effort cleanup
        try:
            staging.unlink(missing_ok=True)
        except Exception:
            pass
        raise


# ---------------------------------------------------------------------------
# Conflict logging
# ---------------------------------------------------------------------------

def log_conflict(
    slug: str,
    bucket_id: str,
    conflict_path: Path,
    existing_node_path: Path,
) -> None:
    """Append one conflict record to working/wiki/pass2-buckets/conflicts.jsonl."""
    row = {
        "page": slug,
        "bucket_id": bucket_id,
        "conflict_path": str(conflict_path),
        "existing_node_path": str(existing_node_path),
        "detected_at": datetime.now(timezone.utc).isoformat(),
    }
    CONFLICTS_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFLICTS_JSONL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Per-bucket processing
# ---------------------------------------------------------------------------

def process_bucket(
    manifest_path: Path,
    apply: bool,
    verbose: bool,
) -> dict:
    """Process one secondary bucket.  Returns a stats dict.

    Stats keys:
      bucket_id, promoted, already_promoted_byte_equal, conflicted,
      missing_skeleton, unclassified_type, pages_promoted (list)
    """
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        bucket_id = manifest_path.parent.name
        print(f"  ERROR reading manifest {manifest_path}: {exc}", file=sys.stderr)
        return {
            "bucket_id": bucket_id,
            "error": str(exc),
            "promoted": 0,
            "already_promoted_byte_equal": 0,
            "conflicted": 0,
            "missing_skeleton": 0,
            "unclassified_type": 0,
            "pages_promoted": [],
            "type_dist": Counter(),
            "dest_dist": Counter(),
        }

    bucket_id = manifest["bucket_id"]
    bucket_dir = manifest_path.parent
    skeleton_dir = bucket_dir / "skeleton"
    prose_dir = bucket_dir / "prose"

    # Enumerate Tier A + Tier B pages (skip Tier C entirely)
    priority = manifest.get("priority", {})
    tier_a: list[str] = priority.get("tier_a", [])
    tier_b: list[str] = priority.get("tier_b", [])
    pages_to_process = tier_a + tier_b

    stats: dict = {
        "bucket_id": bucket_id,
        "promoted": 0,
        "already_promoted_byte_equal": 0,
        "conflicted": 0,
        "missing_skeleton": 0,
        "unclassified_type": 0,
        "pages_promoted": [],
        "type_dist": Counter(),
        "dest_dist": Counter(),
        "unclassified": [],
    }

    if not pages_to_process:
        if verbose:
            print(f"  {bucket_id}: no Tier A/B pages")
        return stats

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")

    for page_name in pages_to_process:
        # Derive slug (must match wiki-pass2-emit-deterministic.py::page_to_slug)
        slug = page_to_slug(page_name)

        # --- Locate skeleton (required) ---
        skeleton_path = skeleton_dir / f"{slug}.node.md"
        if not skeleton_path.exists():
            if verbose:
                print(f"    MISSING skeleton: {slug}.node.md (page={page_name!r})")
            stats["missing_skeleton"] += 1
            continue

        skeleton_bytes = skeleton_path.read_bytes()

        # --- Locate prose (optional) ---
        prose_path = prose_dir / f"{slug}.prose.md"
        if prose_path.exists():
            prose_bytes = prose_path.read_bytes()
        else:
            prose_bytes = b""

        # --- Concatenate ---
        if prose_bytes:
            final_bytes = skeleton_bytes + b"\n" + prose_bytes
        else:
            final_bytes = skeleton_bytes

        # --- Resolve destination directory ---
        entity_type = read_entity_type(skeleton_bytes)
        dest_subdir = resolve_type_dir(entity_type)
        if dest_subdir is None:
            dest_dir = GRAPH_NODES_DIR / "_unclassified"
            stats["unclassified_type"] += 1
            stats["unclassified"].append(
                {"page": page_name, "slug": slug, "type": entity_type}
            )
            if verbose:
                print(
                    f"    UNCLASSIFIED type={entity_type!r}: {slug} → _unclassified/"
                )
        else:
            dest_dir = GRAPH_NODES_DIR / dest_subdir

        stats["type_dist"][entity_type] += 1
        stats["dest_dist"][dest_subdir or "_unclassified"] += 1

        dest_path = dest_dir / f"{slug}.node.md"

        # --- Conflict detection ---
        outcome: str  # "promoted" | "byte_equal" | "conflict"

        if not dest_path.exists():
            # Happy path: new node
            if apply:
                atomic_write(dest_path, final_bytes)
            outcome = "promoted"
            stats["promoted"] += 1

        else:
            existing_bytes = dest_path.read_bytes()
            if existing_bytes == final_bytes:
                # Idempotent re-run: skip silently
                outcome = "byte_equal"
                stats["already_promoted_byte_equal"] += 1
            else:
                # Conflict: different content already at dest
                conflict_name = f"{slug}-{bucket_id}-{now_iso}.node.md"
                conflict_path = GRAPH_NODES_DIR / "_conflicts" / conflict_name

                if apply:
                    atomic_write(conflict_path, final_bytes)
                    log_conflict(slug, bucket_id, conflict_path, dest_path)

                outcome = "conflict"
                stats["conflicted"] += 1
                print(
                    f"  CONFLICT: {slug}.node.md already exists with different bytes "
                    f"→ {conflict_name}"
                )

        stats["pages_promoted"].append(
            {
                "page": page_name,
                "slug": slug,
                "entity_type": entity_type,
                "dest": str(dest_path),
                "outcome": outcome,
                "has_prose": bool(prose_bytes),
            }
        )

        if verbose:
            prose_tag = "skeleton+prose" if prose_bytes else "skeleton-only"
            print(
                f"    [{outcome:10s}] {slug:<50s} type={entity_type} ({prose_tag})"
            )

    # --- Update manifest on --apply ---
    if apply:
        try:
            manifest["stage3_promoted_at"] = datetime.now(timezone.utc).isoformat()
            manifest["stage3_promoted_count"] = stats["promoted"]
            manifest["stage3_skipped_count"] = stats["already_promoted_byte_equal"]
            manifest["stage3_conflicted_count"] = stats["conflicted"]
            manifest_path.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"  WARNING: could not update manifest {manifest_path}: {exc}", file=sys.stderr)

    return stats


# ---------------------------------------------------------------------------
# Slug generation — must match wiki-pass2-emit-deterministic.py exactly
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    """Convert a wiki page name to a filesystem slug."""
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help=(
            "Write final nodes to graph/nodes/, update manifests, write summary. "
            "Without --apply, prints stats only — no filesystem writes."
        ),
    )
    parser.add_argument(
        "--bucket",
        metavar="BUCKET_ID",
        default=None,
        help="Process a single bucket only (by bucket_id directory name).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-page outcome within each bucket.",
    )
    args = parser.parse_args()

    mode_label = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n=== Stage 3 promotion [{mode_label}] ===")

    # --- Discover manifests ---
    if args.bucket:
        bucket_dir = WIKI_PASS2_DIR / args.bucket
        manifest_path = bucket_dir / "manifest.json"
        if not manifest_path.exists():
            print(f"ERROR: No manifest at {manifest_path}", file=sys.stderr)
            sys.exit(1)
        manifest_paths = [manifest_path]
    else:
        manifest_paths = sorted(WIKI_PASS2_DIR.glob("*/manifest.json"))

    # --- Filter to secondary buckets only ---
    secondary_manifests: list[Path] = []
    core_skipped = 0

    for mpath in manifest_paths:
        bucket_id = mpath.parent.name
        try:
            manifest = json.loads(mpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if manifest.get("tier") == "core" or is_core_bucket(bucket_id):
            core_skipped += 1
            continue
        secondary_manifests.append(mpath)

    print(f"Secondary buckets to process: {len(secondary_manifests)}")
    if core_skipped and not args.bucket:
        print(f"Core buckets skipped (already promoted via Stage 1): {core_skipped}")
    print()

    # --- Process ---
    all_stats: list[dict] = []
    for mpath in secondary_manifests:
        bucket_id = mpath.parent.name
        if args.verbose:
            print(f"  Bucket: {bucket_id}")
        stats = process_bucket(mpath, apply=args.apply, verbose=args.verbose)
        all_stats.append(stats)
        if not args.verbose:
            total = (
                stats["promoted"]
                + stats["already_promoted_byte_equal"]
                + stats["conflicted"]
            )
            print(
                f"  {bucket_id}: {stats['promoted']} promoted, "
                f"{stats['already_promoted_byte_equal']} byte-equal, "
                f"{stats['conflicted']} conflicts, "
                f"{stats['missing_skeleton']} missing-skeleton"
                + (f", {stats['unclassified_type']} unclassified" if stats["unclassified_type"] else "")
            )

    # --- Aggregate ---
    total_promoted = sum(s["promoted"] for s in all_stats)
    total_byte_equal = sum(s["already_promoted_byte_equal"] for s in all_stats)
    total_conflicted = sum(s["conflicted"] for s in all_stats)
    total_missing_skeleton = sum(s["missing_skeleton"] for s in all_stats)
    total_unclassified = sum(s["unclassified_type"] for s in all_stats)

    type_dist: Counter = Counter()
    dest_dist: Counter = Counter()
    all_unclassified: list[dict] = []
    for s in all_stats:
        type_dist.update(s.get("type_dist", {}))
        dest_dist.update(s.get("dest_dist", {}))
        all_unclassified.extend(s.get("unclassified", []))

    print()
    print("=" * 60)
    print(f"Buckets processed:                {len(all_stats)}")
    if core_skipped:
        print(f"Core buckets skipped:             {core_skipped}")
    print(f"Pages promoted (new writes):      {total_promoted}")
    print(f"Pages byte-equal (skipped):       {total_byte_equal}")
    print(f"Pages conflicted:                 {total_conflicted}")
    print(f"Pages missing skeleton:           {total_missing_skeleton}")
    print(f"Pages with unclassified type:     {total_unclassified}")
    print()

    if type_dist:
        print("Type distribution (top 20):")
        for t, n in type_dist.most_common(20):
            print(f"  {t:<45s} {n:>6,}")
        print()

    if dest_dist:
        print("Destination directories used:")
        for d, n in sorted(dest_dist.items()):
            print(f"  graph/nodes/{d:<30s} {n:>6,}")
        print()

    if all_unclassified:
        print(f"Unclassified pages ({len(all_unclassified)}) → graph/nodes/_unclassified/:")
        for entry in all_unclassified[:20]:
            print(f"  {entry['slug']}  (type={entry['type']!r})")
        if len(all_unclassified) > 20:
            print(f"  ... and {len(all_unclassified) - 20} more")
        print()

    if total_conflicted:
        print(f"WARNING: {total_conflicted} conflict(s) detected. See graph/nodes/_conflicts/ and {CONFLICTS_JSONL}")

    print("=" * 60)

    # --- Write summary JSON ---
    if args.apply:
        summary = {
            "version": "v1",
            "ran_at": datetime.now(timezone.utc).isoformat(),
            "buckets_processed": len(all_stats),
            "core_buckets_skipped": core_skipped,
            "pages_promoted": total_promoted,
            "pages_already_promoted_byte_equal": total_byte_equal,
            "pages_conflicted": total_conflicted,
            "pages_missing_skeleton": total_missing_skeleton,
            "pages_unclassified_type": total_unclassified,
            "type_distribution": dict(type_dist.most_common()),
            "destinations_used": dict(sorted(dest_dist.items())),
            "unclassified": all_unclassified,
        }
        SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_FILE.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"\nSummary written to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
