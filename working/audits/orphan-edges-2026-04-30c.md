# Orphan Edges Audit — 2026-04-30c

**Nodes scanned:** 4774
**Total edges checked:** 18635
**Edges that resolve cleanly:** 15110
**Orphan / problematic edges found:** 3525

**Breakdown:**
- Category 1 (target genuinely missing): 3413 edges across 1353 unique missing targets
- Category 2 (alias-mismatch — resolves via alias-resolver): 57 edges across 29 unique alias slugs
- Stale-data legacy (religion-bleed leftovers): 14
- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): 41
- Title-like missing targets (subset of Cat 1): 62 edges, 18 unique title slugs

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

**18 unique title slugs referenced; 62 total edge references.**

**Recommendation:** stand up a Title Pass that promotes the most-referenced title slugs to actual nodes.

Top 30 title slugs by edge-count:

| Target slug | Edges referencing | in_count |
|---|---|---|
| `khal` | 20 | 34 |
| `captain` | 18 | 0 |
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
| `captain-of-the-salty-wench` | 1 | 0 |
| `captain-of-the-sea-bitch` | 1 | 0 |
| `high-council-of-the-triarchy` | 1 | 6 |
| `high-hermitage` | 1 | 4 |
| `king-of-winter-king-in-the-north` | 1 | 0 |

---

## Category 1: target genuinely missing

