#!/usr/bin/env python3
"""Split the Dunk & Egg Calibre plaintext into per-novella markdown files with YAML frontmatter.

The input file (TDAE.txt) is a Calibre plaintext conversion of the collected
Tales of Dunk and Egg.  It contains three novellas separated by title lines in
mixed case.  There are no internal chapter divisions — each novella is one
continuous block of prose, so the output is exactly three files.

Usage:
    python scripts/dunk-egg-splitter.py sources/raw/TDAE.txt
    python scripts/dunk-egg-splitter.py sources/raw/TDAE.txt --verbose
    python scripts/dunk-egg-splitter.py sources/raw/TDAE.txt --output /tmp/test/
"""

import argparse
import os
import sys
from pathlib import Path

# Import the normalize helper from the sibling chapter-splitter.py module.
# The filename uses a hyphen so we can't use a plain `import` statement;
# we load it via importlib instead.
import importlib.util as _ilu

_SPLITTER_PATH = Path(__file__).resolve().parent / "chapter-splitter.py"
_spec = _ilu.spec_from_file_location("chapter_splitter", _SPLITTER_PATH)
_chapter_splitter = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_chapter_splitter)
normalize = _chapter_splitter.normalize


# ---------------------------------------------------------------------------
# Novella metadata
# ---------------------------------------------------------------------------
NOVELLAS = [
    {
        "title_line": "The Hedge Knight",
        "code": "thk",
        "book": "THK",
        "pov_character": "Dunk",
        "real_identity": "Duncan the Tall",
        "file_name": "thk-dunk-01.md",
        "pov_label": "Dunk I",
    },
    {
        "title_line": "The Sworn Sword",
        "code": "tss",
        "book": "TSS",
        "pov_character": "Dunk",
        "real_identity": "Duncan the Tall",
        "file_name": "tss-dunk-01.md",
        "pov_label": "Dunk I",
    },
    {
        "title_line": "The Mystery Knight",
        "code": "tmk",
        "book": "TMK",
        "pov_character": "Dunk",
        "real_identity": "Duncan the Tall",
        "file_name": "tmk-dunk-01.md",
        "pov_label": "Dunk I",
    },
]

# Lines that appear between the novella title and the prose — skip them.
SKIP_SUBHEADERS = {
    "a tale of the seven kingdoms",
    "george r.r. martin",
    "george r. r. martin",
}


def build_frontmatter(meta):
    """Render the YAML frontmatter block for a novella file."""
    return (
        f"---\n"
        f"book: {meta['book']}\n"
        f"chapter_number: 1\n"
        f"pov_character: {meta['pov_character']}\n"
        f"real_identity: {meta['real_identity']}\n"
        f"pov_chapter_number: 1\n"
        f'pov_label: "{meta["pov_label"]}"\n'
        f"collection: tales-of-dunk-and-egg\n"
        f"first_available: pre-agot\n"
        f"file_name: {meta['file_name']}\n"
        f"---\n\n"
    )


def find_novella_starts(lines, verbose=False):
    """Locate the line index at which each novella's prose begins.

    Returns a list of (meta_dict, prose_start_line_idx) tuples in order.
    Titles are matched case-insensitively on their own line.  Sub-header lines
    (e.g. "A Tale of the Seven Kingdoms", "George R.R. Martin") that appear
    between the title and the prose are skipped.
    """
    title_targets = {m["title_line"].lower(): m for m in NOVELLAS}

    # Pass 1 — find the line index of each title line.
    title_positions = {}
    for i, raw_line in enumerate(lines):
        stripped = normalize(raw_line).strip()
        key = stripped.lower()
        if key in title_targets and key not in title_positions:
            title_positions[key] = i
            if verbose:
                print(f"  Novella title found at line {i + 1}: {stripped!r}")

    if len(title_positions) != len(NOVELLAS):
        found = list(title_positions.keys())
        missing = [m["title_line"] for m in NOVELLAS if m["title_line"].lower() not in title_positions]
        print(f"WARNING: Expected {len(NOVELLAS)} novella titles, found {len(found)}. Missing: {missing}", file=sys.stderr)

    # Pass 2 — for each title, scan forward past sub-headers and blank lines to
    # find the first line of actual prose.
    results = []
    for meta in NOVELLAS:
        key = meta["title_line"].lower()
        if key not in title_positions:
            continue
        title_idx = title_positions[key]
        prose_start = title_idx + 1
        while prose_start < len(lines):
            candidate = normalize(lines[prose_start]).strip()
            lower_candidate = candidate.lower()
            if not candidate:
                # blank line — skip
                prose_start += 1
            elif lower_candidate in SKIP_SUBHEADERS:
                # sub-header — skip
                if verbose:
                    print(f"    Skipping sub-header at line {prose_start + 1}: {candidate!r}")
                prose_start += 1
            else:
                # First non-blank, non-sub-header line → prose begins here.
                break
        results.append((meta, prose_start))
        if verbose:
            print(f"  Prose of {meta['title_line']!r} starts at line {prose_start + 1}")

    return results


