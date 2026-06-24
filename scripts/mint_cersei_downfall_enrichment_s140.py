#!/usr/bin/env python3
"""Mint Cersei's-downfall enrichment pass 1 (S140) — seventh major-arc enrichment dip.

Fork-1 board pick (Matt S140): the AFFC Cersei's-downfall event-arc. The S114 causal
SPINE (assassination-of-tywin -> cersei-rearms-the-faith -> cersei-is-captured-in-the-sept
-> cersei-is-stripped-and-imprisoned; the Margaery-plot branch -> blue-bard-arrest +
osney-confesses -> capture) was already built. This pass ENRICHES the off-spine substrate
the spine lacked: the HIDDEN MOTIVATES ENGINE (Maggy the Frog's valonqar/younger-queen
prophecy that drives the whole arc), the murder-of-the-old-High-Septon backstory crime
(the Kettleblack assassination that enabled the High Sparrow's rise), the de-islanding of
cersei-fills-in-the-arrest-warrants, the dead-end downstream fix (Cersei resolves on trial
by combat + the Robert-Strong/Qyburn champion counsel), and the secondary-character
substrate (Qyburn's torture of the Blue Bard, Taena's intelligence + co-conspiracy, Lancel
joining the Warrior's Sons).

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+SUSPECTED+WITNESS /
descriptive-object-depth / existing-node<->existing-node causal-wiring) over the built
cluster. PROPOSE-only lenses -> Opus orchestrator synthesized + LINE-CHECKED every cite
against the AFFC source files -> this mint set.

THE LINE-CHECK / ADJUDICATION CATCHES (orchestrator, vs the lenses):
  - Murder-of-old-High-Septon agency: lenses 2/3 proposed `cersei SUSPECTED_OF murder`.
    OVERRIDDEN -> `cersei COMMANDS_IN murder` (T2): affc-cersei-10.md:247 is CERSEI'S OWN
    POV ("I'll rid myself of this High Septon just as I did the other") — her culpability is
    authorially POV-confirmed, NOT in-world-contested. SUSPECTED_OF would understate it.
  - `cersei LOVER_OF osney` (lens 2) DROPPED — already in graph (pass1-derived, ADWD).
  - `orton AGENT_IN blue-bard-arrest` (lens 2) DROPPED — already in graph (plate3).
  - `cersei FEARS tyrion` (lens 4) DROPPED — already in graph (pass1-derived, ACOK).
  - Lancel: graph has wiki `SWORN_TO warriors-sons`; minting book-grounded `MEMBER_OF`
    (the order-membership, upgrades the wiki allegiance with an AFFC cite).
  - Warrants de-island: chose `blue-bard-arrest ENABLES warrants` (textually airtight —
    the bard's coerced names at ch09:199 literally fill the warrants at ch10:77) over the
    lenses' ambiguous CAUSES-from-plot / SUB_BEAT_OF split.

DEFERRED at synthesis (pass-2 / Robert-Strong character unit):
  - creation-of-robert-strong node (off-page across ch2/ch7 — over-read risk; Qyburn ADVISES
    captures the champion thread now). - cersei-s-walk-of-atonement (ADWD anchor, no AFFC
    quote — true source-deferral). - cersei-sends-osney-to-seduce-margaery (constitutive of
    the plot; granular). - lancel BETRAYS cersei (AFFC shows only Cersei's FEAR; the
    confession that damns her is ADWD).

FINAL: 3 new nodes + 15 edges. (verified=pending-fresh-verify on the 5 interpretive
motive/causal edges; Tier-1 role/structural edges verified=None.)

NEW NODES (3):
  - maggy-the-frogs-prophecy          (concept.prophecy) — the hidden MOTIVATES engine
  - murder-of-the-old-high-septon     (event.incident)   — Kettleblack backstory crime
  - cersei-resolves-on-trial-by-combat(event.incident)   — dead-end downstream fix (-> ADWD)

Safeguards mirror mint_tywin_death_enrichment_s139.py: backup, re-run guard, slug pre-check
(NEW_NODE_SLUGS excluded), new-node create-if-absent, optional qualifier.
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
NODES_PROPHECIES = REPO / "graph" / "nodes" / "prophecies"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-cersei-downfall-enrichment-2026-06-23.jsonl"

RUN_ID = "cersei-downfall-enrichment-s140"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "maggy-the-frogs-prophecy",
    "murder-of-the-old-high-septon",
    "cersei-resolves-on-trial-by-combat",
}


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-cersei-downfall-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

MAGGY_PROPHECY = """\
---
name: "Maggy the Frog's prophecy"
type: concept.prophecy
slug: maggy-the-frogs-prophecy
aliases: ["Maggy's prophecy", "the valonqar prophecy", "the younger and more beautiful queen", "Maggy the Frog's foretelling", "Cersei's prophecy"]
confidence: tier-1
era: current-narrative
pass_origin: s140-cersei-downfall-enrich
node_version: 1
evidence_chapters:
  - AFFC Cersei V
  - AFFC Cersei VIII
