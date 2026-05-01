# Orphan Edges Audit — 2026-04-30e

**Nodes scanned:** 4958
**Total edges checked:** 19083
**Edges that resolve cleanly:** 16002
**Orphan / problematic edges found:** 3081

**Breakdown:**
- Category 1 (target genuinely missing): 2968 edges across 1186 unique missing targets
- Category 2 (alias-mismatch — resolves via alias-resolver): 57 edges across 29 unique alias slugs
- Stale-data legacy (religion-bleed leftovers): 14
- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): 42
- Title-like missing targets (subset of Cat 1): 68 edges, 21 unique title slugs

**Other observations:**
- Unknown edge types encountered (schema-drift; deferred to schema-drift-auditor): 0 occurrences across 0 types
- Malformed edge lines: 25
- Nodes with no `## Edges` section: 0

---

## Stale-data legacy: religion-bleed leftovers

Location nodes still carrying legacy `WORSHIPS` edges with religion-field category labels as targets (e.g., `religions`, `Mixed`, `Old gods`) instead of actual religion entities. Parser fix landed in Session 27; these nodes have not been re-emitted. **Batch-fix recommendation: re-emit affected location nodes from the corrected parser output.**

| Source node | Edge type | Target text | Target slug |
|---|---|---|---|
| `barrow-hall` | WORSHIPS | Old gods | `old-gods` |
| `blackpool` | WORSHIPS | Old gods | `old-gods` |
| `braavos` | WORSHIPS | Mixed religions | `mixed-religions` |
| `deepwood-motte` | WORSHIPS | Old gods | `old-gods` |
| `greywater-watch` | WORSHIPS | Old gods | `old-gods` |
| `karhold` | WORSHIPS | Old gods | `old-gods` |
| `last-hearth` | WORSHIPS | Old gods | `old-gods` |
| `old-empire-of-ghis` | WORSHIPS | Mixed | `mixed` |
| `raventree-hall` | WORSHIPS | Old gods | `old-gods` |
| `triarchy` | WORSHIPS | Mixed | `mixed` |
| `vaes-dothrak` | WORSHIPS | Dothraki | `dothraki` |
| `valyrian-freehold` | WORSHIPS | Mixed | `mixed` |
| `whitetree` | WORSHIPS | Old gods | `old-gods` |
| `winterfell` | WORSHIPS | Old gods | `old-gods` |

---

## Edge-format issues: BORN_AT / DIED_AT / BURIED_AT date-bleed

**42 edges still treat dates/year-ranges as the target slug.** These nodes were not part of the Session 27 re-emission wave and need a follow-up re-promote.

Up to 50 examples (sorted by source):

