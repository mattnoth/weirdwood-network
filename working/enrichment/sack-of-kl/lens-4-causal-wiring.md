# Lens 4 — Causal Wiring (existing-node↔existing-node cross-arc seams)
# Sack of King's Landing arc, S142 double-dip

> Lens: causal/agency edges between two ALREADY-BUILT nodes, with special focus on
> seams bridging the Sack to other arcs. Propose-only; no minting.

---

## Verification Log — Slug Existence Checks

All slugs verified via `graph-query.py --neighbors` or direct node file check before proposing:

| Slug | Exists? | Note |
|------|---------|------|
| `wildfire-plot` | YES | event.battle — 3 out, 3 in |
| `aerys-commands-the-city-burned` | YES | event.incident — 1 in (COMMANDS_IN aerys only) |
| `slaying-of-aerys-ii-the-kingslaying` | YES | event.assassination — 2 out, 4 in |
| `wildfire-trap-on-the-blackwater` | YES | event.battle — 1 out, 2 in |
| `battle-of-the-blackwater` | YES | (parent of above) |
| `belis` | YES | character.human — 0 incoming edges |
| `garigus` | YES | character.human — 0 incoming edges |
| `qarlton-chelsted` | YES | character.human — 0 incoming edges |
| `murder-of-elia-martell-and-rhaegars-children` | YES | event.assassination — 4 out, 6 in |
| `doran-martell` | YES | character.human |
| `doran-reveals-fire-and-blood-pact` | YES | event.incident — 0 outgoing |
| `coronation-of-robert-i-baratheon` | YES | event.coronation — 1 out, 1 in |

---

## WILDFIRE-CACHES → BLACKWATER SEAM: Adjudication

**Verdict: TEXT-DIRECT. Propose as ENABLES with Tier-1 confidence.**

The question was whether Tyrion's Blackwater wildfire literally drew on Aerys's 283 AC caches —
or whether "King Aerys's fickle fruits" (acok-tyrion-13:19) was merely Tyrion's colorful nickname
for the wildfire substance in general.

The answer is in ACOK Tyrion XI:

> "Another cache of Lord Rossart's was found, more than three hundred jars. Under the Dragonpit!
> Some whores have been using the ruins to entertain their patrons, and one of them fell through
> a patch of rotted floor into a cellar."
> — acok-tyrion-11:107 (Hallyne to Tyrion)

This is Hallyne confirming that Rossart's cached wildfire (Aerys's pyromancer, central agent in
`wildfire-plot`) was physically recovered and folded into Tyrion's 13,000-jar arsenal.
Then at acok-tyrion-13:19 Tyrion calls the wildfire "King Aerys's fickle fruits" precisely
BECAUSE he knows they are Aerys's/Rossart's surviving stores. This is not colloquial — it is
accurate attribution. The surviving-caches ENABLES seam is TEXT-DIRECT, not an inference.

**S138 kept these nodes separate (correctly — they are distinct events, 16 years apart), but
the two ARE causally connected by the discovered cache. The ENABLES seam is real and should
be wired, with the Dragonpit-cache quote as the evidence anchor.**

---

## PROPOSED EDGES

---

### EDGE 1 — Wildfire caches enable the Blackwater trap (CROSS-ARC HIGH VALUE)

```
wildfire-plot --ENABLES--> wildfire-trap-on-the-blackwater
```

- **Tier:** Tier-1
- **Edge type:** ENABLES (necessary precondition — a portion of the Blackwater arsenal came
  from Rossart's surviving 283 AC stores; without the Dragonpit find the 13,000-jar count
  drops by 300+ and the operational window tightens, though Tyrion's own production was the
  bulk of the arsenal)
- **Ref:** `sources/chapters/acok/acok-tyrion-11.md:107` (Hallyne confirms Rossart-cache
  discovery) + `sources/chapters/acok/acok-tyrion-13.md:19` (Tyrion attributes the weapons
  to Aerys)
- **Evidence quote (primary):**
  > "Another cache of Lord Rossart's was found, more than three hundred jars. Under the Dragonpit!
  > Some whores have been using the ruins to entertain their patrons, and one of them fell through
  > a patch of rotted floor into a cellar."
  — Hallyne to Tyrion, ACOK Tyrion XI (`acok-tyrion-11.md:107`)
- **Evidence quote (attribution):**
  > "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the
  > hungry flames."
  — Tyrion POV, ACOK Tyrion XIII (`acok-tyrion-13.md:19`)
- **Rationale:** The Dragonpit cache quote establishes that Rossart's surviving 283 AC stores
  (the material output of `wildfire-plot`) were physically incorporated into Tyrion's
  Blackwater arsenal. The "King Aerys's fickle fruits" attribution at the battle confirms
  Tyrion knew this. ENABLES is the right type: the caches were a precondition-contribution to
  the Blackwater trap, not its direct sufficient cause (Tyrion's planning + Hallyne's new
  production drove the bulk). The two nodes remain distinct events; this edge wires the causal
  thread across 16 years.
