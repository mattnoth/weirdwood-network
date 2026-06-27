#!/usr/bin/env python3
"""Locate verbatim quotes in chapter files using the SAME norm() as the mint script.
Usage: pass a list of (chapter, substring) below; prints line number + the line, or NOT FOUND.
Also usable to validate candidates.json: --cands."""
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
    ("acok-davos-01", "wrenched it free of the burning wood"),
    ("acok-davos-01", "jade-green flames swirling around cherry-red steel"),
    ("acok-davos-01", "It is time I tried another hawk"),
    ("acok-davos-01", "Davos watched them burn"),
    ("acok-davos-01", "Queen Selyse echoed the words"),
    ("acok-prologue", "Now I will hear hers"),
    ("acok-davos-02", "huge with child"),
    ("acok-davos-02", "steering a tiny boat with a black sail"),
    ("acok-davos-02", "He knew that shadow"),
    ("acok-davos-02", "command of Storm"),
    ("acok-davos-02", "My brother's bastard must be surrendered"),
    ("acok-davos-02", "Then my answer is still no"),
    ("acok-davos-02", "I dream of it sometimes"),
    ("acok-davos-02", "go to my grave thinking of my brother"),
    ("acok-davos-02", "I will have justice for him"),
    ("acok-davos-02", "Lady Stark who slew the king"),
    ("acok-davos-02", "It was Brienne"),
    ("acok-catelyn-04", "only the king's shadow shifting"),
    ("acok-catelyn-04", "cried Brienne"),
    ("acok-catelyn-04", "it was Stannis killed him"),
    ("asos-davos-04", "three large black leeches"),
    ("asos-davos-04", "Joffrey Baratheon"),
    ("asos-davos-04", "The boy's blood"),
    ("asos-davos-04", "Chamber of the Painted Table"),
    ("asos-davos-06", "a king protects his people"),
    ("asos-davos-06", "Edric Storm is gone"),
    ("asos-davos-06", "safely out to sea"),
    ("adwd-jon-04", "Eat their bread and salt"),
]
for ch, q in PROBES:
    line, txt = find(ch, q)
    print(f"[{('L'+str(line)) if line else 'NOT FOUND':>10}] {ch}: {q!r}")
    if line: print(f"            -> {txt}")
