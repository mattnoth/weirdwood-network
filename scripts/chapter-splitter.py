#!/usr/bin/env python3
"""Split ASOIAF source text files into per-chapter markdown files with YAML frontmatter.

Usage:
    python scripts/chapter-splitter.py sources/raw/GoT.txt agot
    python scripts/chapter-splitter.py sources/raw/ACOK.txt acok --verbose
    python scripts/chapter-splitter.py sources/raw/GoT.txt agot --output /tmp/test/
"""

import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Known chapter headings → filename slugs
# Keys are ALL-CAPS with straight apostrophes (source files use smart quotes,
# which are normalised before matching).
# ---------------------------------------------------------------------------
POV_HEADINGS = {
    # Special
    "PROLOGUE": "prologue",
    "EPILOGUE": "epilogue",

    # Standard character names (multi-book)
    "BRAN": "bran",
    "CATELYN": "catelyn",
    "DAENERYS": "daenerys",
    "EDDARD": "eddard",
    "JON": "jon",
    "ARYA": "arya",
    "TYRION": "tyrion",
    "SANSA": "sansa",
    "THEON": "theon",
    "DAVOS": "davos",
    "JAIME": "jaime",
    "SAMWELL": "samwell",
    "BRIENNE": "brienne",
    "CERSEI": "cersei",
    "ALAYNE": "alayne",
    "MELISANDRE": "melisandre",
    "BARRISTAN": "barristan",
    "VICTARION": "victarion",
    "QUENTYN": "quentyn",
    "JON CONNINGTON": "jon-connington",

    # AFFC descriptive titles
    "THE PROPHET": "the-prophet",
    "THE DROWNED MAN": "the-drowned-man",
    "THE IRON CAPTAIN": "the-iron-captain",
    "THE REAVER": "the-reaver",
    "THE KRAKEN'S DAUGHTER": "the-krakens-daughter",
    "THE CAPTAIN OF GUARDS": "the-captain-of-guards",
    "THE SOILED KNIGHT": "the-soiled-knight",
    "THE QUEENMAKER": "the-queenmaker",
    "THE PRINCESS IN THE TOWER": "the-princess-in-the-tower",
    "CAT OF THE CANALS": "cat-of-the-canals",

    # ADWD descriptive titles
    "REEK": "reek",
    "THE MERCHANT'S MAN": "the-merchants-man",
    "THE TURNCLOAK": "the-turncloak",
    "THE PRINCE OF WINTERFELL": "the-prince-of-winterfell",
    "THE LOST LORD": "the-lost-lord",
    "THE WINDBLOWN": "the-windblown",
    "THE WAYWARD BRIDE": "the-wayward-bride",
    "THE WATCHER": "the-watcher",
    "THE KING'S PRIZE": "the-kings-prize",
    "THE DRAGONTAMER": "the-dragontamer",
    "THE GRIFFIN REBORN": "the-griffin-reborn",
    "THE SACRIFICE": "the-sacrifice",
    "THE UGLY LITTLE GIRL": "the-ugly-little-girl",
    "THE DISCARDED KNIGHT": "the-discarded-knight",
    "THE SPURNED SUITOR": "the-spurned-suitor",
    "THE QUEENSGUARD": "the-queensguard",
    "THE BLIND GIRL": "the-blind-girl",
    "A GHOST IN WINTERFELL": "a-ghost-in-winterfell",
    "THE IRON SUITOR": "the-iron-suitor",
    "THE KINGBREAKER": "the-kingbreaker",
    "THE QUEEN'S HAND": "the-queens-hand",
}

