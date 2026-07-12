#!/usr/bin/env python3
"""upgrade-wiki-quote-cites.py — S213 book-citation overlay for the QUOTE layer.

Node `## Quotes` blocks hold thousands of quotes whose only provenance is a raw
MediaWiki token (`(wiki:<Page>.cite_ref-…)`). Most are verbatim book lines the
wiki itself quoted. This script deterministically upgrades them:

  1. Extract each wiki-cited quote's clean text (strip `[label](wiki:Page)`
     links and `(wiki:…)` tokens).
  2. Normalized-containment search over the WHOLE chapter corpus
     (sources/chapters/*/*.md) — same norm() family as verify_node_quotes.py,
     so an upgraded cite passes the verifier by construction.
  3. On a UNIQUE corpus hit: rewrite the quote block — wiki artifacts stripped
     from the text, and the attribution line gains the navigable book cite
     (`— …, AGOT (`sources/chapters/agot/agot-arya-05.md:43`)`).
  4. No hit / ambiguous hit: quote left untouched (render-layer handles the
     token cosmetically) and reported.

Dry-run by default; --apply writes. Report always written to
working/quote-cite-upgrade/report-<mode>.json.

Matt's ask (2026-07-12): "Quotes should always be backed up by the book, and
not state the wiki. If we have the quote, you can easily GREP for that line."
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NODES = REPO / "graph/nodes"
CHAPTERS = REPO / "sources/chapters"
OUTDIR = REPO / "working/quote-cite-upgrade"

WIKI_LINK_RE = re.compile(r"\[([^\]]+)\]\(wiki:[^)]*\)")
WIKI_TOKEN_RE = re.compile(r"\(wiki:[^)]*\)")
HAS_BOOK_CITE_RE = re.compile(r"sources/chapters/[a-z0-9/_-]+\.md:\d+")

BOOK_LABEL = {
    "agot": "AGOT", "acok": "ACOK", "asos": "ASOS", "affc": "AFFC", "adwd": "ADWD",
    "fab": "F&B", "tmk": "The Mystery Knight", "tss": "The Sworn Sword",
    "thk": "The Hedge Knight",
}

MIN_NORM_LEN = 40  # below this, containment matches are too accidental


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def clean_wiki(s: str) -> str:
    s = WIKI_LINK_RE.sub(r"\1", s)
    s = WIKI_TOKEN_RE.sub("", s)
    return re.sub(r"[ \t]+", " ", s).strip()


def build_corpus():
    """[(book, relpath, normtext, line_offsets)] — one normalized blob per file,
    newline-joined with ' ' so matches can span wrapped lines; offsets map a
    match position back to its starting line number."""
    corpus = []
    for f in sorted(CHAPTERS.rglob("*.md")):
        book = f.parent.name
        lines = f.read_text().splitlines()
        parts, offsets, pos = [], [], 0
        for ln in lines:
            nl = norm(ln)
            offsets.append(pos)
            parts.append(nl)
            pos += len(nl) + 1  # the joining space
        corpus.append((book, str(f.relative_to(REPO)), " ".join(parts), offsets))
    return corpus


def find_unique(corpus, nq: str):
    """Return (relpath, book, line_no) if nq appears exactly once corpus-wide."""
    hit = None
    for book, rel, blob, offsets in corpus:
        start = 0
        while True:
            i = blob.find(nq, start)
            if i == -1:
                break
            if hit is not None:
                return None  # second hit anywhere → ambiguous
            # offset → line: last offset <= i
            lo, hi = 0, len(offsets) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if offsets[mid] <= i:
                    lo = mid
                else:
                    hi = mid - 1
            hit = (rel, book, lo + 1)
            start = i + 1
    return hit


def process_file(path: Path, corpus, apply: bool, report: list) -> bool:
    text = path.read_text()
    m = re.search(r"^## Quotes[ \t]*\n", text, re.M)
    if not m:
        return False
    head, body = text[: m.end()], text[m.end():]
    nxt = re.search(r"^## ", body, re.M)
    qbody, tail = (body[: nxt.start()], body[nxt.start():]) if nxt else (body, "")

    changed = False
    out_lines = []
    block: list[str] = []

    def flush_block():
        nonlocal changed
        if not block:
            return
        blk = list(block)
        joined = "\n".join(blk)
        if "cite_ref" not in joined or HAS_BOOK_CITE_RE.search(joined):
            out_lines.extend(blk)
            return
        # quote text lines = "> " lines that are not the attribution line
        text_idx = [i for i, ln in enumerate(blk)
                    if ln.lstrip().startswith(">") and not ln.lstrip().lstrip("> ").startswith("—")]
        attr_idx = next((i for i, ln in enumerate(blk)
                         if ln.lstrip().lstrip("> ").startswith("—")), None)
        raw_text = " ".join(re.sub(r"^\s*>\s?", "", blk[i]) for i in text_idx)
        clean = clean_wiki(raw_text)
        nq = norm(clean)
        slugrec = {"node": path.name[:-8], "quote": clean[:120]}
        if len(nq) < MIN_NORM_LEN:
            report.append({**slugrec, "outcome": "too-short"})
            out_lines.extend(blk)
            return
        hit = find_unique(corpus, nq)
        if hit is None:
            report.append({**slugrec, "outcome": "no-unique-match"})
            out_lines.extend(blk)
            return
        rel, book, line_no = hit
        label = BOOK_LABEL.get(book, book.upper())
        cite = f"{label} (`{rel}:{line_no}`)"
        # rewrite: strip wiki artifacts from text lines; single joined text line
        # keeps the verifier's window logic simple and matches the applied
        # convention elsewhere (one "> text" line per quote).
        newblk = [f"> {clean}"]
        if attr_idx is not None:
            attr = re.sub(r"^\s*>\s?", "", blk[attr_idx])
            attr = clean_wiki(attr).rstrip()
            newblk.append(">")
            newblk.append(f"> {attr}, {cite}" if not attr.endswith(",") else f"> {attr} {cite}")
        else:
            newblk.append(">")
            newblk.append(f"> — {cite}")
        out_lines.extend(newblk)
        report.append({**slugrec, "outcome": "upgraded", "cite": f"{rel}:{line_no}", "book": book})
        changed = True

    for ln in qbody.splitlines():
        if ln.lstrip().startswith(">"):
            block.append(ln)
        else:
            flush_block()
            block = []
            out_lines.append(ln)
    flush_block()

    if changed and apply:
        body_out = "\n".join(out_lines).rstrip("\n") + "\n"
        if tail:
            body_out += "\n"  # keep one blank line before the next ## section
        path.write_text(head + body_out + tail)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="stop after N changed files (smoke)")
    args = ap.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    print(f"corpus: {len(corpus)} chapter files")

    report: list = []
    changed_files = 0
    files = sorted(NODES.rglob("*.node.md"))
    for p in files:
        if "_conflicts" in p.parts:  # parked conflict copies — not the live graph
            continue
        if "cite_ref" not in p.read_text():
            continue
        if process_file(p, corpus, args.apply, report):
            changed_files += 1
            if args.limit and changed_files >= args.limit:
                break

    mode = "apply" if args.apply else "dry"
    (OUTDIR / f"report-{mode}.json").write_text(json.dumps(report, indent=1))
    c = Counter(r["outcome"] for r in report)
    books = Counter(r["book"] for r in report if r["outcome"] == "upgraded")
    print(f"quotes seen (wiki-cited, no book cite): {len(report)}")
    print(f"outcomes: {dict(c)}")
    print(f"upgraded by book: {dict(books)}")
    print(f"files changed: {changed_files}{' (DRY RUN)' if not args.apply else ''}")


if __name__ == "__main__":
    main()
