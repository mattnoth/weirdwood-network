# Lens B: Insurgency + Whodunit — Daenerys / Meereen Arc
# Run: 2026-06-24

---

## DEDUP NOTES (pre-check)

Checked `graph/edges/edges.jsonl` for all proposed source+target pairs before writing any proposal.

- `sons-of-the-harpy-insurgency` hub node: **MISSING** — confirmed no node file exists. The prior curator arc (run `causal-arc-essos-e2-slavers-bay-20260621`, line 22357) explicitly flagged this gap: "a `sons-of-the-harpy-insurgency` condition node is the cleaner future model (flagged, not minted)." **Green-lit to propose.**
- `hizdahr-zo-loraq COMMANDS_IN sons-of-the-harpy-kill-twenty-nine`: **EXISTS** (line 4693, confidence_tier 3, pass1-reified). Reclassification to `SUSPECTED_OF` considered — see notes below.
- `sons-of-the-harpy AGENT_IN sons-of-the-harpy-kill-twenty-nine`: **EXISTS** (line 4690).
- `poisoned-locusts` node: **EXISTS** (`graph/nodes/foods/poisoned-locusts.node.md`), 0 edges wired — islanded. Wire it.
- `belwas VICTIM_IN drogon-returns-to-daznak-pit`: NOT in edges.jsonl. **New.**
- `hizdahr-zo-loraq SUSPECTED_OF drogon-returns-to-daznak-pit (poisoning)`: NOT in edges.jsonl. **New.**
- `skahaz-mo-kandaq OPPOSES sons-of-the-harpy-insurgency`: NOT in edges.jsonl (only `brazen-beasts` edges exist). **New.**
- `sons-of-the-harpy AGENT_IN sons-of-the-harpy-insurgency`: No insurgency hub → NEW per hub creation.
- Note: existing `hizdahr-zo-loraq COMMANDS_IN sons-of-the-harpy-kill-twenty-nine` (Tier-3) is a DIFFERENT edge type from the proposed `SUSPECTED_OF` on the insurgency hub. Coexistence is fine — one models the specific-night speculation, the other the whole campaign.

---

## PROPOSED NODES

### sons-of-the-harpy-insurgency
**Type:** event.incident (or faction.campaign — recommend event.incident, as it represents an ongoing conflict)
**Proposed slug:** `sons-of-the-harpy-insurgency`
**Rationale:** The "shadow war" is a distinct narrative object — Dany thinks of it as an ongoing condition, not a single event. `sons-of-the-harpy-kill-twenty-nine` is one climactic beat within a longer campaign. The prior curator flagged this gap explicitly. Creating the hub unlocks the full web: the Brazen Beasts opposition, the peace-as-ceasefire logic, and the Hizdahr-is-the-Harpy whodunit.

**Proposed frontmatter:**
```yaml
---
slug: sons-of-the-harpy-insurgency
type: event.incident
name: Sons of the Harpy Insurgency
aliases:
  - shadow war of Meereen
  - the Harpy's shadow war
containers: [essos]
---
```

**Note on Barristan's confectioner source:** Skahaz names the poisoner as Hizdahr's confectioner (a catspaw) in `adwd-the-queensguard-01.md:155`. This character has no node. He is a named role (unnamed individual), not worth a standalone character node — his role is better captured as an edge note. No node proposed for the confectioner.

---

## PROPOSED EDGES

Format: `source | type | target | tier | ref | quote`

---

### 1. Insurgency Hub Wires

**E1**
```
sons-of-the-harpy | AGENT_IN | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:31 | "Every night the shadow war was waged anew beneath the stepped pyramids of Meereen."
```
*Note: This edge establishes the factions as the perpetrators of the named campaign.*

**E2**
```
sons-of-the-harpy-kill-twenty-nine | SUB_BEAT_OF | sons-of-the-harpy-insurgency | tier-1 | adwd-the-queens-hand-01.md:61 | "The Sons of the Harpy had resumed their shadow war two days ago. Three murders the first night, nine the second."
```
*The twenty-nine-night is the climactic escalation within the campaign, not the campaign itself.*

