#!/usr/bin/env python3
"""Mint the S152 harvest-pass edges (4 edges; NO new nodes).

Reads working/harvest-pass-s152/candidates-edges.json; RE-GREPS each quote for the
authoritative line (FAIL-fast if a quote moved). Backup, re-run guard, slug pre-check.
Modeled on mint_cheap_l2_round_s151.py. Additive only.

  H1  breaking-of-theon-greyjoy ENABLES fall-of-moat-cailin   (T2, adwd-reek-02)
  H2  marillion ASSAULTS sansa-stark                          (T1, asos-sansa-06)
  H3  lothor-brune RESCUES sansa-stark                        (T1, asos-sansa-06)
  H4  melisandre FORESHADOWS jon-is-stabbed-repeatedly        (T2, adwd-jon-01)
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
CAND = REPO / "working" / "harvest-pass-s152" / "candidates-edges.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-harvest-s152.jsonl"

RUN_ID = "harvest-s152"
PRODUCED_AT = "2026-08-01T00:00:00+00:00"


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    if not f.exists():
        sys.exit(f"ABORT: chapter file missing: {f}")
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1
    sys.exit(f"ABORT: quote not found in {chapter}.md -> {quote!r}")


def make_edge_row(e):
    book, chapter = e["book"], e["chapter"]
    line = authoritative_line(book, chapter, e["quote"])
    return {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        "decision": "emit_edge",
        "candidate_kind": "harvest-curator",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-harvest-s152",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": e["note"],
        "candidate_id": e["id"],
        "unit": e.get("unit", ""),
    }


def main():
    data = json.loads(CAND.read_text())
    edges = data["edges"]

    all_slugs = set()
    for e in edges:
        all_slugs.add(e["source"]); all_slugs.add(e["target"])
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent: {sorted(missing)}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw = EDGES.read_text(encoding="utf-8").splitlines()
    existing = [ln for ln in raw if ln.strip()]
    if any(RUN_ID in ln for ln in existing):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    new_rows = [make_edge_row(e) for e in edges]  # FAIL-fast on any unfound quote
    print(f"Line-check OK: all {len(new_rows)} quotes located in source.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written -> {BACKUP.relative_to(REPO)}")

    out = existing + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    print("\n── SUMMARY ──")
    print(f"Edges appended ({len(new_rows)}):")
    for r in new_rows:
        print(f"  {r['source_slug']} {r['edge_type']} {r['target_slug']}  (T{r['confidence_tier']}, {r['evidence_ref']})")
    print(f"Total edges now: {len(out)}")


if __name__ == "__main__":
    main()