| Source node | Edge type | Target text | Target slug |
|---|---|---|---|
| `alys-stackspear` | BORN_AT | ~192–233 AC (track_b: Born) | `192-233-ac` |
| `alyssa-blackwood` | BORN_AT | ~217–254 AC (track_b: Born) | `217-254-ac` |
| `amarei-crakehall` | BORN_AT | ~212–246 AC (track_b: Born) | `212-246-ac` |
| `annara-farring` | BORN_AT | ~240–273 AC (track_b: Born) | `240-273-ac` |
| `bethany-rosby` | BORN_AT | ~230–266 AC (track_b: Born) | `230-266-ac` |
| `cassana-estermont` | BORN_AT | ~225–250 AC (track_b: Born) | `225-250-ac` |
| `corenna-swann` | BORN_AT | ~233–237 AC (track_b: Born) | `233-237-ac` |
| `corenna-swann` | DIED_AT | ~245–249 AC (track_b: Died) | `245-249-ac` |
| `cyrenna-swann` | BORN_AT | ~196–237 AC (track_b: Born) | `196-237-ac` |
| `denys-swann` | BORN_AT | ~64 AC (track_b: Born) | `64-ac` |
| `dorna-swyft` | BORN_AT | ~244–261 AC (track_b: Born) | `244-261-ac` |
| `dyanna-dayne` | BORN_AT | ~149–179 AC (track_b: Born) | `149-179-ac` |
| `elenda-baratheon` | BORN_AT | ~79–97 AC (track_b: Born) | `79-97-ac` |
| `ella-lannister` | BORN_AT | ~204–261 AC (track_b: Born) | `204-261-ac` |
| `gilliane-glover` | BORN_AT | ~57–96 AC (track_b: Born) | `57-96-ac` |
| `hazel-harte` | BORN_AT | ~75–115 AC (track_b: Born) | `75-115-ac` |
| `jasper-waynwood` | BORN_AT | ~239–271 AC (track_b: Born) | `239-271-ac` |
| `jasper-waynwood` | DIED_AT | ~242–275 AC (track_b: Died) | `242-275-ac` |
| `jena-dondarrion` | BORN_AT | ~131–181 AC (track_b: Born) | `131-181-ac` |
| `jeyne-marbrand` | BORN_AT | ~203–230 AC (track_b: Born) | `203-230-ac` |
| `joy-penrose` | BORN_AT | ~187–200 AC (track_b: Born) | `187-200-ac` |
| `kiera-of-tyrosh` | BORN_AT | ~170–197 AC (track_b: Born) | `170-197-ac` |
| `laena-penrose` | BORN_AT | ~185–198 AC (track_b: Born) | `185-198-ac` |
| `maegelle-frey` | BORN_AT | ~250–268 AC (track_b: Born) | `250-268-ac` |
| `marianne-vance` | BORN_AT | ~262–290 AC (track_b: Born) | `262-290-ac` |
| `marna-locke` | BORN_AT | ~178–238 AC (track_b: Born) | `178-238-ac` |
| `megette` | BORN_AT | ~106–143 AC (track_b: Born) | `106-143-ac` |
| `melessa-florent` | BORN_AT | ~235–271 AC (track_b: Born) | `235-271-ac` |
| `patrek-vance` | BORN_AT | ~264–294 AC (track_b: Born) | `264-294-ac` |
| `perra-royce` | BORN_AT | ~187–222 AC (track_b: Born) | `187-222-ac` |
| `princess-of-dorne-mother-of-doran` | BORN_AT | ~205–236 AC (track_b: Born) | `205-236-ac` |
| `robin-penrose` | BORN_AT | ~184–197 AC (track_b: Born) | `184-197-ac` |
| `rohanne-of-tyrosh` | BORN_AT | ~141–172 AC (track_b: Born) | `141-172-ac` |
| `ryman-frey` | BORN_AT | ~245–249 AC (track_b: Born) | `245-249-ac` |
| `steffon-frey` | BORN_AT | ~260–280 AC (track_b: Born) | `260-280-ac` |
| `sylwa-paege` | BORN_AT | ~236–275 AC (track_b: Born) | `236-275-ac` |
| `teora-kyndall` | BORN_AT | ~157–197 AC (track_b: Born) | `157-197-ac` |
| `tyana-wylde` | BORN_AT | ~217–261 AC (track_b: Born) | `217-261-ac` |
| `walder-vance` | BORN_AT | ~263–291 AC (track_b: Born) | `263-291-ac` |
| `walton-frey` | BORN_AT | ~250–268 AC (track_b: Born) | `250-268-ac` |
| `wet-wat` | BORN_AT | ~191–196 AC (track_b: Born) | `191-196-ac` |
| `wylla-fenn` | BORN_AT | ~100–183 AC (track_b: Born) | `100-183-ac` |

---

## Title-like missing targets

Edges referencing title slugs that have no corresponding node (`warden-of-the-north`, `lord-of-dragonstone`, `ser`, `prince`, etc.). The `title` entity type exists; ~89 title nodes are populated but the broad title vocabulary used in `HOLDS_TITLE` edges is largely unpopulated.

**21 unique title slugs referenced; 68 total edge references.**

**Recommendation:** stand up a Title Pass that promotes the most-referenced title slugs to actual nodes.

Top 30 title slugs by edge-count:

