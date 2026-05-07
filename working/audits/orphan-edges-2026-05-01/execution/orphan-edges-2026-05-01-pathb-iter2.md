# Orphan Edges Audit — 2026-05-01-pathb-iter2

**Nodes scanned:** 7159
**Total edges checked:** 21027
**Edges that resolve cleanly:** 18720
**Orphan / problematic edges found:** 2307

**Breakdown:**
- Category 1 (target genuinely missing): 1973 edges across 828 unique missing targets
- Category 2 (alias-mismatch — resolves via alias-resolver): 292 edges across 34 unique alias slugs
- Stale-data legacy (religion-bleed leftovers): 0
- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): 42
- Title-like missing targets (subset of Cat 1): 51 edges, 24 unique title slugs

**Other observations:**
- Unknown edge types encountered (schema-drift; deferred to schema-drift-auditor): 0 occurrences across 0 types
- Malformed edge lines: 25
- Nodes with no `## Edges` section: 0

---

## Stale-data legacy: religion-bleed leftovers

Location nodes still carrying legacy `WORSHIPS` edges with religion-field category labels as targets (e.g., `religions`, `Mixed`, `Old gods`) instead of actual religion entities. Parser fix landed in Session 27; these nodes have not been re-emitted. **Batch-fix recommendation: re-emit affected location nodes from the corrected parser output.**

| Source node | Edge type | Target text | Target slug |
|---|---|---|---|

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

**24 unique title slugs referenced; 51 total edge references.**

**Recommendation:** stand up a Title Pass that promotes the most-referenced title slugs to actual nodes.

Top 30 title slugs by edge-count:

| Target slug | Edges referencing | in_count |
|---|---|---|
| `captain` | 20 | 0 |
| `lord-paramount-of-the-mander` | 8 | 6 |
| `lord-of-wyl` | 2 | 0 |
| `captain-of-the-guards-at-sunspear` | 1 | 0 |
| `princess-of-winterfell` | 1 | 0 |
| `captain-of-black-wind` | 1 | 0 |
| `captain-of-foamdrinker` | 1 | 0 |
| `captain-of-the-unsullied` | 1 | 0 |
| `lady-of-torrhens-square` | 1 | 0 |
| `warden-of-the-east-formerly` | 1 | 0 |
| `lady-of-the-eyrie` | 1 | 5 |
| `queen-of-the-rivers-and-the-hills` | 1 | 0 |
| `lady-of-felwood` | 1 | 0 |
| `lord-commander-of-the-rainbow-guard` | 1 | 0 |
| `queen-of-love-and-beauty` | 1 | 22 |
| `lord-of-darkdell` | 1 | 0 |
| `queen-of-the-high-tower` | 1 | 0 |
| `captain-of-the-salty-wench` | 1 | 0 |
| `lady-of-runestone` | 1 | 0 |
| `lady-of-coldmoat` | 1 | 7 |
| `captain-of-the-sea-bitch` | 1 | 0 |
| `high-king` | 1 | 0 |
| `king-of-winter-king-in-the-north` | 1 | 0 |
| `lord-of-highpoint` | 1 | 0 |

---

## Category 1: target genuinely missing

Sorted by `in_count` desc, then by edge_count. Top 100 of 828 unique missing targets shown.

Severity: **HIGH** for top entries (high in_count → many references → recovery candidate). **LOW** for long-tail singletons.

