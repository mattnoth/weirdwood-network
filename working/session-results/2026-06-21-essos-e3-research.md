# ESSOS Arc E3 Research — Daznak's Pit → Dany Lost on Dothraki Sea
**Date:** 2026-06-21  
**Session:** S120 subagent  
**Chapters read:** adwd-daenerys-09 (ch53), adwd-daenerys-10 (ch72)  
**Task:** Gather quotes, adjudicate causal spine, propose node bodies for 3 net-new nodes in E3 juncture.

---

## 1. Live Graph State

All five queried nodes confirmed live. Summary of current edges:

### `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen`
- **OUTGOING (1):** PRECEDES → `landing-of-the-golden-company`
- **INCOMING (3):** PRECEDES ← `wedding-of-ramsay-bolton-and-arya-stark`; SUB_BEAT_OF ← `wedding-morning-daario-leaves-angrily`; TRIGGERS ← `sons-of-the-harpy-kill-twenty-nine`
- **Causal status: DARK outward** — zero causal outgoing edges. The wedding is a sink in the current graph. No connection to the Daznak cluster exists yet.

### `hizdahr-orders-drogon-killed`
- **OUTGOING (0):** None
- **INCOMING (3):** AGENT_IN ← `pit-spearmen`; COMMANDS_IN ← `hizdahr-zo-loraq`; VICTIM_IN ← `drogon`
- **Causal status: DARK** — no causal in or out.

### `drogon-kills-more-attackers`
- **OUTGOING (0):** None
- **INCOMING (3):** AGENT_IN ← `drogon`; COMMANDS_IN ← `hizdahr-zo-loraq`; VICTIM_IN ← `pitmaster`
- **Causal status: DARK**

### `unnamed-spearman-attacks-drogon`
- **OUTGOING (0):** None
- **INCOMING (3):** AGENT_IN ← `unnamed-spearman`; COMMANDS_IN ← `hizdahr-zo-loraq`; VICTIM_IN ← `drogon`
- **Causal status: DARK**

### `sons-of-the-harpy-kill-twenty-nine`
- **OUTGOING (3):** LOCATED_AT → `meereen`; MOTIVATES → `daenerys-targaryen`; TRIGGERS → `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen`
- **INCOMING (5):** AGENT_IN ← `sons-of-the-harpy`; CAUSES ← `siege-of-meereen`; COMMANDS_IN ← `hizdahr-zo-loraq`; VICTIM_IN ← `freedmen`, `shavepates`
- **Causal status: Live upstream/downstream** — this is the node that triggers the wedding, confirming the chain root.

**Conclusion:** No existing node is connected causally to the three dark Daznak sub-beat nodes or to the wedding's downstream consequence. The three new nodes will close this gap completely.

---

## 2. The Three New Node Proposals

---

### NODE A: `drogon-returns-to-daznak-pit`

**type:** `event.incident`

**Aliases (natural SPACED phrases only):**
- "Drogon descends on Daznak's Pit"
- "Drogon's return to the fighting pit"
- "Drogon appears at the games"
- "Drogon kills Barsena and the boar"

**Prose body (3-5 sentences):**
During the opening of Daznak's Pit — the fighting games Daenerys grudgingly permitted as a concession of her marriage to Hizdahr zo Loraq — a vast shadow falls across the arena. Drogon, wild and grown enormous in his self-exile, descends from the sky, kills the boar and devours Barsena Blackhair along with it. His arrival causes immediate panic among fighters, pit staff, and spectators, who scatter or flee the tiers. Hizdahr zo Loraq shouts for the spearmen to kill the dragon, triggering the chaotic assault that will wound Drogon and culminate in Daenerys mounting him. This is the precipitating incident of the E3 juncture: the moment Drogon's presence at the pit makes Dany's flight mechanically possible.

**## Quotes:**

```
"A shadow rippled across his face."
— sources/chapters/adwd/adwd-daenerys-09.md:229

"Above them all the dragon turned, dark against the sun. His scales were black, his eyes and horns
and spinal plates blood red. Ever the largest of her three, in the wild Drogon had grown larger
still. His wings stretched twenty feet from tip to tip, black as jet. He flapped them once as he
swept back above the sands, and the sound was like a clap of thunder. The boar raised his head,
snorting … and flame engulfed him, black fire shot with red. Dany felt the wash of heat thirty feet
away. The beast's dying scream sounded almost human. Drogon landed on the carcass and sank his claws
into the smoking flesh. As he began to feed, he made no distinction between Barsena and the boar."
— sources/chapters/adwd/adwd-daenerys-09.md:233

"The tumult and the shouting died. Ten thousand voices stilled. Every eye turned skyward."
— sources/chapters/adwd/adwd-daenerys-09.md:231
```