| Target slug | Edges referencing | in_count |
|---|---|---|
| `khal` | 22 | 34 |
| `captain` | 19 | 0 |
| `lord-paramount-of-the-mander` | 8 | 6 |
| `lord-of-wyl` | 2 | 0 |
| `captain-of-the-guards-at-sunspear` | 1 | 0 |
| `princess-of-winterfell` | 1 | 0 |
| `captain-of-black-wind` | 1 | 0 |
| `captain-of-foamdrinker` | 1 | 0 |
| `captain-of-the-unsullied` | 1 | 0 |
| `lady-of-torrhens-square` | 1 | 0 |
| `warden-of-the-east-formerly` | 1 | 0 |
| `lord-commander-of-the-rainbow-guard` | 1 | 0 |
| `lord-of-darkdell` | 1 | 0 |
| `queen-of-the-high-tower` | 1 | 0 |
| `captain-of-the-salty-wench` | 1 | 0 |
| `lady-of-runestone` | 1 | 0 |
| `lady-of-coldmoat` | 1 | 7 |
| `captain-of-the-sea-bitch` | 1 | 0 |
| `high-council-of-the-triarchy` | 1 | 6 |
| `high-hermitage` | 1 | 4 |
| `king-of-winter-king-in-the-north` | 1 | 0 |

---

## Category 1: target genuinely missing

Sorted by `in_count` desc, then by edge_count. Top 100 of 1186 unique missing targets shown.

Severity: **HIGH** for top entries (high in_count → many references → recovery candidate). **LOW** for long-tail singletons.

