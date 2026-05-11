#!/usr/bin/env python3
"""Attach prose body to stub-only graph nodes.

For each stub-only graph node with `pass_origin: pass2-wiki-deterministic`,
look up the matching bucket prose file and append its content to the current
node body. Preserves the current frontmatter and existing ## Identity + ##
Edges sections (which carry late-stage parser fixes like date-bleed corrections).

The concat rule mirrors wiki-pass2-promote.py:
    final_bytes = current_node_bytes_stripped_trailing_blank + b"\n" + prose_bytes

Existing prose-already-attached nodes (have ## Origins or ## Narrative Arc or
## Appearances section in body) are not touched.

Skip rules:
  - pass_origin != pass2-wiki-deterministic   → SKIP (Stage 1 agent-rich)
  - node already has prose section            → SKIP
  - prose file missing or empty               → SKIP (leave stub)

Reads `working/audits/wiki-prose-coverage-2026-05-12/execution/coverage.jsonl`
if available (faster) — otherwise rebuilds the index in-process.

Usage:
  python3 scripts/wiki-pass2-attach-prose.py             # dry-run
  python3 scripts/wiki-pass2-attach-prose.py --apply
  python3 scripts/wiki-pass2-attach-prose.py --apply --limit 10   # smoke-test
  python3 scripts/wiki-pass2-attach-prose.py --slug walgrave      # single-node
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
BUCKETS_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
COVERAGE_JSONL = (
    PROJECT_ROOT
    / "working"
    / "audits"
    / "wiki-prose-coverage-2026-05-12"
    / "execution"
    / "coverage.jsonl"
)
SUMMARY_OUT = (
    PROJECT_ROOT
    / "working"
    / "audits"
    / "wiki-prose-coverage-2026-05-12"
    / "execution"
    / "attach-prose-summary.json"
)


def atomic_write(dest_path: Path, data: bytes) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    staging = dest_path.parent / f".staging-{dest_path.name}.tmp"
    try:
        staging.write_bytes(data)
        os.rename(staging, dest_path)
    except Exception:
        try:
            staging.unlink(missing_ok=True)
        except Exception:
            pass
        raise


def load_coverage_rows() -> list[dict]:
    if not COVERAGE_JSONL.exists():
        print(
            f"ERROR: coverage.jsonl not found at {COVERAGE_JSONL}\n"
            "Run scripts/audit-prose-coverage.py first.",
            file=sys.stderr,
        )
        sys.exit(1)
    rows = []
    with open(COVERAGE_JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def find_prose_path(slug: str, recorded_bucket: str | None) -> Path | None:
    """Return the largest non-empty prose file path for this slug, or None."""
    candidates: list[Path] = []
    if recorded_bucket:
        cand = BUCKETS_DIR / recorded_bucket / "prose" / f"{slug}.prose.md"
        if cand.exists() and cand.stat().st_size > 0:
            return cand
    # Fallback: scan all buckets
    for p in BUCKETS_DIR.glob(f"*/prose/{slug}.prose.md"):
        if p.stat().st_size > 0:
            candidates.append(p)
    if not candidates:
        return None
    candidates.sort(key=lambda p: -p.stat().st_size)
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write files (default: dry-run).")
    parser.add_argument("--limit", type=int, default=None, help="Cap nodes touched.")
    parser.add_argument("--slug", default=None, help="Process a single slug only.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    rows = load_coverage_rows()
    print(f"Loaded {len(rows):,} coverage rows.")

    # Filter
    candidates: list[dict] = []
    for r in rows:
        if args.slug and r["slug"] != args.slug:
            continue
        if not r["is_stub"]:
            continue
        if r["pass_origin"] != "pass2-wiki-deterministic":
            continue
        if not r["has_prose_file"]:
            continue
        candidates.append(r)

    if args.limit is not None:
        candidates = candidates[: args.limit]

    print(f"Candidates: {len(candidates):,} stub-only deterministic nodes with prose")
    if not candidates:
        return 0

    stats = {
        "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "apply": args.apply,
        "candidates_total": len(candidates),
        "attached": 0,
        "skipped_no_prose_file": 0,
        "skipped_already_has_prose": 0,
        "skipped_other": 0,
        "by_type": {},
    }

    for r in candidates:
        slug = r["slug"]
        node_path = PROJECT_ROOT / r["node_path"]
        if not node_path.exists():
            stats["skipped_other"] += 1
            continue
        current_bytes = node_path.read_bytes()
        current_text = current_bytes.decode("utf-8", errors="replace")

        # Double-check: not already populated
        if any(
            h in current_text
            for h in ("\n## Origins", "\n## Narrative Arc", "\n## Appearances", "\n## Culture", "\n## Organization")
        ):
            stats["skipped_already_has_prose"] += 1
            if args.verbose:
                print(f"  SKIP (already has prose): {slug}")
            continue

        prose_path = find_prose_path(slug, r.get("prose_bucket"))
        if prose_path is None:
            stats["skipped_no_prose_file"] += 1
            if args.verbose:
                print(f"  SKIP (no prose file): {slug}")
            continue
        prose_bytes = prose_path.read_bytes()
        if not prose_bytes.strip():
            stats["skipped_no_prose_file"] += 1
            continue

        # Concat: ensure exactly one trailing newline on current, then "\n" then prose.
        body_bytes = current_bytes
        if not body_bytes.endswith(b"\n"):
            body_bytes += b"\n"
        # Strip extra trailing blank lines to keep output tidy
        while body_bytes.endswith(b"\n\n"):
            body_bytes = body_bytes[:-1]
        final_bytes = body_bytes + b"\n" + prose_bytes
        # Ensure single trailing newline
        while final_bytes.endswith(b"\n\n"):
            final_bytes = final_bytes[:-1]
        if not final_bytes.endswith(b"\n"):
            final_bytes += b"\n"

        if args.apply:
            atomic_write(node_path, final_bytes)
        stats["attached"] += 1
        t = r["type"]
        stats["by_type"][t] = stats["by_type"].get(t, 0) + 1

        if args.verbose:
            print(
                f"  {'ATTACHED' if args.apply else 'WOULD-ATTACH'}: {slug:<40s} "
                f"(+{len(prose_bytes):,} bytes from {prose_path.parent.parent.name})"
            )

    print()
    print("=" * 60)
    print(f"Mode:                {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Candidates:          {stats['candidates_total']:,}")
    print(f"Attached:            {stats['attached']:,}")
    print(f"Skipped already-has-prose: {stats['skipped_already_has_prose']:,}")
    print(f"Skipped no-prose:    {stats['skipped_no_prose_file']:,}")
    print(f"Skipped other:       {stats['skipped_other']:,}")
    if stats["by_type"]:
        print("By type (top 15):")
        for t, n in sorted(stats["by_type"].items(), key=lambda kv: -kv[1])[:15]:
            print(f"  {t:<40s} {n:,}")
    print("=" * 60)

    if args.apply and not args.slug and args.limit is None:
        SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_OUT.write_text(
            json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"\nSummary written to: {SUMMARY_OUT}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
