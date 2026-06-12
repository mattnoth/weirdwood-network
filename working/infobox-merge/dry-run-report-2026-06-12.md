# Infobox-Merge Dry-Run Report — 2026-06-12

> Generated: 2026-06-12T20:51:40.837088+00:00  
> Run ID: `infobox-merge-20260612`  
> RNG seed for 20-edge sample: `42`

---

## What this is (read this first)

This is the rehearsal output of `scripts/infobox-merge.py --dry-run`. **Nothing has been
written to the graph** — every number below describes what *would* happen when the script
runs with `--apply`.

What the merge does, in two sentences: it promotes the wiki's structured infobox
relationships — parents, spouses, sworn houses, titles, seats, birthplaces — from the
parsed wiki layer (`working/wiki/data/infobox-data.jsonl`, sitting finished on disk since
April) into the canonical edge file `graph/edges/edges.jsonl`, as clearly-labeled
second-tier wiki edges. That adds 17,006 edges to the existing 4,760, roughly tripling
graph connectivity (nodes with at least one edge go from 14.7% to 71%).

**What you need to do:** read the TL;DR below → skim the count tables (every line should
say PASS) → answer or accept the 11 decisions in section 8 → then the ship continue prompt
runs `--apply`. The merge does not ship until you've signed off on this report.

---

## TL;DR

**Headline: every expected count matched the spec exactly.** The spec (v2) predicted every
number before the script was written; the script reproduced all of them:

| Bucket | Count | Meaning |
|---|---|---|
| MERGED | 17,006 | rows that become new edges |
| FILTERED | 1,128 | mechanical noise (placeholders, unresolvable names) — logged, not promoted |
| QUARANTINED | 1,037 | real signal the graph must not assert (rumors, contract violations) — preserved for later curation |
| DEDUPED | 1,356 | the wiki saying the same fact twice (once from each page) — collapsed to one edge |
| CORROBORATIONS | 87 | wiki rows that restate an existing Tier-1 book edge — skipped, logged |

Sum = 20,614 = every input row accounted for. Nothing was silently dropped.

**The three things most worth your eyeballs:**

1. **The 2 semantic remaps (§3a).** `lady-stoneheart → catelyn-stark` and
   `abel → mance-rayder` collapse an in-story persona onto the underlying person. They
   follow established project conventions, but they change *who an edge is about*, so they
   get a human glance before apply.
2. **The quarantine protections fired.** The R3a count (46) includes Jon Snow's two
   "Mothers" rows (Wylla *supposedly*, Ashara Dayne *rumored*) — without quarantine the
   graph would canonize R+L=J's biggest red herrings as Tier-2 facts. The R3e count (24)
   includes Robert's and Jaime's `Issue` mirror rows for the Lannister-incest children —
   without fact-key closure, Robert's own page would have made Joffrey his *biological*
   son. Both protections worked.
3. **Decisions you might plausibly override:** Q2 (should unqualified titles/allegiances
   default to `unknown` or `current`?), Q3 (43 real ship-captaincies sit in quarantine —
   accept, or queue a retype?), Q9 (24 individually-clean mirror rows suppressed
   conservatively — override per-fact if you want any back).

---

## Field glossary — terms used throughout this report

One entry per term, plain English, with a real example from this run's data.

- **`direction_corrected`** — The parser's FIELD_EDGE_MAP had 10 infobox fields backwards:
  "Acorn Hall · Ruler · Theomar Smallwood" would have minted `acorn-hall RULES
  theomar-smallwood` — the castle ruling the man. The script flips these 10 fields at
  promotion (Ruler, Heir, Successor, Predecessor, Founder, Owner, Head, Cadet branches,
  and plurals) and stamps `direction_corrected: true` on each flipped edge, so every
  corrected edge is findable later. The bug was invisible until now because the only
  prior consumer rendered rows page-relatively without materializing endpoints.

- **`evidence_kind: wiki-infobox`** — Stamped on every merged edge. Says where the claim
  comes from: the structured fact-table in the top-right corner of a wiki article, not a
  book quote and not wiki prose. Lets any consumer (or you) filter this entire layer in
  or out with one field. Example: `walder-frey PARENT_OF roslin-frey` carries it.

