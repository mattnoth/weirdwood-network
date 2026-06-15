# tourney-at-harrenhal — Historical Anchor Notes

**Hub:** `tourney-at-harrenhal` (event.tournament)
**Produced:** 2026-06-15
**Pre-existing edges:** 0 (confirmed via `--neighbors`)

## Structural attachments

- **LOCATED_AT → harrenhal**: 1 edge. Slug verified. Evidence: wiki-historical-anchor tier-2 (direct name in node body; no standalone book sentence names the location without the event already being assumed).

- **PART_OF**: Deliberately skipped per task instructions — a tourney is not a war; its abduction-aftermath leading to Robert's Rebellion is arc-level and out of scope for this structural-attachment pass.

## Edge counts

| Type | Count |
|------|-------|
| LOCATED_AT | 1 |
| FIGHTS_IN | 8 |
| ATTENDS | 17 |
| **Total** | **26** |

## Provenance split

| Tier | Evidence kind | Count |
|------|---------------|-------|
| Tier-1 | book-pass1 | 22 |
| Tier-2 | book-pass1 (indirect/recalled) | 1 (oswell-whent: present on page, jousting role from wiki) |
| Tier-2 | wiki-historical-anchor | 3 (walter-whent, lewyn-martell, jonothor-darry) |

**Primary book sources used:**
- `sources/chapters/agot/agot-eddard-15.md` lines 41, 43, 45 — Ned's Harrenhal memory (year of false spring)
- `sources/chapters/asos/asos-bran-02.md` lines 163, 191, 225 — Meera Reed's Knight of the Laughing Tree story
- `sources/chapters/asos/asos-jaime-04.md` line 57 — Jaime's bathhouse confession (confirms Kingsguard induction at Harrenhal; not used as primary source since agot-eddard-15 already establishes Jaime's presence more directly)

## FIGHTS_IN assignments

- `rhaegar-targaryen` — joust champion (tier-1 book, agot-eddard-15:43+45)
- `barristan-selmy` — jousted, fell to Rhaegar in final tilt (tier-1, agot-eddard-15:45)
- `arthur-dayne` — jousted, fell to Rhaegar (tier-1, agot-eddard-15:43)
- `brandon-stark` — jousted, fell to Rhaegar (tier-1, agot-eddard-15:43)
- `yohn-royce` — jousted (Bronze Yohn Royce), fell to Rhaegar (tier-1, agot-eddard-15:43)
- `robert-baratheon` — competed in the melee, unhorsed many (tier-1, agot-eddard-15:41)
- `knight-of-the-laughing-tree` — jousted, defeated 3 knights (tier-1, asos-bran-02:225)
- `oswell-whent` — present on-page (tier-2 book); wiki says he jousted to defend Walter's daughter's honor and was defeated; FIGHTS_IN role wiki-corroborated but book quote only confirms presence

## ATTENDS assignments

All named, node-resolved attendees from the node body's Known Attendees section who are non-combatants (or whose primary role is attendance, not joust/melee).

- `aerys-ii-targaryen` — tier-1 book (asos-bran-02:163)
- `eddard-stark` — tier-1 book (agot-eddard-15:41)
- `lyanna-stark` — tier-1 book (agot-eddard-15:45)
- `elia-martell` — tier-1 book (agot-eddard-15:45)
- `jon-arryn` — tier-1 book (agot-eddard-15:45, "Jon" = Jon Arryn, Ned's foster-father who accompanied him from the Eyrie)
- `eon-hunter` — tier-1 book (agot-eddard-15:45, "old Lord Hunter")
- `jaime-lannister` — tier-1 book (agot-eddard-15:41; inducted into Kingsguard at Harrenhal, left early by Aerys's command; ATTENDS not FIGHTS_IN because Aerys forbade him from jousting)
- `gerold-hightower` — tier-1 book (agot-eddard-15:41, "White Bull himself, Lord Commander Ser Gerold Hightower")
- `howland-reed` — tier-1 book (asos-bran-02:191, the crannogman of the KotLT story)
- `benjen-stark` — tier-1 book (asos-bran-02:191, "pup brother")
- `ashara-dayne` — tier-1 book (asos-bran-02:191, "maid with laughing purple eyes")
- `oberyn-martell` — tier-1 book (asos-bran-02:191, "red snake")
- `jon-connington` — tier-1 book (asos-bran-02:191, "lord of griffins")
- `mace-tyrell` — tier-1 book (asos-bran-02:163, "rose lord")
- `richard-lonmouth` — tier-1 book (asos-bran-02:191, "knight of skulls and kisses")
- `walter-whent` — tier-2 wiki (host; no on-page book sentence names Walter Whent directly at the tourney in the chapters surveyed)
- `lewyn-martell` — tier-2 wiki (named in Known Attendees section; on-page book references to Lewyn Martell are about the Trident, not Harrenhal)
- `jonothor-darry` — tier-2 wiki (named in Known Attendees; ASOS Jaime 08 mentions him as a Kingsguard teacher but does not place him at Harrenhal specifically)

## Unresolved participants (skipped — no node)

The following named persons from the node body have no graph node and were skipped:

- **Walter Whent's unnamed daughter** ("the fair maid") — unnamed, no node
- **Walter Whent's four sons** — unnamed group, no individual nodes
- **A wandering crow** (possibly Yoren) — Yoren does have a node (`yoren`?) but the identity is speculative; skipped because the node body marks this as uncertain ("possibly Yoren") and the wiki attendee entry is for an unnamed wandering crow, not Yoren specifically

## Skipped group entries

The node body lists House Dustin members, House Hornwood members, House Manderly members, House Mormont members — these are groups, not named individuals with nodes. Skipped per spec rule ("skip 'House X members' group entries").
