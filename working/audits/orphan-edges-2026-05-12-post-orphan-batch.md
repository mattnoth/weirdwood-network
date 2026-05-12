# Orphan Edges Audit — 2026-05-12-post-orphan-batch

**Nodes scanned:** 7720
**Total edges checked:** 21087
**Edges that resolve cleanly:** 19055
**Orphan / problematic edges found:** 2004

**Breakdown:**
- Category 1 (target genuinely missing): 1673 edges across 814 unique missing targets
- Category 2 (alias-mismatch — resolves via alias-resolver): 289 edges across 35 unique alias slugs
- Stale-data legacy (religion-bleed leftovers): 0
- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): 42
- Title-like missing targets (subset of Cat 1): 49 edges, 22 unique title slugs

**Other observations:**
- Unknown edge types encountered (schema-drift; deferred to schema-drift-auditor): 28 occurrences across 4 types
- Malformed edge lines: 42
- Nodes with no `## Edges` section: 19

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

**22 unique title slugs referenced; 49 total edge references.**

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
| `lord-of-darkdell` | 1 | 0 |
| `queen-of-the-high-tower` | 1 | 0 |
| `captain-of-the-salty-wench` | 1 | 0 |
| `lady-of-runestone` | 1 | 0 |
| `lady-of-coldmoat` | 1 | 7 |
| `captain-of-the-sea-bitch` | 1 | 0 |
| `king-of-winter-king-in-the-north` | 1 | 0 |
| `lord-of-highpoint` | 1 | 0 |

---

## Category 1: target genuinely missing

Sorted by `in_count` desc, then by edge_count. Top 100 of 814 unique missing targets shown.

Severity: **HIGH** for top entries (high in_count → many references → recovery candidate). **LOW** for long-tail singletons.