| # | Target slug | Edges in graph | Cross-ref in_count | Title-like | Example source / edge_type / target text |
|---|---|---|---|---|---|
| 1 | `small-council` | 1 | 215 |  | `qyburn` / MEMBER_OF / Small council |
| 2 | `blacks` | 124 | 138 |  | `addam-velaryon` / SWORN_TO / Blacks |
| 3 | `greens` | 75 | 127 |  | `adrian-tarbeck` / SWORN_TO / Greens |
| 4 | `narrow-sea` | 1 | 120 |  | `assassination-of-tywin-lannister` / DEFEATS / narrow sea |
| 5 | `unsullied` | 17 | 68 |  | `black-fist` / SWORN_TO / Unsullied |
| 6 | `haunted-forest` | 2 | 55 |  | `clubfoot-karl` / DIED_AT / Haunted forest (track_b: Died) |
| 7 | `queens-men` | 18 | 43 |  | `alester-florent` / SWORN_TO / Queen's men |
| 8 | `age-of-heroes` | 1 | 43 |  | `battle-of-crookwater` / FIGHTS_IN / Age of Heroes |
| 9 | `crossroads-inn` | 2 | 39 |  | `masha-heddle` / DIED_AT / Crossroads inn (track_b: Died) |
| 10 | `dothraki-sea` | 21 | 35 |  | `caggo` / BORN_AT / Dothraki Sea |
| 11 | `dragons` | 1 | 32 |  | `dance-of-the-dragons` / DEFEATS / dragons |
| 12 | `flea-bottom` | 5 | 30 |  | `clayton-suggs` / BORN_AT / Flea Bottom |
| 13 | `crypt-of-winterfell` | 14 | 29 |  | `barthogan-stark` / BURIED_AT / Crypt of Winterfell |
| 14 | `ruby-ford` | 1 | 29 |  | `rhaegar-targaryen` / DIED_AT / Ruby Ford (track_b: Died) |
| 15 | `silent-sisters` | 4 | 26 |  | `alysanne-osgrey` / SWORN_TO / Silent Sisters |
| 16 | `ship` | 2 | 26 |  | `allaquo` / SWORN_TO / Ship |
| 17 | `299-ac` | 1 | 24 |  | `house-bolton` / OVERLORD_OF / 299 AC (track_b: Overlords) |
| 18 | `betrothal` | 1 | 24 |  | `lyonel-baratheons-rebellion` / DEFEATS / Betrothal |
| 19 | `joffrey-i-baratheon` | 2 | 22 |  | `robert-i-baratheon` / SUCCEEDS / Joffrey I Baratheon |
| 20 | `queen-of-love-and-beauty` | 1 | 22 | yes | `lord-ashfords-daughter` / HOLDS_TITLE / Queen of Love and Beauty |
| 21 | `vale` | 5 | 21 |  | `battle-in-the-waters-off-gulltown` / DEFEATS / Vale |
| 22 | `two-betrayers` | 2 | 21 |  | `hugh-hammer` / SWORN_TO / Two Betrayers |
| 23 | `cinnamon-wind` | 2 | 19 |  | `aemon-targaryen-son-of-maekar-i` / DIED_AT / Cinnamon Wind |
| 24 | `tower-of-joy` | 1 | 18 |  | `roberts-rebellion` / FIGHTS_IN / Tower of joy |
| 25 | `andal-invasion` | 3 | 17 |  | `battle-of-the-seven-stars` / FIGHTS_IN / Andal invasion |
| 26 | `lads` | 3 | 16 |  | `alysanne-blackwood` / SWORN_TO / Lads |
| 27 | `282-ac` | 1 | 16 |  | `house-baratheon` / OVERLORD_OF / 282 AC (track_b: Overlords) |
| 28 | `moon-of-the-three-kings` | 1 | 16 |  | `riot-of-kings-landing-dance-of-the-dragons` / DEFEATS / Moon of the Three Kings |
| 29 | `300-ac` | 1 | 15 |  | `house-bolton` / OVERLORD_OF / 300 AC (track_b: Overlords) |
| 30 | `pirates` | 2 | 12 |  | `korra` / SWORN_TO / Pirates |
| 31 | `elephant` | 1 | 12 |  | `trianna` / SWORN_TO / Elephant |
| 32 | `winter-wolves` | 1 | 12 |  | `roderick-dustin` / SWORN_TO / Winter Wolves |
| 33 | `chatayas-brothel` | 6 | 11 |  | `alayaya` / SWORN_TO / Chataya's brothel |
| 34 | `happy-port` | 6 | 10 |  | `assadora` / SWORN_TO / Happy Port |
| 35 | `kings-men` | 5 | 10 |  | `andrew-estermont` / SWORN_TO / King's men |
| 36 | `the-wall` | 1 | 10 |  | `harma-dogshead` / DIED_AT / The Wall (track_b: Died) |
| 37 | `king-s-landing` | 1 | 9 |  | `bramm-of-blackhull` / DIED_AT / King’s Landing (track_b: Died) |
| 38 | `kings-of-the-reach` | 1 | 9 |  | `order-of-the-green-hand` / SWORN_TO / Kings of the Reach |
| 39 | `tommen-i-baratheon` | 7 | 8 |  | `boots` / OWNS / Tommen I Baratheon |
| 40 | `battle-of-the-red-fork` | 1 | 8 |  | `daven-lannister` / FIGHTS_IN / Battle of the Red Fork |
| 41 | `frozen-shore` | 1 | 8 |  | `great-walrus` / BORN_AT / Frozen Shore |
| 42 | `storm-kings` | 1 | 8 |  | `battle-of-six-kings` / DEFEATS / Storm Kings |
| 43 | `the-gate` | 1 | 8 |  | `izembaro` / SWORN_TO / The Gate |
| 44 | `house-flint` | 3 | 7 |  | `byam-flint` / SWORN_TO / House Flint |
| 45 | `iron-bank` | 1 | 7 |  | `bessaro-reyaan` / SWORN_TO / Iron Bank |
| 46 | `lady-of-coldmoat` | 1 | 7 | yes | `rohanne-webber` / HOLDS_TITLE / Lady of Coldmoat |
| 47 | `lord-paramount-of-the-mander` | 8 | 6 | yes | `bertrand-tyrell` / HOLDS_TITLE / Lord Paramount of the Mander |
| 48 | `bastards-boys` | 3 | 6 |  | `grunt` / SWORN_TO / Bastard's Boys |
| 49 | `house-fossoway` | 3 | 6 |  | `derrick-fossoway` / SWORN_TO / House Fossoway |
| 50 | `valyrian-peninsula` | 1 | 6 |  | `aurion` / DIED_AT / Valyrian peninsula (track_b: Died) |
| 51 | `wedding-of-aegon-iii-targaryen-and-jaehaera-targaryen` | 1 | 6 |  | `dance-of-the-dragons` / DEFEATS / Wedding of Aegon III Targaryen and Jaehaera Targaryen |
| 52 | `yunkish` | 1 | 6 |  | `crunch` / DIED_AT / Yunkish (track_b: Died) |
| 53 | `artys-arryn` | 3 | 5 |  | `robar-ii-royce` / SUCCEEDS / Artys Arryn |
| 54 | `drowned-men` | 3 | 5 |  | `emmond` / SWORN_TO / Drowned men |
| 55 | `battle-of-stonebridge` | 1 | 5 |  | `faith-militant-uprising` / FIGHTS_IN / Battle of Stonebridge |
| 56 | `lady-of-the-eyrie` | 1 | 5 | yes | `jeyne-arryn` / HOLDS_TITLE / Lady of the Eyrie |
| 57 | `motherhouse-of-maris` | 1 | 5 |  | `jeyne-arryn` / DIED_AT / Motherhouse of Maris (track_b: Died) |
| 58 | `elephants` | 3 | 4 |  | `doniphos-paenymion` / SWORN_TO / Elephants |
| 59 | `last-greenseer` | 3 | 4 |  | `ash` / SWORN_TO / last greenseer |
| 60 | `tiger` | 3 | 4 |  | `belicho` / SWORN_TO / Tiger |
| 61 | `battle-at-the-mander` | 1 | 4 |  | `roberts-rebellion` / FIGHTS_IN / Battle at the Mander |
| 62 | `battle-of-the-green-fork` | 1 | 4 |  | `bronn` / FIGHTS_IN / Battle of the Green Fork |
| 63 | `battle-of-the-whispering-wood` | 1 | 4 |  | `jaime-lannister` / FIGHTS_IN / Battle of the Whispering Wood |
| 64 | `lichyard` | 1 | 4 |  | `mikken` / BURIED_AT / lichyard |
| 65 | `pyntos` | 1 | 4 |  | `pynto` / SWORN_TO / Pynto's |
| 66 | `free-company` | 1 | 3 |  | `howard-bullock` / SWORN_TO / Free Company |
| 67 | `oakenseat` | 1 | 3 |  | `anarchy-in-the-reach` / DEFEATS / Oakenseat |
| 68 | `old-palace` | 1 | 3 |  | `house-martell` / SEAT_OF / Old Palace |
| 69 | `conflict-beyond-the-wall` | 6 | 2 |  | `attack-on-castle-black` / FIGHTS_IN / Conflict beyond the Wall |
| 70 | `great-hall` | 3 | 2 |  | `aerys-ii-targaryen` / DIED_AT / Great Hall (track_b: Died) |
| 71 | `daemon-blackfyre` | 1 | 2 |  | `house-blackfyre` / FOUNDED / Daemon Blackfyre |
| 72 | `godswife` | 1 | 2 |  | `mirri-maz-duur` / HOLDS_TITLE / Godswife |
| 73 | `kingdom-of-the-three-daughters` | 1 | 2 |  | `racallio-ryndoon` / SWORN_TO / Kingdom of the Three Daughters |
| 74 | `sarnori` | 1 | 2 |  | `mazor-alexi` / CULTURE_OF / Sarnori |
| 75 | `silent-sister` | 1 | 2 |  | `maris-baratheon` / HOLDS_TITLE / Silent sister |
| 76 | `slate` | 1 | 2 |  | `house-slate` / RULES / Slate |
| 77 | `lannister` | 15 | 1 |  | `battle-at-the-mummers-ford` / DEFEATS / Lannister |
| 78 | `the-vale` | 9 | 1 |  | `roland-i-arryn` / DIED_AT / the Vale |
| 79 | `cerelle-lannister` | 6 | 1 |  | `gerold-lannister` / SUCCEEDS / Cerelle Lannister |
| 80 | `drogos-khalasar` | 4 | 1 |  | `drogo` / SWORN_TO / Drogo's khalasar |
| 81 | `2-bc` | 3 | 1 |  | `house-baratheon` / OVERLORD_OF / 2 BC (track_b: Overlords) |
| 82 | `thenn` | 3 | 1 |  | `sigorn` / BORN_AT / Thenn |
| 83 | `aegon-ii` | 1 | 1 |  | `dance-of-the-dragons` / DEFEATS / Aegon II |
| 84 | `aegon-iii` | 1 | 1 |  | `dance-of-the-dragons` / DEFEATS / Aegon III |
| 85 | `aegon-vi-targaryen` | 1 | 1 |  | `varys` / SWORN_TO / Aegon VI Targaryen |
| 86 | `blackfyre-rebellions` | 1 | 1 |  | `second-blackfyre-rebellion` / FIGHTS_IN / Blackfyre Rebellions |
| 87 | `house-farwynd` | 1 | 1 |  | `triston-farwynd` / SWORN_TO / House Farwynd |
| 88 | `joffrey-lydden` | 1 | 1 |  | `gerold-iii-lannister` / SUCCEEDS / Joffrey Lydden |
| 89 | `lord-caswell` | 1 | 1 |  | `lady-caswell` / SPOUSE_OF / Lord Caswell |
| 90 | `lord-commander` | 1 | 1 |  | `mutiny-at-castle-black` / DEFEATS / Lord Commander |
| 91 | `rhaenyra` | 1 | 1 |  | `dance-of-the-dragons` / DEFEATS / Rhaenyra |
| 92 | `sabitha-vypren` | 1 | 1 |  | `forrest-frey` / SPOUSE_OF / Sabitha Vypren |
| 93 | `sea-watch` | 1 | 1 |  | `tristimun` / MEMBER_OF / Sea watch |
| 94 | `unknown` | 321 | 0 |  | `addam-hightower` / SPOUSE_OF / Unknown |
| 95 | `the-citadel` | 83 | 0 |  | `abelon` / SWORN_TO / The Citadel |
| 96 | `extinct` | 37 | 0 |  | `house-amber` / RULES / Extinct |
| 97 | `son` | 31 | 0 |  | `alyn-tarbeck` / PARENT_OF / Son |
| 98 | `none` | 29 | 0 |  | `aerys-i-targaryen` / PARENT_OF / None |
| 99 | `sons` | 27 | 0 |  | `antario-jast` / PARENT_OF / Sons |
| 100 | `daughter` | 26 | 0 |  | `alysane-mormont` / PARENT_OF / Daughter |

