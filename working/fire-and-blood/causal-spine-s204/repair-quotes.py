#!/usr/bin/env python3
"""S204: repair quote-not-located rows by trimming to the longest locatable
verbatim fragment (sentence-boundary split, then word-window shrink).
Edits the proposal files IN PLACE so re-assembly picks the fixes up."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "working/fire-and-blood/causal-spine-s204"


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def locate(chapter, quote):
    f = ROOT / "sources/chapters/fab" / f"{chapter}.md"
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1
    return None


def candidates(quote):
    # sentence-ish splits first, longest first
    parts = re.split(r"(?<=[.!?;])\s+", quote)
    cands = sorted({p.strip() for p in parts if len(p.strip()) >= 25},
                   key=len, reverse=True)
    # then shrinking word windows from each end of the full quote
    words = quote.split()
    for take in range(len(words) - 1, 4, -1):
        cands.append(" ".join(words[:take]))
        cands.append(" ".join(words[-take:]))
    return cands


fails = []
for line in (BASE / "review-queue.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    if r.get("reasons") and any("not located" in x for x in r["reasons"]):
        fails.append(r)

by_file = {}
for r in fails:
    by_file.setdefault(r["_file"], []).append(r)

for stem, rows in by_file.items():
    path = BASE / "proposals" / f"{stem}.json"
    prop = json.loads(path.read_text(encoding="utf-8"))
    for r in rows:
        edge = next(e for e in prop["edges"] if e["id"] == r["id"])
        fixed = None
        for cand in candidates(edge["quote"]):
            ln = locate(edge["chapter"], cand)
            if ln:
                fixed = (cand, ln)
                break
        if fixed:
            print(f"{edge['id']}: FIXED (line {fixed[1]}) -> {fixed[0][:90]}")
            edge["quote"], edge["line"] = fixed
            edge["note"] = (edge.get("note") or "") + " [S204 quote trimmed to single-line fragment; original spanned an OCR blank-line break]"
        else:
            print(f"{edge['id']}: STILL UNLOCATED — needs manual review")
    path.write_text(json.dumps(prop, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
