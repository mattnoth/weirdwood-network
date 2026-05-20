#!/usr/bin/env python3
"""stage4-haiku-smoke-cleanup.py — Reverse stage4-haiku-smoke-prep.py.

The 2026-05-19 Haiku smoke archived batch-0020's Sonnet prose-edges output and
ran Haiku into the live `prose-edges/` paths. The Haiku worker is now being
rebuilt as a separate Python-orchestrated worker that writes to its own dir, so
this restores the Sonnet mission to its exact pre-smoke state:

  1. Move the 3 Haiku smoke output files OUT of the live `prose-edges/` paths
     into `_archive/batch-0020-haiku-smoke-output-2026-05-19/` (kept, not deleted).
  2. Move the 30 archived Sonnet files back INTO the live `prose-edges/` paths.
  3. Remove the `batch-0020-haiku-smoke` row from the Sonnet batch manifest.

state.jsonl smoke events are left in place (append-only log; harmless).

Usage:  python3 scripts/stage4-haiku-smoke-cleanup.py
"""

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl"
BUCKETS = REPO / "working/wiki/pass2-buckets"
SONNET_ARCHIVE = BUCKETS / "_archive/batch-0020-sonnet-control-2026-05-19"
HAIKU_ARCHIVE = BUCKETS / "_archive/batch-0020-haiku-smoke-output-2026-05-19"

SRC_BATCH = "batch-0020"
SMOKE_BATCH = "batch-0020-haiku-smoke"


def main() -> int:
    lines = [ln for ln in MANIFEST.read_text().splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]
    src_row = next((r for r in rows if r.get("batch_id") == SRC_BATCH), None)
    if src_row is None:
        print(f"ERROR: {SRC_BATCH} not in manifest", file=sys.stderr)
        return 1

    haiku_moved, sonnet_restored = 0, 0
    for cand in src_row["files"]:
        parts = cand.split("/")
        bucket, slug = parts[3], parts[5].removesuffix(".candidates.jsonl")
        live = BUCKETS / bucket / "prose-edges" / f"{slug}.edges.jsonl"
        sonnet_arch = SONNET_ARCHIVE / bucket / f"{slug}.edges.jsonl"

        # 1. a live file here right now is a Haiku smoke output — move it aside
        if live.exists():
            dest = HAIKU_ARCHIVE / bucket / f"{slug}.edges.jsonl"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(live), str(dest))
            print(f"  haiku out   {bucket}/{slug}.edges.jsonl")
            haiku_moved += 1

        # 2. restore the Sonnet original
        if sonnet_arch.exists():
            live.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(sonnet_arch), str(live))
            sonnet_restored += 1
        else:
            print(f"  WARN: no archived Sonnet file for {bucket}/{slug}", file=sys.stderr)

    print(f"-> {haiku_moved} Haiku smoke files set aside, "
          f"{sonnet_restored}/30 Sonnet files restored to prose-edges/")

    # 3. drop the smoke row from the manifest
    new_lines = [ln for ln, r in zip(lines, rows) if r.get("batch_id") != SMOKE_BATCH]
    if len(new_lines) != len(lines):
        tmp = MANIFEST.with_suffix(".jsonl.tmp")
        tmp.write_text("\n".join(new_lines) + "\n")
        tmp.replace(MANIFEST)
        print(f"-> removed {SMOKE_BATCH} row; manifest back to {len(new_lines)} rows")
    else:
        print(f"-> {SMOKE_BATCH} row already absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
