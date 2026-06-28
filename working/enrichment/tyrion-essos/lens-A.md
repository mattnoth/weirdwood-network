# Lens A — Spine + Secondary-Character Sub-Arcs — A2.4 Tyrion / Essos proposal (S161)

Chapters read: adwd-tyrion-01, adwd-tyrion-02, adwd-tyrion-08, adwd-tyrion-09, adwd-tyrion-11, adwd-tyrion-12.

---

## Proposed NEW nodes

### 1. `tyrion-arrives-at-pentos`
- **type:** event.incident
- **Summary:** Tyrion Lannister is smuggled off the ship inside a wine cask, delivered to the cellar of Illyrio Mopatis's manse in Pentos. This is the first beat after `varys-smuggles-tyrion-out-of-kings-landing` — it is the forward wire that makes that hub no longer causally islanded. The sojourn in Illyrio's manse (baths, feasts, the poisoned-mushroom test, the dragon revelation) unfolds across ch01–02.
- **Anchor quote:** "A rotting sea cow." Tyrion's mouth was full of blood. He spat it at the fat man's feet. (adwd-tyrion-01:59)
- **LOCATED_AT:** pentos (Illyrio's manse, Pentos)

### 2. `jorah-captures-tyrion-at-selhorys`
- **type:** event.incident
- **Summary:** Jorah Mormont, in search of a way back to Daenerys's favour, seizes Tyrion Lannister at a brothel in Selhorys on the upper Rhoyne. This beat is referenced directly in ch08: Tyrion still wears chains from the capture and Mormont had "removed Tyron's chains and fetters once they were safely under way." The capture is Jorah's AGENT_IN act; Tyrion is VICTIM_IN. Lens B covers ch07 directly but the aftermath is confirmed here.
- **Anchor quote (ch08 reference to prior event):** "Jorah Mormont had removed Tyron's chains and fetters once they were safely under way" (adwd-tyrion-08:17)
- **LOCATED_AT:** selhorys

### 3. `execution-of-oppo-in-volantis`
- **type:** event.incident
- **Summary:** Oppo ("Groat"), Penny's dwarf brother and performing partner, is beheaded by sailors in Volantis who mistake him for Tyrion Lannister. This is Cersei's bounty on Tyrion's head striking an innocent proxy. Ch08 contains the first-person Tyrion account of the aftermath: Penny's grief, her raw eyes, the cabin isolation, and her accusation that Tyrion bears responsibility. Penny also recounts a parallel death in Tyrosh (a juggler beheaded and divided at the Temple of Trios).
- **Anchor quote:** "They hacked off her brother's head in the hope that it was mine, yet here I sit like some bloody gargoyle, offering empty consolations." (adwd-tyrion-08:39)
- **LOCATED_AT:** volantis

### 4. `sale-of-tyrion-penny-jorah-to-yezzan`
- **type:** event.incident
- **Summary:** After the shipwreck of the Selaesori Qhoran, slavers capture Tyrion, Penny, Jorah, and the remaining crew/passengers. Tyrion engineers a bidding war at the slave auction outside Meereen's walls between Yezzan, Ben Plumm, the Girl General, and Zahrina. Yezzan bids five thousand silver pieces and wins. Tyrion + Penny become Yezzan's grotesquerie; Jorah joins as a claimed part of the act. This event is explicitly narrated in the yezzan-zo-qaggaz node and referenced throughout ch11. The capture-by-slavers beat (the slaver galley closing on the Selaesori Qhoran wreck) is the immediate precursor; the sale is the follow-through.
- **Anchor quote (ch09 — the slaver galley arrives):** "'We're downwind. I can smell her.' Mormont drew his sword. 'That's a slaver.'" (adwd-tyrion-09:215)
- **Secondary anchor (ch11 — Tyrion as Yezzan's slave):** "He was a slave in a golden collar, with little bells that tinkled cheerfully with every step he took." (adwd-tyrion-11:21)
- **LOCATED_AT:** meereen (outside the walls, the Yunkish siege camp)

### 5. `pale-mare-kills-nurse-and-yezzan`
- **type:** event.incident
- **Summary:** The bloody flux (pale mare) sweeps the Yunkish siege camp. Tyrion tends to the overseer Nurse while secretly poisoning him with mushrooms in his broth. Nurse dies. Two days later Yezzan himself is struck with the pale mare and is dying. This is the enabling condition for the escape — Yezzan's nephews flee, Scar and the soldiers lose command authority. The `bloody-flux` node (0 edges) is lit here with its first narrative-active edge (AFFLICTED_BY / KILLED_BY relationships).
- **Anchor quote:** "Two days ago Nurse had been hale and healthy. Two days ago Yezzan had not heard the pale mare's ghostly hoofbeats." (adwd-tyrion-11:25)
- **LOCATED_AT:** meereen (Yunkish siege camp, outside Meereen walls)

### 6. `tyrion-joins-the-second-sons`
- **type:** event.incident
- **Summary:** Tyrion Lannister, Penny, and Jorah Mormont walk out of the Yunkish camp under cover of water-fetching, approach the Second Sons' camp, and Tyrion talks his way in — signing promissory notes worth a lordship and one hundred thousand dragons for Ben Plumm, plus thousands for Kasporio and Inkpots. Tyrion signs the company book in blood (mixing a drop into red ink per tradition), formally enrolling as Tyrion of House Lannister. This is the arc's TERMINUS in published ADWD. Jorah and Penny also end up at the camp (though Penny is not enrolled). Tyrion immediately signals that the Second Sons should turn their cloaks back to Daenerys — the plan is conceived here, execution is TWOW.
- **Anchor quote:** "Tyrion of House Lannister, Lord of Casterly Rock, in a big bold hand, just below Jorah Mormont's far more modest signature." (adwd-tyrion-12:89)
- **LOCATED_AT:** meereen (Second Sons camp, Meereen siege lines)

---

## Proposed NEW edges

All deduped against the 180 internal-edge baseline. Existing edges marked explicitly in the Dropped section.

### Causal spine — wiring the islanded launch FORWARD

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| varys-smuggles-tyrion-out-of-kings-landing | ENABLES | tyrion-arrives-at-pentos | Tier-2 | — | "Varys had escorted him through the tunnels" (adwd-tyrion-01:31) | The smuggling is the necessary precondition; Pentos arrival is the direct next beat. Wires the islanded-forward launch hub. |
| tyrion-arrives-at-pentos | TRIGGERS | tyrion-lannister TRAVELS_TO shy-maid | Tier-2 | — | "They departed Pentos by the Sunrise Gate" (adwd-tyrion-02:1) | The Pentos sojourn ends with departure; the Shy Maid journey begins. Route through Illyrio's departure is the immediate next beat. |
| tyrion-arrives-at-pentos | LOCATED_AT | pentos | Tier-1 | — | "This is Pentos, yes? — Just so." (adwd-tyrion-01:79) | Location of the event. |
| tyrion-arrives-at-pentos | AGENT_IN | tyrion-arrives-at-pentos | *(self-ref — dropped, use participant roles below)* | | | |

### New event node — participant roles

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| tyrion-lannister | AGENT_IN | tyrion-arrives-at-pentos | Tier-1 | — | "A drunken dwarf" (adwd-tyrion-01:57) — Tyrion is decanted from the cask | Tyrion arrives; active participant |
| illyrio-mopatis | AGENT_IN | tyrion-arrives-at-pentos | Tier-1 | — | "My house is yours. Any friend of my friend across the water is a friend to Illyrio Mopatis" (adwd-tyrion-01:65) | Illyrio receives and hosts him |
| tyrion-lannister | GUEST_OF | illyrio-mopatis | *(already exists — DROPPED)* | | | |
| tyrion-arrives-at-pentos | LOCATED_AT | pentos | Tier-1 | — | "This is Pentos, yes?" (adwd-tyrion-01:79) | Location anchor |

### Jorah capture event — participant roles

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| jorah-mormont | AGENT_IN | jorah-captures-tyrion-at-selhorys | Tier-1 | — | "Jorah Mormont had removed Tyron's chains and fetters once they were safely under way" (adwd-tyrion-08:17) | Jorah held the chains, hence he was the captor |
| tyrion-lannister | VICTIM_IN | jorah-captures-tyrion-at-selhorys | Tier-1 | — | "Jorah Mormont had removed Tyron's chains and fetters once they were safely under way" (adwd-tyrion-08:17) | Tyrion was chained |
| jorah-captures-tyrion-at-selhorys | LOCATED_AT | selhorys | Tier-1 | — | "a whore who had been sitting on his cock back in Selhorys" (adwd-tyrion-08:107) | The capture happened at a brothel in Selhorys |
| jorah-captures-tyrion-at-selhorys | ENABLES | jorah-mormont TRAVELS_TO meereen | Tier-2 | — | "he was about the queen's business… He hopes to buy your way back into her favor by presenting her with me." (adwd-tyrion-09:73) | The capture gives Jorah his plan to return to Daenerys; Tyrion is the prize |
| jorah-mormont | MOTIVATES | jorah-captures-tyrion-at-selhorys | **[BORDERLINE]** Tier-2 | — | "You hope to buy your way back into her favor by presenting her with me. An ill-considered scheme, I'd say." (adwd-tyrion-09:73) | MOTIVATES target should be a CHARACTER not an event — use this as: `daenerys-targaryen [MOTIVATES] jorah-mormont` instead (he is driven to seize Tyrion TO reach Daenerys). Already `daenerys-targaryen [MOTIVATES] jorah-mormont` — check. *Not already in baseline.* Propose it. |
| daenerys-targaryen | MOTIVATES | jorah-mormont | Tier-2 | — | "You hope to buy your way back into her favor by presenting her with me." (adwd-tyrion-09:73) | Daenerys motivates Jorah's every move in this arc; the capture is his method |

**Correction to above table:** `MOTIVATES` target must be a CHARACTER (per shared rules). I propose:
`daenerys-targaryen MOTIVATES jorah-mormont` (Tier-2) — not in baseline, justified above.

### Oppo execution — participant roles + secondary-character sub-arc

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| execution-of-oppo-in-volantis | LOCATED_AT | volantis | Tier-1 | — | "the horror visited on her in Volantis" (adwd-tyrion-08:41) | Ch08 confirms Volantis as the location |
| oppo | VICTIM_IN | execution-of-oppo-in-volantis | Tier-1 | — | "They hacked off her brother's head in the hope that it was mine" (adwd-tyrion-08:39) | Oppo is the victim |
| cersei-lannister | CAUSES | execution-of-oppo-in-volantis | Tier-2 | — | "His blood is on my sister's hands, and the hands of the brutes who killed him." (adwd-tyrion-08:161) | Cersei's bounty on Tyrion's head is the root cause; the executing sailors are the proximate instrument |
| penny | MOURNS | oppo | *(already exists — DROPPED)* | | | |
| penny | SIBLING_OF | oppo | Tier-1 | full_sibling | "My brother and me. She always said it didn't matter what your voice was like…" (adwd-tyrion-08:213) | Explicit sibling relationship; `oppo` node has `aliases: Groat`, confirm this is the same person (ch08:85 Tyrion: "He hated her name. Her brother had gone by the name of Groat, though his true name had been Oppo.") |
| execution-of-oppo-in-volantis | CAUSES | penny MOURNS oppo | **[BORDERLINE]** Tier-1 | — | "by the time they raised sail she had locked herself in her cabin with her dog and her pig, but at night they could hear her weeping." (adwd-tyrion-08:41) | The execution directly causes the observable mourning state. But MOURNS is a state-edge (person→person), not an event-→state edge. Better: wire execution as VICTIM_IN oppo + penny MOURNS oppo (already exists). So this edge would be: `execution-of-oppo-in-volantis MOTIVATES penny`. MOTIVATES target must be a CHARACTER — acceptable: `execution-of-oppo-in-volantis MOTIVATES penny`. |
| execution-of-oppo-in-volantis | MOTIVATES | penny | Tier-1 | — | "Sick with grief, you mean." (adwd-tyrion-08:35) | The execution drives Penny's grief-state and her initial hostility to Tyrion throughout the arc |
| penny | COMPANION_OF | tyrion-lannister | *(already exists — DROPPED)* | | | |
| penny | COMPANION_OF | oppo | Tier-1 | — | "Oppo … he was my last family, and now he's gone too." (adwd-tyrion-08:221) | Penny and Oppo were a performing duo and siblings; their relationship is foundational |

**Note on Penny's father Hop-Bean (named in ch08):**

> "He traveled to all the Free Cities, and Westeros as well. In Oldtown they used to call him Hop-Bean." (adwd-tyrion-08:217)

Hop-Bean is Penny and Oppo's father. Penny's node doesn't record PARENT_OF edges. Propose:

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| hop-bean | PARENT_OF | penny | Tier-1 | father | "He traveled to all the Free Cities… In Oldtown they used to call him Hop-Bean." (adwd-tyrion-08:217) — Penny says "our father" |
| hop-bean | PARENT_OF | oppo | Tier-1 | father | "It was Father's idea to do the tilts… He even trained the first pig." (adwd-tyrion-08:225) | Same father, same act |

*Note: `hop-bean` may already be a node; this is a new-edge proposal regardless. If the node doesn't exist, the gate should verify and mint it as character.human.*

### Sale-to-Yezzan event — participant roles and causal web

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| tyrion-lannister | VICTIM_IN | sale-of-tyrion-penny-jorah-to-yezzan | Tier-1 | — | "He was a slave in a golden collar, with little bells that tinkled cheerfully with every step he took." (adwd-tyrion-11:21) | Tyrion enslaved |
| penny | VICTIM_IN | sale-of-tyrion-penny-jorah-to-yezzan | Tier-1 | — | "One of Yezzan's special treasures." (adwd-tyrion-11:21) | Penny enslaved |
| jorah-mormont | VICTIM_IN | sale-of-tyrion-penny-jorah-to-yezzan | Tier-1 | — | "The knight had not adapted well to bondage." (adwd-tyrion-11:127) | Jorah enslaved as part of the lot |
| yezzan-zo-qaggaz | AGENT_IN | sale-of-tyrion-penny-jorah-to-yezzan | Tier-1 | — | "Yezzan bids five thousand silver pieces for the lot and wins." (from yezzan-zo-qaggaz node, per baseline research) | Yezzan is the buyer |
| sale-of-tyrion-penny-jorah-to-yezzan | LOCATED_AT | meereen | Tier-1 | — | "slave market is set up outside Meereen" (yezzan-zo-qaggaz node) | Location |
| shipwreck-of-selaesori-qhoran | ENABLES | sale-of-tyrion-penny-jorah-to-yezzan | Tier-2 | — | "Mormont drew his sword. 'That's a slaver.'" (adwd-tyrion-09:215) — the slaver finds the drifting wreck | The shipwreck strands them, enabling the slavers to capture them. **Note:** `shipwreck-of-selaesori-qhoran` is likely a node built by Lens C (ch09-10); if it doesn't exist, use the Selaesori Qhoran wreck as the source via a note. |
| yezzan-zo-qaggaz | PURCHASED_FROM | slavers | **[BORDERLINE]** Tier-2 | — | (not directly quoted from my assigned chapters — the purchase details are in adwd-tyrion-47 which is not my chapter; proposing structurally) | PURCHASED_FROM is buyer→seller; Yezzan purchased from unnamed slavers. Flag as borderline pending ch47 quote. |

### Pale-mare-kills-Nurse-and-Yezzan — participant roles and causal web

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| yezzan-zo-qaggaz | AFFLICTED_BY | bloody-flux | Tier-1 | — | "'The pale mare,' the man told Sweets." (adwd-tyrion-11:12) | Yezzan is diagnosed with the pale mare / bloody flux |
| nurse | AFFLICTED_BY | bloody-flux | Tier-1 | — | "Sweet fresh water didn't help Nurse. Poor old Nurse. Yezzan's soldiers had tossed him onto the corpse wagon last night at dusk, another victim of the pale mare." (adwd-tyrion-11:69) | Nurse dies of the flux first |
| tyrion-lannister | KILLS | nurse | *(already exists — DROPPED)* | | | |
| tyrion-lannister | AGENT_IN | pale-mare-kills-nurse-and-yezzan | Tier-1 | — | "slivers of mushroom in the broth… The last word Nurse ever said was, 'No.' The last words he ever heard were, 'A Lannister always pays his debts.'" (adwd-tyrion-11:69) | Tyrion accelerates Nurse's death via mushrooms |
| nurse | VICTIM_IN | pale-mare-kills-nurse-and-yezzan | Tier-1 | — | "another victim of the pale mare" (adwd-tyrion-11:69) | Nurse is a victim (primary) |
| yezzan-zo-qaggaz | VICTIM_IN | pale-mare-kills-nurse-and-yezzan | Tier-1 | — | "'The pale mare,' the man told Sweets." (adwd-tyrion-11:12) | Yezzan struck down |
| pale-mare-kills-nurse-and-yezzan | LOCATED_AT | meereen | Tier-1 | — | "Meereenese morning. The air was muggy and oppressive" (adwd-tyrion-11:65) | Yunkish camp outside Meereen |
| bloody-flux | AFFLICTED_BY | yezzan-zo-qaggaz | **[BORDERLINE — direction check]** | | | AFFLICTED_BY is person→disease; use yezzan-zo-qaggaz AFFLICTED_BY bloody-flux (proposed above) |
| pale-mare-kills-nurse-and-yezzan | ENABLES | tyrion-joins-the-second-sons | Tier-1 | — | "Nurse is dead and Yezzan's dying. It could be dark before anyone thinks to miss us. We will never have a better chance than now." (adwd-tyrion-11:252) | The deaths create the window for escape — Tyrion explicitly states this |

### Tyrion-joins-the-Second-Sons — participant roles and causal web

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| tyrion-lannister | AGENT_IN | tyrion-joins-the-second-sons | Tier-1 | — | "Tyrion of House Lannister, Lord of Casterly Rock, in a big bold hand" (adwd-tyrion-12:89) | Tyrion signs the book |
| jorah-mormont | PARTICIPATES_IN | tyrion-joins-the-second-sons | Tier-1 | — | "just below Jorah Mormont's far more modest signature" (adwd-tyrion-12:89) | Jorah also signs |
| ben-plumm | AGENT_IN | tyrion-joins-the-second-sons | Tier-1 | — | "'Welcome to the Second Sons, Lord Tyrion.'" (adwd-tyrion-12:93) | Ben Plumm officially admits them |
| tybero-istarion | PARTICIPATES_IN | tyrion-joins-the-second-sons | Tier-1 | — | "'Inkpots, fetch the book.' The book was leather-bound with iron hinges" (adwd-tyrion-12:80) | Inkpots administers the signing |
| kasporio | WITNESS_IN | tyrion-joins-the-second-sons | Tier-1 | — | "Kasporio the Cunning touched his sword hilt." (adwd-tyrion-12:17) | Present and perceives the event (hostile, but a load-bearing witness) |
| tyrion-joins-the-second-sons | LOCATED_AT | meereen | Tier-1 | — | "The Second Sons are on the losing side. They need to turn their cloaks again and do it now." (adwd-tyrion-12:283) | Meereen siege lines |
| tyrion-joins-the-second-sons | ENABLES | siege-of-meereen | **[BORDERLINE]** Tier-3 | — | "The Second Sons are on the losing side. They need to turn their cloaks again and do it now." (adwd-tyrion-12:283) | BORDERLINE: the joining ENABLES the eventual Second Sons back-defection to Daenerys which affects the siege — but the back-defection itself is TWOW. The join only ENABLES a future event not yet published. Propose as Tier-3 borderline; the synthesis may want a CAUSES edge to the existing `siege-of-meereen` node as a wire-in. Safer: propose `tyrion-joins-the-second-sons PARTICIPATES_IN siege-of-meereen` or simply wire via `tyrion-lannister MEMBER_OF second-sons` (already exists). Keep this one as a borderline note for the Opus gate. |
| pale-mare-kills-nurse-and-yezzan | ENABLES | tyrion-joins-the-second-sons | Tier-1 | — | "We will never have a better chance than now." (adwd-tyrion-11:252) | *(repeated from above — keep once in final)* |

### Moqorro sub-arc (ch08) — Moqorro is on the Selaesori Qhoran but lost overboard in the storm (ch09)

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| moqorro | AGENT_IN | pale-mare-kills-nurse-and-yezzan | **DROPPED** | | | Moqorro is lost overboard in the storm (ch09:185) — he is NOT present in the Yunkish camp; he later resurfaces with Victarion. Do not attach to this event. |
| moqorro | TRAVELS_TO | meereen | **[BORDERLINE]** Tier-2 | — | "No doubt that was one reason the high priest Benerro had chosen him to bring the faith of R'hllor to Daenerys Targaryen." (adwd-tyrion-08:49) | Moqorro's mission is Meereen/Daenerys; but he goes via Victarion in the published arc — Moqorro is already in the graph at adwd-victarion-01 and has his own arc. Do NOT propose this; it's in his node already. **DROPPED.** |
| benerro | APPOINTS | moqorro | Tier-2 | — | "one reason the high priest Benerro had chosen him to bring the faith of R'hllor to Daenerys Targaryen" (adwd-tyrion-08:49) | Benerro dispatches Moqorro. This is a new edge (not in baseline). Worth proposing for the Moqorro node enrichment. |
| moqorro | SEEKS | daenerys-targaryen | Tier-1 | — | "he was chosen him to bring the faith of R'hllor to Daenerys Targaryen" (adwd-tyrion-08:49) | Moqorro's explicit mission |
| tyrion-lannister | ENCOUNTERS | moqorro | Tier-1 | — | "Tyrion squatted across from him and warmed his hands against the night's chill." (adwd-tyrion-08:45) | Tyrion and Moqorro have the fireside conversation about dragons and shadows |

### Ben Plumm sub-arc (ch11–12)

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| ben-plumm | MEMBER_OF | second-sons | **check** — baseline has `ben-plumm [COMMANDS] second-sons` and `[SWORN_TO]`; MEMBER_OF is a separate and lower-specificity edge. DROPPED as redundant with COMMANDS. |
| tyrion-lannister | MANIPULATES | ben-plumm | Tier-1 | via_flattery | "You're a clever Plumm… you know this head of mine is worth a lordship … back in Westeros, half a world away. By the time you get it there, only bone and maggots will remain." (adwd-tyrion-11:315) | Tyrion cons Ben Plumm — classic via_flattery + via_false_information combo. Use `via_flattery` as the dominant qualifier. |
| tybero-istarion | MEMBER_OF | second-sons | Tier-1 | — | "You will work for Inkpots. Keeping books, counting coin, writing contracts and letters." (adwd-tyrion-12:62) | Inkpots is the company paymaster; his membership is explicit |
| tybero-istarion | COMPANION_OF | ben-plumm | Tier-2 | — | "Inkpots, fetch the book" — Inkpots and Ben Plumm work in close concert (adwd-tyrion-12:79) | Confirmed working relationship |
| kasporio | COMPANION_OF | ben-plumm | Tier-2 | — | "One was slim and elegant, with a pointed beard, a bravo's blade" — Kasporio is present as Ben Plumm's second (adwd-tyrion-11:297) | Structural working relationship |
| jorah-mormont | ENCOUNTERS | kasporio | Tier-1 | — | "'Jorah Mormont? Is that you?… Kasporio gave him a startled look'" (adwd-tyrion-11:331) | Jorah and Kasporio know each other from past Second Sons service |
| jorah-mormont | MEMBER_OF | second-sons | *(already exists — DROPPED: baseline has jorah-mormont [MEMBER_OF] second-sons)* | | | |

### Widow of the waterfront (ch08 context)

Penny boards the Selaesori Qhoran from Volantis after being housed by the widow. The widow is already in the graph (baseline: `widow-of-the-waterfront` has core_out=0, core_in=1, boundary=1).

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| widow-of-the-waterfront | PROTECTS | penny | Tier-2 | — | "She is given a room at the inn by the widow" (from penny node, summarizing adwd-tyrion-27 which is ch08 context for the Volantis sequence) | The widow shelters the grieving Penny after Oppo's death |
| penny | GUEST_OF | widow-of-the-waterfront | Tier-2 | — | (same source: penny node states "given a room at the inn by the widow") | Penny is briefly housed at the widow's inn |

### Selaesori Qhoran shipwreck (ch09 — at boundary of Lens A scope)

The shipwreck itself unfolds at the end of ch09 (my last page read). Lens C covers ch09-10 more fully. I will note the terminal beat only.

| source | EDGE_TYPE | target | Tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| tyrion-lannister | VICTIM_IN | shipwreck-of-selaesori-qhoran | Tier-1 | — | "By the time the storm abated and the surviving passengers and crew came crawling back on deck…the Selaesori Qhoran was a broken thing" (adwd-tyrion-09:185) | Tyrion is aboard; he survives the wreck (clung to the rail) |
| penny | VICTIM_IN | shipwreck-of-selaesori-qhoran | Tier-1 | — | "In the end, they did not drown" (adwd-tyrion-09:171) | Penny is below decks; she is a victim |

*Note: `shipwreck-of-selaesori-qhoran` is likely a Lens C node; Lens A is contributing participant roles only.*

---

## Dropped / considered-but-rejected

1. **`tyrion GUEST_OF illyrio-mopatis`** — already in baseline (line 146).
2. **`penny MOURNS oppo`** — already in baseline (line 121).
3. **`penny COMPANION_OF tyrion-lannister`** — already in baseline (line 118).
4. **`jorah-mormont CAPTURES tyrion-lannister`** — already in baseline (line 91) as a bare dyad. The new event node `jorah-captures-tyrion-at-selhorys` is NEW; the bare dyad is the pre-existing edge, not re-proposed.
5. **`tyrion-lannister KILLS nurse`** — already in baseline (line 150).
6. **`jorah-mormont MEMBER_OF second-sons`** — already in baseline (line 95).
7. **`penny SWORN_TO second-sons`** — already in baseline (line 123). Actually, Penny is NOT formally enrolled in ch12 (Tyrion explicitly says "I think not" when she asks to sign). This existing edge may be wrong/premature — flagging for Opus gate review. Lens A does not re-propose it.
8. **`tyrion MANIPULATES aegon`** — already in baseline; do not re-propose.
9. **`moqorro TRAVELS_TO meereen`** — Moqorro's arc is Victarion-side; his node is enriched; not Lens A's job.
10. **False causal ladder (pure travel):** Did not propose `pentos-arrival CAUSES rhoyne-voyage CAUSES volantis-arrival CAUSES shipwreck`; these are travel sequences, not causal consequences.
11. **Moqorro prophecy / fire-visions (GATED):** Moqorro tells Tyrion he sees "A small man with a big shadow, snarling in the midst of it all." This is a prophecy reading — GATED. Did not propose any APPEARS_TO_FULFILL or SUBJECT_OF_PROPHECY edge. Noted only in Harvest.
12. **TWOW terminus:** `second-sons BETRAYS yunkai` / `second-sons MEMBER_OF daenerys-army` — these are the published TWOW excerpt outcomes. NOT proposed. Tyrion only JOINS in ADWD.
13. **`tyrion AFFLICTED_BY greyscale`** — explicitly excluded per LENS-SHARED.md. Tyrion fears it, washes obsessively, is NOT infected. No edge.
14. **illyrio-mopatis poisoned-mushroom test:** Illyrio offers buttered mushrooms potentially to test if Tyrion wants to die (ch01:191–211). This is a character-beat, not an event worthy of reification; no clear victim or clear agency of harm. Dropped — capture in node prose.
15. **`illyrios-manse` node enrichment** — the baseline shows `illyrios-manse` has 0 edges. Proposals here would be legitimate but are entity-level enrichment not event-spine, and my focus is the spine + secondary sub-arcs. Defer to synthesis or a separate entity-enrichment pass.
16. **`qavo-nogarys DEFEATS tyrion-lannister`** — already in baseline; not my chapters.
17. **Widow-of-the-waterfront INFORMS jorah-mormont about Selaesori Qhoran** — plausible from penny node summary but adwd-tyrion-08 does not contain the specific dialogue; this is adwd-tyrion-27 (ch08 is actually chapter 27 in publication order — same chapter, but the widow scene is in the first half of ch08 which describes the immediate Volantis departure context as narrated by Tyrion looking BACK from the ship). The widow scene I can cite is: "The widow should have put us on a galley" (adwd-tyrion-09:57) — Tyrion referencing the widow's recommendation indirectly. Too indirect for a Tier-1 edge; dropping.
18. **`penny SIBLING_OF oppo`** is proposed (new) but `penny [COMPANION_OF] oppo` was also considered — not in baseline and legitimate, but SIBLING_OF is more specific; propose SIBLING_OF, not the weaker COMPANION_OF.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | ADWD | adwd-tyrion-01:179 | First great Illyrio feast: "broth of crab and monkfish, and cold egg lime soup as well. Then came quails in honey, a saddle of lamb, goose livers drowned in wine, buttered parsnips, and suckling pig" |
| food | ADWD | adwd-tyrion-01:213 | Second course: "heron stuffed with figs, veal cutlets blanched with almond milk, creamed herring, candied onions, foul-smelling cheeses, plates of snails and sweetbreads, and a black swan in her plumage" |
| food | ADWD | adwd-tyrion-01:247 | Dessert: "black cherries in sweet cream for them both" |
| food | ADWD | adwd-tyrion-01:187 | The mushroom course: "Mushrooms … Kissed with garlic and bathed in butter." (Illyrio may be offering them as a death-test) |
| food | ADWD | adwd-tyrion-01:107 | Illyrio's wine cellar: "sweet reds from the Reach and sour reds from Dorne, pale Pentoshi ambers, the green nectar of Myr, three score casks of Arbor gold, even wines from the fabled east, from Qarth and Yi Ti and Asshai by the Shadow" |
| food | ADWD | adwd-tyrion-02:31 | Litter breakfast: "spiced sausage that morning, washed down with a dark smokeberry brown. Jellied eels and Dornish reds filled their afternoon. Come evening there were sliced hams, boiled eggs, and roasted larks stuffed with garlic and onions, with pale ales and Myrish fire wines" |
| food | ADWD | adwd-tyrion-02:155 | Cold capon and carrot-raisin-lime-orange relish in the litter |
| food | ADWD | adwd-tyrion-02:121 | Garlic snails from Illyrio's gardens, roasted chestnuts |
| food | ADWD | adwd-tyrion-08:117 | Shipboard: "buttered beets, cold fish stew, and biscuits that could have been used to drive nails" |
| food | ADWD | adwd-tyrion-08:129 | Captain's wine: "Closer to piss than Arbor gold, if truth be told, but even piss tastes better than the black tar rum the sailors drink" |
| food | ADWD | adwd-tyrion-11:69 | Tyrion poisons Nurse: "nice hot dogtail soup, with slivers of mushroom in the broth" — poisoned mushrooms reappear (mirrors the ch01 mushroom test) |
| food | ADWD | adwd-tyrion-12:179–187 | KL nostalgia — bowl o' brown from the Flea Bottom pot shop: "So thick you could stand your spoon up in the bowl, with chunks of this and that" — Kem's reminiscence. Tyrion calls it "Singer's stew." |
| description | ADWD | adwd-tyrion-01:55 | Illyrio's first physical description: "grotesque fat man with a forked yellow beard … His bedrobe was large enough to serve as a tourney pavilion … a huge white belly and a pair of heavy breasts that sagged like sacks of suet covered with coarse yellow hair" |
| description | ADWD | adwd-tyrion-01:159 | Illyrio's jewels: "Jewels danced when he moved his hands; onyx and opal, tiger's eye and tourmaline, ruby, amethyst, sapphire, emerald, jet and jade, a black diamond, and a green pearl" |
| description | ADWD | adwd-tyrion-01:119 | Tyrion's poisonous mushrooms: "Pale white they were, with speckles, and red-ribbed undersides dark as blood" — he picks 7, stores them |
| description | ADWD | adwd-tyrion-02:165 | Serra's silver locket: "a painted likeness of a woman with big blue eyes and pale golden hair streaked by silver" — Illyrio's dead wife |
| description | ADWD | adwd-tyrion-08:13 | Moqorro first appearance: "taller than Ser Jorah and wide enough to make two of him … scarlet robes embroidered at sleeve and hem and collar with orange satin flames. His skin was black as pitch, his hair as white as snow; the flames tattooed across his cheeks and brow yellow and orange. His iron staff … crowned with a dragon's head; when he stamped its butt upon the deck, the dragon's maw spat crackling green flame." |
| description | ADWD | adwd-tyrion-08:179 | Penny at the rail: "From behind, she looked as small and vulnerable as a child." |
| description | ADWD | adwd-tyrion-09:13 | The jousting armor: "The painted wooden armor clattered as Pretty trotted across the deck." |
| description | ADWD | adwd-tyrion-11:131 | Jorah after cage-beatings: "Both eyes blackened and his back crusty with dried blood. His face was so bruised and swollen that he hardly looked human." |
| description | ADWD | adwd-tyrion-12:213 | Jorah in company armor: "his left greave did not match his right, his gorget was spotted with rust, his vambraces rich and ornate, inlaid with niello flowers. On his right hand was a gauntlet of lobstered steel, on his left a fingerless mitt of rusted mail. The nipples on his muscled breastplate had a pair of iron rings through them. His greathelm sported a ram's horns, one of which was broken." |
| description | ADWD | adwd-tyrion-12:213 | Jorah's demon-brand: "The demon's mask the slavers had burned into his right cheek to mark him for a dangerous and disobedient slave would never leave him." |
| quote (load-bearing) | ADWD | adwd-tyrion-08:49 | Moqorro to Tyrion: "Dragons old and young, true and false, bright and dark. And you. A small man with a big shadow, snarling in the midst of all." |
| quote (load-bearing) | ADWD | adwd-tyrion-11:252 | Tyrion to Penny: "Nurse is dead and Yezzan's dying. It could be dark before anyone thinks to miss us. We will never have a better chance than now." |
| quote (load-bearing) | ADWD | adwd-tyrion-11:319 | Tyrion to Ben Plumm: "I was born a second son. This company is my destiny." |
| quote (load-bearing) | ADWD | adwd-tyrion-12:283 | Tyrion to Penny and Jorah: "The Second Sons are on the losing side. They need to turn their cloaks again and do it now. Leave that to me." |
| foreshadowing | ADWD | adwd-tyrion-09:205 | Tyrion's nightmare: "he was back in King's Landing again, a crossbow in his hand. 'Wherever whores go,' Lord Tywin said, but when Tyrion's finger clenched and the bowstring thrummed, it was Penny with the quarrel buried in her belly." |
| hospitality | ADWD | adwd-tyrion-01:65 | Illyrio: "My house is yours. Any friend of my friend across the water is a friend to Illyrio Mopatis" — formal hospitality offer |
| hospitality | ADWD | adwd-tyrion-01:197 | Illyrio: "In the Seven Kingdoms it is considered a grave breach of hospitality to poison your guest at supper." (Tyrion, testing Illyrio on the mushrooms) |
| curiosity | ADWD | adwd-tyrion-02:165 | Illyrio's dead wife Serra: "I found her in a Lysene pillow house and brought her home to warm my bed, but in the end I wed her… I keep her hands in my bedchamber. Her hands that were so soft…" — deeply personal; potential Serra-Illyrio backstory edge for the node |
| curiosity | ADWD | adwd-tyrion-08:265 | Moqorro's nightfire vision: "One most of all. A tall and twisted thing with one black eye and ten long arms, sailing on a sea of blood." (reference to Euron Greyjoy — theory-gated but a pointer) |
| curiosity | ADWD | adwd-tyrion-09:81 | Company book inscription: "Aegor Rivers served a year with us, before he left to found the Golden Company… The Bright Prince, Aerion Targaryen, he was a Second Son. And Rodrik Stark, the Wandering Wolf" — historical Second Sons members, possible graph edges |