Sorted by `in_count` desc, then by edge_count. Top 100 of 1353 unique missing targets shown.

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
| 11 | `red-fork` | 3 | 64 |  | `hoster-tully` / BURIED_AT / Red Fork |
| 12 | `129-ac` | 1 | 63 |  | `aegon-ii-targaryen` / HEIR_TO / 129 AC (track_b: Heirs) |
| 13 | `house-manderly` | 23 | 61 |  | `bartimus` / SWORN_TO / House Manderly |
| 14 | `dragonpit` | 6 | 60 |  | `burning-knight` / DIED_AT / Dragonpit (track_b: Died) |
| 15 | `drogon` | 1 | 58 |  | `dreamfyre` / PARENT_OF / Drogon (track_b: Issue) |
| 16 | `alicent-hightower` | 3 | 57 |  | `aegon-ii-targaryen` / PARENT_OF / Alicent Hightower |
| 17 | `maegors-holdfast` | 3 | 56 |  | `aegon-targaryen-son-of-rhaegar` / DIED_AT / Maegor's Holdfast (qualifier: supposedly) |
| 18 | `kingswood` | 3 | 55 |  | `simon-toyne` / DIED_AT / Kingswood (track_b: Died) |
| 19 | `haunted-forest` | 2 | 55 |  | `clubfoot-karl` / DIED_AT / Haunted forest (track_b: Died) |
| 20 | `jacaerys-velaryon` | 3 | 54 |  | `rhaenyra-targaryen` / HEIR_TO / Jacaerys Velaryon |
| 21 | `starry-sept` | 3 | 53 |  | `high-lickspittle` / DIED_AT / Starry Sept (track_b: Died) |
| 22 | `disputed-lands` | 6 | 52 |  | `aegor-rivers` / DIED_AT / Disputed Lands (track_b: Died) |
| 23 | `eustace-osgrey` | 4 | 51 |  | `addam-osgrey` / PARENT_OF / Eustace Osgrey |
| 24 | `blackwater-bay` | 6 | 50 |  | `allard-seaworth` / DIED_AT / Blackwater Bay (track_b: Died) |
| 25 | `aerys-i-targaryen` | 5 | 50 |  | `aelinor-penrose` / SPOUSE_OF / Aerys I Targaryen |
| 26 | `neck` | 3 | 50 |  | `coming-of-the-andals` / DEFEATS / Neck |
| 27 | `blackfyre` | 2 | 50 |  | `war-of-the-ninepenny-kings` / DEFEATS / Blackfyre |
| 28 | `red-mountains` | 1 | 50 |  | `vulture-king-jaehaerys-i` / DIED_AT / Red Mountains (track_b: Died) |
| 29 | `house-blackwood` | 29 | 46 |  | `agnes-blackwood` / SWORN_TO / House Blackwood |
| 30 | `iron-bank-of-braavos` | 2 | 46 |  | `noho-dimittis` / SWORN_TO / Iron Bank of Braavos |
| 31 | `house-bracken` | 23 | 45 |  | `aegor-rivers` / SWORN_TO / House Bracken |
| 32 | `wolfswood` | 2 | 45 |  | `harwood-fell` / DIED_AT / Wolfswood (track_b: Died) |
| 33 | `sunset-sea` | 1 | 45 |  | `norman-hightower` / DIED_AT / Sunset Sea (track_b: Died) |
| 34 | `mountains-of-the-moon` | 12 | 44 |  | `chiggen` / DIED_AT / Mountains of the Moon (track_b: Died) |
| 35 | `fair-isle` | 6 | 44 |  | `arron` / BORN_AT / Fair Isle |
| 36 | `stoney-sept` | 5 | 44 |  | `denys-arryn` / DIED_AT / Stoney Sept |
| 37 | `131-ac` | 1 | 44 |  | `aegon-ii-targaryen` / HEIR_TO / 131 AC (track_b: Heirs) |
| 38 | `queens-men` | 18 | 43 |  | `alester-florent` / SWORN_TO / Queen's men |
| 39 | `134-ac` | 1 | 43 |  | `aegon-iii-targaryen` / HEIR_TO / 134 AC (track_b: Heirs) |
| 40 | `ormund-hightower` | 5 | 42 |  | `bethany-hightower` / PARENT_OF / Ormund Hightower |
| 41 | `old-wyk` | 6 | 41 |  | `baelor-blacktyde` / DIED_AT / Old Wyk (track_b: Died) |
| 42 | `crossroads-inn` | 1 | 39 |  | `wat-orphan` / SWORN_TO / Crossroads inn |
| 43 | `rohanne-webber` | 7 | 38 |  | `gerold-lannister` / SPOUSE_OF / Rohanne Webber |
| 44 | `tarth` | 6 | 37 |  | `aemon-targaryen-son-of-jaehaerys-i` / DIED_AT / Tarth |
| 45 | `dornish-marches` | 4 | 36 |  | `anguy` / BORN_AT / Dornish Marches |
| 46 | `laenor-velaryon` | 4 | 36 |  | `alyn-velaryon` / PARENT_OF / Laenor Velaryon (track_b: Fathers) |
| 47 | `three-sisters` | 4 | 36 |  | `lark` / BORN_AT / Three Sisters |
| 48 | `dothraki-sea` | 19 | 35 |  | `caggo` / BORN_AT / Dothraki Sea |
| 49 | `house-rogare` | 12 | 35 |  | `drako-rogare` / SWORN_TO / House Rogare |
| 50 | `joffrey-velaryon` | 3 | 35 |  | `rhaenyra-targaryen` / HEIR_TO / Joffrey Velaryon |
| 51 | `addam-velaryon` | 1 | 35 |  | `corlys-velaryon` / PARENT_OF / Addam Velaryon (track_b: Issue) |
| 52 | `great-council` | 1 | 35 |  | `maekar-i-targaryen` / HEIR_TO / Great Council |
| 53 | `khal` | 20 | 34 | yes | `cohollo` / SWORN_TO / Khal |
| 54 | `house-darry` | 16 | 34 |  | `damon-darry` / SWORN_TO / House Darry |
| 55 | `century-of-blood` | 3 | 34 |  | `agnes-blackwood` / DIED_AT / Century of Blood |
| 56 | `great-pyramid` | 1 | 34 |  | `house-targaryen` / SEAT_OF / Great Pyramid |
| 57 | `tower-of-the-hand` | 1 | 34 |  | `jaehaerys-targaryen-son-of-aegon-ii` / DIED_AT / Tower of the Hand (track_b: Died) |
| 58 | `house-florent` | 18 | 33 |  | `aladore-florent` / SWORN_TO / House Florent |
| 59 | `summer-isles` | 16 | 33 |  | `bellegere-otherys` / PARENT_OF / Summer Isles |
| 60 | `crackclaw-point` | 5 | 33 |  | `dick-crabb` / BORN_AT / Crackclaw Point |
| 61 | `dragons` | 1 | 32 |  | `dance-of-the-dragons` / DEFEATS / dragons |
| 62 | `fingers` | 5 | 31 |  | `petyr-baelish` / BORN_AT / Fingers (track_b: Born) |
| 63 | `shae` | 3 | 31 |  | `tyrion-lannister` / LOVER_OF / Shae |
| 64 | `torrhen-manderly` | 1 | 31 |  | `desmond-manderly` / PARENT_OF / Torrhen Manderly |
| 65 | `flea-bottom` | 4 | 30 |  | `clayton-suggs` / BORN_AT / Flea Bottom |
| 66 | `faircastle` | 3 | 30 |  | `alester-wynch` / DIED_AT / Faircastle (track_b: Died) |
| 67 | `lucerys-velaryon` | 2 | 30 |  | `rhaenyra-targaryen` / PARENT_OF / Lucerys Velaryon |
| 68 | `crypt-of-winterfell` | 14 | 29 |  | `barthogan-stark` / BURIED_AT / Crypt of Winterfell |
| 69 | `runestone` | 6 | 29 |  | `andar-royce` / BORN_AT / Runestone |
| 70 | `house-durrandon` | 5 | 29 |  | `argella-durrandon` / SWORN_TO / House Durrandon |
| 71 | `daznaks-pit` | 1 | 29 |  | `yurkhaz-zo-yunzak` / DIED_AT / Daznak's Pit (track_b: Died) |
| 72 | `ruby-ford` | 1 | 29 |  | `rhaegar-targaryen` / DIED_AT / Ruby Ford (track_b: Died) |
| 73 | `rhoynar` | 11 | 28 |  | `druselka` / SWORN_TO / Rhoynar |
| 74 | `robert-baratheon` | 6 | 28 |  | `becca` / LOVER_OF / Robert Baratheon |
| 75 | `jason-lannister` | 10 | 27 |  | `alys-stackspear` / SPOUSE_OF / Jason Lannister |
| 76 | `lords-declarant` | 7 | 27 |  | `anya-waynwood` / SWORN_TO / Lords Declarant |
| 77 | `house-cerwyn` | 6 | 27 |  | `argelle-stark` / SWORN_TO / House Cerwyn |
| 78 | `jeyne-arryn` | 4 | 27 |  | `arnold-arryn` / OPPOSES / Jeyne Arryn (wiki:Arnold_Arryn) |
| 79 | `green-fork` | 3 | 27 |  | `conn` / DIED_AT / Green Fork (track_b: Died) |
| 80 | `thenns` | 2 | 27 |  | `alys-karstark` / SPOUSE_OF / Thenns |
| 81 | `lady-forlorn` | 1 | 27 |  | `house-corbray` / ANCESTRAL_WEAPON_OF / Lady Forlorn |
| 82 | `bear-island` | 9 | 26 |  | `alysane-mormont` / BORN_AT / Bear Island (track_b: Born) |
| 83 | `giants-lance` | 4 | 26 |  | `artys-i-arryn` / BORN_AT / Giant's Lance |
| 84 | `silent-sisters` | 4 | 26 |  | `alysanne-osgrey` / SWORN_TO / Silent Sisters |
| 85 | `arlan-of-pennytree` | 1 | 26 |  | `chestnut` / OWNS / Arlan of Pennytree |
| 86 | `paramour` | 1 | 26 |  | `ellaria-sand` / LOVER_OF / paramour (track_b: Lover) |
| 87 | `ship` | 1 | 26 |  | `quence` / SWORN_TO / Ship |
| 88 | `larys-strong` | 1 | 25 |  | `hour-of-the-wolf` / DEFEATS / Larys Strong |
| 89 | `house-gardener` | 10 | 24 |  | `alester-tyrell` / SWORN_TO / House Gardener |
| 90 | `stormcrows` | 7 | 24 |  | `daario-naharis` / SWORN_TO / Stormcrows |
| 91 | `oldstones` | 5 | 24 |  | `merrett-frey` / DIED_AT / Oldstones (track_b: Died) |
| 92 | `shipbreaker-bay` | 3 | 24 |  | `arrax` / DIED_AT / Shipbreaker Bay (track_b: Died) |
| 93 | `house-of-black-and-white` | 2 | 24 |  | `umma` / SWORN_TO / House of Black and White |
| 94 | `299-ac` | 1 | 24 |  | `house-bolton` / OVERLORD_OF / 299 AC (track_b: Overlords) |
| 95 | `betrothal` | 1 | 24 |  | `lyonel-baratheons-rebellion` / DEFEATS / Betrothal |
| 96 | `house-hornwood` | 7 | 23 |  | `berena-hornwood` / SWORN_TO / House Hornwood |
| 97 | `house-dustin` | 6 | 23 |  | `barbrey-dustin` / SWORN_TO / House Dustin |
| 98 | `shield-islands` | 4 | 23 |  | `talbert-serry` / DIED_AT / Shield Islands (track_b: Died) |
| 99 | `marwyn` | 1 | 23 |  | `qyburn` / RESPECTS / Marwyn |
| 100 | `298-ac` | 2 | 22 |  | `robert-i-baratheon` / HEIR_TO / 298 AC (track_b: Heirs) |