---

### NODE B: `dany-mounts-drogon-and-flees-meereen`

**type:** `event.incident`

**Aliases (natural SPACED phrases only):**
- "Daenerys mounts Drogon in Daznak's Pit"
- "Dany flees Meereen on Drogon"
- "Dany vaults onto Drogon and flies"
- "Daenerys's wild flight from Meereen"

**Prose body (3-5 sentences):**
After forcing Drogon to submit through whip and will — picking up the pitmaster's discarded lash and driving the dragon down with shouts and blows — Daenerys vaults onto his back, tears out the spear embedded at the base of his neck, and is carried into the air as the scarlet sands fall away beneath her. She gives him his head and cries "Higher!" as Drogon beats his wings and clears the pit, climbing above the pyramids of Meereen, wounded and trailing smoke. The flight is not fully controlled: Drogon is wounded, she has no saddle or conventional means of steering, and the ascent is described from a retrospective haze. This event strips Daenerys of her role as queen of Meereen and initiates the Dothraki-sea sojourn that constitutes E3's terminus.

**## Quotes:**

```
"Daenerys Targaryen vaulted onto the dragon's back, seized the spear, and ripped it out. The point
was half-melted, the iron red-hot, glowing. She flung it aside. Drogon twisted under her, his
muscles rippling as he gathered his strength. The air was thick with sand. Dany could not see, she
could not breathe, she could not think. The black wings cracked like thunder, and suddenly the
scarlet sands were falling away beneath her."
— sources/chapters/adwd/adwd-daenerys-09.md:265

"The lash was still in her hand. She flicked it against Drogon's neck and cried, 'Higher!' Her other
hand clutched at his scales, her fingers scrabbling for purchase. Drogon's wide black wings beat the
air. Dany could feel the heat of him between her thighs. Her heart felt as if it were about to burst.
Yes, she thought, yes, now, now, do it, do it, take me, take me, FLY!"
— sources/chapters/adwd/adwd-daenerys-09.md:269

"In the smoldering red pits of Drogon's eyes, Dany saw her own reflection. How small she looked, how
weak and frail and scared. I cannot let him see my fear."
— sources/chapters/adwd/adwd-daenerys-09.md:259
(context: the confrontation immediately before she seizes the whip and forces his submission)
```

---

### NODE C: `dany-lost-on-dothraki-sea`

**type:** `event.incident`

**Aliases (natural SPACED phrases only):**
- "Dany lost on the Dothraki sea"
- "Daenerys stranded on the Dothraki sea"
- "Daenerys barefoot in the grass"
- "Dany's sojourn on Dragonstone hill"

**Prose body (3-5 sentences):**
Drogon carries Daenerys north beyond the Skahazadhan river and sets down on a volcanic hill she names Dragonstone, stranding her far out in the Dothraki sea — alone, barefoot (one sandal lost in the flight), dressed in rags, and without supplies. She spends days recovering from burns, eating Drogon's scorched leavings, and trying unsuccessfully to ride him back to Meereen, but Drogon repeatedly returns to his lair rather than obeying her direction. A retrospective passage in the chapter reconstructs the chaos of the flight and the city receding below them. The chapter closes when a Dothraki scout discovers her and she summons Drogon, leaping on his back and turning him north by east toward the approaching khalasar of Khal Jhaqo — the published terminus of Daenerys's arc in ADWD.

**## Quotes:**

```
"North they flew, beyond the river, Drogon gliding on torn and tattered wings through clouds that
whipped by like the banners of some ghostly army. Dany glimpsed the shores of Slaver's Bay and the
old Valyrian road that ran beside it through sand and desolation until it vanished in the west. The
road home. Then there was nothing beneath them but grass rippling in the wind."
— sources/chapters/adwd/adwd-daenerys-10.md:55

"One of her sandals had slipped off during her wild flight from Meereen and she had left the other
up by Drogon's cave, preferring to go barefoot rather than half-shod. Her tokar and veils she had
abandoned in the pit, and her linen undertunic had never been made to withstand the hot days and cold
nights of the Dothraki sea."
— sources/chapters/adwd/adwd-daenerys-10.md:35

"That was how Khal Jhaqo found her, when half a hundred mounted warriors emerged from the drifting
smoke."
— sources/chapters/adwd/adwd-daenerys-10.md:229
(final line; the ADWD terminus for Daenerys's arc)
```

