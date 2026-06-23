#!/usr/bin/env python3
"""Mint Blackwater enrichment pass 1 (S138) — fifth major-arc enrichment dip.

Board-picked target (S136 clean #2 after Ned's Downfall). The hub
`battle-of-the-blackwater` was causally wired up/down (S111 downstream CAUSES +
S123 J2/J9 upstream ENABLES) and carries rich wiki prose, but the OFF-SPINE battle
substrate was unbuilt as graph nodes/edges: the wildfire trap, the chain boom,
Tyrion's sortie, Sandor's nerve-break/desertion, Garlan-as-Renly's-ghost (the
decisive rout), the participants/witnesses, the whodunit on Mandon Moore's attempt.

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+SUSPECTED_OF
+WITNESS / descriptive-object-depth / existing-node<->existing-node causal-wiring)
over the built cluster. PROPOSE-only lenses -> Opus orchestrator synthesized +
LINE-CHECKED every cite against the ACOK source files -> this mint set.

FINAL: 6 new nodes + 42 edges. (verified=pending-fresh-verify on the 7 interpretive
causal/IMPERSONATES edges; Tier-1 role/structural edges verified=None.)

NEW NODES (6):
  - wildfire-trap-on-the-blackwater       (event.battle)   — the green-fire trap; NOT `wildfire-plot` (Aerys/RR node)
  - tyrion-s-sortie-at-the-king-s-gate    (event.battle)   — Tyrion leads the sortie after Sandor refuses
  - garlan-tyrell-routs-stannis-as-renly-s-ghost (event.battle) — the decisive "Renly's ghost" rout
  - sandor-clegane-deserts-the-kingsguard (event.incident) — the Hound's nerve breaks -> desertion
  - joffrey-recalled-to-the-red-keep      (event.incident) — Cersei pulls Joffrey; gold-cloak morale collapse
  - blackwater-chain-boom                 (object.artifact)— the iron chain across the river mouth

DEDUP DROPS (already in graph, confirmed via grep):
  - tyrion-lannister VICTIM_IN a-knight-attacks-tyrion-s-shield (exists)
  - podrick-payne KILLS mandon-moore (exists)
  - mandon-moore ATTACKS tyrion-lannister (exists)

CRITICAL non-conflation: `wildfire-plot` is the AERYS-II / Robert's-Rebellion 283 AC
wildfire-cache node (FIGHTS_IN robert's-rebellion; MOTIVATES slaying-of-aerys-ii from
RR-S133). The Blackwater wildfire gets its OWN node `wildfire-trap-on-the-blackwater`
and is NEVER wired to `wildfire-plot`.

First-use canonical types this run: none new (all from the 170-type locked vocab).
IMPERSONATES first appearance in an enrichment dip (Garlan-as-Renly).

DEFERRED -> pass-2 / harvest (NOT minted):
  - the-antler-men-conspiracy wiring (needs member nodes or a clearer event model; no
    clean AGENT_IN/causal edge without conflating conspirators with executioners)
  - battle-of-oxcross / battle-of-the-fords ENABLES battle-of-the-blackwater (sound WO5K
    seams but grounded in inference/wiki-text, not clean book quotes -> WO5K enrichment)
  - battle -> tyrion-processes-the-assassination-attempt / Tyrion-loses-Handship (thin
    plate-3 stub target; mint a clean `tyrion-loses-the-handship` node first)
  - the full named-ship roster WIELDED_IN battle (~20 ships) -> deterministic Python batch
    (only the 3 narratively load-bearing flagships minted here: fury, black-betha, swordfish)
  - song `Gentle Mother` text node (no clean event-edge type for a song; captured as harvest)
  - cersei WITNESS_IN battle (FAILS text-anchor gate — she receives reports in Maegor's,
    does not SEE the battle; the S137-style mistarget catch)

Safeguards mirror mint_neds_downfall_enrichment_s137.py: backup, re-run guard, slug
pre-check (new-node slugs excluded), new-node create-if-absent.
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-blackwater-enrichment-2026-06-23.jsonl"

RUN_ID = "blackwater-enrichment-s138"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "wildfire-trap-on-the-blackwater",
    "tyrion-s-sortie-at-the-king-s-gate",
    "garlan-tyrell-routs-stannis-as-renly-s-ghost",
    "sandor-clegane-deserts-the-kingsguard",
    "joffrey-recalled-to-the-red-keep",
    "blackwater-chain-boom",
}


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-bw-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

WILDFIRE_TRAP = """\
---
name: "Wildfire trap on the Blackwater"
type: event.battle
slug: wildfire-trap-on-the-blackwater
aliases: ["the burning of the Blackwater", "the green fire on the Blackwater"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
evidence_chapters:
  - ACOK Davos III
  - ACOK Tyrion XIII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

The decisive tactical event of the [Battle of the Blackwater](battle-of-the-blackwater): [Tyrion Lannister](tyrion-lannister), advised by the pyromancer [Hallyne](hallyne) of the Alchemists' Guild, pre-positioned rotting hulks stuffed with thousands of jars of [wildfire](wildfire) in the Blackwater Rush. When [Stannis Baratheon](stannis-baratheon)'s fleet had rowed up the river, the wildfire was ignited — a wall of green flame that consumed most of both fleets and turned the river into "the mouth of hell." Distinct from [the Aerys-II wildfire-cache plot](wildfire-plot) of 283 AC. A SUB_BEAT_OF the battle.

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. SUB_BEAT_OF battle-of-the-blackwater; [Tyrion Lannister](tyrion-lannister) + [Hallyne](hallyne) AGENT_IN; [wildfire](wildfire) WIELDED_IN the battle.)

