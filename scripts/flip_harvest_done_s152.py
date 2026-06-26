#!/usr/bin/env python3
"""S152 harvest pass — flip consumed queue rows to done/parked (orchestrator, central).

Merges the 4 owner reports (foods/chars/events/edges) keyed by queue line number,
then rewrites working/harvest-queue.md in place: each `| open |` row at a recorded
qline becomes `| done |` (or `| parked |` for the 7 blocked rows), with a
`[S152 harvest: …]` audit tag appended to the note cell. Backup first; guard that the
target line is still `| open |` (queue unchanged since extraction).
"""
import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PASS = REPO / "working" / "harvest-pass-s152"
QUEUE = REPO / "working" / "harvest-queue.md"
BACKUP = REPO / "working" / "harvest-pass-s152" / "harvest-queue-pre-flip-s152.md"
ROWS = PASS / "rows.json"


def get_rows(o):
    return o["rows"] if isinstance(o, dict) else o


def qn(v):
    return int(re.sub(r"\D", "", str(v)))


def main():
    qline_of = {r["qline"]: r["qline"] for r in json.loads(ROWS.read_text())}  # qline IS the queue line no.

    # merge reports; done-edges overlays the agent reports (handback resolutions + parks)
    merged = {}
    for fn in ["done-foods.json", "done-chars.json", "done-events.json", "done-edges.json"]:
        for x in get_rows(json.loads((PASS / fn).read_text())):
            merged[qn(x["qline"])] = x

    def final_status(x):
        st = x.get("status")
        if st in ("done", "parked"):
            return st
        # agent reports use 'action'; everything except an unresolved handback is done
        if x.get("action") == "handback":
            return None  # should have been overlaid by done-edges; flag if not
        return "done"

    def note_for(q, x, status):
        act = x.get("action", "")
        node = x.get("node", "")
        detail = x.get("detail", "")
        if status == "parked":
            return f"PARKED ({detail})" if detail else f"PARKED ({act})"
        if act in ("dedup-noop",):
            return f"dedup-noop — {node}".strip(" —")
        if "edge-minted" in act:
            return f"edge minted: {node}"
        if "mint" in act:
            return f"minted node {node}"
        tgt = node or detail
        return f"attached -> {tgt}"

    raw = QUEUE.read_text(encoding="utf-8").splitlines()
    changed, parked, errors = 0, 0, []
    for q, x in merged.items():
        idx = q - 1
        if idx < 0 or idx >= len(raw):
            errors.append(f"q{q}: line out of range"); continue
        line = raw[idx]
        if not line.startswith("| open |"):
            errors.append(f"q{q}: line not '| open |' (got: {line[:40]!r})"); continue
        status = final_status(x)
        if status is None:
            errors.append(f"q{q}: unresolved handback (no done-edges overlay)"); continue
        cells = line.split("|")  # ['', ' open ', ' kind ', ' book ', ' cite ', ' note ', ' found ', '']
        cells[1] = f" {status} "
        tag = f" **[S152 harvest: {note_for(q, x, status)}]**"
        cells[5] = cells[5].rstrip() + tag + " "
        raw[idx] = "|".join(cells)
        changed += 1
        if status == "parked":
            parked += 1

    if errors:
        print("ERRORS — aborting, no write:")
        for e in errors:
            print("  " + e)
        raise SystemExit(1)

    shutil.copy2(QUEUE, BACKUP)
    print(f"Backup -> {BACKUP.relative_to(REPO)}")
    QUEUE.write_text("\n".join(raw) + "\n", encoding="utf-8")
    print(f"Flipped {changed} rows: {changed - parked} -> done, {parked} -> parked")


if __name__ == "__main__":
    main()
