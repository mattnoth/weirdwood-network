#!/usr/bin/env python3
"""S152 harvest pass — extract the open queue rows keyed by queue line number.

Step 1 (this run): parse working/harvest-queue.md, pull every `| open |` row,
emit working/harvest-pass-s152/rows.json with stable queue-line-number keys.
The line number is the flip key (deterministic, unique, survives note text).
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
QUEUE = REPO / "working" / "harvest-queue.md"
OUT = REPO / "working" / "harvest-pass-s152" / "rows.json"


def main():
    rows = []
    for lineno, raw in enumerate(QUEUE.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.startswith("| open |"):
            continue
        # | open | kind | book | chapter:line | note | found |
        cells = [c.strip() for c in raw.split("|")]
        # cells[0] empty, [1]=open, [2]=kind, [3]=book, [4]=cite, [5]=note, [6]=found, [7] empty(maybe)
        kind = cells[2]
        book = cells[3]
        cite = cells[4]
        note = cells[5] if len(cells) > 5 else ""
        found = cells[6] if len(cells) > 6 else ""
        # chapter:line — split on last ':' only if trailing is a line range/number
        m = re.match(r"^(?P<chap>.+?\.md|[a-z0-9-]+):(?P<ln>[\d–\-]+)$", cite)
        if m:
            chap = m.group("chap")
            cline = m.group("ln")
        else:
            chap = cite
            cline = ""
        rows.append({
            "qline": lineno,
            "kind": kind,
            "book": book,
            "cite": cite,
            "chapter": chap,
            "chap_line": cline,
            "note": note,
            "found": found,
            "route": None,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    # quick console summary
    by_kind = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
    print(f"Extracted {len(rows)} open rows -> {OUT.relative_to(REPO)}")
    for k, c in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  {k}: {c}")


if __name__ == "__main__":
    main()
