#!/usr/bin/env python3
"""Re-partition the Stage 4 batch manifest from 30-file batches to N-file batches.

Keeps done entries untouched. Re-divides queued entries into smaller sub-batches.
Backs up the original manifest before writing.
"""
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mission-dir", default="working/missions/2026-05-14-stage4-v1-bulk-sonnet")
    p.add_argument("--new-batch-size", type=int, default=5)
    p.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = p.parse_args()

    mission = Path(args.mission_dir)
    manifest_path = mission / "batch-manifest.jsonl"
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    entries = [json.loads(l) for l in manifest_path.read_text().splitlines() if l.strip()]

    done = [e for e in entries if e.get("status") == "done"]
    queued = [e for e in entries if e.get("status") == "queued"]
    other = [e for e in entries if e.get("status") not in ("done", "queued")]

    if other:
        print(f"WARNING: {len(other)} entries with status not in done/queued — will preserve as-is")

    # Determine starting batch number for new sub-batches.
    # Keep done batch_ids untouched. Renumber queued starting from max(done_id) + 1.
    max_done_num = 0
    for e in done:
        n = int(e["batch_id"].split("-")[1])
        if n > max_done_num:
            max_done_num = n
    next_num = max_done_num + 1

    new_entries = []
    new_entries.extend(done)
    new_entries.extend(other)

    bs = args.new_batch_size
    created_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_queued_count = 0
    for old in queued:
        files = old["files"]
        for i in range(0, len(files), bs):
            chunk = files[i : i + bs]
            new_entry = {
                "batch_id": f"batch-{next_num:04d}",
                "shape": old["shape"],
                "priority_tier": old["priority_tier"],
                "file_count": len(chunk),
                "files": chunk,
                "status": "queued",
                "created_at": created_ts,
                "_repartitioned_from": old["batch_id"],
            }
            new_entries.append(new_entry)
            next_num += 1
            new_queued_count += 1

    # Sort: done first (by original order), then queued by batch_id
    new_entries.sort(key=lambda e: (
        0 if e.get("status") == "done" else (1 if e.get("status") == "queued" else 2),
        int(e["batch_id"].split("-")[1]),
    ))

    print(f"Input:  {len(done)} done + {len(queued)} queued (30-file batches)")
    print(f"Output: {len(done)} done + {new_queued_count} queued ({bs}-file batches)")
    print(f"New queued batch IDs: batch-{max_done_num + 1:04d} .. batch-{next_num - 1:04d}")
    print(f"Total file count preserved: {sum(len(e['files']) if isinstance(e.get('files'), list) else 0 for e in new_entries[len(done):])}")

    if not args.apply:
        print("\nDRY RUN — re-run with --apply to write.")
        return

    backup = manifest_path.with_suffix(f".jsonl.bak-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    shutil.copy2(manifest_path, backup)
    print(f"\nBacked up: {backup}")

    with manifest_path.open("w") as f:
        for e in new_entries:
            f.write(json.dumps(e) + "\n")
    print(f"Wrote new manifest: {manifest_path}")


if __name__ == "__main__":
    main()
