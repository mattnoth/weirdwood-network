#!/usr/bin/env python3
"""Mint Ned's Downfall enrichment pass 1 (S137) — fourth major-arc enrichment dip.

Board-picked target (S136, unanimous A/B/C): the conspiracy/betrayal SUBSTRATE of
Ned's downfall is minted-but-causally-unwired. The arrest->execution spine exists; the
gap is the hidden-architect layer (Cersei/Littlefinger/Varys/Pycelle), the revelation
engine (`ned-discovers...` was causally islanded), and the black-cells island
(`varys-confirms...` had 0 out-edges).

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+SUSPECTED_OF /
descriptive-object-depth / existing-node<->existing-node causal-wiring) over the built
cluster. PROPOSE-only lenses -> Opus orchestrator synthesized + LINE-CHECKED every cite
against the source files -> this mint set.

FINAL: mints 12 edges, 0 new nodes. (15 minted → independent fresh-verify 11 CONFIRM /
1 ADJUST-kept / 2 REJECT → 3 edges + the 1 new node backed out; see fresh-verify drops below.)

  CAUSAL / SUBSTRATE (2, verified=sonnet-fresh-verify-s137):
    - ned-discovers-the-truth-of-joffrey-s-parentage ENABLES arrest-of-eddard-stark
        (the revelation engine, was islanded; now a 2-cause convergence with Robert's death.
         fresh-verify flagged ENABLES→MOTIVATES; KEPT ENABLES — MOTIVATES-to-event is wrong
         shape, and `discovery MOTIVATES cersei-lannister` already carries the agency-routing.)
    - cersei-lannister SUSPECTED_OF death-of-robert-baratheon
        (the hidden origin of the whole arc; in-world + reader-known, never asserts murder)
  DECEIVES — hidden-architect manipulation (3, verified=sonnet-fresh-verify-s137):
    - petyr-baelish DECEIVES eddard-stark    ("I did warn you not to trust me")
    - varys DECEIVES eddard-stark            ("just as I allow Cersei to believe I am hers")
    - pycelle DECEIVES eddard-stark          (Pycelle relays Cersei's threats feigning help)
  ROLE / STRUCTURAL (7, Tier-1 facts, verified=None):
    - arya-stark / varys / cersei-lannister WITNESS_IN execution-of-eddard-stark
        (both Stark daughters now wired; Varys+Cersei present & trying to stop Joffrey)
    - high-septon OFFICIATES ned-confesses-to-treason
    - janos-slynt KILLS varly · sandor-clegane KILLS cayn · cayn VICTIM_IN gold-cloaks-betray-ned
        (the throne-room household-guard massacre)

First-use canonical types (in the 170-type locked vocab, first appearance in edges.jsonl):
OFFICIATES. NO invented types. (PREVENTS was on the backed-out Renly edge — not minted.)

DROPPED at independent fresh-verify (3 edges + 1 node):
  - varys-confirms-cersei-s-role ENABLES ned-confesses — MISTARGET: the node is the narrow
    WINE-REVEAL beat; the confession is driven by the Sansa threat, a different beat of the same
    scene. Black-cells island stays dark → pass-2 candidate (broader cell-visit / sansa-threat node).
  - eddard-stark PREVENTS renly-offers... + the new node + renly-baratheon AGENT_IN —
    SEMANTIC INVERSION: an offer that HAPPENED can't be "prevented"; Ned prevented the SEIZURE,
    not the offer, and the node had no other clean causal anchor (the counterfactual the schema
    can't model). Whole Renly addition backed out → pass-2 candidate.

DROPPED at synthesis (line-checked / dedup / agency):
  - gold-cloaks-betray-ned ENABLES cersei-orders-the-sleeping-guards-executed (lens4 L4-04)
    — MISTARGET: `cersei-orders-the-sleeping-guards-executed` is an AFFC Cersei I event, NOT
    the AGOT Tower-of-the-Hand guards. Wrong event, wrong book. (cf. the S135 tyrell-plot conflation.)
  - littlefinger-betrays-ned CAUSES arrest-of-eddard-stark (lens2 A4) — AGENCY-COLLAPSE: the
    betrayal is CONSTITUTIVE of the arrest (already SUB_BEAT_OF), not a cause of it. (S120 policy.)
  - ned-discovers... MOTIVATES cersei-lannister (lens4 L4-02) — DEDUP: already exists in graph.
  - lancel-lannister AGENT_IN death-of-robert-baratheon — DEFER: name+role split across
    non-adjacent lines (eddard-13:143 role / :149 name); no clean single-window evidence. The
    Cersei SUSPECTED_OF edge carries the substrate. -> pass-2/harvest.
  - varys SUSPECTED_OF death-of-robert-baratheon (lens2 B1) — OVERCLAIM: text shows Varys KNEW,
    not that he is a suspected agent of the poisoning.
  - ned-orders-slynt ENABLES gold-cloaks-betray-ned / ned-orders-slynt PREVENTS cersei-orders-arrest
    — sibling sub-beats of the same arrest; constitutive sequencing, not causal.
  - sansa-stark-held-hostage / renly-flees / sansa-warns-cersei / godswood-warning NEW NODES —
    DEFER (sustained-state / forward-dangling / scope) -> pass-2 candidates.
  - execution TRIGGERS war-of-the-five-kings — redundant w/ existing PART_OF + execution CAUSES
    robb-proclaimed-king; war-of-the-five-kings is a container, not a causal target.
  - valyrian-dagger WIELDED_IN littlefinger-betrays-ned — no `valyrian-dagger`/`catspaw` node -> harvest.

Safeguards mirror mint_red_wedding_enrichment_s134.py: backup, re-run guard, slug pre-check,
new-node create-if-absent.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-neds-downfall-enrichment-2026-06-23.jsonl"

RUN_ID = "neds-downfall-enrichment-s137"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"

NEW_NODE_SLUGS = set()  # Renly-offer node BACKED OUT at fresh-verify (see header)


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-nd-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


RENLY_OFFER_NODE = """\
---
name: "Renly offers Ned swords to seize Joffrey"
type: event.incident
slug: renly-offers-ned-swords-to-seize-joffrey
aliases: ["Renly's offer to Ned", "Renly offers a hundred swords", "Renly's plan to seize Joffrey"]
confidence: tier-1
era: robert's-reign
pass_origin: s137-nd-enrich
node_version: 1
evidence_chapters:
  - AGOT Eddard XIII
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

