# Lens 2 — Secondary Character Substrate + SUSPECTED_OF + WITNESS_IN
# Sack of King's Landing (283 AC) — Enrichment Dip

> Written 2026-06-24. Proposals only — nothing minted. All quotes line-checked against source files.
> Dedup baseline: `working/enrichment/sack-of-kl/baseline.md`

---

## VERIFICATION LOG — Slug Lookups

The following slugs are confirmed in the baseline as existing nodes — no re-minting needed:

- `belis` ✓ (baseline §Existing character/object nodes)
- `garigus` ✓ (baseline §Existing character/object nodes)
- `qarlton-chelsted` ✓ (baseline §Existing character/object nodes)
- `rossart` ✓ (already AGENT_IN wildfire-plot — confirmed baseline)
- `roland-crakehall` ✓ (baseline §Existing character/object nodes)
- `eddard-stark` ✓ (baseline §Existing character/object nodes)
- `wildfire-plot` ✓ (baseline §The wildfire thread)
- `aerys-commands-the-city-burned` ✓ (baseline §The 4 existing sub-beats)
- `slaying-of-aerys-ii-the-kingslaying` ✓ (baseline §The 4 existing sub-beats)
- `iron-throne` ✓ (baseline §Existing character/object nodes — slug confirmed as `iron-throne`)
- `jaime-lannister` ✓ (baseline §AGENT_IN sack)

**What is NOT yet wired per baseline:**
- `belis` and `garigus` — not yet AGENT_IN wildfire-plot
- `qarlton-chelsted` — not yet VICTIM_IN or AGENT_IN anything
- `roland-crakehall` — not yet wired to any sack event
- Jaime seated on the Iron Throne after the kingslaying — unwired beat
- `wildfire-plot` not wired to `aerys-commands-the-city-burned`

---

## PROPOSED EDGES / NODES

### P1 — `belis` AGENT_IN `wildfire-plot` (Tier 1, book-provenance)

**Source:** `asos-jaime-05.md`, lines ~54–63

**Verbatim quote:**
> "Everything was done in the utmost secrecy by a handful of master pyromancers. They did not even trust their own acolytes to help. … Aerys's new mace-and-dagger Hand was not utterly stupid, and with Rossart, Belis, and Garigus coming and going night and day, he became suspicious."

And:
> "Days later, I hunted down the others and slew them as well. Belis offered me gold, and Garigus wept for mercy."