## Quotes

> He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames. A fountain of burning jade rose from the river, the blast so bright he had to shield his eyes.

— Tyrion Lannister's POV, ACOK Tyrion XIII (`sources/chapters/acok/acok-tyrion-13.md:19`)
"""

TYRION_SORTIE = """\
---
name: "Tyrion's sortie at the King's Gate"
type: event.battle
slug: tyrion-s-sortie-at-the-king-s-gate
aliases: ["Tyrion leads the sortie", "the King's Gate sortie"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
evidence_chapters:
  - ACOK Tyrion XIII
  - ACOK Tyrion XIV
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

After [Sandor Clegane](sandor-clegane) refused to lead another sortie into the fire, [Tyrion Lannister](tyrion-lannister) personally led a mounted sortie out the sally port of the King's Gate, dispersing the battering-ram party and routing Stannis's men along the burning riverfront ("So come with me and kill the son of a bitch!"). The sortie carried him onto the bridge of ships, where [Ser Mandon Moore](mandon-moore) attempted to murder him. A SUB_BEAT_OF the [Battle of the Blackwater](battle-of-the-blackwater).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. SUB_BEAT_OF battle-of-the-blackwater; [Tyrion Lannister](tyrion-lannister) AGENT_IN; caused by [Sandor's refusal](sandor-clegane-deserts-the-kingsguard); ENABLES [the attack on Tyrion](a-knight-attacks-tyrion-s-shield).)

## Quotes

> "You won't hear me shout out Joffrey's name," he told them. "You won't hear me yell for Casterly Rock either. This is your city Stannis means to sack, and that's your gate he's bringing down. So come with me and kill the son of a bitch!"

— Tyrion Lannister to the gold cloaks, ACOK Tyrion XIII (`sources/chapters/acok/acok-tyrion-13.md:87`)
"""

GARLAN_ROUT = """\
---
name: "Garlan Tyrell routs Stannis as Renly's ghost"
type: event.battle
slug: garlan-tyrell-routs-stannis-as-renly-s-ghost
aliases: ["Renly's ghost", "the vanguard breaks Stannis", "Lord Renly's shade at the Blackwater"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
evidence_chapters:
  - ACOK Sansa VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: secondary-report
  date_confidence: tier-2
---

## Identity

The decisive psychological stroke of the [Battle of the Blackwater](battle-of-the-blackwater). [Ser Garlan Tyrell](garlan-tyrell), wearing the dead [Renly Baratheon](renly-baratheon)'s distinctive green armor and golden antlers, led the Lannister-Tyrell relief vanguard into Stannis's rear. Stannis's host — mostly former Renly men — broke at the sight of "Lord Renly," many shouting his name and going over or fleeing. The rout it produced forced [Stannis's retreat to Dragonstone](stannis-retreats-to-dragonstone). A SUB_BEAT_OF the battle. (In-the-moment witnesses, incl. Dontos relaying it to Sansa, believe it is literally Renly's shade; the Garlan-in-Renly's-armor identification is established canon.)

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. SUB_BEAT_OF battle-of-the-blackwater; [Garlan Tyrell](garlan-tyrell) AGENT_IN + IMPERSONATES [Renly](renly-baratheon) + KILLS [Guyard Morrigen](guyard-morrigen) [Tier-2 hearsay]; CAUSES [Stannis's retreat](stannis-retreats-to-dragonstone).)

## Quotes

> "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand! They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well. It was Renly, it was Renly, it was Renly!"

— Ser Dontos Hollard to Sansa Stark, ACOK Sansa VII (`sources/chapters/acok/acok-sansa-07.md:145`)
"""

SANDOR_DESERTS = """\
---
name: "Sandor Clegane deserts the Kingsguard"
type: event.incident
slug: sandor-clegane-deserts-the-kingsguard
aliases: ["the Hound's failure of nerve", "Sandor refuses the sortie", "the Hound quits the Kingsguard"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
evidence_chapters:
  - ACOK Tyrion XIII
  - ACOK Sansa VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

Terrified by the wildfire, [Sandor Clegane](sandor-clegane) — the [Hound](sandor-clegane) — refused [Tyrion Lannister](tyrion-lannister)'s order to lead another sortie ("Bugger that. And you. ... Bring me wine"), forcing Tyrion to lead it himself. Later that night Sandor abandoned the Kingsguard entirely: he appeared drunk in [Sansa Stark](sansa-stark)'s chamber, held a knife to her throat, and left his bloodstained white cloak behind on the floor when he fled King's Landing. The fire-fear that breaks the realm's most feared warrior, and the start of his arc on the road. A SUB_BEAT_OF the [Battle of the Blackwater](battle-of-the-blackwater).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. SUB_BEAT_OF battle-of-the-blackwater; [Sandor Clegane](sandor-clegane) AGENT_IN; the battle MOTIVATES him; his refusal CAUSES [Tyrion's sortie](tyrion-s-sortie-at-the-king-s-gate).)

## Quotes

> "Bugger the King's Hand." Where the Hound's face was not sticky with blood, it was pale as milk. "Someone bring me a drink." A gold cloak officer handed him a cup. Clegane took a swallow, spit it out, flung the cup away. "Water? Fuck your water. Bring me wine."

— ACOK Tyrion XIII (`sources/chapters/acok/acok-tyrion-13.md:71`)
"""

JOFFREY_RECALLED = """\
---
name: "Joffrey recalled to the Red Keep"
type: event.incident
slug: joffrey-recalled-to-the-red-keep
aliases: ["Cersei pulls Joffrey from the walls", "Joffrey leaves the Mud Gate"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
evidence_chapters:
  - ACOK Sansa VI
  - ACOK Sansa VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

At the height of the battle, [Cersei Lannister](cersei-lannister) sent [Osfryd Kettleblack](osfryd-kettleblack) to fetch King [Joffrey](joffrey-baratheon) back from the walls to the safety of Maegor's Holdfast — against [Tyrion](tyrion-lannister)'s arrangement and [Lancel](lancel-lannister)'s furious protest. When the gold cloaks saw their king leaving, hundreds threw down their spears and ran; the defense very nearly collapsed before [Tywin](tywin-lannister)'s relief arrived. Cersei's near-fatal interference. A SUB_BEAT_OF the [Battle of the Blackwater](battle-of-the-blackwater).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. SUB_BEAT_OF battle-of-the-blackwater; [Cersei Lannister](cersei-lannister) AGENT_IN.)

## Quotes

> Gods be damned, Cersei, why did you have them fetch Joffrey back to the castle? The gold cloaks are throwing down their spears and running, hundreds of them. When they saw the king leaving, they lost all heart.

— Ser Lancel Lannister to Cersei, ACOK Sansa VII (`sources/chapters/acok/acok-sansa-07.md:13`)
"""

CHAIN_BOOM = """\
---
name: "The chain boom of the Blackwater"
type: object.artifact
slug: blackwater-chain-boom
aliases: ["the great chain", "the Blackwater chain"]
confidence: tier-1
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
material: iron
evidence_chapters:
  - ACOK Tyrion XIII
  - ACOK Davos III
---

## Identity

A massive iron chain boom stretched across the mouth of the Blackwater Rush between two newly built winch-towers, commissioned by [Tyrion Lannister](tyrion-lannister) for the defense of King's Landing. [Bronn](bronn) raised it at the winches — earning his knighthood as "Ser Bronn of the Blackwater" — the moment Stannis's fleet had rowed past, sealing the burning ships inside the river: "King Stannis had rowed his fleet up the Blackwater, but he would not row out again." The decisive material instrument of the battle alongside the [wildfire](wildfire).

## Edges

(Edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. WIELDED_IN [battle-of-the-blackwater](battle-of-the-blackwater).)

## Quotes

> Where the river broadened out into Blackwater Bay, the boom stretched taut, a bare two or three feet above the water. Already a dozen galleys had crashed into it, and the current was pushing others against them. Almost all were aflame, and the rest soon would be.

— Davos Seaworth's POV, ACOK Davos III (`sources/chapters/acok/acok-davos-03.md:147`)
"""

# (slug, dir, body)
NODES = [
    ("wildfire-trap-on-the-blackwater", NODES_EVENTS, WILDFIRE_TRAP),
    ("tyrion-s-sortie-at-the-king-s-gate", NODES_EVENTS, TYRION_SORTIE),
    ("garlan-tyrell-routs-stannis-as-renly-s-ghost", NODES_EVENTS, GARLAN_ROUT),
    ("sandor-clegane-deserts-the-kingsguard", NODES_EVENTS, SANDOR_DESERTS),
    ("joffrey-recalled-to-the-red-keep", NODES_EVENTS, JOFFREY_RECALLED),
    ("blackwater-chain-boom", NODES_ARTIFACTS, CHAIN_BOOM),
]


# ════════════════════════════ EDGES ════════════════════════════
# (source, edge_type, target, tier, book, chap_id, line, quote, asserted, verified_or_None)
EDGES_SPEC = [
    # ════ CAUSAL / SUBSTRATE (7) — verified=pending → fresh-verify ════
    ("garlan-tyrell-routs-stannis-as-renly-s-ghost", "CAUSES",
     "stannis-retreats-to-dragonstone", 2,
     "acok", "acok-sansa-07", 141,
     "Lord Tywin himself had their right wing on the north side of the river, with Randyll Tarly commanding the center and Mace Tyrell the left, but the vanguard won the fight.",
     "The relief vanguard under Garlan-as-Renly's-ghost broke Stannis's host (former Renly men shouting for 'Lord Renly' and going over). The on-field rout is the proximate cause of Stannis's withdrawal; sharper attribution than the existing battle->retreat hub CAUSES. Stannis's retreat is constrained, not free => CAUSES Tier-2.",
     "pending-fresh-verify-s138"),
    ("sandor-clegane-deserts-the-kingsguard", "CAUSES",
     "tyrion-s-sortie-at-the-king-s-gate", 2,
     "acok", "acok-tyrion-13", 77,
     "This is madness, he thought, but sooner madness than defeat. Defeat is death and shame.",
     "Sandor's fire-driven refusal to lead another sortie produced the command vacuum that forced Tyrion to lead it himself (Tyrion reasons Mandon is 'not a man other men would follow'). CAUSES, mediation = Tyrion's own decision; not constitutive (separate beats).",
     "pending-fresh-verify-s138"),
    ("tyrion-s-sortie-at-the-king-s-gate", "ENABLES",
     "a-knight-attacks-tyrion-s-shield", 2,
     "acok", "acok-tyrion-14", 69,
     "The point slashed just beneath his eyes, and he felt its cold hard touch and then a blaze of pain.",
     "The sortie put Tyrion onto the bridge of ships in an exposed position where Mandon Moore could attempt the murder. ENABLES (door-opener): Mandon's free choice to strike is the proximate agent; the sortie only created the opportunity.",
     "pending-fresh-verify-s138"),
    ("battle-of-the-blackwater", "MOTIVATES", "sandor-clegane", 2,
     "acok", "acok-tyrion-14", 31,
     "Gods be good, no wonder the Hound was frightened. It's the flames he fears",
     "The wildfire battle drives Sandor's decision to break and desert — the fire-fear that overrides the realm's most feared warrior. MOTIVATES (event -> character), routing the human choice rather than collapsing it into a false event->event CAUSES.",
     "pending-fresh-verify-s138"),
    ("joffrey-sets-sansa-aside-and-agrees-to-wed-margaery", "ENABLES",
     "purple-wedding", 2,
     "acok", "acok-sansa-08", 41,
     "set Sansa Stark aside. The Lady Margaery will make you a far more suitable queen.",
     "The formal setting-aside of Sansa and betrothal to Margaery is the precondition for the Joffrey-Margaery marriage (= the Purple Wedding, ASOS). Cross-arc seam wiring the Blackwater aftermath forward into the Purple Wedding arc. ENABLES (planning/preparation steps intervene), Tier-2.",
     "pending-fresh-verify-s138"),
    ("cersei-lannister", "SUSPECTED_OF", "a-knight-attacks-tyrion-s-shield", 2,
     "acok", "acok-tyrion-15", 97,
     "Cersei must have paid him to see that I never came back from the battle. Why else? I never did Ser Mandon any harm that I know of.",
     "Tyrion's load-bearing in-world suspicion that Cersei suborned Mandon Moore to murder him during the battle — the whodunit substrate. SUSPECTED_OF never asserts the act (unconfirmed in the published text). Tier-2 cap.",
     "pending-fresh-verify-s138"),
    ("garlan-tyrell", "IMPERSONATES", "renly-baratheon", 2,
     "acok", "acok-sansa-07", 145,
     "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand!",
     "Garlan deliberately wore the dead Renly's distinctive green-and-antlers armor to break Renly's former men. IMPERSONATES (impersonator -> impersonated). The grounding quote is the in-moment perception ('Lord Renly'); the Garlan identification is established canon. Tier-2 (interpretive).",
     "pending-fresh-verify-s138"),

    # ════ SUB_BEAT_OF (5) — Tier-1, verified=None ════
    ("wildfire-trap-on-the-blackwater", "SUB_BEAT_OF", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 19,
     "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames.",
     "The wildfire trap is the central tactical sub-event of the battle.", None),
    ("tyrion-s-sortie-at-the-king-s-gate", "SUB_BEAT_OF", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 87,
     "So come with me and kill the son of a bitch!",
     "Tyrion's sortie is a bounded tactical sub-event of the battle.", None),
    ("garlan-tyrell-routs-stannis-as-renly-s-ghost", "SUB_BEAT_OF", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 145,
     "but the vanguard won the fight.",
     "The Renly's-ghost rout is the decisive sub-event within the relief assault.", None),
    ("sandor-clegane-deserts-the-kingsguard", "SUB_BEAT_OF", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 57,
     "Clegane's breath came ragged. \"Bugger that. And you.\"",
     "Sandor's nerve-break begins during the battle and completes immediately after.", None),
    ("joffrey-recalled-to-the-red-keep", "SUB_BEAT_OF", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 13,
     "why did you have them fetch Joffrey back to the castle? The gold cloaks are throwing down their spears and running, hundreds of them.",
     "Cersei's recall of Joffrey is a discrete command decision inside the battle.", None),

    # ════ AGENT_IN on new nodes (5) — Tier-1 ════
    ("tyrion-lannister", "AGENT_IN", "wildfire-trap-on-the-blackwater", 1,
     "acok", "acok-tyrion-13", 19,
     "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames.",
     "Tyrion designed and positioned the wildfire hulks — the trap is his.", None),
    ("hallyne", "AGENT_IN", "wildfire-trap-on-the-blackwater", 1,
     "acok", "acok-tyrion-13", 31,
     "Hallyne said that sometimes the substance burned so hot that flesh melted like tallow.",
     "Hallyne and the Alchemists' Guild produced and managed the wildfire for the trap.", None),
    ("tyrion-lannister", "AGENT_IN", "tyrion-s-sortie-at-the-king-s-gate", 1,
     "acok", "acok-tyrion-13", 77,
     "Very well, I'll lead the sortie.",
     "Tyrion personally leads the sortie after Sandor refuses.", None),
    ("garlan-tyrell", "AGENT_IN", "garlan-tyrell-routs-stannis-as-renly-s-ghost", 1,
     "acok", "acok-sansa-07", 145,
     "And do you know who led the vanguard?",
     "Garlan led the relief vanguard that routed Stannis.", None),
    ("sandor-clegane", "AGENT_IN", "sandor-clegane-deserts-the-kingsguard", 1,
     "acok", "acok-tyrion-13", 57,
     "Clegane's breath came ragged. \"Bugger that. And you.\"",
     "Sandor is the agent of his own refusal/desertion.", None),
    ("cersei-lannister", "AGENT_IN", "joffrey-recalled-to-the-red-keep", 1,
     "acok", "acok-sansa-07", 13,
     "why did you have them fetch Joffrey back to the castle?",
     "Cersei ordered Joffrey fetched back to the castle (Lancel blames her directly).", None),

    # ════ HUB participant roles (15) — Tier-1 ════
    ("tyrion-lannister", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 87,
     "This is your city Stannis means to sack, and that's your gate he's bringing down.",
     "Tyrion is the overall commander of the King's Landing defense (defense side).", None),
    ("stannis-baratheon", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 21,
     "He would command from the rear, from the reserve, much as Lord Tywin Lannister was wont to do.",
     "Stannis commands the Baratheon host from the south bank (attacker side).", None),
    ("imry-florent", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 15,
     "trusting Fury and the command of his fleet to his wife's brother Ser Imry",
     "Ser Imry Florent commands Stannis's fleet from Fury (attacker fleet).", None),
    ("bronn", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 27,
     "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep",
     "Bronn commands the winch towers that raise the chain (defense side); knighted as 'Ser Bronn of the Blackwater' for it.", None),
    ("tywin-lannister", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 141,
     "Lord Tywin himself had their right wing on the north side of the river",
     "Tywin commands the right wing of the relief force (defense relief).", None),
    ("mace-tyrell", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 141,
     "with Randyll Tarly commanding the center and Mace Tyrell the left",
     "Mace Tyrell commands the left wing of the relief force.", None),
    ("randyll-tarly", "COMMANDS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 141,
     "with Randyll Tarly commanding the center and Mace Tyrell the left",
     "Randyll Tarly commands the center of the relief force.", None),
    ("sandor-clegane", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 87,
     "Davos recognized the dog's-head helm of the Hound. A white cloak streamed from his shoulders as he rode his horse up the plank onto the deck of Prayer, hacking down anyone who blundered within reach.",
     "Sandor fights on the riverbank against Stannis's archers before his nerve breaks.", None),
    ("davos-seaworth", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 99,
     "\"Ramming speed!\" Davos shouted.",
     "Davos commands Black Betha, rams and boards in the river fight.", None),
    ("podrick-payne", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-15", 117,
     "It was Pod on the bridge of boats, the lad saved my life.",
     "Pod rides in the sortie and fights through the bridge-of-ships melee, saving Tyrion.", None),
    ("balon-swann", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-14", 45,
     "Every bit of Ser Balon was spattered with gore and smudged by smoke.",
     "Balon Swann fights on the riverfront and rides with Tyrion's sortie.", None),
    ("mandon-moore", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-14", 53,
     "Ser Mandon fell in with them, his shield a ragged ruin.",
     "Mandon Moore rides in Tyrion's sortie and fights in the bridge-of-ships melee.", None),
    ("garlan-tyrell", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 141,
     "but the vanguard won the fight.",
     "Garlan Tyrell leads the relief vanguard in the battle.", None),
    ("guyard-morrigen", "FIGHTS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 145,
     "They say he killed Ser Guyard Morrigen himself in single combat",
     "Ser Guyard Morrigen, a Stannis van commander, fights and is slain in the battle.", None),
    ("ilyn-payne", "PARTICIPATES_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-06", 115,
     "Sansa had not even seen Ser Ilyn return to the hall, but suddenly there he was, striding from the shadows behind the dais as silent as a cat. He carried Ice unsheathed.",
     "Ilyn Payne holds a battlefield-contingency role in Maegor's Holdfast — posted to kill the highborn women with Ice if the city falls. PARTICIPATES_IN (active role, not a combatant).", None),

    # ════ WITNESS_IN (1) — Tier-1, text-anchor satisfied ════
    ("sansa-stark", "WITNESS_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-sansa-07", 59,
     "The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires that burned below.",
     "Sansa directly perceives the burning river / wildfire spectacle from her bedchamber window — text-anchor gate satisfied (she SEES the charged spectacle). (Cersei, by contrast, only receives reports in Maegor's -> NOT a witness.)", None),

    # ════ Attack-stub role (1 NEW; VICTIM_IN tyrion already exists) — Tier-1 ════
    ("mandon-moore", "AGENT_IN", "a-knight-attacks-tyrion-s-shield", 1,
     "acok", "acok-tyrion-14", 69,
     "The point slashed just beneath his eyes, and he felt its cold hard touch and then a blaze of pain.",
     "Mandon Moore is the agent of the attack on Tyrion (he first feigns a helping hand, then cuts Tyrion's face). tyrion-lannister VICTIM_IN already in graph.", None),

    # ════ RESCUES / KILLS (2 NEW; podrick KILLS mandon already exists) ════
    ("podrick-payne", "RESCUES", "tyrion-lannister", 1,
     "acok", "acok-tyrion-15", 117,
     "It was Pod on the bridge of boats, the lad saved my life.",
     "Pod saves Tyrion's life on the bridge of ships (by killing Mandon Moore — that KILLS edge already exists). RESCUES = the dramatic single-moment extraction from death.", None),
    ("garlan-tyrell", "KILLS", "guyard-morrigen", 2,
     "acok", "acok-sansa-07", 145,
     "They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well.",
     "Garlan (as Renly's ghost) slays Ser Guyard Morrigen in the vanguard charge. Tier-2: in-world hearsay ('they say').", None),

    # ════ OBJECT WIELDED_IN (5) — Tier-1 ════
    ("blackwater-chain-boom", "WIELDED_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 145,
     "The chain. Gods save us, they've raised the chain.",
     "The chain boom is raised across the river mouth to trap Stannis's burning fleet — the decisive material instrument of the battle.", None),
    ("wildfire", "WIELDED_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-tyrion-13", 11,
     "The kiss of wildfire turned proud ships into funeral pyres and men into living torches.",
     "Wildfire (the substance) is deployed as the battle's primary weapon; first book-grounded WIELDED_IN wiring of the wildfire node to the event.", None),
    ("fury", "WIELDED_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 15,
     "Davos could make out Fury well to the southeast, her sails shimmering golden as they came down, the crowned stag of Baratheon blazoned on the canvas.",
     "Fury is Stannis's fleet flagship, centering the first battle line.", None),
    ("black-betha", "WIELDED_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 11,
     "Black Betha rode the flood tide, her sail cracking and snapping at each shift of wind.",
     "Black Betha is Davos's flagship and the POV ship for the river fight.", None),
    ("swordfish-ship", "WIELDED_IN", "battle-of-the-blackwater", 1,
     "acok", "acok-davos-03", 131,
     "With a grinding, splintering, tearing crash, Swordfish split the rotted hulk asunder.",
     "Swordfish rams the wildfire hulk that triggers the conflagration — the pivotal ship of the battle.", None),
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
