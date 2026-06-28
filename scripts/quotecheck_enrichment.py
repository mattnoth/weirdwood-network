#!/usr/bin/env python3
"""Pre-flight quote line-checker for an enrichment dip's candidates.json (S159 — generalized).

Locates every edge quote in its chapter file using the SAME norm() as scripts/mint_enrichment.py,
so a green run here guarantees the mint's own fail-fast line-check will pass. This is an OPTIONAL
pre-flight — the mint re-greps every quote anyway and aborts on any miss — but it lets you validate
quotes before touching the graph.

Replaces the per-dip `working/enrichment/<unit>/quotecheck.py` copies (dorne/euron/stannis/... were
byte-identical clones — the same copy-paste debt S158 retired for mint/finalize). One parameterized
tool, pass the candidates path.

USAGE
  python scripts/quotecheck_enrichment.py working/enrichment/<unit>/candidates.json
  python scripts/quotecheck_enrichment.py --candidates working/enrichment/<unit>/candidates.json
Exit 0 if all found, 1 if any quote is not located (prints the offending ids).
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


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


def main():
    ap = argparse.ArgumentParser(description="Pre-flight quote line-checker for an enrichment candidates.json.")
    ap.add_argument("candidates", nargs="?", type=Path, help="path to a dip's candidates.json")
    ap.add_argument("--candidates", dest="candidates_opt", type=Path, help="(alt) path to candidates.json")
    args = ap.parse_args()
    path = args.candidates or args.candidates_opt
    if not path:
        ap.error("provide a candidates.json path (positional or --candidates)")

    cand = json.loads(path.read_text(encoding="utf-8"))
    bad = 0
    for e in cand["edges"]:
        line, _txt = find(e["chapter"], e["quote"])
        status = f"L{line}" if line else "*** NOT FOUND ***"
        if not line:
            bad += 1
        print(f"  {e['id']:>4} [{status:>16}] {e['chapter']}  {e['type']}  {e['source']}->{e['target']}")
        if not line:
            print(f"        quote: {e['quote']!r}")
    print(f"\n{'ALL FOUND' if bad == 0 else str(bad) + ' NOT FOUND'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