- **NOTE FOR ORCHESTRATOR:** This is the contested seam S138 deliberately deferred. The
  Dragonpit passage makes it text-direct. The ENABLES type correctly reflects the partial
  precondition (not full causation). The two nodes should remain separate. Recommend: add
  the Dragonpit quote to `wildfire-trap-on-the-blackwater.node.md` ## Quotes.

---

### EDGE 2 — Wildfire-plot ENABLES aerys-commands-the-city-burned (WITHIN-ARC INTEGRATION)

```
wildfire-plot --ENABLES--> aerys-commands-the-city-burned
```

- **Tier:** Tier-1
- **Edge type:** ENABLES (the caches ARE the precondition — Aerys could not issue the
  burn-order without the wildfire having been placed; the plot is the mechanism the command
  activates)
- **Ref:** `sources/chapters/asos/asos-jaime-05.md:53–57` (Jaime's bath confession: Aerys
  commands wildfire placement, then Aerys gives the burn-order to Rossart)
- **Evidence quote:**
  > "So His Grace commanded his alchemists to place caches of wildfire all over King's Landing.
  > Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all
  > seven gates, even in the cellars of the Red Keep itself."
  — then —
  > "The traitors want my city, I heard him tell Rossart, but I'll give them naught but ashes."
  — Jaime's confession, ASOS Jaime V (`asos-jaime-05.md:53,57`)
- **Rationale:** The placement of caches (wildfire-plot) is the necessary precondition for
  Aerys's burn-order (aerys-commands-the-city-burned) to be executable. Without the caches,
  the command is empty. The baseline notes that `aerys-commands-the-city-burned` has only
  1 inbound edge (COMMANDS_IN aerys) — this gap is the clearest within-arc missing wire.
  ENABLES, not CAUSES: Aerys's free choice to issue the order is the intervening agency;
  the wildfire-plot is the precondition he activates.

---

### EDGE 3 — Belis AGENT_IN wildfire-plot

```
belis --AGENT_IN--> wildfire-plot
```

- **Tier:** Tier-1
- **Edge type:** AGENT_IN
- **Ref:** `sources/chapters/asos/asos-jaime-05.md:55`
- **Evidence quote:**
  > "Everything was done in the utmost secrecy by a handful of master pyromancers. They did not
  > even trust their own acolytes to help. [...] with Rossart, Belis, and Garigus coming and going
  > night and day, he became suspicious."
  — Jaime's confession, ASOS Jaime V (`asos-jaime-05.md:55`)
- **Rationale:** Belis is named alongside Rossart and Garigus as one of the three master
  pyromancers executing the wildfire-plot. Rossart is already wired; Belis (existing node,
  0 incoming edges) is not. This is a direct on-page cite.

---

### EDGE 4 — Garigus AGENT_IN wildfire-plot

```
garigus --AGENT_IN--> wildfire-plot
```

- **Tier:** Tier-1
- **Edge type:** AGENT_IN
- **Ref:** `sources/chapters/asos/asos-jaime-05.md:55,63`
- **Evidence quote:**
  > "with Rossart, Belis, and Garigus coming and going night and day"
  — and —
  > "Garigus wept for mercy. Well, a sword's more merciful than fire, but I don't think Garigus
  > much appreciated the kindness I showed him."
  — Jaime's confession, ASOS Jaime V (`asos-jaime-05.md:55,63`)
- **Rationale:** Garigus is named directly alongside Rossart and Belis as a co-executor of
  the wildfire-plot. Existing node, 0 incoming edges. Jaime's "Days later, I hunted down the
  others" (asos-jaime-05:63) also confirms Garigus was killed post-Sack, but a
  separate VICTIM_IN edge for that killing is out of scope here (it would require a
  distinct pyromancer-hunt event node or attaching to the slaying — that's Lens 2/3
  territory).

---

### EDGE 5 — Qarlton Chelsted VICTIM_IN wildfire-plot

```
qarlton-chelsted --VICTIM_IN--> wildfire-plot
```

- **Tier:** Tier-1
- **Edge type:** VICTIM_IN (burned alive by Aerys for opposing the plot)
- **Ref:** `sources/chapters/asos/asos-jaime-05.md:55`
- **Evidence quote:**
  > "He did all he could to dissuade him. He reasoned, he jested, he threatened, and finally he
  > begged. When that failed he took off his chain of office and flung it down on the floor.
  > Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite
  > pyromancer."
  — Jaime's confession, ASOS Jaime V (`asos-jaime-05.md:55`)
- **Rationale:** Chelsted (Hand of the King) directly opposed the wildfire plot and was
  killed by Aerys as a consequence. He is the human cost of wildfire-plot's internal
  politics — a first-class victim who is currently unwired to the event (0 incoming edges).
  VICTIM_IN is the correct type: he suffered lethal harm as a direct result of the event's
  execution.

