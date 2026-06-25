#!/usr/bin/env python3
"""Mint Bran / greenseer arc enrichment pass 1 (S146) — twelfth major-arc enrichment dip;
A1.4 in the S143 reopened L1 round (the third spine-only heavyweight after Daenerys/Meereen
S144 and Jon/Wall S145). Matt-picked the Bran fork at STEP 0.

The BRAN spine (BR1-BR7, 8 beats) was built S130 as a clean ENABLES chain, but it was the bare
journey skeleton: no greendream catalogue, the `greensight` concept node dead (0 edges),
Bloodraven's cave mentorship unwired, Leaf un-affiliated, and the legacy `wight-ambush` node
islanded. This EDGE-ONLY pass (0 new nodes) wires the texture the spine lacked:

  - THE GREENDREAM CATALOGUE (marquee): Jojen's green dreams, all unwired, modeled as DREAMS_OF
    (+ FORESHADOWS for the two cleanest Chekhov's guns). Two are BRAN->WO5K/NORTH cross-container
    seams: the 'sea comes to Winterfell' dream -> sack-of-winterfell, the 'Reek skinning your
    faces' dream -> robb-receives-false-news. Plus the 'winged wolf in stone chains' ->
    bran-becomes-a-greenseer (the terminus, foreseen) and the crypts dream -> the survival.
  - LIGHTING THE DEAD `greensight` NODE (0 edges): bran-stark / brynden-rivers / jojen-reed
    PRACTICES greensight (first PRACTICES instances in the graph).
  - BLOODRAVEN CAVE-MENTOR SUBSTRATE (textual, NOT theory): brynden-rivers TUTORS bran-stark
    (distinct from the existing jojen TUTORS), BONDED_TO weirwood (drawn his life from the tree).
  - CHILDREN/LEAF: leaf MEMBER_OF children-of-the-forest (was 0 incoming), leaf TEACHES bran.
  - SECONDARY CAST: meera TRAVELS_WITH/RESCUES/AGENT_IN, osha TRAVELS_WITH rickon, the iconic
    Bran-wargs-Hodor-in-combat instance, the coldhands/brynden REVEALS_TO identity thread.
  - PLACE/STRUCTURAL: black-gate LOCATED_AT nightfort; bran/brynden LOCATED_AT the cave;
    wight-ambush SUB_BEAT_OF bran-reaches-the-cave (de-islands the legacy orphan).

POST-VERIFY MODIFICATIONS (NOT in this additive mint — applied after fresh-verify by
finalize_bran_enrichment.py, see candidates.json.post_verify_modifications): the `three-eyed-crow`
slug-trap fix — re-point coldhands SERVES/SWORN_TO from the species node to `brynden-rivers`;
retire `three-eyed-crow TEACHES bran-stark` (superseded by the minted brynden TUTORS) and
`three-eyed-crow HOLDS_TITLE lord` (brynden already holds it). Leaves the species node islanded
-> flagged for a future cross-identity pass (do NOT SAME_AS species<->character).

Reads working/enrichment/bran/candidates.json; RE-GREPS each quote in its chapter file for the
authoritative line (FAIL-fast if a quote moved). Safeguards mirror the prior enrichment mints:
backup, re-run guard, slug pre-check.

Theory gate: greenseer cosmology (Night's King / time-travel / Hodor-origin / Jojen-paste /
Bloodraven-manipulates) NOT engaged — only textual fact + dreams that predict events that happen.
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
CAND = REPO / "working" / "enrichment" / "bran" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-bran-enrichment-2026-06-25.jsonl"

RUN_ID = "bran-enrichment-s146"
PRODUCED_AT = "2026-06-25T00:00:00+00:00"

NEW_NODE_SLUGS = set()  # edge-only pass


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    """Grep the whole chapter file for the normalized quote; return its 1-indexed line."""
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


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-bran-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


def make_edge_row(e):
    book, chapter = e["book"], e["chapter"]
    line = authoritative_line(book, chapter, e["quote"])
    row = {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        **common(),
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": e["note"],
        "candidate_id": e["id"],
    }
    if e.get("verify"):
        row["verified_by"] = "pending"
    return row


def main():
    data = json.loads(CAND.read_text())
    edges = data["edges"]

    all_slugs = set()
    for e in edges:
        all_slugs.add(e["source"]); all_slugs.add(e["target"])
    resolved, missing = precheck_slugs(all_slugs - NEW_NODE_SLUGS)
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

    tc = {}
    for e in edges:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
    print("\n── SUMMARY ──")
    print(f"Edges appended ({len(new_rows)}):")
    for t, c in sorted(tc.items()):
        print(f"  {t}: {c}")
    print(f"edges.jsonl: {len(existing)} -> {len(out)} lines (+{len(new_rows)})")


if __name__ == "__main__":
    main()