| # | Target slug | Edges in graph | Cross-ref in_count | Title-like | Example source / edge_type / target text |
|---|---|---|---|---|---|
| 1 | `small-council` | 1 | 215 |  | `qyburn` / MEMBER_OF / Small council |
| 2 | `blacks` | 94 | 138 |  | `addam-velaryon` / SWORN_TO / Blacks |
| 3 | `greens` | 58 | 127 |  | `adrian-tarbeck` / SWORN_TO / Greens |
| 4 | `narrow-sea` | 1 | 120 |  | `assassination-of-tywin-lannister` / DEFEATS / narrow sea |
| 5 | `valyrian-steel` | 1 | 106 |  | `house-celtigar` / ANCESTRAL_WEAPON_OF / Valyrian steel |
| 6 | `others` | 14 | 76 |  | `chett` / SWORN_TO / Others (track_b: Allegiances) |
| 7 | `unsullied` | 17 | 68 |  | `black-fist` / SWORN_TO / Unsullied |
| 8 | `red-fork` | 4 | 64 |  | `hoster-tully` / BURIED_AT / Red Fork |
| 9 | `house-manderly` | 24 | 61 |  | `bartimus` / SWORN_TO / House Manderly |
| 10 | `dragonpit` | 6 | 60 |  | `burning-knight` / DIED_AT / Dragonpit (track_b: Died) |
| 11 | `harren-hoare` | 3 | 56 |  | `halleck-hoare` / HEIR_TO / Harren Hoare |
| 12 | `maegors-holdfast` | 3 | 56 |  | `aegon-targaryen-son-of-rhaegar` / DIED_AT / Maegor's Holdfast (qualifier: supposedly) |
| 13 | `kingswood` | 3 | 55 |  | `simon-toyne` / DIED_AT / Kingswood (track_b: Died) |
| 14 | `haunted-forest` | 2 | 55 |  | `clubfoot-karl` / DIED_AT / Haunted forest (track_b: Died) |
| 15 | `starry-sept` | 3 | 53 |  | `high-lickspittle` / DIED_AT / Starry Sept (track_b: Died) |
| 16 | `disputed-lands` | 6 | 52 |  | `aegor-rivers` / DIED_AT / Disputed Lands (track_b: Died) |
| 17 | `blackwater-bay` | 6 | 50 |  | `allard-seaworth` / DIED_AT / Blackwater Bay (track_b: Died) |
| 18 | `neck` | 3 | 50 |  | `coming-of-the-andals` / DEFEATS / Neck |
| 19 | `blackfyre` | 2 | 50 |  | `war-of-the-ninepenny-kings` / DEFEATS / Blackfyre |
| 20 | `red-mountains` | 1 | 50 |  | `vulture-king-jaehaerys-i` / DIED_AT / Red Mountains (track_b: Died) |
| 21 | `house-blackwood` | 30 | 46 |  | `agnes-blackwood` / SWORN_TO / House Blackwood |
| 22 | `iron-bank-of-braavos` | 2 | 46 |  | `noho-dimittis` / SWORN_TO / Iron Bank of Braavos |
| 23 | `house-bracken` | 24 | 45 |  | `aegor-rivers` / SWORN_TO / House Bracken |
| 24 | `wolfswood` | 2 | 45 |  | `harwood-fell` / DIED_AT / Wolfswood (track_b: Died) |
| 25 | `sunset-sea` | 1 | 45 |  | `norman-hightower` / DIED_AT / Sunset Sea (track_b: Died) |
| 26 | `mountains-of-the-moon` | 13 | 44 |  | `chiggen` / DIED_AT / Mountains of the Moon (track_b: Died) |
| 27 | `fair-isle` | 6 | 44 |  | `arron` / BORN_AT / Fair Isle |
| 28 | `stoney-sept` | 6 | 44 |  | `bella` / BORN_AT / Stoney Sept (track_b: Born) |
| 29 | `queens-men` | 18 | 43 |  | `alester-florent` / SWORN_TO / Queen's men |
| 30 | `old-wyk` | 6 | 41 |  | `baelor-blacktyde` / DIED_AT / Old Wyk (track_b: Died) |
| 31 | `crossroads-inn` | 1 | 39 |  | `wat-orphan` / SWORN_TO / Crossroads inn |
| 32 | `tarth` | 6 | 37 |  | `aemon-targaryen-son-of-jaehaerys-i` / DIED_AT / Tarth |
| 33 | `dornish-marches` | 4 | 36 |  | `anguy` / BORN_AT / Dornish Marches |
| 34 | `three-sisters` | 4 | 36 |  | `lark` / BORN_AT / Three Sisters |
| 35 | `dothraki-sea` | 19 | 35 |  | `caggo` / BORN_AT / Dothraki Sea |
| 36 | `house-rogare` | 12 | 35 |  | `drako-rogare` / SWORN_TO / House Rogare |
| 37 | `khal` | 22 | 34 | yes | `bharbo` / HOLDS_TITLE / Khal |
| 38 | `house-darry` | 16 | 34 |  | `damon-darry` / SWORN_TO / House Darry |
| 39 | `century-of-blood` | 3 | 34 |  | `agnes-blackwood` / DIED_AT / Century of Blood |
| 40 | `tower-of-the-hand` | 2 | 34 |  | `jaehaerys-targaryen-son-of-aegon-ii` / DIED_AT / Tower of the Hand (track_b: Died) |
| 41 | `great-pyramid` | 1 | 34 |  | `house-targaryen` / SEAT_OF / Great Pyramid |
| 42 | `house-florent` | 18 | 33 |  | `aladore-florent` / SWORN_TO / House Florent |
| 43 | `crackclaw-point` | 5 | 33 |  | `dick-crabb` / BORN_AT / Crackclaw Point |
| 44 | `dragons` | 1 | 32 |  | `dance-of-the-dragons` / DEFEATS / dragons |
| 45 | `fingers` | 5 | 31 |  | `petyr-baelish` / BORN_AT / Fingers (track_b: Born) |
| 46 | `flea-bottom` | 5 | 30 |  | `clayton-suggs` / BORN_AT / Flea Bottom |
| 47 | `faircastle` | 3 | 30 |  | `alester-wynch` / DIED_AT / Faircastle (track_b: Died) |
| 48 | `crypt-of-winterfell` | 14 | 29 |  | `barthogan-stark` / BURIED_AT / Crypt of Winterfell |
| 49 | `runestone` | 6 | 29 |  | `andar-royce` / BORN_AT / Runestone |
| 50 | `house-durrandon` | 5 | 29 |  | `argella-durrandon` / SWORN_TO / House Durrandon |
| 51 | `daznaks-pit` | 1 | 29 |  | `yurkhaz-zo-yunzak` / DIED_AT / Daznak's Pit (track_b: Died) |
| 52 | `ruby-ford` | 1 | 29 |  | `rhaegar-targaryen` / DIED_AT / Ruby Ford (track_b: Died) |
| 53 | `rhoynar` | 11 | 28 |  | `druselka` / SWORN_TO / Rhoynar |
| 54 | `lords-declarant` | 7 | 27 |  | `anya-waynwood` / SWORN_TO / Lords Declarant |
| 55 | `house-cerwyn` | 6 | 27 |  | `argelle-stark` / SWORN_TO / House Cerwyn |
| 56 | `jeyne-arryn` | 4 | 27 |  | `arnold-arryn` / OPPOSES / Jeyne Arryn (wiki:Arnold_Arryn) |
| 57 | `green-fork` | 3 | 27 |  | `conn` / DIED_AT / Green Fork (track_b: Died) |
| 58 | `lady-forlorn` | 1 | 27 |  | `house-corbray` / ANCESTRAL_WEAPON_OF / Lady Forlorn |
| 59 | `bear-island` | 9 | 26 |  | `alysane-mormont` / BORN_AT / Bear Island (track_b: Born) |
| 60 | `giants-lance` | 4 | 26 |  | `artys-i-arryn` / BORN_AT / Giant's Lance |
| 61 | `silent-sisters` | 4 | 26 |  | `alysanne-osgrey` / SWORN_TO / Silent Sisters |
| 62 | `arlan-of-pennytree` | 1 | 26 |  | `chestnut` / OWNS / Arlan of Pennytree |
| 63 | `ship` | 1 | 26 |  | `quence` / SWORN_TO / Ship |
| 64 | `larys-strong` | 1 | 25 |  | `hour-of-the-wolf` / DEFEATS / Larys Strong |
| 65 | `house-gardener` | 10 | 24 |  | `alester-tyrell` / SWORN_TO / House Gardener |
| 66 | `stormcrows` | 7 | 24 |  | `daario-naharis` / SWORN_TO / Stormcrows |
| 67 | `oldstones` | 5 | 24 |  | `merrett-frey` / DIED_AT / Oldstones (track_b: Died) |
| 68 | `shipbreaker-bay` | 4 | 24 |  | `arrax` / DIED_AT / Shipbreaker Bay (track_b: Died) |
| 69 | `house-of-black-and-white` | 2 | 24 |  | `umma` / SWORN_TO / House of Black and White |
| 70 | `299-ac` | 1 | 24 |  | `house-bolton` / OVERLORD_OF / 299 AC (track_b: Overlords) |
| 71 | `betrothal` | 1 | 24 |  | `lyonel-baratheons-rebellion` / DEFEATS / Betrothal |
| 72 | `house-hornwood` | 7 | 23 |  | `berena-hornwood` / SWORN_TO / House Hornwood |
| 73 | `house-dustin` | 6 | 23 |  | `barbrey-dustin` / SWORN_TO / House Dustin |
| 74 | `shield-islands` | 4 | 23 |  | `talbert-serry` / DIED_AT / Shield Islands (track_b: Died) |
| 75 | `marwyn` | 1 | 23 |  | `qyburn` / RESPECTS / Marwyn |
| 76 | `joffrey-i-baratheon` | 2 | 22 |  | `robert-i-baratheon` / SUCCEEDS / Joffrey I Baratheon |
| 77 | `hugh-hammer` | 1 | 22 |  | `vermithor` / OWNS / Hugh Hammer |
| 78 | `crag` | 8 | 21 |  | `eleyna-westerling` / BORN_AT / Crag (track_b: Born) |
| 79 | `stone-hedge` | 6 | 21 |  | `hendry-bracken` / DIED_AT / Stone Hedge (track_b: Died) |
| 80 | `vale` | 5 | 21 |  | `battle-in-the-waters-off-gulltown` / DEFEATS / Vale |
| 81 | `dark-sister` | 1 | 21 |  | `visenya-targaryen` / WIELDS / Dark Sister |
| 82 | `greyguard` | 1 | 21 |  | `jarl` / DIED_AT / Greyguard (track_b: Died) |
| 83 | `torrhens-square` | 4 | 20 |  | `helman-tallhart` / BORN_AT / Torrhen's Square |
| 84 | `aegonfort` | 1 | 20 |  | `house-targaryen` / SEAT_OF / Aegonfort (track_b: Seats) |
| 85 | `chequy-water` | 1 | 20 |  | `lucas-inchfield` / DIED_AT / Chequy Water (track_b: Died) |
| 86 | `greenblood` | 1 | 20 |  | `arys-oakheart` / DIED_AT / Greenblood (track_b: Died) |
| 87 | `northern-mountains` | 1 | 20 |  | `house-wull` / SEAT_OF / Northern mountains |
| 88 | `house-glover` | 13 | 19 |  | `benton-glover` / SWORN_TO / House Glover |
| 89 | `house-lothston` | 11 | 19 |  | `bastard-of-harrenhal` / SWORN_TO / House Lothston |
| 90 | `gift` | 5 | 19 |  | `sylas-the-grim` / DIED_AT / Gift (track_b: Died) |
| 91 | `cinnamon-wind` | 2 | 19 |  | `aemon-targaryen-son-of-maekar-i` / DIED_AT / Cinnamon Wind |
| 92 | `ice` | 1 | 19 |  | `house-stark` / ANCESTRAL_WEAPON_OF / Ice (track_b: Ancestral weapon) |
| 93 | `wise-masters` | 15 | 18 |  | `beastmaster` / SWORN_TO / Wise Masters |
| 94 | `helaena-targaryen` | 5 | 18 |  | `alicent-hightower` / PARENT_OF / Helaena Targaryen |
| 95 | `claw-isle` | 3 | 18 |  | `ardrian-celtigar` / BORN_AT / Claw Isle (track_b: Born) |
| 96 | `great-wyk` | 3 | 18 |  | `leo-costayne` / DIED_AT / Great Wyk (track_b: Died) |
| 97 | `longclaw` | 1 | 18 |  | `house-mormont` / ANCESTRAL_WEAPON_OF / Longclaw (track_b: Ancestral weapon) |
| 98 | `tower-of-joy` | 1 | 18 |  | `roberts-rebellion` / FIGHTS_IN / Tower of joy |
| 99 | `quiet-isle` | 5 | 17 |  | `clement` / SWORN_TO / Quiet Isle |
| 100 | `andal-invasion` | 3 | 17 |  | `battle-of-the-seven-stars` / FIGHTS_IN / Andal invasion |

