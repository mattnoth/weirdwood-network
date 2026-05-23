"""Stage 4 — Design Step 4: Deprecate-stamp wiki comention edge output files.

Context
-------
The Weirwood Network pipeline originally produced co-mention ("comention") edges
by running a wiki-prose summarization pass (the "wiki-comention" approach), which
paired any two entities that appeared together in a chapter summary.  That
approach is DEPRECATED in favor of the Pass-1-derived deterministic edge
pipeline decided in Session 65 (2026-05-18, see worklog Active Decisions:
"Stage-4 Pass-1-derived pivot").

This script is design step 4 of that pivot: stamp the DEPRECATED comention
output files IN-DATA.  Files are not moved, deleted, or archived — provenance
lives in the data, which is the project's root-cause fix for
archiving-contention (history/session-details precedent).

Target files
------------
All files matching:
    working/wiki/pass2-buckets/**/prose-edges*/**/*.comention-edges.jsonl

These are JSONL files (one JSON object per line, possible blank lines).  For
every non-blank JSON row that has NOT already been stamped, three fields are
appended (key order preserved — existing keys come first):

    "status": "superseded"
    "superseded_by": "pass1-derived"
    "do_not_promote": true

Idempotency
-----------
A row is considered already-stamped when it contains ``"status": "superseded"``.
Running the script twice produces identical output — the second run reports 0
rows changed.

Usage
-----
Dry-run (safe default — prints what WOULD change, writes nothing):

    python3 scripts/stage4-deprecate-comention-stamp.py

Apply (actually writes):

    python3 scripts/stage4-deprecate-comention-stamp.py --apply

Both modes assert that exactly 133 files are found and halt if the count
differs.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GLOB_PATTERN = "working/wiki/pass2-buckets/**/prose-edges*/**/*.comention-edges.jsonl"
EXPECTED_FILE_COUNT = 133

STAMP_FIELDS = {
    "status": "superseded",
    "superseded_by": "pass1-derived",
    "do_not_promote": True,
}


def find_target_files(repo_root: Path) -> list[Path]:
    """Return all comention-edges.jsonl files under pass2-buckets, sorted."""
    return sorted(repo_root.glob(GLOB_PATTERN))


def stamp_row(row: dict) -> dict:
    """Return a new dict with STAMP_FIELDS appended (existing fields first).

    If the row is already stamped (status == "superseded"), returns the
    original object unchanged.
    """
    if row.get("status") == "superseded":
        return row
    stamped = dict(row)
    stamped.update(STAMP_FIELDS)
    return stamped


def process_file(
    path: Path, *, apply: bool
) -> tuple[int, int, int]:
    """Process one JSONL file.

    Returns (rows_total, rows_changed, rows_already_stamped).
    When apply=False, nothing is written.
    """
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

    rows_total = 0
    rows_changed = 0
    rows_already_stamped = 0
    out_lines: list[str] = []

    for raw in lines:
        stripped = raw.rstrip("\n").rstrip("\r")
        if stripped == "":
            # Preserve blank lines exactly.
            out_lines.append(raw)
            continue

        rows_total += 1
        try:
            obj = json.loads(stripped)
        except json.JSONDecodeError as exc:
            print(
                f"  WARNING: JSON parse error in {path.name} — {exc}",
                file=sys.stderr,
            )
            out_lines.append(raw)
            continue

        if obj.get("status") == "superseded":
            rows_already_stamped += 1
            out_lines.append(raw)
        else:
            stamped = stamp_row(obj)
            rows_changed += 1
            # Preserve trailing newline style of original line.
            newline = raw[len(raw.rstrip("\n\r")):]
            if not newline:
                newline = "\n"
            out_lines.append(json.dumps(stamped, ensure_ascii=False) + newline)

    if apply and rows_changed > 0:
        path.write_text("".join(out_lines), encoding="utf-8")

    return rows_total, rows_changed, rows_already_stamped


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Deprecate-stamp wiki comention edge JSONL files (design step 4, "
            "Pass-1-derived pivot).  Defaults to --dry-run."
        )
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Report what WOULD change without writing anything (default).",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Actually write the stamped files.",
    )
    args = parser.parse_args()

    applying = args.apply

    files = find_target_files(REPO_ROOT)
    found = len(files)

    print(f"Found {found} comention-edges.jsonl files (expected {EXPECTED_FILE_COUNT}).")

    if found != EXPECTED_FILE_COUNT:
        print(
            f"ERROR: Expected exactly {EXPECTED_FILE_COUNT} files, found {found}. "
            "Halting — do not proceed until the discrepancy is resolved.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Mode: {'APPLY' if applying else 'DRY-RUN (pass --apply to write)'}\n")

    total_files = 0
    total_rows = 0
    total_changed = 0
    total_already = 0

    for path in files:
        rows_total, rows_changed, rows_already = process_file(path, apply=applying)
        total_files += 1
        total_rows += rows_total
        total_changed += rows_changed
        total_already += rows_already

    print("=" * 60)
    print(f"Files processed     : {total_files}")
    print(f"Total JSON rows     : {total_rows}")
    print(f"Rows to stamp       : {total_changed}")
    print(f"Already stamped     : {total_already}")
    if applying:
        print(f"Rows written        : {total_changed}")
    else:
        print("(No files written — dry-run mode)")
    print("=" * 60)


if __name__ == "__main__":
    main()