---

## 3. Adjudicated Edge Spec Table

| src | type | tgt | tier | evidence file:line | evidence_quote | rationale |
|-----|------|-----|------|--------------------|----------------|-----------|
| `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` | ENABLES | `drogon-returns-to-daznak-pit` | 2 | sources/chapters/adwd/adwd-daenerys-06.md:139 | "To celebrate your nuptials, it would be most fitting if you would allow the fighting pits to open once again. It would be your wedding gift to Hizdahr and to your loving people." | The wedding does NOT summon Drogon and is not the mechanical cause of his descent. The wedding ENABLES the pit reopening (it is the political concession-vehicle that makes Hizdahr king, which triggers the reopening), and Drogon's descent is his own autonomous choice to hunt in an arena with prey. ENABLES is correct: the wedding creates the structural precondition (open pit with crowd, boar, and spectacle) without which Drogon's arrival at the games would have been impossible. Compare E2 usage: ENABLES was used for army-enablement waypoints where the causal path runs through an intermediate actor's choice. The wedding → pit reopening → Drogon's autonomous descent is the same pattern. If we used CAUSES here, we would be saying the wedding mechanically produced Drogon's arrival, eliding Drogon's agency. ENABLES is the right call. |
| `drogon-returns-to-daznak-pit` | TRIGGERS | `dany-mounts-drogon-and-flees-meereen` | 2 | sources/chapters/adwd/adwd-daenerys-09.md:241 | "Dany and Drogon screamed as one." | The spearman wounding Drogon is the immediate spark for the confrontation that ends in Dany seizing the whip, forcing Drogon's submission, and vaulting onto him. But the trigger for the whole chain is Drogon's arrival at the pit — without it, there is no confrontation, no wound, no Dany-on-the-ground. TRIGGERS is preferred over CAUSES because: (a) the wounding is an intervening agency (the unnamed spearman, acting on Hizdahr's order); (b) Dany's mount requires her own will + action (she chooses to run into the pit, she picks up the whip, she subdues Drogon); the descent does not mechanically produce the mount. TRIGGERS captures that Drogon's arrival in the pit is the precipitating spark, while leaving room for the several acts of will that complete the mount. |
| `dany-mounts-drogon-and-flees-meereen` | CAUSES | `dany-lost-on-dothraki-sea` | 2 | sources/chapters/adwd/adwd-daenerys-10.md:55 | "North they flew, beyond the river, Drogon gliding on torn and tattered wings … Then there was nothing beneath them but grass rippling in the wind." | CAUSES is correct and unambiguous. The flight is a direct mechanical consequence of the mount: Drogon takes her north, lands on the hill, refuses to return to Meereen. There is no intervening agent or choice that could break the causal link — Drogon's instinct to go to his lair is not a separate event requiring its own node, it is part of what happens when Dany mounts a wild dragon without a binding spell. CAUSES. |
| `daenerys-targaryen` | AGENT_IN | `dany-mounts-drogon-and-flees-meereen` | 1 | sources/chapters/adwd/adwd-daenerys-09.md:265 | "Daenerys Targaryen vaulted onto the dragon's back, seized the spear, and ripped it out." | She is the primary actor; she runs into the pit, tames Drogon, mounts him. AGENT_IN. Tier-1 (book-direct). |
| `drogon` | AGENT_IN | `dany-mounts-drogon-and-flees-meereen` | 1 | sources/chapters/adwd/adwd-daenerys-09.md:265 | "The black wings cracked like thunder, and suddenly the scarlet sands were falling away beneath her." | Drogon is the co-agent — he beats his wings and carries her. Include as AGENT_IN. Tier-1. |

### Agency / MOTIVATES edge — evaluation

**Question:** does `drogon-returns-to-daznak-pit` or the chaos MOTIVATE Dany?

**Text:** adwd-daenerys-09.md:259 — "I am looking into hell, but I dare not look away. She had never been so certain of anything. If I run from him, he will burn me and devour me." This is not a MOTIVATES relationship in the graph-vocabulary sense (MOTIVATES = one event reshapes an actor's long-term goals or choices). It describes Dany's survival-reasoning in the moment, not a goal-shift. The actual motivation arc is already present: `sons-of-the-harpy-kill-twenty-nine` MOTIVATES `daenerys-targaryen` (existing edge). The Daznak descent is the occasion for Dany's act, not the motivation for it. **No MOTIVATES edge is warranted.**

There is, however, a `dany-lost-on-dothraki-sea` → MOTIVATES → `daenerys-targaryen` edge worth considering for a *future* session: ch10 line 197 — "Fire and Blood," Daenerys told the swaying grass" — the sojourn crystallizes her identity as blood of the dragon rather than queen of Meereen. But that belongs to a future enrichment pass, not this mint. Not in scope now.

---

## 4. SUB_BEAT_OF Decisions

### `hizdahr-orders-drogon-killed` SUB_BEAT_OF `drogon-returns-to-daznak-pit`?

**Text:** adwd-daenerys-09.md:245 — `"Kill it," Hizdahr zo Loraq shouted to the other spearmen. "Kill the beast!"` 

This shout occurs **during** the chaos of Drogon's descent, after the unnamed spearman has already wounded the dragon. It is squarely inside the Drogon-descent incident — Hizdahr is reacting to Drogon already being present and wounded. The node `hizdahr-orders-drogon-killed` is definitively a beat that occurs WITHIN `drogon-returns-to-daznak-pit`.

**Verdict: YES** — `hizdahr-orders-drogon-killed` SUB_BEAT_OF `drogon-returns-to-daznak-pit`. Tier-3.

---

### `drogon-kills-more-attackers` SUB_BEAT_OF `drogon-returns-to-daznak-pit`?

**Text:** adwd-daenerys-09.md:251 — "As the other spears closed in, the dragon spat fire, bathing two men in black flame. His tail lashed sideways and caught the pitmaster creeping up behind him, breaking him in two."

This happens during the same continuous incident of Drogon's presence in the pit — after he descends, while the spearmen attack him. Unambiguously inside the descent event.

**Verdict: YES** — `drogon-kills-more-attackers` SUB_BEAT_OF `drogon-returns-to-daznak-pit`. Tier-3.

---

### `unnamed-spearman-attacks-drogon` SUB_BEAT_OF `drogon-returns-to-daznak-pit`?

**Text:** adwd-daenerys-09.md:239 — "He darted forward, his boar spear in his hands … The hero leapt onto his back and drove the iron spearpoint down at the base of the dragon's long scaled neck."

Happens during Drogon's descent, while Drogon is eating Barsena. The spearman is one of the dozen men sent out to drive the boar away who impulsively attacks instead.

**Verdict: YES** — `unnamed-spearman-attacks-drogon` SUB_BEAT_OF `drogon-returns-to-daznak-pit`. Tier-3.

**All three dark Daznak nodes become SUB_BEAT_OF `drogon-returns-to-daznak-pit`.**

Note on sequencing within the hub (informational, not edges): the beating order is (1) Drogon descends, kills boar and Barsena; (2) unnamed spearman leaps on and wounds him [→ `unnamed-spearman-attacks-drogon`]; (3) Hizdahr shouts to kill it [→ `hizdahr-orders-drogon-killed`]; (4) spearmen attack en masse and Drogon kills/burns them [→ `drogon-kills-more-attackers`]; (5) Dany runs into the pit. All are tightly sequential within a single continuous incident.

---

## 5. Concerns and Flags

### Flag A: `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` ENABLES vs TRIGGERS — edge to open pit, not Daznak descent
The path `wedding → ENABLES → drogon-returns-to-daznak-pit` is accurate but **mediated**: the wedding enables a pit **reopening** (a separate causally intermediate action by Hizdahr post-wedding), and the first reopened games at Daznak's are what Drogon descends upon. There is an implicit intermediate event ("Hizdahr reopens fighting pits") that is not currently modeled as a node.

**Recommendation for orchestrator:** The ENABLES edge is defensible as written and sufficient for traversal. However, if the graph later needs fine-grained causal tracing, a `hizdahr-reopens-fighting-pits` event node with ENABLES ← `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` and ENABLES → `drogon-returns-to-daznak-pit` would be cleaner. Not required for this mint — defer to enrichment.

### Flag B: Source text for reopening concession
The exact textual basis for the pit reopening as a wedding condition is **adwd-daenerys-06.md:139,143** (Reznak proposes it; Dany defers to Hizdahr's prerogative post-wedding) and **adwd-daenerys-09.md:117** ("By her grace and with her leave, I give you now your mortal art" — Hizdahr's speech opening the games). The link between the wedding and pit opening is asserted in Reznak's framing (line 139) and Dany's acquiescence (line 143). Use `:139` as the evidence cite for the ENABLES edge.

### Flag C: Hizdahr's shout — direct speech vs paraphrase in existing nodes
The existing `hizdahr-orders-drogon-killed` node's evidence quotes read as paraphrases ("Shouts 'Kill it! Kill the beast!' to the spearmen"), not from adwd-daenerys-09.md's actual lines. The direct speech at line 245 is: `"Kill it," Hizdahr zo Loraq shouted to the other spearmen. "Kill the beast!"` — this should be cited as `:245` in any edge refresh, not the existing node evidence_quote form. Not blocking, but worth noting if the node is ever enriched.

### Flag D: Poison / Strong Belwas context
adwd-daenerys-10.md:85 contains Dany's suspicion that the honeyed locusts were poisoned — "Strong Belwas had been on his knees, heaving and shuddering. Poison. It had to be poison. The honeyed locusts." This is relevant to `hizdahr-orders-drogon-killed` and potentially to a `poisoning-of-strong-belwas` event node that does not currently appear in the dedup list. If that node exists (or is in a future arc), this is its primary textual anchor. Not in scope for E3 mints — flagged for orchestrator awareness.

---

## Summary for Orchestrator (Edge Spec + Node Types + Wedding Verdict)

### Wedding → Daznak verdict:
**ENABLES**, not CAUSES or TRIGGERS. The wedding is the political vehicle for the pit-reopening concession; Drogon's descent is his autonomous choice over the opened arena. The causal path is: wedding ENABLES (pit reopening) which ENABLES Drogon's descent opportunity. One waypoint is implicit but the ENABLES edge correctly captures the enabling role without overclaiming.

### Edge spec (paste-ready):

| src | type | tgt | tier | cite | quote |
|-----|------|-----|------|------|-------|
| wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen | ENABLES | drogon-returns-to-daznak-pit | 2 | sources/chapters/adwd/adwd-daenerys-06.md:139 | "it would be most fitting if you would allow the fighting pits to open once again. It would be your wedding gift to Hizdahr" |
| drogon-returns-to-daznak-pit | TRIGGERS | dany-mounts-drogon-and-flees-meereen | 2 | sources/chapters/adwd/adwd-daenerys-09.md:241 | "Dany and Drogon screamed as one." |
| dany-mounts-drogon-and-flees-meereen | CAUSES | dany-lost-on-dothraki-sea | 2 | sources/chapters/adwd/adwd-daenerys-10.md:55 | "North they flew, beyond the river, Drogon gliding on torn and tattered wings … Then there was nothing beneath them but grass rippling in the wind." |
| daenerys-targaryen | AGENT_IN | dany-mounts-drogon-and-flees-meereen | 1 | sources/chapters/adwd/adwd-daenerys-09.md:265 | "Daenerys Targaryen vaulted onto the dragon's back, seized the spear, and ripped it out." |
| drogon | AGENT_IN | dany-mounts-drogon-and-flees-meereen | 1 | sources/chapters/adwd/adwd-daenerys-09.md:265 | "The black wings cracked like thunder, and suddenly the scarlet sands were falling away beneath her." |
| hizdahr-orders-drogon-killed | SUB_BEAT_OF | drogon-returns-to-daznak-pit | 3 | sources/chapters/adwd/adwd-daenerys-09.md:245 | "Kill it," Hizdahr zo Loraq shouted to the other spearmen. "Kill the beast!" |
| drogon-kills-more-attackers | SUB_BEAT_OF | drogon-returns-to-daznak-pit | 3 | sources/chapters/adwd/adwd-daenerys-09.md:251 | "the dragon spat fire, bathing two men in black flame. His tail lashed sideways and caught the pitmaster creeping up behind him, breaking him in two." |
| unnamed-spearman-attacks-drogon | SUB_BEAT_OF | drogon-returns-to-daznak-pit | 3 | sources/chapters/adwd/adwd-daenerys-09.md:239 | "The hero leapt onto his back and drove the iron spearpoint down at the base of the dragon's long scaled neck." |

### Node types: all three are `event.incident`.