_(Long tail: 1086 additional missing targets. See `working/audits/orphan-edges-2026-04-30e-cat1-full.tsv` for the complete list.)_

---

## Category 2: alias-mismatch (resolvable via alias-resolver)

These targets fail direct slug-match but DO resolve via the alias-resolver. **57 edges across 29 unique alias slugs** are affected.

Severity: **MED** — slug-format-drift, not a graph gap. Recommend the graph layer consult the alias-resolver after a direct-slug miss.

Top 50 by edge count:

| Target slug attempted | Resolves to canonical | Edges affected | Example |
|---|---|---|---|
| `catelyn-tully` | `catelyn-stark` | 6 | `arya-stark` / PARENT_OF / Catelyn Tully |
| `varamyr-sixskins` | `varamyr` | 4 | `greyskin` / OWNS / Varamyr Sixskins |
| `lysa-tully` | `lysa-arryn` | 4 | `hoster-tully` / PARENT_OF / Lysa Tully |
| `ramsay-bolton` | `ramsay-snow` | 4 | `jeyne-poole` / SPOUSE_OF / Ramsay Bolton |
| `barbrey-ryswell` | `barbrey-dustin` | 3 | `brandon-stark` / LOVER_OF / Barbrey Ryswell |
| `bethany-ryswell` | `bethany-bolton` | 3 | `domeric-bolton` / PARENT_OF / Bethany Ryswell |
| `durran-the-devout` | `durran-ii-durrandon` | 3 | `durran-godsgrief` / HEIR_TO / Durran the Devout |
| `sybelle-locke` | `sybelle-glover` | 3 | `erena-glover` / PARENT_OF / Sybelle Locke |
| `johanna-westerling` | `johanna-lannister` | 3 | `loreon-lannister-son-of-jason` / PARENT_OF / Johanna Westerling |
| `ravella-swann` | `ravella-smallwood` | 2 | `carellen-smallwood` / PARENT_OF / Ravella Swann |
| `donella-manderly` | `donella-hornwood` | 2 | `daryn-hornwood` / PARENT_OF / Donella Manderly |
| `olenna-redwyne` | `olenna-tyrell` | 2 | `luthor-tyrell` / SPOUSE_OF / Olenna Redwyne |
| `janna-tyrell` | `janna-fossoway` | 2 | `luthor-tyrell` / PARENT_OF / Janna Tyrell |
| `tyanna-of-pentos` | `tyanna-of-the-tower` | 1 | `alys-harroway` / LOVER_OF / Tyanna of Pentos (track_b: Lovers) |
| `brandon-the-shipwright` | `brandon-stark-shipwright` | 1 | `brandon-stark-burner` / SUCCEEDS / Brandon the Shipwright |
| `brandon-the-burner` | `brandon-stark-burner` | 1 | `brandon-stark-shipwright` / SUCCEEDS / Brandon the Burner |
| `durran-the-fair` | `durran-durrandon-the-fair` | 1 | `erich-durrandon-the-sailmaker` / PARENT_OF / Durran the Fair |
| `minisa-whent` | `minisa-tully` | 1 | `hoster-tully` / SPOUSE_OF / Minisa Whent |
| `smalljon-umber` | `jon-umber-son-of-jon` | 1 | `jon-umber` / PARENT_OF / Smalljon Umber |
| `jocasta-tarbeck` | `jocasta-lannister` | 1 | `lyman-lannister` / SPOUSE_OF / Jocasta Tarbeck |
| `mouse` | `marilda-of-hull` | 1 | `marilda-of-hull` / HOLDS_TITLE / Mouse |
| `alyn-of-hull` | `alyn-velaryon` | 1 | `marilda-of-hull` / PARENT_OF / Alyn of Hull |
| `longspear-ryk` | `ryk` | 1 | `munda` / SPOUSE_OF / Longspear Ryk |
| `taena-of-myr` | `taena-merryweather` | 1 | `orton-merryweather` / SPOUSE_OF / Taena of Myr |
| `argilac-the-arrogant` | `argilac-durrandon` | 1 | `orys-baratheon` / KILLS / Argilac the Arrogant |
| `lucinda-broome` | `lucinda-tully` | 1 | `prentys-tully` / SPOUSE_OF / Lucinda Broome |
| `giant` | `bedwyck` | 1 | `wun-weg-wun-dar-wun` / CULTURE_OF / Giant |
| `elia-of-dorne` | `elia-martell` | 1 | `sack-of-kings-landing` / DEFEATS / Elia of Dorne |
| `old-gods` | `old-gods-of-the-forest` | 1 | `seven-kingdoms` / WORSHIPS / Old gods (track_b: Religion) |

