#!/usr/bin/env python3
"""Locate verbatim quotes in chapter files using the SAME norm() as the mint script.
Usage: python3 working/enrichment/euron/quotecheck.py --cands   (validates candidates.json)"""
import json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

def book_of(chapter):
    return chapter.split("-")[0]

def find(chapter, quote):
    f = REPO / "sources" / "chapters" / book_of(chapter) / f"{chapter}.md"
    if not f.exists():
        return None, f"FILE MISSING {f}"
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i, ln.strip()[:100]
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1, "(spans 2 lines) " + lines[i].strip()[-60:]
    return None, "NOT FOUND"

if "--cands" in sys.argv:
    cand = json.loads((Path(__file__).parent / "candidates.json").read_text())
    bad = 0
    for e in cand["edges"]:
        line, txt = find(e["chapter"], e["quote"])
        status = f"L{line}" if line else "*** NOT FOUND ***"
        if not line: bad += 1
        print(f"  {e['id']:>4} [{status:>16}] {e['chapter']}  {e['type']}  {e['source']}->{e['target']}")
        if not line:
            print(f"        quote: {e['quote']!r}")
    print(f"\n{'ALL FOUND' if bad==0 else str(bad)+' NOT FOUND'}")
    sys.exit(1 if bad else 0)

print("pass --cands to validate candidates.json")
