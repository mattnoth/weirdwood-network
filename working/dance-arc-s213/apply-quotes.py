#!/usr/bin/env python3
"""S213 Dance arc dip — deterministically append verified curated quotes to node
`## Quotes` sections. Input: quotes-to-apply.json (byte-verified at stated lines
by assemble-final.py). Idempotent: a quote already present in the node is skipped.

Format matches the existing book-cited convention (e.g. aegon-i-targaryen):
  > <quote>
  >
  > — <attribution>, F&B (`sources/chapters/fab/<chapter>.md:<line>`)
"""
import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true", help="write files (default: dry-run)")
args = ap.parse_args()

quotes = json.loads((OUT / "quotes-to-apply.json").read_text())["quotes"]

by_slug = {}
for q in quotes:
    by_slug.setdefault(q["slug"], []).append(q)

node_files = {p.name[:-8]: p for p in (REPO / "graph/nodes").rglob("*.node.md")}

applied = skipped = 0
for slug, qs in sorted(by_slug.items()):
    path = node_files.get(slug)
    if path is None:
        print(f"!! NO NODE FILE for {slug} — aborting")
        raise SystemExit(1)
    text = path.read_text()
    blocks = []
    for q in qs:
        if q["quote"] in text:
            skipped += 1
            continue
        cite = f"sources/chapters/fab/{q['chapter']}.md:{q['line']}"
        blocks.append(f"> {q['quote']}\n>\n> — {q['attribution']}, F&B (`{cite}`)\n")
        applied += 1
    if not blocks:
        continue
    addition = "\n" + "\n".join(blocks)
    m = re.search(r"^## Quotes\s*$", text, re.M)
    if m:
        # insert at the END of the ## Quotes section (before the next ## header)
        nxt = re.search(r"^## ", text[m.end():], re.M)
        insert_at = m.end() + (nxt.start() if nxt else len(text) - m.end())
        text = text[:insert_at].rstrip("\n") + "\n" + addition + "\n" + text[insert_at:]
    else:
        text = text.rstrip("\n") + "\n\n## Quotes\n" + addition
    if args.apply:
        path.write_text(text)
    print(f"{'APPLIED' if args.apply else 'DRY'} {slug}: +{len(blocks)} quote(s)")

print(f"\ntotal: {applied} applied, {skipped} skipped-as-present, "
      f"{len(by_slug)} nodes{' (DRY RUN — no writes)' if not args.apply else ''}")
