# E5 Research: doran-reveals-fire-and-blood-pact + death-of-quentyn-martell
**Date:** 2026-06-21  **Session:** S120-E5  **Agent:** research+verify subagent

---

## 1. Live Graph State

### arianne-collapses-and-is-captured
- **Type:** event.capture
- **File:** `graph/nodes/events/arianne-collapses-and-is-captured.node.md`
- **Outgoing (1):**
  - `LOCATED_AT` → `greenblood`
- **Incoming (4):**
  - `AGENT_IN` ← `areo-hotah`
  - `CAUSES` ← `areo-hotah-springs-the-ambush`
  - `COMMANDS_IN` ← `doran-martell`
  - `VICTIM_IN` ← `arianne-martell`
- **Verdict:** Confirmed S117 terminus. Causally dark on the OUTGOING side (no CAUSES/TRIGGERS outgoing). This is the node that must gain the new outgoing `CAUSES` → `doran-reveals-fire-and-blood-pact`.

### quentyn-orders-the-attack
- **Type:** event.incident
- **File:** `graph/nodes/events/quentyn-orders-the-attack.node.md`
- **Outgoing (0):** Confirmed causally dark. The new outgoing `TRIGGERS` → `death-of-quentyn-martell` is the only causal edge needed.
- **Incoming (5):**
  - `AGENT_IN` ← `archibald-yronwood` (torch/warhammer)
  - `AGENT_IN` ← `gerris-drinkwater` (sword through locust's throat)
  - `AGENT_IN` ← `caggo` (Valyrian steel arakh beheading)
  - `AGENT_IN` ← `windblown` (crossbow bolt)
  - `COMMANDS_IN` ← `quentyn-martell` ("He croaks 'Take them,' and the fight begins.")

### arrest-of-the-sand-snakes (checked per task spec)
- **Outgoing (1):** `MOTIVATES` → `arianne-martell`
- **Incoming (6):** `AGENT_IN` ← `areo-hotah`; `CAUSES` ← `gregor-confesses-and-kills-oberyn`; `COMMANDS_IN` ← `doran-martell`; `VICTIM_IN` ← `obara-sand`, `nymeria-sand`, `tyene-sand`
- **Note:** The chain `arrest-of-the-sand-snakes` → `arianne-martell` uses `MOTIVATES` (drives Arianne's Queenmaker plan), which eventually reaches `arianne-collapses-and-is-captured`. This confirms the S117 upstream; `arianne-collapses` is correctly the cross-book root.

---

## 2. Verbatim Quotes with Exact file:line

### Node: doran-reveals-fire-and-blood-pact
**Source file:** `sources/chapters/affc/affc-the-princess-in-the-tower-01.md`

**Quote A — the "Fire and blood" whisper + onyx dragon (primary anchor):**
> "Vengeance." His voice was soft, as if he were afraid that someone might be listening. "Justice." Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, "Fire and blood."

**Line:** `affc-the-princess-in-the-tower-01.md:325` ✅ VERIFIED (re-pinned; earlier estimate of ≈325 confirmed exact)

**Quote B — Arianne's betrothal reveal (the long-secret pact context):**
> "The pact was sealed in secret. I meant to tell you when you were old enough . . . when you came of age, I thought, but . . ."

**Line:** `affc-the-princess-in-the-tower-01.md:297`

**Quote C — Doran names Quentyn's quest as the pact's active arm:**
> "Your brother went with Cletus Yronwood, Maester Kedry, and three of Lord Yronwood's best young knights on a long and perilous voyage, with an uncertain welcome at its end. He has gone to bring us back our heart's desire."

**Line:** `affc-the-princess-in-the-tower-01.md:321`

**Quote D — Arianne told she was betrothed (now-dead Viserys implicit):**
> "It was a pot of molten gold. We princes make our careful plans and the gods smash them all awry."

**Line:** `affc-the-princess-in-the-tower-01.md:309`
*(context: Doran says her betrothed "died" from "a pot of molten gold" — the death of Viserys Targaryen; this line establishes the pact predates the reveal by years)*

---

### Node: death-of-quentyn-martell
**Source files:** `sources/chapters/adwd/adwd-the-dragontamer-01.md` (burning moment); `sources/chapters/adwd/adwd-the-queens-hand-01.md` (death confirmed)

**Quote A — the burning moment (Rhaegal's attack):**
> "When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning. Oh, he thought. Then he began to scream."

**Lines:** `adwd-the-dragontamer-01.md:267-269`

**Quote B — death confirmed by Barristan (aftermath):**
> "So much of the prince's flesh had sloughed away that he could see the skull beneath. His eyes were pools of pus. He should have stayed in Dorne. He should have stayed a frog. Not all men are meant to dance with dragons."

**Line:** `adwd-the-queens-hand-01.md:39`

**Quote C — Barristan reports time of death to Shavepate:**
> "Prince Quentyn died just before first light."

**Line:** `adwd-the-queens-hand-01.md:45`

**Quote D — Quentyn's internal thought just before the burning (establishes motive/context):**
> "Fire and blood," he whispered, "blood and fire." The blood was pooling at his feet, soaking into the brick floor. The fire was beyond those doors.

**Line:** `adwd-the-dragontamer-01.md:199`

**Additional context — Gerris Drinkwater's testimony on Quentyn's justification (The Queen's Hand):**
> "Quentyn told the Tattered Prince he could control them. It was in his blood, he said. He had Targaryen blood."

**Line:** `adwd-the-queens-hand-01.md:205`

---

## 3. Adjudicated Edge Spec

| src | type | tgt | tier | cite | quote | rationale |
|-----|------|-----|------|------|-------|-----------|
| `arianne-collapses-and-is-captured` | CAUSES | `doran-reveals-fire-and-blood-pact` | Tier-2 | `affc-the-princess-in-the-tower-01.md:293` | "Because I knew that you would spurn him. I had to be seen to try to find a consort for you once you'd reached a certain age, else it would have raised suspicions, but **I dared not bring you any man you might accept. You were promised, Arianne.**" | Doran explicitly says he withheld the pact because he couldn't risk Arianne knowing — the "Queenmaker fallout / her capture" is what forces the reveal. He chose this moment because Arianne's imprisonment created a controlled, private setting where the secret could finally be disclosed safely. CAUSES is the correct type: the imprisonment (arianne-collapses-and-is-captured) is a necessary and sufficient precondition for the reveal scene to occur in this form. |
| `quentyn-orders-the-attack` | TRIGGERS | `death-of-quentyn-martell` | Tier-2 | `adwd-the-dragontamer-01.md:263` | "And then a hot wind buffeted him and he heard the sound of leathern wings and the air was full of ash and cinders and a monstrous roar went echoing off the scorched and blackened bricks and he could hear his friends shouting wildly … 'Behind you, behind you, behind you!'" | Quentyn's order sets off the fight; the fight triggers Rhaegal's attack (Rhaegal, not Viserion, strikes Quentyn from behind while Quentyn is focused on Viserion). Direct mechanistic chain: command → fight → dragons excited → Rhaegal burns Quentyn. TRIGGERS is correct (immediate mechanistic chain, not planning or enabling). |
| `doran-martell` | AGENT_IN | `doran-reveals-fire-and-blood-pact` | Tier-1 | `affc-the-princess-in-the-tower-01.md:325` | "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, 'Fire and blood.'" | He is the disclosing agent of the pact — the one who speaks the words and presses the token. |
| `arianne-martell` | WITNESS_IN | `doran-reveals-fire-and-blood-pact` | Tier-1 | `affc-the-princess-in-the-tower-01.md:325` | "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, 'Fire and blood.'" | **WITNESS_IN text-anchor gate:** She physically receives the onyx dragon into her palm; the entire chapter is her POV; she is the one to whom the secret is revealed. She does not merely overhear — she is the addressee and the receiver of the token. WITNESS_IN gate passes. |
| `quentyn-martell` | VICTIM_IN | `death-of-quentyn-martell` | Tier-1 | `adwd-the-dragontamer-01.md:267` | "When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning." | He is the person who dies. Unambiguous. |
| `rhaegal` | AGENT_IN | `death-of-quentyn-martell` | Tier-1 | `adwd-the-dragontamer-01.md:263-267` | "And then a hot wind buffeted him and he heard the sound of leathern wings … 'Behind you, behind you, behind you!' … All of him, all of him was burning." | Rhaegal is the dragon that burns Quentyn from behind. The text establishes leathern wings + the direction warning, and Quentyn's burning follows immediately. **This is defensible:** dragons in this graph are modeled as agents capable of autonomous violence (compare Viserion's unprompted killing of the sellsword at line 253). AGENT_IN for Rhaegal is justified — he acts independently of Quentyn's intent. |

### Notes on role-edge adjudication
- **Viserion vs Rhaegal confusion:** Quentyn was focused on Viserion (the white dragon, in front of him). Rhaegal (the green dragon) attacks him from behind — explicitly signaled by "Behind you, behind you, behind you!" and the "green" identification earlier at line 213-215 and the whip-lash on Viserion at line 261. The AGENT_IN edge goes on **Rhaegal**, not Viserion.
- **Caggo / Pretty Meris / Windblown** as AGENT_IN on `death-of-quentyn-martell`? No — they flee or are absent at the moment of burning. Their participation is in `quentyn-orders-the-attack`. Do not add them to the death node.

---

## 4. STRUCTURAL QUESTION Verdict

**Question:** Should `doran-reveals-fire-and-blood-pact` connect causally to `quentyn-orders-the-attack` or `death-of-quentyn-martell`? Or do the two halves of E5 stay as separate segments?

**Verdict: Leave as TWO CLEAN SEGMENTS. Do not add a link from the reveal node to the Quentyn death chain.**

**Reasoning:**

The anti-signal analysis is correct. The timeline is:
1. Doran makes the secret pact with the Targaryens years before AFFC (undated, unmodeled).
2. Doran sends Quentyn on the quest (AGOT/ACOK era — Quentyn's journey begins before AFFC opens).
3. Arianne's imprisonment forces Doran to reveal the pact to Arianne (AFFC, affc-the-princess-in-the-tower-01.md).
4. Quentyn arrives in Meereen, fails to win Daenerys, decides to steal the dragons (ADWD).
5. Quentyn orders the attack → dragons burn him → he dies.

The reveal at step 3 is **posterior to** Quentyn's quest departure at step 2. Doran tells Arianne: "Your brother went … on a long and perilous voyage" (line 321 — past tense, already underway). The reveal scene is an **exposition beat for the reader and for Arianne** — it discloses to both what had already been set in motion. It does not cause Quentyn's quest in any narrative-mechanical sense.

A `doran-reveals CAUSES quentyn-travels` edge would invert the chronology. A `doran-reveals ENABLES quentyn-orders-the-attack` edge would claim the reveal gave Quentyn new capability — also false; Quentyn knew his mission before Arianne knew anything.

The underlying causal agent — Doran's decision to make the pact and send Quentyn — is NOT modeled as a node. That deep cause is unmodeled by design (undated, predates the text, would need its own node like `doran-makes-marriage-pact-with-targaryens` if ever minted). Without that upstream node, the two segments are:

- **Segment A (Dorne):** `arianne-collapses-and-is-captured` → CAUSES → `doran-reveals-fire-and-blood-pact` [with Doran AGENT_IN, Arianne WITNESS_IN]
- **Segment B (Meereen):** `quentyn-orders-the-attack` → TRIGGERS → `death-of-quentyn-martell` [with Quentyn VICTIM_IN, Rhaegal AGENT_IN]

These two segments are thematically united by Doran's pact but **causally independent in the graph**. A graph traversal that wants to surface their connection should use the shared `doran-martell` node (AGENT_IN in segment A's reveal event; COMMANDS_IN in segment B's `quentyn-orders-the-attack`) — that hub links the segments via character, not a forced causal chain.

**If a future session mints `doran-makes-marriage-pact-with-targaryens`**, that upstream node could then receive:
- `doran-makes-marriage-pact` → CAUSES → `doran-sends-quentyn-on-quest` (if that event is minted)
- `doran-makes-marriage-pact` → CAUSES → `doran-reveals-fire-and-blood-pact`

But that is future work. For E5, the two segments stay separate.

---

## 5. Node Body Proposals

### Node: doran-reveals-fire-and-blood-pact
```
---
slug: doran-reveals-fire-and-blood-pact
type: event.incident
aliases:
  - Doran reveals the fire and blood pact
  - Doran discloses the Targaryen marriage pact
  - the fire and blood whisper
  - Doran tells Arianne of the secret pact
cite_ref: sources/chapters/affc/affc-the-princess-in-the-tower-01.md:325
confidence: 1
---

## Summary

Following Arianne's imprisonment after the Queenmaker plot, Prince Doran Martell finally discloses to her a marriage pact he sealed in secret years before: Dorne was promised to the Targaryen cause, and Arianne herself had been secretly betrothed to Viserys Targaryen, who is now dead. Quentyn Martell has already been sent on a perilous voyage to Essos to fulfill Dorne's pledge through a new approach — to win Daenerys Targaryen as bride and ally. Doran reveals that his years of deliberate inaction, his refusal to offer Arianne any suitor she could accept, and his apparent passivity were all calculated to protect this secret. He presses an onyx dragon piece into Arianne's palm and whispers the Targaryen words, "Fire and blood," marking Dorne's true allegiance. The scene is the narrative climax of AFFC's Dorne arc and the exposition hinge that closes the Queenmaker thread while opening the Essos thread.

## Quotes

- `affc-the-princess-in-the-tower-01.md:325` — "Vengeance." His voice was soft, as if he were afraid that someone might be listening. "Justice." Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, "Fire and blood."
- `affc-the-princess-in-the-tower-01.md:297` — "The pact was sealed in secret. I meant to tell you when you were old enough . . . when you came of age, I thought, but . . ."
- `affc-the-princess-in-the-tower-01.md:321` — "Your brother went with Cletus Yronwood, Maester Kedry, and three of Lord Yronwood's best young knights on a long and perilous voyage, with an uncertain welcome at its end. He has gone to bring us back our heart's desire."
```

---

### Node: death-of-quentyn-martell
```
---
slug: death-of-quentyn-martell
type: event.death
aliases:
  - death of Quentyn Martell
  - burning of Quentyn Martell
  - Quentyn burned by Rhaegal
  - Frog burned by the dragon
cite_ref: sources/chapters/adwd/adwd-the-dragontamer-01.md:267
confidence: 1
---

## Summary

After Quentyn Martell commands his sellsword allies to attack the dragon-pit guards, Rhaegal — the green dragon — strikes from behind while Quentyn is focused on trying to whip Viserion into submission. Rhaegal's fire engulfs Quentyn completely. He does not die immediately: badly burned, he survives for several days in Daenerys's pyramid before dying just before first light, as confirmed by Ser Barristan Selmy. Archibald Yronwood was found cradling Quentyn's smoldering body, his own hands burned from beating out the flames. Ser Barristan's epitaph is terse: "Not all men are meant to dance with dragons." The death closes Doran Martell's Essos gambit and sets up the return of Quentyn's bones to Dorne.

## Quotes

- `adwd-the-dragontamer-01.md:267-269` — "When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning. Oh, he thought. Then he began to scream."
- `adwd-the-queens-hand-01.md:39` — "So much of the prince's flesh had sloughed away that he could see the skull beneath. His eyes were pools of pus. He should have stayed in Dorne. He should have stayed a frog. Not all men are meant to dance with dragons."
- `adwd-the-queens-hand-01.md:45` — "Prince Quentyn died just before first light."
- `adwd-the-queens-hand-01.md:99` — "Archibald Yronwood had been cradling his prince's scorched and smoking body when the Brazen Beasts had found him, as his burned hands could testify. He had used them to beat out the flames that had engulfed Quentyn Martell."
```

---

## 6. Harvest Additions
*(appended to working/harvest-queue.md)*

| open | quote | affc | affc-the-princess-in-the-tower-01.md:47 | Arianne's first prison meal: "The kid had been roasted with lemon and honey. With it were grape leaves stuffed with a mélange of raisins, onions, mushrooms, and fiery dragon peppers." — detailed named-dish hospitality even in captivity | 2026-06-21 s120-e5-research |
| open | appearance | affc | affc-the-princess-in-the-tower-01.md:133 | Arianne's appearance before facing Doran: "a simple gown of ivory linen, with vines and purple grapes embroidered around the sleeves and bodice. She wore no jewels." — calculated dress-down for submission scene | 2026-06-21 s120-e5-research |
| open | appearance | adwd | adwd-the-queens-hand-01.md:39 | Quentyn's burned face: "So much of the prince's flesh had sloughed away that he could see the skull beneath. His eyes were pools of pus." — canonical death-appearance for quentyn-martell node | 2026-06-21 s120-e5-research |
| open | quote | adwd | adwd-the-dragontamer-01.md:199 | "'Fire and blood,' he whispered, 'blood and fire.' The blood was pooling at his feet, soaking into the brick floor." — Quentyn echoes the Targaryen words before the burning; thematic bookend to Doran's whisper at affc:325 | 2026-06-21 s120-e5-research |
| open | foreshadowing | adwd | adwd-the-dragontamer-01.md:77 | "Horses seldom turn their riders into charred bones and ashes." — Gerris's dark joke foreshadows Quentyn's death by dragon fire, spoken hours before the burning | 2026-06-21 s120-e5-research |

---

## 7. Concerns / Flags

1. **Which dragon burned Quentyn?** The text is unambiguous on close reading: Rhaegal (green, "behind you") attacks from behind while Quentyn is focused on Viserion (white, in front). The AGENT_IN edge must be `rhaegal`, not `viserion`. This is frequently confused in fan discussion; verify this is correctly attributed in any existing `rhaegal` node edges.

2. **Quentyn POV chapter self-identifies as "The Dragontamer" in frontmatter but Quentyn's real_identity is confirmed as Quentyn Martell.** The `adwd-the-dragontamer-01.md` chapter uses `pov_character: The Dragontamer` / `real_identity: Quentyn Martell` in frontmatter. The cite_ref should use the actual filename, not the POV alias.

3. **`doran-reveals-fire-and-blood-pact` node name is accurate:** The reveal IS the pact, not merely its existence. The naming correctly captures what this event IS — the disclosure act, not the pact's original formation (which is unmodeled).

4. **Betrothal to Viserys:** Doran alludes to Arianne's betrothal at line 293 and confirms the betrothed died via "a pot of molten gold" (line 309 = Viserys). This is implicit, not named. If `pact-of-dorne-and-targaryens` or similar node is ever minted, this is the textual anchor. For now, the node prose captures it in the summary.

5. **Two-chapter death:** The burning occurs in `adwd-the-dragontamer-01.md` (Quentyn POV) but death is confirmed in `adwd-the-queens-hand-01.md` (Barristan POV). The `cite_ref` anchor points to the burning moment (line 267) as the initiating event, with the Queens Hand as secondary evidence. Both should appear in ## Quotes.