| # | Target slug | Edges in graph | Cross-ref in_count | Title-like | Example source / edge_type / target text |
|---|---|---|---|---|---|
| 1 | `crossroads-inn` | 2 | 39 |  | `masha-heddle` / DIED_AT / Crossroads inn (track_b: Died) |
| 2 | `dragons` | 1 | 32 |  | `dance-of-the-dragons` / DEFEATS / dragons |
| 3 | `ship` | 2 | 26 |  | `allaquo` / SWORN_TO / Ship |
| 4 | `299-ac` | 1 | 24 |  | `house-bolton` / OVERLORD_OF / 299 AC (track_b: Overlords) |
| 5 | `betrothal` | 1 | 24 |  | `lyonel-baratheons-rebellion` / DEFEATS / Betrothal |
| 6 | `joffrey-i-baratheon` | 2 | 22 |  | `robert-i-baratheon` / SUCCEEDS / Joffrey I Baratheon |
| 7 | `vale` | 5 | 21 |  | `battle-in-the-waters-off-gulltown` / DEFEATS / Vale |
| 8 | `lads` | 3 | 16 |  | `alysanne-blackwood` / SWORN_TO / Lads |
| 9 | `282-ac` | 1 | 16 |  | `house-baratheon` / OVERLORD_OF / 282 AC (track_b: Overlords) |
| 10 | `moon-of-the-three-kings` | 1 | 16 |  | `riot-of-kings-landing-dance-of-the-dragons` / DEFEATS / Moon of the Three Kings |
| 11 | `300-ac` | 1 | 15 |  | `house-bolton` / OVERLORD_OF / 300 AC (track_b: Overlords) |
| 12 | `giant` | 1 | 14 |  | `wun-weg-wun-dar-wun` / CULTURE_OF / Giant |
| 13 | `happy-port` | 6 | 10 |  | `assadora` / SWORN_TO / Happy Port |
| 14 | `kings-men` | 5 | 10 |  | `andrew-estermont` / SWORN_TO / King's men |
| 15 | `the-wall` | 1 | 10 |  | `harma-dogshead` / DIED_AT / The Wall (track_b: Died) |
| 16 | `dornish` | 15 | 9 |  | `alleras` / CULTURE_OF / Dornish (track_b: Race) |
| 17 | `king-s-landing` | 1 | 9 |  | `bramm-of-blackhull` / DIED_AT / King’s Landing (track_b: Died) |
| 18 | `kings-of-the-reach` | 1 | 9 |  | `order-of-the-green-hand` / SWORN_TO / Kings of the Reach |
| 19 | `tommen-i-baratheon` | 7 | 8 |  | `boots` / OWNS / Tommen I Baratheon |
| 20 | `storm-kings` | 1 | 8 |  | `battle-of-six-kings` / DEFEATS / Storm Kings |
| 21 | `the-gate` | 1 | 8 |  | `izembaro` / SWORN_TO / The Gate |
| 22 | `house-flint` | 3 | 7 |  | `byam-flint` / SWORN_TO / House Flint |
| 23 | `iron-bank` | 1 | 7 |  | `bessaro-reyaan` / SWORN_TO / Iron Bank |
| 24 | `lady-of-coldmoat` | 1 | 7 | yes | `rohanne-webber` / HOLDS_TITLE / Lady of Coldmoat |
| 25 | `lord-paramount-of-the-mander` | 8 | 6 | yes | `bertrand-tyrell` / HOLDS_TITLE / Lord Paramount of the Mander |
| 26 | `house-fossoway` | 3 | 6 |  | `derrick-fossoway` / SWORN_TO / House Fossoway |
| 27 | `wedding-of-aegon-iii-targaryen-and-jaehaera-targaryen` | 1 | 6 |  | `dance-of-the-dragons` / DEFEATS / Wedding of Aegon III Targaryen and Jaehaera Targaryen |
| 28 | `yunkish` | 1 | 6 |  | `crunch` / DIED_AT / Yunkish (track_b: Died) |
| 29 | `battle-of-stonebridge` | 1 | 5 |  | `faith-militant-uprising` / FIGHTS_IN / Battle of Stonebridge |
| 30 | `lady-of-the-eyrie` | 1 | 5 | yes | `jeyne-arryn` / HOLDS_TITLE / Lady of the Eyrie |
| 31 | `motherhouse-of-maris` | 1 | 5 |  | `jeyne-arryn` / DIED_AT / Motherhouse of Maris (track_b: Died) |
| 32 | `elephants` | 3 | 4 |  | `doniphos-paenymion` / SWORN_TO / Elephants |
| 33 | `last-greenseer` | 3 | 4 |  | `ash` / SWORN_TO / last greenseer |
| 34 | `battle-at-the-mander` | 1 | 4 |  | `roberts-rebellion` / FIGHTS_IN / Battle at the Mander |
| 35 | `pyntos` | 1 | 4 |  | `pynto` / SWORN_TO / Pynto's |
| 36 | `free-company` | 1 | 3 |  | `howard-bullock` / SWORN_TO / Free Company |
| 37 | `conflict-beyond-the-wall` | 6 | 2 |  | `attack-on-castle-black` / FIGHTS_IN / Conflict beyond the Wall |
| 38 | `great-hall` | 3 | 2 |  | `aerys-ii-targaryen` / DIED_AT / Great Hall (track_b: Died) |
| 39 | `daemon-blackfyre` | 1 | 2 |  | `house-blackfyre` / FOUNDED / Daemon Blackfyre |
| 40 | `kingdom-of-the-three-daughters` | 1 | 2 |  | `racallio-ryndoon` / SWORN_TO / Kingdom of the Three Daughters |
| 41 | `sarnori` | 1 | 2 |  | `mazor-alexi` / CULTURE_OF / Sarnori |
| 42 | `lannister` | 15 | 1 |  | `battle-at-the-mummers-ford` / DEFEATS / Lannister |
| 43 | `cerelle-lannister` | 6 | 1 |  | `gerold-lannister` / SUCCEEDS / Cerelle Lannister |
| 44 | `2-bc` | 3 | 1 |  | `house-baratheon` / OVERLORD_OF / 2 BC (track_b: Overlords) |
| 45 | `thenn` | 3 | 1 |  | `sigorn` / BORN_AT / Thenn |
| 46 | `aegon-ii` | 1 | 1 |  | `dance-of-the-dragons` / DEFEATS / Aegon II |
| 47 | `aegon-iii` | 1 | 1 |  | `dance-of-the-dragons` / DEFEATS / Aegon III |
| 48 | `aegon-vi-targaryen` | 1 | 1 |  | `varys` / SWORN_TO / Aegon VI Targaryen |
| 49 | `blackfyre-rebellions` | 1 | 1 |  | `second-blackfyre-rebellion` / FIGHTS_IN / Blackfyre Rebellions |
| 50 | `house-farwynd` | 1 | 1 |  | `triston-farwynd` / SWORN_TO / House Farwynd |
| 51 | `joffrey-lydden` | 1 | 1 |  | `gerold-iii-lannister` / SUCCEEDS / Joffrey Lydden |
| 52 | `lord-caswell` | 1 | 1 |  | `lady-caswell` / SPOUSE_OF / Lord Caswell |
| 53 | `lord-commander` | 1 | 1 |  | `mutiny-at-castle-black` / DEFEATS / Lord Commander |
| 54 | `rhaenyra` | 1 | 1 |  | `dance-of-the-dragons` / DEFEATS / Rhaenyra |
| 55 | `sea-watch` | 1 | 1 |  | `tristimun` / MEMBER_OF / Sea watch |
| 56 | `unknown` | 321 | 0 |  | `addam-hightower` / SPOUSE_OF / Unknown |
| 57 | `the-citadel` | 83 | 0 |  | `abelon` / SWORN_TO / The Citadel |
| 58 | `extinct` | 37 | 0 |  | `house-amber` / RULES / Extinct |
| 59 | `son` | 31 | 0 |  | `alyn-tarbeck` / PARENT_OF / Son |
| 60 | `none` | 29 | 0 |  | `aerys-i-targaryen` / PARENT_OF / None |
| 61 | `sons` | 27 | 0 |  | `antario-jast` / PARENT_OF / Sons |
| 62 | `daughter` | 26 | 0 |  | `alysane-mormont` / PARENT_OF / Daughter |
| 63 | `captain` | 20 | 0 | yes | `alvyn-sharp` / HOLDS_TITLE / Captain |
| 64 | `commander` | 13 | 0 |  | `bedwyck` / HOLDS_TITLE / Commander |
| 65 | `daughters` | 8 | 0 |  | `choq-choq` / PARENT_OF / Daughters |
| 66 | `two-daughters` | 8 | 0 |  | `corwyn-corbray` / PARENT_OF / Two daughters |
| 67 | `unborn-child` | 8 | 0 |  | `alyce-graceford` / PARENT_OF / Unborn child |
| 68 | `gate` | 7 | 0 |  | `big-brusco` / SWORN_TO / Gate |
| 69 | `deceased-husband` | 6 | 0 |  | `anya-waynwood` / SPOUSE_OF / Deceased husband |
| 70 | `deceased-wife` | 6 | 0 |  | `mors-umber` / SPOUSE_OF / Deceased wife |
| 71 | `golden-company-victory` | 6 | 0 |  | `fall-of-mistwood` / DEFEATS / Golden Company victory |
| 72 | `lord-marshal-of-the-mander` | 6 | 0 |  | `desmond-manderly` / HOLDS_TITLE / Lord Marshal of the Mander |
| 73 | `red-keep-kings-landing` | 6 | 0 |  | `aemon-targaryen-son-of-viserys-ii` / BORN_AT / Red Keep, King's Landing |
| 74 | `the-reach` | 6 | 0 |  | `house-ambrose` / REGION_OF / The Reach |
| 75 | `a-son` | 5 | 0 |  | `davos-dayne` / PARENT_OF / A son |
| 76 | `at-least-one-son` | 5 | 0 |  | `arlan-i-durrandon` / PARENT_OF / At least one son |
| 77 | `brother` | 5 | 0 |  | `clement` / HOLDS_TITLE / Brother |
| 78 | `father-is-oberyn-martell` | 5 | 0 |  | `nymeria-sand` / PARENT_OF / (reverse) Father is Oberyn Martell |
| 79 | `iron-throne-victory` | 5 | 0 |  | `burning-of-the-sept-of-remembrance` / DEFEATS / Iron Throne victory |
| 80 | `three-sons` | 5 | 0 |  | `ambrose-butterwell` / PARENT_OF / Three sons |
| 81 | `three-wives` | 5 | 0 |  | `horton-redfort` / SPOUSE_OF / Three wives |
| 82 | `1-unknown` | 4 | 0 |  | `cregan-karstark` / SPOUSE_OF / 1: Unknown |
| 83 | `durrandon` | 4 | 0 |  | `battle-by-the-bloody-pool` / DEFEATS / Durrandon |
| 84 | `goodman` | 4 | 0 |  | `beck` / HOLDS_TITLE / Goodman |
| 85 | `khal-drogos-khalasar` | 4 | 0 |  | `doreah` / SWORN_TO / Khal Drogo's khalasar |
| 86 | `2-unknown` | 3 | 0 |  | `cregan-karstark` / SPOUSE_OF / 2: Unknown |
| 87 | `300-ac-meereen` | 3 | 0 |  | `loyal-spear` / DIED_AT / 300 AC, Meereen |
| 88 | `a-daughter` | 3 | 0 |  | `gerold-iii-lannister` / HEIR_TO / A daughter |
| 89 | `admiral` | 3 | 0 |  | `alyn-velaryon` / HOLDS_TITLE / Admiral |
| 90 | `at-least-four-sons` | 3 | 0 |  | `agnes-blackwood` / PARENT_OF / At least four sons |
| 91 | `balon-ix-greyjoy` | 3 | 0 |  | `euron-greyjoy` / SUCCEEDS / Balon IX Greyjoy |
| 92 | `bolton` | 3 | 0 |  | `battle-outside-the-gates-of-winterfell` / DEFEATS / Bolton |
| 93 | `cerwyn` | 3 | 0 |  | `cley-cerwyn` / BORN_AT / Cerwyn (track_b: Born) |
| 94 | `euron-iii-greyjoy` | 3 | 0 |  | `balon-greyjoy` / SUCCEEDS / Euron III Greyjoy (track_b: Successor) |
| 95 | `four-wives` | 3 | 0 |  | `jasper-wylde` / SPOUSE_OF / Four wives |
| 96 | `healing` | 3 | 0 |  | `ebrose` / HOLDS_TITLE / healing |
| 97 | `house-baratheon-of-storms-end` | 3 | 0 |  | `holy-hundred` / SWORN_TO / House Baratheon of Storm's End (track_b: Allegiance) |
| 98 | `house-tyrell-of-highgarden` | 3 | 0 |  | `garlan-tyrell` / SWORN_TO / House Tyrell of Highgarden |
| 99 | `issue` | 3 | 0 |  | `garth-the-gardener` / PARENT_OF / Issue |
| 100 | `lady-stonetree` | 3 | 0 |  | `harlon-greyjoy` / PARENT_OF / Lady Stonetree |

