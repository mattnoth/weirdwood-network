# Orphan Edges Audit — 2026-04-30

**Nodes scanned:** 4236
**Total edges checked:** 18635
**Edges that resolve cleanly:** 10740
**Orphan / problematic edges found:** 7895

**Breakdown:**
- Category 1 (target genuinely missing): 7784 edges across 1881 unique missing targets
- Category 2 (alias-mismatch — resolves via alias-resolver): 56 edges across 28 unique alias slugs
- Stale-data legacy (religion-bleed leftovers): 14
- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): 41
- Title-like missing targets (subset of Cat 1): 1847 edges, 256 unique title slugs

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

**41 edges still treat dates/year-ranges as the target slug.** These nodes were not part of the Session 27 re-emission wave and need a follow-up re-promote.

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

**256 unique title slugs referenced; 1847 total edge references.**

**Recommendation:** stand up a Title Pass that promotes the most-referenced title slugs to actual nodes.

Top 30 title slugs by edge-count:

| Target slug | Edges referencing | in_count |
|---|---|---|
| `ser` | 693 | 4 |
| `prince` | 46 | 3 |
| `archmaester` | 42 | 45 |
| `princess` | 40 | 0 |
| `castellan` | 29 | 44 |
| `lord-of-the-seven-kingdoms` | 27 | 24 |
| `warden-of-the-north` | 24 | 62 |
| `prince-of-dragonstone` | 21 | 56 |
| `king` | 20 | 12 |
| `lord-of-harrenhal` | 20 | 38 |
| `khal` | 20 | 34 |
| `captain` | 18 | 0 |
| `king-of-the-rock` | 18 | 20 |
| `defender-of-oldtown` | 17 | 0 |
| `defender-of-the-citadel` | 17 | 0 |
| `lord-of-oldtown` | 17 | 1 |
| `lord-of-the-hightower` | 17 | 7 |
| `lord-of-the-port` | 17 | 0 |
| `queen` | 16 | 0 |
| `master-of-coin` | 15 | 57 |
| `lord-of-dragonstone` | 13 | 29 |
| `king-of-mountain-and-vale` | 13 | 26 |
| `high-king-of-the-iron-islands` | 13 | 14 |
| `captain-of-the-guards` | 13 | 4 |
| `master-of-laws` | 12 | 18 |
| `lord-of-the-tides` | 12 | 19 |
| `master-of-driftmark` | 12 | 1 |
| `lord-of-starpike` | 12 | 3 |
| `lord-paramount-of-the-trident` | 12 | 36 |
| `defender-of-the-vale` | 11 | 3 |

---

## Category 1: target genuinely missing

Sorted by `in_count` desc, then by edge_count. Top 100 of 1881 unique missing targets shown.

Severity: **HIGH** for top entries (high in_count → many references → recovery candidate). **LOW** for long-tail singletons.