---

### EDGE 6 — murder-of-elia MOTIVATES doran-reveals-fire-and-blood-pact (CROSS-ARC SEAM)

```
murder-of-elia-martell-and-rhaegars-children --MOTIVATES--> doran-reveals-fire-and-blood-pact
```

- **Tier:** Tier-2
- **Edge type:** MOTIVATES (routes through Doran's long-game agency — the murder is the
  grievance he has nursed for 17 years; the reveal is the moment he finally acts on it by
  bringing Arianne into the secret)
- **Ref:** `sources/chapters/affc/affc-the-princess-in-the-tower-01.md:293,297,325`
- **Evidence quote:**
  > "Vengeance." His voice was soft, as if he were afraid that someone might be listening.
  > "Justice." Prince Doran pressed the onyx dragon into her palm with his swollen, gouty
  > fingers, and whispered, "Fire and blood."
  — Doran's reveal, AFFC The Princess in the Tower (`affc-the-princess-in-the-tower-01.md:325`)
- **Rationale:** Doran's entire covert Targaryen pact is the Dornish answer to the murder of
  Elia and her children. His first word in the reveal is "Vengeance." The `doran-reveals-fire-
  and-blood-pact` node currently has 0 outgoing edges and no upstream connection to the
  283 AC murder that motivated the pact. This seam bridges a 17-year causal chain: Sack (283
  AC) → Dornish long game → Doran reveals pact (300 AC). MOTIVATES is correct: the murder is
  the emotional-political motivation routed through Doran's decade-long patience and his
  eventual choice to bring Arianne into the secret.
- **INFERENCE FLAG:** The causal chain is long (17 years) and routes through Doran's
  undated, undocumented original pact-making with Viserys. The text does not say "because
  Elia was murdered, Doran made the Targaryen pact" — it implies it through the "Vengeance /
  Justice" framing. This is a strong, widely-accepted narrative inference, but it is an
  inference. Tier-2 is appropriate; consider annotating with `inferred: true`.

---

## EDGES NOT PROPOSED — With Reasoning

### Slaying-of-Aerys PREVENTS city-burning

The `slaying-of-aerys-ii-the-kingslaying --PREVENTS--> aerys-commands-the-city-burned`
direction considered by the prompt is **backwards temporally**: Aerys issues the command
(aerys-commands-the-city-burned) *before* Jaime kills him. The killing prevents the command's
*execution*, not the command itself. The right formulation would be:
`slaying-of-aerys-ii-the-kingslaying --PREVENTS--> [city burning as outcome]` — but there is
no existing node for "the city being burned" as an unrealized outcome event. PREVENTS requires
two existing nodes. Without a "King's Landing wildfire detonation" unrealized-event node
(not built), this edge cannot be cleanly modeled from existing slugs. **Do not propose.**

### Sack ENABLES Tywin's Handship / Lannister ascendancy

There is no existing node for "Tywin as Hand" or "Lannister ascendancy" as discrete events.
The `coronation-of-robert-i-baratheon` already CAUSED by sack, and the wedding
(`wedding-of-robert-i-baratheon-and-cersei-lannister`) is already downstream of the
coronation. The Lannister-Baratheon political union is captured through that chain.
**No new slug pair to wire.**

### Slaying-of-Aerys → Jaime's "Kingslayer" reputation

There is no existing node for the Kingslayer reputation or Ned-finds-Jaime-on-the-throne
beat. Lens 2 may be proposing a beat node for this (check before any mint). The AGOT Eddard
II text is rich (agot-eddard-02:151–155), but without a target node to wire to, PREVENTS
this lens from proposing here. **Out of scope for Lens 4.**

---

## Summary

| # | Edge | Type | Tier | Arc span |
|---|------|------|------|----------|
| 1 | `wildfire-plot --ENABLES--> wildfire-trap-on-the-blackwater` | ENABLES | 1 | CROSS-ARC (283→299 AC) |
| 2 | `wildfire-plot --ENABLES--> aerys-commands-the-city-burned` | ENABLES | 1 | Within-arc |
| 3 | `belis --AGENT_IN--> wildfire-plot` | AGENT_IN | 1 | Within-arc |
| 4 | `garigus --AGENT_IN--> wildfire-plot` | AGENT_IN | 1 | Within-arc |
| 5 | `qarlton-chelsted --VICTIM_IN--> wildfire-plot` | VICTIM_IN | 1 | Within-arc |
| 6 | `murder-of-elia-martell-and-rhaegars-children --MOTIVATES--> doran-reveals-fire-and-blood-pact` | MOTIVATES | 2 | CROSS-ARC (283→300 AC) |

**Total: 6 edges proposed** (2 cross-arc seams, 3 within-arc integrations, 1 Dornish long-game bridge)