# ---------------------------------------------------------------------------
# Real identity mapping (descriptive titles + standard names → full name)
# ---------------------------------------------------------------------------
REAL_IDENTITIES = {
    # Standard names
    "bran": "Bran Stark",
    "catelyn": "Catelyn Stark",
    "daenerys": "Daenerys Targaryen",
    "eddard": "Eddard Stark",
    "jon": "Jon Snow",
    "arya": "Arya Stark",
    "tyrion": "Tyrion Lannister",
    "sansa": "Sansa Stark",
    "theon": "Theon Greyjoy",
    "davos": "Davos Seaworth",
    "jaime": "Jaime Lannister",
    "samwell": "Samwell Tarly",
    "brienne": "Brienne of Tarth",
    "cersei": "Cersei Lannister",
    "melisandre": "Melisandre",
    "barristan": "Barristan Selmy",
    "victarion": "Victarion Greyjoy",
    "quentyn": "Quentyn Martell",
    "jon-connington": "Jon Connington",

    # AFFC descriptive titles
    "the-prophet": "Aeron Greyjoy",
    "the-drowned-man": "Aeron Greyjoy",
    "the-iron-captain": "Victarion Greyjoy",
    "the-reaver": "Victarion Greyjoy",
    "the-krakens-daughter": "Asha Greyjoy",
    "the-captain-of-guards": "Areo Hotah",
    "the-soiled-knight": "Arys Oakheart",
    "the-queenmaker": "Arianne Martell",
    "the-princess-in-the-tower": "Arianne Martell",
    "alayne": "Sansa Stark",
    "cat-of-the-canals": "Arya Stark",

    # ADWD descriptive titles
    "reek": "Theon Greyjoy",
    "the-merchants-man": "Quentyn Martell",
    "the-turncloak": "Theon Greyjoy",
    "the-prince-of-winterfell": "Theon Greyjoy",
    "the-lost-lord": "Jon Connington",
    "the-windblown": "Quentyn Martell",
    "the-wayward-bride": "Asha Greyjoy",
    "the-watcher": "Areo Hotah",
    "the-kings-prize": "Asha Greyjoy",
    "the-dragontamer": "Quentyn Martell",
    "the-griffin-reborn": "Jon Connington",
    "the-sacrifice": "Asha Greyjoy",
    "the-ugly-little-girl": "Arya Stark",
    "the-discarded-knight": "Barristan Selmy",
    "the-spurned-suitor": "Quentyn Martell",
    "the-queensguard": "Barristan Selmy",
    "the-blind-girl": "Arya Stark",
    "a-ghost-in-winterfell": "Theon Greyjoy",
    "the-iron-suitor": "Victarion Greyjoy",
    "the-kingbreaker": "Barristan Selmy",
    "the-queens-hand": "Barristan Selmy",
}

BOOK_NAMES = {
    "agot": "AGOT",
    "acok": "ACOK",
    "asos": "ASOS",
    "affc": "AFFC",
    "adwd": "ADWD",
}

EXPECTED_COUNTS = {
    "agot": 73,
    "acok": 70,
    "asos": 82,
    "affc": 46,
    "adwd": 73,
}

# Lines starting with these (case-insensitive) signal end of chapters
END_MARKERS = [
    "APPENDIX",
    "ACKNOWLEDGMENTS",
    "MEANWHILE, BACK ON THE WALL",
    "WESTEROS",
]


