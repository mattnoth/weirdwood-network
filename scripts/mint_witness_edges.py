#!/usr/bin/env python3
"""Mint the first WITNESS_IN role edges + flip the one mis-typed ATTENDS (S117).

WITNESS_IN (new edge type, architecture.md): the observer/perceiver participant
slot on an event hub. Default EDGE (the Q2 three-lens panel consensus: reify a
witnessing as its own NODE only when the *act of seeing* owns an outgoing causal
edge; otherwise it is the perceiver role-edge onto the existing event).

Adds (Tier-1 role edges, verbatim-cited; text-anchor gate satisfied — the source
actually SEES it):
  - sansa-stark   WITNESS_IN execution-of-eddard-stark   (agot-sansa-06:15)
  - arianne-martell WITNESS_IN myrcella-is-maimed-by-darkstar (affc-the-queenmaker-01:291)

Flip (1 mis-typed ATTENDS -> WITNESS_IN, from the 42-edge ATTENDS re-audit):
  - hoster-tully battle-of-the-camps : ATTENDS -> WITNESS_IN
    (he was carried to the gatehouse and "watched from the battlements" a discrete
    violent engagement — a witnessed incident, not voluntary audience at a gathering.
    Existing evidence_quote already supports it; only the type changes.)

NOT included (routed elsewhere by the re-audit, not WITNESS_IN fixes):
  - 2 mistargeted ATTENDS edges (cersei->robert-baratheon = a character; ghost-of-
    high-heart->summerhall = a place) -> retarget queue (todos).
  - 5 siege-of-riverrun ATTENDS edges -> GARRISONS / HELD_AT relation audit (todos).

Re-run safe: refuses to re-add if run_id already present; flip is idempotent.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-witness-edges-2026-06-21.jsonl"

RUN_ID = "witness-edges-s117-20260621"
PRODUCED_AT = "2026-06-21T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "curator-witness-role",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-witness",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
ADDS = [
    ("sansa-stark", "WITNESS_IN", "execution-of-eddard-stark", 1,
     "agot", "agot-sansa-06", 15,
     "Waking or sleeping, she saw him, saw the gold cloaks fling him down, saw Ser Ilyn striding forward, unsheathing Ice from the scabbard on his back",
     "Sansa, on the dais at the Great Sept of Baelor, could not turn her head as Ser Ilyn beheaded her father — the defining trauma she relives waking and sleeping. Perceiver/observer role on the execution hub => WITNESS_IN Tier-1."),
    ("arianne-martell", "WITNESS_IN", "myrcella-is-maimed-by-darkstar", 1,
     "affc", "affc-the-queenmaker-01", 291,
     "Myrcella was on the ground, wailing, shaking, her pale face in her hands, blood streaming through her fingers.",
     "Arianne, thrown from her horse in the ambush, sees the maimed Myrcella wailing with blood streaming through her fingers — bystander/perceiver to the maiming Darkstar performs. => WITNESS_IN Tier-1."),
]

# flip: (source_slug, target_slug, from_type, to_type)
FLIP = ("hoster-tully", "battle-of-the-camps", "ATTENDS", "WITNESS_IN")


def make_row(spec):
    src, etype, tgt, tier, book, chap, line, quote, asserted = spec
    return {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **COMMON,
        "evidence_book": book,
        "evidence_chapter": chap,
        "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    already_added = any(RUN_ID in ln for ln in lines)

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    # flip the one ATTENDS -> WITNESS_IN (idempotent)
    src, tgt, from_t, to_t = FLIP
    flipped = 0
    out = []
    for ln in lines:
        if (f'"source_slug": "{src}"' in ln and f'"target_slug": "{tgt}"' in ln
                and f'"edge_type": "{from_t}"' in ln):
            row = json.loads(ln)
            row["edge_type"] = to_t
            row["typed_by"] = "curator-witness-reclass"
            row["reclass_note"] = f"{from_t}->{to_t} (S117 ATTENDS re-audit: watched a discrete engagement from the battlements)"
            out.append(json.dumps(row, ensure_ascii=False))
            flipped += 1
        else:
            out.append(ln)

    new_rows = [] if already_added else [json.dumps(make_row(s), ensure_ascii=False) for s in ADDS]
    out.extend(new_rows)

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Flipped {flipped} ATTENDS -> WITNESS_IN ({src} -> {tgt}).")
    if already_added:
        print(f"ADDS skipped (run_id {RUN_ID} already present).")
    else:
        print(f"Added {len(new_rows)} WITNESS_IN role edges (Tier-1).")
    print(f"edges.jsonl now: {len(out)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