- **`typed_by: python-infobox-map`** — Stamped on every merged edge. Says *how the edge
  got its type*: a deterministic Python dict mapping infobox field names to edge types
  (`Allegiance` → SWORN_TO, `Seat` → SEAT_OF), not an LLM's judgment. Distinguishes these
  edges from LLM-typed ones (e.g. Stage 4's classifier output).

- **`confidence_tier: 2`** — Every merged edge is Tier 2, hard ceiling, no exceptions.
  Tier 1 is earned by a verbatim book quote, and an infobox row has no quote — so even
  obviously-true facts (`eddard-stark SPOUSE_OF catelyn-tully`) cap at Tier 2 when sourced
  from the wiki. This is what keeps the wiki layer honest next to the book layer.

- **`cite: wiki:<Page>`** — Each merged edge cites the wiki page it came from, e.g.
  `wiki:Walder_Frey`. Page-level only: the parser stripped per-row citation markers, so
  chapter-level anchors don't exist at row granularity (see decision Q11).

- **`wiki_qualifier`** — The raw qualifier string from the infobox, preserved verbatim
  (`"formerly"`, `"salt wife"`, `"155 AC"`). Separate from the validated `qualifier` enum
  field, which only enum-bearing edge types get. Nothing the wiki said is thrown away —
  sample edge #11 below keeps `155 AC` here.

- **Fact key (and mirror rows)** — The wiki states most kinship twice, once from each
  page: Joffrey's page says `Fathers: Robert (legally) / Jaime (biologically)`; Robert's
  page says `Issue: Joffrey`. A *fact key* is the underlying claim — (relation class,
  the two people) — regardless of which page carries the row. Quarantining one side must
  quarantine both (rule R3e), or Joffrey becomes Robert's biological son via Robert's own
  page. 24 such mirror rows quarantine in this run.

- **Corroboration** — A wiki row asserting something a Tier-1 book edge already says,
  e.g. `arianne-martell` · father · `doran-martell`, already in canon from Pass 1. The
  book edge owns the fact; the wiki agreeing is confirmation, not a second edge. These 87
  rows are skipped and logged to `corroborations.jsonl` (see decision Q8).

- **In-run dedupe** — The wiki's bidirectional encoding collapsing correctly: Eddard's
  page lists `Spouse: Catelyn Tully` and Catelyn's lists `Spouse: Eddard Stark` — one
  marriage, one edge. 1,356 rows collapse this way. Dedupe is qualifier-aware: a
  qualified row beats an unqualified twin (3 such swaps this run).

- **Hygiene fix A** — A side repair to the *existing* edge file: 115 endpoint slugs in
  current edges point at no node file (e.g. `ned-stark` where the node is
  `eddard-stark`). Fix A rewrites the resolvable ones in place via the alias resolver;
  140 rows affected. Section 3.

- **Hygiene fix B** — A second side repair: 948 existing edges (from the Plate-3/Plate-4
  reification work) are missing their `typed_by` stamp. Fix B backfills it and normalizes
  their citation shape. Section 4.

- **Semantic remap** — A remap that changes WHO the edge is about, not just the spelling:
  `lady-stoneheart → catelyn-stark`, `abel → mance-rayder`. Both follow the project's
  impersonation/alias conventions (attach identity-fraud edges to the actual actor), but
  persona-collapse is a judgment call, not a spelling fix — so they're flagged for your
  glance in §3a rather than buried in the alias list.

### Rule codes used in the tables

| Code | Plain name |
|---|---|
| R1 | Source page isn't a node — filter |
| R2a | Placeholder target ("None", "Unknown") — filter |
| R2b | Bare kinship word target ("Son", "Two daughters") — filter |
| R2c | Pure numeral/date target — filter (defensive; 0 today) |
| R3a | Plural Mothers/Fathers field = competing claims — quarantine |
| R3b | Two values in a singular Father/Mother field = the wiki hedging — quarantine |
| R3c | Speculative qualifier on kinship ("rumored", "allegedly", "legally") — quarantine |
| R3d | "disputed" on a kinship type that can't carry the flag — quarantine |
| R3e | Mirror of a quarantined fact (fact-key closure) — quarantine |
| R4 | Target string resolves to no node — filter |
| R5 | Deterministic retypes (battle→war PART_OF; location WORSHIPS→RELIGION_OF) |
| R6a | Kinship edge with a non-character endpoint — quarantine |
| R6b | HOLDS_TITLE target isn't a title node — quarantine |
| R6c | Result-field DEFEATS rows (never properly extracted) — quarantine |
| R7 | Direction conventions + the 10-field flip table (`direction_corrected`) |
| R8 | Self-loop (source == target) — filter |
| R9 | In-run dedupe (bidirectional encoding collapsing) |
| R9q | Dedupe found two *conflicting* qualifiers — quarantine the fact (0 today) |
| R10 | Row matches an existing book edge — skip, log as corroboration |
| R11 | Stamping: tier, provenance, qualifier normalization |

---

## 1. Disposition Counts vs Spec v2

*Every one of the 20,614 input rows ends in exactly one bucket; this table checks each
bucket's actual count against the count the spec predicted before the script existed. An
exact match on every line means the implementation does what the reviewed spec says — any
✗/FAIL would have halted the ship. The sum-check line at the bottom proves no row was
silently dropped.*

| Bucket | Expected | Actual | Status |
|---|---|---|---|
| rows_in (total input) | 20614 | 20614 | PASS |
| MERGED | 17006 | 17006 | PASS |
| Filtered: source unresolved (R1) | 3 | 3 | PASS |
| Filtered: noise placeholder (R2a) | 412 | 412 | PASS |
| Filtered: noise bare-kinship (R2b) | 204 | 204 | PASS |
| Filtered: noise numeral/date (R2c) | 0 | 0 | PASS |
| Filtered: target unresolved (R4) | 507 | 507 | PASS |
| Filtered: self-loop (R8) | 2 | 2 | PASS |
| **Filtered total** | 1128 | 1128 | PASS |
| Quarantined: plural Mothers/Fathers (R3a) | 46 | 46 | PASS |
| Quarantined: multi-value singular father/mother (R3b) | 8 | 8 | PASS |
| Quarantined: speculative qualifier (R3c) | 102 | 102 | PASS |
| Quarantined: disputed on non-PARENT_OF kinship (R3d) | 5 | 5 | PASS |
| Quarantined: mirror of quarantined fact (R3e) | 24 | 24 | PASS |
| Quarantined: kinship endpoint contract (R6a) | 73 | 73 | PASS |
| Quarantined: HOLDS_TITLE target contract (R6b) | 464 | 464 | PASS |
| Quarantined: Result-field DEFEATS (R6c) | 315 | 315 | PASS |
| **Quarantined total** | 1037 | 1037 | PASS |
| Quarantined: dedupe qualifier conflict (R9q) | 0 | 0 | PASS |
| Deduped within run (R9, incl. 3 preferred swaps) | 1356 | 1356 | PASS |
|   └─ qualified-row-preferred swaps (sub-count) | 3 | 3 | PASS |
| Skipped, corroborates existing (R10) | 87 | 87 | PASS |
| **Sum check (must equal rows_in)** | 20614 | 20614 | PASS |

Reading the buckets: **filtered** rows are mechanical noise with nothing to recover (a
target literally reading "None"); **quarantined** rows are real information the graph
must not assert as fact — they're preserved in full in `quarantined.jsonl` for a future
curator, never deleted. The R3a 46 includes Jon Snow's two "Mothers" rows; the R3e 24
includes the Robert/Jaime mirrors of the incest children (see TL;DR item 2).

## 2. Merged Edges by Type (all 22)

*Where the 17,006 new edges land, by edge type — again checked against the spec's
predictions. Good = all PASS, and the shape is what you'd expect from the wiki: lots of
allegiances, titles, and cultures (every character page has those fields), fewer of the
rare structural types. All 22 types are already in the locked master vocabulary; nothing
new was invented.*

| Type | Expected | Actual | Status |
|---|---|---|---|
| SWORN_TO | 4064 | 4064 | PASS |
| HOLDS_TITLE | 3401 | 3401 | PASS |
| CULTURE_OF | 3252 | 3252 | PASS |
| PARENT_OF | 1645 | 1645 | PASS |
| DIED_AT | 915 | 915 | PASS |
| BORN_AT | 833 | 833 | PASS |
| REGION_OF | 573 | 573 | PASS |
| OVERLORD_OF | 551 | 551 | PASS |
| SEAT_OF | 329 | 329 | PASS |
| SPOUSE_OF | 313 | 313 | PASS |
| RULES | 264 | 264 | PASS |
| PART_OF | 184 | 184 | PASS |
| HEIR_TO | 179 | 179 | PASS |
| RELIGION_OF | 93 | 93 | PASS |
| SUCCEEDS | 93 | 93 | PASS |
| OWNS | 84 | 84 | PASS |
| FOUNDED | 71 | 71 | PASS |
| LOVER_OF | 71 | 71 | PASS |
| BURIED_AT | 48 | 48 | PASS |
| CADET_BRANCH_OF | 26 | 26 | PASS |
| ANCESTRAL_WEAPON_OF | 13 | 13 | PASS |
| FIGHTS_IN | 4 | 4 | PASS |

Note: RULES, HEIR_TO, SUCCEEDS, FOUNDED, OWNS, and CADET_BRANCH_OF (717 edges total) are
the direction-flip types — every one of those edges carries `direction_corrected: true`
(see glossary). Without the flip, all 717 would point backwards.

## 3. Hygiene Fix A — Orphan Endpoint Remaps

*This section is about the EXISTING edge file, not the new wiki edges: 115 endpoint slugs
in current edges point at no node file (typos, aliases, minor entities that never got
nodes). Fix A rewrites the ones the alias machinery can resolve, in place, and leaves the
rest as-is, logged. Good = the remap counts below, and zero new duplicate edges created
by the rewrites.*

**115 orphan endpoint slugs, 140 affected rows** (recomputed from edges.jsonl).

| Resolution | Slugs | Rows | Action |
|---|---|---|---|
| Alias-resolver remap | 23 | 35 | rewrite slug in place |
| Leading `the-` strip | 3 | 4 | rewrite slug in place |
| Honorific-prefix strip | 26 | 33 | rewrite slug in place (characters-only guard) |
| Unresolvable | 63 | 68 | leave as-is, logged below |

**Post-remap duplicates created: 0** — no new collision introduced by remaps.

### 3a. Semantic Remaps — Require Matt Review

*The only two remaps in the whole fix that change WHO an edge is about rather than just
the spelling — flagged here so you see them before apply, per the spec's review
requirement. Both are already canonicalized this way by the alias resolver and both
follow the impersonation-edges rule (attach the edge to the actual person behind the
persona), but persona-collapse is a judgment call.*

These two remaps collapse an in-story *persona* onto the underlying person. They follow established project conventions (alias-resolver already canonicalizes them, impersonation-edges rule applies), but persona-collapse is a judgment call. The default can be overridden before `--apply`.

- **`lady-stoneheart` → `catelyn-stark`** (1 row(s) affected)
  - `COMMANDS_IN lady-stoneheart → merrett-attempts-to-defend-his-innocence-in-the-red-wedding` (extractions/mechanical/asos/asos-epilogue.extraction.md)
- **`abel` → `mance-rayder`** (1 row(s) affected)
  - `COMMANDS_IN abel → holly-kills-first-guard` (extractions/mechanical/adwd/adwd-theon-01.extraction.md)

### 3b. Honorific-Strip Remaps (26 slugs / 33 rows, characters-only)

*These strip a leading title (`ser-`, `lord-`, `maester-`, `khal-`...) and accept the
result only if it's an existing CHARACTER node — the category guard is what makes this
safe. Skim for anything that maps to the wrong person; the list is intentionally boring.
This rung is decision Q7 if you'd rather exclude it.*

The `maester-griffins-roost → griffins-roost` case is correctly **rejected** (griffins-roost is a location, not a character).

- `khal-drogo` → `drogo` (2 rows)
- `lord-beric-dondarrion` → `beric-dondarrion` (1 rows)
- `lord-wyman-manderly` → `wyman-manderly` (1 rows)
- `maester-kerwin` → `kerwin` (1 rows)
- `maester-luwin` → `luwin` (1 rows)
- `septa-scolera` → `scolera` (1 rows)
- `ser-aenys-frey` → `aenys-frey` (1 rows)
- `ser-alliser-thorne` → `alliser-thorne` (1 rows)
- `ser-amory-lorch` → `amory-lorch` (2 rows)
- `ser-boros-blount` → `boros-blount` (1 rows)
- `ser-corliss-penny` → `corliss-penny` (1 rows)
- `ser-dontos-hollard` → `dontos-hollard` (1 rows)
- `ser-garlan-tyrell` → `garlan-tyrell` (1 rows)
- `ser-godry-farring` → `godry-farring` (1 rows)
- `ser-gregor-clegane` → `gregor-clegane` (1 rows)
- `ser-imry-florent` → `imry-florent` (1 rows)
- `ser-jorah-mormont` → `jorah-mormont` (1 rows)
- `ser-lothor-brune` → `lothor-brune` (1 rows)
- `ser-mandon-moore` → `mandon-moore` (1 rows)
- `ser-meryn-trant` → `meryn-trant` (1 rows)
- `ser-rodrik-cassel` → `rodrik-cassel` (3 rows)
- `ser-ryman-frey` → `ryman-frey` (2 rows)
- `ser-tallad` → `tallad` (3 rows)
- `ser-vardis-egen` → `vardis-egen` (1 rows)
- `ser-wendel-manderly` → `wendel-manderly` (1 rows)
- `ser-willis-wode` → `willis-wode` (1 rows)

### 3c. Unresolvable Orphans (stay as-is)

*Slugs nothing in the alias machinery can map to an existing node — mostly Pass-1 minor
entities (`unnamed-soldier`, `rooftop-sentinel`) that never got node files. They are NOT
fixed and NOT deleted: the rows keep their current slugs, logged here. Minting nodes for
these is a separate backlog item, not this script's job. Nothing to approve — this list
is informational.*

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
- `siege-of-storm-s-end-recalled` (1 rows)
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

*Second repair to existing edges: 948 rows from the earlier reification work
(Plate 3/Plate 4) never got a `typed_by` stamp, so downstream consumers have to
special-case them. Fix B stamps each population with the name of the pipeline that typed
it (the convention names pipelines, not models) and normalizes their chapter-label
citations into file paths. Good = the two populations sum to 948 and nearly all chapter
labels resolve to real files.*

| Population | Count | typed_by assigned |
|---|---|---|
| `evidence_kind: book-pass1-reified` | 897 | `plate3-reifier` |
| `evidence_kind: plate4-wiki-cluster` | 51 | `plate4-cluster-classifier` |
| **Total** | **948** | — |

Chapter-label → file synthesis: 944 resolved, 2 unresolvable (empty label + non-POV-pattern chapters).
Plate-4 stale `stage` field dropped: 51 rows. *(These 51 rows still said "STAGED — DO NOT
promote" even though they were promoted long ago; the obsolete field is removed.)*

## 5. Rule 9 Qualifier-Conflict Quarantine (R9q)

*When dedupe finds the same fact stated twice with two DIFFERENT qualifiers (e.g. one
page says a marriage was "annulled", the other says "salt wife"), it can't pick a winner,
so it quarantines the whole fact. The spec predicted zero such conflicts in the current
data — every collision today is qualified-vs-blank, which the qualified row wins. Good =
0; the bucket exists for future data.*

Expected: 0. Actual: 0.

## 6. Parser-Artifact Qualifier Log (Rule 11)

*The April parser occasionally split a value badly, leaving debris in the qualifier slot:
the tails of "Child(ren)"/"Son(s)" (`ren`, `s`), and date ranges on Heirs fields. The
spec requires every such row to be listed here with its fate, so the debris is eyeballed
rather than silently carried. What you should see: the `ren`/`s` rows all die as
bare-kinship noise (their targets are words like "Child"), and the date-range rows merge
with the dates safely preserved in `wiki_qualifier` — heir-tenure ranges are real
information.*

Rows with raw qualifier matching artifact patterns (`^(ren|s)$` or date-range shape):

- `Aegon III Targaryen` · `Heirs` · `Baela Targaryen` [HEIR_TO] qual=`131–134 AC` → merged (date-range in wiki_qualifier)
- `Aegon III Targaryen` · `Heirs` · `Viserys Targaryen` [HEIR_TO] qual=`134–143 AC` → merged (date-range in wiki_qualifier)
- `Aegon III Targaryen` · `Heirs` · `Daeron Targaryen` [HEIR_TO] qual=`143–157 AC` → merged (date-range in wiki_qualifier)
- `Aegon II Targaryen` · `Heirs` · `Maelor Targaryen` [HEIR_TO] qual=`129–130 AC` → merged (date-range in wiki_qualifier)
- `Aegon II Targaryen` · `Heirs` · `Aegon Targaryen` [HEIR_TO] qual=`130–131 AC` → merged (date-range in wiki_qualifier)
- `Aerys II Targaryen` · `Heirs` · `Rhaegar Targaryen` [HEIR_TO] qual=`262–283 AC` → merged (date-range in wiki_qualifier)
- `Benjen Stark (son of Artos)` · `Issue` · `Child` [PARENT_OF] qual=`ren` → noise-bare-kinship
- `Brogg` · `Issue` · `Son` [PARENT_OF] qual=`s` → noise-bare-kinship
- `Daeron II Targaryen` · `Heirs` · `Baelor Targaryen` [HEIR_TO] qual=`184–209 AC` → merged (date-range in wiki_qualifier)
- `Daeron II Targaryen` · `Heirs` · `Valarr Targaryen` [HEIR_TO] qual=`209–209 AC` → merged (date-range in wiki_qualifier)
- `Hugh Arryn` · `Issue` · `Son` [PARENT_OF] qual=`s` → noise-bare-kinship
- `Osric Umber` · `Issue` · `Child` [PARENT_OF] qual=`ren` → noise-bare-kinship
- `Robard Cerwyn` · `Issue` · `Child` [PARENT_OF] qual=`ren` → noise-bare-kinship
- `Robert I Baratheon` · `Heirs` · `Joffrey Baratheon` [HEIR_TO] qual=`286–298 AC` → merged (date-range in wiki_qualifier)

## 7. Random 20-Edge Sample (seed=42)

*Twenty merged edges drawn at random (seeded, so re-runnable) for spot-checking — does
each one read as a true statement about the world? The Reading column is a plain-English
gloss of each edge. Note: by chance, none of the 20 drew a direction-flip type
(RULES/HEIR_TO/SUCCEEDS/FOUNDED/OWNS/CADET_BRANCH_OF), so every `direction_corrected`
here is False; the flip types total 717 of 17,006 edges. "unknown" qualifiers are the
Q2 default for rows where the wiki gave no qualifier.*

| # | edge_type | source → target | field | qualifier | direction_corrected | Reading |
|---|---|---|---|---|---|---|
| 1 | CULTURE_OF | `dannel` → `westeros` | Culture |  | False | Dannel's culture is recorded as "Westeros" — a region name standing in for a culture (the Q4 class) |
| 2 | SWORN_TO | `alyn-cockshaw` → `house-cockshaw` | Allegiances | unknown | False | Alyn Cockshaw is sworn to House Cockshaw (his own house — typical for the wiki's Allegiances field) |
| 3 | HOLDS_TITLE | `jasper-arryn` → `warden-of-the-east` | Titles | unknown | False | Jasper Arryn held the title Warden of the East |
| 4 | OVERLORD_OF | `house-baratheon-of-dragonstone` → `house-seaworth` | Overlord |  | False | House Baratheon of Dragonstone is overlord of House Seaworth (Davos's house) |
| 5 | SEAT_OF | `wolfs-den` → `house-greystark` | Seat |  | False | The Wolf's Den was the seat of House Greystark |
| 6 | HOLDS_TITLE | `ellendor` → `grand-maester` | Title | unknown | False | Ellendor held the title Grand Maester (a historical one) |
| 7 | CULTURE_OF | `daemon-targaryen` → `crownlands` | Culture |  | False | Daemon Targaryen's culture recorded as "Crownlands" — region-as-culture again (Q4) |
| 8 | BORN_AT | `charioteer` → `yunkai` | Born |  | False | The charioteer was born at Yunkai |
| 9 | SWORN_TO | `rhaenys-targaryen` → `house-targaryen` | Allegiance | unknown | False | Rhaenys Targaryen is sworn to House Targaryen |
| 10 | PARENT_OF | `alysanne-targaryen` → `valerion-targaryen` | Issue | biological | False | Alysanne Targaryen is parent of Valerion Targaryen — "biological" is the Q2 default for unqualified Issue rows |
| 11 | BORN_AT | `alysanne-daughter-of-aegon-iv` → `kings-landing` | Born | 155 AC | False | Alysanne (Aegon IV's daughter) was born at King's Landing in 155 AC — the date rides along in wiki_qualifier |
| 12 | HOLDS_TITLE | `corlys-velaryon` → `master-of-driftmark` | Titles | unknown | False | Corlys Velaryon held the title Master of Driftmark |
| 13 | REGION_OF | `house-foote-of-nightsong` → `stormlands` | Region |  | False | House Foote of Nightsong belongs to the Stormlands |
| 14 | SEAT_OF | `snakewood` → `house-lynderly` | Seat |  | False | Snakewood is the seat of House Lynderly |
| 15 | SWORN_TO | `walys-mooton` → `blacks` | Allegiances | unknown | False | Walys Mooton sided with the blacks (Rhaenyra's faction in the Dance of the Dragons) |
| 16 | SWORN_TO | `alyn-terrick` → `house-terrick` | Allegiances | unknown | False | Alyn Terrick is sworn to House Terrick |
| 17 | HOLDS_TITLE | `hosman-norcross` → `ser` | Title | unknown | False | Hosman Norcross holds the title Ser (a knighthood — "ser" is a real title node) |
| 18 | HOLDS_TITLE | `rhaella-targaryen` → `dowager-queen` | Titles | unknown | False | Rhaella Targaryen held the title Dowager Queen |
| 19 | REGION_OF | `house-garner` → `westerlands` | Region |  | False | House Garner belongs to the Westerlands |
| 20 | SWORN_TO | `samwell-rivers` → `house-tully` | Allegiance | unknown | False | Samwell Rivers is sworn to House Tully |

## 8. YOUR-DECISIONS — Open Questions (11 items, spec §8)

*The spec flagged 11 open questions. None block anything: every one has a
decided-by-default answer already baked into the dry-run numbers above. If you do nothing,
the defaults ship. Each item below: the question in one sentence → what the default does
concretely → what overriding would change → the recommendation. Mark your answer on each
line; the ship session reads this section.*

**1. Should the apply session also fix the parser's backwards direction map?**
- *If you do nothing:* the merge is unaffected either way (the script already corrects
  the 10 flipped fields at promotion — see `direction_corrected` in the glossary); the
  apply session additionally patches `FIELD_EDGE_MAP` in the parser and architecture.md's
  infobox table so code and docs stop contradicting each other. No re-parse needed.
- *If you override:* the parser and architecture.md keep the inverted directions; only
  future re-parses or doc readers would be misled.
- *Recommendation (unchanged):* yes, fix FIELD_EDGE_MAP + architecture.md in the --apply session (CLAUDE.md rule 6: schema and architecture.md must not stay contradictory).
- **Your answer:** [ ] accept default — [ ] override: ____________

**2. When the wiki gives no qualifier, what should the default qualifier be?**
- *If you do nothing:* unqualified HOLDS_TITLE/SWORN_TO/SPOUSE_OF rows ship as
  `unknown` (thousands of rows — see the sample, most rows above carry it) and
  unqualified PARENT_OF ships as `biological`.
- *If you override (alternative: `current` for the first three):* the graph would claim
  titles/allegiances/marriages are *currently held*, which over-claims for the wiki's
  many historical figures. Cheap to change before apply.
- *Recommendation (unchanged):* default shipped (`unknown`). Change before --apply if preferred.
- **Your answer:** [ ] accept default — [ ] override: ____________

**3. What to do with the 43 ship-captaincy rows caught by the title contract?**
- *If you do nothing:* rows like `aeron-greyjoy HOLDS_TITLE golden-storm` (a ship, i.e.
  an artifact, not a title) stay quarantined — real captaincies, wrong edge type.
- *If you override:* nothing changes in this run; the alternative is queuing a small
  follow-up pass that retypes them to a future `CAPTAIN_OF`.
- *Recommendation (unchanged):* default: quarantined. Future: retype to CAPTAIN_OF in a small follow-up pass.
- **Your answer:** [ ] accept default — [ ] override: ____________

**4. Accept 927 CULTURE_OF edges whose target is a region, not a culture node?**
- *If you do nothing:* rows where the wiki used a region name as the culture ("Reach",
  "Crownlands" — sample edges #1 and #7) merge with the location node as target:
  type-impure but information-preserving, and exactly what "which characters are from
  the Reach?" needs.
- *If you override:* hold those 927 rows out until `reachmen`/`crownlanders`-style
  culture nodes are minted and retargeted.
- *Recommendation (unchanged):* default: merged as-is. Future: mint reachmen/crownlanders culture nodes.
- **Your answer:** [ ] accept default — [ ] override: ____________

**5. Accept wholesale quarantine of the 315 Result-field DEFEATS rows?**
- *If you do nothing:* all 315 stay quarantined. The victor-extraction these rows needed
  was never implemented, so as parsed they say `<battle> DEFEATS <linked combatant>` —
  wrong direction AND wrong endpoints. Unsalvageable deterministically.
- *If you override:* nothing changes in this run; the alternative is queuing a curator
  pass that extracts the actual victor/defeated pairs from the result text.
- *Recommendation (unchanged):* default: quarantined wholesale. Future: curator pass for victor-extraction.
- **Your answer:** [ ] accept default — [ ] override: ____________

**6. Let the `the-` strip resolve names the alias file marks "ambiguous"?**
- *If you do nothing:* names like "The Citadel"/"The Wall" resolve by stripping the
  leading `the-` and requiring an exact node match — even where the alias file's
  collision list says "ambiguous-do-not-resolve" despite there being exactly one
  candidate. 89 target rows + 4 orphan rows depend on this rung.
- *If you override:* those 93 rows fall to unresolved (filtered / left orphaned).
- *Recommendation (unchanged):* default: the-strip wins (exact-match only, no fuzzy).
- **Your answer:** [ ] accept default — [ ] override: ____________

**7. Keep the honorific-strip rung in hygiene fix A?**
- *If you do nothing:* the 26 slugs / 33 rows in §3b (`ser-jorah-mormont` →
  `jorah-mormont` and kin) get repaired. The characters-only guard already blocked the
  one false positive (`maester-griffins-roost` → a location).
- *If you override:* Fix A restricts to pure alias remaps (23 slugs / 35 rows) and the
  26 honorific slugs stay orphaned.
- *Recommendation (unchanged):* default: included.
- **Your answer:** [ ] accept default — [ ] override: ____________

**8. Do anything with the 87 corroborations beyond logging them?**
- *If you do nothing:* the 87 wiki rows that restate an existing Tier-1 book edge are
  skipped and logged to `corroborations.jsonl`; the existing edges are untouched.
- *If you override:* apply time additionally stamps `corroborated_by: wiki-infobox` on
  the 87 matching Tier-1 edges — "the wiki agrees" recorded as metadata.
- *Recommendation (unchanged):* default: log-only. Future: stamp at apply time.
- **Your answer:** [ ] accept default — [ ] override: ____________

**9. Accept quarantining the 24 individually-clean mirror rows (fact-key closure)?**
- *If you do nothing:* the 24 R3e rows (see "fact key" in the glossary — e.g. Jaime's
  clean `Issue: Joffrey` row, mirror of Joffrey's contested Fathers field) stay
  quarantined. Conservative: quarantine ≠ delete; every row is in `quarantined.jsonl`
  with full context.
- *If you override:* you can promote individual facts back per-fact from
  `quarantined.jsonl` (e.g. decide Jaime's paternity should merge with a qualifier).
- *Recommendation (unchanged):* default: quarantine (conservative). Override per-fact from quarantined.jsonl.
- **Your answer:** [ ] accept default — [ ] override: ____________

**10. Accept the dedupe-conflict policy (qualified beats unqualified; conflicts quarantine)?**
- *If you do nothing:* when the same fact appears qualified on one page and unqualified
  on the other, the qualified row wins (3 such swaps this run — e.g. a marriage's
  `annulled` is kept rather than silently lost); two *different* qualifiers would
  quarantine the fact (R9q — 0 rows today, the policy exists for future data).
- *If you override (alternative):* union both qualifiers into `wiki_qualifier` and merge
  anyway, never quarantining on conflict.
- *Recommendation (unchanged):* default: qualified row beats unqualified; conflicting qualifiers quarantine.
- **Your answer:** [ ] accept default — [ ] override: ____________

**11. Emit `evidence_book`/`evidence_chapter` as explicit nulls?**
- *If you do nothing:* every merged edge carries both keys set to `null`. The keys exist
  on all 4,760 current canon rows, so consumers expect them; null is honest because the
  wiki's chapter citations only survive at page level (a page citing 70+ chapters tells
  you nothing about one row — false precision).
- *If you override (alternative, rejected for v2):* derive a chapter where a page cites
  exactly one — a special case that changes meaning per-row; revisit only if per-row
  citations are ever re-parsed from the infobox HTML.
- *Recommendation (unchanged):* default: null.
- **Your answer:** [ ] accept default — [ ] override: ____________

---

## 9. What happens next

1. You finish this report: confirm the count tables are all-PASS (they are), glance at
   §3a's two semantic remaps and the sample in §7, and mark your answer on each of the
   11 decisions above.
2. The ship continue prompt (in `progress/continue-prompts/`) runs
   `scripts/infobox-merge.py --apply`. **Gate:** apply re-runs the dry-run first and
   requires it to still match these numbers exactly — if the repo drifted, it halts
   instead of writing.
3. Apply then: backs up `graph/edges/edges.jsonl` to `_regrounding/`, applies hygiene
   fixes A and B in place, appends the 17,006 merged rows (4,760 → 21,766 total), and
   re-runs the validators (type contracts, qualifier enums, orphan check — zero new
   violations expected by construction).
4. Companion files in this directory if you want to drill into any bucket:
   `merged-candidate.jsonl` (the 17,006 exactly as they'd be appended),
   `quarantined.jsonl`, `filtered.jsonl`, `corroborations.jsonl`,
   `hygiene-a-remaps.jsonl`, `hygiene-b-stamps.jsonl`.
