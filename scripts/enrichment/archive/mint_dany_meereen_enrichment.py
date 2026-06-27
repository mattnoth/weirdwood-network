#!/usr/bin/env python3
"""Mint Daenerys / Meereen enrichment pass 1 (S144) — the L1 round REOPENS.

Tenth major-arc enrichment dip; first of the spine-only heavyweight arcs (Matt S143,
"9 isn't enough" — the prior 9 dips clustered in KL/Riverlands/backstory; Essos/North/
Aegon/Bran were spine-built with 0 enrichment). The Essos spine E1–E5 was already wired
(fall-of-astapor → ... → dany-lost-on-dothraki-sea); `siege-of-meereen` had 4 edges and the
whole Slaver's-Bay political/whodunit layer was absent. This pass builds that texture:

  - THE INSURGENCY HUB: new `sons-of-the-harpy-insurgency` (flagged-but-unminted since the
    S121 essos-e2 track). The night-killings (`sons-of-the-harpy-kill-twenty-nine`) become a
    SUB_BEAT_OF it; the Brazen Beasts + Skahaz OPPOSE it; it MOTIVATES Dany's marriage and
    ENABLES the wedding bargain (the 90-day-peace condition).
  - THE HIZDAHR-AS-THE-HARPY WHODUNIT (our wheelhouse, unproven-agency SUSPECTED_OF, never
    asserts): Hizdahr SUSPECTED_OF the insurgency + the twenty-nine-night + the poisoned
    locusts. The stale tier-3 `hizdahr COMMANDS_IN sons-of-the-harpy-kill-twenty-nine` (which
    asserted proven command authority) is RETIRED in favor of the SUSPECTED_OF model.
  - THE POISONED LOCUSTS: the islanded `poisoned-locusts` (0 edges) wired — WIELDED_IN the
    Daznak pit event; Belwas VICTIM_IN; Dany the intended VICTIM_IN; the Sons-of-the-Harpy
    catspaw chain SUSPECTED_OF. (Quentyn-as-suspect REJECTED at fresh-verify — the passage
    suspects Hizdahr as the intended *victim*, doesn't implicate Quentyn.)
  - THE KINGBREAKER COUP: new `barristan-arrests-hizdahr` (the hour-of-the-wolf seizure).
  - PARTICIPANT ROLES on the thin siege/pit hubs: Barristan ADVISES/COMMANDS_IN; Grey Worm /
    the Unsullied; Daario+Groleo PRISONER_OF Yunkai (Groleo KILLED_BY Yunkai); the Green Grace
    + Reznak ADVISE; Marghaz COMMANDS the Brazen Beasts.
  - THE QUENTYN BRIDGE: new `quentyn-contracts-tattered-prince` (the Pentos bargain) ENABLES
    `quentyn-orders-the-attack`; the Dornish pact MOTIVATES it; Dany's flight ENABLES it.
  - THE THIRD TREASON: new `ben-plumm-defects-to-yunkai` (the Second Sons go over for gold).
  - CROSS-CONTAINER SEAMS (lens 4): `dragon-hatching-on-drogo-pyre` ENABLES `fall-of-astapor`
    (the AGOT→Essos root the conquest arc lacked); `dany-mounts-drogon-and-flees-meereen`
    TRIGGERS `second-siege-of-meereen` (orphan node lit; CAUSES→TRIGGERS per fresh-verify,
    co-causes Yurkhaz's death + the Volantene fleet).
  - DESCRIPTIVE: new `bronze-harpy-of-meereen` object; Quaithe FORESHADOWS edges; tokar
    SACRED_TO ghiscari.

Machine: 4 fresh Sonnet lenses (secondary-char / insurgency-whodunit / descriptive-depth /
causal-wiring) PROPOSE-only → Opus orchestrator synthesis → deterministic line-check of every
quote (working/enrichment/dany-meereen/verify_lines.py, 48/48 PASS) → independent Sonnet
fresh-verify of the interpretive edges (8C/7A/1R; verdicts applied) → this mint set.

FRESH-VERIFY ADJUDICATIONS APPLIED:
  - REJECT B14 (quentyn SUSPECTED_OF poisoned-locusts): dropped.
  - D1 doran-pact MOTIVATES quentyn-attack: tier 1→2 (one inferential step).
  - D5 dany-flees → second-siege: CAUSES→TRIGGERS (necessary-not-sufficient; co-causes named).
  - C_qf1 quaithe FORESHADOWS dany-flees: tier 2→3 (interpretive mapping).
  - B10: retire the existing tier-3 COMMANDS_IN edge (asserts proven agency) — DONE below.
  - B7 MOTIVATES daenerys-targaryen KEPT (skeptic flagged person-target as malformed, but it's
    established graph convention — sibling `kill-twenty-nine MOTIVATES daenerys-targaryen`
    already exists; documented orchestrator override).

5 new nodes + 46 edges − 1 retired stale edge.
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
NODES_ARTIFACTS = REPO / "graph" / "nodes" / "artifacts"
CANDIDATES = REPO / "working" / "enrichment" / "dany-meereen" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-dany-meereen-enrichment-2026-06-24.jsonl"

RUN_ID = "dany-meereen-enrichment-s144"
PRODUCED_AT = "2026-06-24T00:00:00+00:00"

# The stale tier-3 edge to retire (asserts proven Harpy-command; superseded by B10 SUSPECTED_OF).
RETIRE = ("hizdahr-zo-loraq", "COMMANDS_IN", "sons-of-the-harpy-kill-twenty-nine")

NEW_NODE_SLUGS = {
    "sons-of-the-harpy-insurgency",
    "barristan-arrests-hizdahr",
    "quentyn-contracts-tattered-prince",
    "ben-plumm-defects-to-yunkai",
    "bronze-harpy-of-meereen",
}

# Fresh-verified interpretive edges → stamp verified_by; structural/role edges left unstamped
# (Tier-1 line-verified, mirrors prior dips). B14 already dropped from candidates.
VERIFIED = {
    "B7": "fresh-verify-confirmed-s144", "B8": "fresh-verify-confirmed-s144",
    "B9": "fresh-verify-confirmed-s144", "B10": "fresh-verify-confirmed-s144",
    "B11": "fresh-verify-confirmed-s144", "B12": "fresh-verify-confirmed-s144",
    "B13": "fresh-verify-confirmed-s144", "B16": "fresh-verify-confirmed-s144",
    "D1": "fresh-verify-adjusted-s144-tier", "D2": "fresh-verify-confirmed-s144",
    "D4": "fresh-verify-confirmed-s144", "D5": "fresh-verify-adjusted-s144-triggers",
    "C_qf1": "fresh-verify-adjusted-s144-tier", "C_qf2": "fresh-verify-confirmed-s144",
    "A_grkb": "fresh-verify-confirmed-s144",
}

# Per-edge asserted_relation. Falls back to a generic role note if absent.
ASSERTED = {
    "B1": "The Sons of the Harpy are the perpetrators of the masked night-killing campaign. AGENT_IN = faction -> campaign-hub.",
    "B2": "The twenty-nine-night is the climactic escalation within the longer shadow war, not the war itself. SUB_BEAT_OF.",
    "B3": "The Brazen Beasts are raised expressly as the counter-force to the Harpy insurgency. OPPOSES.",
    "B4": "Skahaz is the queen's spear against the Harpy — interrogates the captured, drives the counter-insurgency. OPPOSES.",
    "B7": "The ongoing slaughter is what drives Dany to accept the Ghiscari marriage ('owed it to her dead'). MOTIVATES = event-arc -> character (graph convention; sibling kill-twenty-nine MOTIVATES dany exists).",
    "B8": "The insurgency's 90-day-peace condition is the structural bargain that produces the marriage. ENABLES.",
    "B9": "Barristan's case: the killings stopped when Hizdahr commanded peace and resumed after — the central in-world suspicion he is the Harpy. SUSPECTED_OF (unproven, never asserts).",
    "B10": "Same Barristan confrontation, pointed at the specific twenty-nine-night. SUSPECTED_OF replaces the retired tier-3 COMMANDS_IN, which over-asserted proven agency.",
    "B11": "The poisoned honeyed locusts are deployed in the royal box at the Daznak pit event. WIELDED_IN = object -> event (the instrument).",
    "B12": "Hizdahr stocked the box and urged Dany to eat the locusts but tasted none himself — Barristan's smoking-gun circumstantial case. SUSPECTED_OF.",
    "B13": "Skahaz's informant: the confectioner was a catspaw whose daughter the Sons of the Harpy held hostage 'once the queen was dead' — the Sons as organizational sponsor. SUSPECTED_OF tier-3 (two layers of reported speech).",
    "B15": "Strong Belwas eats the whole bowl of locusts and collapses retching blood at the pit. VICTIM_IN = the confirmed casualty of the poisoning.",
    "B16": "Dany was the intended target; spared only because she chose figs and dates. VICTIM_IN (intended).",
    "B17": "The Reznak/Skahaz counsel session is a direct response to the killings — a beat within the shadow war. SUB_BEAT_OF.",
    "A_baco": "Barristan leads the hour-of-the-wolf seizure of Hizdahr in person ('I am here for Hizdahr'). COMMANDS_IN.",
    "A_skco": "Skahaz the Shavepate co-plans and executes the coup (the watchword is 'Groleo'). AGENT_IN.",
    "A_bbco": "Six Brazen Beasts move with Skahaz to disarm Hizdahr's guard. PARTICIPATES_IN.",
    "A_badv": "Barristan counsels Dany on the Yunkai siege ('I do not think we should allow them to invest us'). ADVISES.",
    "A_bmo": "Barristan mourns the murdered hostage Admiral Groleo ('a good man... did not deserve this end'). MOURNS.",
    "A_dapo": "Daario is held hostage in the Yunkish camp under the peace exchange. PRISONER_OF.",
    "A_grpo": "Admiral Groleo is held hostage in the Yunkish camp under the peace exchange. PRISONER_OF.",
    "A_grkb": "Bloodbeard (Yunkai'i) beheads the hostage Groleo and flings his head at the seneschal. KILLED_BY = victim -> killer-organization (proximate hand: Bloodbeard).",
    "A_bpco": "Brown Ben leads the Second Sons over to the Yunkai'i ('we went over to the winning side'). COMMANDS_IN the defection.",
    "A_ssag": "The Second Sons as a company defect with him ('I put it to my men'). AGENT_IN.",
    "A_rzadv": "Reznak presses Dany to take Hizdahr for king at once to make peace. ADVISES.",
    "A_gladv": "The Green Grace counsels Dany to pray and heed the Ghiscari signs (the marriage path). ADVISES.",
    "A_mgco": "Marghaz zo Loraq, Hizdahr's cousin, is the new commander of the Brazen Beasts. COMMANDS.",
    "A_hzap": "Hizdahr gives command of the Brazen Beasts to his cousin Marghaz (displacing Skahaz). APPOINTS.",
    "A_bpro": "Barristan quietly warns Quentyn to flee the city after Hizdahr marks him. PROTECTS.",
    "A_qneg": "Quentyn approaches the Tattered Prince to bargain for help stealing a dragon. NEGOTIATES_WITH.",
    "A_qcon": "The deal is struck — the Windblown's price is Pentos. CONTRACTED_WITH.",
    "A_qag": "Quentyn is the initiating party of the bargain. AGENT_IN.",
    "A_tpag": "The Tattered Prince sets the terms (Pentos). AGENT_IN.",
    "A_qen": "The Tattered Prince's bundle (disguises + the watchword 'dog') is what equips Quentyn's dragon-theft attempt. ENABLES.",
    "A_gwco": "Grey Worm commands the Unsullied, who will obey whatever is asked. COMMANDS.",
    "A_unco": "The Unsullied man the walls and towers during the siege. PARTICIPATES_IN.",
    "D1": "Quentyn acts on his father's covert pact ('For Dorne. For my father') — the obligation that compels the dragon-theft. MOTIVATES tier-2 (one inferential step from reveal to act, per fresh-verify).",
    "D2": "Dany's flight on Drogon leaves Rhaegal and Viserion unguarded and forecloses the marriage — the window Quentyn steps into ('your bride flew off on a dragon'). ENABLES.",
    "D4": "Without the hatched dragons Dany has no leverage in Astapor; the dragons are the wonder that funds the Unsullied purchase that takes the city. ENABLES = AGOT->Essos root seam (the conquest arc otherwise begins unrooted).",
    "D5": "Dany's flight removes the deterrent (queen + dragon) and the pit panic kills the old Yunkish negotiator Yurkhaz — emboldening the jackals to renew the siege. TRIGGERS (necessary-not-sufficient; co-causes named in-passage) per fresh-verify.",
    "C_drag": "Drogon descends into the Daznak pit, the event's defining actor. AGENT_IN.",
    "C_drloc": "The event occurs at Daznak's Pit (the Gates of Fate). LOCATED_AT = event -> place.",
    "C_bhloc": "The bronze harpy stands atop the Great Pyramid, eight hundred feet up. LOCATED_AT.",
    "C_bhdep": "The bronze harpy is the visible signature of Meereen as Dany's host approaches in the conquest. DEPICTED_IN.",
    "C_tksac": "The tokar is the Ghiscari master's garment Dany must don to be accepted as Meereen's queen. SACRED_TO ghiscari (cultural).",
    "C_qf1": "Quaithe's glass-candles warning ('the pale mare, and after her the others') points toward Dany's eventual flight/scattering. FORESHADOWS tier-3 (interpretive mapping) per fresh-verify.",
    "C_qf2": "Quaithe's 'the others' who come to Meereen = the besieging host. FORESHADOWS the renewed siege.",
}
GENERIC = "Participant/role edge on the Dany/Meereen arc (line-verified book cite)."


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-dany-meereen-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

INSURGENCY = """\
---
name: "Sons of the Harpy Insurgency"
type: event.incident
slug: sons-of-the-harpy-insurgency
aliases: ["the shadow war of Meereen", "the Harpy's shadow war", "the Sons of the Harpy insurgency"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s144-dany-meereen-enrich
node_version: 1
evidence_chapters:
  - ADWD Daenerys II
  - ADWD Daenerys IV
  - ADWD The Queen's Hand
---

## Identity

The masked-killer insurgency the [Sons of the Harpy](sons-of-the-harpy) wage by night against
[Daenerys](daenerys-targaryen)'s freedmen and Meereenese supporters after she takes the city —
the "shadow war" fought anew each night beneath the stepped pyramids. The killings (freedmen
knifed in their homes, the harpist Rylona Rhee's fingers cut off, the night the Harpy kills
twenty-nine) drive Dany toward the Ghiscari marriage to [Hizdahr zo Loraq](hizdahr-zo-loraq)
and the creation of the [Brazen Beasts](brazen-beasts) counter-watch under
[Skahaz the Shavepate](skahaz-mo-kandaq). Whether [Hizdahr](hizdahr-zo-loraq) himself is the
Harpy — the killings ceased during the peace and resumed once Dany fled — is the arc's central
unproven whodunit.

## Edges
(Edges in `graph/edges/edges.jsonl`, S144 Dany/Meereen enrichment. [Sons of the Harpy](sons-of-the-harpy)
AGENT_IN; [the twenty-nine-night](sons-of-the-harpy-kill-twenty-nine) + [the Reznak/Skahaz
counsel](reznak-and-skahaz-advise-on-the-murders) SUB_BEAT_OF; [Brazen Beasts](brazen-beasts) +
[Skahaz](skahaz-mo-kandaq) OPPOSES; MOTIVATES [Daenerys](daenerys-targaryen); ENABLES
[the wedding](wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen); [Hizdahr](hizdahr-zo-loraq)
SUSPECTED_OF.)

## Quotes

> Every night the shadow war was waged anew beneath the stepped pyramids of Meereen.

— ADWD Daenerys II (`sources/chapters/adwd/adwd-daenerys-02.md:31`)
"""

KINGBREAKER = """\
---
name: "Barristan Selmy Arrests Hizdahr zo Loraq"
type: event.incident
slug: barristan-arrests-hizdahr
aliases: ["the Kingbreaker", "the hour of the wolf coup", "Barristan arrests Hizdahr"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s144-dany-meereen-enrich
node_version: 1
evidence_chapters:
  - ADWD The Kingbreaker
---

## Identity

In the hour of the wolf after [Daenerys](daenerys-targaryen) flees the pit on
[Drogon](drogon), Ser [Barristan Selmy](barristan-selmy) and [Skahaz the Shavepate](skahaz-mo-kandaq)
move against King [Hizdahr zo Loraq](hizdahr-zo-loraq) — whom they suspect of the
[poisoned locusts](poisoned-locusts) and the [Harpy killings](sons-of-the-harpy-insurgency).
Barristan kills the pit fighter [Khrazz](khrazz) in single combat and takes Hizdahr prisoner,
seizing the rule of Meereen as the city's defender. The watchword of the coup is "Groleo," for
the murdered hostage admiral.

## Edges
(Edges in `graph/edges/edges.jsonl`, S144 Dany/Meereen enrichment. [Barristan](barristan-selmy)
COMMANDS_IN; [Skahaz](skahaz-mo-kandaq) AGENT_IN; [Brazen Beasts](brazen-beasts) PARTICIPATES_IN.
[Barristan KILLS khrazz](khrazz-killed) and IMPRISONS [Hizdahr](hizdahr-zo-loraq) already in graph.)

## Quotes

> "I am here for Hizdahr," the knight said. "Throw down your steel and stand aside, and no harm need come to you."

— Ser Barristan, ADWD The Kingbreaker (`sources/chapters/adwd/adwd-the-kingbreaker-01.md:295`)
"""

QUENTYN_CONTRACT = """\
---
name: "Quentyn Martell Contracts the Tattered Prince"
type: event.incident
slug: quentyn-contracts-tattered-prince
aliases: ["the Pentos bargain", "Quentyn hires the Windblown"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s144-dany-meereen-enrich
node_version: 1
evidence_chapters:
  - ADWD The Spurned Suitor
---

## Identity

His suit foreclosed by [Daenerys](daenerys-targaryen)'s marriage to
[Hizdahr](hizdahr-zo-loraq), [Quentyn Martell](quentyn-martell) secretly meets the
[Tattered Prince](tattered-prince) in the Purple Lotus cellar and bargains: the Windblown will
help him steal a dragon in exchange for the promise of Pentos. The contract equips and
greenlights the dragon-theft attempt that gets Quentyn killed.

## Edges
(Edges in `graph/edges/edges.jsonl`, S144 Dany/Meereen enrichment. [Quentyn](quentyn-martell) +
[the Tattered Prince](tattered-prince) AGENT_IN; Quentyn NEGOTIATES_WITH + CONTRACTED_WITH the
Tattered Prince; ENABLES [Quentyn orders the attack](quentyn-orders-the-attack).)

## Quotes

> "What I want," said the Tattered Prince, "is Pentos."

— ADWD The Spurned Suitor (`sources/chapters/adwd/adwd-the-spurned-suitor-01.md:193`)
"""

BEN_PLUMM_DEFECTS = """\
---
name: "Brown Ben Plumm Defects to the Yunkai'i"
type: event.incident
slug: ben-plumm-defects-to-yunkai
aliases: ["the third treason", "Brown Ben's defection", "the Second Sons go over"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s144-dany-meereen-enrich
node_version: 1
evidence_chapters:
  - ADWD Daenerys VIII
---

## Identity

[Brown Ben Plumm](ben-plumm) leads the [Second Sons](second-sons) out of
[Daenerys](daenerys-targaryen)'s service and over to the Yunkai'i once he concludes she cannot
loose her chained dragons against the besiegers — "we went over to the winning side." Dany later
reckons it the third of the three treasons foretold (the treason "for gold").

## Edges
(Edges in `graph/edges/edges.jsonl`, S144 Dany/Meereen enrichment. [Brown Ben](ben-plumm)
COMMANDS_IN; [Second Sons](second-sons) AGENT_IN. [Ben BETRAYS daenerys](ben-plumm) already in graph.)

## Quotes

> "We went over to the winning side, is all. Same as we done before. It weren't all me, neither. I put it to my men."

— Brown Ben Plumm, ADWD Daenerys VIII (`sources/chapters/adwd/adwd-daenerys-08.md:75`)
"""

BRONZE_HARPY = """\
---
name: "Bronze Harpy of Meereen"
type: object.artifact
slug: bronze-harpy-of-meereen
aliases: ["the bronze harpy", "the towering bronze harpy"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s144-dany-meereen-enrich
node_version: 1
evidence_chapters:
  - ASOS Daenerys V
---

## Identity

The great bronze statue of a harpy that stood eight hundred feet up atop the
[Great Pyramid](great-pyramid) of [Meereen](meereen) — a woman's torso, an eagle's wings, a
lion's legs, a scorpion's tail, holding chains in its claws — the civic symbol of Ghiscari
slaver-power, visible to armies miles outside the walls. [Daenerys](daenerys-targaryen) ordered
it taken down after the conquest; Ser [Barristan](barristan-selmy) later set a signal beacon on
the same apex.

## Edges
(Edges in `graph/edges/edges.jsonl`, S144 Dany/Meereen enrichment. LOCATED_AT
[the Great Pyramid](great-pyramid); DEPICTED_IN [the siege/taking of Meereen](siege-of-meereen).)

## Quotes

> Behind them, huge against the sky, could be seen the top of the Great Pyramid, a monstrous thing eight hundred feet tall with a towering bronze harpy at its top.

— Daenerys first sees Meereen, ASOS Daenerys V (`sources/chapters/asos/asos-daenerys-05.md:11`)

> "The harpy is a craven thing," Daario Naharis said when he saw it. "She has a woman's heart and a chicken's legs. Small wonder her sons hide behind their walls."

— Daario Naharis, ASOS Daenerys V (`sources/chapters/asos/asos-daenerys-05.md:13`)
"""

NODES = [
    ("sons-of-the-harpy-insurgency", NODES_EVENTS, INSURGENCY),
    ("barristan-arrests-hizdahr", NODES_EVENTS, KINGBREAKER),
    ("quentyn-contracts-tattered-prince", NODES_EVENTS, QUENTYN_CONTRACT),
    ("ben-plumm-defects-to-yunkai", NODES_EVENTS, BEN_PLUMM_DEFECTS),
    ("bronze-harpy-of-meereen", NODES_ARTIFACTS, BRONZE_HARPY),
]


def make_edge_row(e):
    book = e["ref"].split("/")[2]
    chap_id = e["ref"].split("/")[-1].rsplit(".md:", 1)[0]
    row = {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        **common(),
        "evidence_book": book,
        "evidence_chapter": chap_id,
        "evidence_ref": e["ref"],
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": ASSERTED.get(e["id"], GENERIC),
    }
    if e["id"] in VERIFIED:
        row["verified_by"] = VERIFIED[e["id"]]
    return row


def main():
    data = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    edges = data["edges"]

    all_slugs = {e["source"] for e in edges} | {e["target"] for e in edges}
    check = all_slugs - NEW_NODE_SLUGS
    resolved, missing = precheck_slugs(check)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent: {missing}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw = EDGES.read_text(encoding="utf-8").splitlines()
    existing = [ln for ln in raw if ln.strip()]
    if any(RUN_ID in ln for ln in existing):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup → {BACKUP}")

    # Retire the stale tier-3 COMMANDS_IN edge (superseded by B10 SUSPECTED_OF).
    kept, retired = [], 0
    for ln in existing:
        o = json.loads(ln)
        if (o.get("source_slug"), o.get("edge_type"), o.get("target_slug")) == RETIRE:
            retired += 1
            continue
        kept.append(ln)
    print(f"Retired stale edge {RETIRE}: {retired} removed.")

    created = []
    for slug, node_dir, body in NODES:
        path = node_dir / f"{slug}.node.md"
        if path.exists():
            print(f"  SKIP node (exists): {path.name}")
        else:
            path.write_text(body, encoding="utf-8")
            created.append(slug)
            print(f"  Created node: {path.relative_to(REPO)}")

    new_rows = [make_edge_row(e) for e in edges]
    out = kept + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    counts = {}
    for e in edges:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(created)}): {', '.join(created) or '(none)'}")
    print(f"Edges appended ({len(new_rows)}):")
    for t, c in sorted(counts.items()):
        print(f"  {t}: {c}")
    print(f"Stale edges retired: {retired}")
    print(f"edges.jsonl: {len(existing)} → {len(out)} lines (net {len(out) - len(existing):+d})")


if __name__ == "__main__":
    main()
