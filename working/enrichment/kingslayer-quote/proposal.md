# B7 Kingslayer Quote — Proposal
Session: S151 | Date: 2026-06-26 | Unit: kingslayer-quote enrichment
Sources: `sources/chapters/asos/asos-jaime-05.md` (primary), `sources/chapters/asos/asos-jaime-02.md` (secondary)

---

## Quotes to home

### → `slaying-of-aerys-ii-the-kingslaying` (hub node `## Quotes`)

**Q1 — wildfire caches (the plan, Jaime V)**
> "His Grace commanded his alchemists to place caches of wildfire all over King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself."

`asos-jaime-05.md:53`
_Why load-bearing:_ establishes scale of the wildfire threat Jaime acted to prevent; the direct evidence substrate for the `wildfire-plot` node.

---

**Q2 — Aerys's burn order (Jaime V)**
> "The traitors want my city, I heard him tell Rossart, but I'll give them naught but ashes. Let Robert be king over charred bones and cooked meat."

`asos-jaime-05.md:57`
_Why load-bearing:_ verbatim Aerys quote — this IS the `aerys-commands-the-city-burned` event in Aerys's own words; grounds the hub's causal chain.

---

**Q3 — Jaime kills Rossart then Aerys (Jaime V)**  ← already in hub node, confirmed verbatim
> "When I came on Rossart, he was dressed as a common man-at-arms, hurrying to a postern gate. I slew him first. Then I slew Aerys, before he could find someone else to carry his message to the pyromancers."

`asos-jaime-05.md:63`
_Status:_ ALREADY in hub `## Quotes` block. No addition needed here. Confirmed verbatim — exact match.

---

**Q4 — Aerys last words / throne-room scene (Jaime II)**
> "I want him dead, the traitor. I want his head, you'll bring me his head, or you'll burn with all the rest. All the traitors. Rossart says they are inside the walls! He's gone to make them a warm welcome. Whose blood? Whose?" … Those purple eyes grew huge then, and the royal mouth drooped open in shock. He lost control of his bowels, turned, and ran for the Iron Throne. … Jaime hauled the last dragonking bodily off the steps, squealing like a pig and smelling like a privy. A single slash across his throat was all it took to end it.

`asos-jaime-02.md:291–295`
_Why load-bearing:_ the throne-room scene — Aerys's final words + the moment of the kill; complements the V confession which covers motive/sequence. Note: "Burn them all" as a set phrase does NOT appear verbatim in either Jaime chapter — Aerys's equivalent is "burn with all the rest" (Jaime II:291). Do not quote as "Burn them all" — that phrasing is common fan shorthand but is not the book text.

---

### → `jaime-lannister` node `## Quotes`

**Q5 — Jaime's self-exculpation / Ned's judgment (Jaime V)**
> "Do you think the noble Lord of Winterfell wanted to hear my feeble explanations? Such an honorable man. He only had to look at me to judge me guilty. By what right does the wolf judge the lion? By what right?"

`asos-jaime-05.md:71`
_Why load-bearing:_ Jaime's voice on honor, silence, and being judged without a hearing — key to his character arc; suits `jaime-lannister ## Quotes`.

---

## Edge-evidence upgrade

**Existing edge:** `jaime-lannister KILLS aerys-ii-targaryen` (T1, in edges.jsonl)

**Current evidence state:**
```json
{
  "evidence_kind": "book-pass1",
  "evidence_book": "agot",
  "evidence_chapter": "agot-eddard-09",
  "evidence_ref": "sources/chapters/agot/agot-eddard-09.md:91",
  "evidence_quote": "Jaime Lannister poked at Ned's chest with the gilded sword that had sipped the blood of the last of the Dragonkings."
}
```

This is a T1 indirect reference (AGOT Eddard IX — the sword, not the act). The direct first-person confession is in ASOS Jaime V and Jaime II.

**Proposed evidence upgrade** (add `evidence_quote_supplemental` or replace primary):
- `evidence_ref`: `sources/chapters/asos/asos-jaime-05.md:63`
- `evidence_quote`: `"I slew him first. Then I slew Aerys, before he could find someone else to carry his message to the pyromancers."`
- `evidence_chapter`: `asos-jaime-05`
- `evidence_book`: `asos`

**Recommended action for synthesis step:** upgrade or supplement the KILLS edge to carry the ASOS Jaime V first-person confession cite alongside the existing AGOT Eddard IX cite. The AGOT cite is not wrong (it's T1 by inference), but the ASOS cite is the direct admission.

---

## Edges proposed

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|----|-------------|-----------|-------------|------|------|--------------|----------------|------|
| B7-01 | jaime-lannister | PREVENTS | aerys-commands-the-city-burned | T1 | asos | asos-jaime-05.md:63 | "I slew him first. Then I slew Aerys, before he could find someone else to carry his message to the pyromancers." | Jaime killed Aerys to stop the burn order — clean causal prevention. NOT a dup of existing edges (AGENT_IN = role, KILLS = dyad; PREVENTS = causal mechanism). Dedup confirmed via baseline-intra.tsv. |

**WITNESS_IN considered and skipped:** `jaime WITNESS_IN aerys-commands-the-city-burned` is weaker — Jaime was a *witness to the planning* but the order itself was relayed via Rossart. The PREVENTS framing is cleaner and more load-bearing: it expresses *why* he killed Aerys, which is the entire arc significance of the slaying. One edge proposed; not both.

---

## NEW-TYPE-REQUEST

_(empty — PREVENTS is in the locked 170-type vocabulary)_

---

## Line-check notes

1. **"Burn them all" does NOT appear verbatim** in either Jaime V (`asos-jaime-05.md`) or Jaime II (`asos-jaime-02.md`). Aerys's equivalent phrasing in the text is: *"you'll burn with all the rest"* (Jaime II:291) and *"I'll give them naught but ashes"* (Jaime V:57). The phrase "Burn them all" is widely cited in fandom but is not a direct book quote from these chapters. Do not use it as a verbatim quote.
2. Q3 (asos-jaime-05.md:63) confirmed exact verbatim — already in hub node, no change needed.
3. Aerys throne-room scene is in **Jaime II** (asos-jaime-02.md:291–295), not Jaime V. Jaime V has the sequence/motive confession; Jaime II has the visual scene. Both are needed for full coverage.
4. The existing KILLS edge is grounded in AGOT Eddard IX (indirect). No ASOS cite yet attached — upgrade is a genuine gap.
