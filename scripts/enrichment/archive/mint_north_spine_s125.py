#!/usr/bin/env python3
"""Mint the NORTH spine top-3 junctures (S125): N5 + N2 + N1.

NORTH decomposition (working/north-decomposition.md), ranked top-3:
  N5 (Rank 1) — Red Wedding -> Roose named Warden of the North (Bolton-thread entry).
                1 mint (roose-named-warden-of-the-north, written as .node.md) + 3 edges.
  N2 (Rank 2) — Wall battle -> Stannis routs wildlings -> Mance captured (the NORTH pivot).
                ENRICH, do NOT duplicate-mint: battle-beneath-the-wall ALREADY is "Stannis routs
                the wildlings" (its final section + Aftermath). Only 1 bridge mint
                (stannis-moves-to-the-wall, [wo5k, north] seam, written as .node.md) + 5 edges.
  N1 (Rank 3) — Great Ranging -> Fight at the Fist -> Mutiny at Craster's Keep (Watch spine).
                0 mints. great-ranging declared two CAUSES in node prose but NONE were in
                edges.jsonl (staging-vs-live gap, confirmed: grep great-ranging edges.jsonl = 0).
                CAUSAL CORRECTION (fresh research, S125): the declared `great-ranging CAUSES
                mutiny-at-crasters-keep` is re-pointed to `fight-at-the-fist CAUSES mutiny` --
                the proximate cause of the mutiny is the Fist catastrophe (the broken, starving
                Fist survivors who straggle into Craster's erupt over food and kill Craster then
                Mormont). Chain, not fan. + role edges (Mormont/Craster VICTIM_IN; Ollo/Dirk
                AGENT_IN).

Three independent run_ids so fresh-verify can flip verified_by per-arc. One shared backup.
Re-run safe: aborts if any of the three run_ids is already present.

Edge types: locked vocab only (CAUSES / ENABLES / MOTIVATES + roles AGENT_IN / VICTIM_IN).
Causal/agency edges carry verified_by='pending-*-verify' until a fresh subagent confirms.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-north-spine-2026-06-22.jsonl"

RUN_N5 = "causal-arc-n5-roose-warden-20260622"
RUN_N2 = "causal-arc-n2-stannis-wall-20260622"
RUN_N1 = "causal-arc-n1-great-ranging-20260622"
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
N5 = [
    ("red-wedding", "CAUSES", "roose-named-warden-of-the-north", 2, "asos", "asos-jon-11", 129,
     "Tywin Lannister has named Roose Bolton his Warden of the North, to reward him for betraying your brother.",
     "The wardenship is Tywin's explicit reward FOR the Red Wedding betrayal ('to reward him for betraying your brother'). The Red Wedding is the prior, prerequisite event; the appointment is its off-page consequence (the payoff Roose was promised). CAUSES Tier-2.",
     "fresh-subagent-confirm-2026-06-22-n5"),
    # DROPPED at fresh-verify (2026-06-22): (roose-named-warden MOTIVATES roose-bolton).
    #   The proposed cite (asos-tyrion-06:215) is Tywin describing his OWN plan, not Roose being
    #   motivated by the office, and Roose is not present in the scene -- the quote does not support
    #   the agency claim. A Roose-consolidation MOTIVATES edge would need a Roose-action quote (he
    #   holds/wields the wardenship); deferred to a later NORTH enrichment pass.
    ("tywin-lannister", "AGENT_IN", "roose-named-warden-of-the-north", 1, "asos", "asos-jon-11", 129,
     "Tywin Lannister has named Roose Bolton his Warden of the North",
     "Tywin is the explicit actor who confers the wardenship ('Tywin Lannister has named...'). Role edge => AGENT_IN Tier-1.",
     None),
]

N2 = [
    ("attack-on-castle-black", "CAUSES", "battle-beneath-the-wall", 3, "asos", "asos-jon-08", 55,
     "They must take the gate, or they cannot pass.",
     "The Thenns' attack from the south (Styr) was meant to open the gate from inside; its failure forced Mance to assault the gate directly. fresh-verify: the book cite grounds gate-necessity only ('They must take the gate, or they cannot pass'); the failure->forced-assault MECHANISM is wiki-stated, not book-grounded by this cite => downgraded to Tier-3. Real causation (a prior, separately-located prerequisite that failed), not mere sequence.",
     "fresh-subagent-confirm-2026-06-22-n2"),
    ("stannis-retreats-to-dragonstone", "ENABLES", "stannis-moves-to-the-wall", 2, "asos", "asos-davos-05", 283,
     "How could the Watch have looked to him for help? They may not know how weak he is, how lost his cause.",
     "The retreat is the enabling precondition, not the efficient cause: Stannis's broken, cause-lost state on Dragonstone is what creates the opening for Davos to read him the Watch's plea and sell the Wall as the path to a kingdom. A pre-Blackwater Stannis would have ignored the letter. Prerequisite-state => ENABLES Tier-2. fresh-verify CONFIRM.",
     "fresh-subagent-confirm-2026-06-22-n2"),
    ("stannis-moves-to-the-wall", "CAUSES", "battle-beneath-the-wall", 2, "asos", "asos-jon-10", 287,
     "when the trumpets blew again and the knights charged, the name they cried was “Stannis! Stannis! STANNIS!”",
     "RETYPED at fresh-verify (2026-06-22): originally `bridge CAUSES mance-rayder-brought-to-execution` -- REJECTED as cite-mismatched (the Davos cite is counsel, not Stannis's act) and as skipping the battle. Re-pointed to battle-beneath-the-wall, SCOPED TO THE ROUT: Stannis's arrival and charge cause the wildlings' DEFEAT (the rout that resolves the battle), NOT the battle's occurrence (Mance's assault was Stannis-independent). Grounded by Jon's POV of Stannis's knights charging. CAUSES Tier-2.",
     "fresh-subagent-confirm-2026-06-22-n2"),
    ("battle-beneath-the-wall", "CAUSES", "mance-rayder-brought-to-execution", 2, "asos", "asos-jon-11", 155,
     "He will leave me no choice but to give him to the flames.",
     "Mance is defeated and captured AT the battle; the capture is the prerequisite for the execution. Stannis, holding Mance, resolves to burn him. Chronologically prior + prerequisite (distinct downstream event, not a constitutive action within the battle) => CAUSES Tier-2. fresh-verify CONFIRM. The NORTH spine now walks: retreat ENABLES bridge CAUSES battle CAUSES execution.",
     "fresh-subagent-confirm-2026-06-22-n2"),
    ("stannis-baratheon", "AGENT_IN", "stannis-moves-to-the-wall", 1, "asos", "asos-jon-11", 155,
     "Whilst your brothers have been struggling to decide who shall lead them, I have been speaking with this Mance Rayder.",
     "Stannis is the agent who sails north and relieves the Wall (here speaking at the Wall, having come and dealt with Mance). Davos counsels but has no clean role type (a counselor is not COMMANDS_IN). Role edge => AGENT_IN Tier-1.",
     None),
]

N1 = [
    ("great-ranging", "CAUSES", "fight-at-the-fist", 2, "asos", "asos-samwell-01", 49,
     "He had written out the messages ahead of time, short messages and simple, telling of an attack on the Fist of the First Men",
     "The ranging's advance and fortified base camp at the Fist is what put the Watch there to be attacked by the Others/wights. The Fist engagement is a consequence of the ranging, a distinct named battle (not a sub-beat of the ranging). CAUSES Tier-2 (matches the node-prose-declared edge; just wiring it). fresh-verify CONFIRM.",
     "fresh-subagent-confirm-2026-06-22-n1"),
    ("fight-at-the-fist", "CAUSES", "mutiny-at-crasters-keep", 2, "asos", "asos-samwell-02", 111,
     "Forty-four had come straggling into Craster’s out of the storm, out of the sixty-odd who’d cut their way free of the Fist, but three of those had died of their wounds, and Bannen would soon make four.",
     "CAUSAL CORRECTION: the proximate cause of the mutiny is the Fist catastrophe, NOT the great-ranging directly. The mutineers are the broken, starving Fist survivors who straggled into Craster's; their post-Fist desperation over Craster's hidden food detonates the mutiny. SUPERSEDES the great-ranging->mutiny edge declared in great-ranging.node.md prose. CAUSES Tier-2. fresh-verify CONFIRM.",
     "fresh-subagent-confirm-2026-06-22-n1"),
    ("jeor-mormont", "VICTIM_IN", "mutiny-at-crasters-keep", 1, "asos", "asos-samwell-02", 317,
     "He twisted free of the old man’s grasp, shoved the knife into Mormont’s belly, and yanked it out again, all red.",
     "Lord Commander Jeor Mormont is killed in the mutiny. Role edge => VICTIM_IN Tier-1.",
     None),
    ("ollo-lophand", "AGENT_IN", "mutiny-at-crasters-keep", 1, "asos", "asos-samwell-02", 317,
     "He twisted free of the old man’s grasp, shoved the knife into Mormont’s belly, and yanked it out again, all red.",
     "Ollo Lophand is the named killer of the Lord Commander -- the defining act of the mutiny. Role edge => AGENT_IN Tier-1.",
     None),
    ("craster", "VICTIM_IN", "mutiny-at-crasters-keep", 1, "asos", "asos-samwell-02", 311,
     "Dirk had grabbed him by the hair, yanked his head back, and opened his throat ear to ear with one long slash.",
     "Craster is killed in the mutiny (its first death). Role edge => VICTIM_IN Tier-1.",
     None),
    ("dirk", "AGENT_IN", "mutiny-at-crasters-keep", 1, "asos", "asos-samwell-02", 311,
     "Dirk had grabbed him by the hair, yanked his head back, and opened his throat ear to ear with one long slash.",
     "Dirk is the named killer of Craster. Role edge => AGENT_IN Tier-1.",
     None),
]

ARCS = [(RUN_N5, N5), (RUN_N2, N2), (RUN_N1, N1)]


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
    n_role = len(new_rows) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal/agency + {n_role} role Tier-1).")
    print(f"  N5={len(N5)}  N2={len(N2)}  N1={len(N1)}")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