_(Long tail: 728 additional missing targets. See `working/audits/orphan-edges-2026-05-01-pathb-iter2-cat1-full.tsv` for the complete list.)_

---

## Category 2: alias-mismatch (resolvable via alias-resolver)

These targets fail direct slug-match but DO resolve via the alias-resolver. **292 edges across 34 unique alias slugs** are affected.

Severity: **MED** — slug-format-drift, not a graph gap. Recommend the graph layer consult the alias-resolver after a direct-slug miss.

Top 50 by edge count:

| Target slug attempted | Resolves to canonical | Edges affected | Example |
|---|---|---|---|
| `stormlander` | `stormlanders` | 119 | `aelinor-penrose` / CULTURE_OF / Stormlander |
| `andal` | `andals` | 63 | `alester-ii-arryn` / CULTURE_OF / Andal |
| `lysene` | `lyseni` | 26 | `bambarro-bazanne` / CULTURE_OF / Lysene |
| `dornish` | `dornishmen` | 15 | `alleras` / CULTURE_OF / Dornish (track_b: Race) |
| `ramsay-bolton` | `ramsay-snow` | 14 | `alison` / OWNS / Ramsay Bolton |
| `catelyn-tully` | `catelyn-stark` | 6 | `arya-stark` / PARENT_OF / Catelyn Tully |
| `varamyr-sixskins` | `varamyr` | 4 | `greyskin` / OWNS / Varamyr Sixskins |
| `lysa-tully` | `lysa-arryn` | 4 | `hoster-tully` / PARENT_OF / Lysa Tully |
| `barbrey-ryswell` | `barbrey-dustin` | 3 | `brandon-stark` / LOVER_OF / Barbrey Ryswell |
| `bethany-ryswell` | `bethany-bolton` | 3 | `domeric-bolton` / PARENT_OF / Bethany Ryswell |
| `durran-the-devout` | `durran-ii-durrandon` | 3 | `durran-godsgrief` / HEIR_TO / Durran the Devout |
| `sybelle-locke` | `sybelle-glover` | 3 | `erena-glover` / PARENT_OF / Sybelle Locke |
| `johanna-westerling` | `johanna-lannister` | 3 | `loreon-lannister-son-of-jason` / PARENT_OF / Johanna Westerling |
| `ravella-swann` | `ravella-smallwood` | 2 | `carellen-smallwood` / PARENT_OF / Ravella Swann |
| `donella-manderly` | `donella-hornwood` | 2 | `daryn-hornwood` / PARENT_OF / Donella Manderly |
| `dornishman` | `dornishmen` | 2 | `davos-dayne` / CULTURE_OF / Dornishman |
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
| `lhazarene` | `lhazareen` | 1 | `red-lamb` / CULTURE_OF / Lhazarene |
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

