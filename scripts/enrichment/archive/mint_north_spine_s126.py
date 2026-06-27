#!/usr/bin/env python3
"""Mint the NORTH spine N3 + N4 junctures (S126): the Jon Lord-Commander spine.

NORTH decomposition (working/north-decomposition.md §3 Rank 4 + Rank 5):
  N3 (Rank 4) — LC election -> Slynt execution -> Jon's authority established.
                1 node minted out-of-band (jon-elected-lord-commander, event.ceremony,
                [north, jon]). Edges: battle-beneath-the-wall ENABLES the choosing
                (research adjudicated ENABLES, not CAUSES: post-battle precondition, not
                the precipitating cause -- Jon's win was Sam-engineered); choosing CAUSES
                execution-of-janos-slynt (office = prerequisite for the authority to
                behead Slynt); choosing MOTIVATES jon-snow (command reorients his agency);
                jon-snow AGENT_IN the choosing (Tier-1 role).

  N4 (Rank 5) — Free folk through the Wall -> Pink Letter -> the stabbing (NORTH terminus).
                2 nodes minted out-of-band (jon-allows-free-folk-through-the-wall event.decree
                [north, jon]; pink-letter-delivered event.incident [north]). The merge of
                mutiny-at-castle-black -> jon-is-stabbed-repeatedly was done out-of-band
                (survivor rewrite + redirect stub). AGENCY-PRESERVING TOPOLOGY (fresh research
                REJECTED any blunt free-folk->stabbing CAUSES): upstream causation routes
                through MOTIVATES bowen-marsh (the human actor, already AGENT_IN the stabbing)
                + the Pink-Letter TRIGGERS spark. Edges: execution-of-janos-slynt MOTIVATES
                bowen-marsh (seeds the grievance -- WEAKEST edge, flagged for fresh-verify);
                jon-allows-free-folk-through-the-wall MOTIVATES bowen-marsh (the central
                provocation); pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly (the
                Shieldhall march announcement is the spark); jon-snow AGENT_IN both new nodes.

Also DROPS one junk edge at this build: battle-on-the-green-fork PRECEDES mutiny-at-castle-black
(a bogus cross-year derived-chronology artifact on the now-merged loser node).

Two independent run_ids so fresh-verify can flip verified_by per-arc. One shared backup.
Re-run safe: aborts if either run_id is already present.

Edge types: locked vocab only (ENABLES / CAUSES / MOTIVATES / TRIGGERS + roles AGENT_IN).
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-north-spine-n3n4-2026-06-24.jsonl"

RUN_N3 = "causal-arc-n3-lc-election-20260624"
RUN_N4 = "causal-arc-n4-pink-letter-stabbing-20260624"
PRODUCED_AT = "2026-06-24T00:00:00+00:00"

# The junk PRECEDES edge to drop (loser of the N4 merge; bogus cross-year chronology).
DROP_PREDICATE = lambda r: (
    r.get("edge_type") == "PRECEDES"
    and r.get("source_slug") == "battle-on-the-green-fork"
    and r.get("target_slug") == "mutiny-at-castle-black"
)


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
N3 = [
    ("battle-beneath-the-wall", "ENABLES", "jon-elected-lord-commander", 2, "asos", "asos-jon-12", 41,
     "If we let Stannis choose our Lord Commander, we become his bannermen in all but name.",
     "ENABLES, not CAUSES (fresh research adjudication): the post-battle conditions -- a leaderless Watch (Mormont dead since Craster's) and Stannis present at Castle Black pressuring the succession -- are the precondition for a choosing to occur. The battle did not precipitate Jon's SPECIFIC win (engineered by Sam, clinched by Mormont's raven). Enabling state => ENABLES Tier-2.",
     "pending-n3-verify"),
    ("jon-elected-lord-commander", "CAUSES", "execution-of-janos-slynt", 2, "adwd", "adwd-jon-02", 385,
     "Longclaw descended.",
     "Jon's election is the prerequisite that gives him the authority to sentence and behead Slynt for refusing the command to take Greyguard. Without the office there is no command to refuse and no authority to execute. Prior prerequisite event (not a constitutive action within the execution) => CAUSES Tier-2.",
     "pending-n3-verify"),
    ("jon-elected-lord-commander", "MOTIVATES", "jon-snow", 2, "asos", "asos-jon-12", 139,
     "The Wall was his, the night was dark, and he had a king to face.",
     "The office immediately reorients Jon's agency -- the chapter's closing line registers the Wall and the command as now his responsibility. The role drives his subsequent choices to enforce his authority (the Slynt execution, the free-folk decree). Office -> motivates the character's downstream agency => MOTIVATES Tier-2.",
     "pending-n3-verify"),
    ("jon-snow", "AGENT_IN", "jon-elected-lord-commander", 1, "asos", "asos-jon-12", 87,
     "Your name has been put forth as Lord Commander, Jon.",
     "Jon is the elected party -- Aemon announces his name has been put forth, and he is chosen 998th Lord Commander. Central participant => AGENT_IN Tier-1.",
     None),
]

N4 = [
    ("execution-of-janos-slynt", "MOTIVATES", "bowen-marsh", 2, "adwd", "adwd-jon-13", 153,
     "I know all these men by their deeds. We should be fitting them for nooses, not giving them our castles.",
     "Slynt's execution established Jon's willingness to kill disobedient conservative officers, seeding Marsh's accumulating fear and disapproval of Jon's rule that culminates in the mutiny. NOTE (flagged at mint): the execution is not named in this chapter; the edge rests on Marsh's accumulated-grievance pattern, not a Slynt-specific line -- the WEAKEST edge in the set, mint pending => fresh-verify to keep/adjust/drop. MOTIVATES Tier-2.",
     "pending-n4-verify"),
    ("jon-allows-free-folk-through-the-wall", "MOTIVATES", "bowen-marsh", 2, "adwd", "adwd-jon-13", 149,
     "Especially when it concerned the free folk, where their disapproval went bone deep.",
     "Jon opening the Wall to ~4,000 wildlings is the central provocation tipping Marsh and the conservative officers toward mutiny; their disapproval of the free-folk settlements 'went bone deep'. MOTIVATES Tier-2.",
     "pending-n4-verify"),
    ("pink-letter-delivered", "TRIGGERS", "jon-is-stabbed-repeatedly", 2, "adwd", "adwd-jon-13", 299,
     "Yarwyck and Marsh were slipping out, he saw, and all their men behind them.",
     "Jon's response to the Pink Letter -- announcing at the Shieldhall that he will march on Winterfell -- is the specific spark that makes the conspirators act. Marsh and Yarwyck slip out DURING the speech and ambush him minutes later. Specific spark (not a slow CAUSES) => TRIGGERS Tier-2.",
     "pending-n4-verify"),
    ("jon-snow", "AGENT_IN", "jon-allows-free-folk-through-the-wall", 1, "adwd", "adwd-jon-12", 61,
     "“Open the gate,” Jon Snow said softly.",
     "Jon Snow, as Lord Commander, gives the order opening the Wall to the free folk -- the decreeing actor. AGENT_IN Tier-1.",
     None),
    ("jon-snow", "AGENT_IN", "pink-letter-delivered", 1, "adwd", "adwd-jon-13", 227,
     "He cracked the seal, flattened the parchment, and read.",
     "Jon receives, reads, and acts on the Pink Letter -- the receiving/reading actor whose response (the Shieldhall march) is the event's consequence. Ramsay's agency belongs to the artifact authorship, not this delivery beat. AGENT_IN Tier-1.",
     None),
]

ARCS = [(RUN_N3, N3), (RUN_N4, N4)]


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

    # Drop the junk PRECEDES edge on the merged loser node.
    kept, dropped = [], 0
    for ln in lines:
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            kept.append(ln)
            continue
        if DROP_PREDICATE(r):
            dropped += 1
            continue
        kept.append(ln)

    new_rows = []
    for run_id, specs in ARCS:
        new_rows.extend(make_row(s, run_id) for s in specs)

    with open(EDGES, "w", encoding="utf-8") as f:
        for ln in kept:
            f.write(ln + "\n")
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    causal_types = ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES")
    n_causal = sum(1 for _, specs in ARCS for s in specs if s[1] in causal_types)
    n_role = len(new_rows) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"Dropped {dropped} junk PRECEDES edge (battle-on-the-green-fork -> mutiny-at-castle-black).")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal/agency + {n_role} role Tier-1).")
    print(f"  N3={len(N3)}  N4={len(N4)}")
    print(f"edges.jsonl now: {len(kept) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