---

## Identity

The blood-magic foretelling the maegi [Maggy the Frog](maggy-the-frog) gave a ten-year-old [Cersei Lannister](cersei-lannister) in a tent at Lannisport, after sucking the blood from her finger. In answer to Cersei's three questions Maggy foretold: that Cersei would wed not the prince (Rhaegar) but the king; that she would be queen — "until there comes another, younger and more beautiful, to cast you down and take all that you hold dear"; that the king would have twenty children and she but three; that "gold shall be their crowns and gold their shrouds"; and that "when your tears have drowned you, the **valonqar** shall wrap his hands about your pale white throat and choke the life from you" (*valonqar* = High Valyrian "little brother").

The prophecy is the **hidden engine of Cersei's entire AFFC downfall**: her terror of the "younger and more beautiful queen" drives her to destroy [Margaery Tyrell](margaery-tyrell) — the campaign that backfires into her own arrest. She reads the *valonqar* as [Tyrion](tyrion-lannister). Theory READINGS of the prophecy's fulfillment (who the valonqar is, whether it can be subverted) stay GATED; this node is the Tier-1/2 evidence substrate.

## Edges

(Edges live in `graph/edges/edges.jsonl`, S140 Cersei-downfall enrichment. PROPHESIED_BY [Maggy the Frog](maggy-the-frog); MOTIVATES [Cersei](cersei-lannister); [Cersei](cersei-lannister) SUBJECT_OF_PROPHECY; FORESHADOWS [Cersei's capture](cersei-is-captured-in-the-sept).)

## Quotes

> "Aye." Malice gleamed in Maggy's yellow eyes. "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear."

— Maggy the Frog, in Cersei's recollection, AFFC Cersei VIII (`sources/chapters/affc/affc-cersei-08.md:243`)

> The old woman was not done with her, however. "Gold shall be their crowns and gold their shrouds," she said. "And when your tears have drowned you, the valonqar shall wrap his hands about your pale white throat and choke the life from you."

— AFFC Cersei VIII (`sources/chapters/affc/affc-cersei-08.md:251`)

> "Tyrion is the valonqar," she said. "Do you use that word in Myr? It's High Valyrian, it means little brother."

— Cersei Lannister, AFFC Cersei IX (`sources/chapters/affc/affc-cersei-09.md:267`)
"""

MURDER_HIGH_SEPTON = """\
---
slug: murder-of-the-old-high-septon
type: event.incident
name: "Murder of the old High Septon"
aliases: ["death of the old High Septon", "Osney smothers the High Septon", "the High Septon killed in his sleep", "Cersei has the old High Septon murdered"]
confidence: tier-2
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s140-cersei-downfall-enrich
node_version: 1
evidence_chapters:
  - AFFC Cersei X
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-confessed
---

# Murder of the old High Septon

The backstory crime that, once revealed, breaks [Cersei](cersei-lannister). [Osney Kettleblack](osney-kettleblack), on Cersei's order, smothered the previous (fat, Tywin-installed) High Septon in his sleep with a pillow — clearing the way for the militant **High Sparrow** to be elected. The deed is off-page; it surfaces when Osney, broken by the High Sparrow, confesses it before the altar. Cersei's own POV confirms her culpability ("I'll rid myself of this High Septon just as I did the other"), turning her charges from mere adultery-procuring to murder and treason — which is why the Faith holds her for trial rather than questioning.

## Edges
(Edges in `graph/edges/edges.jsonl`, S140 Cersei-downfall enrichment. [Osney Kettleblack](osney-kettleblack) AGENT_IN; [Cersei](cersei-lannister) COMMANDS_IN; ENABLES [Cersei rearms the Faith](cersei-rearms-the-faith-and-forgives-the-debt).)

## Quotes

> "That one there. She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."

— Osney Kettleblack's confession, AFFC Cersei X (`sources/chapters/affc/affc-cersei-10.md:243`)

> The Kettleblacks, I need the Kettleblacks, I will send in Osfryd with the gold cloaks and Osmund with the Kingsguard, Osney will deny it all once they cut him free, and I'll rid myself of this High Septon just as I did the other.

— Cersei Lannister's POV, AFFC Cersei X (`sources/chapters/affc/affc-cersei-10.md:247`)
"""

CERSEI_TRIAL_RESOLVE = """\
---
slug: cersei-resolves-on-trial-by-combat
type: event.incident
name: "Cersei resolves on trial by combat"
aliases: ["Cersei resolves on trial by battle", "Cersei sends for Jaime", "Cersei's plea to Jaime", "trial by battle"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s140-cersei-downfall-enrich
node_version: 1
evidence_chapters:
  - AFFC Cersei X
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
---

# Cersei resolves on trial by combat

Imprisoned and stripped in a cell of the Great Sept, unable to trust a court of sparrows or to count on [Ser Kevan](kevan-lannister) after their last bitter words, Cersei resolves that "it will have to be a trial by battle" and begs [Qyburn](qyburn) to send a desperate raven to Riverrun summoning her brother [Jaime](jaime-lannister) — "Come at once. Help me. Save me." (Jaime will burn the letter unread; her true champion will be Qyburn's secret creation, [Robert Strong](robert-strong).) The closing beat of AFFC Cersei X and the hinge into her ADWD trial arc — the downstream the imprisonment beat previously lacked.

## Edges
(Edges in `graph/edges/edges.jsonl`, S140 Cersei-downfall enrichment. CAUSED by [Cersei is stripped and imprisoned](cersei-is-stripped-and-imprisoned); [Cersei](cersei-lannister) AGENT_IN; [Qyburn](qyburn) ADVISES her toward the champion.)

## Quotes

> Even in her exhausted, frightened state, the queen knew she dare not trust her fate to a court of sparrows. Nor could she count on Ser Kevan to intervene, after the words that had passed between them at their last meeting. It will have to be a trial by battle. There is no other way.

— Cersei Lannister's POV, AFFC Cersei X (`sources/chapters/affc/affc-cersei-10.md:313`)

> She licked her lips, shivering. "Come at once. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once."

— Cersei's message to Jaime, AFFC Cersei X (`sources/chapters/affc/affc-cersei-10.md:317`)
"""

NODES = [
    ("maggy-the-frogs-prophecy", NODES_PROPHECIES, MAGGY_PROPHECY),
    ("murder-of-the-old-high-septon", NODES_EVENTS, MURDER_HIGH_SEPTON),
    ("cersei-resolves-on-trial-by-combat", NODES_EVENTS, CERSEI_TRIAL_RESOLVE),
]

# ════════════════════════════ EDGES ════════════════════════════
# (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified, qualifier)

EDGES_SPEC = [
    # ════ PROPHECY — the hidden MOTIVATES engine (4) ════
    ("maggy-the-frogs-prophecy", "PROPHESIED_BY", "maggy-the-frog", 1,
     "affc", "affc-cersei-08", 243,
     "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear.",
     "Maggy the Frog is the source of the foretelling, given to young Cersei via blood-magic ritual at Lannisport. PROPHESIED_BY = prophecy -> prophet.", None, None),
    ("maggy-the-frogs-prophecy", "MOTIVATES", "cersei-lannister", 1,
     "affc", "affc-cersei-08", 243,
     "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear.",
     "The prophecy of a younger, more beautiful queen is the psychological engine driving Cersei's campaign to destroy Margaery (the perceived 'younger queen'). MOTIVATES = prophecy -> character (the rule: motive moves a person).",
     "pending-fresh-verify-s140", None),
    ("cersei-lannister", "SUBJECT_OF_PROPHECY", "maggy-the-frogs-prophecy", 1,
     "affc", "affc-cersei-08", 243,
     "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear.",
     "Cersei is the named subject of all of Maggy's clauses (queenship, the three gold-shrouded children, the valonqar). SUBJECT_OF_PROPHECY = subject -> prophecy.", None, None),
    ("maggy-the-frogs-prophecy", "FORESHADOWS", "cersei-is-captured-in-the-sept", 2,
     "affc", "affc-cersei-08", 243,
     "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear.",
     "The 'cast you down' clause anticipates Cersei's downfall; her plot against the younger queen backfires into her own capture by the Faith. FORESHADOWS = earlier prophecy -> later event. FLAG: the proximate cast-down agent is the Faith/Osney, not Margaery directly.",
     "pending-fresh-verify-s140", None),

    # ════ MURDER of the old High Septon — the Kettleblack backstory crime (3) ════
    ("osney-kettleblack", "AGENT_IN", "murder-of-the-old-high-septon", 1,
     "affc", "affc-cersei-10", 243,
     "I just come in when he was sleeping and pushed a pillow down across his face.",
     "Osney confesses on-page to physically smothering the old High Septon. AGENT_IN = physical actor.", None, None),
    ("cersei-lannister", "COMMANDS_IN", "murder-of-the-old-high-septon", 2,
     "affc", "affc-cersei-10", 247,
     "Osney will deny it all once they cut him free, and I'll rid myself of this High Septon just as I did the other.",
     "Cersei ordered the killing (sent Osney) — her OWN POV confirms culpability ('as I did the other'), so this is authorially confirmed, not in-world-contested: COMMANDS_IN (orderer), NOT SUSPECTED_OF. Tier 2 only because the deed itself is off-page.",
     "pending-fresh-verify-s140", None),
    ("murder-of-the-old-high-septon", "ENABLES", "cersei-rearms-the-faith-and-forgives-the-debt", 2,
     "affc", "affc-cersei-10", 247,
     "I'll rid myself of this High Septon just as I did the other.",
     "Removing the old High Septon vacated the seat the militant High Sparrow then filled; his leverage is the precondition for the rearming bargain. ENABLES = distal door-opener. FLAG: distal (mediated by the off-node High-Sparrow election).",
     "pending-fresh-verify-s140", None),

    # ════ DE-ISLAND the arrest-warrants node (1) ════
    ("cersei-confronts-and-arrests-the-blue-bard", "ENABLES", "cersei-fills-in-the-arrest-warrants", 1,
     "affc", "affc-cersei-10", 77,
     "Cersei had written in the names herself: Ser Tallad the Tall, Jalabhar Xho, Hamish the Harper, Hugh Clifton, Mark Mullendore, Bayard Norcross, Lambert Turnberry, Horas Redwyne, Hobber Redwyne, and a certain churl named Wat, who called himself the Blue Bard.",
     "The Blue Bard, tortured into naming Margaery's alleged lovers (ch09:199 — Tallad, Turnberry, Jalabhar Xho, the Redwyne twins, Clifton), supplied the very names Cersei writes into the warrants. The bard's coerced testimony is the precondition for the warrant list. ENABLES de-islands the formerly causally-orphaned warrants node.", None, None),

    # ════ DEAD-END DOWNSTREAM FIX — Cersei resolves on trial by combat (3) ════
    ("cersei-is-stripped-and-imprisoned", "CAUSES", "cersei-resolves-on-trial-by-combat", 1,
     "affc", "affc-cersei-10", 313,
     "It will have to be a trial by battle. There is no other way.",
     "Imprisoned and unable to trust the sparrow court or Kevan, Cersei resolves on trial by battle and dispatches her plea to Jaime. CAUSES = distinct downstream resolution; fixes the spine's dead-end (the imprisonment beat had 0 downstream).", None, None),
    ("cersei-lannister", "AGENT_IN", "cersei-resolves-on-trial-by-combat", 1,
     "affc", "affc-cersei-10", 313,
     "Qyburn, for the love you bear me, I beg you, send a message for me. A raven if you can. A rider, if not. You must send to Riverrun, to my brother.",
     "Cersei is the sole agent resolving on the trial and dispatching the raven to Jaime. AGENT_IN.", None, None),
    ("qyburn", "ADVISES", "cersei-lannister", 1,
     "affc", "affc-cersei-10", 307,
     "Hope remains. Your Grace has the right to prove your innocence by battle. My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him.",
     "Qyburn counsels Cersei toward trial by battle, holding out his secret champion (Robert Strong). ADVISES = person -> person (actively shaping her decision, not merely informing).", None, None),

    # ════ SECONDARY-CHARACTER SUBSTRATE (4) ════
    ("qyburn", "TORTURES", "blue-bard", 1,
     "affc", "affc-cersei-09", 191,
     "Lord Qyburn ran a hand up the Blue Bard's chest. “Does she take your nipples in her mouth during your love play?” He took one between his thumb and forefinger, and twisted.",
     "Qyburn personally tortures the Blue Bard (Wat) through the night to extract the false confession of Margaery's adultery. TORTURES = torturer -> victim.", None, None),
    ("taena-merryweather", "INFORMS", "cersei-lannister", 1,
     "affc", "affc-cersei-03", 173,
     "There is something you must know. Your maid is bought and paid for. She tells Lady Margaery everything you do.",
     "Taena warns Cersei that her maid spies for Margaery — the intelligence that opens Cersei's counter-conspiracy. INFORMS = informer -> recipient.", None, None),
    ("taena-merryweather", "CONSPIRES_WITH", "cersei-lannister", 1,
     "affc", "affc-cersei-09", 251,
     "So she seems, but there is more of sly than shy in her. Leave her to me, my sweet.",
     "Taena actively co-designs the frame against Margaery, taking the Alla Tyrell angle. CONSPIRES_WITH = co-conspirator (symmetric).",
     "pending-fresh-verify-s140", None),
    ("lancel-lannister", "MEMBER_OF", "warriors-sons", 1,
     "affc", "affc-cersei-08", 147,
     "her mooncalf cousin had forsaken castle, lands, and wife and wandered back to the city to join the Noble and Puissant Order of the Warrior's Sons",
     "Lancel renounces his castle, lands, and wife to join the Warrior's Sons of the reborn Faith Militant — book-grounded membership that upgrades the wiki SWORN_TO allegiance with an AFFC cite. MEMBER_OF = person -> order.", None, None),
]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified, qualifier) = spec
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
    if qualifier is not None:
        row["qualifier"] = qualifier
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for spec in EDGES_SPEC:
        all_slugs.add(spec[0])
        all_slugs.add(spec[2])
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
    for slug, node_dir, body in NODES:
        node_path = node_dir / f"{slug}.node.md"
        if node_path.exists():
            print(f"  SKIP node (already exists): {node_path.name}")
        else:
            node_path.write_text(body, encoding="utf-8")
            nodes_created.append(slug)
            print(f"  Created node: {node_path.relative_to(REPO)}")

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