---

## Category 3: redirect-resolution (wiki redirect chain)

**Not separately classified in this run.** The Session 27 cleanup leaves the most actionable signal in Cat 1 / Cat 2 / stale / date-bleed; redirect-resolution is a future pass.

If a follow-up wants to mine Cat 3 specifically, the procedure: take Cat 1 entries with `in_count >= 5`, look up each `<Page_Name>.json` in `sources/wiki/_raw/`, and check whether the cached HTML body matches `<div class="redirectMsg">…</div>`. If so, the target slug should be remapped to the redirect target.

---

## Malformed `## Edges` lines

25 bullet lines did not match the `- TYPE: target` pattern. Sample (up to 30):

| Source node | Filename | Raw line |
|---|---|---|
| `luthor-tyrell-son-of-theodore` | `luthor-tyrell-son-of-theodore.node.md` | `- PARENT_OF [reverse]: Theodore Tyrell (cite: track_b: Father)` |
| `luthor-tyrell-son-of-theodore` | `luthor-tyrell-son-of-theodore.node.md` | `- PARENT_OF [reverse]: Lia Serry (cite: track_b: Mother)` |
| `lyonel-tyrell-son-of-leo` | `lyonel-tyrell-son-of-leo.node.md` | `- PARENT_OF [reverse]: Leo Tyrell (cite: track_b: Father)` |
| `lyonel-tyrell-son-of-leo` | `lyonel-tyrell-son-of-leo.node.md` | `- PARENT_OF [reverse]: Alys Beesbury (cite: track_b: Mother)` |
| `mace-tyrell` | `mace-tyrell.node.md` | `- PARENT_OF [reverse]: Luthor Tyrell (cite: track_b: Father)` |
| `mace-tyrell` | `mace-tyrell.node.md` | `- PARENT_OF [reverse]: Olenna Redwyne (cite: track_b: Mother)` |
| `margaery-tyrell` | `margaery-tyrell.node.md` | `- PARENT_OF [reverse]: Mace Tyrell (cite: track_b: Father)` |
| `margaery-tyrell` | `margaery-tyrell.node.md` | `- PARENT_OF [reverse]: Alerie Hightower (cite: track_b: Mother)` |
| `medwick-tyrell` | `medwick-tyrell.node.md` | `- PARENT_OF [reverse]: Luthor Tyrell (cite: track_b: Father)` |
| `medwick-tyrell` | `medwick-tyrell.node.md` | `- PARENT_OF [reverse]: Elyn Norridge (cite: track_b: Mother)` |
| `mina-tyrell` | `mina-tyrell.node.md` | `- PARENT_OF [reverse]: Luthor Tyrell (cite: track_b: Father)` |
| `mina-tyrell` | `mina-tyrell.node.md` | `- PARENT_OF [reverse]: Olenna Redwyne (cite: track_b: Mother)` |
| `olene-tyrell` | `olene-tyrell.node.md` | `- PARENT_OF [reverse]: Luthor Tyrell (cite: track_b: Father)` |
| `olene-tyrell` | `olene-tyrell.node.md` | `- PARENT_OF [reverse]: Elyn Norridge (cite: track_b: Mother)` |
| `olymer-tyrell` | `olymer-tyrell.node.md` | `- PARENT_OF [reverse]: Quentin Tyrell (cite: track_b: Father)` |
| `raymund-tyrell` | `raymund-tyrell.node.md` | `- PARENT_OF [reverse]: Olymer Tyrell (cite: track_b: Father)` |
| `raymund-tyrell` | `raymund-tyrell.node.md` | `- PARENT_OF [reverse]: Lysa Meadows (cite: track_b: Mother)` |
| `rickard-tyrell` | `rickard-tyrell.node.md` | `- PARENT_OF [reverse]: Olymer Tyrell (cite: track_b: Father)` |
| `rickard-tyrell` | `rickard-tyrell.node.md` | `- PARENT_OF [reverse]: Lysa Meadows (cite: track_b: Mother)` |
| `robert-tyrell` | `robert-tyrell.node.md` | `- PARENT_OF [reverse]: Osmund Tyrell (cite: track_b: Father)` |
| `theo-tyrell` | `theo-tyrell.node.md` | `- PARENT_OF [reverse]: Harlan Tyrell (cite: track_b: Father)` |
| `theodore-tyrell` | `theodore-tyrell.node.md` | `- PARENT_OF [reverse]: Luthor Tyrell (cite: track_b: Father)` |
| `theodore-tyrell` | `theodore-tyrell.node.md` | `- PARENT_OF [reverse]: Elyn Norridge (cite: track_b: Mother)` |
| `willas-tyrell` | `willas-tyrell.node.md` | `- PARENT_OF [reverse]: Mace Tyrell (cite: track_b: Father)` |
| `willas-tyrell` | `willas-tyrell.node.md` | `- PARENT_OF [reverse]: Alerie Hightower (cite: track_b: Mother)` |

