# Historical-Anchor Notes: melee-at-bitterbridge

**Hub:** `melee-at-bitterbridge` (event.tournament; ACOK — Catelyn II at Renly's camp)
**Produced:** 2026-06-15
**Source files consulted:**
- `sources/wiki/_raw/Melee_at_Bitterbridge.json`
- `sources/chapters/acok/acok-catelyn-02.md` (primary — melee + feast scenes)
- `sources/chapters/acok/acok-catelyn-04.md` (Emmon Cuy's Rainbow Guard presence)

---

## Edge Counts

| Type | Count |
|------|-------|
| LOCATED_AT | 1 |
| FIGHTS_IN | 3 |
| ATTENDS | 11 |
| **Total** | **15** |

## Provenance Split

| Evidence kind | Count |
|--------------|-------|
| book-pass1 (tier 1) | 7 |
| book-pass1 (tier 2) | 5 |
| wiki-historical-anchor (tier 2) | 3 |

**Tier-1 edges (verbatim book quotes, direct involvement):**
- LOCATED_AT melee-at-bitterbridge → bitterbridge (acok-catelyn-02:83)
- FIGHTS_IN brienne-tarth → melee-at-bitterbridge (acok-catelyn-02:137)
- FIGHTS_IN loras-tyrell → melee-at-bitterbridge (acok-catelyn-02:117)
- ATTENDS renly-baratheon → melee-at-bitterbridge (acok-catelyn-02:137)
- ATTENDS catelyn-stark → melee-at-bitterbridge (acok-catelyn-02:83)
- ATTENDS arwyn-oakheart → melee-at-bitterbridge (acok-catelyn-02:101)
- ATTENDS mathis-rowan → melee-at-bitterbridge (acok-catelyn-02:101)
- ATTENDS randyll-tarly → melee-at-bitterbridge (acok-catelyn-02:101)

**Tier-2 book edges (present at camp/feast on melee day, not directly narrated in-melee):**
- ATTENDS bryce-caron (acok-catelyn-02:219 — at the feast that evening; his banner seen earlier in the chapter)
- ATTENDS robar-royce (acok-catelyn-02:219 — same feast scene; later escorts Catelyn at line 283)
- ATTENDS guyard-morrigen (acok-catelyn-02:211 — at the feast singing)
- ATTENDS emmon-cuy (acok-catelyn-04:45 — Rainbow Guard at Renly's pavilion; the melee is in ch.02 but Emmon is documented at the same Bitterbridge camp)

**Tier-2 wiki-only:**
- FIGHTS_IN ronnet-connington (wiki lists as defeated by Brienne; no named book reference)
- ATTENDS lorent-caswell (wiki lists as host; not named in text of ch.02)
- ATTENDS margaery-tyrell (wiki "Known Attendees"; Margaery's presence at camp implied in ch.02/03 but she's not named watching the melee)

---

## Unresolved (named, no node or no usable evidence)

**Named melee combatants in the wiki fight list with no node resolved:**
- Ser Richard Farrow — no node found
- Ser Edmund Ambrose — no node found
- Ser Ben Bushy — no node found
- Ser Mark Mullendore — note: node may exist as `mark-mullendore` but wiki lists him as a melee combatant; NOT checked (wiki only lists him as a defeated opponent, and he appears at the feast in ch.02 but not clearly as a combatant — SKIP to be safe)
- Ser Raymond Nayland — no node found
- Ser Will the Stork — no node found
- Ser Harry Sawyer — no node found
- Ser Robin Potter — no node found

**Late-arrival attendees (Catelyn's party — not emitted):**
- Lucas Blackwood, Robin Flint, Perwyn Frey, Wendel Manderly, Hallis Mollen — all arrive after the melee begins and are attendees of Catelyn's retinue, not Renly's guests. No ATTENDS edges emitted for them (they arrive at the camp, not as tourney guests). Could be added as ATTENDS in a future pass if desired.

---

## Deliberate Skips

- **PART_OF**: Not emitted. Per spec and per subagent instructions, a melee/tourney is NOT PART_OF a war; PART_OF is battle→war only.
- **Unnamed combatants**: The wiki notes 116 competitors; only named, node-resolved fighters emitted.
- **Mark Mullendore**: Appears in wiki fight list (defeated by Brienne) and is present at the feast (ch.02:211) but `mark-mullendore` node was not slug-checked against graph-query.py. Skipped to avoid emitting an unverified slug; a future pass can add FIGHTS_IN if node confirmed.
- **Emmon Cuy (FIGHTS_IN consideration)**: He is not listed as a melee combatant in the wiki. ATTENDS only, with evidence from his Rainbow Guard posting at camp.
- **Ser Colen of Greenpools**: Escorts Catelyn's party to the camp; not a melee participant or named attendee. No node checked; skipped.
