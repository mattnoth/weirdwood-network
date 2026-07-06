#!/usr/bin/env python3
"""s195_dossier_residue_cleanup.py — S194-addendum residue, data-side.

Two user-visible blemish classes in dossier/quote prose (S194 made node BODY
sections render live, exposing them):

1. INTERNAL-PROVENANCE MARKERS in shipped prose: "**Book-cite overlay (S152
   harvest):**", inline "Book-cite overlay: ...", session stamps "(S152
   harvest)", and the bowl-of-brown trailing sentence "Navigable book cite
   overlay on the wiki cite above." Stripped from READER-FACING sections only —
   the internal ledger sections (headings matching book-cit|overlay|harvest,
   and ## Notes) keep their bookkeeping voice and never ship.

2. DOUBLED QUOTE ATTRIBUTIONS: "— ADWD Chapter 66 (Tyrion XII), `path:line`"
   renders doubled because the front-end derives "ADWD Tyrion 12" from the
   cite and the attribution text doesn't contain that substring. Normalized to
   the canonical S193 shape "— [gloss, ]ADWD Tyrion XII (`path:line`)" which
   app.js cleanQuote() collapses to a single label. A "(Pov ROMAN)" gloss that
   just restates the chapter is dropped; scene glosses ("(Red Wedding)") are
   kept, moved before the label.

Usage: python3 scripts/s195_dossier_residue_cleanup.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "graph" / "query"))

NODES_DIR = REPO / "graph" / "nodes"

SKIP_HEADING = re.compile(r"(?i)book.?cit|overlay|harvest|^notes\b")

OVERLAY_BOLD = re.compile(r"\*\*Book-cite overlays?(?: \([^)]*\))?:?\*\*:?\s*", re.I)
# a whole italic run that IS provenance ("*book-cite overlay, S147 AEGON
# enrichment (navigable upgrade)*", "*Book-cite overlay for the wiki quote in
# ## Quotes below.*"), with any leading dash — removed wholesale
OVERLAY_ITALIC_RUN = re.compile(r"\s*[—–-]?\s*\*[^*\n]*book-cite overlay[^*\n]*\*", re.I)
# "[Book-cite overlay onto <gloss>: <content>]" — bracketed WITH a colon means
# real content follows; keep gloss + content, drop marker + brackets
OVERLAY_BRACKET_CONTENT = re.compile(
    r"\[Book-cite overlays? (?:for|on|onto) ([^\]]*:[^\]]*)\]", re.I)
# "Book-cite overlay for/on/onto <gloss>:" keeps its gloss ("<Gloss>:")
OVERLAY_FOR = re.compile(r"Book-cite overlays? (?:for|on|onto) ([^:\n]{1,100}):", re.I)
# bare provenance tags "(book-cite overlay)" / "[book-cite overlay onto wiki
# description]" — no colon, pure commentary, dropped wholesale
OVERLAY_TAG = re.compile(r"\s*[\[(]book-cite overlays?[^\])\n:]{0,80}[\])]", re.I)
OVERLAY_PLAIN = re.compile(r"Book-cite overlays?(?: \([^)]*\))?\s*[,;:—–-]\s*([a-z])?", re.I)
NAVIGABLE_SENT = re.compile(r"\s*Navigable book cite overlay[^.]*\.\s*")
SESSION_STAMP = re.compile(r"\s*\(\s*[Ss]1\d{2}[^)]*\)")

ATTR_LINE = re.compile(
    r"^(?P<prefix>\s*(?:>\s*)?—\s*)"
    r"(?P<book>A[A-Z]{3}) Chapter \d+"
    r"(?:\s*\((?P<gloss>[^)]*)\))?"
    r",\s*`(?P<path>sources/chapters/[a-z0-9/_-]+\.md:\d+)`"
    r"(?P<tail>.*)$"
)
POV_ROMAN = re.compile(r"^[A-Z][\w' ]*\s+[IVXLCDM]+$")


def to_roman(n: int) -> str:
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
            (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
            (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for v, s in vals:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)


def chapter_label(path: str) -> str | None:
    """sources/chapters/adwd/adwd-tyrion-12.md:183 -> 'ADWD Tyrion XII'."""
    m = re.match(r"sources/chapters/[a-z]+/([a-z0-9]+)-(.+)-(\d+)\.md:\d+$", path)
    if not m:
        return None
    book = m.group(1).upper()
    pov = " ".join(w.capitalize() for w in m.group(2).split("-"))
    return f"{book} {pov} {to_roman(int(m.group(3)))}"


def fix_attr_line(line: str) -> str:
    m = ATTR_LINE.match(line)
    if not m:
        return line
    label = chapter_label(m.group("path"))
    if label is None:
        return line
    gloss = (m.group("gloss") or "").strip()
    # a gloss that just restates the chapter ("Tyrion XII") is redundant
    if gloss and (POV_ROMAN.match(gloss) and gloss.split()[0] in label):
        gloss = ""
    lead = f"{gloss}, " if gloss else ""
    return f"{m.group('prefix')}{lead}{label} (`{m.group('path')}`){m.group('tail')}"


def strip_provenance(text: str) -> str:
    text = NAVIGABLE_SENT.sub(" ", text)
    text = OVERLAY_BOLD.sub("", text)
    text = OVERLAY_ITALIC_RUN.sub("", text)

    def cap(s: str) -> str:
        return s[:1].upper() + s[1:] if s else s
    text = OVERLAY_BRACKET_CONTENT.sub(lambda m: cap(m.group(1)), text)
    text = OVERLAY_FOR.sub(lambda m: f"{cap(m.group(1))}:", text)
    text = OVERLAY_TAG.sub("", text)
    # strip the inline marker; capitalize the word it prefixed so the sentence
    # still reads ("… company. Book-cite overlay: named …" -> "… company. Named …")
    text = OVERLAY_PLAIN.sub(lambda m: (m.group(1) or "").upper(), text)
    text = SESSION_STAMP.sub("", text)
    return text


def process_file(path: Path, dry: bool) -> int:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    changed = 0
    heading = ""
    for i, ln in enumerate(lines):
        h = re.match(r"^##+\s+(.*)$", ln)
        if h:
            heading = h.group(1).strip()
            continue
        if SKIP_HEADING.search(heading):
            continue
        new = fix_attr_line(ln)
        if new == ln and ("Book-cite overlay" in ln or "book-cite overlay" in ln
                          or "Navigable book cite" in ln or SESSION_STAMP.search(ln)):
            new = strip_provenance(ln)
            new = re.sub(r"[ \t]+$", "", new)
            if not new.strip() and ln.strip():
                new = ln  # never blank a line wholesale; leave for manual review
        if new != ln:
            lines[i] = new
            changed += 1
    if changed and not dry:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total_files = total_lines = 0
    for path in sorted(NODES_DIR.rglob("*.node.md")):
        if "_conflicts" in path.parts:
            continue
        n = process_file(path, args.dry_run)
        if n:
            total_files += 1
            total_lines += n
            print(f"  {path.relative_to(REPO)}: {n} line(s)")
    print(f"{'DRY RUN: ' if args.dry_run else ''}{total_lines} lines in {total_files} files")


if __name__ == "__main__":
    main()
