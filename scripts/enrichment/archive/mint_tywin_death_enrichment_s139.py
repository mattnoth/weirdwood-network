#!/usr/bin/env python3
"""Mint Tywin's-Death enrichment pass 1 (S139) — sixth major-arc enrichment dip.

Fork-1 board pick (Matt S139): the assassination-of-tywin-lannister event-arc. The
S109 causal SPINE (trial -> Oberyn-Gregor combat -> Jaime frees -> Tysha reveal ->
assassination, + Shae-kill sibling + cersei-rearms downstream) was already built and
well-wired. This pass ENRICHES the OFF-SPINE substrate the spine lacked as graph
nodes/edges: the murder instruments (crossbow, Hand's chain, Oberyn's poisoned spear),
Shae's betrayal-testimony, Oberyn's Elia-vengeance motive, Tywin's Tysha deception,
the trial witness-parade + judges, the trial-by-combat roles, and the escape -> exile.

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+WITNESS /
descriptive-object-depth / existing-node<->existing-node causal-wiring) over the built
cluster. PROPOSE-only lenses -> Opus orchestrator synthesized + LINE-CHECKED every cite
against the ASOS source files -> this mint set.

THE LINE-CHECK CATCH: lenses 1 & 3 mis-cited Shae's testimony / "my giant of Lannister"
to ch09:39. It is actually ch10 (she is the "one final witness" brought "on the morrow",
ch09:329): "my giant of Lannister" = ch10:39 (testimony) + ch11:205 (dying echo);
confession ch10:57; trial-by-combat demand ch10:65. All cites re-verified by grep.

FINAL: 5 new nodes + 37 edges. (verified=pending-fresh-verify on the 8 interpretive
causal/motive/dyadic edges; Tier-1 role/structural/object edges verified=None.)

NEW NODES (5):
  - tywins-crossbow                          (object.artifact) — wall-hung crossbow; Tywin killed with his own bow
  - hands-chain-of-office                     (object.artifact) — the Hand's gold chain; Shae strangled with it
  - oberyn-spear                              (object.artifact) — Oberyn's 8-ft ash spear; the manticore-venom vector
  - shae-testifies-against-tyrion-at-trial    (event.incident)  — Cersei's final witness; the betrayal he avenges
  - varys-smuggles-tyrion-out-of-kings-landing(event.incident)  — the escape -> exile (forward-wires the ADWD arc)

REJECTED at synthesis (see working/enrichment/tywin-death/synthesis-decisions.md):
  - tywin AGENT_IN/COMMANDS_IN jaime-reveals (conflates lie-author with reveal-agent)
  - tywin MANIPULATES jaime (command != manipulation; Jaime knew he lied)
  - cersei MANIPULATES shae (Shae knew she lied; redundant with COMMANDS_IN testimony)
  - pycelle/varys BETRAYS tyrion (enmity / surface; shae BETRAYS tyrion already x2 in graph)
  - tysha VICTIM_IN reveal (stretch); jaime-reveals MOTIVATES jaime (circular)

DEFERRED -> pass-2 / harvest: Tommen-accession node; Jaime-burns-Cersei-letter node;
  the-strangler poison node + Pycelle pharmacopoeia; widows-wail book-cite overlay.

Safeguards mirror mint_blackwater_enrichment_s138.py: backup, re-run guard, slug
pre-check (NEW_NODE_SLUGS excluded), new-node create-if-absent, optional qualifier.
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-tywin-death-enrichment-2026-06-23.jsonl"

RUN_ID = "tywin-death-enrichment-s139"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "tywins-crossbow",
    "hands-chain-of-office",
    "oberyn-spear",
    "shae-testifies-against-tyrion-at-trial",
    "varys-smuggles-tyrion-out-of-kings-landing",
}


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-tywin-death-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

TYWINS_CROSSBOW = """\
---
name: "Tywin's crossbow"
type: object.artifact
slug: tywins-crossbow
aliases: ["the crossbow on the wall", "Lord Tywin's crossbow"]
confidence: tier-1
era: current-narrative
pass_origin: s139-tywin-death-enrich
node_version: 1
material: wood-and-iron
evidence_chapters:
  - ASOS Tyrion XI
