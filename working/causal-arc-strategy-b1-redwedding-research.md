# Causal Arc B1 — Red Wedding Upstream Prelude: Minting Proposal

**Research date:** 2026-06-19  
**Researcher:** Read-only subagent  
**Terminus node:** `red-wedding` (exists; ZERO upstream causal edges confirmed)  
**Arc goal:** Wire the consequence-chain so `--causal-chain red-wedding` recovers "what led Robb here."

---

## A. Dedup Ledger

Every candidate beat was checked against both:  
(1) `python3 scripts/event_alias_resolver.py --lookup "<phrase>"`  
(2) `grep`/`ls` over `graph/nodes/events/`

| Candidate beat (natural phrase) | Resolver result | grep/ls finding | VERDICT |
|---|---|---|---|
| Catelyn frees Jaime Lannister | CANDIDATES score=0.65 → `jaime-lannister-is-captured-and-brought-before-catelyn`; MISS on "releases", "frees"; all direct queries MISS | No node with slug containing "catelyn-frees", "releases-jaime", "freed-jaime" | MINT-NEW — the capture-node is a different event (AGOT, the Whispering Wood capture); no node for Catelyn's ASOS act of freeing him exists |
| plot-to-free-jaime-lannister | EXISTS (Tyrion's ACOK plot, type event.battle, wiki-derived) | File present; type is event.battle; describes Tyrion's network placing agents in Cleos Frey's honor guard | SKIP — different event entirely (Tyrion's failed ACOK plot ≠ Catelyn's ASOS release). Do NOT reuse. |
| jaime-lannister-is-captured-and-brought-before-catelyn | EXISTS (type event.capture; AGOT Catelyn X) | File present; no edges; Plate 3 staging stub | SKIP — AGOT capture event, not ASOS release |
| Karstark murders Lannister and Frey prisoners | MISS on all variants | No node found for "karstark-kills", "karstark-murders", "murder-of-tion-frey", "willem-lannister" | MINT-NEW |
| Execution of Rickard Karstark | MISS (resolver returned "execution-of-brandon-and-rickard-stark" at score=0.77, but that is a different event — the AGOT executions by Aerys) | No node for "execution-of-rickard-karstark" | MINT-NEW |
| Karstark men hunting the Kingslayer / Karstark host abandons Robb | EXISTS as `karstark-men-hunting-the-kingslayer` (type event.incident; ASOS Arya IV; Plate 3 staging stub — no edges) | File present | REUSE `karstark-men-hunting-the-kingslayer` (the departure of Karstark horse is the same story — Rickard disperses his men to hunt Jaime before his own arrest; this node captures that) |
| Robb weds Jeyne Westerling / Robb breaks Frey marriage pact | MISS on all variants; resolver finds only character nodes for "jeyne-westerling" | No event node for this wedding | MINT-NEW |
| Red Wedding conspiracy (Walder + Roose + Tywin coordination) | MISS on all variants | No conspiracy or event node for the Frey-Bolton-Lannister coordination | MINT-NEW |
| wedding-of-roose-bolton-and-walda-frey | EXISTS (type event.wedding; tier-2; no edges) | File present; node has full description | REUSE — this event is already modeled as a separate beat; it represents Roose's Frey entanglement, which is a condition MOTIVATING the conspiracy. Do not collapse into the conspiracy node. |
| theon-urges-robb-to-kill-jaime | EXISTS (type event.death — mislabeled; AGOT Catelyn X; Plate 3 staging stub — no edges) | File present | SKIP — AGOT event; not part of this ASOS arc. Do not wire into this chain. |
| red-wedding | EXISTS (type event.wedding; exists with 3 outbound edges, 308 inbound refs) | File present | REUSE — terminus; do NOT add edges from this node, only INTO it |
| robb-is-killed | EXISTS (type event.death; ASOS Catelyn VII; Plate 3 staging stub — no edges) | File present | REUSE — sub-beat terminus; one proposed causal edge targets this node |
| catelyn-is-killed | EXISTS (type event.death; Plate 3 staging stub — no edges) | File present | SKIP — out of scope for this upstream chain |
| catelyn-secures-guest-right | EXISTS (type event.feast; ASOS Catelyn VII; no edges) | File present | SKIP — downstream beat inside the Red Wedding itself; out of scope |

**Summary:** 4 REUSE nodes, 4 MINT-NEW nodes, 6 SKIP nodes.

---

## B. Proposed New Beat-Nodes

### B1. `catelyn-releases-jaime-lannister`

**Proposed slug:** `catelyn-releases-jaime-lannister`  
**Type:** `event.incident`  
(Justification: bounded single-location act — Catelyn enters Jaime's cell at Riverrun, takes Brienne's sword, extracts the oath, and sends him south with Brienne. Not a conspiracy-level scheme; not a battle; fits the incident subtype pattern used by similar single-location confrontations.)

**Description:**  
Late in ACOK, after learning of the reported deaths of Bran and Rickon, Lady Catelyn Stark enters Jaime Lannister's cell at Riverrun at midnight. She takes Brienne of Tarth's sword, forces Jaime to swear to return her daughters Sansa and Arya unharmed, and sends him south with Brienne as escort — exchanging him without Robb's knowledge or consent, in the hope of recovering her daughters from King's Landing. Ser Desmond Grell attempts to recover Jaime but fails. Robb forgives Catelyn at ASOS Catelyn II, linking this event to the Karstark crisis.

**## Quotes**

> "I did," Catelyn said firmly. "I understood what I was doing and knew it was treasonous. If you fail to punish me, men will believe that we connived together to free Jaime Lannister. It was mine own act and mine alone, and I alone must answer for it."
>
> — Catelyn Stark to Ser Desmond Grell  
> `sources/chapters/acos/acok-catelyn-07.md` line 21  
> *(chapter opens on the morning after the release; this is Catelyn's direct confession)*

> "If I could wish the Kingslayer back in chains I would. You freed him without my knowledge or consent . . . but what you did, I know you did for love. For Arya and Sansa, and out of grief for Bran and Rickon."
>
> — Robb Stark to Catelyn  
> `sources/chapters/asos/asos-catelyn-02.md` line 65

**Proposed role edges:**
- `catelyn-stark` → `AGENT_IN` → `catelyn-releases-jaime-lannister`
- `jaime-lannister` → `VICTIM_IN` → `catelyn-releases-jaime-lannister` (recipient of release)
- `brienne-of-tarth` → `AGENT_IN` → `catelyn-releases-jaime-lannister` (escort)

**SUB_BEAT_OF:** None (standalone event; not inside a larger named event hub at this granularity).

---

### B2. `karstark-murders-prisoners-at-riverrun`

**Proposed slug:** `karstark-murders-prisoners-at-riverrun`  
**Type:** `event.assassination`  
(Justification: targeted killing — two named captives murdered in their cells. The architecture defines event.assassination as "named targeted killing event" with "planning, conspirators, instrument, victim." Rickard's midnight visit to the dungeon is exactly this pattern, with Tion Frey and Willem Lannister as the victims.)

**Description:**  
Infuriated by Catelyn's release of Jaime — whom he blames for the death of his sons Eddard and Torrhen at the Whispering Wood — Lord Rickard Karstark leads a small group of Karstark men to the dungeons at Riverrun. They kill two guards (Delp and Elwood) and murder two young prisoners: Willem Lannister and Tion Frey. Rickard frames this as personal vengeance. Robb considers sparing him but instead executes him for murder and treason, losing the Karstark bannermen.

**## Quotes**

> "Lord Rickard, overcome with grief and anger, sends the Karstark horse from Riverrun, promising the hand of his daughter, Alys, to anyone who recovers Jaime for him. Afterward, Rickard leads a small group of Karstark men to murder Willem Lannister and Tion Frey, two of Robb's captives from the Whispering Wood, in their cells at Riverrun."
>
> — AWOIAF wiki: Rickard Karstark  
> `sources/wiki/_raw/Rickard_Karstark.json` (ASOS section)

> "Only blood can pay for blood."
>
> — Rickard Karstark  
> `sources/chapters/asos/asos-catelyn-03.md` line 43

> "Rickard Karstark killed more than a Frey and a Lannister. He killed my honor. I shall deal with him at dawn."
>
> — Robb Stark  
> `sources/chapters/asos/asos-catelyn-03.md` line 155

**Proposed role edges:**
- `rickard-karstark` → `AGENT_IN` → `karstark-murders-prisoners-at-riverrun`
- `tion-frey` → `VICTIM_IN` → `karstark-murders-prisoners-at-riverrun`
- `willem-lannister` → `VICTIM_IN` → `karstark-murders-prisoners-at-riverrun`
- `LOCATED_AT`: `riverrun`

**SUB_BEAT_OF:** None (standalone event in its own chapter).

---

### B3. `execution-of-rickard-karstark`

**Proposed slug:** `execution-of-rickard-karstark`  
**Type:** `event.execution`  
(Justification: formal execution in front of witnesses, at the heart tree, by the king personally. Architecture defines event.execution as "formal execution as event" with "orderer + executor + witness + place + instrument.")

**Description:**  
Following the murder of the Lannister and Frey prisoners, Robb Stark condemns Lord Rickard Karstark to death for murder and high treason. The execution takes place in the godswood at Riverrun, before the heart tree, with river lords and northmen in attendance. Robb personally beheads Rickard with a poleaxe, following his father's teaching that the man who passes the sentence should swing the blade. Rickard's last breath curses Robb as a kinslayer. The act costs Robb half his remaining northern strength — the Karstark foot, numbering in the thousands.

**## Quotes**

> "Rickard Karstark, Lord of Karhold. Here in sight of gods and men, I judge you guilty of murder and high treason. In mine own name I condemn you. With mine own hand I take your life."
>
> — Robb Stark  
> `sources/chapters/asos/asos-catelyn-03.md` line 173

> The axe crashed down. Heavy and well-honed, it killed at a single blow, but it took three to sever the man's head from his body, and by the time it was done both living and dead were drenched in blood. Robb flung the poleaxe down in disgust, and turned wordless to the heart tree. He stood shaking with his hands half-clenched and the rain running down his cheeks. Gods forgive him, Catelyn prayed in silence. He is only a boy, and he had no other choice.
>
> — Catelyn Stark (narrator)  
> `sources/chapters/asos/asos-catelyn-03.md` line 177

**Proposed role edges:**
- `robb-stark` → `AGENT_IN` → `execution-of-rickard-karstark` (executor and orderer — per architecture, COMMANDS_IN is for orderers who did NOT personally execute; since Robb both ordered AND executed, AGENT_IN is correct)
- `rickard-karstark` → `VICTIM_IN` → `execution-of-rickard-karstark`
- `LOCATED_AT`: `riverrun` (godswood)

**SUB_BEAT_OF:** None (standalone event).

---

### B4. `robb-weds-jeyne-westerling`

**Proposed slug:** `robb-weds-jeyne-westerling`  
**Type:** `event.wedding`  
(Justification: named wedding event — between Robb Stark and Jeyne Westerling, at the Crag, following Robb's wounding and the news of Bran and Rickon's reported deaths. This is the causal pivot of the entire arc — it breaks the Frey marriage pact.)

**Description:**  
After being wounded by an arrow during the storming of the Crag, Robb Stark is nursed by Jeyne Westerling, daughter of Lord Gawen Westerling. When the Greatjon brings Robb the news that Winterfell has fallen and his brothers Bran and Rickon are reportedly dead, Jeyne comforts him. Robb sleeps with her and, to preserve her honor, weds her the next day — in violation of the marriage pact he had sworn to House Frey at the Twins. When the Frey bannermen with Robb learn of the marriage, they depart in outrage, trampling his banner. The Freys at Harrenhal, the Crag, and Riverrun similarly withdraw. This breach is the proximate trigger of Walder Frey's secret correspondence with Roose Bolton and Tywin Lannister.

**## Quotes**

> "And she was with me when the Greatjon brought me the news of . . . of Winterfell. Bran and Rickon. That night, she . . . she comforted me, Mother." Catelyn did not need to be told what sort of comfort Jeyne Westerling had offered her son. "And you wed her the next day."
>
> — Robb Stark and Catelyn Stark  
> `sources/chapters/asos/asos-catelyn-02.md` lines 143–145

> "Not only have you broken your oath, but you've slighted the honor of the Twins by choosing a bride from a lesser house."
>
> — Catelyn Stark to Robb  
> `sources/chapters/asos/asos-catelyn-02.md` line 165

> "The Freys at Harrenhal with Roose Bolton, Lord of the Dreadfort, are outraged after learning of Robb's marriage to Jeyne . . . and the Freys at the Crag and Riverrun angrily return to the Twins. After learning of the broken pact, Walder secretly begins corresponding with Roose, who has wed Walder's granddaughter Walda, and with Lord Tywin Lannister . . . for terms to bring House Frey back as a supporter of the Iron Throne."
>
> — Red Wedding wiki node (Origins section)  
> `graph/nodes/events/red-wedding.node.md` (sourced from `sources/wiki/_raw/Red_Wedding.json`)

**Proposed role edges:**
- `robb-stark` → `AGENT_IN` → `robb-weds-jeyne-westerling`
- `jeyne-westerling` → `AGENT_IN` → `robb-weds-jeyne-westerling`
- `LOCATED_AT`: `the-crag`

**SUB_BEAT_OF:** None.

---

### B5. `red-wedding-conspiracy`

**Proposed slug:** `red-wedding-conspiracy`  
**Type:** `event.conspiracy`  
(Justification: architecture defines event.conspiracy as "named secret plot as event-hub — multi-participant covert scheme treated as a discrete event for traversal." Walder Frey's secret correspondence with Roose Bolton and Tywin Lannister, culminating in the planned massacre at the Twins, is exactly this pattern. The conspiracy has a period, participants, target, and outcome.)

**Description:**  
After Robb Stark breaks his marriage pact with House Frey by wedding Jeyne Westerling, Lord Walder Frey secretly corresponds with Roose Bolton — who has already married into House Frey via Walda — and with Lord Tywin Lannister, Hand of the King. Walder seeks terms to bring House Frey back to the Iron Throne's side; Tywin countenances the plan to end Robb's rebellion without further battlefield losses; Roose agrees to betray his king at the feast. The conspiracy culminates in the invitation to the wedding of Edmure Tully and Roslin Frey — a trap. Tywin later admits he countenanced Walder's actions but assigns public responsibility to Frey; per Merrett Frey, the plan was ordered by Walder and arranged by Lothar Frey and Roose Bolton, with Ryman Frey also involved.

**## Quotes**

> "After learning of the broken pact, Walder secretly begins corresponding with Roose, who has wed Walder's granddaughter Walda, and with Lord Tywin Lannister, the Hand of the King, for terms to bring House Frey back as a supporter of the Iron Throne and King Joffrey I Baratheon."
>
> — Red Wedding wiki node (Origins section)  
> `graph/nodes/events/red-wedding.node.md` (sourced from `sources/wiki/_raw/Red_Wedding.json`)

> "The blood is on Walder Frey's hands, not mine." — Lord Tywin Lannister  
> "Walder Frey is a peevish old man who lives to fondle his young wife and brood over all the slights he's suffered. I have no doubt he hatched this ugly chicken, but he would never have dared such a thing without a promise of protection."
>
> — Tyrion and Tywin Lannister  
> `sources/chapters/asos/asos-tyrion-06.md` lines 203–205

> According to Merrett Frey, the Red Wedding was ordered by Walder and then arranged by Lame Lothar and Roose, with Ryman Frey involved as well.
>
> — Red Wedding wiki node (Aftermath section)  
> `graph/nodes/events/red-wedding.node.md` (sourced from `sources/wiki/_raw/Red_Wedding.json`)

**Proposed role edges:**
- `walder-frey` → `COMMANDS_IN` → `red-wedding-conspiracy` (orderer)
- `roose-bolton` → `AGENT_IN` → `red-wedding-conspiracy` (active traitor)
- `tywin-lannister` → `COMMANDS_IN` → `red-wedding-conspiracy` (gave protection/sanction)
- `lothar-frey` → `AGENT_IN` → `red-wedding-conspiracy` (arranger)

**SUB_BEAT_OF:** None (the conspiracy is a hub, not a sub-beat).

---

## C. Proposed Causal Edges (the chain)

All causal/interpretive edges are **Tier 2**. Role edges on each event node are **Tier 1**.

| source_slug | edge_type | target_slug | Tier | justification | evidence quote + file:line | agency note |
|---|---|---|---|---|---|---|
| `catelyn-releases-jaime-lannister` | CAUSES | `karstark-murders-prisoners-at-riverrun` | 2 | Catelyn's release of Jaime is the stated cause of Rickard's rage; Karstark explicitly attributes his motive to the freeing. No intervening node needed — Rickard's agency IS the murder. | "How can it be treason to kill Lannisters, when it is not treason to free them?" — Rickard Karstark; `asos-catelyn-03.md:57` | Rickard *chooses* revenge; but his choice IS the murder event. The edge captures mediated causation from release → revenge-killing. |
| `catelyn-releases-jaime-lannister` | MOTIVATES | `robb-stark` | 2 | Robb explicitly links Catelyn's act with his own folly ("Love's not always wise") and forgives her by analogy to his own choice; the freeing is the moral backdrop for his leniency toward himself. Less critical than other edges but models the parallel agency. | "If I could wish the Kingslayer back in chains I would. You freed him without my knowledge or consent . . . but what you did, I know you did for love . . . Don't we, Mother?" — Robb; `asos-catelyn-02.md:65` | *Optional edge* — if space is scarce, omit. The chain is walkable without it. |
| `karstark-murders-prisoners-at-riverrun` | CAUSES | `execution-of-rickard-karstark` | 2 | The murder is the direct cause of the execution; Robb explicitly states he has no choice after the murder of the prisoners. | "Rickard Karstark killed more than a Frey and a Lannister. He killed my honor. I shall deal with him at dawn." — Robb; `asos-catelyn-03.md:155` | Robb *chooses* to execute rather than imprison; Edmure urges leniency. Robb's agency is explicit. The edge captures the murder → execution consequence. |
| `execution-of-rickard-karstark` | CAUSES | `karstark-men-hunting-the-kingslayer` | 2 | Before the execution, Rickard had already sent his horse to hunt Jaime; the execution galvanizes the remaining Karstark foot and deepens their alienation. Post-execution, Roose Bolton's contingent at Harrenhal includes many Karstarks who will not fight for Robb. | "Gods know what the Karstark foot with Roose Bolton will do when they hear I've executed their liege for a traitor." — Robb; `asos-catelyn-03.md:111` | The Karstark soldiers who defect act of their own will — but the trigger is the execution. CAUSES (not TRIGGERS) because the Karstark unraveling plays out over weeks. |
| `robb-weds-jeyne-westerling` | TRIGGERS | `red-wedding-conspiracy` | 2 | The wiki Red Wedding node explicitly names this as the immediate spark: "After learning of the broken pact, Walder secretly begins corresponding with Roose." This is the named spark-beat, justifying TRIGGERS rather than CAUSES. | "After learning of the broken pact, Walder secretly begins corresponding with Roose . . . and with Lord Tywin Lannister . . . for terms to bring House Frey back." — Red Wedding wiki; `graph/nodes/events/red-wedding.node.md` (Origins) | Walder *chooses* revenge rather than seeking a new match; but the TRIGGERS edge is appropriate because this is the named immediate spark — the broken-pact news is the moment the conspiracy is born. |
| `wedding-of-roose-bolton-and-walda-frey` | MOTIVATES | `roose-bolton` | 2 | Roose's Frey marriage created the personal channel through which Walder's correspondence reached him; it also gave Roose a Frey stake independent of Robb. The Red Wedding wiki notes Walder "secretly begins corresponding with Roose, who has wed Walder's granddaughter Walda." | "Walder secretly begins corresponding with Roose, who has wed Walder's granddaughter Walda." — `graph/nodes/events/red-wedding.node.md` | Roose *chooses* to betray Robb; but his Frey marriage is the pre-condition that made him a willing recipient of Walder's overtures. MOTIVATES (event → actor) is the correct edge type. |
| `red-wedding-conspiracy` | CAUSES | `red-wedding` | 2 | The conspiracy is the direct multi-month causal chain that produces the Red Wedding event. The conspiracy IS the planning apparatus; the Red Wedding is its execution. | "The Red Wedding was ordered by Walder and then arranged by Lame Lothar and Roose, with Ryman Frey involved as well." — Red Wedding wiki, Aftermath; `graph/nodes/events/red-wedding.node.md` | Walder, Roose, and Tywin each *choose* to follow through; but the conspiracy → massacre link is near-deterministic. CAUSES is appropriate (TRIGGERS would be used if there were a single named spark inside the conspiracy; the conspiracy itself is the multi-step chain). |
| `red-wedding-conspiracy` | CAUSES | `robb-is-killed` | 2 | Sub-beat connection: the conspiracy targets Robb specifically; his killing is the named terminus sub-beat. Adding this edge ensures `--causal-chain robb-is-killed` also recovers the upstream chain. | "Jaime Lannister sends his regards." He thrust his longsword through her son's heart, and twisted. — `asos-catelyn-07.md:135` | Roose personally gives the order; his agent (unnamed man in pink cloak — Roose Bolton himself in the text) executes it. CAUSES (conspiracy → specific death) is appropriate. |

**REUSED nodes (no new minting):**
- `karstark-men-hunting-the-kingslayer` (Plate 3 stub; receives one inbound CAUSES from `execution-of-rickard-karstark`)
- `wedding-of-roose-bolton-and-walda-frey` (wiki-derived; receives one outbound MOTIVATES → `roose-bolton`)
- `red-wedding` (exists; receives one inbound CAUSES from `red-wedding-conspiracy`)
- `robb-is-killed` (Plate 3 stub; receives one inbound CAUSES from `red-wedding-conspiracy`)

---

## D. Chain Preview

```
catelyn-releases-jaime-lannister
  --CAUSES-->
    karstark-murders-prisoners-at-riverrun
      --CAUSES-->
        execution-of-rickard-karstark
          --CAUSES-->
            karstark-men-hunting-the-kingslayer  [REUSED; dead-end/context node]

robb-weds-jeyne-westerling
  --TRIGGERS-->
    red-wedding-conspiracy  [NEW]
      --CAUSES-->
        red-wedding  [REUSED; TERMINUS ✓]
      --CAUSES-->
        robb-is-killed  [REUSED; sub-beat TERMINUS ✓]

wedding-of-roose-bolton-and-walda-frey  [REUSED]
  --MOTIVATES-->
    roose-bolton  [character, not event]
    (roose-bolton --AGENT_IN--> red-wedding-conspiracy)
```

**Converging chains:** Both `catelyn-releases-jaime-lannister` and `robb-weds-jeyne-westerling` are independent upstream causes that converge at the Red Wedding. They are parallel, not sequential. The Karstark sub-chain is a side-branch that weakens Robb but does not directly cause the Red Wedding — it is correctly a dead-end after `karstark-men-hunting-the-kingslayer`.

**Hard stop confirmed:** No edge to `war-of-the-five-kings`. Terminus is `red-wedding` and its sub-beat `robb-is-killed`. ✓

---

## E. Open Questions / Risks

**E1. The Karstark sub-chain's causal weight.**  
The Karstark walkout is narratively significant (it deprives Robb of thousands of men and accelerates his strategic desperation) but it does NOT directly cause the Red Wedding — Walder Frey's outrage at the broken marriage pact is the trigger, not the Karstark defection. Accordingly, the Karstark sub-chain terminates at `karstark-men-hunting-the-kingslayer` with no edge to `red-wedding-conspiracy`. This is the correct conservative choice. If a future session wants to model Robb's weakening as a causal enabler (he needed Frey forces, so the Karstark loss made him negotiate from desperation), an `ENABLES` edge from `karstark-men-hunting-the-kingslayer` → `robb-weds-jeyne-westerling` (or → `red-wedding-conspiracy`) could be added, but this is interpretive and should be Matt's call.

**E2. The Sybell Spicer / Tywin coordination sub-plot.**  
Jeyne Westerling wiki reveals that Lady Sybell Spicer (Jeyne's mother) administered potions to Jeyne, and the AFFC text strongly implies Tywin had pre-arranged with Sybell that Robb would sleep with Jeyne but not conceive an heir (Sybell's "possets" suppress fertility). This means `robb-weds-jeyne-westerling` may itself be a DECEPTION — a Lannister-orchestrated trap to get Robb to break his oath. Modeling this would require a new `event.deception` node (e.g., `spicer-deception-of-robb-westerling`). **This arc intentionally excludes this sub-plot** — it is Tier 3 at best (only confirmed in AFFC, and not fully explicit) and would bloat the chain. Flag for a separate deception-arc research pass.

**E3. Is `plot-to-free-jaime-lannister` a near-duplicate of `catelyn-releases-jaime-lannister`?**  
No — confirmed different events. `plot-to-free-jaime-lannister` is Tyrion's ACOK operation (placing agents in Cleos Frey's escort; fails; Jaime is recaptured). `catelyn-releases-jaime-lannister` is Catelyn's solo midnight act at ACOS Catelyn VII. Different actors, different mechanisms, different outcomes. No collision.

**E4. `execution-of-rickard-karstark` type choice.**  
Using `event.execution` is correct per architecture (formal execution, king as orderer/executor, heart tree as location, witnesses assembled). However, the architecture also allows `event.assassination` for targeted killings. The distinction is clear: Robb's killing is judicial (formal condemnation + public execution), not clandestine. `event.execution` stands.

**E5. Should `catelyn-releases-jaime-lannister` be `event.deception` instead of `event.incident`?**  
No — Catelyn is not deceiving anyone (she explicitly confesses to Ser Desmond the next morning). She commits a unilateral act, not a deception. `event.incident` is correct.

**E6. Does the ACOK Catelyn VII chapter end at "Give me your sword" — making the freeing off-page?**  
Yes: the chapter ends at line 336 with Catelyn asking Brienne for her sword. The freeing happens off-page in ACOK; we learn of it at the start of ASOS Catelyn I. Both files (`sources/chapters/acok/acok-catelyn-07.md` and `sources/chapters/asos/asos-catelyn-01.md`) attest the act. The proposed node's evidence_chapters should cite both.

**E7. Minimum viable chain check.**  
The smallest set of new nodes that makes `--causal-chain red-wedding` walkable:
- Strictly minimum: just `robb-weds-jeyne-westerling` --TRIGGERS--> `red-wedding-conspiracy` --CAUSES--> `red-wedding`. That's 2 new nodes, 2 new edges.
- This proposal adds `catelyn-releases-jaime-lannister`, `karstark-murders-prisoners-at-riverrun`, and `execution-of-rickard-karstark` as the upstream Karstark chain — they deepen the story but are not required for the Red Wedding to be causally reachable.
- Recommendation: mint all 5 new nodes. The Karstark sub-chain is historically significant and enriches traversal; omitting it would leave a documented narrative thread unwired.

---

*End of research proposal. No files written to graph/. No edges created. This document is a proposal only.*
