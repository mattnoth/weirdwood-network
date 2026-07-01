#!/usr/bin/env python3
"""dunk-egg-scene-splitter.py — Split a D&E novella source into scene-sized part files.

Driven by a scene-boundary spec JSON produced separately. Writes one markdown part file per
scene into sources/chapters/<unit>/parts/ and emits/refreshes a queue-parts.jsonl file that
the dunk-egg-pass1-extraction.py worker can consume.

Usage:
    python3 scripts/dunk-egg-scene-splitter.py --spec <boundaries.json> [--dry-run]

The spec JSON lives at:
    working/dunk-egg-pass1/scene-boundaries/<unit>.json

Output part files land at:
    sources/chapters/<unit>/parts/<stem>-p0k.md

The parts queue is written to:
    working/dunk-egg-pass1/queue-parts.jsonl
"""

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = next(
    (p for p in [SCRIPT_DIR.parent, SCRIPT_DIR.parent.parent] if (p / "CLAUDE.md").exists()),
    SCRIPT_DIR.parent,
)
QUEUE_PARTS_FILE = PROJECT_ROOT / "working" / "dunk-egg-pass1" / "queue-parts.jsonl"


# ---------------------------------------------------------------------------
# Frontmatter helpers (no yaml dependency — hand-rolled)
# ---------------------------------------------------------------------------
def _parse_frontmatter(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    """Return (header_lines_between_dashes, ordered_dict_of_key->raw_value_str).

    Lines include the leading/trailing '---' markers. Preserves order.
    Parses only simple scalar values (strings, numbers); does not handle YAML lists/dicts.
    """
    if not lines or lines[0].rstrip() != "---":
        return [], {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            end = i
            break
    if end is None:
        return [], {}

    fm_lines = lines[1:end]  # between the two ---
    fields = {}
    order = []
    for line in fm_lines:
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        val = rest.strip()
        if key not in fields:
            order.append(key)
        fields[key] = val
    # Return original fm_lines (for verbatim preservation) plus parsed dict
    return fm_lines, fields


def _render_frontmatter(original_fm_lines: list[str], overrides: dict[str, str]) -> str:
    """Rebuild frontmatter:
    - Keep all original lines verbatim UNLESS their key is in overrides.
    - Append any override keys not already present.
    - Wrap in --- delimiters.
    """
    written_keys = set()
    out_lines = ["---\n"]

    for raw_line in original_fm_lines:
        if ":" in raw_line:
            key = raw_line.partition(":")[0].strip()
            if key in overrides:
                out_lines.append(f"{key}: {overrides[key]}\n")
                written_keys.add(key)
                continue
        out_lines.append(raw_line if raw_line.endswith("\n") else raw_line + "\n")

    # Append override keys not already present (in insertion order)
    for key, val in overrides.items():
        if key not in written_keys:
            out_lines.append(f"{key}: {val}\n")

    out_lines.append("---\n")
    return "".join(out_lines)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def _validate_spec(spec: dict, source_lines: list[str]) -> list[str]:
    """Return a list of error strings. Empty list means valid."""
    errors = []

    # frontmatter_lines validation
    fm = spec.get("frontmatter_lines")
    if not (isinstance(fm, list) and len(fm) == 2):
        errors.append("frontmatter_lines must be a 2-element list [start, end] (1-indexed)")
    else:
        fm_start, fm_end = fm[0] - 1, fm[1] - 1  # 0-indexed
        total = len(source_lines)
        if fm_start < 0 or fm_end >= total:
            errors.append(f"frontmatter_lines [{fm[0]}, {fm[1]}] out of range (total_lines={total})")
        elif source_lines[fm_start].rstrip() != "---":
            errors.append(f"Line {fm[0]} (frontmatter start) is not '---', got: {source_lines[fm_start]!r}")
        elif source_lines[fm_end].rstrip() != "---":
            errors.append(f"Line {fm[1]} (frontmatter end) is not '---', got: {source_lines[fm_end]!r}")

    # body_start_line validation
    body_start = spec.get("body_start_line")
    if not isinstance(body_start, int) or body_start < 1:
        errors.append("body_start_line must be a positive integer")

    # total_lines validation
    total_lines = spec.get("total_lines")
    actual_lines = len(source_lines)
    if isinstance(total_lines, int) and total_lines != actual_lines:
        errors.append(
            f"total_lines={total_lines} in spec but source has {actual_lines} lines"
        )

    parts = spec.get("parts", [])
    if not parts:
        errors.append("parts list is empty")
        return errors  # nothing more to check

    # parts[0].start_line must equal body_start_line
    if isinstance(body_start, int) and parts[0].get("start_line") != body_start:
        errors.append(
            f"parts[0].start_line={parts[0].get('start_line')} != body_start_line={body_start}"
        )

    # Check each part's start_line
    prev_start = None
    for i, part in enumerate(parts):
        pnum = part.get("part", i + 1)
        sl = part.get("start_line")
        if not isinstance(sl, int) or sl < 1:
            errors.append(f"Part {pnum}: start_line must be a positive integer, got {sl!r}")
            continue
        # Strictly increasing
        if prev_start is not None and sl <= prev_start:
            errors.append(
                f"Part {pnum}: start_line={sl} is not strictly greater than previous {prev_start}"
            )
        prev_start = sl

        # 1-indexed, so line index = sl - 1
        idx = sl - 1
        if idx >= len(source_lines):
            errors.append(f"Part {pnum}: start_line={sl} exceeds source length {len(source_lines)}")
            continue
        line_content = source_lines[idx]
        if not line_content.strip():
            errors.append(f"Part {pnum}: start_line={sl} is blank, must be non-blank content")
        # (except part 1, which IS the first body line) preceding line must be blank
        if i > 0 and idx > 0:
            preceding = source_lines[idx - 1]
            if preceding.strip():
                errors.append(
                    f"Part {pnum}: start_line={sl} is not preceded by a blank line "
                    f"(line {sl - 1}={preceding!r})"
                )

    # Part numbers must be contiguous 1..N
    nums = [p.get("part") for p in parts]
    expected = list(range(1, len(parts) + 1))
    if nums != expected:
        errors.append(f"Part numbers must be contiguous 1..N, got {nums}")

    return errors


# ---------------------------------------------------------------------------
# Core splitting logic
# ---------------------------------------------------------------------------
def _word_count(lines: list[str]) -> int:
    return sum(len(line.split()) for line in lines)


def _trim_blank(lines: list[str]) -> list[str]:
    """Strip leading and trailing blank lines."""
    start = 0
    while start < len(lines) and not lines[start].strip():
        start += 1
    end = len(lines)
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def split_novella(spec: dict, source_lines: list[str], dry_run: bool = False) -> int:
    """Perform the split. Return 0 on success, 1 on error."""
    unit_id = spec["unit_id"]
    stem = spec["stem"]
    parts = spec["parts"]
    n = len(parts)
    total_lines = len(source_lines)

    # FM line range (0-indexed)
    fm_start_idx = spec["frontmatter_lines"][0] - 1
    fm_end_idx = spec["frontmatter_lines"][1] - 1
    fm_lines_raw = source_lines[fm_start_idx : fm_end_idx + 1]

    # Parse original frontmatter fields
    inner_fm_lines, fm_fields = _parse_frontmatter(fm_lines_raw)

    # Determine book value for queue rows
    book = fm_fields.get("book", unit_id.upper()).strip('"').strip("'")

    # Determine output directory
    source_path = Path(spec["source"])
    parts_dir = source_path.parent / "parts"

    # Extraction output base
    extractions_dir = PROJECT_ROOT / "extractions" / "mechanical" / unit_id

    print(f"\n{'DRY RUN — ' if dry_run else ''}Scene splitter: {stem} ({n} parts)")
    print(f"  Source:       {source_path}")
    print(f"  Parts dir:    {parts_dir}")
    print(f"  Extractions:  {extractions_dir}")
    print()

    # Table header
    header = f"{'Part':<6} {'Lines':<12} {'Words':<8} {'Scene label':<45} {'Output file'}"
    print(header)
    print("-" * len(header))

    new_rows: list[dict] = []

    for i, part_spec in enumerate(parts):
        k = part_spec["part"]
        part_label = f"p{k:02d}"
        start_line = part_spec["start_line"]
        scene_label = part_spec.get("scene_label", "")
        # end_line is inclusive; last part goes to total_lines
        if i + 1 < n:
            end_line = parts[i + 1]["start_line"] - 1
        else:
            end_line = total_lines

        # Body slice (0-indexed, inclusive on both ends)
        body_lines_raw = source_lines[start_line - 1 : end_line]
        body_lines = _trim_blank(body_lines_raw)
        words = _word_count(body_lines)
        line_count = end_line - start_line + 1

        part_stem = f"{stem}-{part_label}"
        out_filename = f"{part_stem}.md"
        out_path = parts_dir / out_filename
        extraction_out = extractions_dir / f"{part_stem}.extraction.md"

        # Print table row
        label_trunc = scene_label[:44] if len(scene_label) > 44 else scene_label
        print(
            f"  {k:<4} {start_line}-{end_line:<9} {words:<8} {label_trunc:<45} {out_filename}"
        )

        # Build the queue row
        new_rows.append({
            "unit_id": part_stem,
            "book": book,
            "stem": part_stem,
            "source": str(out_path.resolve()),
            "out": str(extraction_out.resolve()),
            "unit_part": f"{k} of {n}",
        })

        if dry_run:
            continue

        # --- Write the part file ---
        parts_dir.mkdir(parents=True, exist_ok=True)

        overrides = {
            "unit_part": f'"{k} of {n}"',
            "part_of": stem,
            "scene_label": f'"{scene_label}"',
            "file_name": out_filename,
        }
        fm_block = _render_frontmatter(inner_fm_lines, overrides)

        body_text = "".join(
            line if line.endswith("\n") else line + "\n" for line in body_lines
        )
        # Ensure single trailing newline on body
        body_text = body_text.rstrip("\n") + "\n"

        content = fm_block + "\n" + body_text
        out_path.write_text(content, encoding="utf-8")

    print()

    if dry_run:
        print("Dry run complete — nothing written.")
        return 0

    # --- Write/refresh queue-parts.jsonl (idempotent: replace rows for this unit) ---
    QUEUE_PARTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing rows, drop any rows for this unit's stems, append new
    existing_rows: list[dict] = []
    if QUEUE_PARTS_FILE.exists():
        for raw in QUEUE_PARTS_FILE.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            # Drop rows belonging to this unit (stem prefix match)
            if not row.get("stem", "").startswith(stem + "-p"):
                existing_rows.append(row)

    all_rows = existing_rows + new_rows
    tmp = QUEUE_PARTS_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        for row in all_rows:
            fh.write(json.dumps(row) + "\n")
    tmp.replace(QUEUE_PARTS_FILE)

    print(f"Wrote {n} part files -> {parts_dir}/")
    print(f"Refreshed queue-parts.jsonl ({len(all_rows)} total rows) -> {QUEUE_PARTS_FILE}")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="dunk-egg-scene-splitter.py",
        description="Split a D&E novella into scene-sized part files from a boundary spec.",
    )
    parser.add_argument(
        "--spec",
        required=True,
        metavar="BOUNDARIES_JSON",
        help="Path to the scene-boundary spec JSON for the novella.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print line ranges/word counts/paths; write nothing.",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    if not spec_path.exists():
        print(f"ERROR: spec file not found: {spec_path}", file=sys.stderr)
        return 1

    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in spec: {e}", file=sys.stderr)
        return 1

    source_path = Path(spec.get("source", "")).resolve()
    if not source_path.exists():
        print(f"ERROR: source file not found: {source_path}", file=sys.stderr)
        return 1

    source_lines = source_path.read_text(encoding="utf-8").splitlines(keepends=True)

    # Validate
    errors = _validate_spec(spec, source_lines)
    if errors:
        print("ERROR: spec validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    return split_novella(spec, source_lines, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
