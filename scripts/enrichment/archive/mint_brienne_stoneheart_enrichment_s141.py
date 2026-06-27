#!/usr/bin/env python3
"""Mint Brienne->Stoneheart enrichment pass 1 (S141) — eighth major-arc enrichment dip.

The last clean L1 arc (Matt S141). The S115 AFFC spine was a 2-edge dead-ended chain
(catelyn-is-killed -> catelyn-rises-as-lady-stoneheart -> brienne-brought-before-lady-
stoneheart, which had 0 outgoing). The character layer was already dense (Brienne 73 edges)
but the EVENT nodes were thin/islanded. This pass builds the OFF-SPINE substrate:

  - THE MARQUEE FIX: de-island `raid-on-saltpans` (it had 0 participant edges — only a
    PART_OF war). Rorge/Biter/Brave-Companions AGENT_IN/ENABLES; LOCATED_AT saltpans; the
    Elder Brother's grave-helm "grievous error" ENABLES; the raid MOTIVATES Brienne's hunt;
    Randyll Tarly DECEIVES the Brotherhood (the counter-rumor); Quincy Cox WITNESS_IN.
  - THE HOUND'S-HELM MISATTRIBUTION ENGINE: new object.artifact `hound-helm` with its chain
    of custody (Sandor OWNS -> grave-cairn -> Rorge LOOTED_BY -> WIELDED_IN Saltpans+inn ->
    Lem LOOTED_BY off the corpse). Rorge in Sandor's helm is why the realm blames the Hound.
  - TWO NEW EVENT HUBS: `ambush-at-crossroads-inn` (Rorge's band attacks the inn; Brienne
    kills Rorge, Biter maims her, Gendry kills Biter; the Brotherhood captures the party ->
    CAUSES brienne-brought-before-lady-stoneheart, forward-wiring the new node into the spine)
    and `fight-at-the-whispers` (the Brave-Companions remnant — Pyg/Timeon/Shagwell; Shagwell
    KILLS Nimble Dick Crabb; Pod stones Shagwell).
  - STONEHEART'S VENGEANCE + CROSS-ARC SEAM: red-wedding MOTIVATES catelyn-stark (the RW arc
    drives the AFFC antagonist); catelyn MOTIVATES lem (her enforcer); tribunal participants
    (lem AGENT_IN, thoros PARTICIPATES_IN); the dead-end fix `brienne-brought-before-lady-
    stoneheart MOTIVATES brienne-tarth` (the sword-or-noose ultimatum -> her screamed word).
  - ELDER-BROTHER REVELATIONS that redirect the whole arc (Arya-not-Sansa; Saltpans-not-Sandor).

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+SUSPECTED+WITNESS /
descriptive-object-depth / existing-node<->existing-node causal-wiring) over the built
cluster. PROPOSE-only lenses -> Opus orchestrator synthesized + LINE-CHECKED every cite via
grep against the AFFC source files -> this mint set.

THE LINE-CHECK / ADJUDICATION CATCHES (orchestrator, vs the lenses):
  - SLUG TRAPS corrected: lenses used `thoros-of-myr`/`septon-meribald`/`nimble-dick-crabb`
    (all non-existent) -> `thoros`/`meribald`/`dick-crabb`. The baseline mis-named the BWB
    Lem as `lem-standfast`; the real Lem Lemoncloak node is `lem` (aliases incl. "The Hound (III)").
  - NOT MINTING Sandor's death: lens 3 proposed `sandor DIED_AT/BURIED_AT quiet-isle`.
    DROPPED — the gravedigger-lives subtext (affc-brienne-06:79, harvested) makes asserting
    Sandor's death an over-read. Deferred to a Hound/Sandor character unit. Kept only the
    Elder Brother's REVELATIONS (which happened on-page regardless of whether Sandor truly died).
  - NOT MINTING `brienne-pod-hyle-hanged` (lens 4 wanted it): asserting the hanging as a
    completed death-event is FALSE (Brienne survives in TWOW). The chapter ends on the
    "screamed a word" cliffhanger. De-dead-ended the Stoneheart node HONESTLY via MOTIVATES
    -> brienne (the ultimatum motivates her choice), not a fabricated death node.
  - DEDUP drops: `gendry KILLS biter` (exists), `thoros SWORN_TO brotherhood` (exists, so no
    MEMBER_OF), `gendry SWORN_TO/VOWS_TO brotherhood` (exists, so no MEMBER_OF),
    `house-frey ... catelyn` already VIOLATES_GUEST_RIGHT (used red-wedding MOTIVATES instead).
  - "Mad Dog of Saltpans" REPUTED_AS dropped (no concept node target) -> noted as an
    alias-add pass-2 item, not forced into a broken-shape edge.

FINAL: 3 new nodes + 40 edges. (verified=pending-fresh-verify on the interpretive
MOTIVATES/ENABLES/DECEIVES/CAUSES/WITNESS/REVEALS edges; Tier-1 structural role edges verified=None.)

NEW NODES (3):
  - hound-helm                (object.artifact) — the misattribution engine
  - ambush-at-crossroads-inn  (event.battle)    — the AFFC inn climax; CAUSES the tribunal
  - fight-at-the-whispers      (event.battle)    — the Brave-Companions remnant sub-arc

Safeguards mirror mint_cersei_downfall_enrichment_s140.py: backup, re-run guard, slug
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-brienne-stoneheart-enrichment-2026-06-24.jsonl"

RUN_ID = "brienne-stoneheart-enrichment-s141"
PRODUCED_AT = "2026-06-24T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "hound-helm",
    "ambush-at-crossroads-inn",
    "fight-at-the-whispers",
}


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-brienne-stoneheart-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

HOUND_HELM = """\
---
name: "The Hound's helm"
type: object.artifact
slug: hound-helm
aliases: ["the Hound's helm", "the snarling dog helm", "the dog's-head helm", "the dog's head greathelm"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s141-brienne-stoneheart-enrich
node_version: 1
evidence_chapters:
  - AFFC Brienne VI
  - AFFC Brienne VII
  - AFFC Brienne VIII
---

## Identity

[Sandor Clegane](sandor-clegane)'s distinctive steel greathelm, forged in the shape of a
snarling dog's head with bared teeth — the signature of "the Hound." After Sandor is
gravely wounded and (per the Elder Brother) dies on the [Quiet Isle](quiet-isle), the
[Elder Brother](elder-brother-quiet-isle) sets the helm atop his grave-cairn as a marker —
"a grievous error." Some other wayfarer — [Rorge](rorge), fleeing Harrenhal with the
[Brave Companions](brave-companions) remnant — finds and claims it, and wears it to sack
[Saltpans](saltpans). Because the realm recognises the helm, the atrocity is misattributed
to Sandor ("the Mad Dog of Saltpans"), and his accused-murder count rises from twelve to
twenty. [Brienne](brienne-tarth) kills Rorge at the crossroads inn while he wears it
(her face mashed against the cold wet dog's-head steel); [Lem Lemoncloak](lem) then strips
the helm off Rorge's corpse and wears it himself — becoming, the wiki notes, "the Hound (III)."
The helm is the misattribution engine of the entire AFFC Brienne arc.

## Edges
(Edges in `graph/edges/edges.jsonl`, S141 Brienne-Stoneheart enrichment. [Sandor](sandor-clegane)
OWNS; LOOTED_BY [Rorge](rorge); WIELDED_IN [the Saltpans raid](raid-on-saltpans) +
[the inn ambush](ambush-at-crossroads-inn); LOOTED_BY [Lem](lem) off Rorge's corpse.)

## Quotes

> I covered him with stones to keep the carrion eaters from digging up his flesh, and set his helm atop the cairn to mark his final resting place. That was a grievous error. Some other wayfarer found my marker and claimed it for himself.

— The Elder Brother, AFFC Brienne VI (`sources/chapters/affc/affc-brienne-06.md:185`)

> beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling.

— AFFC Brienne VII (`sources/chapters/affc/affc-brienne-07.md:265`)

> It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse.

— Brienne to Lem, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:215`)
"""

AMBUSH_INN = """\
---
slug: ambush-at-crossroads-inn
type: event.battle
name: "Ambush at the crossroads inn"
aliases: ["the crossroads inn fight", "Rorge's attack on the inn", "Brienne kills Rorge", "the fight at the inn"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s141-brienne-stoneheart-enrich
node_version: 1
evidence_chapters:
  - AFFC Brienne VII
  - AFFC Brienne VIII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
---

# Ambush at the crossroads inn

The climax of the AFFC Brienne arc. [Rorge](rorge)'s band of fleeing
[Brave Companions](brave-companions) — Rorge wearing [the Hound's helm](hound-helm) — ride
on the [crossroads inn](inn-at-the-crossroads) in a thunderstorm to rape and rob. [Brienne](brienne-tarth)
steps into the rain with [Oathkeeper](oathkeeper) and kills Rorge clean (whispering
"Sapphires" as he dies behind the dog's-head helm), but [Biter](biter) falls on her like an
avalanche, maims her, and begins eating her face before [Gendry](gendry) drives a spearpoint
through the back of his neck. In the aftermath the [Brotherhood without banners](brotherhood-without-banners)
seizes the survivors — Brienne, [Podrick](podrick-payne), and [Hyle Hunt](hyle-hunt) — and
hauls them off to answer to Lady Stoneheart. The capture is the direct precondition of
[Brienne being brought before Lady Stoneheart](brienne-brought-before-lady-stoneheart).

## Edges
(Edges in `graph/edges/edges.jsonl`, S141 Brienne-Stoneheart enrichment. LOCATED_AT
[the inn](inn-at-the-crossroads); [Rorge](rorge)+[Biter](biter)+[Brienne](brienne-tarth)+
[Gendry](gendry) AGENT_IN; [Willow](willow-heddle) AGENT_IN; [Oathkeeper](oathkeeper)+
[the Hound's helm](hound-helm) WIELDED_IN; [Brienne](brienne-tarth)+[Hyle](hyle-hunt) VICTIM_IN;
CAUSES [Brienne brought before Lady Stoneheart](brienne-brought-before-lady-stoneheart).)

## Quotes

> She stepped out into the rain, Oathkeeper in hand. "Leave her be. If you want to rape someone, try me."

— AFFC Brienne VII (`sources/chapters/affc/affc-brienne-07.md:275`)

> His headlong charge brought him right onto her point, and Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back, rasping as it scraped along his spine.

— Brienne kills Rorge, AFFC Brienne VII (`sources/chapters/affc/affc-brienne-07.md:293`)

> "He's dead. Gendry shoved a spearpoint through the back of his neck. Drink, m'lady, or I'll pour it down your throat."

— Long Jeyne Heddle, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:53`)
"""

FIGHT_WHISPERS = """\
---
slug: fight-at-the-whispers
type: event.battle
name: "Fight at the Whispers"
aliases: ["the fight at the Whispers", "Brienne's fight with the Brave Companions remnant", "Nimble Dick's death"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s141-brienne-stoneheart-enrich
node_version: 1
evidence_chapters:
  - AFFC Brienne IV
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
---

# Fight at the Whispers

At the ruined cliff-top castle of [the Whispers](whispers) on Crackclaw Point, three
fugitive [Brave Companions](brave-companions) — [Shagwell](shagwell), [Timeon](timeon), and
[Pyg](pyg) — ambush [Brienne](brienne-tarth) and her guide [Nimble Dick Crabb](dick-crabb).
Shagwell crushes Crabb's knee and then his face with a triple morningstar, killing him;
Brienne, with [Oathkeeper](oathkeeper) "alive in her hands," kills Pyg and Timeon, and —
after [Podrick](podrick-payne) stones Shagwell from atop the fallen wall — finishes Shagwell
too. Timeon's taunt that the Hound rode off with "the Stark girl" is part of what later sends
Brienne hunting Sandor. The bloodied close of the Brave Companions as a fighting force.

## Edges
(Edges in `graph/edges/edges.jsonl`, S141 Brienne-Stoneheart enrichment. LOCATED_AT
[the Whispers](whispers); [Brienne](brienne-tarth)+[Shagwell](shagwell)+[Pyg](pyg)+
[Timeon](timeon)+[Podrick](podrick-payne) AGENT_IN; [Oathkeeper](oathkeeper) WIELDED_IN;
[Dick Crabb](dick-crabb) VICTIM_IN + KILLED_BY [Shagwell](shagwell).)

## Quotes

> Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face. There was a sickening crunch.

— AFFC Brienne IV (`sources/chapters/affc/affc-brienne-04.md:263`)

> Oathkeeper was alive in her hands. She had never been so quick. The blade became a grey blur.

— AFFC Brienne IV (`sources/chapters/affc/affc-brienne-04.md:319`)

> Podrick had climbed the fallen wall and was standing amongst the ivy glowering, a fresh rock in his hand. "I told you I could fight!" he shouted down.

— AFFC Brienne IV (`sources/chapters/affc/affc-brienne-04.md:325`)
"""

NODES = [
    ("hound-helm", NODES_ARTIFACTS, HOUND_HELM),
    ("ambush-at-crossroads-inn", NODES_EVENTS, AMBUSH_INN),
    ("fight-at-the-whispers", NODES_EVENTS, FIGHT_WHISPERS),
]

# ════════════════════════════ EDGES ════════════════════════════
# (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified, qualifier)

EDGES_SPEC = [
    # ════ DE-ISLAND raid-on-saltpans — the marquee fix (9) ════
    ("rorge", "AGENT_IN", "raid-on-saltpans", 1,
     "affc", "affc-brienne-08", 215,
     "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse.",
     "Brienne names Rorge as the Saltpans raider (he wore Sandor's helm). AGENT_IN = physical actor. The node previously had 0 participant edges.", None, None),
    ("biter", "AGENT_IN", "raid-on-saltpans", 2,
     "affc", "affc-brienne-06", 131,
     "her breasts had been torn and chewed and eaten, as if by some . . . cruel beast.",
     "The Elder Brother's account of a Saltpans victim eaten alive matches Biter's signature cannibalism (he is Rorge's constant companion per the raid node body). Tier-2: the 'cruel beast' identification is strong inference, not a named cite.",
     "pending-fresh-verify-s141", None),
    ("brave-companions", "ENABLES", "raid-on-saltpans", 1,
     "affc", "affc-brienne-04", 273,
     "We all went our own ways, after we left Harrenhal. Urswyck and his lot rode south for Oldtown. Rorge thought he might slip out at Saltpans.",
     "The Brave Companions' dissolution at Harrenhal dispersed the remnant; Rorge's band fled toward Saltpans seeking a ship, putting them in position to sack it. ENABLES = distal door-opener.",
     "pending-fresh-verify-s141", None),
    ("capture-of-harrenhal", "ENABLES", "raid-on-saltpans", 2,
     "affc", "affc-brienne-04", 273,
     "We all went our own ways, after we left Harrenhal.",
     "The Lannister recapture of Harrenhal (the Mountain killing Hoat) ended the Brave Companions' hold and scattered them — without that dissolution there is no Rorge-band at Saltpans. Cross-arc seam (Harrenhal/Lannister arc -> Brienne arc). Tier-2: the link is wiki-corroborated; the AFFC quote names the leaving-of-Harrenhal but not the capture-event by name.",
     "pending-fresh-verify-s141", None),
    ("raid-on-saltpans", "LOCATED_AT", "saltpans", 1,
     "affc", "affc-brienne-06", 131,
     "They burned everything at Saltpans, save the castle.",
     "Event location is definitional; the islanded node had no LOCATED_AT. LOCATED_AT = event -> place.", None, None),
    ("elder-brother-quiet-isle", "ENABLES", "raid-on-saltpans", 1,
     "affc", "affc-brienne-06", 185,
     "set his helm atop the cairn to mark his final resting place. That was a grievous error.",
     "The Elder Brother's placing of Sandor's helm on the grave-cairn (which Rorge then found and wore) is the inadvertent precondition for the misattributed raid — he himself calls it 'a grievous error.' ENABLES = accidental door-opener, not CAUSES.",
     "pending-fresh-verify-s141", None),
    ("raid-on-saltpans", "MOTIVATES", "brienne-tarth", 1,
     "affc", "affc-brienne-05", 127,
     "Sandor Clegane was last seen in Saltpans, the day of the raid. Afterward he rode west, along the Trident.",
     "The Saltpans raid (falsely attributed to the Hound) pivots Brienne's quest toward hunting Sandor along the Trident. MOTIVATES = event -> character (motive moves a person).",
     "pending-fresh-verify-s141", None),
    ("randyll-tarly", "DECEIVES", "brotherhood-without-banners", 1,
     "affc", "affc-brienne-05", 135,
     "Lord Randyll is putting it about that they did in hopes of turning the commons against Beric and his brotherhood.",
     "Tarly deliberately spreads a false rumor blaming the Saltpans raid on Beric's Brotherhood to strip their popular support. DECEIVES = deliberate false narrative aimed at the organization (he hunts the Hound simultaneously, so he knows it's false).",
     "pending-fresh-verify-s141", None),
    ("quincy-cox", "WITNESS_IN", "raid-on-saltpans", 2,
     "affc", "affc-brienne-06", 131,
     "her worst curses were not for the men who had raped her, nor the monster who devoured her living flesh, but for Ser Quincy Cox, who barred his gates when the outlaws entered the town and sat safe behind stone walls as his people screamed and died.",
     "Cox watched the raid from his holdfast battlements (per the dying woman's curse + the raid node body 'tells what saw from the battlements') and did nothing. WITNESS_IN = load-bearing perceiver. Tier-2: text-anchor is the survivor's curse, not Cox's own POV.",
     "pending-fresh-verify-s141", None),

    # ════ THE HOUND'S-HELM chain of custody (5) ════
    ("sandor-clegane", "OWNS", "hound-helm", 1,
     "affc", "affc-brienne-06", 185,
     "I covered him with stones to keep the carrion eaters from digging up his flesh, and set his helm atop the cairn to mark his final resting place.",
     "The dog's-head greathelm is Sandor's signature piece; the Elder Brother marks his grave with it. OWNS = possessor -> artifact.", None, None),
    ("hound-helm", "LOOTED_BY", "rorge", 1,
     "affc", "affc-brienne-08", 215,
     "He took the helm from Clegane's grave, and you stole it off his corpse.",
     "Rorge takes the helm off Sandor's grave-cairn. LOOTED_BY = artifact -> new holder (the transactional taking).", None, None),
    ("hound-helm", "WIELDED_IN", "raid-on-saltpans", 2,
     "affc", "affc-brienne-06", 185,
     "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous.",
     "Rorge wore the helm during the Saltpans raid, which is precisely what made the realm misattribute it to Sandor. WIELDED_IN = artifact -> event (instrument of the misattribution). Tier-2: the wearing-at-Saltpans is established by the misID, not shown on-page.",
     "pending-fresh-verify-s141", None),
    ("hound-helm", "WIELDED_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-07", 265,
     "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling.",
     "Rorge wears the dog's-head helm leading the inn attack (Brienne's face is mashed against it as she kills him). WIELDED_IN = artifact -> event.", None, None),
    ("hound-helm", "LOOTED_BY", "lem", 1,
     "affc", "affc-brienne-08", 215,
     "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse.",
     "Lem Lemoncloak strips the helm off Rorge's corpse after the inn fight and wears it himself. LOOTED_BY = artifact -> new holder. (`lem` = Lem Lemoncloak, aliases incl. 'The Hound (III)'.)", None, None),

    # ════ THE INN AMBUSH — ambush-at-crossroads-inn (10) ════
    ("ambush-at-crossroads-inn", "LOCATED_AT", "inn-at-the-crossroads", 1,
     "affc", "affc-brienne-07", 85,
     "The inn's yard was a sea of brown mud that sucked at the hooves of the horses.",
     "The ambush takes place in the crossroads inn's yard. LOCATED_AT = event -> place.", None, None),
    ("rorge", "AGENT_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-07", 265,
     "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling.",
     "Rorge leads the seven-rider band against the inn, wearing the Hound's helm. AGENT_IN.", None, None),
    ("biter", "AGENT_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-07", 295,
     ". . . and Biter crashed into her, shrieking.",
     "Biter falls on Brienne after she kills Rorge, mauling and biting her. AGENT_IN.", None, None),
    ("brienne-tarth", "AGENT_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-07", 275,
     "She stepped out into the rain, Oathkeeper in hand. “Leave her be. If you want to rape someone, try me.”",
     "Brienne initiates combat to protect Willow and the children, killing Rorge. AGENT_IN.", None, None),
    ("gendry", "AGENT_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-08", 53,
     "He's dead. Gendry shoved a spearpoint through the back of his neck.",
     "Gendry kills Biter, resolving the threat that was killing Brienne. AGENT_IN. (The dyadic `gendry KILLS biter` already exists; this is the event-role edge.)", None, None),
    ("oathkeeper", "WIELDED_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-07", 293,
     "Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back, rasping as it scraped along his spine.",
     "Oathkeeper is the instrument Brienne uses to kill Rorge at the inn. WIELDED_IN = artifact -> event.", None, None),
    ("brienne-tarth", "VICTIM_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-07", 305,
     "She saw his teeth, yellow and crooked, filed into points. When they closed on the soft meat of her cheek, she hardly felt it.",
     "Brienne is mauled (face bitten, arm broken) by Biter and left near death. VICTIM_IN complements her AGENT_IN — she fights AND is grievously wounded.", None, None),
    ("willow-heddle", "AGENT_IN", "ambush-at-crossroads-inn", 2,
     "affc", "affc-brienne-07", 271,
     "The door to the inn banged open. Willow stepped out into the rain, a crossbow in her hands.",
     "Willow confronts the raiders with a crossbow, defending the inn and the orphan children. AGENT_IN. Tier-2: she is driven back before loosing.",
     "pending-fresh-verify-s141", None),
    ("hyle-hunt", "VICTIM_IN", "ambush-at-crossroads-inn", 1,
     "affc", "affc-brienne-08", 279,
     "Hyle Hunt had been beaten so badly that his face was swollen almost beyond recognition.",
     "Hyle fights in the skirmish and is beaten and captured by the Brotherhood. VICTIM_IN.", None, None),
    ("ambush-at-crossroads-inn", "CAUSES", "brienne-brought-before-lady-stoneheart", 1,
     "affc", "affc-brienne-08", 71,
     "“M'lady means for you to answer for your crimes.”",
     "The Brotherhood's capture of the survivors at the inn leads directly to Brienne being hauled before Lady Stoneheart. CAUSES = distinct downstream event; forward-wires the new node into the spine.",
     "pending-fresh-verify-s141", None),

    # ════ THE WHISPERS FIGHT — fight-at-the-whispers (9) ════
    ("fight-at-the-whispers", "LOCATED_AT", "whispers", 1,
     "affc", "affc-brienne-04", 173,
     "“The Whispers,” said Nimble Dick. “Have a listen. You can hear the heads.”",
     "The fight occurs at the ruined castle of the Whispers on Crackclaw Point. LOCATED_AT = event -> place.", None, None),
    ("brienne-tarth", "AGENT_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 319,
     "Oathkeeper was alive in her hands. She had never been so quick. The blade became a grey blur.",
     "Brienne kills Pyg, Timeon, and Shagwell at the Whispers. AGENT_IN. (The dyadic KILLS edges already exist; this is the event-role edge.)", None, None),
    ("shagwell", "AGENT_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 255,
     "He swung it hard and low, and one of Crabb's knees exploded in a spray of blood and bone.",
     "Shagwell ambushes from the weirwood and kills Nimble Dick. AGENT_IN.", None, None),
    ("pyg", "AGENT_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 247,
     "From the bushes slid a man, so caked with dirt that he looked as if he had sprouted from the earth.",
     "Pyg attacks Brienne with a broken sword at the Whispers. AGENT_IN.", None, None),
    ("timeon", "AGENT_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 273,
     "The Dornishman hefted his spear.",
     "Timeon, the Dornish Brave Companion, fights Brienne with his spear at the Whispers. AGENT_IN.", None, None),
    ("dick-crabb", "VICTIM_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 263,
     "Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face. There was a sickening crunch.",
     "Nimble Dick Crabb is killed by Shagwell at the Whispers. VICTIM_IN.", None, None),
    ("dick-crabb", "KILLED_BY", "shagwell", 1,
     "affc", "affc-brienne-04", 263,
     "Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face. There was a sickening crunch.",
     "Shagwell crushes Crabb's face with the triple morningstar. KILLED_BY = victim -> killer (dyadic).", None, None),
    ("podrick-payne", "AGENT_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 325,
     "Podrick had climbed the fallen wall and was standing amongst the ivy glowering, a fresh rock in his hand. “I told you I could fight!” he shouted down.",
     "Podrick stones Shagwell from the wall, stunning him so Brienne can finish him. AGENT_IN (active combatant, not mere witness).", None, None),
    ("oathkeeper", "WIELDED_IN", "fight-at-the-whispers", 1,
     "affc", "affc-brienne-04", 319,
     "Oathkeeper was alive in her hands. She had never been so quick. The blade became a grey blur.",
     "Brienne wields Oathkeeper to kill Pyg and Timeon at the Whispers. WIELDED_IN = artifact -> event.", None, None),

    # ════ STONEHEART VENGEANCE + CROSS-ARC SEAM + DEAD-END FIX (5) ════
    ("red-wedding", "MOTIVATES", "catelyn-stark", 1,
     "affc", "affc-brienne-08", 323,
     "She wants to feed the crows, like they did at the Red Wedding. Freys and Boltons, aye.",
     "The Red Wedding's slaughter is the explicit motive source for all of Lady Stoneheart's vengeance. MOTIVATES = event -> character. Cross-arc seam: the ASOS Red Wedding arc drives the AFFC Brienne arc's antagonist.",
     "pending-fresh-verify-s141", None),
    ("catelyn-stark", "MOTIVATES", "lem", 2,
     "affc", "affc-brienne-08", 323,
     "She wants to feed the crows, like they did at the Red Wedding. Freys and Boltons, aye.",
     "Lady Stoneheart's vengeance drives Lem Lemoncloak, her operational enforcer who runs the hangings and speaks her will. MOTIVATES = character -> character. Tier-2: Lem relays her wants; her motivating role is interpretive.",
     "pending-fresh-verify-s141", None),
    ("lem", "AGENT_IN", "brienne-brought-before-lady-stoneheart", 1,
     "affc", "affc-brienne-08", 333,
     "“As you command, m'lady,” said the big man.",
     "Lem (the big man in the yellow cloak, now wearing the Hound's helm) carries out Stoneheart's 'Hang them' order. AGENT_IN.", None, None),
    ("thoros", "PARTICIPATES_IN", "brienne-brought-before-lady-stoneheart", 1,
     "affc", "affc-brienne-08", 259,
     "Thoros of Myr drew a parchment from his sleeve, and put it down next to the sword. “It bears the boy king's seal and says the bearer is about his business.”",
     "Thoros presents the Lannister letter as evidence against Brienne at the tribunal. PARTICIPATES_IN = non-combat involvement in the event.", None, None),
    ("brienne-brought-before-lady-stoneheart", "MOTIVATES", "brienne-tarth", 2,
     "affc", "affc-brienne-08", 327,
     "She says that you must choose. Take the sword and slay the Kingslayer, or be hanged for a betrayer. The sword or the noose, she says. Choose, she says. Choose.",
     "The sword-or-noose ultimatum forces Brienne's choice and her screamed word that ends the chapter. MOTIVATES = event -> character; the honest de-dead-end of the previously 0-outgoing tribunal node, WITHOUT asserting the cliffhanger's resolution (no fabricated hanging-death node).",
     "pending-fresh-verify-s141", None),

    # ════ ELDER-BROTHER REVELATIONS — arc-redirecting (2) ════
    ("elder-brother-quiet-isle", "REVEALS_TO", "brienne-tarth", 1,
     "affc", "affc-brienne-06", 169,
     "You are chasing the wrong wolf, my lady. Eddard Stark had two daughters. It was the other one that Sandor Clegane made off with, the younger one.",
     "The Elder Brother reveals it was Arya, not Sansa, with the Hound — redirecting Brienne's search. REVEALS_TO = revealer -> recipient.", None, None),
    ("elder-brother-quiet-isle", "REVEALS_TO", "brienne-tarth", 1,
     "affc", "affc-brienne-06", 185,
     "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous.",
     "The Elder Brother clears Sandor of the Saltpans atrocity, exposing the helm-driven misattribution. REVEALS_TO = revealer -> recipient. (Records the revelation, which happened on-page regardless of the gravedigger-lives subtext — no claim about Sandor's actual death is minted.)", None, None),
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