_(Long tail: 714 additional missing targets. See `working/audits/orphan-edges-2026-05-12-post-orphan-batch-cat1-full.tsv` for the complete list.)_

---

## Category 2: alias-mismatch (resolvable via alias-resolver)

These targets fail direct slug-match but DO resolve via the alias-resolver. **289 edges across 35 unique alias slugs** are affected.

Severity: **MED** — slug-format-drift, not a graph gap. Recommend the graph layer consult the alias-resolver after a direct-slug miss.

Top 50 by edge count:

| Target slug attempted | Resolves to canonical | Edges affected | Example |
|---|---|---|---|
| `stormlander` | `stormlanders` | 119 | `aelinor-penrose` / CULTURE_OF / Stormlander |
| `andal` | `andals` | 63 | `alester-ii-arryn` / CULTURE_OF / Andal |
| `lysene` | `lyseni` | 26 | `bambarro-bazanne` / CULTURE_OF / Lysene |
| `ramsay-bolton` | `ramsay-snow` | 14 | `alison` / OWNS / Ramsay Bolton |
| `the-vale` | `vale-of-arryn` | 9 | `roland-i-arryn` / DIED_AT / the Vale |
| `catelyn-tully` | `catelyn-stark` | 6 | `arya-stark` / PARENT_OF / Catelyn Tully |
| `varamyr-sixskins` | `varamyr` | 4 | `greyskin` / OWNS / Varamyr Sixskins |
| `lysa-tully` | `lysa-arryn` | 4 | `hoster-tully` / PARENT_OF / Lysa Tully |
| `barbrey-ryswell` | `barbrey-dustin` | 3 | `brandon-stark` / LOVER_OF / Barbrey Ryswell |
| `bethany-ryswell` | `bethany-bolton` | 3 | `domeric-bolton` / PARENT_OF / Bethany Ryswell |
| `durran-the-devout` | `durran-ii-durrandon` | 3 | `durran-godsgrief` / HEIR_TO / Durran the Devout |
| `sybelle-locke` | `sybelle-glover` | 3 | `erena-glover` / PARENT_OF / Sybelle Locke |
| `johanna-westerling` | `johanna-lannister` | 3 | `loreon-lannister-son-of-jason` / PARENT_OF / Johanna Westerling |
| `artys-arryn` | `winged-knight` | 3 | `robar-ii-royce` / SUCCEEDS / Artys Arryn |
| `ravella-swann` | `ravella-smallwood` | 2 | `carellen-smallwood` / PARENT_OF / Ravella Swann |
| `donella-manderly` | `donella-hornwood` | 2 | `daryn-hornwood` / PARENT_OF / Donella Manderly |
| `dornishman` | `dornishmen` | 2 | `davos-dayne` / CULTURE_OF / Dornishman |
| `olenna-redwyne` | `olenna-tyrell` | 2 | `luthor-tyrell` / SPOUSE_OF / Olenna Redwyne |
| `janna-tyrell` | `janna-fossoway` | 2 | `luthor-tyrell` / PARENT_OF / Janna Tyrell |
| `tyanna-of-pentos` | `tyanna-of-the-tower` | 1 | `alys-harroway` / LOVER_OF / Tyanna of Pentos (track_b: Lovers) |
| `brandon-the-shipwright` | `brandon-stark-shipwright` | 1 | `brandon-stark-burner` / SUCCEEDS / Brandon the Shipwright |
| `brandon-the-burner` | `brandon-stark-burner` | 1 | `brandon-stark-shipwright` / SUCCEEDS / Brandon the Burner |
| `durran-the-fair` | `durran-durrandon-the-fair` | 1 | `erich-durrandon-the-sailmaker` / PARENT_OF / Durran the Fair |
| `sabitha-vypren` | `sabitha-frey` | 1 | `forrest-frey` / SPOUSE_OF / Sabitha Vypren |
| `minisa-whent` | `minisa-tully` | 1 | `hoster-tully` / SPOUSE_OF / Minisa Whent |
| `smalljon-umber` | `jon-umber-son-of-jon` | 1 | `jon-umber` / PARENT_OF / Smalljon Umber |
| `jocasta-tarbeck` | `jocasta-lannister` | 1 | `lyman-lannister` / SPOUSE_OF / Jocasta Tarbeck |
| `alyn-of-hull` | `alyn-velaryon` | 1 | `marilda-of-hull` / PARENT_OF / Alyn of Hull |
| `silent-sister` | `silent-sisters` | 1 | `maris-baratheon` / HOLDS_TITLE / Silent sister |
| `longspear-ryk` | `ryk` | 1 | `munda` / SPOUSE_OF / Longspear Ryk |
| `taena-of-myr` | `taena-merryweather` | 1 | `orton-merryweather` / SPOUSE_OF / Taena of Myr |
| `argilac-the-arrogant` | `argilac-durrandon` | 1 | `orys-baratheon` / KILLS / Argilac the Arrogant |
| `lucinda-broome` | `lucinda-tully` | 1 | `prentys-tully` / SPOUSE_OF / Lucinda Broome |
| `lhazarene` | `lhazareen` | 1 | `red-lamb` / CULTURE_OF / Lhazarene |
| `elia-of-dorne` | `elia-martell` | 1 | `sack-of-kings-landing` / DEFEATS / Elia of Dorne |

