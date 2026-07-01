# Infobox-Merge Dry-Run Report — 2026-06-12

> Generated: 2026-07-01T16:30:58.025745+00:00  
> Run ID: `infobox-merge-20260701`  
> RNG seed for 20-edge sample: `42`

## 1. Disposition Counts vs Spec v2

| Bucket | Expected | Actual | Status |
|---|---|---|---|
| rows_in (total input) | 20614 | 20614 | PASS |
| MERGED | 17006 | 0 | FAIL |
| Filtered: source unresolved (R1) | 3 | 3 | PASS |
| Filtered: noise placeholder (R2a) | 412 | 412 | PASS |
| Filtered: noise bare-kinship (R2b) | 204 | 204 | PASS |
| Filtered: noise numeral/date (R2c) | 0 | 0 | PASS |
| Filtered: target unresolved (R4) | 507 | 477 | FAIL |
| Filtered: self-loop (R8) | 2 | 0 | FAIL |
| **Filtered total** | 1128 | 1096 | FAIL |
| Quarantined: plural Mothers/Fathers (R3a) | 46 | 46 | PASS |
| Quarantined: multi-value singular father/mother (R3b) | 8 | 8 | PASS |
| Quarantined: speculative qualifier (R3c) | 102 | 102 | PASS |
| Quarantined: disputed on non-PARENT_OF kinship (R3d) | 5 | 5 | PASS |
| Quarantined: mirror of quarantined fact (R3e) | 24 | 25 | FAIL |
| Quarantined: kinship endpoint contract (R6a) | 73 | 73 | PASS |
| Quarantined: HOLDS_TITLE target contract (R6b) | 464 | 466 | FAIL |
| Quarantined: Result-field DEFEATS (R6c) | 315 | 315 | PASS |
| **Quarantined total** | 1037 | 1040 | FAIL |
| Quarantined: dedupe qualifier conflict (R9q) | 0 | 0 | PASS |
| Deduped within run (R9, incl. 3 preferred swaps) | 1356 | 1628 | FAIL |
|   └─ qualified-row-preferred swaps (sub-count) | 3 | 0 | FAIL |
| Skipped, corroborates existing (R10) | 87 | 16850 | FAIL |
| **Sum check (must equal rows_in)** | 20614 | 20614 | PASS |

## 2. Merged Edges by Type (all 22)

| Type | Expected | Actual | Status |
|---|---|---|---|
| SWORN_TO | 4064 | 0 | FAIL |
| HOLDS_TITLE | 3401 | 0 | FAIL |
| CULTURE_OF | 3252 | 0 | FAIL |
| PARENT_OF | 1645 | 0 | FAIL |
| DIED_AT | 915 | 0 | FAIL |
| BORN_AT | 833 | 0 | FAIL |
| REGION_OF | 573 | 0 | FAIL |
| OVERLORD_OF | 551 | 0 | FAIL |
| SEAT_OF | 329 | 0 | FAIL |
| SPOUSE_OF | 313 | 0 | FAIL |
| RULES | 264 | 0 | FAIL |
| PART_OF | 184 | 0 | FAIL |
| HEIR_TO | 179 | 0 | FAIL |
| RELIGION_OF | 93 | 0 | FAIL |
| SUCCEEDS | 93 | 0 | FAIL |
| OWNS | 84 | 0 | FAIL |
| FOUNDED | 71 | 0 | FAIL |
| LOVER_OF | 71 | 0 | FAIL |
| BURIED_AT | 48 | 0 | FAIL |
| CADET_BRANCH_OF | 26 | 0 | FAIL |
| ANCESTRAL_WEAPON_OF | 13 | 0 | FAIL |
| FIGHTS_IN | 4 | 0 | FAIL |

## 3. Hygiene Fix A — Orphan Endpoint Remaps

**115 orphan endpoint slugs, 140 affected rows** (recomputed from edges.jsonl).

| Resolution | Slugs | Rows | Action |
|---|---|---|---|
| Alias-resolver remap | 0 | 0 | rewrite slug in place |
| Leading `the-` strip | 0 | 0 | rewrite slug in place |
| Honorific-prefix strip | 0 | 0 | rewrite slug in place (characters-only guard) |
| Unresolvable | 62 | 67 | leave as-is, logged below |

**Post-remap duplicates created: 0** — no new collision introduced by remaps.

### 3a. Semantic Remaps — Require Matt Review

These two remaps collapse an in-story *persona* onto the underlying person. They follow established project conventions (alias-resolver already canonicalizes them, impersonation-edges rule applies), but persona-collapse is a judgment call. The default can be overridden before `--apply`.

