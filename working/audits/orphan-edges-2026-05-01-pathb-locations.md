# Orphan Edges Audit — 2026-05-01-pathb-locations

**Nodes scanned:** 6060
**Total edges checked:** 19059
**Edges that resolve cleanly:** 16208
**Orphan / problematic edges found:** 2851

**Breakdown:**
- Category 1 (target genuinely missing): 2539 edges across 991 unique missing targets
- Category 2 (alias-mismatch — resolves via alias-resolver): 270 edges across 35 unique alias slugs
- Stale-data legacy (religion-bleed leftovers): 0
- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): 42
- Title-like missing targets (subset of Cat 1): 67 edges, 20 unique title slugs

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

**20 unique title slugs referenced; 67 total edge references.**

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
| `king-of-winter-king-in-the-north` | 1 | 0 |

---

## Category 1: target genuinely missing

Sorted by `in_count` desc, then by edge_count. Top 100 of 991 unique missing targets shown.

Severity: **HIGH** for top entries (high in_count → many references → recovery candidate). **LOW** for long-tail singletons.

| # | Target slug | Edges in graph | Cross-ref in_count | Title-like | Example source / edge_type / target text |
|---|---|---|---|---|---|
| 1 | `small-council` | 1 | 215 |  | `qyburn` / MEMBER_OF / Small council |
| 2 | `blacks` | 94 | 138 |  | `addam-velaryon` / SWORN_TO / Blacks |
| 3 | `greens` | 58 | 127 |  | `adrian-tarbeck` / SWORN_TO / Greens |
| 4 | `narrow-sea` | 1 | 120 |  | `assassination-of-tywin-lannister` / DEFEATS / narrow sea |
| 5 | `others` | 14 | 76 |  | `chett` / SWORN_TO / Others (track_b: Allegiances) |
| 6 | `unsullied` | 17 | 68 |  | `black-fist` / SWORN_TO / Unsullied |
| 7 | `house-manderly` | 24 | 61 |  | `bartimus` / SWORN_TO / House Manderly |
| 8 | `harren-hoare` | 3 | 56 |  | `halleck-hoare` / HEIR_TO / Harren Hoare |
| 9 | `haunted-forest` | 2 | 55 |  | `clubfoot-karl` / DIED_AT / Haunted forest (track_b: Died) |
| 10 | `house-blackwood` | 30 | 46 |  | `agnes-blackwood` / SWORN_TO / House Blackwood |
| 11 | `house-bracken` | 24 | 45 |  | `aegor-rivers` / SWORN_TO / House Bracken |
| 12 | `queens-men` | 18 | 43 |  | `alester-florent` / SWORN_TO / Queen's men |
| 13 | `crossroads-inn` | 1 | 39 |  | `wat-orphan` / SWORN_TO / Crossroads inn |
| 14 | `dothraki-sea` | 19 | 35 |  | `caggo` / BORN_AT / Dothraki Sea |
| 15 | `house-rogare` | 12 | 35 |  | `drako-rogare` / SWORN_TO / House Rogare |
| 16 | `khal` | 22 | 34 | yes | `bharbo` / HOLDS_TITLE / Khal |
| 17 | `house-darry` | 16 | 34 |  | `damon-darry` / SWORN_TO / House Darry |
| 18 | `century-of-blood` | 3 | 34 |  | `agnes-blackwood` / DIED_AT / Century of Blood |
| 19 | `house-florent` | 18 | 33 |  | `aladore-florent` / SWORN_TO / House Florent |
| 20 | `dragons` | 1 | 32 |  | `dance-of-the-dragons` / DEFEATS / dragons |
| 21 | `flea-bottom` | 5 | 30 |  | `clayton-suggs` / BORN_AT / Flea Bottom |
| 22 | `crypt-of-winterfell` | 14 | 29 |  | `barthogan-stark` / BURIED_AT / Crypt of Winterfell |
| 23 | `house-durrandon` | 5 | 29 |  | `argella-durrandon` / SWORN_TO / House Durrandon |
| 24 | `ruby-ford` | 1 | 29 |  | `rhaegar-targaryen` / DIED_AT / Ruby Ford (track_b: Died) |
| 25 | `rhoynar` | 11 | 28 |  | `druselka` / SWORN_TO / Rhoynar |
| 26 | `lords-declarant` | 7 | 27 |  | `anya-waynwood` / SWORN_TO / Lords Declarant |
| 27 | `house-cerwyn` | 6 | 27 |  | `argelle-stark` / SWORN_TO / House Cerwyn |
| 28 | `jeyne-arryn` | 4 | 27 |  | `arnold-arryn` / OPPOSES / Jeyne Arryn (wiki:Arnold_Arryn) |
| 29 | `silent-sisters` | 4 | 26 |  | `alysanne-osgrey` / SWORN_TO / Silent Sisters |
| 30 | `arlan-of-pennytree` | 1 | 26 |  | `chestnut` / OWNS / Arlan of Pennytree |
| 31 | `ship` | 1 | 26 |  | `quence` / SWORN_TO / Ship |
| 32 | `larys-strong` | 1 | 25 |  | `hour-of-the-wolf` / DEFEATS / Larys Strong |
| 33 | `house-gardener` | 10 | 24 |  | `alester-tyrell` / SWORN_TO / House Gardener |
| 34 | `stormcrows` | 7 | 24 |  | `daario-naharis` / SWORN_TO / Stormcrows |
| 35 | `house-of-black-and-white` | 2 | 24 |  | `umma` / SWORN_TO / House of Black and White |
| 36 | `299-ac` | 1 | 24 |  | `house-bolton` / OVERLORD_OF / 299 AC (track_b: Overlords) |
| 37 | `betrothal` | 1 | 24 |  | `lyonel-baratheons-rebellion` / DEFEATS / Betrothal |
| 38 | `house-hornwood` | 7 | 23 |  | `berena-hornwood` / SWORN_TO / House Hornwood |
| 39 | `house-dustin` | 6 | 23 |  | `barbrey-dustin` / SWORN_TO / House Dustin |
| 40 | `marwyn` | 1 | 23 |  | `qyburn` / RESPECTS / Marwyn |
| 41 | `joffrey-i-baratheon` | 2 | 22 |  | `robert-i-baratheon` / SUCCEEDS / Joffrey I Baratheon |
| 42 | `hugh-hammer` | 1 | 22 |  | `vermithor` / OWNS / Hugh Hammer |
| 43 | `vale` | 5 | 21 |  | `battle-in-the-waters-off-gulltown` / DEFEATS / Vale |
| 44 | `house-glover` | 13 | 19 |  | `benton-glover` / SWORN_TO / House Glover |
| 45 | `house-lothston` | 11 | 19 |  | `bastard-of-harrenhal` / SWORN_TO / House Lothston |
| 46 | `cinnamon-wind` | 2 | 19 |  | `aemon-targaryen-son-of-maekar-i` / DIED_AT / Cinnamon Wind |
| 47 | `wise-masters` | 15 | 18 |  | `beastmaster` / SWORN_TO / Wise Masters |
| 48 | `helaena-targaryen` | 5 | 18 |  | `alicent-hightower` / PARENT_OF / Helaena Targaryen |
| 49 | `tower-of-joy` | 1 | 18 |  | `roberts-rebellion` / FIGHTS_IN / Tower of joy |
| 50 | `andal-invasion` | 3 | 17 |  | `battle-of-the-seven-stars` / FIGHTS_IN / Andal invasion |
| 51 | `long-night` | 1 | 17 |  | `battle-for-the-dawn` / DEFEATS / Long Night |
| 52 | `lads` | 3 | 16 |  | `alysanne-blackwood` / SWORN_TO / Lads |
| 53 | `282-ac` | 1 | 16 |  | `house-baratheon` / OVERLORD_OF / 282 AC (track_b: Overlords) |
| 54 | `moon-of-the-three-kings` | 1 | 16 |  | `riot-of-kings-landing-dance-of-the-dragons` / DEFEATS / Moon of the Three Kings |
| 55 | `house-botley` | 14 | 15 |  | `balon-botley` / SWORN_TO / House Botley |
| 56 | `house-connington` | 12 | 15 |  | `alyn-connington` / SWORN_TO / House Connington |
| 57 | `300-ac` | 1 | 15 |  | `house-bolton` / OVERLORD_OF / 300 AC (track_b: Overlords) |
| 58 | `street-of-silk` | 1 | 15 |  | `jory-cassel` / DIED_AT / Street of Silk (track_b: Died) |
| 59 | `shepherd` | 1 | 14 |  | `barefoot-lambs` / SWORN_TO / Shepherd |
| 60 | `house-royce` | 26 | 13 |  | `alayne-royce` / SWORN_TO / House Royce |
| 61 | `battle-of-ashford` | 1 | 13 |  | `roberts-rebellion` / FIGHTS_IN / Battle of Ashford |
| 62 | `three-eyed-crow` | 1 | 13 |  | `coldhands` / SWORN_TO / Three-eyed crow |
| 63 | `bridge-of-skulls` | 3 | 12 |  | `aladale-wynch` / DIED_AT / Bridge of Skulls (track_b: Died) |
| 64 | `pirates` | 2 | 12 |  | `korra` / SWORN_TO / Pirates |
| 65 | `elephant` | 1 | 12 |  | `trianna` / SWORN_TO / Elephant |
| 66 | `house-harroway` | 6 | 11 |  | `alys-harroway` / SWORN_TO / House Harroway |
| 67 | `chatayas-brothel` | 5 | 11 |  | `alayaya` / SWORN_TO / Chataya's brothel |
| 68 | `good-masters` | 4 | 11 |  | `grazdan-fat-one` / SWORN_TO / Good Masters |
| 69 | `pureborn` | 3 | 11 |  | `egon-emeros` / SWORN_TO / Pureborn |
| 70 | `lyonel-strong` | 2 | 11 |  | `alys-rivers` / PARENT_OF / Lyonel Strong (track_b: Father) |
| 71 | `vulture-hunt` | 2 | 11 |  | `davos-baratheon` / FIGHTS_IN / Vulture Hunt |
| 72 | `dosh-khaleen` | 1 | 11 |  | `one-eyed-crone` / SWORN_TO / Dosh khaleen |
| 73 | `house-estermont` | 10 | 10 |  | `aemon-estermont` / SWORN_TO / House Estermont |
| 74 | `happy-port` | 5 | 10 |  | `assadora` / SWORN_TO / Happy Port |
| 75 | `kings-men` | 5 | 10 |  | `andrew-estermont` / SWORN_TO / King's men |
| 76 | `house-norrey` | 4 | 10 |  | `arra-norrey` / SWORN_TO / House Norrey |
| 77 | `submission-of-sunspear` | 1 | 10 |  | `conquest-of-dorne` / FIGHTS_IN / Submission of Sunspear |
| 78 | `house-farman` | 12 | 9 |  | `alysanne-farman` / SWORN_TO / House Farman |
| 79 | `house-crakehall` | 10 | 9 |  | `amarei-crakehall` / SWORN_TO / House Crakehall |
| 80 | `house-flint-of-the-mountains` | 3 | 9 |  | `artos-flint` / SWORN_TO / House Flint of the mountains |
| 81 | `king-s-landing` | 1 | 9 |  | `bramm-of-blackhull` / DIED_AT / King’s Landing (track_b: Died) |
| 82 | `kings-of-the-reach` | 1 | 9 |  | `order-of-the-green-hand` / SWORN_TO / Kings of the Reach |
| 83 | `house-harlaw` | 12 | 8 |  | `alannys-harlaw` / SWORN_TO / House Harlaw |
| 84 | `house-butterwell` | 11 | 8 |  | `alton-butterwell` / SWORN_TO / House Butterwell |
| 85 | `house-caswell` | 9 | 8 |  | `armond-caswell` / SWORN_TO / House Caswell |
| 86 | `house-morrigen` | 7 | 8 |  | `damon-morrigen` / SWORN_TO / House Morrigen |
| 87 | `tommen-i-baratheon` | 6 | 8 |  | `boots` / OWNS / Tommen I Baratheon |
| 88 | `house-lannister-of-lannisport` | 5 | 8 |  | `ella-lannister` / SWORN_TO / House Lannister of Lannisport |
| 89 | `house-goodbrook` | 4 | 8 |  | `garse-goodbrook` / SWORN_TO / House Goodbrook |
| 90 | `battle-of-the-red-fork` | 1 | 8 |  | `daven-lannister` / FIGHTS_IN / Battle of the Red Fork |
| 91 | `frozen-shore` | 1 | 8 |  | `great-walrus` / BORN_AT / Frozen Shore |
| 92 | `gate-of-the-gods` | 1 | 8 |  | `lucas-leygood` / DIED_AT / Gate of the Gods (track_b: Died) |
| 93 | `house-casterly` | 1 | 8 |  | `corlos` / SWORN_TO / House Casterly |
| 94 | `luthor-largent` | 1 | 8 |  | `house-largent` / FOUNDED / Luthor Largent |
| 95 | `the-gate` | 1 | 8 |  | `izembaro` / SWORN_TO / The Gate |
| 96 | `undying-ones` | 1 | 8 |  | `pyat-pree` / SWORN_TO / Undying Ones |
| 97 | `stone-crows` | 10 | 7 |  | `conn` / SWORN_TO / Stone Crows |
| 98 | `house-costayne` | 9 | 7 |  | `aemon-costayne` / SWORN_TO / House Costayne |
| 99 | `house-drumm` | 9 | 7 |  | `andrik-the-unsmiling` / SWORN_TO / House Drumm |
| 100 | `house-dondarrion` | 8 | 7 |  | `bastard-of-blackhaven` / SWORN_TO / House Dondarrion |

