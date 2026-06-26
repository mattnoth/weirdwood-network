#!/usr/bin/env python3
"""Whole-file line-check for Theon/Reek enrichment candidates: for each edge, search the
ENTIRE cited chapter file for the normalized quote substring and report the TRUE line.
PASS prints the real line; FAIL prints the quote so it can be fixed or dropped before minting."""
import json, re, pathlib

ROOT = pathlib.Path("/Users/mnoth/source/asoiaf-chat")
CAND = ROOT / "working/enrichment/arya-braavos/candidates.json"

def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

def main():
    data = json.loads(CAND.read_text())
    edges = data["edges"]
    npass = nfail = 0
    for e in edges:
        book, chap = e["book"], e["chapter"]
        f = ROOT / "sources" / "chapters" / book / f"{chap}.md"
        if not f.exists():
            print(f"FAIL {e['id']:5} FILE-MISSING {f}")
            nfail += 1; continue
        lines = f.read_text().splitlines()
        q = norm(e["quote"])
        hits = [i + 1 for i, ln in enumerate(lines) if q in norm(ln)]
        if not hits:
            for i in range(len(lines) - 1):
                if q in norm(lines[i] + " " + lines[i + 1]):
                    hits.append(i + 1); break
        if hits:
            claimed = e["line"]
            flag = "" if claimed in hits else f"  (claimed {claimed}, FOUND {hits})"
            print(f"PASS {e['id']:5} {e['source']:34.34} -{e['type']:13}-> {e['target']:36.36} L{hits[0]}{flag}")
            npass += 1
        else:
            print(f"FAIL {e['id']:5} {e['source']} -{e['type']}-> {e['target']}  ({chap})")
            print(f"        quote: {e['quote']}")
            nfail += 1
    print(f"\n{npass} PASS / {nfail} FAIL  of {len(edges)} edges")

if __name__ == "__main__":
    main()