**E3**
```
brazen-beasts | OPPOSES | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:55 | "Skahaz, make me a new watch, made up in equal parts of shavepates and freedmen."
```
*The Brazen Beasts are created specifically as the counter-force to the Harpy insurgency.*

**E4**
```
skahaz-mo-kandaq | OPPOSES | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:39 | "Give them to the Shavepate. Skahaz, keep each apart from the others and put them to the question."
```
*Skahaz is the primary military commander against the Harpy; he drives the interrogation and counter-force.*

**E5**
```
freedmen | VICTIM_IN | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:44 | "Three freedmen, murdered in their homes … A moneylender, a cobbler, and the harpist Rylona Rhee. They cut her fingers off before they killed her."
```

**E6**
```
sons-of-the-harpy-insurgency | CAUSES | sons-of-the-harpy-kill-twenty-nine | tier-2 | adwd-the-queens-hand-01.md:61 | "The Sons of the Harpy had resumed their shadow war two days ago. Three murders the first night, nine the second."
```
*DEDUP NOTE: Existing edge `siege-of-meereen CAUSES sons-of-the-harpy-kill-twenty-nine` (line 22357) — different source. This new edge models insurgency-campaign → climactic-incident causality. No collision.*

**E7**
```
sons-of-the-harpy-insurgency | MOTIVATES | daenerys-targaryen | tier-2 | adwd-daenerys-04.md:67 | "She thought of Stalwart Shield, of Missandei's brother, of the woman Rylona Rhee … if a husband could help end the slaughter, then she owed it to her dead to marry."
```
*DEDUP NOTE: Existing `sons-of-the-harpy-kill-twenty-nine MOTIVATES daenerys-targaryen` (line 22358) — different source; this models the broader campaign as the ongoing motivation, not just the one night.*

