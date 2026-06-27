#!/usr/bin/env python3
"""Locate verbatim quotes in chapter files using the SAME norm() as the mint script.
Usage: python working/enrichment/dorne/quotecheck.py --cands   (validates candidates.json)
       python working/enrichment/dorne/quotecheck.py           (runs ad-hoc PROBES)"""
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
            return i, ln.strip()[:120]
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

# ad-hoc probes
PROBES = [
    ("affc-the-captain-of-guards-01", "By law the Iron Throne should pass to her"),
    ("affc-the-queenmaker-01", "the Iron Throne by rights is yours"),
    ("affc-the-princess-in-the-tower-01", "I want my rights"),
    ("affc-the-princess-in-the-tower-01", "Her seduction of Ser Arys had required half a year"),
    ("affc-the-princess-in-the-tower-01", "she would give us leave to marry"),
    ("affc-the-soiled-knight-01", "I swore an oath"),
    ("affc-the-queenmaker-01", "put his golden spurs into his horse and charged"),
    ("affc-the-queenmaker-01", "His mother was my wet nurse"),
    ("affc-the-queenmaker-01", "of the orphans of the Greenblood"),
    ("affc-the-queenmaker-01", "Yielding seems the wisest course"),
    ("affc-the-queenmaker-01", "I give you Ser Andrey Dalt"),
    ("affc-the-queenmaker-01", "My dearest Spotted Sylva"),
    ("affc-the-princess-in-the-tower-01", "Her father has shipped her to Greenstone to wed Lord Estermont"),
    ("affc-the-princess-in-the-tower-01", "sent to Norvos to serve your lady mother"),
    ("affc-the-princess-in-the-tower-01", "Garin will spend his next two years in Tyrosh"),
    ("affc-the-princess-in-the-tower-01", "Because I knew that you would spurn him"),
    ("affc-the-queenmaker-01", "Nor will you get the war you want"),
    ("adwd-the-watcher-01", "Darkstar did it"),
    ("adwd-the-watcher-01", "It is all true"),
    ("adwd-the-watcher-01", "smashed her babe"),
    ("adwd-the-watcher-01", "lead him to High Hermitage"),
    ("adwd-the-watcher-01", "ash-and-iron wife"),
    ("affc-the-queenmaker-01", "removed the head of Arys Oakheart"),
    ("affc-the-queenmaker-01", "stepped Areo Hotah"),
    ("affc-the-captain-of-guards-01", "left Sunspear for the peace and isolation of the Water Gardens"),
    ("affc-the-princess-in-the-tower-01", "happily ensconced at the Water Gardens"),
    ("affc-the-princess-in-the-tower-01", "crumbling old castle perched on a rock in the Sea of Dorne"),
    ("affc-the-princess-in-the-tower-01", "delivered her to the Spear Tower"),
    ("affc-the-captain-of-guards-01", "confine them in the cells atop the Spear Tower"),
    ("affc-the-captain-of-guards-01", "the slender Spear Tower"),
]
for ch, q in PROBES:
    line, txt = find(ch, q)
    print(f"[{('L'+str(line)) if line else 'NOT FOUND':>10}] {ch}: {q!r}")
    if line: print(f"            -> {txt}")
