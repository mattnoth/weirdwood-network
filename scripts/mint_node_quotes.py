#!/usr/bin/env python3
"""mint_node_quotes.py — attach verbatim `## Quotes` entries to graph nodes.

S193 quote-minting track, step 1 tool (reusable for future slices). Reads a
plan JSON of {slug, quotes:[{file, line, start, end, speaker?}]} rows and, for
each quote, extracts the VERBATIM span between the `start` and `end` markers
from the cited chapter line (a window of up to WINDOW lines starting at
`line`, so couplets that span a blank line still extract). Because the text is
pulled straight from `sources/chapters/`, transcription drift is impossible —
if a marker doesn't match, the mint fails loudly and nothing is written.

Output format matches what `weirwood_query.load.parse_quotes` consumes (the
snake-stew convention):

    ## Quotes

    > quote text

    — [Speaker, ]BOOK (Chapter Pretty), `sources/chapters/<book>/<chapter>.md:<line>`

Appends to an existing `## Quotes` section (right after the header) or creates
the section at end-of-file. Skips any quote whose exact text is already
present in the node (idempotent re-runs).

Usage:
    python3 scripts/mint_node_quotes.py --plan working/quote-census/s193-mint-plan.json [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NODES_DIR = REPO / "graph" / "nodes"
WINDOW = 5  # lines of source joined for marker search (line .. line+WINDOW-1)

BOOK_LABELS = {"agot": "AGOT", "acok": "ACOK", "asos": "ASOS",
               "affc": "AFFC", "adwd": "ADWD",
               "thk": "THK", "tss": "TSS", "tmk": "TMK"}

_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV"]


def chapter_pretty(file_path: str) -> tuple[str, str]:
    """'sources/chapters/adwd/adwd-the-watcher-01.md' -> ('ADWD', 'The Watcher I')."""
    stem = Path(file_path).stem            # adwd-the-watcher-01
    parts = stem.split("-")
    book = parts[0]
    rest = parts[1:]
    num = None
    if rest and rest[-1].isdigit():
        num = int(rest[-1])
        rest = rest[:-1]
    name = " ".join(w.capitalize() for w in rest)
    if num:
        name = f"{name} {_ROMAN[num]}"
    return BOOK_LABELS.get(book, book.upper()), name


def find_node_file(slug: str) -> Path | None:
    hits = [p for p in NODES_DIR.rglob(f"{slug}.node.md")
            if "_conflicts" not in p.parts]
    return hits[0] if hits else None


def extract_span(file_path: str, line: int, start: str, end: str) -> str:
    src = (REPO / file_path).read_text().splitlines()
    if line < 1 or line > len(src):
        raise ValueError(f"{file_path}:{line} out of range")
    window = " ".join(
        s.strip() for s in src[line - 1: line - 1 + WINDOW] if s.strip()
    )
    i = window.find(start)
    if i < 0:
        raise ValueError(f"start marker not found at {file_path}:{line}: {start[:60]!r}")
    j = window.find(end, i)
    if j < 0:
        raise ValueError(f"end marker not found at {file_path}:{line}: {end[:60]!r}")
    text = window[i: j + len(end)]
    # the marker must sit on the CITED line, not later in the window
    first_line = src[line - 1].strip()
    if not first_line or start not in first_line:
        raise ValueError(f"start marker not on cited line {file_path}:{line}")
    return re.sub(r"\s+", " ", text).strip()


def format_block(text: str, attribution: str) -> str:
    return f"> {text}\n\n— {attribution}\n"


def quotes_section(content: str) -> str:
    m = re.search(r"^## Quotes[ \t]*\n", content, re.M)
    if not m:
        return ""
    body = content[m.end():]
    nxt = re.search(r"^## ", body, re.M)
    return body[: nxt.start()] if nxt else body


def attach(node_path: Path, blocks: list[str], dry: bool) -> str:
    content = node_path.read_text()
    # dedup only against RENDERED quotes (blockquote lines) already in the
    # section — un-rendered wiki-format prose there doesn't count, minting
    # over it is the book-cite upgrade
    existing = " ".join(l.lstrip("> ").strip()
                        for l in quotes_section(content).splitlines()
                        if l.lstrip().startswith(">"))
    new_blocks = [b for b in blocks
                  if b.splitlines()[0].lstrip("> ").strip() not in existing]
    if not new_blocks:
        return "already-present"
    joined = "\n".join(new_blocks)
    m = re.search(r"^## Quotes[ \t]*\n", content, re.M)
    if m:
        content = content[: m.end()] + "\n" + joined + content[m.end():]
    else:
        if not content.endswith("\n"):
            content += "\n"
        content += f"\n## Quotes\n\n{joined}"
    if not dry:
        node_path.write_text(content)
    return f"minted {len(new_blocks)}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text())
    failures = []
    report = []
    for row in plan:
        slug = row["slug"]
        node_path = find_node_file(slug)
        if node_path is None:
            failures.append(f"{slug}: node file not found")
            continue
        blocks = []
        for q in row["quotes"]:
            try:
                text = extract_span(q["file"], q["line"], q["start"], q["end"])
            except ValueError as e:
                failures.append(f"{slug}: {e}")
                continue
            book, chap = chapter_pretty(q["file"])
            speaker = q.get("speaker")
            attribution = (f"{speaker}, " if speaker else "") + \
                f"{book} ({chap}), `{q['file']}:{q['line']}`"
            blocks.append(format_block(text, attribution))
            report.append(f"### {slug}\n> {text}\n— {attribution}\n")
        if blocks:
            status = attach(node_path, blocks, args.dry_run)
            print(f"{slug:55} {status}")
    print(f"\n{'DRY RUN — nothing written' if args.dry_run else 'written'}")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