**E8**
```
sons-of-the-harpy-insurgency | ENABLES | wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen | tier-2 | adwd-daenerys-04.md:141 | "Put an end to this shadow war, my lord. That is your quest. Give me ninety days and ninety nights without a murder, and I will know that you are worthy of a throne."
```
*DEDUP NOTE: Existing `sons-of-the-harpy-kill-twenty-nine CAUSES wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (line 22378) — different source (specific night); this models the insurgency campaign as the structural enabler of the marriage bargain (the ninety-day peace condition). Coexistence with that edge is fine — same arc, different granularity.*

---

### 2. Hizdahr-as-the-Harpy Whodunit

**E9**
```
hizdahr-zo-loraq | SUSPECTED_OF | sons-of-the-harpy-insurgency | tier-2 | adwd-the-queens-hand-01.md:295 | "In return he gave her poisoned locusts."
```
*Barristan's flat statement in dialogue with the Green Grace — the fullest on-page accusation. This edges the whodunit onto the insurgency hub.*

*Key textual reasoning captured as asserted_relation:*
*Barristan's suspicion: "You told them to stop killing and they obeyed. Why would they do that if you were not one of them?" (adwd-the-kingbreaker-01.md:277). The cessation of killings during the ninety-day peace and their resumption after Dany fled is the text's central circumstantial evidence. Hizdahr never touches the locusts. Skahaz: "Once he had [the crown], why share the rule?" The confectioner's catspaw chain, per Skahaz's disclosure.*

**E10**
```
hizdahr-zo-loraq | SUSPECTED_OF | sons-of-the-harpy-kill-twenty-nine | tier-2 | adwd-the-kingbreaker-01.md:277 | "You say that, yet when you told them to stop killing they obeyed. Why would they do that if you were not one of them?"
```
*DEDUP NOTE: Existing `hizdahr-zo-loraq COMMANDS_IN sons-of-the-harpy-kill-twenty-nine` (Tier-3, plate3-reified, line 4693) models a different claim — command authority over the specific killing event (speculative). This new SUSPECTED_OF edge models the in-world whodunit suspicion at the broader level. Tier-2 (stronger in-world textual basis than COMMANDS_IN Tier-3). Both coexist — the plate3 edge should probably be DEPRECATED in favor of this, but proposing coexistence for now; Matt can consolidate.*

---

### 3. Poisoned Locusts at Daznak — Wiring the Islanded Node

**E11**
```
poisoned-locusts | WIELDED_IN | drogon-returns-to-daznak-pit | tier-2 | adwd-daenerys-09.md:109 | "Hizdahr had stocked their box with flagons of chilled wine and sweetwater, with figs, dates, melons, and pomegranates, with pecans and peppers and a big bowl of honeyed locusts."
```
*The poisoned locusts are placed in the royal box for the Daznak pit fight — the event in which Drogon returns. WIELDED_IN is the correct vocabulary: the object is deployed in this event. The chapter already has an existing GUEST_OF hospitality edge wired (lines 3711-3712) confirming the placement.*

**E12**
```
hizdahr-zo-loraq | SUSPECTED_OF | poisoned-locusts | tier-2 | adwd-the-kingbreaker-01.md:257 | "You urged the queen to try the locusts but never tasted one yourself."
```
*Barristan confronts Hizdahr directly: Hizdahr provided the box, urged Dany to eat the locusts, but ate none himself. Skahaz also names Hizdahr's confectioner as the physical poisoner (adwd-the-queensguard-01.md:155), making Hizdahr the commander-level suspect and the confectioner the catspaw.*

*Alternative suspect captured below:*

**E13**
```
sons-of-the-harpy | SUSPECTED_OF | poisoned-locusts | tier-3 | adwd-the-queensguard-01.md:155 | "The Sons of the Harpy took his daughter and swore she would be returned unharmed once the queen was dead."
```
*Skahaz's disclosure: the confectioner was a catspaw coerced by the Sons of the Harpy. This makes the Sons the organizational sponsor of the attempt, with Hizdahr (if he is the Harpy) as the ultimate commander. Tier-3: the attribution runs through two layers of reported speech (Skahaz reports the confectioner's confession).*

*Third suspect (Barristan's in-chapter counterspeculation):*

**E14**
```
quentyn-martell | SUSPECTED_OF | poisoned-locusts | tier-3 | adwd-the-discarded-knight-01.md:57 | "Who can say that the locusts were meant for Daenerys? It was the king's own box. What if he was meant to be the victim all along?"
```
*Barristan briefly entertains the possibility that Quentyn (kin to the Red Viper, a Dornish poisoner's nephew) targeted Hizdahr rather than Dany. Tier-3: this is a momentary counter-hypothesis, not the dominant suspicion in the text.*

**E15**
```
belwas | VICTIM_IN | drogon-returns-to-daznak-pit | tier-1 | adwd-daenerys-09.md:231 | "Strong Belwas gave a moan, stumbled from his seat, and fell to his knees."
```
*Belwas eats the entire bowl of honeyed locusts (adwd-daenerys-09.md:109, 135: "Strong Belwas bellowed, 'Locusts!' as he seized the bowl and began to crunch them by the handful") and collapses during Drogon's arrival. Later confirmed gravely ill in adwd-the-queensguard-01.md:83. He is the confirmed victim of the poisoning attempt — the intended target (Dany) did not eat the locusts.*

**E16**
```
daenerys-targaryen | VICTIM_IN | poisoned-locusts | tier-2 | adwd-the-queens-hand-01.md:295 | "In return he gave her poisoned locusts."
```
*Daenerys was the intended target; she was spared only because she chose figs and dates instead. Barristan states the intent flatly.*

---

### 4. Reznak/Skahaz Hostage-Execution Counsel

**E17**
```
reznak-and-skahaz-advise-on-the-murders | SUB_BEAT_OF | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:23 | "The rest she had from Skahaz, Reznak, and Grey Worm, when they were ushered into her presence."
```
*The advice session is a direct response to the insurgency's killings — situates it as a beat within the shadow war.*

**E18**
```
skahaz-mo-kandaq | ADVISES | daenerys-targaryen | tier-1 | adwd-daenerys-04.md:31 | "The Shavepate would feed them to your dragons, it is said. A life for a life."
```
*DEDUP NOTE: Check if this edge already exists. The relationship is documented but the specific hostage-execution counsel in ADWD-IV may not be wired. This is a new specific scene reference for the same long-running advisory relationship. If a general ADVISES edge exists, this provides a new `ref` and quote; propose it regardless.*

---

### 5. The Galazza-Insurgency Causal Chain (completing the seam)

**E19**
```
galazza-galare | ADVISES | daenerys-targaryen | tier-1 | adwd-daenerys-04.md:43 | "Then heed me now and marry."
```
*DEDUP NOTE: Existing `galazza-counsels-the-ghiscari-marriage` node exists and the CAUSES chain is wired (line 22375). This edge is already captured implicitly through the event node. Do NOT propose as a new edge — covered.*

---

## NEEDS_VOCAB

None. All proposed edges use locked vocabulary: `AGENT_IN`, `SUB_BEAT_OF`, `OPPOSES`, `VICTIM_IN`, `MOTIVATES`, `ENABLES`, `CAUSES`, `WIELDED_IN`, `SUSPECTED_OF`, `ADVISES`.

One observation: there is currently no `POISONED_BY` or `ATTEMPTED_MURDER` edge type, but `SUSPECTED_OF` + `VICTIM_IN` + `WIELDED_IN` together model the poisoning attempt adequately without a new type.

---

## CONSOLIDATED EDGE TABLE

| # | source | type | target | tier | ref |
|---|--------|------|--------|------|-----|
| E1 | sons-of-the-harpy | AGENT_IN | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:31 |
| E2 | sons-of-the-harpy-kill-twenty-nine | SUB_BEAT_OF | sons-of-the-harpy-insurgency | tier-1 | adwd-the-queens-hand-01.md:61 |
| E3 | brazen-beasts | OPPOSES | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:55 |
| E4 | skahaz-mo-kandaq | OPPOSES | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:39 |
| E5 | freedmen | VICTIM_IN | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:44 |
| E6 | sons-of-the-harpy-insurgency | CAUSES | sons-of-the-harpy-kill-twenty-nine | tier-2 | adwd-the-queens-hand-01.md:61 |
| E7 | sons-of-the-harpy-insurgency | MOTIVATES | daenerys-targaryen | tier-2 | adwd-daenerys-04.md:67 |
| E8 | sons-of-the-harpy-insurgency | ENABLES | wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen | tier-2 | adwd-daenerys-04.md:141 |
| E9 | hizdahr-zo-loraq | SUSPECTED_OF | sons-of-the-harpy-insurgency | tier-2 | adwd-the-queens-hand-01.md:295 |
| E10 | hizdahr-zo-loraq | SUSPECTED_OF | sons-of-the-harpy-kill-twenty-nine | tier-2 | adwd-the-kingbreaker-01.md:277 |
| E11 | poisoned-locusts | WIELDED_IN | drogon-returns-to-daznak-pit | tier-2 | adwd-daenerys-09.md:109 |
| E12 | hizdahr-zo-loraq | SUSPECTED_OF | poisoned-locusts | tier-2 | adwd-the-kingbreaker-01.md:257 |
| E13 | sons-of-the-harpy | SUSPECTED_OF | poisoned-locusts | tier-3 | adwd-the-queensguard-01.md:155 |
| E14 | quentyn-martell | SUSPECTED_OF | poisoned-locusts | tier-3 | adwd-the-discarded-knight-01.md:57 |
| E15 | belwas | VICTIM_IN | drogon-returns-to-daznak-pit | tier-1 | adwd-daenerys-09.md:231 |
| E16 | daenerys-targaryen | VICTIM_IN | poisoned-locusts | tier-2 | adwd-the-queens-hand-01.md:295 |
| E17 | reznak-and-skahaz-advise-on-the-murders | SUB_BEAT_OF | sons-of-the-harpy-insurgency | tier-1 | adwd-daenerys-02.md:23 |

---

## CONSOLIDATION NOTE ON EXISTING PLATE-3 EDGE

`hizdahr-zo-loraq COMMANDS_IN sons-of-the-harpy-kill-twenty-nine` (Tier-3, line 4693) was minted by the plate3 reifier using the same Barristan quote. That edge asserts command-authority over the specific killing event; E10 above (`SUSPECTED_OF sons-of-the-harpy-kill-twenty-nine`, Tier-2) models the in-world suspicion at a higher textual confidence. **Recommendation for Matt:** retire or supersede the Tier-3 `COMMANDS_IN` edge once E10 is minted. The COMMANDS_IN overstates certainty; SUSPECTED_OF is the correct modeling for unproven-but-load-bearing agency per the project policy.

---

## HARVEST

Items found while reading chapters — drop points for a later harvest pass.

| ref | kind | note |
|-----|------|-------|
| adwd-daenerys-02.md:31 | food | "Nine" victims' identities: Mossador (Missandei's brother, gelded Unsullied), Rylona Rhee (harpist, fingers cut off before death), Eladon Goldenhair and Loyal Spear (poisoned at wineshop), Black Fist and Cetherys (crossbow bolts), Duran and Mossador (crushed by falling stones) — individual victim identities available for future node-wiring |
| adwd-daenerys-02.md:63 | object/economy | Blood tax: 100 pieces of gold from each pyramid per freedman killed — Dany's financial counter-insurgency policy; notable economic mechanism |
| adwd-daenerys-04.md:15 | food | Supper with Galazza: "honeyed lamb, fragrant with crushed mint and served with the small green figs she liked so much" — notable hospitality scene, Green Grace dinner |
| adwd-daenerys-04.md:21 | siege/external | Qartheen galleys closing the Skahazadhan, three New Ghis galleys, one Tolos carrack in the bay — context for the siege ring; Mantarys sent heads of three envoys in a cedar chest |
| adwd-daenerys-09.md:109 | food (grim register) | Royal box provisions at Daznak: "flagons of chilled wine and sweetwater, with figs, dates, melons, and pomegranates, with pecans and peppers and a big bowl of honeyed locusts" — the poisoned feast; Belwas eats the entire bowl |
| adwd-daenerys-09.md:109 | food (grim register) | Dog sausages, roast onions, unborn puppies on a stick sold by peddlers in the pit stands |
| adwd-daenerys-09.md:115 | description | Sellswords placed in black and purple benches (highest, most distant from sand); Bloodbeard's fiery red whiskers and long braids; Brown Ben's weathered face spotted in the crowd |
| adwd-daenerys-09.md:73 | description | Brazen Beast masks on parade to Daznak: "boars and bulls, hawks and herons, lions and tigers and bears, fork-tongued serpents and hideous basilisks" — visual inventory of mask types |
| adwd-the-queensguard-01.md:155 | object/plot | Skahaz's confectioner disclosure: daughter taken by the Harpy, killed in nine pieces (one per year of her age) after the attempt failed — the catspaw chain; grim register; potential Quaithe thematic echo (nine) |
| adwd-the-kingbreaker-01.md:257 | quote (load-bearing) | Barristan confronting Hizdahr: "You urged the queen to try the locusts but never tasted one yourself" — the smoking-gun circumstantial quote; already captured in E12 above |
| adwd-daenerys-02.md:125 | foreshadowing | Quaithe's appearance at the pool: "Kraken and dark flame, lion and griffin, the sun's son and the mummer's dragon. Trust none of them. Remember the Undying. Beware the perfumed seneschal." — full Quaithe warning text |
| adwd-daenerys-02.md:149 | foreshadowing | Dany reciting the three treasons: "one for blood and one for gold and one for…" — interrupted; the three-treasons motif unresolved here |
| adwd-daenerys-02.md:265 | foreshadowing / description | Hazzea: "Her name had been Hazzea. She was four years old." — the first named dragon-victim child; the Shavepate's theory that the Sons of the Harpy burned her to frame Drogon |