---

## Category 3: redirect-resolution (wiki redirect chain)

**Not separately classified in this run.** The Session 27 cleanup leaves the most actionable signal in Cat 1 / Cat 2 / stale / date-bleed; redirect-resolution is a future pass.

If a follow-up wants to mine Cat 3 specifically, the procedure: take Cat 1 entries with `in_count >= 5`, look up each `<Page_Name>.json` in `sources/wiki/_raw/`, and check whether the cached HTML body matches `<div class="redirectMsg">…</div>`. If so, the target slug should be remapped to the redirect target.

---

## Unknown edge types (deferred to schema-drift-auditor)

Per the conflict protocol, these edges were skipped (their targets were not classified).

| Edge type | Occurrences |
|---|---|
| `HELD_BY` | 24 |
| `KILLED_BY` | 2 |
| `DECEIVED_BY` | 1 |
| `PART_OF` | 1 |

---

## Malformed `## Edges` lines

42 bullet lines did not match the `- TYPE: target` pattern. Sample (up to 30):

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
| `brotherhood-without-banners` | `brotherhood-without-banners.node.md` | `- `SWORN_TO` ← Beric Dondarrion (founder and leader until ASOS epilogue)` |
| `brotherhood-without-banners` | `brotherhood-without-banners.node.md` | `- `SWORN_TO` ← Thoros of Myr (priest of R'hllor; repeatedly resurrects Beric)` |
| `brotherhood-without-banners` | `brotherhood-without-banners.node.md` | `- `SWORN_TO` ← Anguy (the Archer)` |
| `brotherhood-without-banners` | `brotherhood-without-banners.node.md` | `- `SWORN_TO` ← Lem Lemoncloak` |
| `brotherhood-without-banners` | `brotherhood-without-banners.node.md` | `- `SWORN_TO` ← Beardless Dick` |

