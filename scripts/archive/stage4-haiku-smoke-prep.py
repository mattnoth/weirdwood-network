#!/usr/bin/env python3
"""stage4-haiku-smoke-prep.py — Prepare a clean Haiku re-run of batch-0020.

Stage 4 Haiku smoke (2026-05-19). batch-0020 was already classified by Sonnet
(the frozen control arm). To re-run the SAME 30 candidate files through Haiku
for a cross-model comparison, two things must happen:

  1. Archive batch-0020's Sonnet prose-edges output out of the live paths so
     the Haiku run writes fresh (output paths are per-source-slug, not per-batch).
  2. Register the re-run under a NEW batch_id (`batch-0020-haiku-smoke`) so the
     worker's state.jsonl resume-check does not skip files already done by Sonnet.

Idempotent: re-running skips already-archived files and will not double-insert
the manifest row.

Usage:  python3 scripts/stage4-haiku-smoke-prep.py
"""

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MISSION = REPO / "working/missions/2026-05-14-stage4-v1-bulk-sonnet"
MANIFEST = MISSION / "batch-manifest.jsonl"
BUCKETS = REPO / "working/wiki/pass2-buckets"
ARCHIVE = BUCKETS / "_archive/batch-0020-sonnet-control-2026-05-19"

SRC_BATCH = "batch-0020"
SMOKE_BATCH = "batch-0020-haiku-smoke"


def candidate_to_edges(cand_path: str) -> tuple[str, Path, Path]:
    """Map a candidate file path to (bucket, sonnet-edges-path, archive-dest)."""
    parts = cand_path.split("/")
    # working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/<slug>.candidates.jsonl
    bucket = parts[3]
    slug = parts[5].removesuffix(".candidates.jsonl")
    edges = BUCKETS / bucket / "prose-edges" / f"{slug}.edges.jsonl"
    dest = ARCHIVE / bucket / f"{slug}.edges.jsonl"
    return bucket, edges, dest


def main() -> int:
    if not MANIFEST.exists():
        print(f"ERROR: manifest not found: {MANIFEST}", file=sys.stderr)
        return 1

    lines = [ln for ln in MANIFEST.read_text().splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    src_row = next((r for r in rows if r.get("batch_id") == SRC_BATCH), None)
    if src_row is None:
        print(f"ERROR: {SRC_BATCH} not in manifest", file=sys.stderr)
        return 1

    files = src_row["files"]
    print(f"{SRC_BATCH}: {len(files)} candidate files, shape={src_row.get('shape')}")
    print()

    # ── Step 1: archive Sonnet prose-edges output ────────────────────────────
    moved, missing, already = 0, 0, 0
    print(f"Archiving Sonnet output -> {ARCHIVE.relative_to(REPO)}")
    for cand in files:
        bucket, edges, dest = candidate_to_edges(cand)
        if dest.exists() and not edges.exists():
            already += 1
            continue
        if not edges.exists():
            print(f"  (no sonnet output)  {bucket}/{dest.name}")
            missing += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(edges), str(dest))
        print(f"  moved  {bucket}/{dest.name}")
        moved += 1
    print(f"  -> {moved} moved, {already} already archived, {missing} had no sonnet output")
    print()

    # ── Step 2: register the smoke batch row ─────────────────────────────────
    if any(r.get("batch_id") == SMOKE_BATCH for r in rows):
        print(f"Manifest row {SMOKE_BATCH} already present — not re-inserting.")
        return 0

    smoke_row = {
        "batch_id": SMOKE_BATCH,
        "shape": src_row.get("shape", "source_target"),
        "priority_tier": src_row.get("priority_tier", 1),
        "file_count": len(files),
        "files": files,
        "status": "queued",
        "created_at": "2026-05-19T00:00:00Z",
        "note": "Haiku smoke re-run of batch-0020 against R1-patched prompt; "
                "Sonnet control arm archived to _archive/batch-0020-sonnet-control-2026-05-19/",
    }

    # Insert right after the batch-0020 row so the worker (first-queued-by-tier,
    # file order) claims it before the genuine queue (batch-0057+).
    src_idx = next(i for i, r in enumerate(rows) if r.get("batch_id") == SRC_BATCH)
    new_lines = lines[: src_idx + 1] + [json.dumps(smoke_row)] + lines[src_idx + 1 :]

    tmp = MANIFEST.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(new_lines) + "\n")
    tmp.replace(MANIFEST)
    print(f"Inserted manifest row {SMOKE_BATCH} (queued, tier "
          f"{smoke_row['priority_tier']}) after {SRC_BATCH}.")
    print(f"Manifest now {len(new_lines)} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