| # | Target slug | Edges in graph | Cross-ref in_count | Title-like | Example source / edge_type / target text |
|---|---|---|---|---|---|
| 1 | `small-council` | 1 | 215 |  | `qyburn` / MEMBER_OF / Small council |
| 2 | `smallfolk` | 1 | 204 |  | `ryger-rivers` / PARENT_OF / smallfolk |
| 3 | `blacks` | 79 | 138 |  | `alan-beesbury` / SWORN_TO / Blacks |
| 4 | `greens` | 52 | 127 |  | `adrian-tarbeck` / SWORN_TO / Greens |
| 5 | `narrow-sea` | 1 | 120 |  | `assassination-of-tywin-lannister` / DEFEATS / narrow sea |
| 6 | `valyrian-steel` | 1 | 106 |  | `house-celtigar` / ANCESTRAL_WEAPON_OF / Valyrian steel |
| 7 | `209-ac` | 1 | 79 |  | `daeron-ii-targaryen` / HEIR_TO / 209 AC (track_b: Heirs) |
| 8 | `others` | 14 | 76 |  | `chett` / SWORN_TO / Others (track_b: Allegiances) |
| 9 | `130-ac` | 1 | 71 |  | `aegon-ii-targaryen` / HEIR_TO / 130 AC (track_b: Heirs) |
| 10 | `unsullied` | 17 | 68 |  | `black-fist` / SWORN_TO / Unsullied |
| 11 | `driftmark` | 10 | 68 |  | `alarra-massey` / HOLDS_TITLE / Driftmark |
| 12 | `red-fork` | 3 | 64 |  | `hoster-tully` / BURIED_AT / Red Fork |
| 13 | `northmen` | 261 | 63 |  | `alaric-stark` / CULTURE_OF / Northmen |
| 14 | `129-ac` | 1 | 63 |  | `aegon-ii-targaryen` / HEIR_TO / 129 AC (track_b: Heirs) |
| 15 | `warden-of-the-north` | 24 | 62 | yes | `alaric-stark` / HOLDS_TITLE / Warden of the North |
| 16 | `andals` | 3 | 62 |  | `argos-sevenstar` / CULTURE_OF / Andals |
| 17 | `house-manderly` | 23 | 61 |  | `bartimus` / SWORN_TO / House Manderly |
| 18 | `old-gods` | 1 | 61 |  | `seven-kingdoms` / WORSHIPS / Old gods (track_b: Religion) |
| 19 | `dragonpit` | 6 | 60 |  | `burning-knight` / DIED_AT / Dragonpit (track_b: Died) |
| 20 | `drogon` | 1 | 58 |  | `dreamfyre` / PARENT_OF / Drogon (track_b: Issue) |
| 21 | `master-of-coin` | 15 | 57 | yes | `alton-butterwell` / HOLDS_TITLE / Master of coin |
| 22 | `alicent-hightower` | 3 | 57 |  | `aegon-ii-targaryen` / PARENT_OF / Alicent Hightower |
| 23 | `prince-of-dragonstone` | 21 | 56 | yes | `aegon-iv-targaryen` / HOLDS_TITLE / Prince of Dragonstone |
| 24 | `maegors-holdfast` | 3 | 56 |  | `aegon-targaryen-son-of-rhaegar` / DIED_AT / Maegor's Holdfast (qualifier: supposedly) |
| 25 | `king-of-the-isles-and-the-north` | 2 | 56 | yes | `balon-greyjoy` / HOLDS_TITLE / King of the Isles and the North |
| 26 | `arbor` | 7 | 55 |  | `ballabar` / HOLDS_TITLE / Arbor |
| 27 | `king-beyond-the-wall` | 6 | 55 |  | `bael-the-bard` / HOLDS_TITLE / King-Beyond-the-Wall |
| 28 | `kingswood` | 3 | 55 |  | `simon-toyne` / DIED_AT / Kingswood (track_b: Died) |
| 29 | `haunted-forest` | 2 | 55 |  | `clubfoot-karl` / DIED_AT / Haunted forest (track_b: Died) |
| 30 | `jacaerys-velaryon` | 3 | 54 |  | `rhaenyra-targaryen` / HEIR_TO / Jacaerys Velaryon |
| 31 | `starry-sept` | 3 | 53 |  | `high-lickspittle` / DIED_AT / Starry Sept (track_b: Died) |
| 32 | `king-of-the-trident` | 9 | 52 | yes | `pate-of-fairmarket` / HOLDS_TITLE / King of the Trident |
| 33 | `disputed-lands` | 6 | 52 |  | `aegor-rivers` / DIED_AT / Disputed Lands (track_b: Died) |
| 34 | `storm-king` | 28 | 51 |  | `argilac-durrandon` / HOLDS_TITLE / Storm King |
| 35 | `children-of-the-forest` | 4 | 51 |  | `ash` / CULTURE_OF / children of the forest |
| 36 | `eustace-osgrey` | 4 | 51 |  | `addam-osgrey` / PARENT_OF / Eustace Osgrey |
| 37 | `blackwater-bay` | 6 | 50 |  | `allard-seaworth` / DIED_AT / Blackwater Bay (track_b: Died) |
| 38 | `aerys-i-targaryen` | 5 | 50 |  | `aelinor-penrose` / SPOUSE_OF / Aerys I Targaryen |
| 39 | `neck` | 3 | 50 |  | `coming-of-the-andals` / DEFEATS / Neck |
| 40 | `blackfyre` | 2 | 50 |  | `war-of-the-ninepenny-kings` / DEFEATS / Blackfyre |
| 41 | `nightfort` | 2 | 50 |  | `stannis-baratheon` / HOLDS_TITLE / Nightfort |
| 42 | `royal-fleet` | 2 | 50 |  | `gedmund-peake` / HOLDS_TITLE / royal fleet |
| 43 | `red-mountains` | 1 | 50 |  | `vulture-king-jaehaerys-i` / DIED_AT / Red Mountains (track_b: Died) |
| 44 | `house-blackwood` | 29 | 46 |  | `agnes-blackwood` / SWORN_TO / House Blackwood |
| 45 | `iron-bank-of-braavos` | 2 | 46 |  | `noho-dimittis` / SWORN_TO / Iron Bank of Braavos |
| 46 | `giants` | 1 | 46 |  | `mag-mar-tun-doh-weg` / CULTURE_OF / Giants |
| 47 | `archmaester` | 42 | 45 | yes | `arnel` / HOLDS_TITLE / Archmaester |
| 48 | `house-bracken` | 23 | 45 |  | `aegor-rivers` / SWORN_TO / House Bracken |
| 49 | `master-of-ships` | 10 | 45 | yes | `aethan-velaryon` / HOLDS_TITLE / Master of ships |
| 50 | `wolfswood` | 2 | 45 |  | `harwood-fell` / DIED_AT / Wolfswood (track_b: Died) |
| 51 | `sunset-sea` | 1 | 45 |  | `norman-hightower` / DIED_AT / Sunset Sea (track_b: Died) |
| 52 | `castellan` | 29 | 44 | yes | `amory-lorch` / HOLDS_TITLE / Castellan |
| 53 | `mountains-of-the-moon` | 12 | 44 |  | `chiggen` / DIED_AT / Mountains of the Moon (track_b: Died) |
| 54 | `fair-isle` | 6 | 44 |  | `arron` / BORN_AT / Fair Isle |
| 55 | `stoney-sept` | 5 | 44 |  | `denys-arryn` / DIED_AT / Stoney Sept |
| 56 | `131-ac` | 1 | 44 |  | `aegon-ii-targaryen` / HEIR_TO / 131 AC (track_b: Heirs) |
| 57 | `queens-men` | 18 | 43 |  | `alester-florent` / SWORN_TO / Queen's men |
| 58 | `134-ac` | 1 | 43 |  | `aegon-iii-targaryen` / HEIR_TO / 134 AC (track_b: Heirs) |
| 59 | `master-at-arms` | 22 | 42 |  | `alastor-reyne` / HOLDS_TITLE / Master-at-arms |
| 60 | `vale-mountain-clans` | 17 | 42 |  | `calor` / CULTURE_OF / Vale mountain clans |
| 61 | `ormund-hightower` | 5 | 42 |  | `bethany-hightower` / PARENT_OF / Ormund Hightower |
| 62 | `old-wyk` | 6 | 41 |  | `baelor-blacktyde` / DIED_AT / Old Wyk (track_b: Died) |
| 63 | `king-of-the-iron-islands` | 8 | 40 | yes | `balon-greyjoy` / HOLDS_TITLE / King of the Iron Islands |
| 64 | `red-priest` | 1 | 40 |  | `ezzelyno` / HOLDS_TITLE / Red priest |
| 65 | `septa` | 26 | 39 |  | `alysanne-daughter-of-aegon-iv` / HOLDS_TITLE / Septa (track_b: Title) |
| 66 | `king-of-the-isles-and-the-rivers` | 2 | 39 | yes | `harwyn-hoare` / HOLDS_TITLE / King of the Isles and the Rivers |
| 67 | `crossroads-inn` | 1 | 39 |  | `wat-orphan` / SWORN_TO / Crossroads inn |
| 68 | `lord-of-harrenhal` | 20 | 38 | yes | `bywin-strong` / HOLDS_TITLE / Lord of Harrenhal |
| 69 | `rohanne-webber` | 7 | 38 |  | `gerold-lannister` / SPOUSE_OF / Rohanne Webber |
| 70 | `tarth` | 6 | 37 |  | `aemon-targaryen-son-of-jaehaerys-i` / DIED_AT / Tarth |
| 71 | `lord-paramount-of-the-trident` | 12 | 36 | yes | `edmure-tully` / HOLDS_TITLE / Lord Paramount of the Trident |
| 72 | `dornish-marches` | 4 | 36 |  | `anguy` / BORN_AT / Dornish Marches |
| 73 | `laenor-velaryon` | 4 | 36 |  | `alyn-velaryon` / PARENT_OF / Laenor Velaryon (track_b: Fathers) |
| 74 | `three-sisters` | 4 | 36 |  | `lark` / BORN_AT / Three Sisters |
| 75 | `andal` | 53 | 35 |  | `alester-tyrell` / CULTURE_OF / Andal |
| 76 | `dothraki-sea` | 19 | 35 |  | `caggo` / BORN_AT / Dothraki Sea |
| 77 | `house-rogare` | 12 | 35 |  | `drako-rogare` / SWORN_TO / House Rogare |
| 78 | `joffrey-velaryon` | 3 | 35 |  | `rhaenyra-targaryen` / HEIR_TO / Joffrey Velaryon |
| 79 | `addam-velaryon` | 1 | 35 |  | `corlys-velaryon` / PARENT_OF / Addam Velaryon (track_b: Issue) |
| 80 | `great-council` | 1 | 35 |  | `maekar-i-targaryen` / HEIR_TO / Great Council |
| 81 | `khal` | 20 | 34 | yes | `cohollo` / SWORN_TO / Khal |
| 82 | `house-darry` | 16 | 34 |  | `damon-darry` / SWORN_TO / House Darry |
| 83 | `magister` | 6 | 34 |  | `bambarro-bazanne` / HOLDS_TITLE / Magister |
| 84 | `century-of-blood` | 3 | 34 |  | `agnes-blackwood` / DIED_AT / Century of Blood |
| 85 | `great-pyramid` | 1 | 34 |  | `house-targaryen` / SEAT_OF / Great Pyramid |
| 86 | `tower-of-the-hand` | 1 | 34 |  | `jaehaerys-targaryen-son-of-aegon-ii` / DIED_AT / Tower of the Hand (track_b: Died) |
| 87 | `westermen` | 223 | 33 |  | `addam-marbrand` / CULTURE_OF / Westermen |
| 88 | `house-florent` | 18 | 33 |  | `aladore-florent` / SWORN_TO / House Florent |
| 89 | `summer-isles` | 16 | 33 |  | `bellegere-otherys` / PARENT_OF / Summer Isles |
| 90 | `crackclaw-point` | 5 | 33 |  | `dick-crabb` / BORN_AT / Crackclaw Point |
| 91 | `master-of-whisperers` | 3 | 33 | yes | `brynden-rivers` / HOLDS_TITLE / Master of whisperers |
| 92 | `crannogmen` | 5 | 32 |  | `howland-reed` / CULTURE_OF / Crannogmen |
| 93 | `dragons` | 1 | 32 |  | `dance-of-the-dragons` / DEFEATS / dragons |
| 94 | `rivermen` | 415 | 31 |  | `addam-frey` / CULTURE_OF / Rivermen |
| 95 | `fingers` | 5 | 31 |  | `petyr-baelish` / BORN_AT / Fingers (track_b: Born) |
| 96 | `shae` | 3 | 31 |  | `tyrion-lannister` / LOVER_OF / Shae |
| 97 | `torrhen-manderly` | 1 | 31 |  | `desmond-manderly` / PARENT_OF / Torrhen Manderly |
| 98 | `flea-bottom` | 4 | 30 |  | `clayton-suggs` / BORN_AT / Flea Bottom |
| 99 | `faircastle` | 3 | 30 |  | `alester-wynch` / DIED_AT / Faircastle (track_b: Died) |
| 100 | `lucerys-velaryon` | 2 | 30 |  | `rhaenyra-targaryen` / PARENT_OF / Lucerys Velaryon |