def normalize(text):
    """Replace smart/curly quotes with straight equivalents."""
    return (
        text.replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def to_roman(n):
    """Convert integer to Roman numeral."""
    vals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = ""
    for val, numeral in vals:
        while n >= val:
            result += numeral
            n -= val
    return result


def heading_to_title(heading):
    """Convert an ALL-CAPS heading to display Title Case.

    "PROLOGUE" → "Prologue"
    "THE KRAKEN'S DAUGHTER" → "The Kraken's Daughter"
    "CAT OF THE CANALS" → "Cat of the Canals"
    "A GHOST IN WINTERFELL" → "A Ghost in Winterfell"
    """
    if heading in ("PROLOGUE", "EPILOGUE"):
        return heading.capitalize()

    minor = {"OF", "THE", "IN", "AND", "AT", "A", "ON", "FOR", "WITH"}
    words = heading.split()
    parts = []
    for i, w in enumerate(words):
        if i > 0 and w in minor:
            parts.append(w.lower())
        else:
            # Handle apostrophes: KRAKEN'S → Kraken's
            parts.append(w.capitalize())
    return " ".join(parts)


def is_narrative(lines, start, lookahead=10):
    """Return True if any line in lines[start:start+lookahead] looks like prose.

    Used to distinguish actual chapter headings (followed by story text)
    from table-of-contents entries (followed only by blanks / more headings).
    A prose line must be >30 chars AND contain at least one lowercase letter
    (filters out ALL-CAPS TOC artefacts like "APPENDIX: THE KINGS AND THEIR COURTS").
    """
    end = min(start + lookahead, len(lines))
    for i in range(start, end):
        text = lines[i].strip()
        if len(text) > 30 and any(c.islower() for c in text):
            return True
    return False


def find_chapters(lines, verbose=False):
    """Detect chapter boundaries. Returns [(heading, start_line, end_line), ...]."""
    # Normalise every line for matching purposes (smart quotes → straight)
    norm_lines = [normalize(line) for line in lines]

    # --- pass 1: find every line that exactly matches a known heading ----------
    heading_positions = []
    for i, line in enumerate(norm_lines):
        key = line.strip().upper()
        if key in POV_HEADINGS:
            heading_positions.append((i, key))

    if verbose:
        print(f"  Raw heading matches: {len(heading_positions)}")

    # --- pass 2: keep only headings followed by narrative (filters out TOC) ----
    actual = []
    for line_num, heading in heading_positions:
        if is_narrative(lines, line_num + 1):
            actual.append((line_num, heading))

    if verbose:
        print(f"  Actual chapter headings: {len(actual)}")

    # --- pass 3: determine where chapters end ---------------------------------
    # Pre-compute the first end-marker line that comes after the first chapter
    end_marker_line = len(lines)
    if actual:
        first_chapter = actual[0][0]
        for i in range(first_chapter + 1, len(lines)):
            upper = norm_lines[i].strip().upper()
            if any(upper.startswith(m) for m in END_MARKERS):
                end_marker_line = i
                if verbose:
                    print(f"  End marker at line {i + 1}: {lines[i].strip()}")
                break

    chapters = []
    for idx, (line_num, heading) in enumerate(actual):
        if line_num >= end_marker_line:
            break
        if idx + 1 < len(actual):
            next_start = actual[idx + 1][0]
            text_end = min(next_start, end_marker_line)
        else:
            text_end = end_marker_line
        chapters.append((heading, line_num, text_end))

    return chapters


def split_book(input_file, book_abbrev, output_dir, verbose=False):
    """Split a source .txt file into per-chapter markdown files."""
    book_name = BOOK_NAMES[book_abbrev]

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if verbose:
        print(f"Read {len(lines)} lines from {input_file}")

    chapters = find_chapters(lines, verbose)

    if verbose:
        print(f"\nDetected {len(chapters)} chapters:")
        for heading, start, end in chapters:
            print(f"  Line {start + 1:>6}: {heading}  ({end - start} lines)")

    os.makedirs(output_dir, exist_ok=True)

    # Count how many times each slug appears in total (for pov_label numbering)
    slug_totals = defaultdict(int)
    for heading, _, _ in chapters:
        slug_totals[POV_HEADINGS[heading]] += 1

    pov_counts = defaultdict(int)
    written = []
    warnings = []

    for chapter_idx, (heading, start_line, end_line) in enumerate(chapters):
        slug = POV_HEADINGS[heading]
        pov_counts[slug] += 1
        pov_num = pov_counts[slug]

        # --- filename ---
        if slug in ("prologue", "epilogue"):
            file_name = f"{book_abbrev}-{slug}.md"
        else:
            file_name = f"{book_abbrev}-{slug}-{pov_num:02d}.md"

        # --- display name ---
        pov_character = heading_to_title(heading)
        real_identity = REAL_IDENTITIES.get(slug, pov_character)

        # --- pov_label ---
        if slug in ("prologue", "epilogue"):
            pov_label = pov_character
        elif slug_totals[slug] > 1:
            pov_label = f"{pov_character} {to_roman(pov_num)}"
        else:
            pov_label = pov_character

        # --- extract text ---
        text_lines = lines[start_line + 1 : end_line]
        # trim leading / trailing blank lines
        while text_lines and not text_lines[0].strip():
            text_lines = text_lines[1:]
        while text_lines and not text_lines[-1].strip():
            text_lines = text_lines[:-1]

        chapter_text = "".join(text_lines)

        if not chapter_text.strip():
            warnings.append(f"Empty chapter: {heading} at line {start_line + 1}")

        # --- frontmatter ---
        fm = (
            f"---\n"
            f"book: {book_name}\n"
            f"chapter_number: {chapter_idx + 1}\n"
            f"pov_character: {pov_character}\n"
            f"real_identity: {real_identity}\n"
            f"pov_chapter_number: {pov_num}\n"
            f'pov_label: "{pov_label}"\n'
            f"file_name: {file_name}\n"
            f"---\n\n"
        )

        out_path = os.path.join(output_dir, file_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(fm)
            f.write(chapter_text)
            f.write("\n")

        written.append(file_name)
        if verbose:
            print(f"  Wrote {file_name}  ({len(text_lines)} lines)")

    # --- summary ---
    expected = EXPECTED_COUNTS.get(book_abbrev, "?")
    ok = len(written) == expected

    print(f"\n{'=' * 60}")
    print(f"Book: {book_name}")
    print(f"Input: {input_file}")
    print(f"Output: {output_dir}")
    print(f"Chapters written: {len(written)}")
    print(f"Expected: {expected}")
    if ok:
        print("  ✓ Count matches")
    else:
        print(f"  ✗ MISMATCH — got {len(written)}, expected {expected}")

    print(f"\nPOV breakdown:")
    for slug in sorted(pov_counts):
        print(f"  {slug}: {pov_counts[slug]}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    return written, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Split ASOIAF text files into per-chapter markdown with YAML frontmatter."
    )
    parser.add_argument("input_file", help="Path to source .txt file")
    parser.add_argument(
        "book_abbrev",
        choices=list(BOOK_NAMES.keys()),
        help="Book abbreviation",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output directory (default: sources/chapters/{book}/)",
    )
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    if args.output:
        output_dir = args.output
    else:
        project_dir = Path(__file__).resolve().parent.parent
        output_dir = str(project_dir / "sources" / "chapters" / args.book_abbrev)

    split_book(args.input_file, args.book_abbrev, output_dir, args.verbose)


if __name__ == "__main__":
    main()
