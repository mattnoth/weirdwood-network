# greyjoy-rebellion — Historical Anchor Notes

**Hub slug:** `greyjoy-rebellion` (event.war, 289 AC)
**Pre-existing neighbors:** 1 incoming edge (UNCLE_OF from theon-greyjoy — unrelated, not deduped against)
**Output:** 14 candidate edges

## Edge counts by type

| Type | Count |
|------|-------|
| COMMANDS_IN | 4 (balon-greyjoy, robert-i-baratheon, eddard-stark, stannis-baratheon) |
| FIGHTS_IN | 8 (victarion-greyjoy, euron-greyjoy, thoros, jorah-mormont, jason-mallister, jacelyn-bywater, theon-greyjoy, barristan-selmy) |
| VICTIM_IN | 2 (rodrik-greyjoy, maron-greyjoy) |

## Evidence split

- **Book-grounded (tier-1):** 4 edges — rodrik-greyjoy (VICTIM_IN), maron-greyjoy (VICTIM_IN), jorah-mormont (FIGHTS_IN), jason-mallister (FIGHTS_IN), jacelyn-bywater (FIGHTS_IN). All quotes are verbatim substrings from acok-theon-01.md or acok-daenerys-01.md or acok-tyrion-02.md.
- **Book-grounded (tier-2, recalled/second-hand):** 9 edges — All four COMMANDS_IN edges and victarion/euron/thoros/theon FIGHTS_IN. Tier-2 because the war is narrated retrospectively (Theon, Asha, Ned recall; no on-page action sequence set during the rebellion).
- **Wiki-only (tier-2):** 1 edge — barristan-selmy (FIGHTS_IN). No book chapter found narrating Selmy's role on Old Wyk; wiki is the only sourced claim.

## Source key quotes and their files

| Participant | Source | Line |
|---|---|---|
| balon-greyjoy, robert-i-baratheon, eddard-stark | `agot-eddard-01.md` | 19 |
| robert-i-baratheon, eddard-stark (additional) | `acok-theon-01.md` | 75 |
| stannis-baratheon | `adwd-the-wayward-bride-01.md` | 91 |
| victarion-greyjoy, euron-greyjoy | `acok-theon-02.md` | 257 |
| rodrik-greyjoy, maron-greyjoy | `acok-theon-01.md` | 339 |
| thoros | `agot-sansa-02.md` | 15 |
| jorah-mormont | `acok-daenerys-01.md` | 151 |
| jason-mallister | `acok-theon-01.md` | 217 |
| jacelyn-bywater | `acok-tyrion-02.md` | 39 |
| theon-greyjoy | `acok-theon-01.md` | 43 |
| barristan-selmy | wiki:Greyjoy's_Rebellion |

## LOCATED_AT

**Skipped.** The rebellion is a multi-site war (Iron Islands, Lannisport, Seagard, Fair Isle, Great Wyk, Old Wyk, Pyke). No single place node qualifies as the dominant location. The task instructions explicitly noted to probably skip LOCATED_AT for this hub.

## PART_OF

**Skipped.** The Greyjoy Rebellion is itself the top-level war event, not a sub-event of a larger named conflict. No parent-war PART_OF edge applies.

## Unresolved participants (named in wiki, no node check passed)

All named wiki participants listed under Notable Commanders were checked via `graph-query.py`:
- `balon-greyjoy` — resolved ✓
- `victarion-greyjoy` — resolved ✓
- `euron-greyjoy` — resolved ✓
- `rodrik-greyjoy` — resolved ✓
- `maron-greyjoy` — resolved ✓
- `robert-i-baratheon` — resolved ✓
- `stannis-baratheon` — resolved ✓
- `eddard-stark` — resolved ✓
- `barristan-selmy` — resolved ✓
- `thoros` (alias: thoros-of-myr) — resolved ✓
- `jorah-mormont` — resolved ✓
- `jason-mallister` — resolved ✓
- `jacelyn-bywater` — resolved ✓
- `theon-greyjoy` — resolved ✓

**Wiki-listed commanders not node-checked / deliberately skipped:**
- `Paxter Redwyne` — wiki lists as Notable Commander; not checked. Could be added if node exists. Low priority — command role is naval/supporting, same tier-2 wiki-only evidence as Selmy.
- `Tywin Lannister` — wiki says Robert was "supported by" Tywin; could be COMMANDS_IN but his role is described as supporting westerlands forces, not overall command of the rebellion. Deferred — would require node slug check (`tywin-lannister`).

## Theon-greyjoy edge note

Theon was 9–10 years old and present at Pyke as a non-combatant. Assigned FIGHTS_IN (rather than ATTENDS) because (a) the task prompt assigns him FIGHTS_IN by name, (b) he was the ultimate result/stake of the war's end. Confidence tier-2 (recalled, second-hand; the quote establishes his presence and hostage result, not active combat).