- **`lady-stoneheart` → `catelyn-stark`** (0 row(s) affected)
- **`abel` → `mance-rayder`** (0 row(s) affected)

### 3b. Honorific-Strip Remaps (26 slugs / 33 rows, characters-only)

The `maester-griffins-roost → griffins-roost` case is correctly **rejected** (griffins-roost is a location, not a character).


### 3c. Unresolvable Orphans (stay as-is)

- `harrenhal-dungeon-guards` (2 rows)
- `freedmen` (2 rows)
- `wat-the-blue-bard` (2 rows)
- `big-walder-frey` (2 rows)
- `little-walder-frey` (2 rows)
- `nights-watch-deserter` (1 rows)
- `brans-direwolf` (1 rows)
- `catspaw-assassin` (1 rows)
- `the-red-stallion` (1 rows)
- `bronze-knife` (1 rows)
- `gold-cloaks` (1 rows)
- `mountain-clansmen` (1 rows)
- `lord-brax` (1 rows)
- `one-armed-woman` (1 rows)
- `unnamed-soldier` (1 rows)
- `unnamed-toddler` (1 rows)
- `unnamed-mother` (1 rows)
- `spiked-mace` (1 rows)
- `defiant-knight` (1 rows)
- `kenned` (1 rows)
- `caged-northmen` (1 rows)
- `prisoner-fat-man` (1 rows)
- `prisoner-bearded-man` (1 rows)
- `prisoner-old-man` (1 rows)
- `rooftop-sentinel` (1 rows)
- `kyle` (1 rows)
- `septry-door-guards` (1 rows)
- `old-grazdan` (1 rows)
- `bear-harrenhal` (1 rows)
- `old-man-captive` (1 rows)
- `orell-s-eagle` (1 rows)
- `unnamed-thenn-direwolf-victim` (1 rows)
- `sleeping-guards` (1 rows)
- `the-faith` (1 rows)
- `ser-osfryd` (1 rows)
- `victarion-salt-wife` (1 rows)
- `unknown-rose-banner-defender-1` (1 rows)
- `unknown-rose-banner-defender-2` (1 rows)
- `unknown-rose-banner-defender-3` (1 rows)
- `unknown-rose-banner-spearman` (1 rows)
- `vision-white-haired-woman` (1 rows)
- `vision-bearded-man` (1 rows)
- `vision-captive` (1 rows)
- `bronze-sickle` (1 rows)
- `unnamed-spearman` (1 rows)
- `pit-spearmen` (1 rows)
- `pitmaster` (1 rows)
- `basilisk-serjeant` (1 rows)
- `house-yunkai` (1 rows)
- `hizdahrs-sister` (1 rows)
- `maester-griffins-roost` (1 rows)
- `raymund` (1 rows)
- `alynne` (1 rows)
- `lord-stout` (1 rows)
- `lord-locke` (1 rows)
- `myrish-cog-dove-crew` (1 rows)
- `tolosi-slingers` (1 rows)
- `three-escaped-slaves` (1 rows)
- `ghiscari-galleys` (1 rows)
- `yunkai-slavers` (1 rows)
- `slaver-crew-willing-maiden` (1 rows)
- `perfumed-boys-willing-maiden` (1 rows)

## 4. Hygiene Fix B — `typed_by` Backfill (948 rows)

| Population | Count | typed_by assigned |
|---|---|---|
| `evidence_kind: book-pass1-reified` | 897 | `plate3-reifier` |
| `evidence_kind: plate4-wiki-cluster` | 51 | `plate4-cluster-classifier` |
| **Total** | **948** | — |

Chapter-label → file synthesis: 0 resolved, 0 unresolvable (empty label + non-POV-pattern chapters).
Plate-4 stale `stage` field dropped: 0 rows.

## 5. Rule 9 Qualifier-Conflict Quarantine (R9q)

Expected: 0. Actual: 0.

## 6. Parser-Artifact Qualifier Log (Rule 11)

Rows with raw qualifier matching artifact patterns (`^(ren|s)$` or date-range shape):

