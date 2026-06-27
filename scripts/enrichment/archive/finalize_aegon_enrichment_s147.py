#!/usr/bin/env python3
"""Finalize AEGON enrichment pass 1 (S147) — apply the independent fresh-verify verdicts
(working/enrichment/aegon/fresh-verify.md: 30 CONFIRM / 3 ADJUST / 2 REJECT + 1 node REJECT
+ 1 confirmed addition).

Actions on the aegon-enrichment-s147 run rows in graph/edges/edges.jsonl:
  - DROP K1 (`assassinations PREVENTS kevan-reconciles-the-realm`) + K2
    (`kevan-lannister AGENT_IN kevan-reconciles-the-realm`) — REJECTED: phantom
    counterfactual event minted only to fix a 0-outgoing dead-end; re-models KL politics
    the AEGON decomposition warned against. Delete the kevan-reconciles-the-realm node too.
  - ADJUST V2 (`varys DECEIVES golden-company`): confidence_tier 1 -> 2 (the cite is
    JonCon's reported memory of Varys's words, not a witnessed scene).
  - ADJUST T7 (`black-balaq COMMANDS_IN landing`): note clarification — Balaq commands the
    ARCHER CONTINGENT deployed from the landing, not the landing hub itself (Edoryen does).
  - STAMP verified_by 'pending' -> 'fresh-verify-s147' on all surviving CONFIRM/ADJUST edges.
  - ADD M1 (`tyrion-lannister MANIPULATES aegon-targaryen-young-griff`, qualifier
    via_false_information) — CONFIRMED addition (intended at synthesis, omitted from the mint).
    adwd-tyrion-06:155 "I lied. Trust no one. And keep your dragon close."

Net: 37 minted -2 (K1/K2) +1 (M1) = 36 surviving edges; 3 nodes -1 (kevan) = 2 nodes.
Re-greps the M1 quote for the authoritative line (FAIL-fast). Backup first.
"""
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
KEVAN_NODE = REPO / "graph" / "nodes" / "events" / "kevan-reconciles-the-realm.node.md"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-aegon-finalize-2026-06-25.jsonl"

RUN_ID = "aegon-enrichment-s147"
PRODUCED_AT = "2026-06-25T00:00:00+00:00"
VERIFIER = "fresh-verify-s147"

DROP_IDS = {"K1", "K2"}
T7_NOTE = ("GC archer-command: Black Balaq commands the thousand-bow archer CONTINGENT deployed "
           "from the landing (Gorys Edoryen commands the landing camp itself); the archers are the "
           "operationally central force enabling every simultaneous taking.")


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    sys.exit(f"ABORT: quote not found in {chapter}.md -> {quote!r}")


def main():
    raw = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]

    # Re-run guard: M1 must not already be present.
    if any('"candidate_id": "M1"' in ln and RUN_ID in ln for ln in raw):
        sys.exit("ABORT: M1 already present — finalize already run.")

    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written -> {BACKUP.relative_to(REPO)}")

    out = []
    dropped = stamped = adjusted = 0
    for ln in raw:
        e = json.loads(ln)
        if e.get("run_id") == RUN_ID:
            cid = e.get("candidate_id")
            if cid in DROP_IDS:
                dropped += 1
                continue
            if cid == "V2":
                e["confidence_tier"] = 2; adjusted += 1
            if cid == "T7":
                e["asserted_relation"] = T7_NOTE; adjusted += 1
            if e.get("verified_by") == "pending":
                e["verified_by"] = VERIFIER; stamped += 1
            out.append(json.dumps(e, ensure_ascii=False))
        else:
            out.append(ln)

    # ADD M1 — tyrion MANIPULATES aegon (CONFIRMED addition).
    book, chapter, quote = "adwd", "adwd-tyrion-06", "I lied. Trust no one. And keep your dragon close."
    line = authoritative_line(book, chapter, quote)
    m1 = {
        "edge_type": "MANIPULATES",
        "source_slug": "tyrion-lannister",
        "target_slug": "aegon-targaryen-young-griff",
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-aegon-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": 2,
        "qualifier": "via_false_information",
        "asserted_relation": ("Tyrion goads Aegon to sail west via the cyvasse game using deliberately "
                              "false advice ('I lied'); complements tyrion MOTIVATES golden-company-sails "
                              "(event-level) with the person-to-person mechanism. Aegon acts unknowingly."),
        "candidate_id": "M1",
        "verified_by": VERIFIER,
    }
    out.append(json.dumps(m1, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    if KEVAN_NODE.exists():
        KEVAN_NODE.unlink()
        print(f"Deleted node: {KEVAN_NODE.relative_to(REPO)}")

    print("\n── FINALIZE SUMMARY ──")
    print(f"Dropped (REJECT): {dropped}  (K1, K2)")
    print(f"Adjusted: {adjusted}  (V2 tier->2, T7 note)")
    print(f"verified_by stamped: {stamped}")
    print(f"Added: 1  (M1 tyrion MANIPULATES aegon @ {chapter}:{line})")
    print(f"edges.jsonl: {len(raw)} -> {len(out)} lines  (net {len(out)-len(raw):+d})")


if __name__ == "__main__":
    main()