_(Long tail: 891 additional missing targets. See `working/audits/orphan-edges-2026-05-01-pathb-locations-cat1-full.tsv` for the complete list.)_

---

## Category 2: alias-mismatch (resolvable via alias-resolver)

These targets fail direct slug-match but DO resolve via the alias-resolver. **270 edges across 35 unique alias slugs** are affected.

Severity: **MED** — slug-format-drift, not a graph gap. Recommend the graph layer consult the alias-resolver after a direct-slug miss.

Top 50 by edge count:

| Target slug attempted | Resolves to canonical | Edges affected | Example |
|---|---|---|---|
| `stormlander` | `stormlanders` | 116 | `aelinor-penrose` / CULTURE_OF / Stormlander |
| `andal` | `andals` | 55 | `alester-ii-arryn` / CULTURE_OF / Andal |
| `lysene` | `lyseni` | 24 | `bambarro-bazanne` / CULTURE_OF / Lysene |
| `dornish` | `dornishmen` | 15 | `alleras` / CULTURE_OF / Dornish (track_b: Race) |
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
| `king-of-the-giants` | `mag-mar-tun-doh-weg` | 1 | `lun-the-last` / HOLDS_TITLE / King of the Giants |

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

Of 19059 edges across 6060 nodes, 16208 resolve cleanly. 2851 are orphan or stale, dominated by Cat 1 (2539 edges, 991 unique slugs). Date-bleed status: 42 stragglers remain. Religion-bleed leftovers: 0. Title-like targets are a structural gap: 20 title slugs referenced by 67 edges with no node. Cat 2 alias-mismatches (270 edges) are not gaps — they're handled the moment the graph layer consults `working/wiki-parsed/alias-resolver.json` after a direct-slug miss.

## Recommended actions

Prioritized:

1. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers are the only category where data is actively wrong. Sources: .

2. **HIGH — Re-emit the 42 date-bleed BORN_AT/DIED_AT nodes.** 40 unique source nodes affected. Sample: alys-stackspear, alyssa-blackwood, amarei-crakehall, annara-farring, bethany-rosby, cassana-estermont, corenna-swann, cyrenna-swann, denys-swann, dorna-swyft ….

3. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing targets into Tier 3 recovery. See Cat 1 table.

4. **MED — Wire alias-resolver into the graph query layer.** All 270 Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. Avoids touching 35 source nodes.

5. **MED — Stand up a Title Pass.** Promote the top 20 title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, ser, prince, princess, king, queen, etc.) to actual `title` nodes.

6. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit after Pass 1 chapter extractions add their own missing-target signal.

7. **LOW — Run schema-drift-auditor** on the 0 non-locked edge types observed.