The night [Robert Baratheon](robert-baratheon) lay dying, [Renly Baratheon](renly-baratheon) drew [Eddard Stark](eddard-stark) aside and offered him a hundred swords — thirty of his own guard plus friends — to strike at once "while the castle sleeps," seize [Joffrey](joffrey-baratheon), [Myrcella](myrcella-baratheon) and [Tommen](tommen-baratheon) from [Cersei](cersei-lannister), and rule as Lord Protector: "the man who holds the king holds the kingdom." Ned refused — he would not threaten children, and Robert still lived — and Renly fled King's Landing before dawn. Ned later wonders in his cell whether refusing was his fatal mistake: had Cersei "elected to fight rather than flee, he might well have need of Renly's hundred swords, and more besides." The honor-choice that left Ned without force at the throne-room betrayal. An upstream beat of [Ned's downfall](arrest-of-eddard-stark).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S137 ND enrichment. [Renly Baratheon](renly-baratheon) AGENT_IN (Tier-1); [Eddard Stark](eddard-stark) PREVENTS this plan by refusing it (Tier-2, fresh-verify).)

## Quotes

> "We must get Joffrey away from his mother and take him in hand. Protector or no, the man who holds the king holds the kingdom. We should seize Myrcella and Tommen as well. Once we have her children, Cersei will not dare oppose us."