- `Aegon III Targaryen` · `Heirs` · `Baela Targaryen` [HEIR_TO] qual=`131–134 AC` → merged (date-range in wiki_qualifier)
- `Aegon III Targaryen` · `Heirs` · `Viserys Targaryen` [HEIR_TO] qual=`134–143 AC` → merged (date-range in wiki_qualifier)
- `Aegon III Targaryen` · `Heirs` · `Daeron Targaryen` [HEIR_TO] qual=`143–157 AC` → merged (date-range in wiki_qualifier)
- `Aegon II Targaryen` · `Heirs` · `Maelor Targaryen` [HEIR_TO] qual=`129–130 AC` → merged (date-range in wiki_qualifier)
- `Aegon II Targaryen` · `Heirs` · `Aegon Targaryen` [HEIR_TO] qual=`130–131 AC` → merged (date-range in wiki_qualifier)
- `Aerys II Targaryen` · `Heirs` · `Rhaegar Targaryen` [HEIR_TO] qual=`262–283 AC` → merged (date-range in wiki_qualifier)
- `Benjen Stark (son of Artos)` · `Issue` · `Child` [PARENT_OF] qual=`ren` → noise-bare-kinship
- `Brogg` · `Issue` · `Son` [PARENT_OF] qual=`s` → noise-bare-kinship
- `Daeron II Targaryen` · `Heirs` · `Baelor Targaryen` [HEIR_TO] qual=`184–209 AC` → merged (date-range in wiki_qualifier)
- `Daeron II Targaryen` · `Heirs` · `Valarr Targaryen` [HEIR_TO] qual=`209–209 AC` → merged (date-range in wiki_qualifier)
- `Hugh Arryn` · `Issue` · `Son` [PARENT_OF] qual=`s` → noise-bare-kinship
- `Osric Umber` · `Issue` · `Child` [PARENT_OF] qual=`ren` → noise-bare-kinship
- `Robard Cerwyn` · `Issue` · `Child` [PARENT_OF] qual=`ren` → noise-bare-kinship
- `Robert I Baratheon` · `Heirs` · `Joffrey Baratheon` [HEIR_TO] qual=`286–298 AC` → merged (date-range in wiki_qualifier)

## 7. Random 20-Edge Sample (seed=42)

| # | edge_type | source → target | field | qualifier | direction_corrected |
|---|---|---|---|---|---|

## 8. YOUR-DECISIONS — Open Questions (11 items, spec §8)

The spec identified 11 open questions. Decided-by-default values listed here for Matt to override line by line.

**Q1: FIELD_EDGE_MAP direction inversions (10 fields)**
> Decided-by-default: Recommend: yes, fix FIELD_EDGE_MAP + architecture.md in the --apply session (CLAUDE.md rule 6: schema and architecture.md must not stay contradictory).

**Q2: Tier-1 qualifier defaults (HOLDS_TITLE/SWORN_TO/SPOUSE_OF: `unknown`; PARENT_OF: `biological`)**
> Decided-by-default: Default shipped. Alternative: `current` for the first three. Change before --apply if preferred.

**Q3: Quarantined ship-captaincy HOLDS_TITLE→artifact rows (43 of 464)**
> Decided-by-default: Default: quarantined. Future: retype to CAPTAIN_OF in a small follow-up pass.

**Q4: CULTURE_OF region-name targets (927 rows, person → location)**
> Decided-by-default: Default: merged as-is. Future: mint reachmen/crownlanders culture nodes.

**Q5: Result-field DEFEATS class (315 rows, R6c)**
> Decided-by-default: Default: quarantined wholesale. Future: curator pass for victor-extraction.

**Q6: `the-` strip overrides alias_collisions 'ambiguous-do-not-resolve' for single-candidate variants**
> Decided-by-default: Default: the-strip wins (exact-match only, 89 target rows + 4 orphan rows depend on it).

**Q7: Honorific-strip rung in Fix A (26 slugs / 33 rows, characters-only guard)**
> Decided-by-default: Default: included. Reject: restrict Fix A to pure alias remaps (23/35). Character-category guard prevents maester-griffins-roost false positive.

**Q8: Corroboration handling (87 rows)**
> Decided-by-default: Default: log-only. Future: stamp `corroborated_by: wiki-infobox` on matching Tier-1 edges at apply time.

**Q9: Fact-key mirror quarantine (Rule 3e, 24 rows)**
> Decided-by-default: Default: quarantine (conservative). Override per-fact from quarantined.jsonl.

**Q10: Dedupe-conflict policy (R9q — currently 0 rows)**
> Decided-by-default: Default: qualified row beats unqualified (3 swaps); two different qualifiers quarantine. Alt: union qualifiers and merge anyway.

**Q11: `evidence_book`/`evidence_chapter` emitted as explicit nulls**
> Decided-by-default: Default: null (page-level cite_refs are false precision at row level). Alt: derive from cite_refs where page cites exactly one chapter — rejected for v2.