---

## Identity

The crossbow that hung on the wall of the Tower of the Hand's bedchamber — formerly [Tyrion Lannister](tyrion-lannister)'s own quarters. Fleeing King's Landing through the secret passages, Tyrion took it down, cocked it, and used it to kill his father [Tywin Lannister](tywin-lannister) on the privy. Tywin recognized it as his own ("Is that my crossbow? Put it down."), making the patricide doubly ironic — the Old Lion slain with his own weapon, on the privy, giving the lie to the jape that Tywin Lannister shat gold. The murder weapon of one of the most consequential killings in the series; Tyrion's reputation as a crossbow-killer follows him into ADWD.

## Edges

(Role/object edges live in `graph/edges/edges.jsonl`, S139 Tywin-death enrichment. WIELDED_IN [assassination-of-tywin-lannister](assassination-of-tywin-lannister); [Tyrion Lannister](tyrion-lannister) WIELDS; [Tywin Lannister](tywin-lannister) OWNS + KILLED_WITH.)

## Quotes

> A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls. The poleaxe would be clumsy to wield inside a castle, and the mace was too high to reach, but a large wood-and-iron chest had been placed against the wall directly under the crossbow. He climbed up, pulled down the bow and a leather quiver packed with quarrels, jammed a foot into the stirrup, and pushed down until the bowstring cocked.

— Tyrion Lannister's POV, ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:211`)

> The crossbow whanged just as Lord Tywin started to rise. The bolt slammed into him above the groin and he sat back down with a grunt.

— ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:259`)
"""

HANDS_CHAIN = """\
---
name: "The Hand's chain of office"
type: object.artifact
slug: hands-chain-of-office
aliases: ["the chain of golden hands", "the Hand's golden chain"]
confidence: tier-1
era: current-narrative
pass_origin: s139-tywin-death-enrich
node_version: 1
material: gold
evidence_chapters:
  - ASOS Tyrion XI
---

## Identity

The physical chain of office worn by the [Hand of the King](hand-of-the-king) — a chain of linked golden hands, each clasping the next. (Distinct from the `hand-of-the-king` TITLE node — this is the object.) [Tyrion Lannister](tyrion-lannister) wore it as Hand; [Tywin Lannister](tywin-lannister) wore it after him. Fleeing King's Landing, Tyrion found [Shae](shae) naked in his father's bed wearing the chain about her throat — and strangled her to death with it, reciting the Symon Silver Tongue lyric "For hands of gold are always cold, but a woman's hands are warm." Doubly iconic: the emblem of the office Tyrion lost, turned into the murder weapon of the woman he loved.

## Edges

(Object edges live in `graph/edges/edges.jsonl`, S139 Tywin-death enrichment. WIELDED_IN [tyrion-kills-shae-in-tywins-bed](tyrion-kills-shae-in-tywins-bed); [Tyrion Lannister](tyrion-lannister) WIELDS; [Shae](shae) KILLED_WITH.)

## Quotes

> Beneath it she was naked, but for the chain about her throat. A chain of linked golden hands, each holding the next.

— ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:197`)

> Tyrion slid a hand under his father's chain, and twisted. The links tightened, digging into her neck. "For hands of gold are always cold, but a woman's hands are warm," he said.

— ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:209`)
"""

OBERYN_SPEAR = """\
---
name: "Oberyn Martell's spear"
type: object.artifact
slug: oberyn-spear
aliases: ["the Red Viper's spear", "Oberyn's poisoned spear"]
confidence: tier-1
era: current-narrative
pass_origin: s139-tywin-death-enrich
node_version: 1
material: ash-and-steel
evidence_chapters:
  - ASOS Tyrion X
---

## Identity

[Oberyn Martell](oberyn-martell)'s personal fighting spear: eight feet of turned ash, the last two feet a slender leaf-shaped steel head narrowing to a wicked spike, the shaft glistening black with what Tyrion guessed was oil — or poison. As [Tyrion Lannister](tyrion-lannister)'s champion in the [trial by combat](gregor-confesses-and-kills-oberyn), Oberyn used the spear's reach to wound [Ser Gregor Clegane](gregor-clegane) through the armpit joint, coating the wound with [manticore venom](manticore-venom) that would kill the Mountain slowly. The spear's shaft snapped as Oberyn drove it down for the kill — the instant before Gregor seized him and crushed his skull. The venom vector that begins the AFFC/ADWD "Robert Strong" arc.

## Edges

(Object edges live in `graph/edges/edges.jsonl`, S139 Tywin-death enrichment. WIELDED_IN [gregor-confesses-and-kills-oberyn](gregor-confesses-and-kills-oberyn); [Oberyn Martell](oberyn-martell) WIELDS; carries the [manticore-venom](manticore-venom) that poisons Gregor.)

## Quotes

> The spear was turned ash eight feet long, the shaft smooth, thick, and heavy. The last two feet of that was steel: a slender leaf-shaped spearhead narrowing to a wicked spike. The edges looked sharp enough to shave with. When Oberyn spun the haft between the palms of his hand, they glistened black. Oil? Or poison?

— Tyrion Lannister's POV, ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:123`)
"""

SHAE_TESTIFIES = """\
---
name: "Shae testifies against Tyrion at his trial"
type: event.incident
slug: shae-testifies-against-tyrion-at-trial
aliases: ["Shae's false testimony", "my giant of Lannister", "Shae the final witness"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s139-tywin-death-enrich
node_version: 1
evidence_chapters:
  - ASOS Tyrion X
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

[Cersei Lannister](cersei-lannister)'s coup de grâce at the [trial of Tyrion Lannister](trial-of-tyrion-lannister): she held [Shae](shae) back as "one final witness" and brought her before the judges on the last day. Shae — [Tyrion Lannister](tyrion-lannister)'s lover, whom he had hidden and loved — testified that he and [Sansa](sansa-stark) had plotted Joffrey's poisoning together, and humiliated him before the laughing hall with the detail that she had to call him "my giant of Lannister." Her betrayal broke Tyrion's composure and triggered his confession-speech and his demand for trial by combat. The phrase echoes at her death: when Tyrion later finds her in Tywin's bed and she says it again, he strangles her. A SUB_BEAT_OF the trial.

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S139 Tywin-death enrichment. SUB_BEAT_OF [trial-of-tyrion-lannister](trial-of-tyrion-lannister); [Shae](shae) AGENT_IN; [Cersei](cersei-lannister) COMMANDS_IN; MOTIVATES [Tyrion](tyrion-lannister) toward the trial-by-combat demand; CAUSES [the killing of Shae](tyrion-kills-shae-in-tywins-bed). [Shae](shae) BETRAYS [Tyrion](tyrion-lannister) already in graph.)

## Quotes

> "Unspeakable things." As the tears rolled slowly down that pretty face, no doubt every man in the hall wanted to take Shae in his arms and comfort her. "With my mouth and . . . other parts, m'lord. All my parts. He used me every way there was, and . . . he used to make me tell him how big he was. My giant, I had to call him, my giant of Lannister."

— ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:39`)
"""

VARYS_SMUGGLES = """\
---
name: "Varys smuggles Tyrion out of King's Landing"
type: event.incident
slug: varys-smuggles-tyrion-out-of-kings-landing
aliases: ["Tyrion's escape into exile", "Varys spirits Tyrion away"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s139-tywin-death-enrich
node_version: 1
evidence_chapters:
  - ASOS Tyrion XI
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

After [Jaime Lannister](jaime-lannister) freed him from the black cells, [Tyrion Lannister](tyrion-lannister) was led by [Varys](varys) — who had dosed the gaolers' wine with sweetsleep and disguised himself in a septon's robe — down through the dungeons and secret passages of the [Red Keep](red-keep), bound for the sewers, the river, and a galley waiting in Blackwater Bay to carry him to the Free Cities. Tyrion's detour to kill [Shae](shae) and [Tywin](tywin-lannister) happened mid-escape; Varys then continued spiriting him out. The escape that launches Tyrion's exile arc (Pentos, Illyrio, the road to Daenerys). A SUB_BEAT_OF the Tywin-death sequence; forward-wires into the ADWD Essos arc.

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S139 Tywin-death enrichment. [Jaime frees Tyrion](jaime-frees-tyrion-from-the-black-cells) ENABLES this; [Varys](varys) + [Tyrion](tyrion-lannister) AGENT_IN; LOCATED_AT [red-keep](red-keep).)

## Quotes

> "You're going down into the sewers, and from there to the river. A galley is waiting in the bay. Varys has agents in the Free Cities who will see that you do not lack for funds . . . but try not to be conspicuous. Cersei will send men after you, I have no doubt. You might do well to take another name."

— Jaime relaying Varys's plan, ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:57`)
"""

# (slug, dir, body)
NODES = [
    ("tywins-crossbow", NODES_ARTIFACTS, TYWINS_CROSSBOW),
    ("hands-chain-of-office", NODES_ARTIFACTS, HANDS_CHAIN),
    ("oberyn-spear", NODES_ARTIFACTS, OBERYN_SPEAR),
    ("shae-testifies-against-tyrion-at-trial", NODES_EVENTS, SHAE_TESTIFIES),
    ("varys-smuggles-tyrion-out-of-kings-landing", NODES_EVENTS, VARYS_SMUGGLES),
]


# ════════════════════════════ EDGES ════════════════════════════
# (source, edge_type, target, tier, book, chap_id, line, quote, asserted, verified_or_None, qualifier_or_None)
EDGES_SPEC = [
    # ════ OBJECT — crossbow (4) Tier-1 ════
    ("tywins-crossbow", "WIELDED_IN", "assassination-of-tywin-lannister", 1,
     "asos", "asos-tyrion-11", 259,
     "The crossbow whanged just as Lord Tywin started to rise. The bolt slammed into him above the groin and he sat back down with a grunt.",
     "The crossbow is the instrument of Tywin's killing. WIELDED_IN = artifact -> event.", None, None),
    ("tyrion-lannister", "WIELDS", "tywins-crossbow", 1,
     "asos", "asos-tyrion-11", 211,
     "He climbed up, pulled down the bow and a leather quiver packed with quarrels, jammed a foot into the stirrup, and pushed down until the bowstring cocked.",
     "Tyrion physically takes down, cocks, and fires the crossbow. WIELDS = person -> artifact.", None, None),
    ("tywin-lannister", "KILLED_WITH", "tywins-crossbow", 1,
     "asos", "asos-tyrion-11", 259,
     "The bolt slammed into him above the groin and he sat back down with a grunt. The quarrel had sunk deep, right to the fletching.",
     "Tywin dies of the crossbow bolt. KILLED_WITH = victim -> artifact.", None, None),
    ("tywin-lannister", "OWNS", "tywins-crossbow", 1,
     "asos", "asos-tyrion-11", 225,
     "“The eunuch,” his father decided. “I’ll have his head for this. Is that my crossbow? Put it down.”",
     "Tywin identifies the crossbow as his own (it hung on his bedchamber wall). The Old Lion killed with his own weapon.", None, None),

    # ════ OBJECT — Hand's chain (3) Tier-1 ════
    ("hands-chain-of-office", "WIELDED_IN", "tyrion-kills-shae-in-tywins-bed", 1,
     "asos", "asos-tyrion-11", 209,
     "Tyrion slid a hand under his father’s chain, and twisted. The links tightened, digging into her neck.",
     "The Hand's golden chain is the strangulation instrument. WIELDED_IN = artifact -> event.", None, None),
    ("tyrion-lannister", "WIELDS", "hands-chain-of-office", 1,
     "asos", "asos-tyrion-11", 209,
     "Tyrion slid a hand under his father’s chain, and twisted.",
     "Tyrion takes hold of the chain and uses it as a weapon. WIELDS = person -> artifact.", None, None),
    ("shae", "KILLED_WITH", "hands-chain-of-office", 1,
     "asos", "asos-tyrion-11", 209,
     "The links tightened, digging into her neck. “For hands of gold are always cold, but a woman’s hands are warm,” he said.",
     "Shae is strangled to death with the chain. KILLED_WITH = victim -> artifact.", None, None),

    # ════ OBJECT — Oberyn's spear (4; POISONS + venom WIELDED_IN = pending) ════
    ("oberyn-spear", "WIELDED_IN", "gregor-confesses-and-kills-oberyn", 1,
     "asos", "asos-tyrion-10", 233,
     "Prince Oberyn’s spear flashed like lightning and found the gap in the heavy plate, the joint under the arm. The point punched through mail and boiled leather.",
     "Oberyn's spear is his weapon in the trial by combat and the instrument that wounds Gregor. WIELDED_IN = artifact -> event.", None, None),
    ("oberyn-martell", "WIELDS", "oberyn-spear", 1,
     "asos", "asos-tyrion-10", 119,
     "“Daemon, my spear!” Ser Daemon tossed it to him, and the Red Viper snatched it from the air.",
     "Oberyn calls for his spear and carries it into the combat. WIELDS = person -> artifact.", None, None),
    # (oberyn POISONS gregor + manticore-venom WIELDED_IN DROPPED at fresh-verify S139:
    #  ASOS ch10 leaves the poison unconfirmed — "Oil? Or poison? Tyrion decided that he
    #  would sooner not know"; "manticore" never appears in ASOS. Poison-wiring deferred to
    #  an AFFC/Gregor dip where the venom is named on-page. Spear node prose notes it as canon.)

    # ════ CAUSAL / DYADIC SEAMS (2; was 3 — shae-testifies CAUSES kill dropped below) ════
    ("murder-of-elia-martell-and-rhaegars-children", "MOTIVATES", "oberyn-martell", 1,
     "asos", "asos-tyrion-10", 187,
     "“I am Oberyn Martell, a prince of Dorne,” he said, as the Mountain turned to keep him in sight. “Princess Elia was my sister.”",
     "The marquee cross-arc seam: the murder of Oberyn's sister Elia is why he came to King's Landing, lobbied to be a judge, and agreed to champion Tyrion — to reach Gregor in single combat and extract a confession ('I came to hear you confess', ch10:195). MOTIVATES = event -> character. Wires the Sack-of-KL arc into the Tywin-death arc. (Re-cited ch09:399 -> ch10:187 at fresh-verify for a stronger on-page motive anchor.)",
     "pending-fresh-verify-s139", None),
    ("tywin-lannister", "DECEIVES", "tyrion-lannister", 1,
     "asos", "asos-tyrion-11", 79,
     "She was no whore. I never bought her for you. That was a lie that Father commanded me to tell. Tysha was . . . she was what she seemed to be. A crofter’s daughter, chance met on the road.",
     "Tywin fabricated the story that Tysha was a paid whore and had Jaime sell the lie to Tyrion — a deception sustained for years that, when Jaime reveals it, fires the patricide. DECEIVES = deceiver -> deceived (Tyrion was the one fooled). qualifier by_lie.",
     "pending-fresh-verify-s139", "by_lie"),
    ("tyrion-kills-shae-in-tywins-bed", "ENABLES", "assassination-of-tywin-lannister", 2,
     "asos", "asos-tyrion-11", 211,
     "A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls.",
     "Killing Shae in Tywin's bedchamber put Tyrion inside the Tower of the Hand with the wall-hung crossbow in reach — the instrumental door-opener for the assassination. ENABLES (not CAUSES): Tyrion's free choice to continue to the privy is the proximate agent. The spine already carries the motivational jaime-reveals CAUSES assassination.",
     "pending-fresh-verify-s139", None),

    # ════ TESTIMONY NODE edges (5) ════
    ("shae", "AGENT_IN", "shae-testifies-against-tyrion-at-trial", 1,
     "asos", "asos-tyrion-10", 31,
     "“They plotted it together,” she said, this girl he’d loved. “The Imp and Lady Sansa plotted it after the Young Wolf died.",
     "Shae is the agent of her own (false) testimony. AGENT_IN = executor -> event.", None, None),
    ("shae-testifies-against-tyrion-at-trial", "SUB_BEAT_OF", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-10", 27,
     "No sooner had Tyrion taken his place before the judges than another group of gold cloaks led in Shae.",
     "Shae's testimony is the climactic final-witness beat inside the trial. SUB_BEAT_OF = beat -> parent event.", None, None),
    ("cersei-lannister", "COMMANDS_IN", "shae-testifies-against-tyrion-at-trial", 1,
     "asos", "asos-tyrion-09", 329,
     "“Almost,” said Cersei. “I beg your leave to bring one final witness before you, on the morrow.”",
     "Cersei orchestrated Shae's testimony, holding her back as the climactic 'one final witness'. COMMANDS_IN = orderer who did not personally execute.", None, None),
    ("shae-testifies-against-tyrion-at-trial", "MOTIVATES", "tyrion-lannister", 2,
     "asos", "asos-tyrion-10", 49,
     "“Get this lying whore out of my sight,” said Tyrion, “and I will give you your confession.”",
     "Shae's betrayal is the final intolerable witness that breaks Tyrion and drives his confession-speech + demand for trial by combat. MOTIVATES = event -> character (routes the human choice).",
     "pending-fresh-verify-s139", None),
    # (shae-testifies CAUSES tyrion-kills-shae DROPPED at fresh-verify S139: agency/redundancy —
    #  the MOTIVATES tyrion edge above + the existing spine `jaime-reveals CAUSES tyrion-kills-shae`
    #  already carry the killing's causation; an event->event CAUSES double-routes the human choice.)

    # ════ ESCAPE NODE edges (4) ════
    ("jaime-frees-tyrion-from-the-black-cells", "ENABLES", "varys-smuggles-tyrion-out-of-kings-landing", 2,
     "asos", "asos-tyrion-11", 57,
     "You’re going down into the sewers, and from there to the river. A galley is waiting in the bay.",
     "Jaime freeing Tyrion from the cell is the precondition; Varys's separate smuggling operation (drugged gaolers, septon's disguise, the galley) produces the actual exit. ENABLES preserves Varys's distinct agency.",
     "pending-fresh-verify-s139", None),
    ("varys", "AGENT_IN", "varys-smuggles-tyrion-out-of-kings-landing", 1,
     "asos", "asos-tyrion-11", 153,
     "Varys produced a key. They stepped through into a small round chamber.",
     "Varys personally guides Tyrion through the passages and unlocks the gates. AGENT_IN = executor -> event.", None, None),
    ("tyrion-lannister", "AGENT_IN", "varys-smuggles-tyrion-out-of-kings-landing", 1,
     "asos", "asos-tyrion-11", 57,
     "You’re going down into the sewers, and from there to the river. A galley is waiting in the bay.",
     "Tyrion is the escaping subject who travels the route to the galley. AGENT_IN.", None, None),
    ("varys-smuggles-tyrion-out-of-kings-landing", "LOCATED_AT", "red-keep", 1,
     "asos", "asos-tyrion-11", 153,
     "A light appeared ahead of them, too dim to be daylight, and grew as they hurried toward it.",
     "The escape runs through the dungeons and secret passages beneath the Red Keep. LOCATED_AT = event -> location.", None, None),

    # ════ TRIAL roles — judges + Cersei (3) Tier-1 ════
    ("mace-tyrell", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 15,
     "he has asked Lord Tyrell and Prince Oberyn to sit in judgment with him.",
     "Mace Tyrell is one of the three sitting judges at the trial. PARTICIPATES_IN (judicial/administrative role; Tywin AGENT_IN as the convener already exists).", None, None),
    ("oberyn-martell", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 15,
     "he has asked Lord Tyrell and Prince Oberyn to sit in judgment with him.",
     "Oberyn Martell is one of the three sitting judges (and later Tyrion's champion). PARTICIPATES_IN for the judicial role.", None, None),
    ("cersei-lannister", "COMMANDS_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 329,
     "“Almost,” said Cersei. “I beg your leave to bring one final witness before you, on the morrow.”",
     "Cersei orchestrates the prosecution — assembling and sequencing the witness parade against Tyrion. COMMANDS_IN = orderer.", None, None),

    # ════ COMBAT roles (3) Tier-1 ════
    ("oberyn-martell", "FIGHTS_IN", "gregor-confesses-and-kills-oberyn", 1,
     "asos", "asos-tyrion-10", 75,
     "“He does, my lord.” Prince Oberyn of Dorne rose to his feet. “The dwarf has quite convinced me.”",
     "Oberyn takes the field as Tyrion's champion in the trial by combat. FIGHTS_IN = combatant (his VICTIM_IN already exists).", None, None),
    ("gregor-clegane", "FIGHTS_IN", "gregor-confesses-and-kills-oberyn", 1,
     "asos", "asos-tyrion-10", 169,
     "He looks as though he was chiseled out of rock, standing there. His greatsword was planted in the ground before him, six feet of scarred metal.",
     "Gregor fights as Cersei's champion. FIGHTS_IN = combatant (his AGENT_IN already exists).", None, None),
    ("ellaria-sand", "WITNESS_IN", "gregor-confesses-and-kills-oberyn", 1,
     "asos", "asos-tyrion-10", 247,
     "Ellaria Sand wailed in terror, and Tyrion’s breakfast came boiling back up.",
     "Ellaria is present at the combat, speaks during it, and wails at the moment Gregor crushes Oberyn's skull — text-anchor gate satisfied (she SEES the charged killing). WITNESS_IN.", None, None),

    # ════ TRIAL witness parade (8) Tier-1 — all nodes exist ════
    ("pycelle", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 245,
     "Then they brought forth Grand Maester Pycelle, leaning heavily on a twisted cane and shaking as he walked",
     "Pycelle gives sworn testimony with his jars of poisons, accusing Tyrion of the theft. PARTICIPATES_IN (formal witness).", None, None),
    ("varys", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 321,
     "“Lord Varys,” the herald said, “master of whisperers.”",
     "Varys testifies for a full day with documents — the most damning witness. PARTICIPATES_IN.", None, None),
    ("balon-swann", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 191,
     "the first man ushered in was Ser Balon Swann of the Kingsguard.",
     "Balon Swann is the first sworn witness (he testifies in Tyrion's favor). PARTICIPATES_IN.", None, None),
    ("meryn-trant", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 201,
     "Ser Meryn Trant was pleased to expand on Ser Balon’s account, when he took his place as witness.",
     "Meryn Trant testifies against Tyrion. PARTICIPATES_IN.", None, None),
    ("boros-blount", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 207,
     "Blount himself came next, to echo that sorry tale.",
     "Boros Blount testifies against Tyrion. PARTICIPATES_IN.", None, None),
    ("osmund-kettleblack", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 221,
     "Ser Osmund Kettleblack, a vision of chivalry in immaculate scale armor and white wool cloak, swore that King Joffrey had long known that his uncle Tyrion meant to murder him.",
     "Osmund Kettleblack gives sworn testimony against Tyrion. PARTICIPATES_IN.", None, None),
    ("osney-kettleblack", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 217,
     "Osney and Osfryd told the tale of his supper with Cersei before the Battle of the Blackwater, and of the threats he’d made.",
     "Osney Kettleblack testifies against Tyrion. PARTICIPATES_IN.", None, None),
    ("osfryd-kettleblack", "PARTICIPATES_IN", "trial-of-tyrion-lannister", 1,
     "asos", "asos-tyrion-09", 217,
     "Osney and Osfryd told the tale of his supper with Cersei before the Battle of the Blackwater, and of the threats he’d made.",
     "Osfryd Kettleblack testifies against Tyrion. PARTICIPATES_IN.", None, None),
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
