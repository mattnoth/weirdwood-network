#!/usr/bin/env python3
"""Finalize the D5 "Arya's flight & Harrenhal" enrichment (S154) after independent fresh-verify
(8 CONFIRM / 1 ADJUST / 0 REJECT; theory-gate CLEAN; all 3 traps held; 0 drift 44/44).

Applies to graph/edges/edges.jsonl:
  DROP (run_id d5-arya-harrenhal-enrichment-s154, by candidate_id):
    - E1  gregor-raids-the-riverlands ENABLES fight-at-the-holdfast — SCOPE MISMATCH (fresh-verify ADJUST).
          `gregor-raids-the-riverlands` is explicitly the AGOT 298 AC *opening* raids (Sherrer/Wendish
          Town/Mummer's Ford) and the deliberate "hard-stop terminus" of the Bran's-fall causal chain
          (its own node body, S105). The holdfast attack is the 299 AC ACOK Riverlands campaign (Amory
          Lorch's column on the Beric-hunt) — a different campaign/year. No clean ACOK-chevauchee node
          exists to re-point to, so retire the bridge rather than over-extend the AGOT terminus. The hub
          keeps its causal-OUT (E2 CAUSES arya-captured), so the D5->Braavos chain still walks end-to-end.

  RE-CITE (existing S150 edge, matched by source/type/target):
    - iron-coin GIFTED_TO arya-stark — was cited to the ASOS recollection (asos-arya-13:255); re-ground
      to the actual giving scene (acok-arya-09, "He lifted her hand and pressed a small coin into her
      palm."). Adds recited_by=fresh-verify-s154; preserves the original run_id.

  STAMP verified_by='fresh-verify-s154' on every surviving run_id edge whose verified_by=='pending'.

Backup + re-run guard (aborts if E1 already gone). Idempotent."""
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-d5-arya-harrenhal-finalize-2026-06-26.jsonl"
RUN_ID = "d5-arya-harrenhal-enrichment-s154"
VERIFIED_BY = "fresh-verify-s154"

DROP_CIDS = {"E1"}

RECITE_QUOTE = "He lifted her hand and pressed a small coin into her palm."
RECITE_CHAPTER = "acok-arya-09"
RECITE_BOOK = "acok"


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def find_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    sys.exit(f"ABORT: re-cite quote not found in {chapter}.md")


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    if not any(r.get("run_id") == RUN_ID and r.get("candidate_id") in DROP_CIDS for r in rows):
        sys.exit("ABORT: E1 not present — finalize already applied (or mint missing).")

    recite_line = find_line(RECITE_BOOK, RECITE_CHAPTER, RECITE_QUOTE)
    recite_ref = f"sources/chapters/{RECITE_BOOK}/{RECITE_CHAPTER}.md:{recite_line}"

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    out = []
    n_drop = n_stamp = n_recite = 0
    for r in rows:
        if r.get("run_id") == RUN_ID and r.get("candidate_id") in DROP_CIDS:
            n_drop += 1
            continue  # drop E1
        if r.get("run_id") == RUN_ID and r.get("verified_by") == "pending":
            r["verified_by"] = VERIFIED_BY
            n_stamp += 1
        if (r.get("source_slug") == "iron-coin" and r.get("edge_type") == "GIFTED_TO"
                and r.get("target_slug") == "arya-stark"):
            r["evidence_ref"] = recite_ref
            r["evidence_book"] = RECITE_BOOK
            r["evidence_chapter"] = RECITE_CHAPTER
            r["evidence_quote"] = RECITE_QUOTE
            r["recited_by"] = VERIFIED_BY
            n_recite += 1
        out.append(json.dumps(r, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"Backup -> {BACKUP.relative_to(REPO)}")
    print(f"Edges dropped: {n_drop}  (E1 gregor-raids ENABLES holdfast — campaign scope mismatch)")
    print(f"iron-coin GIFTED_TO re-cited: {n_recite}  -> {recite_ref}")
    print(f"verified_by stamped: {n_stamp}")
    print(f"Final edge count: {len(out)}")


if __name__ == "__main__":
    main()
