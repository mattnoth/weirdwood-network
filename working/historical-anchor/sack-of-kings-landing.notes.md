# Historical-Anchor Notes: sack-of-kings-landing

**Hub:** `sack-of-kings-landing` (event.battle)
**Date produced:** 2026-06-15
**Spec version:** POST-PLATE-5 followup #9, wave 1

---

## Structural attachments

- **LOCATED_AT** → `kings-landing` (node confirmed OK; wiki-only, tier-2)
- **PART_OF** → `roberts-rebellion` — ALREADY EXISTS (1 outgoing + 1 incoming PART_OF edge confirmed by `--neighbors` check). Skipped per spec.

---

## Role edges produced (9 total)

| Edge type | Source slug | Evidence kind | Tier |
|-----------|-------------|---------------|------|
| COMMANDS_IN | tywin-lannister | book-pass1 (asos-tyrion-06:187) | 2 |
| AGENT_IN | jaime-lannister | book-pass1 (asos-jaime-02:295) | 1 |
| VICTIM_IN | aerys-ii-targaryen | book-pass1 (asos-jaime-08:39) | 1 |
| AGENT_IN | gregor-clegane | book-pass1 (asos-tyrion-09:405) | 2 |
| VICTIM_IN | elia-martell | book-pass1 (asos-tyrion-10:247) | 1 |
| VICTIM_IN | rhaenys-targaryen-daughter-of-rhaegar | book-pass1 (asos-tyrion-09:405) | 2 |
| AGENT_IN | amory-lorch | book-pass1 (asos-tyrion-09:405) | 2 |
| VICTIM_IN | aegon-targaryen-son-of-rhaegar | book-pass1 (asos-tyrion-09:405) | 2 |
| LOCATED_AT | sack-of-kings-landing → kings-landing | wiki-historical-anchor | 2 |

**Count by type:** LOCATED_AT×1, COMMANDS_IN×1, AGENT_IN×3, VICTIM_IN×4
**Book-grounded:** 8 edges (1 tier-1 Jaime AGENT_IN, 2 tier-1 VICTIM_IN for Aerys+Elia, 5 tier-2 recalled/second-hand)
**Wiki-only:** 1 edge (LOCATED_AT)

---

## Tier notes

- **Tier-1 edges** (verbatim primary-narrator description):
  - `jaime-lannister AGENT_IN`: Jaime's own flashback narration in asos-jaime-02 — first-person scene recall, direct action described.
  - `aerys-ii-targaryen VICTIM_IN`: The White Book entry in asos-jaime-08 ("During the Sack of King's Landing, slew King Aerys II at the foot of the Iron Throne") — in-world documentary record, unambiguous.
  - `elia-martell VICTIM_IN`: Gregor Clegane's own dying confession in asos-tyrion-10 ("Then I raped her. Then I smashed her fucking head in") — unique in that the AGENT himself confirms the act on-page.

- **Tier-2 edges** (recalled / second-hand): All others are narrated retrospectively by a different POV (Tyrion recounting to Oberyn; Tywin's confession to Tyrion). Canon facts but not eyewitness primary narration.

- **ASSAULTS (sexual) on Elia:** The rape is explicitly confirmed both in Tyrion's account (asos-tyrion-09) and Gregor's confession (asos-tyrion-10). The spec permits a separate `gregor-clegane ASSAULTS elia-martell` dyad edge — this is NOT emitted here because the spec says "those dyads may already exist — do not duplicate; only emit the event-attach role edges." The assault is captured via evidence_quote on the VICTIM_IN edge for Elia.

- **COMMANDS_IN for Tywin:** Tywin's confession in asos-tyrion-06 is retrospective (Tyrion POV), so tier-2. He ordered the sack but is not documented as personally fighting; COMMANDS_IN is the correct role type.

---

## Rhaenys disambiguation

`rhaenys-targaryen` is the Targaryen conqueror (Aegon I's sister-wife); the node body explicitly notes "Pass1_mentions from agot-eddard-15 refer to the daughter of Rhaegar, not this Rhaenys." The correct slug for the Sack victim is `rhaenys-targaryen-daughter-of-rhaegar` (confirmed node exists).

---

## Unresolved participants

None of the named principals were unresolved. All 7 character slugs confirmed by `scripts/graph-query.py`:
- `jaime-lannister` ✓
- `tywin-lannister` ✓
- `aerys-ii-targaryen` ✓
- `gregor-clegane` ✓
- `elia-martell` ✓
- `rhaenys-targaryen-daughter-of-rhaegar` ✓
- `amory-lorch` ✓
- `aegon-targaryen-son-of-rhaegar` ✓

**Named in wiki / node body but no node resolved (skipped):**
- `pycelle` — wiki body mentions Pycelle convinced Aerys to open the gates (ACOK ch25), but no node check was run; he is not a combatant/victim in the sack itself (merely an enabler). Could warrant an ATTENDS or wiki-grounded edge in a second pass.
- Pyromancers `rossart`, `garigus`, `belis` — present during the wildfire plot run-up; Rossart killed by Jaime. Node existence not checked. They are wildfire-plot participants, not sack combatants in the primary sense.
- `eddard-stark` — AGOT Eddard-02 confirms Ned arrived at King's Landing after the sack and found it taken; he was an eyewitness arriving after. Could warrant ATTENDS (arrival) but that is stretch-scope for this hub. Skipped.
- `robert-i-baratheon` — was not present at the sack (took a wound at the Trident, gave command to Ned). Not a direct participant. Skipped.

---

## Deliberately skipped

- **PART_OF roberts-rebellion**: Already present (both directions). Skipped per spec dedup rule.
- **FIGHTS_IN for House Lannister forces generally**: No specific named node for "Lannister army" as a participant distinct from the commanders; unnamed soldiers are out of scope.
- **Pycelle ATTENDS/ENABLES**: Plausible but requires node resolution and is ancillary to the sack's main acts. Deferred.