_(Long tail: 1253 additional missing targets. See `working/audits/orphan-edges-2026-04-30c-cat1-full.tsv` for the complete list.)_

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

Of 18635 edges across 4774 nodes, 15110 resolve cleanly. 3525 are orphan or stale, dominated by Cat 1 (3413 edges, 1353 unique slugs). Date-bleed status: 41 stragglers remain. Religion-bleed leftovers: 14. Title-like targets are a structural gap: 18 title slugs referenced by 62 edges with no node. Cat 2 alias-mismatches (57 edges) are not gaps — they're handled the moment the graph layer consults `working/wiki-parsed/alias-resolver.json` after a direct-slug miss.

## Recommended actions

Prioritized:

1. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers are the only category where data is actively wrong. Sources: barrow-hall, blackpool, braavos, deepwood-motte, greywater-watch, karhold, last-hearth, old-empire-of-ghis, raventree-hall, triarchy, vaes-dothrak, valyrian-freehold, whitetree, winterfell.

2. **HIGH — Re-emit the 41 date-bleed BORN_AT/DIED_AT nodes.** 39 unique source nodes affected. Sample: alys-stackspear, alyssa-blackwood, amarei-crakehall, annara-farring, bethany-rosby, cassana-estermont, corenna-swann, cyrenna-swann, denys-swann, dorna-swyft ….

3. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing targets into Tier 3 recovery. See Cat 1 table.

4. **MED — Wire alias-resolver into the graph query layer.** All 57 Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. Avoids touching 29 source nodes.

5. **MED — Stand up a Title Pass.** Promote the top 18 title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, ser, prince, princess, king, queen, etc.) to actual `title` nodes.

6. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit after Pass 1 chapter extractions add their own missing-target signal.

7. **LOW — Run schema-drift-auditor** on the 0 non-locked edge types observed.