**Rationale:** Belis is textually named as one of the three master pyromancers placing wildfire caches for Aerys — the same wildfire-plot already anchored by Rossart. The killings are confirmed on-page (Jaime's direct confession in the bath); both Belis and Garigus are book-canon participants, not wiki-only.

**Evidence kind:** book-pass1 (Jaime V, ASOS ch. 38)

---

### P2 — `garigus` AGENT_IN `wildfire-plot` (Tier 1, book-provenance)

**Source:** same passage as P1 — `asos-jaime-05.md`, lines ~54–63

**Verbatim quote (same citation, second name):**
> "with Rossart, Belis, and Garigus coming and going night and day, he became suspicious."
> "Garigus wept for mercy. Well, a sword's more merciful than fire, but I don't think Garigus much appreciated the kindness I showed him."

**Rationale:** Identical standing to Belis — textually named co-conspirator of the wildfire-plot. Wiring all three named pyromancers closes a clear gap: the node exists, the evidence is crisp, the slot was open.

**Evidence kind:** book-pass1 (Jaime V, ASOS ch. 38)

---

### P3 — `qarlton-chelsted` VICTIM_IN `aerys-commands-the-city-burned` (Tier 1, book-provenance)

**Source:** `asos-jaime-05.md`, lines ~55–56

**Verbatim quote:**
> "He did all he could to dissuade him. He reasoned, he jested, he threatened, and finally he begged. When that failed he took off his chain of office and flung it down on the floor. Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite pyromancer."

**Rationale:** Chelsted was burned by Aerys as a direct consequence of refusing the wildfire plan — making him a victim of Aerys's incendiary madness, the same madness that drove `aerys-commands-the-city-burned`. The beat-node covers Aerys's command to burn the city; Chelsted's immolation is the closest on-page precursor event, contemporaneous with the command-phase. `aerys-commands-the-city-burned` is the most appropriate existing hub. Tier 1: quote is Jaime's direct eyewitness first-person account.

**Note on `qarlton-chelsted`:** The White Book (asos-jaime-08) does not mention Chelsted by name; his existence is from Jaime's bath confession only. If there is a question whether the existing node spells him "Qarlton" — the baseline uses `qarlton-chelsted`, which matches the standard wiki spelling. No new node needed.

**Evidence kind:** book-pass1 (Jaime V, ASOS ch. 38)

---

### P4 — `roland-crakehall` WITNESS_IN `slaying-of-aerys-ii-the-kingslaying` (Tier 1, book-provenance)

**Source:** `asos-jaime-02.md`, lines ~297–304

**Verbatim quote:**
> "Ser Elys Westerling and Lord Crakehall and others of his father's knights burst into the hall in time to see the last of it, so there was no way for Jaime to vanish and let some braggart steal the praise or blame."
> "'The castle is ours, ser, and the city,' Roland Crakehall told him…"

**Rationale:** Roland Crakehall is textually present and perceiving — "burst into the hall in time to see the last of it" — meeting the WITNESS_IN gate (present + perceiving the event's conclusion). He also delivered the status report to Jaime, making him the named POV contact in that hall. This is the Ned-found-Jaime complement: Crakehall arrived during/immediately at the conclusion of the killing, not after the fact the way Ned did.

**Contrast with Eddard-Stark (REJECTED for WITNESS_IN):** Ned arrived *after* the killing was complete — "Aerys was dead on the floor, drowned in his own blood" is what Ned describes. The hall was already settled. Ned was not present for the act. Roland Crakehall and Ser Elys Westerling arrived while "the last of it" was still visible. Ned fails the gate; Crakehall passes.

**Evidence kind:** book-pass1 (Jaime II, ASOS ch. 12)

---

### P5 — `wildfire-plot` ENABLES `aerys-commands-the-city-burned` (Tier 1, book-provenance)

**Source:** `asos-jaime-05.md`, lines ~53–58

**Verbatim quote:**
> "His Grace commanded his alchemists to place caches of wildfire all over King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself."
> "The traitors want my city, I heard him tell Rossart, but I'll give them naught but ashes."

**Rationale:** The wildfire-plot (the 283 AC cache-placement) is the logistical precondition for the burn-command. Without the caches in place, Aerys's command to "burn them all" would be an impotent madman's cry. The caches are what make the command operationally credible and what compels Jaime to act before a pyromancer can relay it. The baseline explicitly flags this gap: "wildfire-plot is NOT wired to `aerys-commands-the-city-burned`."

**Important caution:** This ENABLES edge does NOT conflate `wildfire-plot` with `wildfire-trap-on-the-blackwater` (S138 deliberately kept separate). This edge runs: `wildfire-plot` → ENABLES → `aerys-commands-the-city-burned`, staying entirely in the 283 AC context. No Blackwater entanglement.

**Evidence kind:** book-pass1 (Jaime V, ASOS ch. 38)

---

### P6 — `jaime-lannister` LOCATED_AT `iron-throne` [post-kingslaying scene] — NOTE: propose as a beat-node, not a bare location edge

**Adjudication:** The scene of Jaime seated on the Iron Throne is textually vivid and consequential — it is the moment that seals his reputation in Ned's eyes. However:
- A bare `jaime LOCATED_AT iron-throne` edge loses the narrative weight and doesn't capture *why* it matters (Ned's judgment, the Kingslayer reputation).
- The better proposal is a **new beat-node** for this scene.

**PROPOSED NODE (new event):** `jaime-found-seated-on-the-iron-throne` (event.incident)
- `SUB_BEAT_OF slaying-of-aerys-ii-the-kingslaying` (it is the immediate aftermath)
- `jaime-lannister AGENT_IN` (he chose to sit there)
- `eddard-stark WITNESS_IN` (textually present, perceiving — "I rode the length of the hall in silence … I stopped in front of the throne, looking up at him")
- `roland-crakehall WITNESS_IN` (already present per asos-jaime-02)
- `LOCATED_AT iron-throne`
- **Tier 1** — both POV accounts (Ned's in agot-eddard-02, Jaime's in asos-jaime-02)

**Source for Ned's witness:** `agot-eddard-02.md`, lines ~151–156

**Verbatim quote (Ned's account):**
> "Aerys was dead on the floor, drowned in his own blood. His dragon skulls stared down from the walls. Lannister's men were everywhere. Jaime wore the white cloak of the Kingsguard over his golden armor. I can see him still. Even his sword was gilded. He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head."
> "I was still mounted. I rode the length of the hall in silence, between the long rows of dragon skulls. … I stopped in front of the throne, looking up at him."

**Source for Jaime's account:** `asos-jaime-02.md`, lines ~302–304

**Verbatim quote (Jaime's account):**
> "Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom. As it happened, it had been Eddard Stark."

**WITNESS_IN gate for Eddard-Stark (this beat ONLY):** Ned is textually present and perceiving the scene of Jaime on the throne — he rides down the hall, stops before it, watches, waits. This is not "arriving after the fact" in an abstract sense; the *throne scene* is what Ned observes. He was not present for the killing (Aerys was already dead when Ned arrived), so `eddard-stark WITNESS_IN slaying-of-aerys-ii-the-kingslaying` fails. But `eddard-stark WITNESS_IN jaime-found-seated-on-the-iron-throne` passes — that scene was ongoing when Ned entered.

**Additional edge from this beat:**
- `jaime-found-seated-on-the-iron-throne CAUSES` [Kingslayer reputation / Ned's judgment of Jaime] — but there is no existing "kingslayer-reputation" node. Flag as a character-arc consequence note rather than a minted edge.

---

## REJECTED PROPOSALS

**`eddard-stark WITNESS_IN slaying-of-aerys-ii-the-kingslaying`** — REJECTED.

Ned's account (agot-eddard-02, line 151): "Aerys was dead on the floor" — past tense, completed act. Ned arrived to find an aftermath, not an unfolding event. WITNESS_IN gate requires presence at the event itself, not its aftermath. Precedent: quincy-cox dropped S141. This fails the same gate.

**`varys SUSPECTED_OF` saving/swapping Aegon** — GATED. Theory-level, no book-text anchor in the chapters surveyed. Parked for the theories track only; do NOT mint any edge.

**`robert-baratheon AGENT_IN murder-of-elia-martell-and-rhaegars-children`** — NOT proposed. Robert condoned ("I see no babes, only dragonspawn") but the text (agot-eddard-02, line 71) frames this as a retrospective reaction, not a command. The baseline already notes this rift. COMMANDS_IN or AGENT_IN would overstate his causal role. The Ned↔Jaime contempt seam is downstream of the existing `murder-of-elia MOTIVATES eddard-stark` edge.

---

## HARVEST

Items found while reading that don't rise to a proposed edge — pointers for later harvest passes:

1. `asos-jaime-05.md` / ~line 57 / **quote/foreshadowing** / Aerys: *"Like Aerion Brightfire before him, Aerys thought the fire would transform him … that he would rise again, reborn as a dragon, and turn all his enemies to ash."* — Aerys/dragon-mythology; connects to Targaryen fire-madness pattern; possible foreshadowing overlay for Dany/dragon-birth arc.

2. `asos-jaime-05.md` / ~line 53 / **location/worldbuilding** / Wildfire cache locations named: "Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself." — detailed geography; if a wildfire-cache-locations node or map overlay is ever built, this is the textual anchor.

3. `asos-jaime-05.md` / ~line 56 / **characterization** / Chelsted's dignity: "He did all he could to dissuade him. He reasoned, he jested, he threatened, and finally he begged. When that failed he took off his chain of office and flung it down on the floor." — an act of principled defiance that could anchor Chelsted's character description in his node.

4. `asos-jaime-02.md` / ~line 263 / **quote/characterization** / Jaime on Rossart: *"I ought to have drowned Rossart instead of gutting him."* — darkly wry; a good evidence quote for the slaying-of-aerys beat or Jaime's white-book page.

5. `asos-jaime-02.md` / ~lines 291–295 / **quote/characterization** / Aerys's last moments, Jaime's POV: *"Those purple eyes grew huge then, and the royal mouth drooped open in shock. He lost control of his bowels, turned, and ran for the Iron Throne. … Jaime hauled the last dragonking bodily off the steps, squealing like a pig and smelling like a privy. A single slash across his throat was all it took to end it. … A king should die harder than this."* — the most visceral on-page account of the kingslaying; highly load-bearing for evidence_quote on `slaying-of-aerys-ii-the-kingslaying`; currently no quote is attached to that beat per baseline.

6. `asos-jaime-02.md` / ~line 299 / **character wiring** / Ser Elys Westerling also "burst into the hall" with Crakehall — another named Lannister knight WITNESS_IN the throne scene. Lower priority than Crakehall (less narratively prominent), but exists as a node candidate if the witness substrate is ever expanded.

7. `asos-jaime-05.md` / meal scene lines ~109–183 / **food/hospitality** / Roose Bolton's Harrenhal supper with Jaime and Brienne: "spread of cheese, bread, cold meat, and fruit" / Elmar pours red wine for Jaime, water for Brienne, hippocras for Bolton / Bolton eats prunes ("help move the bowels") and roasted meat (blood running across his plate, stabbed with his dagger) / oatcakes and salt fish mentioned as earlier provisions. — Full hospitality context; Bolton's fastidious eating contrasted with his cold nature; maximally capture-worthy for food/hospitality layer.

8. `asos-jaime-02.md` / ~line 85 / **food/hospitality** / Inn of the Kneeling Man meal: "charred three huge horse steaks and fried the onions in bacon grease, which almost made up for the stale oatcakes. Jaime and Cleos drank ale, Brienne a cup of cider." / earlier provisions = "oatcakes and salt fish" for the midnight camp meal. — Full meal description at a named inn; the inn name itself is notable (Aegon's conquest callback).

---

## SUMMARY

**5 solid proposals** (2 node-wirings for the pyromancer pair, 1 victim-of-Aerys wiring for Chelsted, 1 witness for Crakehall, 1 causal seam closing the wildfire-plot→burn-command gap) **+ 1 beat-node proposal** (the Iron Throne scene, with Eddard as a properly-gated WITNESS_IN for *this specific beat*).

**Key adjudication:** Eddard WITNESS_IN the kingslaying itself = REJECTED (aftermath). Eddard WITNESS_IN `jaime-found-seated-on-the-iron-throne` = PASSES (ongoing scene when Ned arrives, textually anchored in both POV chapters).

**On-page vs. wiki:** All three pyromancer killings (Rossart, Belis, Garigus) are confirmed **on-page** in Jaime's bath confession (asos-jaime-05). Not wiki-only.

**Harvest:** 8 items, including the most load-bearing verbatim kingslaying quote currently missing from the beat node, plus two full meal descriptions.
