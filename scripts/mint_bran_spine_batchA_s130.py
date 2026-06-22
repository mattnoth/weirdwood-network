#!/usr/bin/env python3
"""Mint BRAN causal spine — Batch A (S130): BR3 + BR1 + BR2.

Container `bran` is greenfield (Spine 2 entirely dark). Batch A lights the two
ANCHORED junctures (off the built sack hub + the built fall spine) plus the
lowest-load recognition node. Spec: working/bran-decomposition.md (S129 dip) §5,
confirmed by the Batch-A research dip (line-checked quotes + agency adjudication).

3 node files minted out-of-band (BR3 crypts, BR1 coma, BR2 warg-naming).
Build-step 0 retags (direwolf +[bran,wo5k], sack +[bran]) already applied.

Junctures (one run_id each so fresh-verify can flip verified_by per-arc):
  BR3 (Rank 1) — sack CAUSES crypts-survival (opens Spine 2). Osha ENABLES (feigned
                 defection = precondition) + AGENT_IN; bran AGENT_IN (plans wolf-trail);
                 rickon VICTIM_IN. Luwin's counsel -> party-split deferred to Batch B.
  BR1 (Rank 2) — fall TRIGGERS coma-dream (fall opens the door; crow is the real agent).
                 brynden-rivers MOTIVATES (the crow = Bloodraven, dream-summoner, light
                 agency edge NOT a separate scene node); bran AGENT_IN (chooses to fly).
                 Waking folded into BR1 as terminus (no distinct outgoing edge).
  BR2 (Rank 7) — coma ENABLES the warg-naming (RECOGNITION not cause; gift predates
                 the naming, acok-bran-01:69). jojen AGENT_IN; bran VICTIM_IN.

Slug discipline: greenseer/crow edges target `brynden-rivers` (NOT the `three-eyed-crow`
species node). Wolf role edges (Batch B) target `summer` (NOT the orphan `brans-direwolf`).

Edge types: locked vocab only (CAUSES / TRIGGERS / ENABLES / MOTIVATES + roles
AGENT_IN / VICTIM_IN). Causal/agency edges carry verified_by='pending-*-verify' until
a fresh subagent confirms; Tier-1 role edges do not.
Re-run safe: aborts if any run_id is already present.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-bran-spine-batchA-2026-06-22.jsonl"

RUN_BR3 = "causal-arc-br3-sack-crypts-20260622"
RUN_BR1 = "causal-arc-br1-coma-crow-20260622"
RUN_BR2 = "causal-arc-br2-warg-naming-20260622"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"


def common(run_id):
    return {
        "decision": "emit_edge",
        "candidate_kind": "causal-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-causal-arc",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": run_id,
    }


# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
BR3 = [
    ("sack-of-winterfell", "CAUSES", "bran-and-rickon-survive-the-sack-in-the-crypts", 2, "acok", "acok-bran-07", 155,
     "We never went, said Bran. Well, only to the edge, and then doubled back. I sent the wolves on to make a trail, but we hid in Father's tomb.",
     "The sack is the coarse mediated cause of the boys' survival-in-hiding; the crypt-hiding is the Stark-side consequence of Theon's assault. Coarse hub -> consequence => CAUSES Tier-2 (not ENABLES -- the sack is the active cause, not merely a precondition).",
     "pending-br3-verify"),
    ("osha", "ENABLES", "bran-and-rickon-survive-the-sack-in-the-crypts", 2, "acok", "acok-bran-06", 179,
     "I've had a bellyful of it. Put a spear in my hand again.",
     "Osha's earlier feigned defection (to stay near Bran) is the precondition that makes the crypt-hiding possible -- she becomes the armed guide who leads them down. Precondition, not active cause => ENABLES Tier-2. Genuine human agency, not collapsed into the sack->survival CAUSES.",
     "pending-br3-verify"),
    ("osha", "AGENT_IN", "bran-and-rickon-survive-the-sack-in-the-crypts", 1, "acok", "acok-bran-07", 99,
     "I'll grope my way up.",
     "Osha actively guides, scouts and protects the party in the crypts. Acting participant => AGENT_IN Tier-1.",
     None),
    ("bran-stark", "AGENT_IN", "bran-and-rickon-survive-the-sack-in-the-crypts", 1, "acok", "acok-bran-07", 155,
     "I sent the wolves on to make a trail, but we hid in Father's tomb.",
     "Bran devised the wolf-trail decoy and directs the party -- he is the planner of the survival, not a passive victim => AGENT_IN Tier-1.",
     None),
    ("rickon-stark", "VICTIM_IN", "bran-and-rickon-survive-the-sack-in-the-crypts", 1, "acok", "acok-bran-07", 85,
     "Are we going home? ... I want my horse. ... Are we going where Shaggydog is?",
     "Rickon is the carried child-survivor, passive through the hiding (the agency is Bran's and Osha's) => VICTIM_IN Tier-1.",
     None),
]

BR1 = [
    ("jaime-pushes-bran-from-the-tower", "TRIGGERS", "bran-s-coma-and-the-three-eyed-crow", 2, "agot", "agot-bran-03", 47,
     "You'll die when you hit the ground, the crow said.",
     "The fall is the named specific spark that opens the coma-dream; the crow's intervention (not the fall itself) is the real agent of what happens inside. Specific spark -> the beat => TRIGGERS Tier-2 (not CAUSES). Extends the built fall spine one hop.",
     "pending-br1-verify"),
    ("brynden-rivers", "MOTIVATES", "bran-s-coma-and-the-three-eyed-crow", 2, "agot", "agot-bran-03", 107,
     "Now, Bran, the crow urged. Choose. Fly or die.",
     "The three-eyed crow (Brynden Rivers / Bloodraven, reaching through the weirwood net) is the summoner who drives Bran's choice to live. Agency routed through the human actor => MOTIVATES Tier-2. Target is `brynden-rivers`, NOT the `three-eyed-crow` species node; modeled as a light agency edge, not a separate dream-scene node.",
     "pending-br1-verify"),
    ("bran-stark", "AGENT_IN", "bran-s-coma-and-the-three-eyed-crow", 1, "agot", "agot-bran-03", 111,
     "Bran spread his arms and flew.",
     "Bran makes the active choice (fly vs die) inside the dream -- the choice is the dramatic core of the beat => AGENT_IN Tier-1.",
     None),
]

BR2 = [
    ("bran-s-coma-and-the-three-eyed-crow", "ENABLES", "jojen-reed-names-bran-a-warg", 2, "acok", "acok-bran-01", 69,
     "When I sleep I turn into a wolf.",
     "The warg-gift opened in the coma and predates Jojen's naming -- Jojen recognizes a faculty that already exists. The coma is the precondition for the recognition => ENABLES Tier-2 (NOT CAUSES; the naming does not create the gift -- confirmed anti-signal).",
     "pending-br2-verify"),
    ("jojen-reed", "AGENT_IN", "jojen-reed-names-bran-a-warg", 1, "acok", "acok-bran-05", 97,
     "Warg, said Jojen Reed.",
     "Jojen is the actor who performs the naming/recognition of Bran's gift => AGENT_IN Tier-1.",
     None),
    ("bran-stark", "VICTIM_IN", "jojen-reed-names-bran-a-warg", 1, "acok", "acok-bran-05", 107,
     "I'm not like that, Bran said. I'm not. It's only dreams.",
     "Bran is the subject being named (and resisting); the agency in this beat is Jojen's => VICTIM_IN Tier-1.",
     None),
]

ARCS = [(RUN_BR3, BR3), (RUN_BR1, BR1), (RUN_BR2, BR2)]


def make_row(spec, run_id):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **common(run_id),
        "evidence_book": book,
        "evidence_chapter": chap,
        "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for _, specs in ARCS:
        for s in specs:
            all_slugs.add(s[0])
            all_slugs.add(s[2])
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed (non-existent targets): {missing}")
    print(f"slug pre-check OK: {len(resolved)} resolved.")

    lines = EDGES.read_text(encoding="utf-8").splitlines()
    for run_id, _ in ARCS:
        if any(run_id in ln for ln in lines):
            sys.exit(f"ABORT: run_id {run_id} already present -- already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = []
    for run_id, specs in ARCS:
        new_rows.extend(make_row(s, run_id) for s in specs)

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    causal_types = ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES")
    n_causal = sum(1 for _, specs in ARCS for s in specs if s[1] in causal_types)
    n_role = sum(1 for _, specs in ARCS for s in specs if s[1] in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WITNESS_IN"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges: {n_causal} causal/agency + {n_role} role Tier-1.")
    print(f"  BR3={len(BR3)}  BR1={len(BR1)}  BR2={len(BR2)}")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