def split_dunk_egg(input_file, output_base_dir, verbose=False):
    """Read TDAE.txt and write one markdown file per novella."""
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if verbose:
        print(f"Read {len(lines)} lines from {input_file}")

    novella_starts = find_novella_starts(lines, verbose=verbose)

    if not novella_starts:
        print("ERROR: No novella titles detected. Aborting.", file=sys.stderr)
        sys.exit(1)

    written = []
    warnings = []

    for idx, (meta, prose_start) in enumerate(novella_starts):
        # The prose block ends just before the next novella's title line, or at
        # EOF if this is the last novella.
        if idx + 1 < len(novella_starts):
            _, next_prose_start = novella_starts[idx + 1]
            # Walk backwards from next_prose_start to find the novella title of
            # the next story (which is the real end boundary).
            # The title is a few lines before next_prose_start — just use the
            # next novella's title position, which we can recover from
            # find_novella_starts.  We already have all line indices from the
            # scan, so recompute quickly.
            next_key = novella_starts[idx + 1][0]["title_line"].lower()
            title_end = next_prose_start  # conservative: stop at prose start
            # More precise: rewind to the blank lines before the title.
            for j in range(next_prose_start - 1, prose_start, -1):
                candidate = normalize(lines[j]).strip()
                if candidate.lower() == next_key:
                    title_end = j
                    break
            prose_end = title_end
        else:
            prose_end = len(lines)

        # Extract the raw text lines and strip leading/trailing blanks.
        text_lines = lines[prose_start:prose_end]
        while text_lines and not text_lines[0].strip():
            text_lines = text_lines[1:]
        while text_lines and not text_lines[-1].strip():
            text_lines = text_lines[:-1]

        chapter_text = normalize("".join(text_lines))

        if not chapter_text.strip():
            warnings.append(f"Empty novella body: {meta['title_line']}")

        word_count = len(chapter_text.split())

        # Write output file.
        out_dir = Path(output_base_dir) / meta["code"]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / meta["file_name"]

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_frontmatter(meta))
            f.write(chapter_text)
            f.write("\n")

        written.append((meta, word_count, out_path))

        if verbose:
            print(f"  Wrote {out_path}  ({len(text_lines)} lines, {word_count:,} words)")

    # --- summary ---
    print(f"\n{'=' * 60}")
    print(f"Dunk & Egg splitter")
    print(f"Input:  {input_file}")
    print(f"Output: {output_base_dir}")
    print(f"Novellas written: {len(written)}")
    print()
    print(f"{'Novella':<25} {'Code':<6} {'Words':>8}  File")
    print(f"{'-' * 25} {'-' * 6} {'-' * 8}  {'-' * 30}")
    for meta, word_count, out_path in written:
        print(f"{meta['title_line']:<25} {meta['code']:<6} {word_count:>8,}  {out_path}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARNING: {w}")

    return written, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Split Dunk & Egg source text into per-novella markdown with YAML frontmatter."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="Path to TDAE.txt (default: sources/raw/TDAE.txt relative to repo root)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Base output directory (default: sources/chapters/ relative to repo root). "
             "Each novella goes into a sub-directory named by its code (thk/, tss/, tmk/).",
    )
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent.parent

    input_file = args.input_file or str(project_dir / "sources" / "raw" / "TDAE.txt")
    output_base_dir = args.output or str(project_dir / "sources" / "chapters")

    if not Path(input_file).exists():
        print(f"ERROR: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    split_dunk_egg(input_file, output_base_dir, verbose=args.verbose)


if __name__ == "__main__":
    main()
