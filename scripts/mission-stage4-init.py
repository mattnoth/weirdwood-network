"""
mission-stage4-init.py — Initialize Stage 4 bulk prose-edge classification mission.

Scans all input candidate files across 3 shapes, groups them into batches by
priority tier, and writes a batch-manifest + initializes mission state directories.

Shapes:
  1. source_target  — working/wiki/pass2-buckets/{bucket_id}/prose-edge-candidates/*.candidates.jsonl
  2. comention      — working/wiki/pass2-buckets/meta-chapters-{book}/comention-candidates/*.candidates.jsonl
  3. pass1_relationship — working/wiki/pass2-buckets/extractions-pass1/{book}/{chapter-slug}.candidates.jsonl

Priority tiers (for source_target):
  Tier 1: characters-* buckets
  Tier 2: artifacts-* buckets
  Tier 3: comention files
  Tier 4: pass1_relationship files
  Tier 5: all other source_target buckets

Usage:
  python3 scripts/mission-stage4-init.py [--batch-size N] [--dry-run] [--mission-dir PATH]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_MISSION_DIR = "working/missions/2026-05-14-stage4-v1-bulk-sonnet"
DEFAULT_BATCH_SIZE = 30

PASS2_BUCKETS = Path("working/wiki/pass2-buckets")
EXTRACTIONS_PASS1 = PASS2_BUCKETS / "extractions-pass1"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_source_target_files(repo_root: Path) -> list[dict]:
    """
    Discover all source_target candidate files.
    These are prose-edge-candidates/*.candidates.jsonl in any bucket directory
    EXCEPT meta-chapters-* (those contribute only via comention shape) and
    extractions-pass1 (which is pass1_relationship shape).
    """
    buckets_dir = repo_root / PASS2_BUCKETS
    files = []

    all_bucket_dirs = sorted(
        d for d in buckets_dir.iterdir()
        if d.is_dir()
        and not d.name.startswith("meta-chapters-")
        and d.name != "extractions-pass1"
    )

    print(f"  Scanning {len(all_bucket_dirs)} source_target bucket directories...")

    for bucket_dir in all_bucket_dirs:
        candidates_dir = bucket_dir / "prose-edge-candidates"
        if not candidates_dir.is_dir():
            continue

        bucket_name = bucket_dir.name
        # Determine priority tier from bucket name prefix
        if bucket_name.startswith("characters-"):
            tier = 1
        elif bucket_name.startswith("artifacts-"):
            tier = 2
        else:
            tier = 5

        for f in sorted(candidates_dir.glob("*.candidates.jsonl")):
            if not f.is_file():
                continue
            files.append({
                "path": f,
                "relative_path": str(f.relative_to(repo_root)),
                "shape": "source_target",
                "priority_tier": tier,
                "bucket_name": bucket_name,
            })

    return files


def discover_comention_files(repo_root: Path) -> list[dict]:
    """
    Discover comention candidate files from meta-chapters-* buckets.
    Path: working/wiki/pass2-buckets/meta-chapters-{book}/comention-candidates/*.candidates.jsonl
    """
    buckets_dir = repo_root / PASS2_BUCKETS
    files = []

    meta_dirs = sorted(
        d for d in buckets_dir.iterdir()
        if d.is_dir() and d.name.startswith("meta-chapters-")
    )

    print(f"  Scanning {len(meta_dirs)} meta-chapters directories for comention files...")

    for meta_dir in meta_dirs:
        comention_dir = meta_dir / "comention-candidates"
        if not comention_dir.is_dir():
            continue

        for f in sorted(comention_dir.glob("*.candidates.jsonl")):
            if not f.is_file():
                continue
            files.append({
                "path": f,
                "relative_path": str(f.relative_to(repo_root)),
                "shape": "comention",
                "priority_tier": 3,
                "bucket_name": meta_dir.name,
            })

    return files


def discover_pass1_relationship_files(repo_root: Path) -> list[dict]:
    """
    Discover pass1_relationship candidate files.
    Path: working/wiki/pass2-buckets/extractions-pass1/{book}/{chapter-slug}.candidates.jsonl
    """
    pass1_dir = repo_root / EXTRACTIONS_PASS1
    files = []

    book_dirs = sorted(
        d for d in pass1_dir.iterdir()
        if d.is_dir() and d.name in BOOKS
    )

    print(f"  Scanning {len(book_dirs)} book directories in extractions-pass1...")

    for book_dir in book_dirs:
        for f in sorted(book_dir.glob("*.candidates.jsonl")):
            if not f.is_file():
                continue
            files.append({
                "path": f,
                "relative_path": str(f.relative_to(repo_root)),
                "shape": "pass1_relationship",
                "priority_tier": 4,
                "bucket_name": f"extractions-pass1/{book_dir.name}",
            })

    return files


# ---------------------------------------------------------------------------
# Batch assembly
# ---------------------------------------------------------------------------

def assemble_batches(all_files: list[dict], batch_size: int) -> list[dict]:
    """
    Group files into tier-homogeneous batches of `batch_size`.
    Files are sorted by priority_tier first, then by relative_path within each tier.
    Batches never mix tiers.
    """
    # Sort: primary by tier, secondary by path (deterministic)
    sorted_files = sorted(all_files, key=lambda f: (f["priority_tier"], f["relative_path"]))

    batches = []
    batch_num = 1
    current_tier = None
    current_batch = []

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def flush_batch(tier, files):
        nonlocal batch_num
        # Determine representative shape (all files in a tier-homogeneous batch share shape)
        shape = files[0]["shape"]
        batch_id = f"batch-{batch_num:04d}"
        batches.append({
            "batch_id": batch_id,
            "shape": shape,
            "priority_tier": tier,
            "file_count": len(files),
            "files": [f["relative_path"] for f in files],
            "status": "queued",
            "created_at": now_utc,
        })
        batch_num += 1

    for file_info in sorted_files:
        tier = file_info["priority_tier"]

        # Tier boundary: flush current batch and start fresh
        if tier != current_tier:
            if current_batch:
                flush_batch(current_tier, current_batch)
                current_batch = []
            current_tier = tier

        current_batch.append(file_info)

        # Size boundary: flush when batch is full
        if len(current_batch) >= batch_size:
            flush_batch(current_tier, current_batch)
            current_batch = []

    # Flush any remaining files
    if current_batch:
        flush_batch(current_tier, current_batch)

    return batches


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_mission_files(mission_dir: Path, batches: list[dict], dry_run: bool) -> None:
    """Create mission directory structure and write batch-manifest + empty state files."""
    if dry_run:
        print(f"\n[dry-run] Would create: {mission_dir}/")
        print(f"[dry-run] Would write:  {mission_dir}/batch-manifest.jsonl  ({len(batches)} rows)")
        print(f"[dry-run] Would create: {mission_dir}/state.jsonl  (empty)")
        print(f"[dry-run] Would create: {mission_dir}/results/  (empty dir)")
        print(f"[dry-run] Would create: {mission_dir}/locks/  (empty dir)")
        return

    if mission_dir.exists():
        print(f"WARNING: Mission directory already exists: {mission_dir}")
        print("         Proceeding — will overwrite batch-manifest.jsonl.")
    else:
        mission_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (mission_dir / "results").mkdir(exist_ok=True)
    (mission_dir / "locks").mkdir(exist_ok=True)

    # Write batch-manifest.jsonl
    manifest_path = mission_dir / "batch-manifest.jsonl"
    with manifest_path.open("w", encoding="utf-8") as fh:
        for batch in batches:
            fh.write(json.dumps(batch) + "\n")
    print(f"Wrote {manifest_path} ({len(batches)} rows)")

    # Create empty state.jsonl
    state_path = mission_dir / "state.jsonl"
    state_path.touch()
    print(f"Wrote {state_path} (empty)")


def build_summary(
    mission_dir: Path,
    all_files: list[dict],
    batches: list[dict],
    batch_size: int,
) -> str:
    """Build the summary string for stdout and init-summary.md."""
    tier_names = {
        1: "Tier 1 (characters source_target)",
        2: "Tier 2 (artifacts source_target)",
        3: "Tier 3 (comention)",
        4: "Tier 4 (pass1_relationship)",
        5: "Tier 5 (other source_target)",
    }

    tier_file_counts = {}
    tier_batch_counts = {}
    for t in tier_names:
        tier_file_counts[t] = sum(1 for f in all_files if f["priority_tier"] == t)
        tier_batch_counts[t] = sum(1 for b in batches if b["priority_tier"] == t)

    lines = [
        "MISSION INIT SUMMARY",
        "====================",
        f"Mission dir: {mission_dir}",
        f"Total files scanned: {len(all_files)}",
    ]
    for t, name in tier_names.items():
        lines.append(f"  {name}: {tier_file_counts[t]} files")
    lines.append(f"Total batches: {len(batches)}")
    for t, name in tier_names.items():
        lines.append(f"  {name}: {tier_batch_counts[t]} batches")
    lines.append(f"Batch size: {batch_size} (tunable via --batch-size)")
    lines.append(f"Output: {mission_dir}/batch-manifest.jsonl")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Initialize Stage 4 bulk prose-edge classification mission."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        metavar="N",
        help=f"Number of files per batch (default: {DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary without writing any files",
    )
    parser.add_argument(
        "--mission-dir",
        type=str,
        default=None,
        metavar="PATH",
        help=f"Override mission output directory (default: {DEFAULT_MISSION_DIR})",
    )
    args = parser.parse_args()

    # Resolve repo root (script lives in scripts/, repo root is parent)
    repo_root = Path(__file__).parent.parent.resolve()

    # Resolve mission dir
    if args.mission_dir:
        mission_dir = Path(args.mission_dir).resolve()
    else:
        mission_dir = repo_root / DEFAULT_MISSION_DIR

    print("Stage 4 Mission Init")
    print("====================")
    print(f"Repo root:    {repo_root}")
    print(f"Mission dir:  {mission_dir}")
    print(f"Batch size:   {args.batch_size}")
    print(f"Dry run:      {args.dry_run}")
    print()

    # --- Discover files ---
    print("Scanning files...")
    print()

    print("Shape 1: source_target")
    source_target_files = discover_source_target_files(repo_root)
    print(f"  Found {len(source_target_files)} source_target files")
    print()

    print("Shape 2: comention")
    comention_files = discover_comention_files(repo_root)
    print(f"  Found {len(comention_files)} comention files")
    print()

    print("Shape 3: pass1_relationship")
    pass1_files = discover_pass1_relationship_files(repo_root)
    print(f"  Found {len(pass1_files)} pass1_relationship files")
    print()

    all_files = source_target_files + comention_files + pass1_files
    print(f"Total files discovered: {len(all_files)}")
    print()

    # --- Assemble batches ---
    print("Assembling batches...")
    batches = assemble_batches(all_files, args.batch_size)
    print(f"Assembled {len(batches)} batches")
    print()

    # --- Write output ---
    write_mission_files(mission_dir, batches, args.dry_run)
    print()

    # --- Summary ---
    summary = build_summary(mission_dir, all_files, batches, args.batch_size)
    print(summary)

    # Write summary to file (unless dry-run)
    if not args.dry_run:
        summary_path = mission_dir / "init-summary.md"
        summary_path.write_text(summary + "\n", encoding="utf-8")
        print(f"\nWrote {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