— Renly Baratheon, AGOT Eddard XIII (`sources/chapters/agot/agot-eddard-13.md:167`)
"""

NODES = []  # Renly-offer node BACKED OUT at fresh-verify (semantic-inversion REJECT, see header)


# (source, edge_type, target, tier, book, chap_id, line, quote, asserted, verified_or_None)
EDGES_SPEC = [
    # ════════ CAUSAL / SUBSTRATE (4) — verified=pending → fresh-verify ════════
    ("ned-discovers-the-truth-of-joffrey-s-parentage", "ENABLES",
     "arrest-of-eddard-stark", 2,
     "agot", "agot-eddard-12", 159,
     "When the king returns from his hunt, I intend to lay the truth before him. You must be gone by then.",
     "Ned's godswood warning is the revelation-engine precondition for Cersei's move against him: "
     "it forced her to strike before Robert returned. ENABLES (not TRIGGERS/CAUSES) — Robert's death "
     "supplies the proximate timing (existing CAUSES); the discovery is the motive-precondition Cersei "
     "chose to act on. Was islanded (only MOTIVATES edges); now joins the causal spine as a 2-cause "
     "convergence with death-of-robert.",
     "sonnet-fresh-verify-s137"),
    # [DROPPED at fresh-verify] varys-confirms-cersei-s-role ENABLES ned-confesses — MISTARGET:
    # the node is the narrow WINE-REVEAL beat; the confession is driven by the Sansa threat (a
    # different beat of the same scene). Black-cells island stays dark → pass-2 candidate (mint a
    # broader `varys-visits-ned-in-the-black-cells` or a sansa-threat node, then wire).
    ("cersei-lannister", "SUSPECTED_OF", "death-of-robert-baratheon", 2,
     "agot", "agot-eddard-15", 111,
     "Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage.",
     "Varys confirms in the black cells that Cersei supplied the strongwine that got Robert drunk before "
     "the boar — the hidden origin of the whole arc. SUSPECTED_OF: models the in-world + reader-known "
     "suspicion of engineered death; never asserts murder (node stays event.death). First Cersei-agency "
     "edge on Robert's death.",
     "sonnet-fresh-verify-s137"),
    # [DROPPED at fresh-verify] eddard PREVENTS renly-offers... + the new node + renly AGENT_IN —
    # SEMANTIC INVERSION: an offer that HAPPENED can't be "prevented"; Ned prevented the SEIZURE, not
    # the offer, and the offer-node has no other clean causal anchor (counterfactual the schema can't
    # model). Whole Renly addition backed out → pass-2 candidate (needs a `ned-refuses-renly-s-offer`
    # event node or a seizure-that-never-happened node before it wires cleanly).

    # ════════ DECEIVES — hidden-architect manipulation (3) — fresh-verify CONFIRMED ════════
    ("petyr-baelish", "DECEIVES", "eddard-stark", 1,
     "agot", "agot-eddard-14", 125,
     "His smile was apologetic. \"I did warn you not to trust me, you know.\"",
     "Littlefinger performed loyalty (offering to buy the Watch \"for the love I bear Catelyn\") while "
     "arranging its betrayal; the dagger-to-throat line is the deception's reveal. DECEIVES (actor→actor), "
     "the manipulation is on-page.",
     "sonnet-fresh-verify-s137"),
    ("varys", "DECEIVES", "eddard-stark", 2,
     "agot", "agot-eddard-15", 139,
     "Oh, I feed him choice whispers, sufficient so that he thinks I am his … just as I allow Cersei to "
     "believe I am hers.",
     "Varys confesses to playing every faction; his black-cells alliance with Ned is itself a performance "
     "(he steers Ned to the false confession). DECEIVES (actor→actor), Tier-2 (Ned's own rejoinder confirms "
     "he too was 'allowed to believe').",
     "sonnet-fresh-verify-s137"),
    ("pycelle", "DECEIVES", "eddard-stark", 2,
     "agot", "agot-eddard-12", 31,
     "Ned had little doubt that he was bound straight for the royal apartments, to whisper at the queen.",
     "Grand Maester Pycelle feigns helpfulness ('I thought you had best know') while serving Cersei — Ned "
     "sees through the performance. DECEIVES (actor→actor), Tier-2 (Ned's inference; Pycelle's loyalty to "
     "Cersei later confirmed).",
     "sonnet-fresh-verify-s137"),

    # ════════ ROLE / STRUCTURAL (7) — Tier-1 facts, verified=None ════════
    # [renly-baratheon AGENT_IN renly-offers... DROPPED with the backed-out Renly node, see above]
    ("arya-stark", "WITNESS_IN", "execution-of-eddard-stark", 1,
     "agot", "agot-arya-05", 163,
     "The crowd roared, and Arya felt the statue of Baelor rock as they surged against it.",
     "Arya is in the crowd at the Great Sept and watches her father's execution from the plinth of Baelor's "
     "statue (her POV chapter). Both Stark daughters now wired (sansa WITNESS_IN already exists).",
     None),
    ("varys", "WITNESS_IN", "execution-of-eddard-stark", 1,
     "agot", "agot-arya-05", 163,
     "Varys came rushing over waving his arms, and even the queen was saying something to him, but "
     "Joffrey shook his head.",
     "Varys is present and tries (ineffectually) to stop Joffrey ordering the beheading.",
     None),
    ("cersei-lannister", "WITNESS_IN", "execution-of-eddard-stark", 1,
     "agot", "agot-arya-05", 163,
     "and even the queen was saying something to him, but Joffrey shook his head.",
     "Cersei is present and attempts to dissuade Joffrey from the execution (she wanted a 'tame wolf', not "
     "a corpse — Joffrey overrode her).",
     None),
    ("high-septon", "OFFICIATES", "ned-confesses-to-treason", 1,
     "agot", "agot-arya-05", 159,
     "This man has confessed his crimes in the sight of gods and men, here in this holy place.",
     "The (AGOT-era) High Septon runs the confession ceremony on the pulpit of the Great Sept and asks "
     "Joffrey for judgment. OFFICIATES (first-use canonical type).",
     None),
    ("janos-slynt", "KILLS", "varly", 1,
     "agot", "agot-eddard-14", 123,
     "Janos Slynt himself slashed open Varly's throat.",
     "Janos Slynt personally kills Ned's guardsman Varly in the throne-room massacre.",
     None),
    ("sandor-clegane", "KILLS", "cayn", 1,
     "agot", "agot-eddard-14", 123,
     "Then the Hound was on him. Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his "
     "second drove him to his knees and opened him from shoulder to breastbone.",
     "Sandor Clegane kills Ned's guardsman Cayn in the throne-room massacre.",
     None),
    ("cayn", "VICTIM_IN", "gold-cloaks-betray-ned", 1,
     "agot", "agot-eddard-14", 123,
     "Then the Hound was on him. Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his "
     "second drove him to his knees and opened him from shoulder to breastbone.",
     "Cayn (Ned's household guard) is killed in the gold-cloak betrayal; baseline wired tomard/varly "
     "VICTIM_IN but not cayn.",
     None),
]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified) = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **common(),
        "evidence_book": book,
        "evidence_chapter": chap_id,
        "evidence_ref": f"sources/chapters/{book}/{chap_id}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for (src, _, tgt, *_rest) in EDGES_SPEC:
        all_slugs.add(src)
        all_slugs.add(tgt)
    check_slugs = all_slugs - NEW_NODE_SLUGS
    resolved, missing = precheck_slugs(check_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent targets: {missing}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw_lines = EDGES.read_text(encoding="utf-8").splitlines()
    existing_lines = [ln for ln in raw_lines if ln.strip()]
    if any(RUN_ID in ln for ln in existing_lines):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written → {BACKUP}")

    nodes_created = []
    for slug, body in NODES:
        node_path = NODES_EVENTS / f"{slug}.node.md"
        if node_path.exists():
            print(f"  SKIP node (already exists): {node_path.name}")
        else:
            node_path.write_text(body, encoding="utf-8")
            nodes_created.append(slug)
            print(f"  Created node: {node_path.name}")

    new_rows = [make_edge_row(spec) for spec in EDGES_SPEC]
    lines_before = len(existing_lines)
    all_out = existing_lines + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(all_out) + "\n", encoding="utf-8")
    lines_after = len(all_out)

    type_counts = {}
    for spec in EDGES_SPEC:
        type_counts[spec[1]] = type_counts.get(spec[1], 0) + 1

    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(nodes_created)}): {', '.join(nodes_created) or '(none)'}")
    print(f"Edges appended ({len(new_rows)}):")
    for etype, cnt in sorted(type_counts.items()):
        print(f"  {etype}: {cnt}")
    print(f"edges.jsonl: {lines_before} → {lines_after} lines (+{len(new_rows)})")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