_(Long tail: 1781 additional missing targets. See `working/audits/orphan-edges-2026-04-30-cat1-full.tsv` for the complete list.)_

---

## Category 2: alias-mismatch (resolvable via alias-resolver)

These targets fail direct slug-match but DO resolve via the alias-resolver. **56 edges across 28 unique alias slugs** are affected.

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

Of 18635 edges across 4236 nodes, 10740 resolve cleanly. 7895 are orphan or stale, dominated by Cat 1 (7784 edges, 1881 unique slugs). Date-bleed status: 41 stragglers remain. Religion-bleed leftovers: 14. Title-like targets are a structural gap: 256 title slugs referenced by 1847 edges with no node. Cat 2 alias-mismatches (56 edges) are not gaps — they're handled the moment the graph layer consults `working/wiki-parsed/alias-resolver.json` after a direct-slug miss.

## Recommended actions

Prioritized:

1. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers are the only category where data is actively wrong. Sources: barrow-hall, blackpool, braavos, deepwood-motte, greywater-watch, karhold, last-hearth, old-empire-of-ghis, raventree-hall, triarchy, vaes-dothrak, valyrian-freehold, whitetree, winterfell.

2. **HIGH — Re-emit the 41 date-bleed BORN_AT/DIED_AT nodes.** 39 unique source nodes affected. Sample: alys-stackspear, alyssa-blackwood, amarei-crakehall, annara-farring, bethany-rosby, cassana-estermont, corenna-swann, cyrenna-swann, denys-swann, dorna-swyft ….

3. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing targets into Tier 3 recovery. See Cat 1 table.

4. **MED — Wire alias-resolver into the graph query layer.** All 56 Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. Avoids touching 28 source nodes.

5. **MED — Stand up a Title Pass.** Promote the top 30 title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, ser, prince, princess, king, queen, etc.) to actual `title` nodes.

6. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit after Pass 1 chapter extractions add their own missing-target signal.

7. **LOW — Run schema-drift-auditor** on the 0 non-locked edge types observed.