Of 21027 edges across 7159 nodes, 18720 resolve cleanly. 2307 are orphan or stale, dominated by Cat 1 (1973 edges, 828 unique slugs). Date-bleed status: 42 stragglers remain. Religion-bleed leftovers: 0. Title-like targets are a structural gap: 24 title slugs referenced by 51 edges with no node. Cat 2 alias-mismatches (292 edges) are not gaps — they're handled the moment the graph layer consults `working/wiki-parsed/alias-resolver.json` after a direct-slug miss.

## Recommended actions

Prioritized:

1. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers are the only category where data is actively wrong. Sources: .

2. **HIGH — Re-emit the 42 date-bleed BORN_AT/DIED_AT nodes.** 40 unique source nodes affected. Sample: alys-stackspear, alyssa-blackwood, amarei-crakehall, annara-farring, bethany-rosby, cassana-estermont, corenna-swann, cyrenna-swann, denys-swann, dorna-swyft ….

3. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing targets into Tier 3 recovery. See Cat 1 table.

4. **MED — Wire alias-resolver into the graph query layer.** All 292 Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. Avoids touching 34 source nodes.

5. **MED — Stand up a Title Pass.** Promote the top 24 title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, ser, prince, princess, king, queen, etc.) to actual `title` nodes.

6. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit after Pass 1 chapter extractions add their own missing-target signal.

7. **LOW — Run schema-drift-auditor** on the 0 non-locked edge types observed.