---

## Summary

Of 19083 edges across 4958 nodes, 16002 resolve cleanly. 3081 are orphan or stale, dominated by Cat 1 (2968 edges, 1186 unique slugs). Date-bleed status: 42 stragglers remain. Religion-bleed leftovers: 14. Title-like targets are a structural gap: 21 title slugs referenced by 68 edges with no node. Cat 2 alias-mismatches (57 edges) are not gaps — they're handled the moment the graph layer consults `working/wiki-parsed/alias-resolver.json` after a direct-slug miss.

## Recommended actions

Prioritized:

1. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers are the only category where data is actively wrong. Sources: barrow-hall, blackpool, braavos, deepwood-motte, greywater-watch, karhold, last-hearth, old-empire-of-ghis, raventree-hall, triarchy, vaes-dothrak, valyrian-freehold, whitetree, winterfell.

2. **HIGH — Re-emit the 42 date-bleed BORN_AT/DIED_AT nodes.** 40 unique source nodes affected. Sample: alys-stackspear, alyssa-blackwood, amarei-crakehall, annara-farring, bethany-rosby, cassana-estermont, corenna-swann, cyrenna-swann, denys-swann, dorna-swyft ….

3. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing targets into Tier 3 recovery. See Cat 1 table.

4. **MED — Wire alias-resolver into the graph query layer.** All 57 Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. Avoids touching 29 source nodes.

5. **MED — Stand up a Title Pass.** Promote the top 21 title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, ser, prince, princess, king, queen, etc.) to actual `title` nodes.

6. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit after Pass 1 chapter extractions add their own missing-target signal.

7. **LOW — Run schema-drift-auditor** on the 0 non-locked edge types observed.