---

## Summary

Of 21087 edges across 7720 nodes, 19055 resolve cleanly. 2004 are orphan or stale, dominated by Cat 1 (1673 edges, 814 unique slugs). Date-bleed status: 42 stragglers remain. Religion-bleed leftovers: 0. Title-like targets are a structural gap: 22 title slugs referenced by 49 edges with no node. Cat 2 alias-mismatches (289 edges) are not gaps — they're handled the moment the graph layer consults `working/wiki/data/alias-resolver.json` after a direct-slug miss.

## Recommended actions

Prioritized:

1. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers are the only category where data is actively wrong. Sources: .

2. **HIGH — Re-emit the 42 date-bleed BORN_AT/DIED_AT nodes.** 40 unique source nodes affected. Sample: alys-stackspear, alyssa-blackwood, amarei-crakehall, annara-farring, bethany-rosby, cassana-estermont, corenna-swann, cyrenna-swann, denys-swann, dorna-swyft ….

3. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing targets into Tier 3 recovery. See Cat 1 table.

4. **MED — Wire alias-resolver into the graph query layer.** All 289 Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. Avoids touching 35 source nodes.

5. **MED — Stand up a Title Pass.** Promote the top 22 title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, ser, prince, princess, king, queen, etc.) to actual `title` nodes.

6. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit after Pass 1 chapter extractions add their own missing-target signal.

7. **LOW — Run schema-drift-auditor** on the 4 non-locked edge types observed.
