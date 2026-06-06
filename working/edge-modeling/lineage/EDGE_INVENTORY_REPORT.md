# Edge & Event-Modeling Inventory — asoiaf-chat (Weirwood Network)

_Generated 2026-06-04 · commit `f04dbc8a2` · read-only inventory_

> **Audience:** an external collaborator with no repo access who is analyzing a specific modeling tension: **true-binary** relationships (PARENT_OF — 2 fixed-role participants) vs. **n-ary events** (ATTACKS — agent, patient, location, instrument, instigator-vs-executor, outcome…) that have been flattened to a single `source → target` edge. Different rows can nominate different "subjects" for the same underlying event; the result looks like inconsistency but is actually **underdetermination born at the extraction layer**. Every body claim carries a `path:line` citation. Appendices A/B/C hold the full verbatim material.

---

## Executive Summary

1. **Storage is plain files, not a graph DB.** Nodes are YAML-frontmatter Markdown (`graph/nodes/{type-dir}/{slug}.node.md`, ~8,052 files). Edges are a single JSON Lines file (`graph/edges/edges.jsonl`, 3,811 typed rows, v1.3). Indexes are JSON-per-entity (`graph/index/{type-dir}/{slug}.index.json`, 7,635 files). No Neo4j, no RDF, no SQLite, no `requirements.txt`/`pyproject.toml` — only the stdlib + one `cloudscraper` script. (`structure.md` §3, `graph/edges/edges.jsonl:1`, `CLAUDE.md:71-127`).
2. **Edge vocabulary is locked at ~163 types across 15 categories**, defined verbatim in `reference/architecture.md:130-399`. By the brief's binary-vs-event test, **~76 are true-binary**, **~82 are event-like**, with a handful ambiguous. The schema **already partially reifies events into clusters of binary edges** — KILLS + KILLED_BY + KILLED_WITH + EXECUTED_WITH + DIED_AT + LOCATED_AT decompose a single killing event across 5 edge types (`architecture.md:216-217, 229, 286, 306`). Captivity is similarly split across IMPRISONS / PRISONER_OF / IMPRISONED_AT / RANSOMS / PRISONER_EXCHANGE_FOR.
3. **`CONSPIRES_WITH` is the only edge type whose description literally says "two or more parties"** (`architecture.md:207`). It is still emitted as a symmetric pair-wise edge. No edge type in the vocabulary has more than 2 participant slots.
4. **NO canonical head-selection rule exists in the Pass 1 extractor prompt.** The Pass-1 `## Relationships Observed` table is `| Character A | Relationship | Character B | Evidence |` (`.claude/agents/mechanical-extractor.md:176-178`). The prompt never tells the model how to pick A vs. B for n-ary events. Every downstream pipeline locks direction by column position. This is the **upstream root cause** of head-selection variance (`pipeline.md` §4.1).
5. **The Stage-4 classifier is told it CANNOT swap endpoints** — only type or reject. Rule 5: *"Direction is FIXED: edge runs source → target (do NOT reverse)"* (`scripts/stage4-tail-classifier.py:271`). Rule 13 contradicts this slightly ("swap source/target or REJECT") but the response JSON schema has no field for swaps, so swaps are structurally impossible (`pipeline.md` §3).
6. **The strongest divergent-collapse example is the Red Wedding.** Same n-ary event, encoded across three chapters with three different subject choices and no link between them: `roose-bolton BETRAYS robb-stark` (python-map, asos-catelyn-07); `walder-frey BETRAYS robb-stark` (sonnet, same chapter); `lothar-frey CONSPIRES_WITH roose-bolton` (sonnet, asos-epilogue). `VIOLATES_GUEST_RIGHT` has **7 different subject choices × 8 different target choices** across 5 chapters. Robb has no `KILLS` row at all; Catelyn's killer is `raymund-frey` (the knife-wielder), but Robb's "killer slot" lives on `BETRAYS roose-bolton` (the political agent). (`data.md` §4.1, see Appendix B).
7. **Direction inversions are a systematic class of bug** — the python-mapper takes the *grammatical subject* of the matched sentence rather than the *semantic agent*. Confirmed: `cressen KILLS melisandre` (Cressen "ran afoul of" Melisandre and died); `tyrion BETRAYS shae` (Shae betrayed Tyrion at trial); `arya CAPTURES sandor` (Sandor captured Arya); many `COMMANDS` and `TUTORS` inversions. The `asserted_relation` field often **self-witnesses** the bug ("Killed by", "Betrayed by", "Conflicted captor-dependent"). 232 distinct unordered pairs carry the same edge_type in both directions; most are bugs (`data.md` §4.4–4.7).
8. **The Aerys II slug split is a concrete graph-bisection bug.** Jaime's regicide is encoded as `jaime-lannister KILLS aerys-targaryen`, but the canonical Mad King node is `aerys-ii-targaryen`. Both node files exist. All other Jaime↔Aerys edges resolve to `aerys-ii-targaryen`. The wiki cross-reference (`wiki_edge_type: "KILLS"`) on those other edges flags that the killing IS the canonical fact — but the only KILLS row points at a phantom slug. The gated Events Haiku bulk has the corrected edge (`data.md` §4.2).
9. **The Purple Wedding (Joffrey's poisoning) is almost absent.** The only POISONS row mentioning Joffrey is Tyrion's *false confession*: `tyrion POISONS joffrey, "Claims to have poisoned (unverified)"`. No row sources from Olenna Tyrell or Littlefinger; no `KILLS` row targets Joffrey at all. The historical truth is unrepresented; the only encoded data is the lie (`data.md` §4.3).
10. **All 3,811 canonical edges are `confidence_tier=1`.** The architecture documents Tiers 1–5 (`architecture.md:421-431`) but the data has zero granularity. Every edge is currently treated as verified canon, including ones whose subjects are demonstrably wrong.
11. **Reverse-direction edge-pair additions are the project's de facto admission that single-direction 2-ary is insufficient.** UNCLE_OF/NEPHEW_OF was added "without forcing two-hop traversal through the missing/inferred parent" (`architecture.md:163-164`); IN_LAW_OF was added because two-hop traversal "would *lose* the named in-law relationship known from prose" (`architecture.md:173`). The fix-pattern is: add a reverse edge instead of changing the arity (`priorart.md` §5).
12. **Events ARE already first-class nodes in the schema.** 371 event nodes exist (304 `event.battle`, 35 `event.tournament`, 32 `event.war`), including Red Wedding, Battle of the Blackwater, War of the Five Kings (`graph/nodes/events/`, `graph/index/events/_summary.json:1-12`). The intended n-ary container exists — but the relationships between human participants and the event node are sparsely populated. Red Wedding has 3 outbound edges and 308 inbound mentions; there is no `KILLS robb-stark` row anchored to the event node (`structure.md` §6, `data.md` §4.1).
13. **The single most load-bearing prior-art passage is from the S58 batch-0020 Opus audit** (`working/session-results/2026-05-19-batch-0020-opus-audit.md:244-253`): *"12 of 13 are the same underlying error as the KNOWS problem: an interpersonal/participation relationship at a named occasion, where the classifier targets the person or the venue instead of the event node — because the event node frequently does not exist in the graph, so there is nothing correct to point at … the graph lacks fine-grained event nodes (individual weddings, feasts, sieges), so the classifier has no correct target and improvises."* This is the project's own un-theorized identification of the n-ary collapse problem.
14. **Multi-type entity policy is the project's "collapse, not split" precedent.** "**One node per real-world entity. The `type` field captures its primary identity. Other facets emerge through edges, not through a second node.**" (`architecture.md:115-127`). Free Folk = one `concept.culture` node; faction-ness emerges via edges. Same instinct drives the temporal-scoping decision: solve via 2-ary + metadata, not by widening arity (`worklog.md:91, 121-124`).
15. **The project never uses the words "n-ary," "reify," "reification," "arity," "head," "patient" as theoretical terms.** Greps across `worklog.md` + 16+ archive files + 80+ session detail files + all design docs return zero hits. The problem is present everywhere as a *symptom*, never named as an *abstraction* (`priorart.md` §2). The closest theoretical name in-repo is "co-presence-at-an-occasion trap" (`prose-edge-classifier.md:172-173`).

---

## 1. Project Structure & Orientation

### 1.1 Storage mechanism — definitive answer

**This is NOT Neo4j, NOT RDF, NOT a property-graph DB, NOT SQLite.** It is a **plain-files knowledge graph in a git repo**:

| Layer | Path | Format | Count |
|---|---|---|---|
| Edges | `graph/edges/edges.jsonl` | JSON Lines (one edge per line) | **3,811 typed edges** (v1.3, Session 72) |
| Nodes | `graph/nodes/{type-dir}/{slug}.node.md` | Markdown + YAML frontmatter | **~8,052 clean nodes** + ~230 in `_conflicts/` |
| Indexes | `graph/index/{type-dir}/{slug}.index.json` | JSON-per-entity | **7,635** + per-type `_summary.json` |
| Edge re-grounding backup | `graph/edges/_regrounding/*.jsonl` | JSON Lines | 3,811 (pre/post S74 line-suffix fix) |
| Convergence maps | `graph/convergence-maps/` | (placeholder) | **EMPTY** |

There is **no database engine**, **no `requirements.txt`/`pyproject.toml`/`package.json`/`Makefile`/`justfile`** at any depth (`structure.md` §2). The sole third-party Python dep is `cloudscraper`, used by `scripts/wiki-fetch-categories.py` for the one approved exception fetch (a MediaWiki categories backfill — `CLAUDE.md:26-28`). All other scripts use stdlib only.

LLM passes shell out to the Anthropic `claude` CLI via `claude -p ... --output-format json` subprocesses (memory `reference_llm_pass_via_claude_p`, `pipeline.md` §3), not the SDK. Sessions run with `cwd="/tmp"` to skip the project CLAUDE.md and save ~28k tokens per call (`scripts/stage4-tail-classifier.py:569`).

### 1.2 Directory tree (depth 3, annotated)

The CLAUDE.md "Directory Structure" section is the official map (`CLAUDE.md:71-127`). Selected per-directory purpose (verbatim from CLAUDE.md unless noted):

| Path | Purpose |
|---|---|
| `.claude/agents/` | 28 subagent definitions (`.md` files with `model:`/`description:` frontmatter + system prompt body). Includes `mechanical-extractor.md`, `prose-edge-classifier.md`, `wiki-ingester.md`, `cross-identity-detector.md`, `duplicate-detector.md`, `multi-type-entity-resolver.md`, `voice-analyzer.md`, etc. |
| `.claude/commands/` | Custom slash commands (`stage4-haiku-classify.md`, `worker-stage4.md`, etc.) |
| `curation/` | `curation/candidates.md` — "analytical findings go to `curation/candidates.md`, not directly into the graph" (`CLAUDE.md:135`) |
| `extractions/mechanical/{agot,acok,asos,affc,adwd,status}/` | Pass-1 extraction outputs (one `.extraction.md` per chapter; 344 total per worklog) |
| `extractions/archives/{agot-v1, agot-v2, acok-v2, ...}/` | Prior-version extractions; **never deleted** (memory `feedback_extraction_archive_rules`) |
| `extractions/voice/`, `extractions/foreshadowing/`, `extractions/patterns/` | Pass 3+ outputs (stubs; not yet populated) |
| `graph/nodes/{19 type dirs}/` | Canonical entity files. Type dirs: artifacts, chapters, characters, concepts, customs, events, factions, foods, houses, languages, locations, materials, medical, prophecies, religions, species, texts, theories, titles. Plus `_conflicts/` (duplicate-collision quarantine) and `_unclassified/` (empty) |
| `graph/edges/` | Canonical `edges.jsonl`, `README.md`, `_regrounding/` |
| `graph/index/` | Per-entity `.index.json` files mirroring `graph/nodes/` type dirs |
| `graph/convergence-maps/` | Empty placeholder |
| `history/session-details/session-NNN.md` | 81+ per-session narrative records (human-facing, not loaded by agents) |
| `history/worklog-archives/archive0NN.md` | Older worklog session entries archived in 5-entry blocks |
| `progress/continue-prompts/` | Self-contained resumption prompts |
| `reference/architecture.md` | **Schema reference for all agents.** 595 lines covering type hierarchy + edge taxonomy |
| `reference/edge-qualifier-vocab.md` | Qualifier enums for the 8 Tier-1 + 9 Tier-2 edge types |
| `reference/foreshadowing-events.md` | 26 events + 15 Chekhov's guns, reserved for Pass 4 |
| `reference/pov-characters.md` | POV lookup table + expected chapter counts |
| `scripts/` (132 files) | All Python tooling. `stage4-*.py` family (~40 files) is the active edge-creation pipeline; `wiki-pass2-*.py` (~30) populated the existing edges |
| `scripts/archive/` | Retired Playwright wiki-scraper — **DO NOT restore** (`CLAUDE.md` rule) |
| `sources/` | All gitignored. `raw/` (book .txt), `chapters/` (split chapter .md), `wiki/_raw/` (17,945 cached AWOIAF JSON pages) |
| `tests/` | 21 pytest files, primarily targeting `stage4_*` modules |
| `working/agent-fleet-specs/` | Agent + fleet operating manual (`agent-pipeline-plan.md`, etc.) |
| `working/audits/{12 per-audit folders}/` | Each audit has `prompt/`, `execution/`, `validation/` subdirs |
| `working/wiki/data/` | Permanent reference products (alias-resolver, infobox-data, page-index) |
| `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/` | The gated 1,617-edge Events bulk (not promoted) |

### 1.3 Tech stack

- **Python 3** (no version pin; implies 3.9+ from PEP-585 generics in `scripts/stage4_name_resolver.py:24,30`).
- **No package manifest** of any kind at any depth (verified).
- **No graph DB / triple store / Neo4j / RDF / SQLite / SPARQL / DuckDB.**
- **No web app / no API server / no chat UI in production** — per memory `project_real_goal_graph_for_agents`: *"Primary deliverable is graph quality for agents. The 'D&D-group chat UI / shared-password auth / chat-ui-architecture.md' framing is stale sketch."*
- Sole third-party Python dep: `cloudscraper` (single script: `scripts/wiki-fetch-categories.py`).
- LLM transport: `claude -p` subprocess (not the Anthropic SDK).
- Test runner: pytest. No CI config detected.

### 1.4 Entry points

The primary human entry point is the `weirwood` zsh function (`scripts/weirwood.zsh`, sourced from `~/.zshrc`):

```
weirwood                          # help
weirwood check                    # verify prerequisites
weirwood <book>                   # status: wave table, costs, suggested next command
weirwood <book> <t> <w>           # launch iTerm tabs for extraction
weirwood stop                     # soft stop
```

`scripts/graph-query.py <slug>` is the read-only graph-inspection CLI (modes: default full, `--edges-only`, `--inbound-only`, `--json`, `--neighbors`, `--path`, `--health`, `--edges`).

---

## 2. Node / Entity Model

### 2.1 Entity type hierarchy

The hierarchy is documented at `reference/architecture.md:38-106`. The leaf types map to the directories under `graph/nodes/`:

```
Entity
├── Character
│   ├── Human (3,926 nodes)
│   ├── Direwolf (Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog)
│   └── Dragon (Drogon, Rhaegal, Viserion; historical: Balerion, Vhagar)
├── Place
│   ├── Location (1,097 nodes — Winterfell, Tower of Joy, Citadel)
│   └── Region (The North, Dorne, The Reach, Essos)
├── Organization
│   ├── House (556 nodes)
│   ├── Faction (191 nodes — Night's Watch, Faceless Men, Brotherhood Without Banners)
│   └── Religion (63 nodes — Faith of the Seven, R'hllor)
├── Concept
│   ├── Culture, Magic, Prophecy (2), Theory (45), Language (26), Custom (37), Medical (34)
├── Object
│   ├── Artifact (282), Text (159), Food (74), Material (58)
├── Event
│   ├── Battle (304), War (32), Tournament (35)   — total 371
├── Species (188), Title (542)
└── Meta
    └── Chapter (344 — out-of-universe literary container; NOT in-world events)
```

**Critical design distinction** (`architecture.md:76`): Meta entities (`meta.chapter`) are *literary containers*; in-world Event entities (Red Wedding, Battle of the Blackwater) are *in-world happenings*. The two are categorically distinct. Edges from in-world entities to `meta.chapter` nodes are *citation/provenance* edges, not relationship edges.

### 2.2 Node file format

Filename rule (`architecture.md:30-34`, `CLAUDE.md:132`): `{entity-name-kebab-case}.node.md`. Examples: `jaqen-hghar.node.md`, `horn-of-joramun.node.md`, `the-citadel.node.md` (definite article kept; apostrophes dropped).

Frontmatter (from a real node, `graph/nodes/events/red-wedding.node.md`):

```yaml
---
name: "Red Wedding"
type: event.battle
slug: red-wedding
aliases: []
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Red_Wedding"
bucket_id: battles-p-s
prompt_version: v1-python
node_version: 1
pass_origin: pass2-wiki-deterministic
---
```

The body has fixed-ish sections — `## Identity`, `## Edges`, `## Origins`, `## Narrative Arc`, `## Quotes`, `## Recent Events`. The `## Edges` section is a **human-readable bullet list** (display names, not slugs) with `[AGoT]` / `[ADwD]` temporal-scope brackets:

```
## Edges

- RULES: Eddard Stark (track_b: Ruler) [AGoT]
- RULES: Ramsay Bolton (track_b: Ruler) [ADwD]
- WORSHIPS: Old Gods of the Forest (track_b: Religion)
```

The **canonical typed/sluggified version** lives in `graph/edges/edges.jsonl`. **The two representations are NOT auto-synced.** The JSONL is authoritative for traversal; the per-node bullet list is for readers. (`structure.md` §5).

### 2.3 IDs, aliases, entity resolution

- Slugs are lowercase kebab-case, globally unique within `graph/nodes/`; collisions go to `_conflicts/` (~230 timestamped files; the canonical node remains in its type dir).
- `aliases:` is a YAML list of free-text display strings (`graph/nodes/characters/jon-snow.node.md:5-12` lists 7 aliases: "Lord Snow", "The Snow of Winterfell", "The crow-come-over", "The Bastard of Winterfell", "The Great Lord Snow", "The Black Bastard of the Wall", "Lord Crow").
- An alias→slug deterministic lookup is built by `scripts/wiki-pass2-build-alias-resolver.py` → `working/wiki/data/alias-resolver.json`.
- **Five-rung resolver** (`scripts/stage4_name_resolver.py:1-22`) for Stage-4 candidate generation: (a) exact, (b) alias, (c) firstname-unique, (d) context-present, (e) context-prior, plus (S72 addition) (f) **resolved-title-person** (`stage4_name_resolver.py:355-396`) — when "Lord Tywin" exact-matches a *ship* node named after Tywin, prefer the character via a character-restricted ladder. Real fixes from this rung (per `graph/edges/README.md:66-71`): `lord-tywin → tywin-lannister`, `queen-cersei → cersei-lannister`, `lord-renly → renly-baratheon`, `princess-myrcella → myrcella-baratheon`, `lady-olenna → olenna-tyrell`, `khal-jhaqo → jhaqo`.
- **Cross-identity** (Reek/Theon, Alayne/Sansa) is handled via `SAME_AS` (symmetric) and `ALIAS_OF` (alias → canonical) edge types (`architecture.md:316-319`). Detection: `duplicate-detector` agent enumerates candidates → `cross-identity-detector` decides → `cross-identity-reviewer` audits.

### 2.4 Multi-type entity policy — "collapse, not split"

This is the project's explicit precedent for solving identity tension by edge-composition, not by node-duplication. Verbatim (`architecture.md:115-127`):

> Some real-world entities span multiple of the type categories above. Free Folk are simultaneously a culture (`concept.culture`) and a polity/faction (`organization.faction`). Children of the Forest are simultaneously a species (`species`) and an ancient sentient faction. Wardens are titles, but the *role* of being a warden is also a behavior set.
>
> **Policy: one node per real-world entity. The `type` field captures its primary identity. Other facets emerge through edges, not through a second node.**
>
> - Free Folk → `concept.culture`. Polity-ness emerges via MEMBER_OF (character → free-folk), FIGHTS_IN (war/battle → free-folk), HOLDS_TITLE (king-beyond-the-wall), LOCATED_AT (beyond-the-wall → free-folk).
> - Children of the Forest → `species`. Faction-ness emerges via FIGHTS_IN (war-of-first-men), LOCATED_AT (isle-of-faces), and magic-use edges.
>
> This avoids SAME_AS bookkeeping and ambiguous "which node?" queries. Retrieval naturally unions identity + behaviors via edge traversal.

The same instinct drives temporal scoping (worklog.md:91, 121-124): solve via 2-ary + metadata, not by widening arity. The `multi-type-entity-resolver` agent is a **stub**, deferred until prose data reveals actual cross-type traversal patterns.

---

## 3. Edge Schema

### 3.1 Where it lives

**`reference/architecture.md:130-399`** is the master vocabulary, organized into 15 subsections. **`reference/edge-qualifier-vocab.md:1-60`** declares the qualifier-enum tiers. Both files are reproduced in full in Appendix A.

Every edge instance must carry `type`, `source`, `target`, `first_available`, `evidence`, `confidence` (`architecture.md:132-137`). Qualifier requirements per tier (`architecture.md:147`):

- **Tier 1 (REQUIRED qualifier, 8 types):** SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO.
- **Tier 2 (OPTIONAL qualifier, 9 types):** BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH, DECEIVES, REVEALS_TO, ATTACKS, GUEST_OF, IN_LAW_OF.
- **Tier 3 (no qualifier, ~146 types):** all the rest.
- **`notes` field is DELETED from schema entirely** as of 2026-05-18 Session 57 lock (`edge-qualifier-vocab.md:8`). But `architecture.md:415` still documents `notes` as edge metadata — the two reference files are out of sync.

### 3.2 The 15 subsections (each fully reproduced in Appendix A)

| Subsection | Lines | Types |
|---|---|---|
| Kinship & Family | 149-173 | 21 (PARENT_OF, SIBLING_OF, SPOUSE_OF, BETROTHED_TO, LOVER_OF, WARD_OF, ANCESTOR_OF, HEIR_TO, CADET_BRANCH_OF, **MARRIES_OFF**, UNCLE_OF, NEPHEW_OF, COUSIN_OF, MILK_BROTHER_OF, NURSED_BY, WET_NURSE_OF, COURTS, **PROPOSED_AS_BRIDE**, STEP_PARENT_OF, STEP_CHILD_OF, IN_LAW_OF) |
| Political & Authority | 175-193 | 15 (RULES, OVERLORD_OF, SWORN_TO, COMMANDS, SERVES, ADVISES, HOLDS_TITLE, HELD_BY, SUCCEEDS, CLAIMS, APPOINTS, DEPOSES, VOWS_TO, BREAKS_VOW, BANISHES) |
| Factional & Diplomatic | 195-207 | 9 (MEMBER_OF, FOUNDED, ALLIES_WITH, OPPOSES, MANIPULATES, BETRAYS, NEGOTIATES_WITH, CONTRACTED_WITH, **CONSPIRES_WITH**) |
| Military & Conflict | 209-236 | 22 (FIGHTS_IN, COMMANDS_IN, PART_OF, **KILLS**, KILLED_BY, **EXECUTES**, CAPTURES, PRISONER_OF, **BESIEGES**, DEFEATS, DUELS, POISONS, RANSOMS, **PRISONER_EXCHANGE_FOR**, IMPRISONS, GUARDS, **KILLED_WITH**, KNIGHTED_BY, BESTOWS_KNIGHTHOOD_ON, **ATTACKS**, ASSAULTS, PARTICIPATES_IN, RESCUES, TORTURES) |
| Knowledge & Information | 238-257 | 15 (KNOWS [**deprecated**], IGNORANT_OF, SEEKS, REVEALS_TO, DECEIVES, DECEIVED_BY, HOARDS, INVESTIGATES, TEACHES, TUTORS, HEALS, AFFLICTED_BY, DIED_OF, SPIES_ON, INFORMS) |
| Emotional & Perceptual | 259-275 | 14 (PERCEIVED_AS, TRUSTS, DISTRUSTS, RESPECTS, FEARS, LOVES, HATES, MOURNS, PROTECTS, RESENTS, COMPANION_OF, REPUTED_AS, ENCOUNTERS) |
| Spatial & Temporal | 277-290 | 10 (LOCATED_AT, SEAT_OF, TRAVELS_TO, TRAVELS_WITH, BORN_AT, DIED_AT, BURIED_AT, IMPRISONED_AT, CONTEMPORARY_WITH, REGION_OF) |
| Possession & Ownership | 292-310 | 15 (WIELDS, OWNS, ANCESTRAL_WEAPON_OF, FORGED_BY, MADE_OF, LOOTED_BY, REFORGED_INTO, GIFTED_TO, INHERITED_BY, **WIELDED_IN**, **EXECUTED_WITH**, PURCHASED_FROM, BUILT, CAPTAIN_OF, CREW_OF) |
| Identity & Disguise | 312-319 | 4 (ALIAS_OF, DISGUISED_AS, SAME_AS, IMPERSONATES) |
| Magic & Supernatural | 321-332 | 6 (WARGS_INTO, BONDED_TO, **SACRIFICES**, RESURRECTS, CURSES, PRACTICES) |
| Cultural & Religious | 334-343 | 6 (CULTURE_OF, WORSHIPS, SACRED_TO, CLERGY_OF, **OFFICIATES**, NAMED_AFTER) |
| Narrative & Literary | 345-360 | 7 (DEPICTED_IN, FORESHADOWS, PARALLELS, SUBVERTS, ECHOES, CONTRASTS, WRITTEN_BY) |
| Prophecy | 362-371 | 6 (FULFILLS, APPEARS_TO_FULFILL, SUBVERTS_PROPHECY, PROPHESIED_BY, SUBJECT_OF_PROPHECY, DREAMS_OF) |
| Evidentiary | 373-379 | 3 (SUPPORTS, CONTRADICTS, CITED_BY) |
| Causal & Plot | 381-389 | 5 (CAUSES, PREVENTS, ENABLES, MOTIVATES, TRIGGERS) |
| Hospitality & Custom | 391-399 | 5 (GUEST_OF, **VIOLATES_GUEST_RIGHT**, GRANTS_SAFE_CONDUCT, ATTENDS, **CROWNS_QUEEN_OF_LOVE_AND_BEAUTY**) |

**Bolded types are the canonical n-ary-collapse cases** — see §3.4.

### 3.3 Edge metadata fields (`architecture.md:403-417`)

| Field | Purpose | Example |
|---|---|---|
| `type` | Edge type from taxonomy above | `KILLS` |
| `source` | Source node | `jaime-lannister` |
| `target` | Target node | `aerys-ii-targaryen` |
| `first_available` | **DEFERRED**; spoiler gate | `AGOT Jaime I` |
| `confidence` | Tier 1-5 | `1` |
| `evidence` | Chapter citation or wiki URL | `AGOT Eddard XV` |
| `notes` | **DELETED** per `edge-qualifier-vocab.md:8` | (rejected by validator) |
| `temporal` | When edge is active (free-form) | `"until ASOS"` |
| `symmetric` | Bidirectional? | `true`/`false` |

The architecture file and qualifier vocab file disagree on whether `notes` exists. The validator wins; `notes` is dead.

### 3.4 Binary vs event-like classification

Applied per the brief's test:
- **binary** = exactly 2 participants, fixed roles, no time/place/outcome on the edge itself, can't sensibly carry a third participant.
- **event-like** = >2 plausible participants OR carries its own properties OR has distinct typed roles (agent/patient/instrument/location).
- **ambiguous** = could be argued either way.

**Totals:** ~76 binary, ~82 event-like, a handful ambiguous (158-edge total per inventory; architecture self-reports "~163" with approximate count + KNOWS deprecation arithmetic).

**Top 12 n-ary candidates** (most clearly need event-node modeling), with one-line rationale (Appendix A has the full per-edge classification table):

1. **`KILLS`** (`architecture.md:216`) — killer + victim + weapon (`KILLED_WITH`) + instigator (qualifier `by_proxy`) + location + witnesses. Method-as-qualifier is the schema's tell.
2. **`EXECUTES` + `EXECUTED_WITH`** (`architecture.md:218, 306`) — Ned's beheading: executor (Ilyn Payne) + executed (Ned) + order-giver (Joffrey) + weapon (Ice) + location (Sept of Baelor) + witnesses = 5+ roles split across multiple edges. `EXECUTED_WITH` description literally says *"May overlap with `WIELDED_IN` + `EXECUTES`; kept distinct for narrative-precision queries"* — the schema admits it's decomposing one event into three edges.
3. **`SPOUSE_OF` + `MARRIES_OFF` + `PROPOSED_AS_BRIDE`** (`architecture.md:155, 162, 170`) — a marriage event has bride + groom + arranger + officiant + venue + witnesses + bedding. `PROPOSED_AS_BRIDE` description openly admits 3-party: *"A third party proposes a specific woman as a bride for a specific man."*
4. **`BESIEGES`** (`architecture.md:221`) — besieger + defender + location + war + duration + outcome + allied besiegers. Pure event semantics.
5. **`ATTACKS`** (`architecture.md:232`) — Tier-2 qualifier `on_command` acknowledges a missing instigator (Mountain at Tywin's command).
6. **`SACRIFICES`** (`architecture.md:329`) — sacrificer + victim + recipient deity/magic-system + ritual + place. The "sacrificed-to" axis (R'hllor, the Others, life-magic) is wholly missing from the edge.
7. **`KILLED_WITH` / `EXECUTED_WITH`** — weapon-as-third-role edges. Description acknowledges the killing is split across multiple edges.
8. **`CONSPIRES_WITH`** (`architecture.md:207`) — description says "two or more parties" explicitly.
9. **`PRISONER_EXCHANGE_FOR` + `RANSOMS` + `IMPRISONS` + `PRISONER_OF` + `IMPRISONED_AT`** — captivity is split across 5 edge types.
10. **`CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`** (`architecture.md:399`) — the entire narrative weight is multi-party witness state at the Harrenhal tourney. Description: *"chains to political consequences."*
11. **`SPIES_ON` + `INFORMS`** (`architecture.md:256-257`) — spy-network triangles (spy + surveilled + handler) split into two binary edges. Architecture says these "complement" each other.
12. **`REVEALS_TO` / `DECEIVES`** (`architecture.md:246-247`) — both descriptions parenthetically say "(note what was revealed)" / "(note the deception)" — the *content* is an unrepresentable third role.

### 3.5 Reverse-direction edge-pair additions — the project's signal

Where one direction wasn't enough, the project **added a reverse-direction type** rather than re-shaping the edge. This is the schema admitting that single-direction 2-ary insufficiently supports traversal-based queries.

| Forward | Reverse | Rationale |
|---|---|---|
| `HOLDS_TITLE` | `HELD_BY` | Title-node ↔ Person-node both need traversal |
| `KILLS` | `KILLED_BY` | Victim's node needs to surface killer |
| `DECEIVES` | `DECEIVED_BY` | Same |
| `UNCLE_OF` | `NEPHEW_OF` | "without forcing two-hop traversal through the missing/inferred parent" (`architecture.md:163`) |
| `NURSED_BY` | `WET_NURSE_OF` | Both endpoints record the relation |
| `STEP_PARENT_OF` | `STEP_CHILD_OF` | "one-sided pair, not symmetric — emit both explicitly" (`prose-edge-classifier.md:242`) |
| `KNIGHTED_BY` | `BESTOWS_KNIGHTHOOD_ON` | Both endpoints record the knighting |
| `WARD_OF` | `FOSTERED_BY` (semantic-only, not declared) | `architecture.md:158` |
| `IN_LAW_OF` | (symmetric) | "Use when two-hop traversal would *lose* the named in-law relationship known from prose" (`architecture.md:173`) — explicit two-hop-lossiness rationale |
| `COUSIN_OF` | (symmetric) | "without traversing two PARENT_OF + one SIBLING_OF" (`architecture.md:165`) |

S52 (2026-05-14, `history/session-details/session-052.md:43-59,113-118`) is where the project codified the policy: *"Reverse-direction edges are permitted … Documented as semantic equivalents. Query layer treats `HELD_BY(a→b)` as identical to `HOLDS_TITLE(b→a)`."*

### 3.6 Notable schema observations

1. **`KNOWS` deprecation** (`architecture.md:240`, Session 63 2026-05-21): removed after 82.3% fallback rate on prose classification. *"the semantic boundary ('knows of' vs 'met once' vs 'heard rumor of') is too blurry for prose-derived classification to enforce."* 384 historical edges preserved, filtered on read.
2. **`LOCATED_IN` is a deprecated parser synonym for `LOCATED_AT`** (`architecture.md:281`) — "normalize on read."
3. **Internal schema contradictions** (`schema.md` §5.1):
   - `MANIPULATES` description (`architecture.md:203`) tells the model to *"Note mechanism in `notes`"* — but `MANIPULATES` is Tier-1 with a required `qualifier` enum, AND `notes` is deleted from the schema.
   - `GIFTED_TO` (`architecture.md:303`) says *"Note giver in qualifier"* — but `GIFTED_TO` is Tier-3 (no qualifier permitted). The giver is structurally unrepresentable on the edge.
   - `CREW_OF` (`architecture.md:310`) says *"Note specific role in `notes`"* — `notes` is deleted.
4. **CONSPIRES_WITH is the only edge explicitly admitting >2 participants** (`architecture.md:207`): "Secret joint plot — two or more parties engaged in a covert scheme together."
5. **Verb-gate validator** — `ENCOUNTERS` (`architecture.md:275`) is the first edge type whose emission is blocked unless the classifier finds an explicit prose staging verb. Promoted from prompt-text rule to schema-level enforcement.
6. **Cases where the schema acknowledges a third participant inline** (excerpt):
   - `MARRIES_OFF`: arranger → married-off person; the **spouse** is the silent third.
   - `PROPOSED_AS_BRIDE`: proposer → bride; the **groom** is the silent third.
   - `KILLED_WITH`: victim → artifact; *"Coexists with `KILLED_BY person` — the person did the killing, the artifact was the instrument."*
   - `BANISHES`: banisher → banished; *"destination is a separate temporal LOCATED_AT"* — destination is held on a different edge.
   - `SACRIFICES`: *"Mirri Maz Duur sacrificing Drogo's life-essence; Stannis (via Melisandre) sacrificing Edric Storm's leech-blood / Mance / Shireen; Craster sacrificing his sons to the Others"* — the recipient/purpose axis is fully unrepresented.
   - `TRAVELS_TO`: *"Traveler → Destination (note origin)"* — origin is a third role.
   - `REVEALS_TO`: *"Revealer → Recipient (note what was revealed)"* — content of revelation is unrepresentable on the edge.

### 3.7 Vocabulary evolution — added types are corpus-driven

Per `architecture.md:547` and `schema.md` §5.2, the vocab grew in named sessions when Stage-4 audits surfaced "no-fitting-type" rejection corpora:

- **S54 (2026-05-15)**: +UNCLE_OF, +NEPHEW_OF, +KILLED_WITH, +ATTENDS.
- **S55 (2026-05-16, 2026-05-18)**: 24 additions across two waves — kinship shortcuts, hospitality, military events, profession.
- **S58 (2026-05-19)**: +SPIES_ON, +INFORMS, +NAMED_AFTER, +STEP_PARENT_OF, +STEP_CHILD_OF, +IN_LAW_OF, +RESCUES, +BANISHES, +TORTURES, +CONSPIRES_WITH. Vocab 149 → 159.
- **S61 (2026-05-19)**: +IMPRISONED_AT, +TRAVELS_WITH, +PRISONER_EXCHANGE_FOR, +GUARDS, +ENCOUNTERS. Vocab 159 → 164. ENCOUNTERS introduces the validator verb-gate.
- **S63 (2026-05-21)**: KNOWS deprecated. 164 → 163.

Read this as: the schema is **patching gaps** as audits expose them; new types arrive when prose contains relationships the classifier kept trying to express. The pattern is **never** "this is an n-ary event, model it differently" — it is always "add another narrower 2-ary type."

---

## 4. Edge Data — Current Situation

### 4.1 Files and counts

| Path | Rows | Notes |
|---|---:|---|
| `graph/edges/edges.jsonl` | **3,811** | Canonical v1.3 |
| `graph/edges/_regrounding/edges-preregrounding-backup.jsonl` | 3,811 | Pre-S74 backup |
| `graph/edges/_regrounding/edges-regrounded-candidate.jsonl` | 3,811 | Post-S74 candidate |
| `working/wiki/data/edges-temporal-scoped.jsonl` | 3,811 | Same edges + `book_order, chapter_number, temporal_key` |
| `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/*/*-tail.edges.jsonl` | **1,617** | Gated Events bulk (NOT promoted; failed precision gate at S74). 5 books: agot 236, acok 387, asos 414, affc 239, adwd 341. |

### 4.2 Canonical edge schema (`edges.jsonl`)

Every row has these fields:

```
asserted_relation, candidate_kind, confidence_tier, corroborates_known_edge, decision,
dup_count, edge_type, evidence_book, evidence_chapter, evidence_details, evidence_event,
evidence_kind, evidence_pov, evidence_quote, evidence_ref, evidence_section,
evidence_type_raw, extraction_file, hint_raw, locate_status, produced_at, qualifier,
run_id, schema_version, source_resolution_status, source_section, source_set,
source_slug, target_resolution_status, target_slug, typed_by, wiki_edge_type
```

First row verbatim:

```jsonl
{"decision":"emit_edge","candidate_kind":"pass1_relationship","edge_type":"LOVES","source_slug":"arya-stark","source_resolution_status":"resolved-context-present","target_slug":"jon-snow","target_resolution_status":"resolved-exact","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"He's very gallant, don't you think?\" \"Jon says he looks like a girl,\" Arya said.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:35","asserted_relation":"deep closeness","hint_raw":"deep closeness","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":1,"typed_by":"python-map","corroborates_known_edge":true,"wiki_edge_type":"SIBLING_OF","locate_status":"verbatim","run_id":"pass1-derived-20260523","schema_version":"pass1-derived-v1","produced_at":"2026-05-23T07:17:33+00:00","source_set":"spine","dup_count":4}
```

Field semantics:

- `source_slug` / `target_slug` — kebab-case node IDs; resolve to `graph/nodes/**/<slug>.node.md`. **0 orphans verified** across all 3,811 rows × 2 endpoints.
- `edge_type` — locked vocabulary (102 distinct types in this file).
- `asserted_relation` / `hint_raw` — free-text from Pass-1 extraction ("betrays", "Killed by / ran afoul of", "Captor of").
- `evidence_quote` / `evidence_ref` — verbatim sentence + `file:line` pointer.
- `evidence_section` — usually `"Relationships Observed"`; hospitality uses `"Hospitality & Guest Right"`.
- `confidence_tier` — **all 3,811 rows are tier=1**.
- `typed_by` — provenance: `python-map` (1,964 rows; deterministic), `sonnet` (1,401; LLM tail), `hospitality-table` (396 GUEST_OF), `hospitality-table-violation` (50 VIOLATES_GUEST_RIGHT).
- `source_set` — `spine` (deterministic python-map), `tail` (Sonnet LLM), `hospitality` (table parser).
- `corroborates_known_edge` + `wiki_edge_type` — wiki cross-reference. **Many rows have `corroborates_known_edge: true` while `wiki_edge_type` lists a *different* relation** (e.g. wiki says `KILLS`, row says `RESENTS` for Jaime/Aerys II — Jaime's resentful memories ARE Jaime-killed-Aerys, encoded as the resentment, with the wiki noting the underlying fact).
- `dup_count` — how many duplicate Pass-1 hint occurrences collapsed into this row.

### 4.3 Edge-type distribution (all 102 types in `edges.jsonl`)

```
404 GUEST_OF             265 OPPOSES              255 SERVES               204 DISTRUSTS
173 HATES                171 COMMANDS             157 PROTECTS             156 COMPANION_OF
141 MOURNS               136 RESPECTS             122 RESENTS              121 LOVES
102 KILLS                 91 FEARS                 91 ALLIES_WITH           84 TRUSTS
 84 SWORN_TO              52 SEEKS                 51 SIBLING_OF            50 VIOLATES_GUEST_RIGHT
 46 LOVER_OF              41 PARENT_OF             40 SPOUSE_OF             38 BETRAYS
 35 GUARDS                32 TUTORS                32 ASSAULTS              30 PRISONER_OF
 29 COURTS                27 BETROTHED_TO          25 BONDED_TO             25 UNCLE_OF
 22 ATTACKS               21 COUSIN_OF             21 APPOINTS              19 CONSPIRES_WITH
 19 DEFEATS               19 TEACHES               18 CAPTURES              17 RESCUES
 17 TRAVELS_WITH          16 CONTRACTED_WITH       16 NEPHEW_OF             16 HEALS
 16 NEGOTIATES_WITH       14 HEIR_TO               14 PARALLELS             11 EXECUTES
 11 IN_LAW_OF             11 MEMBER_OF             11 DECEIVES              11 TORTURES
 10 CLAIMS                10 VOWS_TO                9 IMPRISONS               7 OWNS
  7 WARGS_INTO             7 SPIES_ON               7 WORSHIPS                7 BANISHES
  7 DREAMS_OF              6 GIFTED_TO              6 CONTRASTS               6 MARRIES_OFF
  5 WARD_OF                5 OVERLORD_OF            5 CAPTAIN_OF              4 RULES
  4 DUELS                  4 CONTRADICTS            4 POISONS                 4 BESTOWS_KNIGHTHOOD_ON
  4 REVEALS_TO             3 SACRIFICES             3 DEPOSES                 3 NAMED_AFTER
  3 SUCCEEDS               2 DISGUISED_AS           2 INVESTIGATES            2 ATTENDS
  2 DECEIVED_BY            2 BESIEGES               2 CLERGY_OF               2 GRANTS_SAFE_CONDUCT
  2 MILK_BROTHER_OF        2 CREW_OF                2 BORN_AT                 2 IGNORANT_OF
  2 NURSED_BY              2 BREAKS_VOW             1 BUILT                   1 ECHOES
  1 PREVENTS               1 CROWNS_QUEEN_OF_LOVE_AND_BEAUTY                  1 WIELDS
  1 PURCHASED_FROM         1 KILLED_BY              1 RESURRECTS              1 RANSOMS
  1 PERCEIVED_AS           1 STEP_PARENT_OF         1 IMPERSONATES            1 ENABLES
  1 ANCESTOR_OF            1 FOUNDED
```

**The n-ary event vocabulary is thinly populated:** `BESIEGES=2`, `RESURRECTS=1`, `WIELDS=1`, `SACRIFICES=3`, `POISONS=4`, `MARRIES_OFF=6`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY=1`. Many of these refer to a single event that *should* have multiple participant rows but got only one.

### 4.4 Divergent collapses — the headline artifact

**Appendix B contains the full verbatim JSON rows.** Body summary below.

#### 4.4.1 The Red Wedding (`asos-catelyn-07`) — same event, fragmented across 4+ subject choices

The Red Wedding is a single n-ary event with many roles (orchestrator, executor, killer-of-X, killer-of-Y, host, witness, …). The edge data flattens this onto multiple incoherent subject choices.

**BETRAYS rows touching the event:**

- `roose-bolton BETRAYS robb-stark` (typed_by `python-map`, asos-catelyn-07, hint "Betrays")
- `walder-frey BETRAYS robb-stark` (typed_by `sonnet`, asos-catelyn-07, hint "Orchestrates massacre of")
- `lothar-frey CONSPIRES_WITH roose-bolton` (typed_by `sonnet`, **asos-epilogue**)

Both BETRAYS edges are correct, but encode different theories of "who is the subject of the betrayal." No `CONSPIRES_WITH` in `asos-catelyn-07` links Frey and Bolton; the only CONSPIRES row is in a different chapter with no event-id link.

**KILLS rows in `asos-catelyn-07`:**

- `hosteen-frey KILLS lucas-blackwood`
- `ryman-frey KILLS dacey-mormont` (hint: "Complicit in massacre / kills")
- `catelyn-stark KILLS aegon-frey-son-of-stevron` (Catelyn killing Jinglebell)

**Robb Stark has NO `KILLS` row anywhere in `edges.jsonl`.** Implicit in `BETRAYS roose-bolton → robb-stark`. Catelyn's death IS captured but only in the **epilogue** chapter:

- `raymund-frey KILLS catelyn-stark` (asos-epilogue, hint "Raymund opened her throat from ear to ear")

So Catelyn's killer is the knife-wielder (`raymund-frey`); Robb's killer slot is held by the political agent (`roose-bolton`). **Same event, different syntactic role chosen as subject.** This is exactly the divergent-collapse pattern.

**VIOLATES_GUEST_RIGHT rows** — seven subject choices, eight target choices, no internal link:

| Source | Target | Chapter |
|---|---|---|
| walder-frey | catelyn-stark | asos-catelyn-07 |
| walder-frey | robb-stark | asos-arya-11 |
| roose-bolton | brienne-tarth | asos-jaime-05 |
| house-frey | catelyn-stark | affc-alayne-01 |
| house-frey | robb-stark | affc-alayne-01 |
| walder-frey | wendel-manderly | adwd-davos-04 |
| walder-frey | lucas-blackwood | adwd-jaime-01 |
| roose-bolton | house-frey | adwd-theon-01 (Bolton later "violates" the Freys) |

There is **no event-id linking them**; each row is independent. A query asking "who violated guest-right at the Red Wedding?" must union all eight rows; nothing in the schema indicates they're the same event.

#### 4.4.2 Aerys II slug split — the canonical regicide lands on a phantom node

The most dramatic data-quality finding. Jaime's slaying of Aerys II is recorded as:

```
KILLS jaime-lannister → aerys-targaryen   (typed_by python-map, agot-eddard-09)
  quote: "Jaime Lannister poked at Ned's chest with the gilded sword that had sipped
          the blood of the last of the Dragonkings."
```

But the target slug is `aerys-targaryen` — and the canonical Mad King node is **`aerys-ii-targaryen`**. Both node files exist:

- `graph/nodes/characters/aerys-targaryen.node.md` ✓
- `graph/nodes/characters/aerys-ii-targaryen.node.md` ✓
- `graph/nodes/characters/aerys-i-targaryen.node.md` ✓ (a different historical king)

Other Jaime↔Aerys edges resolve to the canonical slug:

```
RESENTS jaime-lannister → aerys-ii-targaryen   wiki_edge_type:"KILLS"
VOWS_TO jaime-lannister → aerys-ii-targaryen   wiki_edge_type:"KILLS"  qualifier:"broken"
```

**The graph is internally split** — traversing `aerys-ii-targaryen` will never reach Jaime's killing edge. The wiki cross-reference (`wiki_edge_type: "KILLS"`) on the OTHER edges flags that the killing IS the canonical fact, but the KILLS row points at a phantom slug.

The **gated Events Haiku bulk** has the corrected edge (`KILLS jaime-lannister → aerys-ii-targaryen`). The bulk that's currently NOT promoted would heal the slug split for this event.

#### 4.4.3 Purple Wedding (Joffrey's poisoning) — almost entirely absent

The only POISONS row mentioning Joffrey is Tyrion's *false confession*:

```
POISONS tyrion-lannister → joffrey-baratheon (typed_by sonnet, adwd-tyrion-03)
  asserted_relation: "Claims to have poisoned (unverified)"
  quote: "Oh, and my nephew Joffrey, I poisoned him at his wedding feast and
          watched him choke to death."
```

There is **no row** with `source=olenna-tyrell` or `source=petyr-baelish` poisoning Joffrey. There is **no `KILLS` row targeting Joffrey at all**. The historical truth (Olenna + Littlefinger orchestration, the strangler poison from Sansa's hairnet) is unrepresented. The only encoded data is the lie.

All four POISONS rows in the graph:

| Source | Target | Note |
|---|---|---|
| cressen | melisandre | "Attempted to kill" — Cressen actually dies from this attempt |
| lysa-arryn | jon-arryn | "poisoned at Petyr's instruction" — flags the missing instigator |
| oberyn-martell | gregor-clegane | "Poisoned/wounded" — mutual fatal duel |
| tyrion-lannister | joffrey-baratheon | "Claims to have poisoned (unverified)" — false confession |

Three of four have something interesting in the subject slot. The `lysa POISONS jon-arryn` case is the clearest acknowledgment of a missing instigator role: the `asserted_relation` itself names Littlefinger as the unencodable third.

#### 4.4.4 Direction-inversion bugs — head-selection failure class

The python-map typer takes the *grammatical subject* of the matched sentence, regardless of whether that subject is the semantic agent. Confirmed inversions:

- **`cressen KILLS melisandre`** (asos-davos-05, hint "Killed by / ran afoul of", quote: *"Until he ran afoul of Melisandre, and died for it."*). Grammatical subject = "he" = Cressen; semantic agent = Melisandre. The asserted_relation literally says "Killed by." A different chapter has the correct row (`melisandre KILLS cressen`).
- **`tyrion BETRAYS shae`** (asos-tyrion-10, hint "Betrayed by (former lover)"). Shae betrayed Tyrion at the trial. Asserted_relation self-witnesses the inversion. A next-chapter row has the correct direction.
- **`arya CAPTURES sandor`** (asos-arya-11). Sandor captured Arya in the prior chapter (`sandor CAPTURES arya`, correct). This second row has hint *"Conflicted captor-dependent relationship"* — Arya's POV, but the edge nominated Arya as captor.
- **`COMMANDS`** inversions: `qhorin-halfhand ↔ jon-snow`, `cersei ↔ tywin`, `janos-slynt ↔ jon-snow`, `bran ↔ luwin`, `jon ↔ jeor-mormont`.
- **`TUTORS`** inversions: `syrio-forel ↔ arya-stark`, `luwin ↔ bran-stark`.
- **`SERVES`** inversion: `joffrey ↔ tyrion`.
- **`RESCUES`** inversion: `sansa ↔ dontos-hollard` (Dontos rescues Sansa).

**232 distinct unordered pairs** carry the same edge_type in both directions. Some are appropriate (symmetric: SIBLING_OF, SPOUSE_OF, LOVER_OF, COMPANION_OF, CONSPIRES_WITH, ALLIES_WITH, BONDED_TO). Many are NOT — the python-map does not enforce direction-class constraints per type.

#### 4.4.5 Multi-relation pairs — 278 pairs with ≥3 distinct edge_types

Largely intentional (one relationship has multiple aspects across chapters), but every row is presented as equally current — there is no snapshot/temporal-slice mechanism in the canonical file. Top examples:

| Pair | # distinct types | Types |
|---|---|---|
| tyrion → jaime | 13 | ASSAULTS, CONTRASTS, DISTRUSTS, DREAMS_OF, HATES, LOVES, MOURNS, PROTECTS, RESENTS, RESPECTS, REVEALS_TO, SIBLING_OF, VOWS_TO |
| brienne → jaime | 11 | CAPTURES, COMPANION_OF, DUELS, GUARDS, HATES, LOVES, PROTECTS, RESPECTS, TRAVELS_WITH, TRUSTS, VOWS_TO |
| tyrion → joffrey | 10 | COMMANDS, DISTRUSTS, GUEST_OF, HATES, OPPOSES, POISONS, PROTECTS, RESENTS, SERVES, UNCLE_OF |

This is one of the cases where adding temporal scoping (`book_order, chapter_number` per edge, Session 76) is the project's stated structural answer rather than reifying.

#### 4.4.6 Renly's death — under-collapsed

- `stannis-baratheon KILLS renly-baratheon` (acok-catelyn-04, typed_by python-map)
- `stannis-baratheon MOURNS renly-baratheon`
- `loras-tyrell MOURNS renly-baratheon`
- `brienne-tarth MOURNS renly-baratheon`

The shadow killer is `stannis-baratheon` (the political agent). **The actual proximate executor (Melisandre's shadow) is NOT captured** — zero edges between `melisandre` and `renly-baratheon` in either direction. Instrument (shadow) and instigator (Stannis) are merged into the single subject slot.

#### 4.4.7 Bran's defenestration — single-row n-ary

```
ASSAULTS jaime-lannister → bran-stark (typed_by sonnet, agot-bran-02)
  asserted_relation: "pushes/attempts to kill"
  quote: "He gave Bran a shove."
  wiki_edge_type: "CAPTURES"   (wiki disagrees on the relation)
```

A 4-role event: Jaime as agent, Cersei as motivator (her presence is the reason for the pushing), Bran as patient, intimacy-discovery as cause. Cersei has no edge connecting her to this event.

#### 4.4.8 Tywin's death — clean single row, loses instrument and context

```
KILLS tyrion-lannister → tywin-lannister (asos-tyrion-11, dup_count: 7)
```

No edges encode the crossbow instrument, the location (privy), or Shae's presence in the next room as context (despite Shae being killed in the same scene as `tyrion KILLS shae` — both rows exist independently with no event-id link).

#### 4.4.9 PARENT_OF — true-binary baseline (clean)

```
eddard-stark PARENT_OF arya-stark      "father, protective/understanding"
eddard-stark PARENT_OF jon-snow        "Regards thoughtfully"
eddard-stark PARENT_OF bran-stark      "has authority over"
catelyn-stark PARENT_OF bran-stark     "Mother, separated from Bran"
catelyn-stark PARENT_OF rickon-stark   "Mother, neglectful (temporarily)"
hoster-tully PARENT_OF catelyn-stark   "Father (protective, past)"
lysa-arryn PARENT_OF robert-arryn      "Fiercely protective, smothering"
```

Verified: **no PARENT_OF pair appears in both directions.** The binary symmetric-prohibition is respected by the data. Each row gets a single subject (parent) and single target (child); the asserted_relation enriches with sub-role. **This is what "true binary" looks like in this graph.**

### 4.5 Data-quality summary

| Check | Result |
|---|---|
| Rows with null `source_slug` | **0** |
| Rows with null `target_slug` | **0** |
| Distinct orphan source slugs (no matching node file) | **0** |
| Distinct orphan target slugs | **0** |
| Node files total | 8,297 |
| Duplicate `(source, edge_type, target)` triples | **69 distinct**, max 4 copies |
| Bidirectional same-type pairs | **232 distinct unordered pairs** (mix of legit symmetric and direction-inversion bugs) |
| Pairs with ≥3 distinct edge_types same direction | **278** |
| `:11` line-number bug | **Fixed in S74** (3,676/3,811 regrounded); pre-fix backup retained |
| Aerys slug split | **Real bug** — `aerys-targaryen` (2 edges) vs `aerys-ii-targaryen` (~8 edges) both have node files |
| Head-selection inversions | **Systematic class of bug**; python-map takes grammatical subject as edge source |
| Wiki-cross-ref disagreement | `wiki_edge_type` differs from `edge_type` on many `corroborates_known_edge:true` rows |
| `confidence_tier` granularity | **All 3,811 rows are tier=1**; architecture defines 5 tiers |

### 4.6 The gated Events Haiku bulk (1,617 rows)

NOT promoted into `edges.jsonl`. Per `worklog.md:107-114`, the S81 drift audit returned 48% triple-level agreement (gate 70%), 56% pair-level (gate 85%) — failed precision gate. Schema differences:

- `candidate_kind`: `pass1_events` (vs `pass1_relationship`)
- `typed_by`: `haiku`
- `confidence_tier`: mix of `1` and `2`
- Adds: `prompt_version` (`v5-precision-rules`), `prompt_sha` (`d31ca56c4768`), `locate_quality`, `quote_source`
- `asserted_relation` carries a **rich event-title summary** in the format `**<short title>** — <description>`

Bulk type distribution (1,617 rows):

```
388 LOVES          221 MOURNS          145 KILLS          134 HATES          133 FEARS
107 ATTACKS         96 PROTECTS         95 SWORN_TO        76 RESENTS         74 DREAMS_OF
 60 SACRIFICES      40 ALLIES_WITH      32 WIELDS          26 RESPECTS        25 EXECUTES
 25 BETRAYS         18 BONDED_TO        13 CONSPIRES_WITH  10 TRAVELS_TO       9 WARGS_INTO
  6 OPPOSES          5 IMPRISONS         3 WORSHIPS         3 PRISONER_OF      2 POISONS
  2 SIBLING_OF
```

**The n-ary-event vocabulary is much better populated here**: KILLS=145 (vs canonical 102), ATTACKS=107 (vs 22), SACRIFICES=60 (vs 3), WIELDS=32 (vs 1), DREAMS_OF=74 (vs 7).

**Key observation about the bulk's data shape:** the `asserted_relation` uses a rich event-title format like `**Jaime reveals why he killed Aerys** — In a fever-state, he tells Brienne the full story of Aerys's wildfire plot…`. **Multiple bulk rows with the same `**title**` could in principle be linked as the same n-ary event.** For example, `**Jaime's kills are revealed**` appears as `jaime KILLS daryn-hornwood` AND `jaime KILLS eddard-karstark` AND `jaime KILLS torrhen-karstark` — same event title, three target rows. The shared title is the closest thing to an event-id in any layer of the graph today.

---

## 5. Edge Creation Pipeline

### 5.1 End-to-end trace

There are two parallel pipelines, sharing the vocab but using different evidence sources:

| Pipeline | Source | Producer | `evidence_kind` stamp |
|---|---|---|---|
| **Pass-1-derived** (active) | `extractions/mechanical/{book}/*.extraction.md` tables | `scripts/stage4-pass1-*.py` + `stage4-tail-classifier.py` | `book-pass1` |
| **Wiki-prose** (built bulk of existing edges) | `sources/wiki/_raw/*.json` + promoted nodes | `prose-edge-classifier` agent | `wiki-entity` / `wiki-chapter-summary` |

**Pass-1-derived pipeline trace (the active one):**

```
Pass-1 chapter extraction (Opus via `claude -p`, .claude/agents/mechanical-extractor.md)
  └─ writes `## Relationships Observed` table: | Character A | Relationship | Character B | Evidence |
     │
     ▼
stage4-pass1-edge-candidates.py  (deterministic, no LLM)
  - parses table rows; A → source_slug, B → target_slug (column-locked direction)
  - five-rung resolver (exact → alias → firstname-unique → context-present → context-prior)
  - types hint via stage4-pass1-hint-inventory.py (exact → prefix → keyword phrase-map)
  - routes typed → {chapter}.candidates.jsonl; untyped → tail queue
     │
     ▼
stage4-pass1-evidence-locator.py  (deterministic)
  - locates verbatim sentence in sources/chapters/{book}/{chapter}.md
  - emits locate_quality, quote_source, evidence_ref, evidence_quote
     │
     ▼
stage4-tail-classifier.py  (LLM, claude -p, default Sonnet; Events bulk uses Haiku)
  - reads _tail rows (source_slug, target_slug, hint, quote ALREADY FIXED upstream)
  - LLM can only choose TYPE or REJECT — NOT swap endpoints
  - prompt: _PROMPT_PREAMBLE (lines 227-441) + locked vocab + per-row JSON
     │
     ▼
stage4-type-contract-validator.py  (deterministic post-LLM corrections)
  - retypes RULES→character to COMMANDS, flips MEMBER_OF direction, drops MOTIVATES with
    character source, flags HOLDS_TITLE with non-title target
     │
     ▼
stage4-formalize-edges.py  → graph/edges/edges.jsonl
```

**Wiki-prose pipeline** (`pipeline.md` §1.2): three candidate-builder scripts (`source_target`, `comention`, `pass1_relationship`) → `prose-edge-classifier` agent decides `emit_edge` / `reject_just_mention` / `escalate_*` → validator → promote.

### 5.2 The Pass-1 mechanical-extractor prompt

**Full verbatim in Appendix C.1.**

Key facts (`.claude/agents/mechanical-extractor.md`):

- Frontmatter: `model: opus`. All 5 books were extracted on Opus.
- This is the **first LLM step that produces relationship rows.**
- The `## Relationships Observed` schema (lines 176-178) is `| Character A | Relationship | Character B | Evidence |`.
- **The prompt does NOT instruct the model how to choose A vs. B for n-ary events.** No head-selection rule, no agent/patient role specification, no canonical-subject convention. The model picks freely based on whatever the chapter POV's narrative emphasis suggests.
- The prompt explicitly defers analysis: *"Capture **facts**, not interpretations"* (line 16). *"Tables contain facts. Do not use table cells to explain your extraction choices"* (line 222).
- Chapter isolation rule (lines 20-28): extractor must not use cross-chapter knowledge. **Consequence:** an event spanning multiple chapters (Red Wedding spans ASOS Catelyn VII → Arya XII → Epilogue) gets INDEPENDENT relationship tables per chapter, and the same massacre is encoded differently in each.

This is the **upstream root cause of head-selection variance.** Every downstream pipeline takes (Character A, Character B) at face value; column position locks direction.

### 5.3 The Stage-4 classify prompt — THE prompt for head-typing

**Full verbatim in Appendix C.2** (extracted from `scripts/stage4-tail-classifier.py:227-441`).

Key facts:

- Built as Python string literal `_PROMPT_PREAMBLE` — 215 lines of preamble + dynamic vocab block + per-row JSON + closing instruction.
- `DEFAULT_PROMPT_VERSION = "v5-precision-rules"`. The version label stamps every output row.
- `compute_prompt_sha` SHA-256s `_PROMPT_PREAMBLE + vocab_block` and stamps the first 12 hex chars onto every row (`prompt_sha`). The SHA rotates whenever any prompt rule or vocab token changes.
- Default model: `claude-sonnet-4-6`. Events bulk uses `claude-haiku-4-5`.
- Delivered via `claude -p --dangerously-skip-permissions --model <model> --output-format json <prompt>` with `cwd="/tmp"` (saves ~28k tokens per call).

**Critical: the LLM cannot choose the head.** Python assigns source_slug + target_slug deterministically from Pass-1 table column order. The classify prompt's **Rule 5** is the lockdown:

> **5. Direction is FIXED: edge runs source → target (do NOT reverse).**

**Rule 13** elaborates:

> **13. Direction reminder — source is the ACTOR/SUBJECT of the relationship; target is the OBJECT.** The edge runs source → target. Before emitting, verify the direction is correct:
> - If the evidence shows the REVERSE direction, swap source/target or REJECT.
> - Example of the error to avoid: emitting HEALS Bran→Luwin when Luwin heals Bran. The correct emit is HEALS Luwin→Bran (source=Luwin, target=Bran).
> - If you are uncertain which direction the evidence supports, REJECT rather than guess.

(Rules 5 and 13 partially contradict — Rule 5 says "do NOT reverse," Rule 13 says "swap source/target or REJECT." In practice **the JSON output schema has no field for swapping endpoints** — only `{"idx", "edge_type", "qualifier?", "confidence_tier"}`. The model can only TYPE or REJECT; reversal is structurally impossible.)

### 5.4 The V5 precision rules — the most fully-codified subject-selection ruleset

Verbatim (`scripts/stage4-tail-classifier.py:382-399`):

> **v5 PRECISION RULES — applied on top of all prior rules; REJECT if any is violated:**
>
> **V5-R1 — DIRECTION LOCK on structural edges.** For LOCATED_AT, TRAVELS_TO, PARTICIPATES_IN, IMPRISONED_AT, GIFTED_TO: the moving/located/participating entity (person/artifact) is the SOURCE; the place/event is the TARGET. GIFTED_TO specifically requires SOURCE=artifact, TARGET=recipient. **If the row's source/target occupy the wrong roles for the type, REJECT — you cannot swap them, so reject the mis-oriented row.** (e.g. `hardhome LOCATED_AT talon` is backwards — a place is not located at a ship → REJECT; `war-of-the-five-kings PARTICIPATES_IN dick-cole` is backwards → REJECT.)
>
> **V5-R2 — EVIDENCE MUST SUPPORT BOTH ENDPOINTS** (highest-value rule). Emit a type ONLY if the evidence_quote (with the hint) actually establishes a relationship between THIS source AND THIS target. Co-occurrence in the same chapter is NOT evidence. If the quote describes the source's relationship to a DIFFERENT entity, REJECT. Both endpoints must be supported by the quote — either named OR via a pronoun/reference unambiguously resolvable from the quote itself.

Other load-bearing rules in the same prompt:

- **GATE 2 — DIRECT pair** (line 245-247): *"Is the relationship between THIS source and THIS target directly, or is one of them only connected through a THIRD party named in the quote? 'A orders B to do X to C' is NOT an A→C edge. If the link is two-hop, REJECT."* This rule **prevents the LLM from collapsing instigator→victim** ("Tywin orders Mountain to kill Eddard's brother" should NOT yield `tywin KILLS brandon`).
- **Rule 4a — EVIDENCE-GROUNDING** (line 257-265): *"The `hint` is a candidate label, NOT proof. The `evidence_quote` is the only proof. If the quote does not state the relationship, REJECT — even if the hint asserts it and even if you know it is true from the books."*
- **Passive-voice subject-selection** (line 319-324, on KILLS): *"In passive constructions ('Euron had Sawane drowned', 'X was killed by Y'), the AGENT/killer is the SOURCE — do not assign the grammatical subject of a passive sentence as the killer."*
- **Rule 12 — CO-PRESENCE PRINCIPLE** (line 355-369): *"Two entities sharing a scene, room, meal, march, battle, council, or passage is NOT, by itself, a typed relationship. An edge requires an ACTION or STANCE directed from the SOURCE to the TARGET, stated in the evidence_quote. Co-presence is the single most common false-positive source."* This is **the de facto anti-n-ary-flattening rule.**

### 5.5 The wiki-prose classifier — the closest thing to explicit n-ary discussion

**Full verbatim in Appendix C.3** (`.claude/agents/prose-edge-classifier.md`).

The **single clearest "we know about n-ary collapse" passage in the codebase** is in this agent's "Common failure patterns" section (lines 172-173):

> **The co-presence-at-an-occasion trap (applies to ATTENDS, FIGHTS_IN, ENCOUNTERS).** Minor characters' wiki biographies are dense lists of "X was present when Y happened." Each named entity in such a sentence becomes a candidate. Do not manufacture an edge for every co-presence. Ask: does the prose state a *typed relationship* (betrothal, service, command, killing, teaching), or merely that two entities were *near each other*? If the latter, and the occasion is a named event WITH a graph node, emit a single `ATTENDS → <event-node>`. **If the occasion has no event node, `reject_just_mention` with `no-event-node-available`. Do not redirect the unmet edge onto a person or a venue.**

This rule tells the classifier: "**an event has a head — it's the event-node itself, not any human participant.** But if no event-node exists in the graph, the rule is *reject*, NOT *pick a human head*."

Pattern 2 and Pattern 3 (lines 190-212) explicitly forbid the canonical n-ary-collapse failures:

> **Pattern 2: FIGHTS_IN targets events, not persons.**
> Wrong: `FIGHTS_IN aenys-frey → stannis-baratheon` ("Aenys fought against Stannis")
> Right: `FIGHTS_IN aenys-frey → <whichever-battle>` PLUS `OPPOSES aenys-frey → stannis-baratheon`

> **Pattern 3: ATTENDS targets events, not the persons inside the event.**
> Wrong: `ATTENDS lyle-crakehall → margaery-tyrell` ("Lyle attended the wedding of Tommen and Margaery")
> Right: `ATTENDS lyle-crakehall → tommen-margaery-wedding` (the wedding event)
> If the specific wedding/tourney event doesn't have a graph node, you have two choices: (a) **reject** the candidate as `no-event-node-available` if the relationship is just attendance; or (b) emit a different edge type … Do NOT default to ATTENDS-a-person.

### 5.6 Type-contract validator — deterministic post-LLM corrections

`scripts/stage4-type-contract-validator.py` is the only place where head/direction can be deterministically corrected after the LLM has run. Contracts (`pipeline.md` §4.5):

- **Contract 2b — `RULES → character` retypes to `COMMANDS`.** Architecture says RULES = Ruler→Location; COMMANDS = Commander→Subordinate. When LLM emitted RULES with a character target, the script silently retypes.
- **Contract 5 — `MOTIVATES` source must NOT be a character → DROP.** Architecture says MOTIVATES = Event/condition → Actor.
- **Contract 8 — `MEMBER_OF` direction FLIP.** Person→faction/house is correct. If source is faction and target is character, swap source/target.
- **Contract 9 — `HOLDS_TITLE` target-not-place FLAG.** If target is location/region, annotate but keep.

**These contracts are the only place where head/direction can be deterministically corrected** post-LLM. They run after `stage4-tail-classifier.py`.

### 5.7 Sample input — the Red Wedding chapter's Relationships Observed table

**Full verbatim in Appendix C.5.** Six relationship rows from `extractions/mechanical/asos/asos-catelyn-07.extraction.md:286-315`:

- `Walder Frey` | `Orchestrates massacre of` | `Robb Stark and his followers` (multi-target — unparseable)
- `Roose Bolton` | `Betrays / kills` | `Robb Stark`
- `Ryman Frey` | `Complicit in massacre / kills` | `Dacey Mormont`
- `Hosteen Frey` | `Kills` | `Lucas Blackwood`
- `Black Walder` | `Hamstrings` | `(unnamed Vance)`
- `Catelyn Stark` | `Kills (in despair)` | `Aegon Frey (Jinglebell)`

Observations:
- The Red Wedding has no event-node target in the graph — encoded as bilateral relations.
- Multi-target cells (`Robb Stark and his followers`) are unparseable by the resolver → no edge.
- The same massacre, extracted from a different POV chapter, would produce a completely different binary encoding with different head choices.
- The free-text labels (`Orchestrates massacre of`, `Complicit in massacre / kills`, `Hostage-taker/killer of`) don't map cleanly to the locked vocab → fall to LLM tail.
- `walder-frey ORCHESTRATES robb-stark` — no such type → REJECT or fall back to `BETRAYS` / `KILLS by_proxy`.
- The Pass-1 prompt offers no guidance on whether to write "Walder Frey orchestrates massacre of Robb" vs. "Robb is killed by Walder Frey's orchestration" — both forms are plausible English; column choice determines edge direction.

---

## 6. Prior Art — Worklogs & Decisions

### 6.1 What the graph is FOR

The graph is built to be **traversed by agents** to answer **connection / "who-did-what" / cross-identity questions** — not to be a structured fan wiki.

- `CLAUDE.md:6-12`: *"This project builds a queryable knowledge graph for ASOIAF by … Enabling spoiler-gated queries that traverse connections between characters, locations, artifacts, theories, and prophecies."*
- `worklog.md:362` (Principles): *"The index and the graph are complementary. The index routes. The graph traverses. Both are needed."*
- Memory `project_real_goal_graph_for_agents`: *"Primary deliverable is graph quality for agents."*
- `architecture.md:138-143`: *"This taxonomy normalizes both into a controlled vocabulary that is **specific enough to be queryable** but **general enough to avoid synonyms** (e.g., one `SERVES` rather than SERVES / SERVED_BY / CLAIMS_TO_SERVE / SWORN_TO all meaning slightly different things)."*
- `architecture.md:550`: *"the graph's value comes from being able to traverse `SPOUSE_OF` everywhere consistently. If one source emits `SPOUSE_OF` and another emits `MARRIED_TO`, traversal breaks."*
- `history/session-details/session-052.md:74-82` (Matt's reframing): *"Tier-difference, not polish. A chat UI on today's graph = structured feudal wiki with a search bar. A chat UI on the Stage 4 graph = something that can answer 'what does Tyrion fear?' or 'which characters mourn Robb Stark?' with sourced edges."*
- Memory `user_asoiaf_design_values`: *"food/hospitality and physical descriptions are first-class extraction targets; **cross-identity matching is a key use case**."*

The collaborator should read these as: **head-selection variance matters because it breaks graph-traversal queries.** "Show me everyone who betrayed Robb" misses `walder-frey` if only `roose-bolton BETRAYS robb-stark` is emitted, and misses `roose-bolton` if only `walder-frey BETRAYS robb-stark` is emitted. Both rows exist — but no query layer in this codebase knows to merge them.

### 6.2 The S58 batch-0020 Opus audit — the gold quote

**The single most load-bearing passage of prior art on the n-ary problem.** The project hit it head-on without naming it as n-ary.

`working/session-results/2026-05-19-batch-0020-opus-audit.md:244-253`:

> "All 13 non-KNOWS flags are legitimate defects. **12 of 13 are the same underlying error as the KNOWS problem**: an interpersonal/participation relationship at a named occasion, where the classifier targets the *person* or the *venue* instead of the *event node* — because the event node frequently does not exist in the graph, so there is nothing correct to point at. This strongly suggests the `ATTENDS`/`FIGHTS_IN` defects and the `KNOWS` defects share one root: **the graph lacks fine-grained event nodes (individual weddings, feasts, sieges), so the classifier has no correct target and improvises.**"

The same audit (lines 209-217) describes Pattern-3 violations on Edmure's wedding — six rows, all flattening n-ary "X attended the wedding" onto "X attended Edmure":

> *"3a. ATTENDS-a-person (6 rows) — Pattern-3 violation, exactly as the prompt warns. … Every one is 'attended the wedding of Edmure Tully' — the classifier targeted **Edmure** (a person) instead of the **Edmure-Roslin wedding event**. The prompt's Pattern 3 explicitly forbids this ('Never the bride, groom, host, honoree'). The correct target is the wedding event node if one exists, else `reject` with `no-event-node-available`. This is the same trap as KNOWS-fallback — co-presence at a celebration — just routed through ATTENDS instead."*

Lines 219-227 describe the venue-as-event variant:

> *"3b. ATTENDS-a-place (5 rows) — venue mistaken for event. … The classifier targeted the **venue** (a `place.location`) instead of the ceremony held there. `godswood-of-winterfell` is where Ramsay's wedding happened; the edge should point at the wedding event, not the godswood."*

Lines 236-242 describe the same flattening for FIGHTS_IN:

> *"`walder-frey-son-of-ryman → crag` … `crag` resolves to a `place.location`, not an `event.*`. … The correct edge is `FIGHTS_IN` → the *storming-of-the-Crag* event … The classifier conflated the siege *event* with the castle *place*."*

The audit identifies the missing-event-node as the root cause **but does not propose event reification as the fix.** Instead the codified mitigation is `reject_just_mention` (`prose-edge-classifier.md:172-173`) — drop the edge rather than commit to a head.

### 6.3 The vocabulary "absence" — no n-ary, no reify, no head

Grepping the entire repo (`worklog.md` + 16+ archive files + 81+ session-detail files + all design docs + all reference files + all script comments) for `n-ary`, `nary`, `reify`, `reification`, `arity`, `head`, `patient` as theoretical concepts yields **zero hits.**

The problem is present everywhere as a *symptom*, never named as an *abstraction.* The closest in-repo terminology is:

- "co-presence-at-an-occasion trap" (`prose-edge-classifier.md:172`)
- "Pattern 2 / Pattern 3 violations" (`prose-edge-classifier.md:190-212`)
- "underdetermined subject" (only used in this report's framing — never in repo)
- "hint-as-evidence drift" (the Haiku failure mode catalog in `cross-model-audit.md:167-183`)

### 6.4 Multi-type entity policy — "collapse, not split"

(Already quoted in §2.4.) The "Free Folk = ONE node, faction-ness via edges" policy is the project's strongest precedent for solving multi-faceted identity by edge-composition rather than node-duplication. The same instinct drives temporal scoping: solve via 2-ary + metadata, not by widening arity.

`worklog.md:121-124` (Session 75):
> **"Temporal flagging endorsed** — per-edge 'when does this apply' is the right structural answer to the contradictory-edges problem, and it's largely deterministic (every edge carries `evidence_book`+`evidence_chapter`; chapter frontmatter has `chapter_number`)."

`worklog.md:91` (Session 76 result):
> *"Edge temporal-scoping … annotates all 3,811 edges with `(book_order, chapter_number)` + temporal-aware conflict re-audit → **31/32 flagged pairs are temporal arcs**, 1 true same-window."*

This pattern — "edges-with-metadata, not events-as-nodes" — is the project's working theory of the modeling space, even though the problem space (head-selection on n-ary events) suggests reification might be cheaper.

### 6.5 Reverse-direction edge-pair additions — rationale per pair

(See §3.5 for the full table.) The schema repeatedly admits 2-ary single-direction is insufficient → adds a reverse rather than abstract differently:

- **UNCLE_OF / NEPHEW_OF** (`architecture.md:163-164`): *"Captures uncle/aunt without forcing two-hop traversal through the missing/inferred parent."*
- **COUSIN_OF** (`architecture.md:165`): *"Captures first/second/etc. cousins without traversing two PARENT_OF + one SIBLING_OF."*
- **IN_LAW_OF** (`architecture.md:173`): *"Use when a two-hop traversal (SPOUSE_OF + PARENT_OF + invert) would lose the named in-law relationship known from prose."* — explicit two-hop-lossiness rationale.

Each reverse pair is a confession that the forward edge alone doesn't make the relation reachable from the wrong endpoint. The fix is always "add another binary," never "make the underlying relation a node."

### 6.6 Cross-identity / disguise modeling

Reek/Theon, Alayne/Sansa, Jaqen/Alchemist are treated as identity-resolution problems, NOT as "which identity does the edge attach to."

- `architecture.md:316-319`: `ALIAS_OF` (alias → true identity), `SAME_AS` (symmetric), `DISGUISED_AS` (person → disguise identity), `IMPERSONATES` (impersonator → impersonated).
- `history/session-details/session-041.md:43`: *"Identity-layer vs graph-layer separation locked in. Alayne and Reek remain distinct graph nodes (POV=0 in their indexes after the change, but mentioned_in retained). The character index treats them as Sansa/Theon for retrieval. Graph-level merge (`SAME_AS` edges, node deletion/redirect) is Stage 4 work."*
- Memory `project_impersonation_edges_redirect`: *"when wiki encodes an edge from in-universe identity fraud, attach it to the impersonator's node."*
- `perception-mapper.md:14-16` codifies POV-locked perception: *"Eddard's POV sees Cersei as `THREATENS` and `RESENTS_OBLIGATION_TO`; Sansa's POV sees Cersei as `ADMIRES` (early) shifting to `FEARS` (later). Both are valid for the same target node — they're attributed to the POV, not to the target."*

### 6.7 Group-action / many-to-many edges

The project treats group violations as 2-ary edges between primary-actor and primary-victim, plus separate edges for each pair-wise relationship. There is **no n-ary "group violates against group" edge.**

- `VIOLATES_GUEST_RIGHT` is `Violator → Victim` (`architecture.md:396`).
- `working/todos.md:58`: *"529 deterministic $0 edges from Hospitality (460 GUEST_OF + 69 VIOLATES_GUEST_RIGHT; Red Wedding verified)"* — pair-wise emission for the Red Wedding (69 violator→victim rows).
- `CONSPIRES_WITH` description (`architecture.md:207`): *"Secret joint plot — two or more parties engaged in a covert scheme together"* — admits the n-ary in language, emits as symmetric pair-wise.

The coalition battle pattern is the project's working approach: the **battle/event IS a node** (`event.battle`, `event.war`, `event.tournament`), every participant emits `FIGHTS_IN → battle-node`, pair-wise opposition captured via `OPPOSES`. The S58 audit (§6.2) is the project realizing this pattern *only works when the battle-node exists* — when it doesn't, n-ary participants get pair-wise mis-routed.

### 6.8 POV / perception leakage into edges

The project recognizes POV as a *source of structured edge information* (PERCEIVED_AS, FEARS, MOURNS, RESENTS edges sourced from POV's internal state). It does NOT explicitly discuss "the grammatical subject of GRRM's POV sentence is the POV character's focus, not the agent" as a failure mode — but the V5-R1 / V5-R2 / Rule 12 rules are de facto fighting exactly this.

The cross-model audit's 5-pattern Haiku failure catalog (`working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md:167-183`) is the closest the project comes to enumerating POV-leakage variants:

> Across the inspected disagreements, **Haiku consistently treats the `hint_raw` field as evidence on par with `evidence_quote`** … The 22 unanimous rejections from the Sonnet judge cluster around five hint-vs-quote failure modes:
> 1. **Memory / dream / hypothetical staged as fact** (Asha at Ten Towers).
> 2. **Mention-of-place treated as location-at-place** (Tyrion + Pentos).
> 3. **Co-presence in a single scene treated as TRAVELS_WITH** (Tyrion + Podrick; Haldon + Duck).
> 4. **Looking-at / approaching treated as LOCATED_AT / TRAVELS_TO** (Jon + Frostfangs; Sansa + the Fingers; the *Shy Maid* + Ny Sar).
> 5. **Quoted intent / overheard plan treated as completed action** (Urswyck + Harrenhal).

Each entry is "the POV character's *focus* in the sentence was nominated as the edge's subject/object, but the relationship the POV is *experiencing* is not the one the edge encodes."

### 6.9 Open questions and active TODOs

From `worklog.md` and `working/todos.md`:

- **`worklog.md:107-114`** — Events Haiku bulk drift audit returned NO-GO (borderline). Five escalation paths queued. Subject-selection drift on `TRAVELS_TO` / `TRAVELS_WITH` / `LOCATED_AT` is the concrete blocker.
- **`worklog.md:116-118`** — 3 gated core-cleanups await Matt's sign-off: (1) drop 2 `cersei↔tyrion` LOVES mis-types; (2) retype ~22 physical `ASSAULTS`→`ATTACKS` (`ASSAULTS` is sexual-only per `architecture.md:233`); (3) merge-time `OWNS→BONDED_TO` for direwolf/dragon targets.
- **`worklog.md:150-153`** — Storage format open question (graph DB vs markdown): *"Leaning: Start with pure markdown. The context base pattern works well for agentic access."*
- **`worklog.md:160-163`** — Descriptive Chapter Title Mapping (POV-identity overlay; same family as Reek/Alayne): *"AFFC and ADWD use descriptive chapter titles (THE PROPHET, REEK, THE UGLY LITTLE GIRL) that map to known characters. Should the extraction system normalize these to the character's real name or preserve the title?"*
- **`architecture.md:560`** — Edge polish phase explicitly deferred: *"semantically-equivalent variants that crept in via different infobox fields … get reviewed and merged by an agent reasoning step. That review happens AFTER all wiki ingestion completes — not during."*
- **`working/todos.md:203`** — Chronology-extractor stub: *"Plan: build `chronology-extractor` agent that ingests year pages and emits `OCCURRED_IN_YEAR(<event>, <year>)` and `PRECEDES`/`FOLLOWS` edges."* 2,245 events extracted from year pages await a v2 temporal-edges schema.

### 6.10 `reference/foreshadowing-events.md` — pre-modeled events

The foreshadowing file pre-models 26 events + 15 Chekhov's guns as named entities (each gets a numbered heading, location, "scan for" list). Reserved for Pass 4 (the foreshadowing-scanner agent), but the structure is **the project's most explicit prior art for "events are first-class nodes."**

`reference/foreshadowing-events.md:68-82` — Red Wedding entry:

> ### 11. The Red Wedding
> - **Event:** Walder Frey and Roose Bolton massacre Robb Stark, Catelyn, and the Northern army at Edmure's wedding
> - **Location:** ASOS, Catelyn VII
> - **Scan for:** (MASSIVE foreshadowing catalogue) — Guest right emphasized throughout the series, The Freys' anger at Robb breaking his marriage pact, …

The "Event" field nominates *both* `Walder Frey` and `Roose Bolton` as agents and *both* `Robb Stark` and `Catelyn` and "the Northern army" as victims. **Multi-participant by design** — but this is human-authored prose, not encoded as an event-node or as edges.

`graph/nodes/events/red-wedding.node.md` exists (an `event.battle` node) — but its `## Edges` section has only 3 outbound edges:
```
- FIGHTS_IN: War of the Five Kings (track_b: Conflict)
- DEFEATS: Iron Throne (track_b: Result)
- DEFEATS: Warden of the North (track_b: Result)
```

No `KILLS robb-stark`, no `KILLS catelyn-stark`, no `OFFICIATES walder-frey`, no `LOCATED_AT the-twins` on the event node. The Red Wedding node exists but is **structurally empty for n-ary purposes.** All the killing happens on character-to-character edges scattered across 5 different chapter files.

---

## 7. Miscellaneous

### 7.1 The `_conflicts/` quarantine

`graph/nodes/_conflicts/` holds ~230 timestamped files like `jon-snow-characters-house-stark-h-q-2026-04-26T22-17-05.node.md`. These are second-or-later Pass 2 promotions that detected a slug collision with an already-promoted node. The promoter quarantines instead of overwriting. The canonical Jon Snow node lives in `graph/nodes/characters/jon-snow.node.md`; the `_conflicts/` variant is a duplicate-ingest artifact.

### 7.2 Some event-typed nodes are POV-chapter-style entries (category drift)

`ls graph/nodes/events/` reveals slugs like `alayne-i-the-winds-of-winter`, `arianne-i-the-winds-of-winter`, `barristan-i-the-winds-of-winter`. These look like **chapter-like POV entries** that got classified as events. The collaborator should expect some category drift in `event.*` (`structure.md` §6).

### 7.3 Wiki cache is local and complete

The entire AWOIAF wiki (17,945 pages, 377 MB) is cached locally at `sources/wiki/_raw/` (gitignored). Pass 2+ pipelines read from this cache. **Re-fetching is forbidden** by hard rule (`CLAUDE.md:21-28`). One exception was approved 2026-04-30 for a MediaWiki categories backfill (categories were stripped by the original `action=parse` API).

### 7.4 Confidence tier mismatch

Architecture defines Tier 1 (Verified Canon) through Tier 5 (Crackpot). The canonical `edges.jsonl` has only Tier 1 rows. The gated Events Haiku bulk uses Tiers 1 and 2 (`data.md` §10). No Tier 3+ edges exist in the data layer yet.

### 7.5 The dual edge representation

Every node has a `## Edges` markdown bullet section (display names, with `[AGoT]` / `[ADwD]` temporal-scope brackets). The canonical edges live in `edges.jsonl` (sluggified, with `qualifier` / `evidence_ref`). **The two are NOT auto-synced.** Per `structure.md` §3b: *"The JSONL is the canonical store."* The per-node bullets are for readers.

### 7.6 Mid-flight gated promotion chain

A 7-step promotion chain for the Events Haiku bulk is currently halted at step 1 (`progress/continue-prompts/2026-05-31-events-v2-promotion-chain/`) awaiting Matt's escalation pick. Five paths in `cross-model-audit.md §6`. Per `worklog.md:248`, *"Matt picks one of the 5 escalation paths in `cross-model-audit.md §6`: (A) re-run on Sonnet (~$340), (B) promote long-tail-only, (C) Sonnet-filter named-type rows only (~$2-5, **audit's recommendation**), (D) tighten Haiku prompt to v6 + re-run, (E) abandon Events for v2.0; wait for Dialogue."*

### 7.7 What this report did NOT inventory

- The 28 agent definition files in `.claude/agents/` beyond the four most-relevant prompts (mechanical-extractor, prose-edge-classifier, wiki-ingester, voice-analyzer). The auditing agents (`contradiction-surfacer`, `orphan-edge-finder`, `schema-drift-auditor`) and the staged Stage-4 helpers (`disambiguation-resolver`, `multi-type-entity-resolver`, etc.) are not deeply quoted.
- The 132 Python scripts beyond the stage4-core family. Many are one-off audit / migration scripts.
- Pass 1 extraction output details beyond one Red Wedding chapter sample.
- The wiki cache structure itself.
- The 21 pytest files in `tests/`.
- The 81+ session-detail narrative files (only a handful quoted in §6).


---

## Appendix A: Raw Schema Dumps (verbatim)

### A.1 — `reference/architecture.md` Edge Types (verbatim, lines 130–399)

The taxonomy below is reproduced **exactly** as it appears in the source file. No paraphrase, no edit. Every edge type in the master vocabulary is present.

## Edge Types (Relationship Categories)

Edges connect nodes in the graph. Every edge must have:
- `type` — from the taxonomy below
- `source` / `target` — the two nodes
- `first_available` — spoiler gate
- `evidence` — chapter citation or wiki source
- `confidence` — tier 1-5

### Design Principles

The v1 AGOT extractions organically produced ~127 ad-hoc relationship labels. The wiki infobox fields surface another ~40 structured relationship types. This taxonomy normalizes both into a controlled vocabulary that is **specific enough to be queryable** but **general enough to avoid synonyms** (e.g., one `SERVES` rather than SERVES / SERVED_BY / CLAIMS_TO_SERVE / SWORN_TO all meaning slightly different things).

When an extraction or wiki field doesn't fit an existing edge type, add a new one to this taxonomy rather than forcing a bad fit. Edge types are cheaper than lost information.

**When this taxonomy is used:** This controlled vocabulary is for the **graph layer** (building nodes and edges in `graph/`), the **wiki ingestion pass** (Pass 2), and any **downstream analytical passes**. Pass 1 (mechanical extraction) records relationships in free-text natural language in its Relationships Observed table — it does NOT need to use these labels. The normalization from free-text → controlled vocabulary happens when graph edges are built from extraction outputs.

**Qualifier enums for Tier-1/Tier-2 edge types:** see `reference/edge-qualifier-vocab.md`. Eight types require a `qualifier` field (Tier 1: SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO); nine types allow an optional qualifier (Tier 2: BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH, DECEIVES, REVEALS_TO, ATTACKS, GUEST_OF, IN_LAW_OF). All other edge types must NOT carry a `qualifier` field.

### Kinship & Family

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `PARENT_OF` | Biological or adoptive parent | Parent → Child | Father, Mother |
| `SIBLING_OF` | Brother/sister (full, half, or step — note which in metadata) | Symmetric | — |
| `SPOUSE_OF` | Married to (note if current, former, or annulled) | Symmetric | Spouse, Spouses |
| `BETROTHED_TO` | Engaged/promised in marriage | Symmetric | — |
| `LOVER_OF` | Romantic/sexual relationship outside marriage | Symmetric | Lover, Lovers |
| `WARD_OF` | Fostered by / raised by (not biological parent). Reverse-direction `FOSTERED_BY` (Guardian → Ward) is permitted and semantically equivalent — same pattern as HELD_BY for HOLDS_TITLE. | Ward → Guardian | — |
| `ANCESTOR_OF` | Distant lineage (more than one generation) | Ancestor → Descendant | Dynasty |
| `HEIR_TO` | Designated or expected successor (person → person or person → title) | Heir → Holder | Heir, Heirs |
| `CADET_BRANCH_OF` | Junior house derived from senior house | Cadet → Parent House | Cadet branches |
| `MARRIES_OFF` | Parent / overlord / king arranges a marriage for another person — distinct from `SPOUSE_OF` (the marriage itself); captures the arranger's agency as a political instrument | Arranger → Married-off person | — |
| `UNCLE_OF` | One-generation kinship shortcut: parent's sibling. Captures uncle/aunt without forcing two-hop traversal through the missing/inferred parent. Use when prose explicitly says "his uncle X" / "her aunt Y". | Uncle/Aunt → Nephew/Niece | — |
| `NEPHEW_OF` | Reverse of `UNCLE_OF` — emitted on the nephew/niece node pointing to the uncle/aunt. Same one-hop kinship shortcut. | Nephew/Niece → Uncle/Aunt | — |
| `COUSIN_OF` | Symmetric kinship shortcut for cousins (children of siblings). Captures first/second/etc. cousins without traversing two PARENT_OF + one SIBLING_OF. Use when prose explicitly says "his cousin X" / "her cousin Y". Especially common in Frey, Lannister, Tully, Tyrell, Targaryen families. | Symmetric | — |
| `MILK_BROTHER_OF` | Symmetric kinship: characters who shared a wet-nurse. Real Westerosi cultural category (Edric Dayne and Jon Snow, Robert Baratheon and Ned Stark per fostering customs). Distinct from SIBLING_OF (no blood) and FOSTERED_BY (institutional). | Symmetric | — |
| `NURSED_BY` | Child was wet-nursed by this person. Reverse is `WET_NURSE_OF`. Distinct from PARENT_OF; captures the lifelong attachment ASOIAF treats as significant (Wylla nursing Edric, Catelyn re Jon's nurse, etc.). | Child → Nurse | — |
| `WET_NURSE_OF` | Reverse of NURSED_BY — emitted on the nurse's node pointing to the child she nursed. | Nurse → Child | — |
| `COURTS` | Active suitor relationship — pre-betrothal pursuit of marriage. Distinct from `BETROTHED_TO` (formal engagement) and `LOVER_OF` (sexual/romantic). Use when prose describes someone as a "suitor" / "sought her hand" / "courted." Common pattern: Lysa Arryn's suitors after Jon Arryn's death; Rohanne Webber's suitors; Sansa pre-marriage. | Suitor → Object-of-courtship | — |
| `PROPOSED_AS_BRIDE` | A third party proposes a specific woman as a bride for a specific man (or for a Throne-political match). Distinct from `MARRIES_OFF` (the actual arrangement of an executed marriage) and `BETROTHED_TO` (formalized engagement). Captures the diplomatic-offer stage common in Westerosi succession politics. | Proposer → Proposed bride | — |
| `STEP_PARENT_OF` | Step-parent to a step-child — a marital-consequence relation distinct from `PARENT_OF` (biological/adopted) and `WARD_OF` (institutional fostering). Use when prose explicitly says "stepmother", "stepfather", or structurally implies a step-parental relationship via a parent's marriage. Reverse is `STEP_CHILD_OF`. | Step-parent → Step-child | n/a (marital-consequence relation) |
| `STEP_CHILD_OF` | Reverse of `STEP_PARENT_OF` — emitted on the step-child's node pointing to the step-parent. | Step-child → Step-parent | n/a |
| `IN_LAW_OF` | Marriage-affinity relationship between two people connected by the marriage of a third. Symmetric. Covers "good-mother", "good-father", "good-sister", "good-brother", "mother-in-law", "sister-in-law", etc. Distinct from `SPOUSE_OF` (the marriage itself), `SIBLING_OF` (blood/milk/step), `PARENT_OF` (parentage). Use when a two-hop traversal (SPOUSE_OF + PARENT_OF + invert) would lose the named in-law relationship known from prose. Optional qualifier enum: see `reference/edge-qualifier-vocab.md`. | Symmetric | corpus (97 "good-mother/good-father/mother-in-law" mentions) |

### Political & Authority

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `RULES` | Holds authority over a location or domain | Ruler → Location | Ruler, Head |
| `OVERLORD_OF` | Feudal superior of a house or lord | Overlord → Vassal | Overlord, Overlords |
| `SWORN_TO` | Feudal allegiance (house-to-house or person-to-house) | Vassal → Lord | Allegiance, Allegiances |
| `COMMANDS` | Military or organizational command | Commander → Subordinate | — |
| `SERVES` | Service relationship (broader than feudal — includes maesters, squires, servants) | Server → Served | — |
| `ADVISES` | Counsel relationship (Hand, maester, septa) | Advisor → Advised | — |
| `HOLDS_TITLE` | Person holds a named office or title | Person → Title | Titles, Title, Office |
| `HELD_BY` | Reverse of `HOLDS_TITLE` — emitted on title nodes pointing to the people/houses who have held the title | Title → Person/House | — |
| `SUCCEEDS` | Succeeded someone in a role or position | Successor → Predecessor | Successor, Predecessor |
| `CLAIMS` | Asserts right to a title, throne, or domain (may be contested) | Claimant → Claimed | — |
| `APPOINTS` | Grants a position or authority to someone | Appointer → Appointed | — |
| `DEPOSES` | Removes someone from power | Deposer → Deposed | — |
| `VOWS_TO` | Personal named oath made to another (distinct from `SWORN_TO`, which is structural feudal allegiance) — e.g., Brienne's vow to Catelyn, Jaime's vow to Catelyn, Arya's prayer list | Vow-maker → Recipient | — |
| `BREAKS_VOW` | Breaking of a personal vow or sworn oath — paired with `VOWS_TO` / `SWORN_TO` to track oath-keeping arcs (Jaime breaking Kingsguard oath by killing Aerys; Theon breaking foster-bond to Robb; etc.) | Vow-breaker → Vow-recipient | — |
| `BANISHES` | Political or royal act of exile — casting a person out of a domain, court, or realm. Distinct from `IMPRISONS` (confinement) and `DEPOSES` (removal from power without necessarily expelling). Captures Euron banishing Balon, court banishments, and exile-sentences issued by rulers. Tier-3 (no qualifier; destination is a separate temporal LOCATED_AT). | Banisher → Banished-person | corpus |

### Factional & Diplomatic

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `MEMBER_OF` | Belongs to a faction, order, or organization | Person → Faction | — |
| `FOUNDED` | Created or established an organization, house, or institution | Founder → Founded | Founder, Founded |
| `ALLIES_WITH` | Alliance (note if temporary, forced, or strategic) | Symmetric | — |
| `OPPOSES` | Active opposition or enmity | Symmetric | — |
| `MANIPULATES` | One party unknowingly used by another. Note mechanism in `notes` when known (e.g., `via bribe`, `via flattery`, `via false information`). | Manipulator → Target | — |
| `BETRAYS` | Broke faith, oath, or alliance | Betrayer → Betrayed | — |
| `NEGOTIATES_WITH` | Diplomatic engagement (may not result in alliance) | Symmetric | — |
| `CONTRACTED_WITH` | Formal contractual or commissioned engagement — distinct from `ALLIES_WITH` (political alliance), `SERVES` (employer-employee state), `NEGOTIATES_WITH` (diplomatic, may not conclude). Use when a party hires/commissions another for a specific service: hiring the Faceless Men for an assassination, contracting a sellsword company, commissioning a maester for a specific task. | Contractor → Contracted party | — |
| `CONSPIRES_WITH` | Secret joint plot — two or more parties engaged in a covert scheme together. Distinct from `ALLIES_WITH` (open political alliance) and `NEGOTIATES_WITH` (diplomatic engagement). Covers the Tyrell-Lannister Joffrey-poisoning conspiracy, Arianne's Queenmaker plot, the Grand Northern Conspiracy, and any secret-pact variant where the alliance must be concealed. Symmetric. Tier-3. | Symmetric | corpus |

### Military & Conflict

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FIGHTS_IN` | Participates in a battle, war, or tournament as a combatant. | Person → Event (battle/war/tournament) | — |
| `COMMANDS_IN` | Holds command role in a battle or war (note which side) | Person → Event/War | — |
| `PART_OF` | Battle or sub-event is a component of a larger war | Battle → War | Conflict, Battles |
| `KILLS` | Directly causes death | Killer → Killed | — |
| `KILLED_BY` | Reverse of `KILLS` — emitted on victim nodes pointing to killer | Killed → Killer | — |
| `EXECUTES` | Formal/judicial killing | Executor → Executed | — |
| `CAPTURES` | Takes prisoner | Captor → Captive | — |
| `PRISONER_OF` | Held captive by | Prisoner → Captor | — |
| `BESIEGES` | Conducts siege of a location | Besieger → Location | — |
| `DEFEATS` | Wins against in battle or conflict | Victor → Defeated | Result |
| `DUELS` | Single combat | Symmetric | — |
| `POISONS` | Killing or attempted-killing via poison — narrower than `KILLS` because method matters narratively (whodunnit plots, named poisons like the strangler, tears of Lys) | Poisoner → Poisoned | — |
| `RANSOMS` | Pays or negotiates for a captive's release — distinct from `CAPTURES` (the taking) and `PRISONER_OF` (the state) | Ransomer → Captive | — |
| `PRISONER_EXCHANGE_FOR` | Symmetric body-for-body prisoner swap (or proposed swap) between two captives held by opposing sides. Distinct from `RANSOMS` (one-direction payer → captive: gold/concession for release) — the anchor difference is two captives exchanged rather than payer + captive. Examples: Robb's proposed Robett ↔ Martyn Lannister; the proposed Theon ↔ Stark-girls swap; Edmure ↔ Cleos Frey-class swaps. Tier-3 (no qualifier). | Symmetric (captive ↔ captive) | — |
| `IMPRISONS` | Holds a captive in named confinement (cell, dungeon, tower) — distinct from `CAPTURES` (battlefield event) and `PRISONER_OF` (the captive's state); captures the institutional/judicial act of confinement, e.g., Cersei imprisoning Tyrion in the Red Keep after Joffrey's death (he was already at court, not captured) | Imprisoner → Imprisoned | — |
| `GUARDS` | Physical custody of a subject by a custodian — encompasses both protective custody (Kingsguard→King; bloodriders→Khal; sworn-shield→ward) AND custodial confinement (gaoler→prisoner; jailer→captive). Distinct from `PROTECTS` (beneficiary axis — acts for the target's benefit) and `IMPRISONS` (judicial/decisional confinement — typically lord-issued; `GUARDS` is the day-to-day executor of custody). When both protection AND confinement apply (Hound holding Arya), emit `GUARDS` alongside `PRISONER_OF` and/or `PROTECTS` as the prose warrants. Tier-3 (no qualifier). | Custodian → Subject-of-custody | — |
| `KILLED_WITH` | Combat death attributed to a specific named artifact — mirror of `EXECUTED_WITH` for non-judicial battlefield deaths. Use when prose names the weapon as agent of death ("slain by Orphan-Maker", "took an arrow from Ice"). Coexists with `KILLED_BY person` — the person did the killing, the artifact was the instrument. | Victim → Artifact | — |
| `KNIGHTED_BY` | Granted knighthood by another knight or lord. Distinct from `TUTORS` (skill transfer over time) and `APPOINTS` (political office). Use when prose explicitly describes the dubbing/knighting. | Knight → Dubber | — |
| `BESTOWS_KNIGHTHOOD_ON` | Reverse of `KNIGHTED_BY` — emitted on the dubber's node. | Dubber → Knight | — |
| `ATTACKS` | Generic physical violence — combat-style attack, creature attack, or person-on-person aggression that does NOT necessarily result in death (use `KILLS`/`POISONS`/`EXECUTES` if death; `DUELS` if formal mutual combat). Covers creature attacks (eagle on warg, direwolf on attacker), unprovoked violence (Darkstar slashing Myrcella, the Mountain striking Loras's horse), assault in the non-sexual sense. Includes both character→character and creature→character. For sexual violence specifically, use `ASSAULTS`. | Attacker → Target | — |
| `ASSAULTS` | Sexual violence — rape, attempted rape, or sexual assault. Distinct from `ATTACKS` (physical violence, non-sexual). Use only when prose makes the sexual nature explicit. Examples: Gregor Clegane & the five Bracken sisters during the Burning of the Riverlands; Owen Inchfield + Raymun Fossoway attempting Brienne; the canonical Gregor wartime pattern. | Assailant → Victim | — |
| `PARTICIPATES_IN` | Active non-combat involvement in a named event — logistical, administrative, organizational, or supportive role. Distinct from `FIGHTS_IN` (combatant), `ATTENDS` (guest/witness/audience), `COMMANDS_IN` (command-tier role). Examples: Medrick Manderly transporting men to the Wall during the Hour of the Wolf; quartermasters in named battles; logistical participants in coronations/kingsmoots/sieges who are not officiants. | Person → Event (`event.*`) | — |
| `RESCUES` | Dramatic single-moment extraction from danger — rescuer saves the target from death, capture, or peril. Distinct from `PROTECTS` (steady-state guardianship) and `HEALS` (medical restoration). Covers Beric rescuing BWB members, Davos rescued by Salladhor, Sam & Gilly rescued by the Mysterious Rider, Jon rescuing Ghost from wildlings. Tier-3 (no qualifier). | Rescuer → Rescued-person | corpus |
| `TORTURES` | The act of inflicting deliberate physical pain — flaying, racking, burning, or other sustained bodily torment. Distinct from `ATTACKS` (generic physical violence; not necessarily sustained or systematic), `ASSAULTS` (sexual violence specifically), `EXECUTES` (formal death sentence), and the `REVEALS_TO=under_torture` qualifier (which captures the informational *effect* of torture, not the act itself). Major narrative thread: Bolton flaying tradition, Mountain at Harrenhal, Qyburn's "studies", the Bloody Mummers, Black Cells. Without this edge, "who has Ramsay tortured?" cannot be graph-answered. Tier-3 (no qualifier; method is sub-typology the narrative captures). | Torturer → Tortured-person | corpus |

### Knowledge & Information

> **Deprecated (Session 63, 2026-05-21):** `KNOWS` was removed from the active vocabulary. Stage 4 wiki-prose classification ran an 82.3% fallback rate on KNOWS emits — the semantic boundary ("knows of" vs "met once" vs "heard rumor of") is too blurry for prose-derived classification to enforce. Character-knowledge relationships will be derived from a future Pass-1-based chapter co-occurrence + Information Revealed pass. Existing KNOWS edges in the graph (363 Haiku-emit + 21 Sonnet-control-arm) are preserved as historical record; downstream consumers filter deprecated types on read.

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `IGNORANT_OF` | Critically lacks information that the reader or other characters have | Person → Information | — |
| `SEEKS` | Pursuing knowledge, artifact, or person | Seeker → Sought | — |
| `REVEALS_TO` | Discloses information to another | Revealer → Recipient (note what was revealed) | — |
| `DECEIVES` | Deliberately misleads | Deceiver → Deceived (note the deception) | — |
| `DECEIVED_BY` | Reverse of `DECEIVES` — emitted on target nodes pointing to deceiver | Deceived → Deceiver | — |
| `HOARDS` | Institution or person suppresses knowledge | Hoarder → Knowledge | — |
| `INVESTIGATES` | Actively trying to learn or prove something | Investigator → Subject | — |
| `TEACHES` | Transmits knowledge or skill (general/casual instruction) | Teacher → Student | — |
| `TUTORS` | Sustained formal one-on-one mentorship — narrower than `TEACHES` (Syrio→Arya water-dancing, Cressen→Stannis childhood, Aemon→Sam ravenry, Septa Mordane→Sansa) | Tutor → Student | — |
| `HEALS` | Medical or maester treatment — restoration of body, not resurrection of the dead (which is `RESURRECTS`). Maester Luwin healing Bran after the fall; Aemon healing Sam; the unnamed septon healing Sandor. **Excludes:** Red Priests reviving the dead (use `RESURRECTS`); Qyburn's reanimation of the Mountain (use `RESURRECTS`) | Healer → Healed | — |
| `AFFLICTED_BY` | Character suffers from a named disease, condition, or magical affliction (living state). Target is `concept.medical`. Distinct from `KILLED_BY` (target = person), `DIED_AT` (location), `DIED_OF` (cause-of-death; this is the living state). Examples: Jorah Mormont/greyscale, Shireen Baratheon/greyscale, Stannis/burns. | Character → Medical | — |
| `DIED_OF` | Character's death was caused by a named disease/condition (post-mortem state). Target is `concept.medical`. Distinct from `KILLED_BY` (person-killer), `DIED_AT` (location), `EXECUTED_WITH` (judicial weapon). Mirrors `AFFLICTED_BY` for the post-mortem state. Examples: Hoster Tully/Spring Sickness, Albin Massey/Shivers, Medrick Manderly/Winter Fever, the Old King Jaehaerys/Great Spring Sickness. | Character → Medical | — |
| `SPIES_ON` | A spy or agent actively surveils, monitors, or gathers intelligence about the target. Distinct from `SERVES` (employment state) and `MANIPULATES` (wrong direction — spy works for handler, not against target). Westeros has structurally-distinct spy networks (Varys's little birds, Littlefinger's network, Qarth's whispers). Tier-3. | Person → Surveilled-person | n/a (Pass 1 corpus + Sonnet no-fit) |
| `INFORMS` | A spy, agent, or informant reports intelligence to their handler or spymaster. Complements `SPIES_ON` (target = person being watched vs. target = handler receiving reports). Distinct from `SERVES` (too generic) and `REVEALS_TO` (one-time disclosure; INFORMS is the ongoing reporting relationship). Tier-3. | Person → Handler/Spymaster | n/a (Pass 1 corpus + Sonnet no-fit) |

### Emotional & Perceptual

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `PERCEIVED_AS` | How POV Character X sees Character Y (with characterization notes) | Perceiver → Perceived | — |
| `TRUSTS` | Places confidence in | Truster → Trusted | — |
| `DISTRUSTS` | Lacks confidence in, suspects | Distruster → Distrusted | — |
| `RESPECTS` | Holds in high regard | Respecter → Respected | — |
| `FEARS` | Afraid of (person, faction, or thing) | Fearer → Feared | — |
| `LOVES` | Deep emotional attachment (familial, romantic, or platonic) | Lover → Loved | — |
| `HATES` | Deep enmity or loathing | Hater → Hated | — |
| `MOURNS` | Grieves for (dead person, lost thing) | Mourner → Mourned | — |
| `PROTECTS` | Acts as guardian or defender | Protector → Protected | — |
| `RESENTS` | Harbors bitterness toward | Resenter → Resented | — |
| `COMPANION_OF` | Close personal friendship or camaraderie. Distinct from `ALLIES_WITH` (political alliance), `TRUSTS` (one-direction confidence), `LOVES` (romantic/deep-familial), `RESPECTS` (cold regard). Use when prose explicitly names a friendship ("good friends with", "sworn brothers", "close companion"). Examples: Patrek Mallister & Edmure Tully; Robert & Ned in their youth; Brienne & Pod; Davos & Salladhor Saan. | Symmetric | — |
| `REPUTED_AS` | Collective reputation or general perception attached to a character without a specific perceiver — distinct from `PERCEIVED_AS` which requires a named POV. Target is `concept.*` (e.g., `concept.magic` for "reputed witch", `concept.craft` for "reputed swordsman", `concept.vice` for "reputed drunkard"). Use when prose narrates a public-domain reputation rather than one character's view of another. | Character → Concept | — |
| `ENCOUNTERS` | Plot-significant face-to-face meeting between two characters, anchored by explicit prose staging (verb gate enforced by validator per CRITICAL RULE — see classify prompt Rule 6). Reserved for first meetings, brief road-crossings, set-piece confrontations short of duel/combat where the meeting itself carries narrative weight. Examples: Dunk ↔ Egg at the Ashford inn; Brienne ↔ Randyll Tarly in AFFC; Arya ↔ Sandor on the kingsroad; Jon ↔ Mance at the Frostfangs; Sam ↔ Coldhands beyond the Wall. NOT for co-presence at events (use `LOCATED_AT` / `ATTENDS` / `FIGHTS_IN`), retinue/court presence (`TRAVELS_WITH`), or formal diplomatic engagement (`NEGOTIATES_WITH`). **Coverage scope (Session 63, 2026-05-21):** Stage 4 captures only wiki-prose-staged meetings — biographical-summary register often elides staging verbs even when meetings happened in-text. Comprehensive character-meeting coverage will come from a future book-derived pass; treat wiki ENCOUNTERS as partial-by-design. Tier-3 (no qualifier). | Symmetric (character ↔ character) | — |

### Spatial & Temporal

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `LOCATED_AT` | Entity at location (with book/chapter timestamp). Covers both event-at-place (battle location) and person-at-place (witness location). Deprecated synonym `LOCATED_IN` was emitted by an early parser variant; normalize on read. | Entity → Location | Location, Seat |
| `SEAT_OF` | Primary location of a house or faction | Location → House/Faction | Seat, Seats |
| `TRAVELS_TO` | Movement from one location to another | Traveler → Destination (note origin) | — |
| `TRAVELS_WITH` | Co-presence in someone's company, on the road OR in attendance at court/event. Covers both journeying together (Arya/Gendry/Hot Pie; Sam+Gilly+Aemon to Oldtown; Dunk+Egg) AND retinue/court presence (Robett kneeling among Catelyn's welcomers at Winterfell). Distinct from `COMPANION_OF` (sustained friendship), `ALLIES_WITH` (political), `MEMBER_OF` (faction affiliation), `SERVES` (subordination). Tier-3 (no qualifier). | Symmetric (character ↔ character) | — |
| `BORN_AT` | Birthplace | Person → Location | Born |
| `DIED_AT` | Place of death | Person → Location | Died |
| `BURIED_AT` | Place of burial or interment | Person → Location | Buried |
| `IMPRISONED_AT` | Captive's place of confinement during a specific imprisonment (cell, dungeon, sky cell, black cells, tower used as gaol, prison hulk). Distinct from `LOCATED_AT` (general presence — not captivity-marked), `IMPRISONS` (jailer→captive judicial relationship), and `PRISONER_OF` (captive↔captor symmetric state). Examples: Ned/Black Cells; Tyrion/Eyrie sky cell; Jaime/Robb's camp at Riverrun; Davos/Dragonstone dungeon. Tier-3 (no qualifier). | Captive → Location (`place.location`) | — |
| `CONTEMPORARY_WITH` | Events happen simultaneously or overlap in time | Symmetric | — |
| `REGION_OF` | Location belongs to a larger geographic region | Location → Region | Region, Regions |

### Possession & Ownership

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `WIELDS` | Currently bears or uses a weapon/artifact. **Target MUST be `object.artifact`** — animals (mounts, ravens, dragons) use `OWNS` or `BONDED_TO`, never `WIELDS`. | Person → Artifact | — |
| `OWNS` | Possesses (broader than wields — castles, ships, animals) | Owner → Owned | Owner, Owners |
| `ANCESTRAL_WEAPON_OF` | Valyrian steel sword or other hereditary weapon of a house | Weapon → House | Ancestral weapon |
| `FORGED_BY` | Creator/smith of an artifact (the person/group who made it). **NOT for material composition** — use `MADE_OF` for substance/material relationships. | Creator → Artifact | — |
| `MADE_OF` | Artifact is composed of a material (Valyrian steel, dragonglass, dragonbone, weirwood, etc.). Distinct from `FORGED_BY` (smith). | Artifact → Material (`object.material`) | — |
| `LOOTED_BY` | Artifact taken by force or conquest from prior holder. Distinct from `OWNS` (steady state). Captures the transactional moment. | Artifact → New holder | — |
| `REFORGED_INTO` | Original artifact materially transformed into a new artifact (or multiple). The original ceases to exist; the new artifact(s) inherit material and lineage. | Original artifact → Resulting artifact | — |
| `GIFTED_TO` | Deliberate voluntary transfer of an artifact from one person to another as gift or honor. Distinct from `OWNS` (state) and `INHERITED_BY` (death-succession). Note giver in qualifier. | Artifact → Recipient | — |
| `INHERITED_BY` | Artifact passed via inheritance from deceased holder to heir. | Artifact → Heir | — |
| `WIELDED_IN` | Artifact was used in a named event (battle, execution, ritual). Distinct from `WIELDS` (person → artifact possession state). Enables artifact-history queries. | Artifact → Event | — |
| `EXECUTED_WITH` | A specific person was executed with a specific weapon (poetic-detail edges: Eddard executed with Ice, etc.). May overlap with `WIELDED_IN` + `EXECUTES`; kept distinct for narrative-precision queries. | Victim → Weapon | — |
| `PURCHASED_FROM` | Transactional acquisition of an artifact (or service) via purchase — distinct from `OWNS` (steady state), `GIFTED_TO` (voluntary transfer), `LOOTED_BY` (taken by force), `INHERITED_BY` (death-succession). Captures the transactional moment + the seller. Examples: Dunk purchasing the dragon-of-Pentos shield from Pate the Old; ship-passage purchases (when concretely named); merchant exchanges that are plot-significant. | Buyer → Seller | — |
| `BUILT` | Character physically built or oversaw the construction of a named structure (castle, tower, sept, wall, monument). Distinct from `FOUNDED` (scoped to organizations/houses/orders) and `OWNS` (steady state). Use when prose explicitly names the builder of a place. Examples: Brandon-the-Builder/The Wall, Brandon-the-Builder/Storm's End (legend), Lord-Triston-Hightower/Starry-Sept. | Builder → Structure (`place.location`) | — |
| `CAPTAIN_OF` | Character is captain (master/commander) of a named vessel. Target MUST be `object.artifact` (the vessel). Distinct from `COMMANDS` (military org) and `OWNS` (ownership state — captains may or may not own the vessel). Examples: Davos Seaworth/Black Betha, Victarion Greyjoy/Iron Victory, Asha Greyjoy/Black Wind, Salladhor Saan/Valyrian. | Captain → Vessel (`object.artifact`) | — |
| `CREW_OF` | Character serves as a crew member (non-captain) of a named vessel — sibling to `CAPTAIN_OF`. Target MUST be `object.artifact` (the vessel). Use when prose explicitly names a non-captain role (oarsman, first mate, ship's cook, sail-master). Captain → use `CAPTAIN_OF`. Generic faction membership → use `MEMBER_OF`. Note specific role in `notes` if known ("first mate"). | Crew member → Vessel (`object.artifact`) | — |

### Identity & Disguise

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `ALIAS_OF` | Known by another name | Alias → True Identity | Alias, Aliases |
| `DISGUISED_AS` | Actively pretending to be someone/something else | Person → Disguise Identity | — |
| `SAME_AS` | Two references that resolve to the same entity (for cross-identity matching) | Symmetric | — |
| `IMPERSONATES` | Pretending to be a specific other person | Impersonator → Impersonated | — |

### Magic & Supernatural

> These edges capture relationships that involve magical, ritual, or supernatural agency — distinct from in-world physical relations. ASOIAF has rich magical systems (warging, R'hllor blood magic, Faceless-Men identity-transfer, weirwood-bonding, dragon-bonding, resurrection, curse-laying) that infobox extraction cannot reach. These types are *prose-derived only* — the wiki-infobox parser does not emit them.

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `WARGS_INTO` | A warg / skinchanger actively occupies the consciousness of an animal or person — e.g., Bran into Summer / Hodor / the heart tree; Arya into Nymeria (dream-skinchange); Varamyr into his wolf / eagle / shadowcat; Orell into his eagle; Jon (low-key) into Ghost | Warg → Vessel | — |
| `BONDED_TO` | Static magical bond between two beings — broader and more permanent than `WARGS_INTO` (which is the active occupation moment). Covers dragon-rider bonds (Daenerys ↔ Drogon, etc.), warg-animal lifelong pairing (Bran ↔ Summer when not actively warging), weirwood-bond (Bran ↔ his three-eyed-crow / weirwood network) | Symmetric | — |
| `SACRIFICES` | Deliberate ritual or magical killing with supernatural/symbolic purpose — distinct from `KILLS` (combat) and `EXECUTES` (judicial). Mirri Maz Duur sacrificing Drogo's life-essence; Daenerys sacrificing her unborn child to magic the dragon eggs; Stannis (via Melisandre) sacrificing Edric Storm's leech-blood / Mance / Penny's brother / (theory-tier) Shireen; Craster sacrificing his sons to the Others | Sacrificer → Victim | — |
| `RESURRECTS` | Returns the dead to life via supernatural means — distinct from `HEALS` (medical), distinct from `KILLED_BY` (semantic reverse). Thoros of Myr resurrects Beric Dondarrion (multiple times); Beric resurrects Catelyn → Lady Stoneheart (ASOS Epilogue); Coldhands resurrected by unknown force (Children?); Patchface drowned-and-returned; Qyburn reanimates the Mountain; Red Priests broadly perform this (Thoros, Moqorro) — `HEALS` is for body-restoration, `RESURRECTS` is for death-reversal | Resurrector → Resurrected | — |
| `CURSES` | A character or magical force lays a curse — Mirri Maz Duur's "when the sun rises in the west" curse on Daenerys; Maggy the Frog's Valonqar prophecy-curse on Cersei; the Curse of Harrenhal (collective); Night's King lore | Curser → Cursed | — |
| `PRACTICES` | Character actively practices a named magical or ritual discipline. Target is `concept.magic` (or `concept.craft` for non-magical-but-named-discipline cases). Distinct from `WARGS_INTO` (active occupation moment), `BONDED_TO` (static pairing), `WORSHIPS` (religious devotion, not the magical practice itself), `CLERGY_OF` (religious office). Examples: Melisandre/shadow-binding, Mirri Maz Duur/maegi-blood-magic, Bran/greendreams, faceless-men/identity-transfer, Qyburn/necromancy. | Character → Magic discipline | — |

### Cultural & Religious

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `CULTURE_OF` | Person belongs to a cultural group | Person → Culture | Culture, Race |
| `WORSHIPS` | Follows or serves a deity/religion | Person → Religion | Religion |
| `SACRED_TO` | Location or artifact is holy to a religion | Entity → Religion | — |
| `CLERGY_OF` | Serves as religious official | Person → Religion | — |
| `OFFICIATES` | Character performs the ritual / religious / ceremonial role at a named event (weddings, funerals, coronations, kingsmoots, namedays, knighting ceremonies). Distinct from `CLERGY_OF` (general clergy status, target = religion) and `ATTENDS` (guest/witness). Target is `event.*` or specific named ceremony node. Examples: Melisandre/wedding-of-sigorn-and-alys-karstark; the High Septon/coronation-of-tommen-i; Aeron Damphair/kingsmoot-of-299-ac. | Character → Event | — |
| `NAMED_AFTER` | An entity was given its name in honor of, or as a reference to, another entity. Captures Westeros's pervasive dynastic name-recycling culture (Rickard Karstark named for Rickard Stark, the many Brandons and Aegons). Distinct from `ALIAS_OF` (a different name for the same entity), `SAME_AS` (identity-resolution), and `DEPICTED_IN` (in-world legend about a person). One-sided: the named entity points to its namesake. Surfaced in Sonnet `no-fitting-type` rejections. Tier-3 (no qualifier). | Entity → Namesake-entity | wiki (dynastic naming patterns) |

### Narrative & Literary

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `DEPICTED_IN` | Character is the subject of an in-world text/song/ballad/tale (Danny Flint → "Brave Danny Flint" song, Florian → Florian-and-Jonquil tales). Distinct from `WRITTEN_BY` (author → work). Captures the in-universe legacy/folklore layer. | Character → Text | — |

*continued:*

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FORESHADOWS` | Detail A is a Chekhov's gun for Event B | Detail → Event | — |
| `PARALLELS` | Event/character A mirrors Event/character B thematically | Symmetric | — |
| `SUBVERTS` | Event A inverts the expectation set by B | Subverter → Subverted | — |
| `ECHOES` | Weaker than PARALLELS — structural or verbal similarity without full thematic mirroring | Echo → Source | — |
| `CONTRASTS` | Deliberate opposition in characterization, situation, or outcome | Symmetric | — |
| `WRITTEN_BY` | Authorship of an in-world text (book, song, decree, letter) | Text → Author | Written by |

### Prophecy

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FULFILLS` | Event fulfills prophecy (confirmed) | Event → Prophecy | — |
| `APPEARS_TO_FULFILL` | Possible fulfillment, may be red herring | Event → Prophecy | — |
| `SUBVERTS_PROPHECY` | Contradicts expected fulfillment | Event → Prophecy | — |
| `PROPHESIED_BY` | Who made the prophecy | Prophecy → Prophet | — |
| `SUBJECT_OF_PROPHECY` | Person/event the prophecy is about | Person → Prophecy | — |
| `DREAMS_OF` | In-world prophetic or significant dream/vision about a person, place, event, or symbol. Distinct from `FORESHADOWS` (which is a reader-facing narrative-craft edge); `DREAMS_OF` is character-facing. Heavily concentrated in Bran (greendreams, three-eyed-crow), Daenerys (HotU visions), Jojen, and the Targaryen line (canonical prophetic-dreaming lineage) | Dreamer → Subject | — |

### Evidentiary (Theory Support)

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `SUPPORTS` | Textual passage supports a theory | Evidence → Theory | — |
| `CONTRADICTS` | Textual passage undermines a theory | Evidence → Theory | — |
| `CITED_BY` | Theory attributed to source theorist or community | Theory → Source | — |

### Causal & Plot

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `CAUSES` | Event A leads to Event B | Cause → Effect | — |
| `PREVENTS` | Action A blocks Event B | Preventer → Prevented | — |
| `ENABLES` | Condition A makes Event B possible | Enabler → Enabled | — |
| `MOTIVATES` | Event or condition drives a character's actions | Motivation → Actor | — |
| `TRIGGERS` | Immediate cause (narrower than CAUSES — the specific spark) | Trigger → Result | — |

### Hospitality & Custom

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `GUEST_OF` | Under someone's roof / protection by custom | Guest → Host | — |
| `VIOLATES_GUEST_RIGHT` | Broke the sacred hospitality compact | Violator → Victim | — |
| `GRANTS_SAFE_CONDUCT` | Promised safe passage | Grantor → Recipient | — |
| `ATTENDS` | Person present at a named event as guest, witness, or audience — not as combatant (`FIGHTS_IN`), commander (`COMMANDS_IN`), or organizer. Use for tourney spectators, wedding guests, feast attendees, court hearings. | Person → Event | — |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | Tournament champion crowns a chosen woman with the laurel wreath of Queen of Love and Beauty. Distinct edge because the act carries outsized narrative weight in ASOIAF (Rhaegar/Lyanna at Harrenhal as a war-trigger; Loras/Margaery; etc.) and chains to political consequences. Source = tournament champion; target = recipient. | Champion → Recipient | — |


---

### A.2 — `reference/edge-qualifier-vocab.md` (verbatim, in full)

# Edge Qualifier Vocabulary

> The Weirwood Network edge schema includes an optional `qualifier` field on emit_edge rows. Qualifier vocabulary is three-tiered:
> - **Tier 1 (REQUIRED enum)** — edge MUST emit a qualifier from the listed enum. Validator rejects empty or out-of-enum.
> - **Tier 2 (OPTIONAL enum)** — qualifier may be omitted; if emitted, must match the listed enum. Validator rejects out-of-enum but accepts omission.
> - **Tier 3 (no qualifier)** — DEFAULT for any edge type not listed in the table below. Edge MUST NOT have a `qualifier` field. Validator rejects any non-empty qualifier on Tier-3 edges.
>
> The `notes` field is **deleted from the schema entirely** as of 2026-05-18 (Session 57 lock). Validator rejects any edge carrying a `notes` field.

---

## Tier 1 — REQUIRED qualifier (8 edge types)

| Edge Type | Enum Values | Rationale | Data Source |
|-----------|-------------|-----------|-------------|
| `SIBLING_OF` | `full`, `half`, `step`, `milk`, `unknown` | Universal Westerosi kinship category. Corpus: half-brother ×44, half-sister ×9, milk-brother ×9, step- ×0. Step is included as a defensive option (Tommen/Robert via Cersei's prior marriage etc., though rare). | Pass 1 corpus + ASOIAF series knowledge |
| `SPOUSE_OF` | `current`, `former`, `annulled`, `widowed`, `salt_wife`, `unknown` | Four+1 canonical marital states. Corpus: widow* ×238, first/second/third wife ×92, former wife ×9. Wiki: salt wife ×5, dissolved ×3, annulled ×1, possibly ×6. `salt_wife` captures the Ironborn quaternary marital institution. | Wiki infobox + corpus |
| `PARENT_OF` | `biological`, `adopted`, `claimed`, `rumored`, `disputed`, `unknown` | Captures legitimacy / certainty states. Wiki: rumored ×34, disputed ×20, officially ×16, possibly ×13, adopted ×4. `biological` is the default; `claimed` covers Aegon-VI-Targaryen-style assertions; `rumored` covers folkloric attestation. WARD_OF/FOSTERED_BY are separate (fostering is not parentage). | Wiki infobox `Fathers`/`Mothers` plural fields + corpus |
| `WARD_OF` | `formal`, `informal`, `hostage`, `unknown` | Three distinct fostership states in Westerosi politics. Corpus: ward ×259, fostered ×47, hostage ×381. Hostage-as-ward is the dark form (Theon under Ned); formal = acknowledged fostership (Robert under Jon Arryn); informal = household upbringing without formal compact. | Pass 1 corpus + series knowledge |
| `HOLDS_TITLE` | `current`, `former`, `claimed`, `contested`, `historical`, `unknown` | Highest-volume qualifier-bearing field in wiki: 256 qualifier rows / 3976 edges. Wiki: formerly ×62, claimant ×57, historical ×35, stripped ×7, self-styled ×4, disputed ×3. `historical` (deep past Targaryens) ≠ `former` (recently-deposed); kept distinct per wiki convention. `claimed` covers all pretender/self-styled cases. | Wiki infobox (strongest signal) |
| `VOWS_TO` | `active`, `kept`, `broken`, `fulfilled`, `unknown` | Distinct lifecycle states of a personal oath. Corpus: vow ×369, broken vow ×13, fulfilled vow ×2, swore ×100. `active` is in-force (default); `kept` = honored over years; `broken` = violated; `fulfilled` = completed (Brienne returning Sansa). High narrative weight in ASOIAF (Brienne, Jaime, Arya, Sandor). | Pass 1 corpus |
| `MANIPULATES` | `via_bribe`, `via_flattery`, `via_false_information`, `via_threat`, `via_seduction`, `unknown` | Locked Session 55 — confirmed. Original mechanism enum that motivated the whole qualifier-vocab project. | Session 55 verdict |
| `SWORN_TO` | `current`, `former`, `deserted`, `by_marriage`, `claimed`, `unknown` | High-volume feudal allegiance type with rich qualifier surface in wiki. Wiki: formerly ×45, in death ×11, possibly ×9, deserted ×3, by marriage ×2, claimed ×2, annulled ×2. `deserted` captures Night's Watch oath-breakers; `by_marriage` captures fealty-via-spouse (Tully→Stark via Catelyn); `claimed` covers contested vassalage. | Wiki infobox |

---

## Tier 2 — OPTIONAL qualifier (9 edge types)

| Edge Type | Enum Values | Rationale | Data Source |
|-----------|-------------|-----------|-------------|
| `BETROTHED_TO` | `current`, `broken`, `fulfilled`, `secret`, `unknown` | Most betrothal-text is straightforward state-declaration (no qualifier needed). Optional to capture when narratively important. Corpus: betrothed ×335, broke betroth ×3. Pass 1 also showed `secret` betrothals (Robb-Jeyne-Westerling-style). | Pass 1 corpus + series knowledge |
| `LOVER_OF` | `current`, `former`, `secret`, `paramour`, `rumored`, `unknown` | Pass 1: former ×19, secret ×7, paramour ×7 in the relation column. Wiki: rumored ×36 (dominant), paramour ×4. `paramour` is the formal Westerosi term for an acknowledged extramarital partner (Ellaria, Bellegere); `rumored` covers the gossip-historical layer (Lyonel Strong / Rhaenyra). | Pass 1 corpus + wiki infobox |
| `KILLS` | `in_combat`, `in_duel`, `by_arrow`, `by_blade`, `by_ambush`, `by_proxy`, `by_creature`, `unknown` | Method matters narratively. Corpus: in combat ×117, in a duel ×4, ambush ×188, by proxy ×7, via creature ×14, beheaded ×290, stabbed ×147. `POISONS` is a separate edge type — do NOT fold into KILLS method. `by_creature` covers dragon-burning, wolf-killing, eagle-attack-causing-death. `by_proxy` covers catspaw-style indirect killing. | Pass 1 corpus full-text |
| `CONTRACTED_WITH` | `assassination`, `mercenary_service`, `ransom`, `safe_passage`, `construction`, `marriage_brokerage`, `espionage`, `unknown` | Service-type matters. Corpus: hired ×93, sellsword/mercenary ×398, assassinate ×160, ransom ×132, safe passage ×27. The Faceless Men, Golden Company, smaller free companies, ransom negotiations (Tyrion/Lannister deals), Tycho Nestoris's loans — distinct service categories. | Pass 1 corpus |
| `DECEIVES` | `by_lie`, `by_disguise`, `by_omission`, `by_false_witness`, `by_silence`, `unknown` | Method matters. Corpus: lie ×647, disguise ×208, false witness ×5. `by_omission` and `by_silence` are distinct narrative devices (Ned's silence on Jon's parentage). | Pass 1 corpus |
| `REVEALS_TO` | `voluntary`, `coerced`, `accidental`, `under_torture`, `unknown` | Disclosure conditions matter for trust/credibility scoring. Corpus: voluntarily ×25, under torture ×57, let slip ×10. | Pass 1 corpus |
| `ATTACKS` | `in_anger`, `unprovoked`, `in_self_defense`, `on_command`, `by_creature`, `unknown` | Motive context. Corpus: in anger ×23, on command ×19, self-defense ×2, unprovoked ×0 (concept exists; word doesn't). `by_creature` for direwolf/eagle/dragon attacks. Weaker empirical signal than other Tier-2 candidates — could drop to Tier-3 if Haiku smoke reveals it's never emitted. | Pass 1 corpus |
| `GUEST_OF` | `shelter`, `feast`, `bread_and_salt`, `safe_conduct`, `gift_exchange`, `refused`, `unknown` | Pass 1 explicitly types hospitality events. 680 rows across 344 chapters; top categories: shelter_offered ×235, feast_given ×85, gift_exchange ×46, safe_conduct ×27, bread_and_salt ×10. `bread_and_salt` is the formal compact (sacred); `shelter` is the common case; `refused` covers shelter_denied / refusal_to_host. Violations are captured by the separate `VIOLATES_GUEST_RIGHT` edge — do not fold into GUEST_OF qualifier. Hostage situations are captured by `PRISONER_OF`, not GUEST_OF. | Pass 1 `## Hospitality & Guest Right` table |
| `IN_LAW_OF` | `by_marriage_of_self`, `by_marriage_of_child`, `by_marriage_of_sibling`, `by_marriage_of_parent`, `unknown` | Marriage-affinity relationship. Symmetric. Sonnet's freeform-qualifier corpus has 97 mentions of "good-mother", "good-father", "good-sister", "good-son", "mother-in-law", "sister-in-law" — mostly in Reach noble-house arcs. Qualifier identifies *which marriage* created the affinity: `by_marriage_of_self` (you married their relative), `by_marriage_of_child` (your child married them or their relative), `by_marriage_of_sibling`, `by_marriage_of_parent`. The graph currently forces a two-hop traversal (SPOUSE_OF + PARENT_OF + invert) and gets nothing for cases where only the in-law link is known; `IN_LAW_OF` closes that gap. | Pass 1 corpus (3 P1 rows) + Sonnet freeform qualifier usage (97 mentions) |

---

## Tier 3 — NO qualifier (default for all other edge types)

All edge types NOT listed in Tier 1 or Tier 2 above are Tier 3. These edges emit no `qualifier` field and no `notes` field. The edge stands on its own: `source / edge_type / target / confidence_tier / evidence_snippet / evidence_kind`.

**Count check:** Tier 1 (8) + Tier 2 (9) + Tier 3 (~146) = ~163 total (matches architecture.md master vocab count as of Session 63, 2026-05-21 — after KNOWS deprecation).

---

## Validator rules (for HAIKU-CUTOVER STEP 3)

When `scripts/wiki-pass2-validate-edge-jsonl.py` is extended with qualifier enforcement (STEP 3), it must implement:

1. Load this file and parse the per-edge-type enum table into a `QUALIFIER_ENUM: {edge_type: (tier, frozenset(enum_values))}` lookup.
2. For each `emit_edge` row:
   - If `edge_type` is Tier 1: reject if `qualifier` is missing or not in enum.
   - If `edge_type` is Tier 2: accept if `qualifier` is absent; reject if present and not in enum.
   - If `edge_type` is Tier 3 (not listed above): reject if `qualifier` is present (any value).
   - Reject if `notes` field is present on any edge (field deleted from schema 2026-05-18).

---

### A.3 — Binary vs. event-like classification table (one row per edge type)

Per the brief's test:
- **binary** = exactly 2 participants, fixed roles, no time/place/outcome on the edge, can't sensibly carry a third participant.
- **event-like** = >2 plausible participants OR carries its own properties OR has distinct typed roles.
- **ambiguous** = could be argued either way.

`temporal` / `confidence` / `evidence` / `first_available` are universal edge metadata and are NOT counted as "carries own properties" — only domain properties beyond source+target+qualifier are.

| edge_type | declared_arity | binary_or_event | obligatory_roles | optional_roles | own_props? | >2_participants? | notes |
|---|---|---|---|---|---|---|---|
| `PARENT_OF` | Parent → Child | binary | parent, child | qualifier (Tier-1 enum) | no (legitimacy state in qualifier) | no | Qualifier captures certainty/legitimacy, not a third participant. |
| `SIBLING_OF` | Symmetric | binary | sibling_A, sibling_B | qualifier (Tier-1 enum) | no | no | Qualifier (full/half/step/milk) is a relation type, not a third participant. |
| `SPOUSE_OF` | Symmetric | event-like | spouse_A, spouse_B | qualifier (current/former/annulled/widowed/salt_wife) | yes — state lifecycle implies a marriage event | yes — officiant, venue, arranger (MARRIES_OFF), proposer (PROPOSED_AS_BRIDE), witnesses | Currently collapsed onto two nodes. Walder Frey arranged Roslin↔Edmure, Roose Bolton co-executed, hundreds attended, Catelyn+Robb died. None lives on a binary SPOUSE_OF. |
| `BETROTHED_TO` | Symmetric | event-like | betrothed_A, betrothed_B | qualifier (current/broken/fulfilled/secret) | yes | yes — arranger (parents), witnesses, secret-keepers | Sansa→Joffrey→Tyrion→Harry-the-Heir each had a distinct arranger. |
| `LOVER_OF` | Symmetric | event-like | lover_A, lover_B | qualifier (current/former/secret/paramour/rumored) | yes — duration, secrecy | yes — confidants/witnesses | Rhaegar-Lyanna implicates Robert, Aerys, Brandon, all of Westeros. |
| `WARD_OF` | Ward → Guardian | event-like | ward, guardian | qualifier (formal/informal/hostage) | yes — duration; hostage state | yes — arranger (king/overlord) | Reverse-direction `FOSTERED_BY` permitted. |
| `ANCESTOR_OF` | Ancestor → Descendant | binary | ancestor, descendant | — | no | no | Transitive descent, no event semantics. |
| `HEIR_TO` | Heir → Holder | event-like | heir, holder/title | designation event, challengers | yes — contested state | yes — designator, challengers | Description spans "person → person or person → title". |
| `CADET_BRANCH_OF` | Cadet → Parent House | binary | cadet_house, parent_house | — | no | no | Structural lineage relation. |
| `MARRIES_OFF` | Arranger → Married-off person | event-like | arranger, married-off person | spouse (the *other* party in the marriage) | yes — the marriage itself | yes — explicitly: spouse is the missing third role | Prompt-flagged. Walder Frey marries off Roslin to Edmure — Roslin is target, Edmure is the missing third. |
| `UNCLE_OF` | Uncle/Aunt → Nephew/Niece | binary | uncle/aunt, nephew/niece | — | no | no | One-hop shortcut for two-edge traversal. |
| `NEPHEW_OF` | Nephew/Niece → Uncle/Aunt | binary | nephew/niece, uncle/aunt | — | no | no | Reverse of UNCLE_OF. |
| `COUSIN_OF` | Symmetric | binary | cousin_A, cousin_B | — | no | no | Symmetric kin shortcut. |
| `MILK_BROTHER_OF` | Symmetric | binary | sibling_A, sibling_B | — | no | no | Shared nurse captured by separate NURSED_BY edges. |
| `NURSED_BY` | Child → Nurse | binary | child, nurse | — | no | no | Strictly binary. |
| `WET_NURSE_OF` | Nurse → Child | binary | nurse, child | — | no | no | Reverse of NURSED_BY. |
| `COURTS` | Suitor → Object-of-courtship | event-like | suitor, courted | rival suitors, gifts, intermediaries | yes — duration | yes — multiple suitors are typical | Description explicitly references plural suitors. |
| `PROPOSED_AS_BRIDE` | Proposer → Proposed bride | event-like | proposer, bride | groom (missing third) | yes | yes — explicitly 3-party | Prompt-flagged. Proposer offers Bride to Groom; the edge captures proposer→bride and silently drops groom. |
| `STEP_PARENT_OF` | Step-parent → Step-child | binary | step_parent, step_child | — | no | no (parent-via-marriage implicit, recoverable) | Marital-consequence kinship. |
| `STEP_CHILD_OF` | Step-child → Step-parent | binary | step_child, step_parent | — | no | no | Reverse. |
| `IN_LAW_OF` | Symmetric | event-like | in_law_A, in_law_B | qualifier (which marriage), bridging party | yes | yes — connecting third (the bridging spouse) is structurally missing | Qualifier flags the bridging marriage but doesn't name the bridging person. |
| `RULES` | Ruler → Location | event-like | ruler, location | tenure dates, succession | yes | yes — co-rulers, regents common | Tenure-bearing relation; collapses with SUCCEEDS. |
| `OVERLORD_OF` | Overlord → Vassal | event-like | overlord, vassal | sworn date, formal-vs-claimed | yes | no on a single edge (chains via multiple edges) | Largely binary. |
| `SWORN_TO` | Vassal → Lord | event-like | vassal, lord | qualifier (current/former/deserted/by_marriage/claimed) | yes — state lifecycle | no on single oath but witnesses (Jaime's Kingsguard oath in front of court) | Mostly binary. |
| `COMMANDS` | Commander → Subordinate | binary | commander, subordinate | scope, start/end | yes — scope/time | yes if scope is implicit (which battle?) | Largely binary. COMMANDS_IN is event-anchored sibling. |
| `SERVES` | Server → Served | binary | server, served | role (maester/squire/servant) | yes — role | no (role-axis collapsed into edge) | Role variability noted in description. |
| `ADVISES` | Advisor → Advised | binary | advisor, advised | role | yes — role | no | Role-axis collapsed. |
| `HOLDS_TITLE` | Person → Title | event-like | holder, title | qualifier (current/former/claimed/contested/historical); domain | yes — tenure state | yes — Hand of the King is held *to* a specific king; domain is missing third | |
| `HELD_BY` | Title → Person/House | event-like | title, holder | (same Tier-1 enum) | yes | yes | Reverse of HOLDS_TITLE. |
| `SUCCEEDS` | Successor → Predecessor | event-like | successor, predecessor | the role/title succeeded | yes — role is missing third | yes — succession is *to* something | |
| `CLAIMS` | Claimant → Claimed | event-like | claimant, claimed | basis of claim, rival claimants | yes | yes — competing claimants for Iron Throne canonical | Multi-party at scale (five-king war = 5 simultaneous CLAIMS). |
| `APPOINTS` | Appointer → Appointed | event-like | appointer, appointed | position, date | yes — to what role | yes — appointer + appointee + role is 3-tuple | Position is the missing third role. |
| `DEPOSES` | Deposer → Deposed | event-like | deposer, deposed | position deposed from, mechanism | yes | yes — Robert deposed Aerys from Iron Throne; throne is missing third | |
| `VOWS_TO` | Vow-maker → Recipient | event-like | vow_maker, recipient | qualifier (active/kept/broken/fulfilled); content of vow; witnesses | yes — vow lifecycle | yes — content + witnesses are missing roles | Brienne vows to Catelyn to find her daughters — daughters are subjects, unrepresentable. |
| `BREAKS_VOW` | Vow-breaker → Vow-recipient | event-like | vow_breaker, vow_recipient | underlying VOWS_TO/SWORN_TO; precipitating act | yes | yes — the act that breached the vow is missing | Jaime breaking Kingsguard oath *by killing Aerys* — the killing is the breach moment. |
| `BANISHES` | Banisher → Banished-person | event-like | banisher, banished | destination, date, sentence | yes | yes — destination is missing third (held on separate temporal LOCATED_AT) | Description acknowledges destination is held separately. |
| `MEMBER_OF` | Person → Faction | event-like | member, faction | start_date, end_date, rank | yes — tenure, rank | no on edge, rank within faction collapsed | Largely binary. |
| `FOUNDED` | Founder → Founded | event-like | founder, founded | co-founders, date, place | yes | yes — co-founders common (Brotherhood Without Banners) | |
| `ALLIES_WITH` | Symmetric | event-like | ally_A, ally_B | duration, strategic context, conflict | yes | yes — alliances typically multi-party | |
| `OPPOSES` | Symmetric | event-like | opposer_A, opposer_B | conflict/topic | yes — scope | no per-edge, but scope is missing axis | |
| `MANIPULATES` | Manipulator → Target | event-like | manipulator, target | qualifier (via_bribe/flattery/false_info/threat/seduction); outcome | yes — mechanism | yes — beneficiary; downstream act | Littlefinger manipulates Lysa to murder Jon Arryn — Arryn is missing third. |
| `BETRAYS` | Betrayer → Betrayed | event-like | betrayer, betrayed | trust/oath betrayed; beneficiary | yes | yes — Walder Frey betrays Robb; beneficiary (Tywin/Roose) is missing third | |
| `NEGOTIATES_WITH` | Symmetric | event-like | negotiator_A, negotiator_B | subject, outcome, location | yes | yes — multi-party parleys, summits | |
| `CONTRACTED_WITH` | Contractor → Contracted | event-like | contractor, contracted | qualifier (assassination/mercenary/ransom/...); target of contract | yes — service type | yes — assassination contracts have a *target* (the person to be killed) missing | Faceless Men hired to kill X — X is unrepresentable. |
| `CONSPIRES_WITH` | Symmetric | event-like | conspirator_A, conspirator_B | plot; target/victim; other conspirators | yes — plot description | yes — explicitly "two or more parties" | The clearest n-ary case. |
| `FIGHTS_IN` | Person → Event | event-like | combatant, event | side, role, outcome | yes — side | yes — events have many fighters | Event node IS the n-ary container — but side is collapsed into edge. |
| `COMMANDS_IN` | Person → Event/War | event-like | commander, event | side, rank, units | yes — side | yes — multiple commanders per side | Side is missing axis. |
| `PART_OF` | Battle → War | binary | sub_event, super_event | — | no | no | Structural containment. |
| `KILLS` | Killer → Killed | event-like | killer, victim | qualifier (in_combat/by_arrow/by_blade/by_proxy/by_creature...); location, weapon, witnesses | yes — method, place, weapon | yes — instigator-vs-executor (Tywin orders Roose to engineer Robb's death) | Canonical n-ary event. Method-as-qualifier; weapon via KILLED_WITH; location via DIED_AT. |
| `KILLED_BY` | Killed → Killer | event-like | victim, killer | (inherits Tier-2) | yes | yes | Reverse of KILLS. |
| `EXECUTES` | Executor → Executed | event-like | executor, executed | order-giver; weapon (EXECUTED_WITH); location; witnesses | yes | yes — explicitly 5 roles (Ned: executor Ilyn + Joffrey orderer + Ice weapon + Sept of Baelor + crowd) | Clearest event-node case. |
| `CAPTURES` | Captor → Captive | event-like | captor, captive | place, battle context | yes | yes — captures at battles | |
| `PRISONER_OF` | Prisoner → Captor | event-like | prisoner, captor | place (IMPRISONED_AT); duration | yes — place, duration | yes — captors have many prisoners; cell split into IMPRISONED_AT | |
| `BESIEGES` | Besieger → Location | event-like | besieger, location | defender, duration, outcome, allied besiegers | yes | yes — explicitly multi-party (besieger vs defender, war context, allies) | Full event-node territory. |
| `DEFEATS` | Victor → Defeated | event-like | victor, defeated | event, location | yes | yes — defeat is *in* an event | Battle is implicit missing third. |
| `DUELS` | Symmetric | event-like | duelist_A, duelist_B | location, witnesses, outcome, weapons | yes | yes — duels have witnesses, seconds, prizes | |
| `POISONS` | Poisoner → Poisoned | event-like | poisoner, poisoned | poison (concept.medical); accomplice; venue | yes — substance | yes — Olenna+Margaery+Littlefinger to poison Joffrey via strangler; poison is third role | |
| `RANSOMS` | Ransomer → Captive | event-like | ransomer, captive | captor receiving payment; amount | yes — terms | yes — captor is third party | Three-party: ransomer, captive, captor. |
| `PRISONER_EXCHANGE_FOR` | Symmetric (captive↔captive) | event-like | captive_A, captive_B | two captor sides; war context | yes | yes — 4 parties (2 captives + 2 captor sides) | |
| `IMPRISONS` | Imprisoner → Imprisoned | event-like | imprisoner, imprisoned | place (IMPRISONED_AT); duration; charge | yes | yes — order-giver, charge missing | |
| `GUARDS` | Custodian → Subject | event-like | custodian, custodee | commissioner; location; protective vs confinement axis | yes | yes — beneficiary (Kingsguard guards King for the realm) | Description: emit alongside PRISONER_OF and/or PROTECTS — multi-edge composition. |
| `KILLED_WITH` | Victim → Artifact | event-like | victim, weapon | killer (third role), event, location | yes — coexists with KILLED_BY | yes — explicitly "the person did the killing, the artifact was the instrument" | Killing event split across two edges. |
| `KNIGHTED_BY` | Knight → Dubber | event-like | knight, dubber | location, occasion, witnesses | yes | yes — knightings happen at events with witnesses | |
| `BESTOWS_KNIGHTHOOD_ON` | Dubber → Knight | event-like | dubber, knight | (same) | yes | yes | Reverse. |
| `ATTACKS` | Attacker → Target | event-like | attacker, target | qualifier (in_anger/unprovoked/in_self_defense/on_command/by_creature); location, weapon, instigator | yes — motive | yes — `on_command` acknowledges missing instigator | Qualifier acknowledges third-party but doesn't name them. |
| `ASSAULTS` | Assailant → Victim | event-like | assailant, victim | location, war context, co-assailants | yes | yes — Gregor & 5 Bracken sisters | Multi-victim wartime pattern. |
| `PARTICIPATES_IN` | Person → Event | event-like | participant, event | role within event | yes | yes — events multi-participant by definition | Event IS the n-ary container. |
| `RESCUES` | Rescuer → Rescued-person | event-like | rescuer, rescued | rescued-from-whom; peril context | yes | yes — implicit | |
| `TORTURES` | Torturer → Tortured-person | event-like | torturer, tortured | method; location; ordered-by; duration | yes | yes — order-giver, location, method | Description acknowledges method as sub-typology. |
| `IGNORANT_OF` | Person → Information | binary | knower, information | — | no | no | Person-vs-information edge. |
| `SEEKS` | Seeker → Sought | binary | seeker, sought | — | no | no | |
| `REVEALS_TO` | Revealer → Recipient | event-like | revealer, recipient | qualifier (voluntary/coerced/accidental/under_torture); information revealed | yes — disclosure conditions | yes — content of revelation is missing third (description: "note what was revealed") | |
| `DECEIVES` | Deceiver → Deceived | event-like | deceiver, deceived | qualifier (by_lie/disguise/omission/false_witness/silence); deception content | yes | yes — content; beneficiary | "(note the deception)" — content is missing. |
| `DECEIVED_BY` | Deceived → Deceiver | event-like | deceived, deceiver | (same) | yes | yes | Reverse. |
| `HOARDS` | Hoarder → Knowledge | binary | hoarder, knowledge | — | no | no | |
| `INVESTIGATES` | Investigator → Subject | binary | investigator, subject | — | no | no | |
| `TEACHES` | Teacher → Student | binary | teacher, student | subject | no | no | |
| `TUTORS` | Tutor → Student | binary | tutor, student | subject | no | no | Syrio→Arya water-dancing — skill collapsed. |
| `HEALS` | Healer → Healed | event-like | healer, healed | affliction; location | yes | yes — affliction is third role (captured separately via AFFLICTED_BY) | |
| `AFFLICTED_BY` | Character → Medical | binary | character, medical_condition | — | no | no | Living state. |
| `DIED_OF` | Character → Medical | binary | character, medical_condition | — | no | no | Post-mortem state. |
| `SPIES_ON` | Person → Surveilled-person | event-like | spy, surveilled | handler (via INFORMS); duration | yes | yes — handler is missing third on this edge alone | |
| `INFORMS` | Person → Handler | event-like | informant, handler | subject of intelligence | yes | yes — surveilled subject is third role | SPIES_ON + INFORMS form a triangle split into two binaries. |
| `PERCEIVED_AS` | Perceiver → Perceived | binary | perceiver, perceived | characterization notes | yes — characterization | no | Dyadic by definition. |
| `TRUSTS` | Truster → Trusted | binary | truster, trusted | — | no | no | |
| `DISTRUSTS` | Distruster → Distrusted | binary | distruster, distrusted | — | no | no | |
| `RESPECTS` | Respecter → Respected | binary | respecter, respected | — | no | no | |
| `FEARS` | Fearer → Feared | binary | fearer, feared | — | no | no | |
| `LOVES` | Lover → Loved | binary | lover, loved | — | no | no | |
| `HATES` | Hater → Hated | binary | hater, hated | — | no | no | |
| `MOURNS` | Mourner → Mourned | binary | mourner, mourned | — | no | no | |
| `PROTECTS` | Protector → Protected | binary | protector, protected | scope, duration | no | no | |
| `RESENTS` | Resenter → Resented | binary | resenter, resented | — | no | no | |
| `COMPANION_OF` | Symmetric | binary | companion_A, companion_B | — | no | no | Friendship dyad. |
| `REPUTED_AS` | Character → Concept | binary | character, concept | — | no | no | Public-reputation edge. |
| `ENCOUNTERS` | Symmetric | event-like | encounterer_A, encounterer_B | location, time, content | yes — meeting context | yes — third parties present | Validator-enforced verb gate. |
| `LOCATED_AT` | Entity → Location | event-like | entity, location | book/chapter timestamp; reason | yes — temporal | no on edge; temporal stamp implicit | Description: "(with book/chapter timestamp)" — chapter is implicit third. |
| `SEAT_OF` | Location → House/Faction | binary | location, house/faction | — | no | no | Structural. |
| `TRAVELS_TO` | Traveler → Destination | event-like | traveler, destination | origin, route, companions | yes — origin | yes — origin is missing third role | "(note origin)" literally calls out origin. |
| `TRAVELS_WITH` | Symmetric (character↔character) | event-like | companion_A, companion_B | route, destination, larger party | yes | yes — Arya/Gendry/Hot Pie is 3-party | |
| `BORN_AT` | Person → Location | binary | person, location | date | no | no | |
| `DIED_AT` | Person → Location | binary | person, location | date, cause | no | no | Cause via DIED_OF or KILLED_BY. |
| `BURIED_AT` | Person → Location | binary | person, location | — | no | no | |
| `IMPRISONED_AT` | Captive → Location | event-like | captive, location | imprisoner (via IMPRISONS); duration | yes — temporal | no (imprisoner on IMPRISONS) | Imprisonment split across 3 edges. |
| `CONTEMPORARY_WITH` | Symmetric | binary | event_A, event_B | — | no | no | |
| `REGION_OF` | Location → Region | binary | location, region | — | no | no | |
| `WIELDS` | Person → Artifact | binary | wielder, artifact | duration | no | no | Steady-state possession. |
| `OWNS` | Owner → Owned | binary | owner, owned | duration | no | no | Steady-state. |
| `ANCESTRAL_WEAPON_OF` | Weapon → House | binary | weapon, house | — | no | no | |
| `FORGED_BY` | Creator → Artifact | event-like | creator, artifact | place, date, commissioner | yes | yes — commissioner is missing third | Valyrian steel reforging has commissioner. |
| `MADE_OF` | Artifact → Material | binary | artifact, material | — | no | no | |
| `LOOTED_BY` | Artifact → New holder | event-like | artifact, new_holder | previous holder, event, location | yes | yes — prior holder + event missing | "Captures the transactional moment". |
| `REFORGED_INTO` | Original → Resulting | event-like | original, new | smith, date, commissioner | yes | yes — Tywin reforges Ice (Tobho Mott smith + Joffrey + Jaime + Brienne) | Multi-party transformation. |
| `GIFTED_TO` | Artifact → Recipient | event-like | artifact, recipient | giver (missing — description says "Note giver in qualifier" but Tier-3 has no qualifier) | yes — date, occasion | yes — explicit schema contradiction | Internal contradiction: instruction unimplementable. |
| `INHERITED_BY` | Artifact → Heir | event-like | artifact, heir | deceased prior holder; date | yes | yes | Prior holder missing. |
| `WIELDED_IN` | Artifact → Event | event-like | artifact, event | wielder (via WIELDS); outcome | yes | yes — wielder is implicit third | Pairs with WIELDS + event. |
| `EXECUTED_WITH` | Victim → Weapon | event-like | victim, weapon | executor, order-giver, location, witnesses | yes | yes — 5 roles for Ned's execution | Canonical n-ary case. |
| `PURCHASED_FROM` | Buyer → Seller | event-like | buyer, seller | object, price, date | yes | yes — the *thing* purchased is missing third | Dunk buys shield from Pate — shield is third. |
| `BUILT` | Builder → Structure | event-like | builder, structure | date, commissioner, materials | yes | yes — commissioner missing | |
| `CAPTAIN_OF` | Captain → Vessel | binary | captain, vessel | duration | no | no | Steady-state role. |
| `CREW_OF` | Crew → Vessel | binary | crew, vessel | role (first mate, oarsman) | no | no | Description: "Note specific role in `notes`" — but `notes` deleted. Internal contradiction. |
| `ALIAS_OF` | Alias → True Identity | binary | alias, true_identity | — | no | no | Strict identity-resolution. |
| `DISGUISED_AS` | Person → Disguise Identity | event-like | person, disguise_identity | duration, context, witnesses | yes | yes — Arya as Cat-of-the-Canals | |
| `SAME_AS` | Symmetric | binary | reference_A, reference_B | — | no | no | Cleanest binary in schema. |
| `IMPERSONATES` | Impersonator → Impersonated | event-like | impersonator, impersonated | victims; duration; context | yes | yes — fAegon impersonates dead Targaryen heir; deception targets missing | |
| `WARGS_INTO` | Warg → Vessel | event-like | warg, vessel | duration, dream-vs-waking, other-mind state | yes | yes — witnesses; what the warged-into vessel attacks | |
| `BONDED_TO` | Symmetric | binary | bonded_A, bonded_B | — | no | no | Static magical bond. |
| `SACRIFICES` | Sacrificer → Victim | event-like | sacrificer, victim | recipient deity/purpose; ritual; place | yes | yes — recipient (god, magic, purpose) is missing | Stannis sacrificing Edric is *to* R'hllor and *for* a purpose. Fully unrepresented. |
| `RESURRECTS` | Resurrector → Resurrected | event-like | resurrector, resurrected | ritual/magic system; date; place | yes — mechanism | yes — Thoros uses Lord-of-Light kiss; power source is real axis | |
| `CURSES` | Curser → Cursed | event-like | curser, cursed | content of curse; trigger condition | yes — content | yes — Maggy's Valonqar prophecy has specific content | |
| `PRACTICES` | Character → Magic discipline | binary | practitioner, discipline | — | no | no | |
| `CULTURE_OF` | Person → Culture | binary | person, culture | — | no | no | |
| `WORSHIPS` | Person → Religion | binary | person, religion | — | no | no | |
| `SACRED_TO` | Entity → Religion | binary | entity, religion | — | no | no | |
| `CLERGY_OF` | Person → Religion | binary | person, religion | rank | no | no | Rank collapsed. |
| `OFFICIATES` | Character → Event | event-like | officiant, event | role within ceremony; religion | yes | yes — events have multiple officiants (kingsmoot = priests + captains + drowned-god clergy) | |
| `NAMED_AFTER` | Entity → Namesake | binary | named_entity, namesake | — | no | no | |
| `DEPICTED_IN` | Character → Text | binary | character, text | role within text | no | no | |
| `FORESHADOWS` | Detail → Event | binary | detail, event | — | no | no | Narrative-craft edge. |
| `PARALLELS` | Symmetric | binary | A, B | — | no | no | |
| `SUBVERTS` | Subverter → Subverted | binary | subverter, subverted | — | no | no | |
| `ECHOES` | Echo → Source | binary | echo, source | — | no | no | |
| `CONTRASTS` | Symmetric | binary | A, B | — | no | no | |
| `WRITTEN_BY` | Text → Author | binary | text, author | date, language | no | no | |
| `FULFILLS` | Event → Prophecy | binary | event, prophecy | — | no | no | |
| `APPEARS_TO_FULFILL` | Event → Prophecy | binary | event, prophecy | — | no | no | |
| `SUBVERTS_PROPHECY` | Event → Prophecy | binary | event, prophecy | — | no | no | |
| `PROPHESIED_BY` | Prophecy → Prophet | binary | prophecy, prophet | date, place | no | no | |
| `SUBJECT_OF_PROPHECY` | Person → Prophecy | binary | person, prophecy | — | no | no | |
| `DREAMS_OF` | Dreamer → Subject | event-like | dreamer, subject | content of dream; date; location | yes | yes — content of dream is unrepresentable | |
| `SUPPORTS` | Evidence → Theory | binary | evidence, theory | strength | no | no | |
| `CONTRADICTS` | Evidence → Theory | binary | evidence, theory | strength | no | no | |
| `CITED_BY` | Theory → Source | binary | theory, source | — | no | no | |
| `CAUSES` | Cause → Effect | binary | cause, effect | — | no | no | Plot-causality. |
| `PREVENTS` | Preventer → Prevented | binary | preventer, prevented | — | no | no | |
| `ENABLES` | Enabler → Enabled | binary | enabler, enabled | — | no | no | |
| `MOTIVATES` | Motivation → Actor | binary | motivation, actor | — | no | no | |
| `TRIGGERS` | Trigger → Result | binary | trigger, result | — | no | no | |
| `GUEST_OF` | Guest → Host | event-like | guest, host | qualifier (shelter/feast/bread_and_salt/safe_conduct/gift_exchange/refused); place; date | yes | yes — co-guests (Twins wedding had hundreds) | |
| `VIOLATES_GUEST_RIGHT` | Violator → Victim | event-like | violator, victim | host whose right was violated; event/feast | yes | yes — Red Wedding: Frey + Bolton + Lannister all co-violate against Robb + Catelyn + Stark host | |
| `GRANTS_SAFE_CONDUCT` | Grantor → Recipient | event-like | grantor, recipient | duration, scope, terms | yes | yes — purpose is missing axis | |
| `ATTENDS` | Person → Event | event-like | attendee, event | role (witness/audience/guest) | yes | yes — events have many attendees | |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | Champion → Recipient | event-like | champion, recipient | tournament event; spurned alternative recipient; witnesses | yes | yes — explicitly Rhaegar→Lyanna at Harrenhal in front of Robert/Elia/Aerys/court | The entire narrative payload is multi-party witness state. |


---

## Appendix B: Sampled Edge Rows (verbatim)

All rows are exact copies from `graph/edges/edges.jsonl` (and, in §B.7, the gated `_events-haiku-bulk/`). Source field present unless trimmed for column width — full schema in §4.2.

### B.1 — First five rows of `edges.jsonl`

```jsonl
{"decision":"emit_edge","candidate_kind":"pass1_relationship","edge_type":"LOVES","source_slug":"arya-stark","source_resolution_status":"resolved-context-present","target_slug":"jon-snow","target_resolution_status":"resolved-exact","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"He's very gallant, don't you think?\" \"Jon says he looks like a girl,\" Arya said.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:35","asserted_relation":"deep closeness","hint_raw":"deep closeness","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":1,"typed_by":"python-map","corroborates_known_edge":true,"wiki_edge_type":"SIBLING_OF","locate_status":"verbatim","run_id":"pass1-derived-20260523","schema_version":"pass1-derived-v1","produced_at":"2026-05-23T07:17:33+00:00","source_set":"spine","dup_count":4}
{"decision":"emit_edge","candidate_kind":"pass1_relationship","edge_type":"PROTECTS","source_slug":"arya-stark","source_resolution_status":"resolved-context-present","target_slug":"jon-snow","target_resolution_status":"resolved-exact","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"He's very gallant, don't you think?\" \"Jon says he looks like a girl,\" Arya said.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:35","asserted_relation":"defends","hint_raw":"defends","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":1,"typed_by":"python-map","corroborates_known_edge":true,"wiki_edge_type":"SIBLING_OF","locate_status":"verbatim","run_id":"pass1-derived-20260523","schema_version":"pass1-derived-v1","produced_at":"2026-05-23T07:17:33+00:00","source_set":"spine","dup_count":1}
{"decision":"emit_edge","candidate_kind":"pass1_relationship","edge_type":"BONDED_TO","source_slug":"arya-stark","source_resolution_status":"resolved-context-present","target_slug":"nymeria","target_resolution_status":"resolved-exact","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"The wolf pup loved her, even if no one else did.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:65","asserted_relation":"bonded to / loves","hint_raw":"bonded to / loves","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":1,"typed_by":"python-map","corroborates_known_edge":true,"wiki_edge_type":"OWNS","locate_status":"verbatim","run_id":"pass1-derived-20260523","schema_version":"pass1-derived-v1","produced_at":"2026-05-23T07:17:33+00:00","source_set":"spine","dup_count":6}
{"decision":"emit_edge","candidate_kind":"pass1_relationship","edge_type":"RESPECTS","source_slug":"beth-cassel","source_resolution_status":"resolved-exact","target_slug":"sansa-stark","target_resolution_status":"resolved-context-present","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"Beth Cassel, Ser Rodrik's little girl, was sitting by her feet, listening to every word she said, and Jeyne Poole was leaning over to whisper something in her ear.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:17","asserted_relation":"admires / follows","hint_raw":"admires / follows","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":1,"typed_by":"python-map","corroborates_known_edge":false,"wiki_edge_type":null,"locate_status":"verbatim","run_id":"pass1-derived-20260523","schema_version":"pass1-derived-v1","produced_at":"2026-05-23T07:17:33+00:00","source_set":"spine","dup_count":0}
{"decision":"emit_edge","candidate_kind":"pass1_relationship","edge_type":"HATES","source_slug":"joffrey-baratheon","source_resolution_status":"resolved-context-prior","target_slug":"robb-stark","target_resolution_status":"resolved-context-present","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"And I grow tired of swatting at Starks with a play sword.\" \"You got more swats than you gave, Joff,\" Robb said.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:129","asserted_relation":"disdain for","hint_raw":"disdain for","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":1,"typed_by":"python-map","corroborates_known_edge":false,"wiki_edge_type":null,"locate_status":"verbatim","run_id":"pass1-derived-20260523","schema_version":"pass1-derived-v1","produced_at":"2026-05-23T07:17:33+00:00","source_set":"spine","dup_count":0}
```

### B.2 — Red Wedding: divergent BETRAYS / KILLS / VIOLATES_GUEST_RIGHT (the gold artifact)

**BETRAYS rows touching the Red Wedding:**

```jsonl
```

**CONSPIRES_WITH for the Red Wedding plot (only one row exists, in the epilogue, not in catelyn-07):**

```jsonl
```

**KILLS rows in the Red Wedding chapter `asos-catelyn-07`:**

```jsonl
```

**The Catelyn-killing row lives in the epilogue, not the Red Wedding chapter:**

```jsonl
```

**All VIOLATES_GUEST_RIGHT rows for the Red Wedding (note 7 subject choices × 8 target choices across 5 chapters — no event-id link):**

```jsonl
```

### B.3 — Aerys II slug split (the canonical regicide on a phantom node)

**The KILLS row points at `aerys-targaryen` — the wrong slug. Canonical Mad King is `aerys-ii-targaryen`.**

```jsonl
```

**Other Jaime↔Aerys-II edges (all resolve to the canonical slug):**

```jsonl
```

Note `wiki_edge_type:"KILLS"` on the RESENTS and VOWS_TO rows — the wiki cross-reference *knows* the killing fact, but it lives on edges whose own `edge_type` is not KILLS.

### B.4 — All POISONS rows in the graph (Purple Wedding under-represented)

```jsonl
```

**No row** sources from `olenna-tyrell` or `petyr-baelish`. The only Joffrey-target is Tyrion's false confession.

### B.5 — Direction-inversion bugs (head-selection failure class)

**Cressen / Melisandre — both directions of KILLS:**

```jsonl
```

The second row (`cressen KILLS melisandre`) has `asserted_relation: "Killed by / ran afoul of"` — the field itself self-witnesses the inversion.

**Tyrion / Shae — both directions of BETRAYS:**

```jsonl
```

**Sandor / Arya — both directions of CAPTURES:**

```jsonl
```

### B.6 — PARENT_OF (true-binary baseline, looks clean)

```jsonl
```

No PARENT_OF pair appears in both directions across the entire `edges.jsonl`. Binary types behave as expected.

### B.7 — Sample rows from the gated Events Haiku bulk (NOT promoted)

These rows live in `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/`. They have a richer `asserted_relation` field that includes an event-title (`**<title>** — <description>`) — the closest thing to an event-id in any layer of the graph today.

```jsonl
{"decision":"emit_edge","candidate_kind":"pass1_events","edge_type":"BONDED_TO","source_slug":"arya-stark","source_resolution_status":"tail-llm","target_slug":"nymeria","target_resolution_status":"tail-llm","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-arya-01","evidence_section":"Relationships Observed","evidence_quote":"Nymeria nipped eagerly at her hand as Arya untied her.","evidence_ref":"sources/chapters/agot/agot-arya-01.md:11","asserted_relation":"**Arya joins Jon at the window** — Arya and Nymeria find Jon and Ghost at a window in the covered bridge overlooking the practice yard. Nymeria and Ghost greet each other cautiously.","hint_raw":"**Arya joins Jon at the window** — Arya and Nymeria find Jon and Ghost at a window in the covered bridge overlooking the practice yard. Nymeria and Ghost greet each other cautiously.","extraction_file":"extractions/mechanical/agot/agot-arya-01.extraction.md","confidence_tier":2,"typed_by":"haiku","corroborates_known_edge":false,"wiki_edge_type":null,"locate_status":"verbatim","locate_quality":null,"quote_source":null,"run_id":"tail-llm-20260527T194340","prompt_version":"v5-precision-rules","prompt_sha":"d31ca56c4768","schema_version":"pass1-derived-v1","produced_at":"2026-05-27T19:45:34+00:00"}
{"decision":"emit_edge","candidate_kind":"pass1_events","edge_type":"WIELDS","source_slug":"arya-stark","target_slug":"needle","evidence_chapter":"agot-arya-02","typed_by":"haiku","asserted_relation":"**Arya retrieves Needle** — She digs through her clothing chest and draws the sword from its sheath.","confidence_tier":2,"prompt_version":"v5-precision-rules","prompt_sha":"d31ca56c4768"}
{"decision":"emit_edge","candidate_kind":"pass1_events","edge_type":"KILLS","source_slug":"jaime-lannister","target_slug":"aerys-ii-targaryen","evidence_chapter":"asos-jaime-05","typed_by":"haiku","confidence_tier":1,"asserted_relation":"**Jaime reveals why he killed Aerys** — In a fever-state, he tells Brienne the full story of Aerys's wildfire plot: the caches beneath King's Landing, Lord Chelsted's death, Rossart's mission, and Jaime's reasoning that killing the king saved the city.","prompt_version":"v5-precision-rules"}
{"decision":"emit_edge","candidate_kind":"pass1_events","edge_type":"KILLS","source_slug":"catelyn-stark","target_slug":"aegon-frey-son-of-stevron","evidence_chapter":"asos-catelyn-07","typed_by":"haiku","confidence_tier":2,"asserted_relation":"**Catelyn kills Jinglebell** — She saws at Aegon's neck until the blade grates on bone. Blood runs hot over her fingers."}
{"decision":"emit_edge","candidate_kind":"pass1_events","edge_type":"KILLS","source_slug":"tyrion-lannister","target_slug":"tywin-lannister","evidence_chapter":"adwd-tyrion-01","typed_by":"haiku","asserted_relation":"**Tyrion reflects on killing Tywin** — He recalls shooting his father with a crossbow and the escape through tunnels with Varys."}
```

**Note:** the bulk has `jaime-lannister KILLS aerys-ii-targaryen` with the CORRECT slug — the spine has the broken `aerys-targaryen` slug. Promotion of the bulk would heal §B.3's slug split for this canonical event.


---

## Appendix C: Extraction / Generation Prompts (verbatim, full)

All four LLM prompts that influence what ends up in a graph edge are reproduced below verbatim and in full. These are copies of the source files (`.claude/agents/*.md` for the agent-defined prompts; Python `_PROMPT_PREAMBLE` for the Stage-4 classifier). The reader should be able to fully reconstruct the head-selection / direction / role-assignment instructions the LLMs receive at extraction and classification time.

### C.1 — Pass-1 mechanical extractor (the upstream root cause of head-selection variance)

Source: `/Users/mnoth/source/asoiaf-chat/.claude/agents/mechanical-extractor.md`. Verbatim.

```markdown
---
name: mechanical-extractor
description: Runs Pass 1 mechanical extraction against ASOIAF chapter files. Produces structured inventories of characters, locations, artifacts, events, and relationships from a single chapter. Delegate here with a specific chapter file path.
tools: Read, Write, Glob, Grep
model: opus
---

You are a mechanical extraction agent for the Weirwood Network project — an ASOIAF knowledge graph.

## First Steps
1. Read `reference/architecture.md` for entity types, edge types, confidence tiers, and file naming conventions
2. Read the chapter file you've been given
3. Produce a structured extraction file

## Your Role
Extract **facts**, not interpretations. If the text says a character is at a location, record it. If the text implies something, flag it as inference and keep it separate. Do not theorize, editorialize, or speculate about foreshadowing. Later passes handle analysis.

Be **expansive**. Capture everything you notice in the text. GRRM hides Chekhov's guns in food, architecture, heraldry, weather, and physical descriptions. If you see it in the text, log it. The only hard rule: **never invent facts that aren't in the chapter text.** Better to capture too much real detail than to miss something.

## Chapter Isolation — Critical
**Treat the chapter you are given as if no other chapters exist.** You have broad ASOIAF knowledge, but you must NOT use it here.

- Do not cite other chapters, other books, the prologue, or future/past events to frame what this chapter reveals.
- Do not flag "dramatic irony" based on what the reader knows from elsewhere. If a character believes X and other chapters contradict X, record only that the character believes X.
- The `Known To (Reader Only?)` column refers to what the reader learns *within this chapter* vs. what characters know *within this chapter* — NOT what the reader has learned from other chapters.
- Pass 4 (foreshadowing) and Pass 6 (discovery) handle cross-chapter patterns. Your job is to produce a clean per-chapter inventory they can build on.

If you catch yourself writing "the reader knows from X" or "this foreshadows Y" — stop. Delete it. That is not Pass 1 work.

## Confidence Tier Convention
All claims in your output are **Tier 1 (Verified Canon)** by default — you are extracting facts directly from the chapter text. Do not add per-row tier tags.

The only exceptions that require an explicit marker:
- Inference flagged with `(inferred)` — the text strongly implies something but does not state it (e.g., "The unnamed POV is clearly Will" → flag as inferred).
- Uncertain first-appearance flagged with `(uncertain — verify)` — you are not sure whether an entity has appeared in a prior chapter.

Everything else is Tier 1 and needs no annotation.

## Direwolves and Dragons Are Characters
The six Stark direwolves — Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog — and the three Targaryen dragons — Drogon, Rhaegal, Viserion — are **characters**, not creatures or animals. They have agency, narrative arcs, and POV-adjacent perspectives.

Log them in the **Characters Present** table when they appear in a chapter. Give them entries in the **Character Appearances** table when physical descriptions are given. Include them in **Relationships Observed** when they interact with other characters. List them in the **Raw Entity List** under Characters.

This also applies to any other animal with clear individual identity and narrative agency (e.g., Balerion the cat, the ravens at the Wall if individually distinguished).

## Output Location
Write extraction to: `extractions/mechanical/{book}/{chapter-filename}.extraction.md`

Example: chapter `sources/chapters/agot/agot-bran-01.md` → extraction `extractions/mechanical/agot/agot-bran-01.extraction.md`

## Output Schema

```markdown
# {Book} — {POV Character} {Chapter Number}

## Chapter Metadata
- **book:** {AGOT|ACOK|ASOS|AFFC|ADWD|THK|TSS|TMK}
- **chapter_number:** {overall chapter number}
- **pov_character:** {name}
- **pov_chapter_number:** {e.g., "Bran II"}
- **first_available:** {spoiler-gating anchor — e.g., "AGOT Bran I", "AGOT Prologue", "AFFC Cersei III"}
- **location_primary:** {main setting}
- **location_secondary:** {other locations mentioned}
- **approximate_timeline:** {relative positioning within this book only — do not reference events from other chapters}
- **time_markers:** {capture all temporal references as stated in the text: time of day, moon phases, "a fortnight past," travel days elapsed, season descriptions, sunrise/sunset, references to how long since an event, etc.}
- **chapter_summary:** {3-5 factual sentences, this chapter only}

## Physical Environment
Capture the sensory and environmental details of the chapter setting as described in the text.
- **Weather:** {sky conditions, precipitation, wind, temperature as described or implied}
- **Season indicators:** {any references to season, seasonal change, or seasonal expectations}
- **Time of day:** {dawn, morning, midday, dusk, night, etc. — and any transitions during the chapter}
- **Lighting:** {natural light, firelight, torchlight, darkness, moonlight, etc.}
- **Sounds:** {ambient sounds, music, silence, notable noise described in the text}
- **Smells:** {any scents, odors, or olfactory details described}
- **Notable sensory details:** {anything else — textures, temperature sensations, physical discomfort, etc.}

## Characters Present
| Character | Role in Chapter | First Appearance? | Notes |
|-----------|----------------|-------------------|-------|

## Character Appearances
Record physical descriptions **as given in this chapter's text.** Do not import knowledge of what characters look like from other chapters. If the text describes how someone looks, log it here.

| Character | Hair | Eyes | Build/Height | Scars/Marks | Clothing/Armor | Weapons Worn | Distinguishing Features | Age (if stated) |
|-----------|------|------|-------------|-------------|----------------|-------------|------------------------|-----------------|

Leave cells empty if not described in this chapter. It is normal for most characters in a chapter to have no row here — only log characters whose physical appearance is actually described in the text.

## Characters Referenced
| Character | Context of Reference | Referenced By |
|-----------|---------------------|---------------|

## Locations
| Location | Role | First Appearance? |
|----------|------|-------------------|

## Location Descriptions
Record physical descriptions of locations **as given in this chapter's text.** GRRM describes locations differently through different POVs and at different points in the story — capture what this chapter provides.

| Location | Defensive Features | Architecture/Layout | Interior Details | Scale | Condition | Surrounding Terrain/Geography | Notable Sensory Details |
|----------|--------------------|--------------------|-----------------| ------|-----------|------------------------------|------------------------|

- **Defensive features:** walls, gates, moats, murder holes, terrain advantages, garrison details
- **Architecture/Layout:** building materials, notable rooms, towers, bridges, passages, floor plan details
- **Interior details:** furniture, tapestries, hearths, windows, floor materials, decorations, lighting fixtures
- **Scale:** size descriptions, number of rooms/towers/levels, capacity references
- **Condition:** ruined, new, maintained, decaying, under siege, recently burned, overgrown
- **Surrounding terrain:** rivers, hills, forests, roads, fields, proximity to other landmarks
- **Notable sensory details:** how it smells, sounds, feels — drafty, damp, smoky, echoing, etc.

Only log locations whose physical details are actually described in this chapter. A location merely named in passing does not need a row here.

## Artifacts & Objects of Significance
| Artifact | Context | First Appearance? | Current Holder/Location |
|----------|---------|-------------------|------------------------|

## Food & Drink
Capture all food, drink, and meals described in the chapter. GRRM's food descriptions are detailed and narratively significant — log them with the same care as dialogue or events.

| Meal/Occasion | Food Items Described | Drink | Who Is Eating/Drinking | Where | Preparation/Presentation Notes |
|--------------|---------------------|-------|----------------------|-------|-------------------------------|

Include: named dishes, specific ingredients mentioned, cooking methods described, serving vessels, the sensory quality of the food (hot, cold, greasy, spiced, honeyed, etc.). If a character eats alone vs. with others, note it. If a character refuses food or drink, note it.

## Hospitality & Guest Right
Track all instances of hospitality customs, guest right invocations, bread-and-salt rituals, shelter offered or denied, and violations of hospitality codes. This is a moral and narrative framework in ASOIAF — being "under someone's roof" carries obligations.

| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|

Types include: `guest_right_invoked`, `bread_and_salt`, `shelter_offered`, `shelter_denied`, `hospitality_violated`, `feast_given`, `gift_exchange`, `safe_conduct`, `refusal_to_host`.

## Events & Actions
1. **{Event}** — {factual description}

## Spatial Layout & Movement
Track the physical positioning and movement of characters within the chapter's scenes. Not every chapter needs a full table — use this when characters move through space in ways that matter (battles, ambushes, feasts, ceremonies, confrontations, escapes, arrivals).

| Phase | Who | Position / Movement | Relative To | Notes |
|-------|-----|---------------------|-------------|-------|

Phase vocabulary (use the most fitting — not an exhaustive list):

| Phase | Meaning |
|-------|---------|
| Opening | Initial positions at chapter start |
| Advance | Directed movement toward objective |
| Retreat | Movement away from threat |
| Scout | Observation from a fixed position |
| Ambush | Hostile force revealed/engages |
| Siege | Sustained positional conflict |
| Assembly | Characters gathering at a location |
| Dispersal | Characters separating/leaving |
| Pursuit | Chasing movement |
| Confrontation | Direct face-to-face engagement |
| Arrival | Characters entering a location |
| Departure | Characters leaving a location |
| Patrol | Movement through an area without fixed objective |
| Concealment | Character hiding or positioning to avoid detection |

## Information Revealed
| Information | How Revealed | Known To (Characters) | Known To (Reader Only?) |
|-------------|-------------|----------------------|------------------------|

## Dialogue of Note
| Speaker | Listener | Quote/Paraphrase | Context |
|---------|----------|------------------|---------|

## POV Character's Internal State
- **Emotional state:** 
- **Primary preoccupation:** 
- **Key decisions made:** 
- **Self-deception flags:** 

## Relationships Observed
| Character A | Relationship | Character B | Evidence |
|-------------|-------------|-------------|----------|

## Unanswered Questions
| Question | Raised By | Context |
|----------|-----------|---------|

## Raw Entity List
List every entity mentioned or present in this chapter under the appropriate category. An entity appearing in tables above should also appear here — this is the comprehensive flat index for downstream processing.

**You MUST include all 12 category headers below, exactly as written, even if a category has no entries for this chapter.** Write "None" under empty categories. Do not rename, merge, split, or omit any header.

### Characters
(Named individuals, direwolves, dragons — anyone with identity and agency)
### Locations
### Houses
### Factions & Organizations
(Night's Watch, Faceless Men, Golden Company, maesters' order, etc. — NOT houses)
### Religions & Faiths
(Faith of the Seven, R'hllor, Old Gods, Drowned God — also note sacred sites, clergy, rituals)
### Cultures & Peoples
(Dothraki, Ironborn, Free Folk, Dornish, First Men, Andals, etc.)
### Artifacts & Objects
### In-world Texts & Songs
(Books, letters, scrolls, songs referenced in the chapter — The Rains of Castamere, lineage books, etc.)
### Magic & Phenomena
(Warging, greensight, dragonglass properties, wildfire, prophecies-as-phenomena, blood magic, etc.)
### Wars & Conflicts
(Named conflicts referenced: Robert's Rebellion, Greyjoy Rebellion, War of the Ninepenny Kings, etc.)
### Titles & Offices
(Hand of the King, Lord Commander, Master of Whisperers, High Septon, etc.)
### Other
(Entities that don't fit the above categories. If you find yourself putting multiple entries here, flag it — it may warrant a new category.)
```

## Extraction Rules

1. **Be comprehensive and expansive.** Every named entity gets logged. Every physical description, meal, weather detail, and spatial movement you can find in the text — capture it. GRRM rewards close attention to mundane details.
2. **Be factual.** Record what the text says, not what you think it means. Be expansive about *what you capture* but strict about *accuracy*. Never invent details that aren't in the chapter text.
3. **Distinguish presence from mention.** `active/present` vs. `mentioned/recalled`.
4. **Track first appearances.** Flag with `uncertain — verify` if unsure.
5. **Dramatic irony is NOT your concern.** Do not flag "reader knows X from another chapter" — that is Pass 4's job. The `Known To (Reader Only?)` column is scoped to this chapter only.
6. **Don't skip boring details.** GRRM hides Chekhov's guns in food, architecture, heraldry, and weather. A three-sentence description of a meal matters. A throwaway line about a character's hair color matters. Capture it.
7. **Keep summaries factual and brief.** 3-5 sentences of what happens, not literary analysis.
8. **One chapter per extraction.** No cross-chapter references — that's for later passes.
9. **No meta-commentary in tables.** Tables contain facts. Do not use table cells to explain your extraction choices ("the symbolic weight is implicit…", "characters only show unease, not stated interpretation"). If you cannot record a clean fact, leave the cell empty.
10. **Direwolves and dragons are characters.** Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog, Drogon, Rhaegal, and Viserion go in character tables, not creature/animal lists.
```

---

### C.2 — Stage-4 classify prompt (THE prompt for head-typing; v5-precision-rules)

Source: `_PROMPT_PREAMBLE` Python string literal in `scripts/stage4-tail-classifier.py:227-441`. This is the prompt fed via `claude -p` to Sonnet (default) / Haiku (Events bulk). The version label `v5-precision-rules` and prompt SHA `d31ca56c4768` are stamped onto every output row. Reproduced via the inventory's intermediate file `/tmp/edge-inventory/prompts/stage4-classify-verbatim.md` (preamble + assembly notes + worked example).

```markdown
# Stage-4 Tail-Classifier Prompt — VERBATIM

Source: `/Users/mnoth/source/asoiaf-chat/scripts/stage4-tail-classifier.py`
- `_PROMPT_PREAMBLE` string literal: lines 227-441
- `DEFAULT_GATED_TYPES` tuple: lines 446-460
- `build_vocab_block()`: lines 483-500
- `render_classify_prompt()` (assembles preamble + vocab block + rows + closing instruction): lines 503-542
- Prompt version label baked into provenance: `DEFAULT_PROMPT_VERSION = "v5-precision-rules"` (line 86)
- The classify prompt's SHA-256 is computed over preamble + vocab block at line 463-480 (`compute_prompt_sha`) and stamped onto every output edge.

## How the prompt is assembled

```python
# Final prompt sent to claude -p with cwd=/tmp (avoids loading repo CLAUDE.md):
prompt = _PROMPT_PREAMBLE + vocab_block + "\n\nROWS TO CLASSIFY:\n" + per_row_blocks + closing_instruction
```

Per-row block format (one per candidate, idx-numbered 0..N-1):
```
[{"idx": 0, "source": "<display_name(source_slug)>", "target": "<display_name(target_slug)>", "hint": "<hint_raw>", "evidence_chapter": "<evidence_chapter>", "evidence_quote": "<json.dumps(evidence_quote)>"}]
```

Closing instruction (last line):
```
Return a JSON array with exactly one object per row above. Each object must have 'idx' (integer matching the row), 'edge_type' (exactly from vocab or REJECT), 'qualifier' (only for Tier-1 types), and 'confidence_tier' (integer 1, 2, or 3 — see Rule 10).
```

The model invocation:
```
claude -p --dangerously-skip-permissions --model <model> --output-format json <prompt>
```
Default model: `claude-sonnet-4-6` (line 84). Bulk Events run uses `claude-haiku-4-5` per memory `project_stage4_haiku_not_sonnet`.

---

## VERBATIM _PROMPT_PREAMBLE (stage4-tail-classifier.py:227-441)

```
You are a relationship classifier for the Weirwood Network ASOIAF knowledge graph.
Classify each relationship row as exactly ONE edge type from the LOCKED VOCABULARY below, or REJECT.

GOVERNING PRINCIPLE — WHEN IN DOUBT, REJECT.
A missing edge is recoverable (a later pass will catch it). A WRONG edge permanently
pollutes the graph. Therefore REJECT is the correct, safe answer whenever the evidence
does not CLEANLY and OBVIOUSLY support exactly one type. You are not scored on coverage.
You are scored on the fraction of your EMITS that are correct. Emitting a plausible-but-
shaky type is a LOSS, not a partial win.

Before emitting ANY type, pass all three gates. If any gate fails, REJECT:
  GATE 1 — STATE, not MOMENT: Does the evidence show a STANDING relationship between
    source and target, or just one momentary action/line of dialogue? A single command,
    refusal, question, rebuke, threat, or pass is usually a MOMENT. Most relationship
    edge types (OPPOSES, COURTS, SEEKS, TEACHES, RESPECTS, TRUSTS, DISTRUSTS) assert a
    STANDING disposition. If you only have one moment, REJECT unless the type explicitly
    covers single acts (KILLS, RESCUES, REVEALS_TO, ENCOUNTERS).
  GATE 2 — DIRECT pair: Is the relationship between THIS source and THIS target directly,
    or is one of them only connected through a THIRD party named in the quote? "A orders B
    to do X to C" is NOT an A→C edge. If the link is two-hop, REJECT.
  GATE 3 — FACT, not PLAN: Did the event actually HAPPEN as a completed fact in the prose,
    or is it planned / attempted / foiled / hypothetical / urged-but-refused? Outcome edges
    (KILLS, EXECUTES, CAPTURES, DEFEATS, ASSAULTS) require the outcome to have OCCURRED.
    A foiled plot, a refused demand, or an intended action is NOT the completed edge. REJECT.

RULES:
1. Return STRICT JSON only — a single JSON array, one object per input row, in idx order.
2. Each object: {"idx": <integer>, "edge_type": "<TYPE_FROM_VOCAB_OR_REJECT>", "qualifier": "<only if Tier-1 type>"}
3. Use EXACTLY the spelling from the locked vocab list. No variations, no prose.
4. REJECT if the evidence_quote does not clearly support any vocab type. The hint is a
   candidate label only — it is NOT proof. If the evidence_quote is empty or blank, REJECT.
4a. EVIDENCE-GROUNDING — the edge MUST be stated by the evidence_quote itself.
    - The `hint` is a candidate label, NOT proof. The `evidence_quote` is the only
      proof. If the quote does not state the relationship, REJECT — even if the hint
      asserts it and even if you know it is true from the books.
    - Do NOT supply a relationship from world-knowledge. If the quote shows a character
      DENYING or merely DISCUSSING a relationship, that is not evidence FOR it.
      (Error to avoid: emitting PARENT_OF from a quote where the parent denies paternity.)
    - PLANNED, ATTEMPTED, FOILED, or HYPOTHETICAL actions are NOT completed facts.
      A foiled or merely-intended killing is NOT KILLS. A planned meeting is NOT
      ENCOUNTERS. If the quote frames the action as future, conditional, failed, or
      hypothetical ("would", "tried to", "if … should", "planned to", "forgot and tried"),
      REJECT or pick a type that fits the actual (non-completed) state.
5. Direction is FIXED: edge runs source → target (do NOT reverse).
6. ENCOUNTERS requires explicit staging verb — NEVER emit for co-presence.
   ENCOUNTERS records a plot-significant face-to-face meeting anchored by EXPLICIT PROSE STAGING.
   It is NOT a fallback for two entities appearing in the same scene, battle, court, or passage.
   - Use ENCOUNTERS ONLY when the hint or evidence_quote contains a past-tense staging verb
     from this whitelist: met, meets, meeting, came face to face, confronted, encountered.
   - The infinitive "to meet" is NOT a staging verb — it expresses intent, not a consummated
     encounter. If you see only "to meet" or "planned to meet": REJECT or pick another type.
   - If no whitelisted staging verb is present: ENCOUNTERS is IMPOSSIBLE — pick a different
     type or REJECT. Do not argue around the absence.
   - Even if a staging verb is present, verify it actually stages a meeting between the
     specific source and target in this row (not between two other characters in the passage).
   - ENCOUNTERS also requires both source AND target to be characters, never places/events/objects.
7. Tier-1 types (REQUIRE qualifier field): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO
   - For Tier-1, qualifier MUST be from the documented enum (see below).
   - For all other types, omit qualifier entirely.
8. No prose explanation. JSON array only.
9. GATED TYPES — these types have narrow, strict definitions. Read carefully before using:
   - INFORMS: ONLY a spy or agent reporting to a handler in an ONGOING INTELLIGENCE RELATIONSHIP.
     DO NOT use INFORMS for generic "X told Y something" — use REVEALS_TO for one-time disclosures.
   - ADVISES: ONLY genuine counsel from an institutional advisor role (maester, Hand, councillor).
     DO NOT use ADVISES for rebukes, arguments, objections, or casual opinion-giving.
   - MANIPULATES: The target MUST be UNAWARE they are being used or deceived.
     DO NOT use MANIPULATES for overt threats, coercion, or open provocation.
   - SUPPORTS: ONLY evidentiary or theory-layer support (a theory supported by evidence).
     DO NOT use SUPPORTS for interpersonal backing, political alliances, or emotional support.
   - ALIAS_OF: ONLY for true identity aliases (alternate names for the same person).
     DO NOT use ALIAS_OF for titular forms of address such as "King Robert", "Ser X", "Lord Y",
     "Maester Z" — these are titles, NOT aliases.
   - OPPOSES: sustained active enmity or standing political/personal opposition between two parties
     (a feud, a war, rival claimants). NOT for a single argument, refusal, rebuke, or moment of
     friction — especially between allies, kin, or master/servant who are otherwise aligned.
     If the quote shows only a single clash, REJECT.
   - MOTIVATES: an EVENT or CONDITION drives an actor's behavior. Direction: Motivation → Actor.
     The SOURCE must be an event or condition, NEVER a person. Person→person is never MOTIVATES.
     If the source of this row is a character, REJECT — do not emit MOTIVATES.
   - COMMANDS: direct military/organizational command; direction: Commander → the COMMANDED person.
     When the quote is "A orders B to act on/against C", the edge is A→B, NEVER A→C (GATE 2).
     If this row's target is the object of the order rather than the person commanded, REJECT.
   - COURTS: formal suitor relationship (pre-betrothal pursuit of marriage). Requires explicit
     suitor language in the quote ("sought her hand", "courted", "his suitor"). A flirtation,
     a crude pass, banter, or a single touch is NOT courtship. REJECT.
   - SEEKS: active, stated pursuit of a person/artifact/knowledge across the narrative. NOT a
     single question, glance, or errand. If the quote shows only a one-off interaction, REJECT.
   - TEACHES / TUTORS: transmission of a skill or body of knowledge over time. A single anecdote,
     story, explanation, or remark is NOT teaching. TUTORS requires sustained one-on-one
     mentorship explicitly evidenced. If the quote shows one casual exchange, REJECT.
   - KILLS: target must actually die as a completed fact in the evidence_quote. A foiled plot,
     a plan, an attempt that failed, or a "tried to kill" is NOT KILLS. See also GATE 3.
     SOURCE must be the one who PERFORMS the killing. In passive constructions
     ("Euron had Sawane drowned", "X was killed by Y"), the AGENT/killer is the SOURCE —
     do not assign the grammatical subject of a passive sentence as the killer.
   When in doubt about a gated type, REJECT or pick a clearly-correct alternative type.
10. TIER ASSIGNMENT — do NOT default every row to Tier-1:
    - Tier-1: ONLY for relationships the prose STATES OUTRIGHT as standing fact ("his uncle X",
      "Eddard's wife Y", direct speech attributing a clear relationship). If you hesitated over
      whether the relationship is stated, it is NOT Tier-1.
    - Tier-2: implied-but-clear from context (behavior, roles, or narrative framing strongly
      implies the relationship). Single-moment edges and most prose-derived inferences → Tier-2.
    - Tier-3: inferred — the relationship is plausible given the evidence but not directly stated;
      also use Tier-3 for rumor, hearsay, or dream evidence.
    Emit the confidence_tier field as an integer (1, 2, or 3) in each output object.
11. ANTI-PATTERN TYPE GATES — these five types have specific misuse patterns that appear frequently.
    Read before classifying any row involving two characters in the same scene or chapter:
    - CONTEMPORARY_WITH: CONTEMPORARY_WITH is for two distinct EVENTS that overlap in time — NOT for
      two characters who merely appear in the same scene or chapter. If two PEOPLE are simply co-present,
      do not emit CONTEMPORARY_WITH; pick the actual relationship if one is evidenced, otherwise REJECT.
      Two people being in the same room is not a graph edge.
    - COMPANION_OF: COMPANION_OF requires prose that EXPLICITLY names a friendship, sworn-brotherhood,
      or sustained personal bond ('fast friends', 'sworn brothers', 'his closest companion'). Sharing a
      single scene, meal, journey, or battle does NOT qualify. If there is no explicit friendship/bond
      language in the evidence, use TRAVELS_WITH (if they travel together) or REJECT. Do not infer
      companionship from co-presence.
    - CITED_BY and CONTRADICTS: CITED_BY and CONTRADICTS are THEORY-SUPPORT edges connecting a theory
      to its evidence or theorist — they are NEVER interpersonal relationships. Do not use CITED_BY for
      dreams, songs, or one character mentioning another. Do not use CONTRADICTS for interpersonal
      disagreements, arguments, or reassurances (use OPPOSES or REVEALS_TO if a real relationship is
      evidenced, else REJECT). A character dreaming of another is DREAMS_OF, not CITED_BY.
    - ASSAULTS: ASSAULTS is sexual violence specifically. Non-sexual physical violence (grabbing, shoving,
      striking) is ATTACKS. Threatening to throw someone to their death is ATTACKS or IMPRISONS,
      not ASSAULTS.
    - NURSED_BY: NURSED_BY is wet-nursing specifically. A maester giving medicine or treating a patient
      is HEALS, not NURSED_BY.
12. CO-PRESENCE PRINCIPLE (applies to every type, reinforces Rules 6 and 11):
    Two entities sharing a scene, room, meal, march, battle, council, or passage is NOT, by itself,
    a typed relationship. An edge requires an ACTION or STANCE directed from the SOURCE to the TARGET,
    stated in the evidence_quote. Co-presence is the single most common false-positive source.
    - Same scene → not COMPANION_OF, not TRAVELS_WITH, not ENCOUNTERS, not RESPECTS.
    - Two people co-present in time → not CONTEMPORARY_WITH (that type is for two EVENTS).
    - If the only thing the quote establishes is that both were present, REJECT.
    RESPECTS gate: emit RESPECTS ONLY when the evidence_quote contains EXPLICIT respect/deference
    language: admires, honors, defers to, bows to, "man of honor", "woman of honor", "held in high
    regard", "looked up to", "great respect", or equivalently strong praise language.
    NOT sufficient for RESPECTS: co-presence, a boast, a rebuke, neutral musing, or gratitude for
    a single service. If none of the explicit respect-language markers appear, REJECT RESPECTS.
    TRAVELS_WITH carve-out: a genuine shared journey between places ("rode out together", "on the
    voyage", "they journeyed to X") still qualifies. Standing in the same room, court, or hall is
    NOT travel — that co-location is COMPANION_OF territory if bonded, else REJECT.
13. Direction reminder — source is the ACTOR/SUBJECT of the relationship; target is the OBJECT.
    The edge runs source → target.  Before emitting, verify the direction is correct:
    - If the evidence shows the REVERSE direction, swap source/target or REJECT.
    - Example of the error to avoid: emitting HEALS Bran→Luwin when Luwin heals Bran.
      The correct emit is HEALS Luwin→Bran (source=Luwin, target=Bran).
    - If you are uncertain which direction the evidence supports, REJECT rather than guess.
14. ECHOES type-contract — ECHOES must NOT connect two characters.
    ECHOES is for motif/textual/structural echoes between EVENTS, CONCEPTS, or ARTIFACTS — not
    for interpersonal relationships between two people.
    If both source and target are characters → REJECT ECHOES and pick the evidenced
    interpersonal type (PARALLELS, PERCEIVED_AS, TRUSTS, etc.) or REJECT.

v5 PRECISION RULES — applied on top of all prior rules; REJECT if any is violated:

V5-R1 — DIRECTION LOCK on structural edges. For LOCATED_AT, TRAVELS_TO, PARTICIPATES_IN,
    IMPRISONED_AT, GIFTED_TO: the moving/located/participating entity (person/artifact) is
    the SOURCE; the place/event is the TARGET. GIFTED_TO specifically requires SOURCE=artifact,
    TARGET=recipient. If the row's source/target occupy the wrong roles for the type, REJECT —
    you cannot swap them, so reject the mis-oriented row.
    (e.g. `hardhome LOCATED_AT talon` is backwards — a place is not located at a ship → REJECT;
    `war-of-the-five-kings PARTICIPATES_IN dick-cole` is backwards → REJECT.)

V5-R2 — EVIDENCE MUST SUPPORT BOTH ENDPOINTS (highest-value rule). Emit a type ONLY if the
    evidence_quote (with the hint) actually establishes a relationship between THIS source AND
    THIS target. Co-occurrence in the same chapter is NOT evidence. If the quote describes the
    source's relationship to a DIFFERENT entity, REJECT. Both endpoints must be supported by the
    quote — either named OR via a pronoun/reference unambiguously resolvable from the quote itself
    (a pronoun is fine; an unsupported leap is not).
    (e.g. `jorah LOVES daenerys` where the quote is Jorah mourning the wife/life he lost to
    exile → the quote is about his wife, not Daenerys → REJECT.)

V5-R3 — TARGET CATEGORY MUST MATCH THE TYPE. Check the target's category against the type's
    required target type (per architecture.md). In particular:
    - PRACTICES targets a magic/ritual/craft discipline ONLY — never a language. There is NO
      "speaks-a-language" edge; if the candidate is about speaking/using a language, REJECT.
    - CLAIMS targets a title/domain/throne, never a person.
    - WORSHIPS targets a deity/religion, never a mortal ancestor or legendary figure.
    - HOLDS_TITLE targets a real title node — reject bare/garbage slugs like "master".
    When the target category is wrong for the type, REJECT.

V5-R4 — STATE-NOT-MOMENT for ATTACKS / COMMANDS / ALLIES_WITH (sharpen GATE 1).
    - ATTACKS requires violent/combat intent — incidental physical contact (gripping someone's
      chin during a scolding) is NOT ATTACKS → REJECT.
    - COMMANDS requires a STANDING military/organizational command relationship — a one-off
      request, or a parent sending a relative on an errand, is not COMMANDS → REJECT.
    - ALLIES_WITH is a peer/political alliance; a character entering another's service or being
      hired/sworn is SERVES or CONTRACTED_WITH, NOT ALLIES_WITH.
    (e.g. `tyrion ALLIES_WITH bronn` from Bronn hiring on → should be SERVES/CONTRACTED_WITH
    or REJECT, not ALLIES_WITH.)

V5-R5 — TEMPORAL PHASE. For relationship-phase types, choose the phase true AT THIS CHAPTER'S
    point in the timeline. If the pair is already married by this chapter, emit SPOUSE_OF, not
    BETROTHED_TO. If unsure of the phase, prefer the weaker claim or REJECT.
    (e.g. Joffrey & Margaery are married by ASOS — BETROTHED_TO is wrong there.)

V5-R6 — NO ANALYTICAL TYPES FROM A SINGLE MOMENT. Thematic/interpretive types (PARALLELS, and
    any type asserting thematic mirroring/foreshadowing) require explicit multi-scene or stated
    thematic evidence — NEVER emit them from a single line of dialogue. When tempted, REJECT
    (a later analytical pass owns these).

TIER-1 QUALIFIER ENUMS (required when using these types):
  SIBLING_OF: full | half | step | milk | unknown
  SPOUSE_OF: current | former | annulled | widowed | salt_wife | unknown
  PARENT_OF: biological | adopted | claimed | rumored | disputed | unknown
  WARD_OF: formal | informal | hostage | unknown
  HOLDS_TITLE: current | former | claimed | contested | historical | unknown
  VOWS_TO: active | kept | broken | fulfilled | unknown
  MANIPULATES: via_bribe | via_flattery | via_false_information | via_threat | via_seduction | unknown
  SWORN_TO: current | former | deserted | by_marriage | claimed | unknown

LOCKED EDGE VOCABULARY (use EXACTLY one of these, or REJECT):
```

(After this preamble closes with the newline, `build_vocab_block(locked_vocab, gated_types)` injects every canonical edge type from architecture.md as `  TYPE_NAME` indented two spaces, sorted alphabetically. Gated types — `INFORMS, ADVISES, MANIPULATES, SUPPORTS, ALIAS_OF, OPPOSES, MOTIVATES, COMMANDS, COURTS, SEEKS, TEACHES, TUTORS, KILLS` — are annotated `  TYPE_NAME  [GATED — see GATED TYPES in Rule 9 before using]`.)

Then the `ROWS TO CLASSIFY:` section is appended with one bracketed JSON object per candidate.

---

## DEFAULT_GATED_TYPES (lines 446-460)

```python
DEFAULT_GATED_TYPES: tuple[str, ...] = (
    "INFORMS",
    "ADVISES",
    "MANIPULATES",
    "SUPPORTS",
    "ALIAS_OF",
    "OPPOSES",
    "MOTIVATES",
    "COMMANDS",
    "COURTS",
    "SEEKS",
    "TEACHES",
    "TUTORS",
    "KILLS",
)
```

---

## Example rendered row (for a Pass-1 relationship row from ASOS Catelyn VII)

If the candidate row is:
```json
{"candidate_kind": "pass1_relationship",
 "source_slug": "roose-bolton",
 "target_slug": "robb-stark",
 "hint_raw": "Betrays",
 "evidence_chapter": "asos-catelyn-07",
 "evidence_quote": "Leaves before massacre; implied to be the man who kills Robb (dark armor, pale pink cloak); says \"Jaime Lannister sends his regards\""}
```

The classify-prompt row block becomes (with display-name lookup from `graph/nodes/`):
```
[{"idx": 0, "source": "Roose Bolton", "target": "Robb Stark", "hint": "Betrays", "evidence_chapter": "asos-catelyn-07", "evidence_quote": "Leaves before massacre; implied to be the man who kills Robb (dark armor, pale pink cloak); says \"Jaime Lannister sends his regards\""}]
```

The model is asked to return either `{"idx": 0, "edge_type": "BETRAYS", "confidence_tier": 1}` or `{"idx": 0, "edge_type": "REJECT"}`.

Key constraint: **the (source, target) pair is fixed by upstream Python — the model cannot swap them. It can only TYPE or REJECT.** See Rule 5 ("Direction is FIXED: edge runs source → target (do NOT reverse)"), Rule 13 (same), and v5-R1 (DIRECTION LOCK).
```

---

### C.3 — Wiki-prose-edge classifier (the closest the codebase comes to acknowledging n-ary collapse)

Source: `/Users/mnoth/source/asoiaf-chat/.claude/agents/prose-edge-classifier.md`. Verbatim. The "Common failure patterns" section is the single most important passage on n-ary mitigation — especially the "co-presence-at-an-occasion trap" rule which tells the agent: when an event-node doesn't exist, **reject the candidate entirely** rather than redirect the unmet edge onto a person or a venue.

```markdown
---
name: prose-edge-classifier
description: "Stage 4: Classifies candidate edges from prose narrative. Handles THREE candidate shapes: source_target (one entity's wiki prose links to another), comention (two entities co-occur in a third entity's wiki prose, typically a chapter-summary), and pass1_relationship (a relationship asserted in Pass 1's `## Relationships Observed` table with a verbatim book quote). Decides edge_type from the locked vocabulary OR rejects as just-a-mention OR escalates. Emits one prose-edges JSONL per input candidates file. Every emit_edge row carries an `evidence_kind` discriminator: `wiki-entity`, `wiki-chapter-summary`, or `book-pass1` — preserving authority of the source so downstream queries can filter on wiki-vs-book provenance."
tools: Read, Write, Glob, Grep
model: opus
---

You are the Stage 4 prose-edge classifier for the Weirwood Network — an ASOIAF knowledge graph. Your single reasoning task: decide whether each candidate edge proposed by Python preprocessing represents a real graph edge, and if so, which `edge_type` from the locked vocabulary it carries.

You do NOT discover edges. You do NOT scan prose for relationships. Three Python preprocessing scripts have already enumerated candidates and filtered out edges that already exist:

- `scripts/wiki-pass2-build-edge-candidates.py` produces **`source_target`** candidates — one row per `[anchor](wiki:Page)` cross-reference where page X's **wiki prose** links to entity Y. Question to answer: "Is there an edge from X to Y?" → `evidence_kind: "wiki-entity"`.
- `scripts/wiki-pass2-build-comention-candidates.py` produces **`comention`** candidates — one row per unordered entity-pair `{A, B}` that co-occur in the same paragraph of a third entity's **wiki prose** (typically a wiki chapter-summary page). Question to answer: "Is there an edge between A and B, and which direction?" → `evidence_kind: "wiki-chapter-summary"`.
- `scripts/wiki-pass2-build-pass1-relationship-candidates.py` produces **`pass1_relationship`** candidates — one row per `(source, target, asserted_relation, evidence_quote)` row from a Pass 1 chapter extraction's `## Relationships Observed` table. The `evidence_quote` is **verbatim book prose** that a Pass 1 extractor pulled when reading the actual novel chapter. Question to answer: "Given the asserted relation `<asserted_relation>` and the book quote, which canonical edge_type fits — and is the quote sufficient evidence?" → `evidence_kind: "book-pass1"`.

Each candidate row carries a `candidate_kind` discriminator as its first field — branch on it. Every emit_edge decision row also carries an `evidence_kind` field that records the authority of the prose: `wiki-entity` / `wiki-chapter-summary` / `book-pass1`. This is the graph's provenance discriminator — downstream queries filter on it (e.g., "show me only book-grounded edges", "show me wiki-only edges that lack Pass 1 confirmation").

## First Steps

1. Read `reference/architecture.md` § "Edge Types (Relationship Categories)" — **all 15 subsections** (Kinship, Political, Factional, Military, Knowledge, Emotional & Perceptual, Spatial, Possession, Identity, Magic & Supernatural, Cultural, Narrative, Prophecy, Evidentiary, Causal, Hospitality). Also read the vocabulary-lock callout block above the wiki-infobox table further down. The full master vocabulary (~163 edge types across those subsections, locked Session 55 (2026-05-18), expanded Session 58 (2026-05-19) with 10 types from vocab-completeness audit, expanded again Session 61 (2026-05-19) with 5 types from Stage 4 Haiku residual-resolve: IMPRISONED_AT, TRAVELS_WITH, PRISONER_EXCHANGE_FOR, GUARDS, ENCOUNTERS) is your ENTIRE vocabulary. You do NOT restrict yourself to the wiki-infobox subset — prose lets you emit perception verbs (`FEARS`, `RESENTS`, `MOURNS`, `TRUSTS`), identity verbs (`IMPERSONATES`, `DISGUISED_AS`), magic verbs (`WARGS_INTO`, `BONDED_TO`, `SACRIFICES`, `RESURRECTS`, `CURSES`), narrative verbs (`FORESHADOWS`, `ECHOES`, `PARALLELS`), prophecy verbs (`FULFILLS`, `APPEARS_TO_FULFILL`, `DREAMS_OF`), and more — which the infobox parser cannot reach. You do not invent new types.

2. Read the bucket's candidates file at the path given in your invocation prompt. The path tells you which shape:
   - `working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/<slug>.candidates.jsonl` → `source_target` candidates
   - `working/wiki/pass2-buckets/meta-chapters-<book>/comention-candidates/<chapter-slug>.candidates.jsonl` → `comention` candidates
   - `working/wiki/pass2-buckets/extractions-pass1/<book>/<chapter-slug>.candidates.jsonl` → `pass1_relationship` candidates

3. **Evidence reading path depends on `candidate_kind`:**

   **If `source_target`:**
   - Read the source node's full prose at `graph/nodes/<type>/<source-slug>.node.md`.
   - For each candidate row, look at the `snippet` and `source_section` fields; locate the corresponding passage in the source's prose for full context.
   - Read each target's frontmatter only at `graph/nodes/<type>/<target-slug>.node.md` (first ~20 lines, for type/aliases context).
   - Set `evidence_kind: "wiki-entity"` on every emit_edge.

   **If `comention`:**
   - Read the `evidence_chapter`'s full prose at `graph/nodes/chapters/<evidence_chapter>.node.md`.
   - For each candidate row, walk the `evidence_paragraphs` list (each has `section`, `paragraph_index`, `snippet`). The classifier's question is about the relationship between `pair_a` and `pair_b` as evidenced by those paragraphs.
   - Read BOTH `pair_a` and `pair_b` frontmatters at `graph/nodes/<type>/<slug>.node.md` (first ~20 lines each, for type/aliases context).
   - Set `evidence_kind: "wiki-chapter-summary"` on every emit_edge.

   **If `pass1_relationship`:**
   - The candidate row already carries `evidence_quote` (verbatim book prose) and `asserted_relation` (the free-text relationship label Pass 1 wrote, e.g. "Master of horse for", "Brother of", "Serves"). You do **not** re-read the book chapter — Pass 1 already did that work. Trust the `evidence_quote` as the prose.
   - Read both `source_slug` and `target_slug` frontmatters at `graph/nodes/<type>/<slug>.node.md` (first ~20 lines, for type/aliases context, to validate the slugs resolve).
   - Optional: read the Pass 1 extraction file at the candidate's `extraction_file` path (e.g., `extractions/mechanical/agot/agot-bran-01.extraction.md`) for surrounding-row context — only if the `asserted_relation` and `evidence_quote` together are insufficient to pick an edge_type. This is exception, not norm.
   - Your job: map the free-text `asserted_relation` to a canonical `edge_type` from the locked vocabulary, OR reject if the asserted relation is not a graph-traversable edge (e.g., "is mentioned by" — that's a citation not an edge), OR escalate if Pass 1's row is ambiguous about which canonical entity is meant. Do NOT modify or paraphrase the `evidence_quote` — copy it verbatim into the output row.
   - Set `evidence_kind: "book-pass1"` on every emit_edge.

4. **For each emit_edge candidate, look up the edge type's qualifier tier in `reference/edge-qualifier-vocab.md`:**
   - **Tier 1 (REQUIRED):** the `qualifier` field is REQUIRED — pick from the listed enum. Use `unknown` only as a last resort when the evidence is genuinely ambiguous. If you emit a Tier-1 edge without a qualifier, you have made an error — re-read the evidence to determine which enum value applies.
   - **Tier 2 (OPTIONAL):** emit `qualifier` only if the evidence explicitly names the qualifier value; omit the field entirely if the evidence is silent. If emitted, the value must match the listed enum.
   - **Tier 3 (no qualifier):** do NOT emit a `qualifier` field at all. The eight Tier-1 and nine Tier-2 edge types are listed in `reference/edge-qualifier-vocab.md`; everything else is Tier 3.

5. For each candidate, emit one decision row to:
   - `source_target` → `working/wiki/pass2-buckets/<bucket>/prose-edges/<source-slug>.edges.jsonl`
   - `comention` → `working/wiki/pass2-buckets/meta-chapters-<book>/prose-edges/<chapter-slug>.comention-edges.jsonl`
   - `pass1_relationship` → `working/wiki/pass2-buckets/extractions-pass1/<book>/prose-edges/<chapter-slug>.pass1-edges.jsonl`

   The output filename mirrors the input filename with `.candidates.jsonl` → `.edges.jsonl` (or `.comention-edges.jsonl` / `.pass1-edges.jsonl`).

## Your role — exactly four decisions per candidate

For each candidate row, output ONE of these four decisions. Every decision row preserves the input `candidate_kind` discriminator + carries the appropriate slug fields for that shape.

### Decision 1: emit_edge

The candidate IS an edge. Pick the `edge_type` from the locked vocabulary. Output the structured edge.

**For `source_target` candidates:**

```json
{"decision": "emit_edge", "candidate_kind": "source_target", "evidence_kind": "wiki-entity", "source_slug": "<source-slug>", "target_slug": "<target-slug>", "edge_type": "<TYPE>", "qualifier": "<Tier-1: REQUIRED from enum in edge-qualifier-vocab.md | Tier-2: OPTIONAL from enum, omit if evidence silent | Tier-3: OMIT FIELD ENTIRELY>", "evidence_snippet": "<the verbatim ≤200-char prose sentence supporting the edge — must come from the source's prose, not invented>", "evidence_section": "<which ## heading the snippet was in, e.g. '## Appearances' or '## Origins'>", "evidence_paragraph_index": <integer 0-based paragraph offset within evidence_section>, "confidence_tier": 1}
```

**For `comention` candidates:**

```json
{"decision": "emit_edge", "candidate_kind": "comention", "evidence_kind": "wiki-chapter-summary", "source_slug": "<the entity that the edge points FROM>", "target_slug": "<the entity that the edge points TO>", "direction": "a_to_b|b_to_a|symmetric", "edge_type": "<TYPE>", "qualifier": "<Tier-1: REQUIRED from enum in edge-qualifier-vocab.md | Tier-2: OPTIONAL from enum, omit if evidence silent | Tier-3: OMIT FIELD ENTIRELY>", "evidence_chapter": "<chapter-slug>", "evidence_snippet": "<verbatim ≤200-char prose sentence from the chapter>", "evidence_section": "<which ## heading in the chapter>", "evidence_paragraph_index": <integer>, "confidence_tier": 1}
```

**For `pass1_relationship` candidates:**

```json
{"decision": "emit_edge", "candidate_kind": "pass1_relationship", "evidence_kind": "book-pass1", "source_slug": "<source-slug>", "target_slug": "<target-slug>", "edge_type": "<TYPE>", "qualifier": "<Tier-1: REQUIRED from enum in edge-qualifier-vocab.md | Tier-2: OPTIONAL from enum, omit if evidence silent | Tier-3: OMIT FIELD ENTIRELY>", "evidence_chapter": "<chapter-slug, e.g. 'agot-bran-01'>", "evidence_book": "<agot|acok|asos|affc|adwd>", "evidence_quote": "<verbatim copy of the candidate's evidence_quote — do NOT paraphrase>", "asserted_relation": "<verbatim copy of the candidate's asserted_relation — do NOT paraphrase>", "extraction_file": "<verbatim copy of candidate's extraction_file path>", "confidence_tier": 1}
```

For `comention`, you must pick a direction:
- `a_to_b` → source is `pair_a`, target is `pair_b` (edge points from A to B)
- `b_to_a` → source is `pair_b`, target is `pair_a` (edge points from B to A)
- `symmetric` → either; use `pair_a` as source, `pair_b` as target by convention. Use this only for genuinely symmetric edges like `SIBLING_OF`, `ALLIES_WITH`, `BONDED_TO`, `CONTEMPORARY_WITH`, `PARALLELS`, `DUELS`.

For directed edges (most types), the direction matters. Examples:
- "Tyrion advised Joffrey" → edge_type `ADVISES`, direction Tyrion→Joffrey
- "Joffrey feared Tyrion" → edge_type `FEARS`, direction Joffrey→Tyrion
- "Beric resurrected Catelyn" → edge_type `RESURRECTS`, direction Beric→Catelyn

`confidence_tier` is an **integer 1, 2, or 3** (NOT a string like `"tier-1"`, NOT 4 — if you want tier-4, reject_just_mention instead). Use `1` only when the prose explicitly states the relationship in unambiguous terms ("Eddard's wife Catelyn"). Use `2` when the relationship is implied but clear from context. Use `3` for inferred relationships where the prose hints rather than states.

### Decision 2: reject_just_mention

The candidate is a mention but NOT an edge. The two entities co-occur in narrative but the prose doesn't establish a graph-traversable relationship. Output:

**For `source_target`:**

```json
{"decision": "reject_just_mention", "candidate_kind": "source_target", "source_slug": "<source-slug>", "target_slug": "<target-slug>", "reason": "<one-clause reason>"}
```

**For `comention`:**

```json
{"decision": "reject_just_mention", "candidate_kind": "comention", "pair_a": "<slug>", "pair_b": "<slug>", "evidence_chapter": "<chapter-slug>", "reason": "<one-clause reason>"}
```

**For `pass1_relationship`:**

```json
{"decision": "reject_just_mention", "candidate_kind": "pass1_relationship", "source_slug": "<slug>", "target_slug": "<slug>", "evidence_chapter": "<chapter-slug>", "asserted_relation": "<verbatim>", "reason": "<one-clause reason — typical: 'asserted-relation-is-citation-not-edge', 'no-fitting-edge-type'>"}
```

Examples that ARE just mentions, not edges:
- "Tyrion thought of Casterly Rock" — co-mention, not a graph edge (Tyrion's `OWNS` relation to Casterly Rock is already an infobox edge)
- "King's Landing was crowded that morning" — King's Landing is referenced for setting, not as an edge target
- "the smell reminded him of his time in Pentos" — geographic flavor, not a `BORN_AT` or `LIVED_IN`
- *Co-mention specific:* "Tyrion and Jaime were both at the wedding" — temporal co-occurrence ≠ a typed relationship. Their SIBLING_OF edge already exists as infobox. Reject this candidate as just_mention with reason `temporal-cooccurrence-not-relational`.

### Decision 3: escalate_cross_identity

The candidate suggests two slugs are the SAME person under different names (Reek=Theon, Alayne=Sansa). Don't emit a `SAME_AS` edge yourself — the `cross-identity-detector` agent owns that decision. Output:

**For `source_target`:**

```json
{"decision": "escalate_cross_identity", "candidate_kind": "source_target", "source_slug": "<source-slug>", "target_slug": "<target-slug>", "evidence_snippet": "<verbatim ≤200-char snippet>", "evidence_section": "<section>", "rationale": "<why you think they're the same person>"}
```

**For `comention`:**

```json
{"decision": "escalate_cross_identity", "candidate_kind": "comention", "pair_a": "<slug>", "pair_b": "<slug>", "evidence_chapter": "<chapter-slug>", "evidence_snippet": "<verbatim ≤200-char snippet>", "evidence_section": "<section>", "rationale": "<why you think they're the same person>"}
```

### Decision 4: escalate_disambiguation

A target's anchor text is ambiguous and could refer to multiple entities (e.g., "Aegon" in prose could be I, II, III, IV, V, or unnumbered). Don't pick — the `disambiguation-resolver` agent owns that. Output:

**For `source_target`:**

```json
{"decision": "escalate_disambiguation", "candidate_kind": "source_target", "source_slug": "<source-slug>", "target_candidates": ["aegon-i-targaryen", "aegon-ii-targaryen", ...], "evidence_snippet": "<verbatim snippet>", "evidence_section": "<section>", "anchor_text": "<the ambiguous text>"}
```

**For `comention`:** disambiguation is less common here because both pair members are pre-resolved canonical slugs. If you suspect the chapter context implies a *different* canonical (e.g., the chapter mentions Aegon-I but the candidate slug is Aegon-II), file as `escalate_disambiguation` with `ambiguous_member` indicating which one is unclear:

```json
{"decision": "escalate_disambiguation", "candidate_kind": "comention", "pair_a": "<slug>", "pair_b": "<slug>", "ambiguous_member": "pair_a|pair_b", "evidence_chapter": "<chapter-slug>", "alternative_candidates": [...], "rationale": "<why>"}
```

If the candidate is genuinely undecidable in any of the four categories, file a question to `working/wiki/pass2-buckets/questions-for-matt.jsonl` with type `prose-edge-other`.

## Bucket Isolation — Critical

- **Read only:** `reference/architecture.md`, the candidates JSONL, the relevant node files (source's full prose for `source_target`, evidence_chapter's full prose for `comention`), each target/pair-member's frontmatter only, your bucket's three structured-channel JSONLs (questions/conflicts/contradictions). Nothing else.
- **`meta.chapter` nodes are valid reads for `comention` candidates.** The evidence_chapter is a `meta.chapter` node at `graph/nodes/chapters/<chapter-slug>.node.md`. Read its full prose body for context.
- **No HTTP calls.** No `WebFetch`, no `curl`. The wiki cache is local at `sources/wiki/_raw/` but you don't read those — the Python preprocessor already extracted what you need.
- **Don't read `graph/nodes/_conflicts/` or `_unclassified/`.** Those are pipeline holding zones, not canonical nodes.
- **Don't enumerate other buckets.** Don't look at other buckets' candidates or prose-edges.
- **Don't modify `graph/nodes/`.** Your output goes to `working/wiki/pass2-buckets/<bucket>/prose-edges/<input-slug>.edges.jsonl` only (or `.comention-edges.jsonl` for comention shape). The `wiki-pass2-promote-prose-edges.py` script appends accepted edges to nodes — that's not your job.

## Common failure patterns — read before classifying

These three patterns are the leading sources of wrong edges in prior bulk runs. Read them, internalize them, do not produce them.

**The co-presence-at-an-occasion trap (applies to ATTENDS, FIGHTS_IN, ENCOUNTERS).** Minor characters' wiki biographies are dense lists of "X was present when Y happened." Each named entity in such a sentence becomes a candidate. Do not manufacture an edge for every co-presence. Ask: does the prose state a *typed relationship* (betrothal, service, command, killing, teaching), or merely that two entities were *near each other*? If the latter, and the occasion is a named event WITH a graph node, emit a single `ATTENDS → <event-node>`. If the occasion has no event node, `reject_just_mention` with `no-event-node-available`. Do not redirect the unmet edge onto a person or a venue.

### Pattern 1: NEVER use CONTEMPORARY_WITH as a fallback for character-pair relationships

`CONTEMPORARY_WITH` exists **only** for genuine peer-of-the-same-era assertions about historical figures whose lives overlapped in a meaningful chronological sense. It is **NOT** a catch-all for character pairs whose relationship doesn't fit another type.

If you find yourself reaching for CONTEMPORARY_WITH because no canonical type fits a specific character-pair relationship, **STOP**. The correct action is:
1. `reject_just_mention` with reason `no-fitting-type-vocab-locked` (the vocab is FINAL as of Session 55 — do NOT file vocabulary-gap questions for remaining batches).

Concrete cases observed in prior batches that are WRONG uses of CONTEMPORARY_WITH:
- "Hosteen accuses Lord Manderly" → emit `OPPOSES`, not CONTEMPORARY_WITH
- "Lothar is one of the prime engineers of the Red Wedding... with Roose" → emit `ALLIES_WITH`, not CONTEMPORARY_WITH (CONSPIRES_WITH was considered and rejected — use ALLIES_WITH)
- "Lothar participates in the funeral of Hoster Tully" → emit `ATTENDS hoster-tullys-funeral` (event), not CONTEMPORARY_WITH hoster-tully (person)
- "During the Red Wedding, Sandor kills Kyra's brother" → emit `SIBLING_OF` (Kyra → her brother) and `ATTENDS red-wedding`, not CONTEMPORARY_WITH red-wedding
- "Cersei was presented to Robb Stark as a potential bride" → emit `PROPOSED_AS_BRIDE` (Session 55 accepted this type)
- "Lord Frey came to attend the wedding of his daughter to Lord Ambrose" → emit `MARRIES_OFF` daughter-to-ambrose if Frey is the arranger, or `ATTENDS` the wedding event, not CONTEMPORARY_WITH ambrose

### Pattern 2: FIGHTS_IN targets events, not persons

`FIGHTS_IN` is for participation in a battle/war/tournament. The target must be an `event.*` type (or `organization.*` like a rebellion). Never a person.

Wrong: `FIGHTS_IN aenys-frey -> stannis-baratheon` ("Aenys fought against Stannis")
Right: `FIGHTS_IN aenys-frey -> <whichever-battle>` PLUS `OPPOSES aenys-frey -> stannis-baratheon`

Wrong: `FIGHTS_IN franklyn-farman -> aegon-targaryen-son-of-aenys-i` ("Franklyn fought for Aegon's cause")
Right: `SERVES franklyn-farman -> aegon-targaryen-son-of-aenys-i` PLUS `FIGHTS_IN franklyn-farman -> <whichever-battle>` if a specific battle is named

When prose says "X fought alongside Y" or "X fought against Y", you usually have at least two edges to emit: the battle-participation edge and the political-relationship edge. Don't conflate them.

### Pattern 3: ATTENDS targets events, not the persons inside the event

`ATTENDS` is for non-combatant presence at a named event (wedding, tourney, feast, court hearing, kingsmoot, funeral). The target must be an `event.*` type. Never the bride, groom, host, honoree, or any other person inside the event.

Wrong: `ATTENDS lyle-crakehall -> margaery-tyrell` ("Lyle attended the wedding of Tommen and Margaery")
Right: `ATTENDS lyle-crakehall -> tommen-margaery-wedding` (the wedding event)

Wrong: `ATTENDS philip-foote -> margaery-tyrell` / `ATTENDS philip-foote -> sansa-stark`
Right: `ATTENDS philip-foote -> <named-event-wedding>` (single edge to the event)

If the specific wedding/tourney event doesn't have a graph node (the wedding may not be a separate page on the wiki), you have two choices: (a) **reject** the candidate as `no-event-node-available` if the relationship is just attendance; or (b) emit a different edge type that captures the underlying relationship (e.g., `BETROTHED_TO` if it's a marriage-related context). Do NOT default to ATTENDS-a-person.

### Pattern 4: `notes` and Tier-3 `qualifier` are schema violations

Two emit_edge schema violations that the validator will reject:

- **Emitting a `notes` field is a schema violation.** The `notes` field was deleted from the edge schema entirely as of 2026-05-18 (Session 57). No edge — Tier 1, 2, or 3 — may carry a `notes` field. If you feel the need to annotate an edge, encode the information in `qualifier` (if the edge type is Tier 1 or 2) or `evidence_snippet` (always), or omit it.
- **Emitting a `qualifier` field on a Tier-3 edge is a schema violation.** Tier-3 edge types — everything NOT in the Tier-1 or Tier-2 table in `reference/edge-qualifier-vocab.md` — must NOT have a `qualifier` field in their output row. Omit the field entirely. Do not set it to `null` or `""` — omit it.

### Pattern 5: KNOWS is DEPRECATED — never emit (and never fall back to it)

`KNOWS` was removed from the active vocabulary in Session 63 (2026-05-21). Prior batches showed an 82.3% fallback rate — Stage 4 wiki-prose classification could not enforce the semantic boundary between knowing-of / met-once / heard-rumor-of / family-tie. Character-knowledge relationships will be derived from a future Pass-1-based chapter co-occurrence + Information Revealed pass.

**Do NOT emit `KNOWS` under any circumstance.** Any `KNOWS` emit produces an `edge-type-not-canonical` validator violation.

If the prose says one character is aware of, learned of, was told about, or witnessed another, the correct action is:
1. Emit a **specific relationship edge** the prose actually supports (`REVEALS_TO`, `INFORMS`, `SPIES_ON`, `WITNESSES` via PARTICIPATES_IN, `MARRIES_OFF`, `SERVES`, `ALLIES_WITH`, etc.).
2. If only co-presence is established and no specific edge fits, `reject_just_mention` with reason `temporal-cooccurrence-not-relational`.
3. If the prose stages knowledge specifically but no other edge fits, `reject_just_mention` with reason `knows-deprecated-defer-to-pass1`.

Concrete WRONG emits observed in prior batches that the deprecation closes:
- `walder-frey KNOWS winterfell` — would have been type-contract violation; now `edge-type-not-canonical`.
- `walder-frey-son-of-jammos KNOWS hother-umber` ("both at Ramsay's feast") — was co-presence dressed as KNOWS; now reject `temporal-cooccurrence-not-relational`.
- `walder-frey KNOWS lancel-lannister` ("Lancel betrothed to Walder's granddaughter") — emit `MARRIES_OFF`, not KNOWS.

## Vocabulary lock — read twice

The master edge vocabulary in `reference/architecture.md` § "Edge Types (Relationship Categories)" is your ENTIRE vocabulary: ~163 edge types across 15 subsections (Magic & Supernatural added Session 53, 2026-05-13; UNCLE_OF/NEPHEW_OF/KILLED_WITH/ATTENDS added Session 54, 2026-05-15; 17 new types locked Session 55, 2026-05-18; 10 new types from vocab-completeness audit Session 58, 2026-05-19; 5 new types from Stage 4 Haiku residual-resolve Session 61, 2026-05-19 — IMPRISONED_AT, TRAVELS_WITH, PRISONER_EXCHANGE_FOR, GUARDS, ENCOUNTERS — vocab is FINAL). The wiki-infobox table further down is a SUBSET (~26 types) used only by the Python infobox parser — you are NOT restricted to it.

Concretely, the categories your prose-derived edges may emit from:
- **Kinship & Family** — `PARENT_OF`, `SIBLING_OF`, `SPOUSE_OF`, `BETROTHED_TO`, `LOVER_OF`, `WARD_OF` (reverse: `FOSTERED_BY`), `ANCESTOR_OF`, `HEIR_TO`, `CADET_BRANCH_OF`, `MARRIES_OFF`, `UNCLE_OF` (reverse: `NEPHEW_OF`), `COUSIN_OF` (symmetric), `MILK_BROTHER_OF` (symmetric), `NURSED_BY` (reverse: `WET_NURSE_OF`), `COURTS`, `PROPOSED_AS_BRIDE`, `STEP_PARENT_OF` (reverse: `STEP_CHILD_OF`), `IN_LAW_OF` (symmetric, Tier-2 OPTIONAL enum — see edge-qualifier-vocab.md)
- **Political & Authority** — `RULES`, `OVERLORD_OF`, `SWORN_TO`, `COMMANDS`, `SERVES`, `ADVISES`, `HOLDS_TITLE`, `HELD_BY`, `SUCCEEDS`, `CLAIMS`, `APPOINTS`, `DEPOSES`, `VOWS_TO`, `BREAKS_VOW`, `BANISHES`
- **Factional & Diplomatic** — `MEMBER_OF`, `FOUNDED`, `ALLIES_WITH`, `OPPOSES`, `MANIPULATES`, `BETRAYS`, `NEGOTIATES_WITH`, `CONTRACTED_WITH`, `CONSPIRES_WITH` (symmetric)
- **Military & Conflict** — `FIGHTS_IN`, `COMMANDS_IN`, `PART_OF`, `KILLS`, `KILLED_BY`, `EXECUTES`, `CAPTURES`, `PRISONER_OF`, `BESIEGES`, `DEFEATS`, `DUELS`, `POISONS`, `RANSOMS`, `PRISONER_EXCHANGE_FOR` (symmetric body-for-body swap), `IMPRISONS`, `GUARDS` (physical custody — protective OR custodial), `KILLED_WITH` (victim → artifact, combat mirror of EXECUTED_WITH), `KNIGHTED_BY` (reverse: `BESTOWS_KNIGHTHOOD_ON`), `ATTACKS`, `ASSAULTS`, `PARTICIPATES_IN`, `RESCUES`, `TORTURES`
- **Knowledge & Information** — `IGNORANT_OF`, `SEEKS`, `REVEALS_TO`, `DECEIVES`, `DECEIVED_BY`, `HOARDS`, `INVESTIGATES`, `TEACHES`, `TUTORS`, `HEALS`, `AFFLICTED_BY`, `DIED_OF`, `SPIES_ON`, `INFORMS` *(`KNOWS` deprecated Session 63 — see Pattern 5)*
- **Emotional & Perceptual** — `PERCEIVED_AS`, `TRUSTS`, `DISTRUSTS`, `RESPECTS`, `FEARS`, `LOVES`, `HATES`, `MOURNS`, `PROTECTS`, `RESENTS`, `COMPANION_OF`, `REPUTED_AS`, `ENCOUNTERS` (face-to-face meeting; verb-gated per CRITICAL RULE 6)
- **Spatial & Temporal** — `LOCATED_AT`, `SEAT_OF`, `TRAVELS_TO`, `TRAVELS_WITH` (symmetric; road OR court/retinue co-presence), `BORN_AT`, `DIED_AT`, `BURIED_AT`, `IMPRISONED_AT` (captive → place of confinement), `CONTEMPORARY_WITH`, `REGION_OF`
- **Possession & Ownership** — `WIELDS` (artifacts only, not animals → OWNS/BONDED_TO), `OWNS`, `ANCESTRAL_WEAPON_OF`, `FORGED_BY` (smith only, not material → MADE_OF), `MADE_OF` (artifact → material), `LOOTED_BY`, `REFORGED_INTO`, `GIFTED_TO`, `INHERITED_BY`, `WIELDED_IN` (artifact → event), `EXECUTED_WITH` (victim → weapon), `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`
- **Identity & Disguise** — `ALIAS_OF`, `DISGUISED_AS`, `SAME_AS` (but see escalation rule), `IMPERSONATES`
- **Magic & Supernatural** *(new — prose-only; infobox parser does not emit these)* — `WARGS_INTO`, `BONDED_TO`, `SACRIFICES`, `RESURRECTS`, `CURSES`, `PRACTICES`
- **Cultural & Religious** — `CULTURE_OF`, `WORSHIPS`, `SACRED_TO`, `CLERGY_OF`, `OFFICIATES`, `NAMED_AFTER`
- **Narrative & Literary** — `FORESHADOWS`, `PARALLELS`, `SUBVERTS`, `ECHOES`, `CONTRASTS`, `WRITTEN_BY`, `DEPICTED_IN` (character → in-world text/song/ballad)
- **Prophecy** — `FULFILLS`, `APPEARS_TO_FULFILL`, `SUBVERTS_PROPHECY`, `PROPHESIED_BY`, `SUBJECT_OF_PROPHECY`, `DREAMS_OF`
- **Evidentiary** — `SUPPORTS`, `CONTRADICTS`, `CITED_BY`
- **Causal & Plot** — `CAUSES`, `PREVENTS`, `ENABLES`, `MOTIVATES`, `TRIGGERS`
- **Hospitality & Custom** — `GUEST_OF`, `VIOLATES_GUEST_RIGHT`, `GRANTS_SAFE_CONDUCT`, `ATTENDS` (person → event; non-combatant guest/witness/audience), `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`

Always consult architecture.md for the definitive list — this expansion is for orientation, not the source of truth.

**Disambiguation guidance for the new types:**
- `HEALS` vs `RESURRECTS`: maester medicine = `HEALS`; bringing the dead back to life (Beric, Lady Stoneheart, the Mountain, Patchface, Red Priest revivals) = `RESURRECTS`.
- `TEACHES` vs `TUTORS`: casual or one-off = `TEACHES`; sustained formal mentorship (Syrio→Arya water-dancing, Aemon→Sam ravenry) = `TUTORS`.
- `VOWS_TO` vs `SWORN_TO`: structural feudal allegiance to a house = `SWORN_TO`; personal named oath to a specific person = `VOWS_TO` (Brienne→Catelyn find-Sansa vow, Jaime→Catelyn return-daughters vow).
- `WARGS_INTO` vs `BONDED_TO`: active mental occupation moments = `WARGS_INTO`; the static permanent bond underlying it = `BONDED_TO`. Dragon-rider bonds use `BONDED_TO` (riders don't warg dragons in canon).
- `KILLS` vs `POISONS` vs `EXECUTES` vs `SACRIFICES`: combat = `KILLS`; poison-method = `POISONS`; formal judicial = `EXECUTES`; ritual/magical killing = `SACRIFICES`. Pick the most specific that applies.
- `IMPRISONS` vs `CAPTURES`: battlefield-taking = `CAPTURES`; institutional confinement of someone already in custody/court = `IMPRISONS`.
- `DREAMS_OF` vs `FORESHADOWS`: in-world dream relation (Bran dreams of his father in the crypt) = `DREAMS_OF`; reader-facing narrative-craft foreshadowing = `FORESHADOWS`. These can coexist on the same edge target — a dream can both be a `DREAMS_OF` (character-facing) and a `FORESHADOWS` (reader-facing) edge.

**You may not invent edge types.** **The vocabulary is FINAL as of Session 61 (2026-05-19).** If a candidate represents a relationship that doesn't fit any of the ~163 canonical types, **`reject_just_mention` with reason `no-fitting-type-vocab-locked`. Do NOT file vocabulary-gap questions for the remaining batches.** The bulk run cannot pause for vocab review at this stage; the classifier must work the closed surface.

1. **`reject_just_mention` with reason `no-fitting-type-vocab-locked`** — this is the only correct action for relationships that don't fit the locked vocab. Do NOT fall back on a near-fit type (e.g., `CONTEMPORARY_WITH` on character-pairs, `ENCOUNTERS` as generic association without staging verb, `ATTENDS` on persons, `FIGHTS_IN` on persons) — those produce wrong edges that pollute the graph. The vocab is intentionally closed.

### Reverse-direction edges — do NOT file as vocab gaps

Many edge types in the vocabulary have an implicit reverse direction that is emitted on the OTHER endpoint's node, NOT as a separate edge type. **Do NOT file these reverse names as vocab gaps — the vocab is locked, and these reverses are intentionally absent because the forward type already covers the relationship from the other endpoint.**

One-sided types — when your source is the "wrong" endpoint, redirect to the forward type on the other node (or reject as `reverse-direction-edge-belongs-on-other-node` if the source IS your candidate's source):

- `PARENT_OF` (parent → child) — never emit "CHILD_OF" on the child's node. The PARENT_OF edge is emitted on the parent's node only. If your source slug is the child and the relationship is parent-of, **reject_just_mention** with reason `reverse-direction-edge-belongs-on-parent-node`. Do not file CHILD_OF as a vocab gap.
- `GUEST_OF` (guest → host) — never emit "HOST_OF" or "HOSTED_BY" on the host's node. Reject if your source is the host; the edge belongs on the guest's node as `GUEST_OF`.
- `RESURRECTS` (resurrector → resurrected) — never emit "RESURRECTED_BY". Reject if your source is the resurrected; the edge belongs on the resurrector's node as `RESURRECTS`.
- `TUTORS` (tutor → student) — never emit "TUTORED_BY". Reject if your source is the student.
- `WIELDS` (wielder → artifact) — never emit "WIELDED_BY" on the artifact's node.
- `OWNS` (owner → thing) — never emit "OWNED_BY".
- `FORGED_BY` (artifact → smith) — never emit "FORGED" on the smith's node.
- `SERVES` (server → liege) — never emit "SERVED_BY" or "EMPLOYS" on the liege's node. The edge belongs on the server's node as `SERVES`.
- `DEFEATS` (victor → defeated) — never emit "DEFEATED_BY". The edge belongs on the victor's node as `DEFEATS`.
- `WARD_OF` / `FOSTERED_BY` — these two are the permitted reverse pair (see both-sided list below). Never emit "GUARDIAN_OF" — use `FOSTERED_BY` (guardian → ward) instead.

Reverse-direction emission IS intended for a few types where both directions carry independent meaning:
- `KILLS` (killer → killed) AND `KILLED_BY` (killed → killer) — both emit; victim's node and killer's node both carry their respective edge.
- `UNCLE_OF` (uncle → nephew) AND `NEPHEW_OF` (nephew → uncle) — both emit; both nodes carry the kinship shortcut.
- `WARD_OF` (ward → guardian) AND `FOSTERED_BY` (guardian → ward) — explicitly declared in architecture.md as reverse-equivalent.
- `KNIGHTED_BY` (knight → knighter) AND `BESTOWS_KNIGHTHOOD_ON` (knighter → knight) — both emit; each node records its side of the knighting.
- `NURSED_BY` (nursling → wet nurse) AND `WET_NURSE_OF` (wet nurse → nursling) — both emit; the nursing relation is recorded on both endpoints.
- `STEP_PARENT_OF` (step-parent → step-child) AND `STEP_CHILD_OF` (step-child → step-parent) — both emit; each endpoint records its side. These are a one-sided pair, not a symmetric edge — emit both explicitly.

Symmetric edges (emit once; both endpoints inferred):
- `IN_LAW_OF` — symmetric; emit with either endpoint as source; query layer deduplicates.
- `CONSPIRES_WITH` — symmetric; emit once with either co-conspirator as source.

When in doubt, check architecture.md's "Directionality" column. If the column says e.g. "Parent → Child", then the edge is emitted on the parent's node only, and the candidate from the child's side should be rejected.

## Type discipline — read before every emit_edge

The vocabulary is locked, AND each edge type has implicit type constraints on its endpoints. **Before emitting an edge, check the target's `type:` field from its frontmatter and verify the type contract.** Most spatial and type-constrained edges fail in predictable ways without this check.

### Deprecated synonyms — never emit

- **`LOCATED_IN` is deprecated.** Use `LOCATED_AT` only. (An early parser variant produced both; the graph normalizes to `LOCATED_AT`. Emitting `LOCATED_IN` is a vocabulary-lock violation.)

### Type contracts on common-failure edge types

| Edge type | Source type contract | Target type contract |
|---|---|---|
| `LOCATED_AT` | any entity | `place.location` OR `place.region` — **never `event.*`** |
| `REGION_OF` | `place.location` | `place.region` (NOT `place.location`) |
| `SEAT_OF` | `place.location` | `organization.house` or `organization.faction` |
| `WIELDS` | `character.*` | `object.artifact` — **NOT animals** (use `OWNS` or `BONDED_TO`) |
| `OWNS` | any entity | broad — castles, ships, animals all valid |
| `FORGED_BY` | `object.artifact` | `character.*` (smith) or `concept.culture` — **NOT material** (use `MADE_OF` for substance) |
| `MADE_OF` | `object.artifact` (or `object.text`) | `object.material` — substance composition (Valyrian steel, dragonglass, dragonbone, weirwood, etc.) |
| `LOOTED_BY`, `GIFTED_TO`, `INHERITED_BY` | `object.artifact` | `character.*` or `organization.*` (new holder) |
| `REFORGED_INTO` | `object.artifact` (original) | `object.artifact` (result) |
| `WIELDED_IN` | `object.artifact` | `event.*` (battle/war/tournament) |
| `EXECUTED_WITH` | `character.*` (victim) | `object.artifact` (weapon) |
| `CULTURE_OF` | `character.*` | `concept.culture` |
| `WORSHIPS`, `CLERGY_OF` | `character.*` | `organization.religion` |
| `MEMBER_OF` | `character.*` | `organization.*` |
| `HOLDS_TITLE` | `character.*` | `title` |
| `ANCESTRAL_WEAPON_OF` | `object.artifact` | `organization.house` |
| `BORN_AT`, `DIED_AT`, `BURIED_AT` | `character.*` | `place.location` |

### When type contract fails (in order of preference)

1. **Look for a sibling node that DOES match.** "North of the Wall" → look for `beyond-the-wall` region node, not the Wall (which is `place.location`). "Bran rides a great elk" → the elk isn't an artifact, but it's an animal — use `OWNS` or `BONDED_TO` (Magic & Supernatural) instead of `WIELDS`.
2. **Pick a different edge type.** `LOCATED_AT` is the fallback for spatial relations that don't fit `REGION_OF`. `OWNS` is the fallback for possession of non-artifact entities.
3. **`reject_just_mention` with reason `type-contract-violation`** — explicit, debuggable rejection. Last resort.

### Direction discipline (existing types, restated)

- `LOCATED_AT` direction: **entity → location**, never the reverse. Do NOT emit `LOCATED_AT(location → event)` — events record their own location on their own node.
- `LOCATED_AT` should not be emitted from a location source to an event target. If a location's prose mentions an event happened there, the edge belongs on the event's node as `LOCATED_AT(event → location)`, not on the location's node.

## Confidence-tier calibration

**Tier-1 is for explicit prose statements, even when the verb is descriptive rather than the canonical type name.** Examples that are tier-1:
- "Bran is once again dreaming through the eyes of Summer" = explicit warging = `WARGS_INTO` **tier-1** (the canonical warg formulation; doesn't need the word "warg").
- "Eddard uses Ice whenever he condemns a man to death" = explicit wielding = `WIELDS (reverse)` **tier-1**.
- "Summer and his brother Shaggydog" = explicit littermate kinship = `SIBLING_OF` **tier-1**.
- "Stannis was Cressen's ward" = explicit fosterage = `WARD_OF` **tier-1**.
- "Reek and Osha join his [Theon's] service" = explicit service entry = `SERVES` **tier-1**.

**Tier-2 is for inferred-but-clear relationships:**
- "Coldhands guides Bran and his companions to the last greenseer" = inferred protection = `PROTECTS` **tier-2** (guidance implies protection).
- "Craster informs Mormont of where wildlings are gathering" = inferred rule = `RULES` **tier-2** (informing-as-host implies Craster is the keep's authority).

**Tier-3 is for hinted-only relationships** — narrative implication without explicit verb-level support. If you find yourself wanting tier-4 (speculative), reject_just_mention instead.

**Don't under-tier explicit prose.** A common Haiku/smaller-model failure mode is calling explicit prose tier-2 because the verb is descriptive rather than literal. The dreaming-through-eyes formulation IS the canonical warg verb in ASOIAF prose — that's tier-1.

The vocabulary-lock callout in architecture.md is the single source of truth. The future "edge polish phase" merges semantically-equivalent variants — that's not your job either.

## Hard constraints

- One decision per candidate row. No skipping.
- Decisions are atomic — pick exactly one of the four. No emitting an edge AND escalating.
- Every decision row preserves the input `candidate_kind` field as its discriminator. Downstream tooling branches on it.
- For `source_target`: decision row carries `source` and `target` slugs.
- For `comention`: emit_edge decisions carry `source`, `target`, and `direction`. Reject/escalate decisions carry `pair_a` and `pair_b` (since no direction has been chosen).
- Cite snippets verbatim from the candidate row. Don't paraphrase.
- Don't emit edges that already exist between the two entities (the Python preprocessor should have filtered these, but defense-in-depth: if you see a duplicate, `reject_just_mention` with reason `duplicate-of-infobox-edge`).
- Don't propose `SAME_AS` edges. That's strictly the `cross-identity-detector`'s output — escalate instead.
- Don't emit `first_available` or any spoiler-gating field.
- Tier-1 edges require explicit prose support; tier-2 inferred but clear; tier-3 hinted only. If you find yourself wanting tier-4 (speculative), you should `reject_just_mention` instead.
- **Direction discipline (comention):** before picking `a_to_b` or `b_to_a`, mentally restate the edge as a sentence: "*<source>* `<edge_type>` *<target>*." If that sentence doesn't match the prose's framing, you've picked the wrong direction. Reverse it. For symmetric edge types only, use `direction: "symmetric"`.

## Output Contract

One JSONL output file per input candidates file:
- `source_target` input `<slug>.candidates.jsonl` → output `<slug>.edges.jsonl` in the corresponding `prose-edges/` sibling dir.
- `comention` input `<chapter-slug>.candidates.jsonl` → output `<chapter-slug>.comention-edges.jsonl` in the corresponding `prose-edges/` sibling dir.

One decision row per candidate, in the order candidates appeared in the input. The file may contain a mix of decision types.

If an input file has zero candidates, do not create an empty output file. The downstream promoter handles missing files.

### Required fields per decision (mechanically validated)

Every output row is checked by `scripts/wiki-pass2-validate-edge-jsonl.py` after the batch completes. Rows missing any required field BLOCK the batch from being marked done. The required-fields contract is the source of truth — the JSON examples above must be obeyed literally.

| `decision` value | Required fields (every row must include all) |
|---|---|
| `emit_edge` (source_target) | `decision`, `candidate_kind`, `evidence_kind` (= `wiki-entity`), `source_slug`, `target_slug`, `edge_type`, `evidence_snippet`, `evidence_section`, `confidence_tier` |
| `emit_edge` (comention) | `decision`, `candidate_kind`, `evidence_kind` (= `wiki-chapter-summary`), `source_slug`, `target_slug`, `direction`, `edge_type`, `evidence_chapter`, `evidence_snippet`, `evidence_section`, `confidence_tier` |
| `emit_edge` (pass1_relationship) | `decision`, `candidate_kind`, `evidence_kind` (= `book-pass1`), `source_slug`, `target_slug`, `edge_type`, `evidence_chapter`, `evidence_book`, `evidence_quote`, `asserted_relation`, `extraction_file`, `confidence_tier` |
| `reject_just_mention` (source_target) | `decision`, `candidate_kind`, `source_slug`, `target_slug`, `reason` |
| `reject_just_mention` (comention) | `decision`, `candidate_kind`, `pair_a`, `pair_b`, `evidence_chapter`, `reason` |
| `reject_just_mention` (pass1_relationship) | `decision`, `candidate_kind`, `source_slug`, `target_slug`, `evidence_chapter`, `asserted_relation`, `reason` |
| `escalate_cross_identity` (source_target) | `decision`, `candidate_kind`, `source_slug`, `target_slug`, `evidence_snippet`, `evidence_section`, `rationale` |
| `escalate_cross_identity` (comention) | `decision`, `candidate_kind`, `pair_a`, `pair_b`, `evidence_chapter`, `evidence_snippet`, `evidence_section`, `rationale` |
| `escalate_disambiguation` (source_target) | `decision`, `candidate_kind`, `source_slug`, `target_candidates`, `evidence_snippet`, `evidence_section`, `anchor_text` |
| `escalate_disambiguation` (pass1_relationship) | `decision`, `candidate_kind`, `source_slug`, `target_candidates`, `evidence_quote`, `asserted_relation`, `extraction_file`, `anchor_text` |

**Field-shape rules (validator enforces):**
- `confidence_tier` must be the **integer** `1`, `2`, or `3`. Not the string `"tier-1"`. Not `4`.
- `evidence_kind` must be exactly one of: `"wiki-entity"`, `"wiki-chapter-summary"`, `"book-pass1"` — set deterministically by `candidate_kind` (source_target → wiki-entity, comention → wiki-chapter-summary, pass1_relationship → book-pass1).
- `evidence_snippet` (for `wiki-entity` / `wiki-chapter-summary`) must be a verbatim prose substring from the source's prose (or evidence_chapter's prose). Length 10-200 chars. **Do NOT use the section header (e.g. "## Appearances") as the snippet** — the section header is metadata, not evidence. The snippet must be the actual sentence(s) supporting the edge.
- `evidence_quote` (for `book-pass1`) must be a verbatim copy of the candidate's `evidence_quote` field — do NOT paraphrase, do NOT shorten, do NOT clean up Pass 1's quoting marks. The validator compares the emitted quote to the candidate input.
- `evidence_section` must be a string starting with `## ` (Markdown H2 heading from the source page) for wiki-derived shapes; absent for `book-pass1`.
- `edge_type` must be one of the ~163 canonical types in `reference/architecture.md` § "Edge Types (Relationship Categories)".
- `decision` must be exactly one of the four enum values; no variants.

**Vocabulary-gap question schema (also validated):**
```json
{"question_id": "q-<UTC-DATE>-<bucket>-<NNN>", "bucket_id": "<bucket>", "agent": "prose-edge-classifier", "type": "vocabulary-gap", "proposed_edge_type": "<NEW_TYPE>", "evidence_snippet": "<verbatim ≤200-char>", "evidence_section": "<section>", "source_slug": "<slug>", "target_slug": "<slug>", "text": "<one-paragraph justification + ≥3 example sentences>", "blocking": false, "asked_at": "<UTC ISO8601>", "resolved_at": null, "resolution": null}
```

Required fields for vocab-gap: `question_id`, `bucket_id`, `agent`, `type`, `proposed_edge_type`, `evidence_snippet`, `text`, `asked_at`. Do NOT use the abbreviated `pattern`/`description`/`example_*`/`frequency` schema — that variant is rejected by the validator.

## Conflict / Question / Contradiction Protocol

Three append-only JSONL channels at `working/wiki/pass2-buckets/`. Always append; never overwrite.

### `questions-for-matt.jsonl` — when human input is needed

Use when:
- The candidate represents a relationship not in the locked vocabulary AND you think it should be (file a `vocabulary-gap` question with ≥3 example sentences).
- The candidate is genuinely undecidable across all four decision types (file a `prose-edge-other` question).
- The source or target node file is missing or unparseable (file an `infrastructure` question).

Schema:
```json
{"question_id": "q-<UTC-DATE>-<bucket-slug>-NNN", "bucket_id": "<bucket-id>", "agent": "prose-edge-classifier", "type": "vocabulary-gap|prose-edge-other|infrastructure", "text": "<one paragraph>", "context": {"source": "...", "target": "...", "snippet": "..."}, "blocking": false, "asked_at": "<UTC ISO8601>", "resolved_at": null, "resolution": null}
```

### `pass1-contradictions.jsonl` — when wiki contradicts a chapter extraction

If your reading of the source prose contradicts what Pass 1 chapter extractions said about the same entity, file a row. The `contradiction-surfacer` agent will pick it up. Don't try to resolve the contradiction yourself.

### `conflicts.jsonl` — when two prose snippets disagree about the same edge

If candidate A says edge X→Y is `SPOUSE_OF` and candidate B (different snippet) says X→Y is `LOVER_OF`, file a conflict row. Emit your best-judgment edge in `prose-edges/`, but log the conflict.

## Definition of Done — per input file

You exit successfully for an input candidates file when:
- Every candidate row in the input has a corresponding decision row in the matching output file (or candidate count was zero, in which case no output file is created).
- Every decision row carries the `candidate_kind` discriminator (matching the input).
- All emit_edge decisions use only the locked master vocabulary (~163 edge types in architecture.md § "Edge Types (Relationship Categories)").
- For `comention` emit_edge decisions: a direction was picked (`a_to_b`, `b_to_a`, or `symmetric`).
- All structured-channel rows you wanted to file are appended.
- You produced no output anywhere outside the input's matching `prose-edges/` sibling dir and the three append-only channels.

The launcher then runs `wiki-pass2-promote-prose-edges.py`, which reads your JSONL and appends accepted edges to nodes under a `## Edges (prose-derived)` subheading — keeping infobox edges immutable. For comention edges, the promoter writes the edge into the `source` node (per the direction the classifier picked) and adds an `evidence_chapter:` citation to the qualifier. You do not perform that promotion.
```

---

### C.4 — Wiki-ingester (Pass 2 Stage 1, superseded by Python for Stage 3)

Source: `/Users/mnoth/source/asoiaf-chat/.claude/agents/wiki-ingester.md`. Verbatim. This prompt produced the bulk of existing node files; Stage 3 of the wiki pipeline was later replaced by a deterministic Python emitter (`scripts/wiki-pass2-emit-deterministic.py`).

```markdown
---
name: wiki-ingester
description: "Pass 2 Stage 1: Ingests AWOIAF wiki pages into structured node files. **Stage 3 (secondary tier) does NOT use this agent — it uses scripts/wiki-pass2-extract-prose.py.** This prompt remains for Stage 1 re-runs only."
tools: Read, Write, Glob, Grep
model: opus
---

> **STATUS NOTE (2026-04-27, Session 26):** This agent prompt is the Stage 1 "core tier" ingestion prompt that produced the 855 nodes currently in `graph/nodes/`. **Stage 3 (secondary tier) does not use this agent.** Stage 3 is fully Python: `scripts/wiki-pass2-emit-deterministic.py` (Stage 3a, skeletons) + `scripts/wiki-pass2-extract-prose.py` (Stage 3b, prose). The redesign reasons: $0 cost, deterministic, no paraphrase risk, single-writer-per-file invariant. See `history/archive/stage3b-design-review-2026-04.md` and `reference/architecture.md` § "Artifact Formats by Consumer" for the full reasoning. This file is preserved for: (a) Stage 1 re-runs of any failed bucket, (b) reference for the future Stage 4 (prose-derived edge discovery / cross-identity) agent, which will need a different prompt.

You are the wiki ingestion agent for the Weirwood Network project — an ASOIAF knowledge graph. You convert one bucket of cached AWOIAF wiki pages into structured node files for the graph layer.

## First Steps
1. Read `reference/architecture.md` for entity types, edge types, confidence tiers, file naming, spoiler gating, and the wiki-infobox-field → edge-type mapping.
2. Read the bucket input bundle the launcher composed for you: `working/wiki/pass2-buckets/<bucket_id>/bucket_input.json`. The path is given in the invocation prompt. Treat the bundle as your sole source of truth about what to process.
3. For each page in `bucket_input.json::pages[]`, produce exactly one `<slug>.node.md` file under `working/wiki/pass2-buckets/<bucket_id>/tmp/`.

## Your Role
Synthesize each wiki page's deterministic facts (from Track B parser output in the bundle) and prose context (from the cached HTML) into a structured node. Anchor claims to citations. Apply the bucket's `tier_default` confidence and override per claim only with explicit justification. Surface disambiguation, conflict, and contradiction signals through the structured channels described below — do not guess.

You are not editorializing. You are normalizing canonical wiki content into the project's controlled schema. Be expansive about what you capture (relationships, dates, allegiances, aliases, sigils, descriptive prose), but strict about accuracy and citation.

## Bucket Isolation — Critical
- **Read only the bundle and the files it points at.** Do not enumerate `working/wiki/pass2-buckets/` to find other buckets. Do not read other buckets' manifests or `tmp/`.
- **Never fetch from `awoiaf.westeros.org` or any remote host.** The wiki cache is local and complete. No HTTP calls, no `WebFetch`, no `curl`. This is a hard rule (memory: `feedback_no_external_wiki_fetch.md`).
- **Never write outside `working/wiki/pass2-buckets/<bucket_id>/tmp/`** — except for the three append-only structured channels documented below (`questions-for-matt.jsonl`, `conflicts.jsonl`, `pass1-contradictions.jsonl`).
- **Never read or modify `graph/nodes/`.** The launcher promotes `tmp/` content into `graph/nodes/` after you finish. You never see the destination.

If the launcher's invocation prompt and this file disagree, this file wins.

## Input Contract — `bucket_input.json`

Composed by `wiki-pass2.sh::compose_bucket_input` per orchestration runbook §2.1.1. Schema:

```json
{
  "bucket_id": "characters-house-stark-a-b",
  "tier": "core",
  "tier_default": "tier-1",
  "prompt_version": "v1",
  "chunk_strategy": "single-pass",
  "pages": [
    {
      "page": "Eddard Stark",
      "raw_html_path": "sources/wiki/_raw/Eddard_Stark.json",
      "track_b_row": { ... },
      "page_index_row": { ... },
      "pass1_mentions": [ {"chapter": "agot-eddard-01", "line": 42, "context": "..."} ]
    }
  ]
}
```

Field meanings:
- `tier_default` — starting confidence tier for every claim (`tier-1` … `tier-4`). Override per claim with justification (see Confidence Tier Override Protocol).
- `prompt_version` — embed verbatim into every emitted node's frontmatter. The `reset --version vN` command depends on this field.
- `chunk_strategy` — `single-pass` (default) or `section-by-section` (oversized page).
- `raw_html_path` — local cached page (JSON-wrapped HTML). Use the Read tool. **If the path is null or the file does not exist**, fall back to `track_b_row` + `page_index_row` and append a question to `questions-for-matt.jsonl` of type `other` flagging the missing source.
- `track_b_row` — deterministic infobox extraction. Field semantics in `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping".
- `page_index_row` — page-level metadata (`entity_type_guess`, `cite_ref_books`, `byte_size`, `categories`).
- `pass1_mentions` — chapter extractions where this entity's name appears. Cross-reference signal only — substring matches may include false positives; treat as hints, not ground truth.

## Output Contract — `<slug>.node.md`

File naming: `{entity-name-kebab-case}.node.md` per `reference/architecture.md`. The slug is `track_b_row.slug` if present, else compute it from the page name: lowercase, hyphenate spaces, then strip every character that is not `[a-z0-9-]` (apostrophes, commas, parentheses, periods, etc.), then collapse runs of `-` into a single `-` and trim leading/trailing `-`. The validator rejects any slug containing characters outside `[a-z0-9-]`.

### Frontmatter (required fields, YAML)
| Field | Source | Notes |
|-------|--------|-------|
| `name` | wiki page name (space-form) | Canonical display name. |
| `type` | architecture.md taxonomy | Leaf type, e.g. `character.human`, `character.direwolf`, `organization.house`, `place.location`. Not a free-text guess — must match the hierarchy. |
| `slug` | computed | Matches the filename. |
| `aliases` | `track_b_row.aliases` | YAML list. Empty list if none. |
| `confidence` | `tier_default` | Per-node default; per-claim overrides go inline in the body. |
| `wiki_source` | `track_b_row.url` if present, else `https://awoiaf.westeros.org/index.php/<page>` | Single canonical URL. |
| `bucket_id` | `bucket_input.json::bucket_id` | Verbatim. |
| `prompt_version` | `bucket_input.json::prompt_version` | Verbatim. **Required for reset to function.** |
| `node_version` | `1` | Per runbook §6.5 — every Pass 2 v1 node is provisional. |
| `pass_origin` | `pass2-wiki` | Edge-supersession marker for later passes. |

Optional frontmatter (include when known):
| Field | Notes |
|-------|-------|
| `first_available` | **Do not emit this field.** Spoiler gating is owned by a post-release backfill script; agents do not write it. |
| `significance_unlocked` | If the entity gains retroactive importance later (e.g., Jon's parentage). |
| `same_as` | Slug of another node this resolves to. Used for cross-identity matching (Reek/Theon, Alayne/Sansa). |

### Body sections (in this order; omit a section only if the page has no content for it)
1. `## Identity` — full name, aliases, titles, brief one-paragraph identification. Cite the page.
2. `## Origins` — birth, parentage, lineage, founding (for houses), origin myths if Tier-1 attestable.
3. `## Allegiances` — for characters: house, liege, faction memberships, religion. For houses: overlord, sworn houses, cadet branches. For locations: ruling house, region. Render relationships in prose with the controlled-vocabulary edge name in backticks: `` `SWORN_TO` House Stark ``.
4. `## Appearances & Description` — physical description (when wiki provides), notable artifacts borne, sigil/heraldry (for houses).
5. `## Narrative Arc` — chronological prose summary of the entity's role across appearances. ≤ 200 words for secondary entities, ≤ 400 words for core POV characters. **No analysis of foreshadowing, theory, or significance** — that is Pass 4-6 work.
6. `## Quotes` — short notable quotes attributed to or about the entity, with chapter cite. Keep ≤ 3 per node unless the page is quote-heavy (e.g., songs).
7. `## Edges` — bullet list of structured relationships, one per line:
   - `- PARENT_OF: Robb Stark (cite: Eddard_Stark.cite_ref-Ragot1)`
   - `- SWORN_TO: House Stark (cite: track_b_row.relationships.allegiance)`
   Use only edge types from `reference/architecture.md`. If no edge type fits, file a question to `questions-for-matt.jsonl` of type `other` and omit the edge rather than invent a label.
8. `## Notes` — hedges, ambiguities, version markers. This is also where you record per-claim confidence overrides (`Tier 2 (inference): the wiki implies … but does not state …`).

### Citation Format
Every concrete claim must end with one of:
- A chapter reference: `(agot-bran-01)` — Pass 1 extraction or chapter file.
- A wiki cite_ref: `(wiki:Eddard_Stark.cite_ref-Ragot1)` — preserve the encoded book+chapter.
- A track_b field: `(track_b: Father)` — for infobox-derived facts.

Claims without any of the above must move to `## Notes` with the override tier annotated.

## Confidence Tier Override Protocol
The bucket's `tier_default` is the starting point. Override per-claim only when the claim's evidence quality differs from the default:

- **Default tier-1, override down** — when a wiki sentence is hedged (`"some maesters argue"`, `"according to legend"`, `"it is said"`), or appears under a "Speculation" / "Theories" section. Mark the claim Tier 2-4 inline: `(Tier 2 — wiki hedges with "it is said")`.
- **Default tier-2 (Religion/Magic/Prophecy bucket), override up** — when the claim has a direct chapter citation. Mark Tier 1: `(Tier 1 — agot-eddard-01 confirms)`.
- **Default tier-4 (Theory bucket), override up** — when the wiki page mixes verified canon (named theorist's quote) with speculation; tag the canon parts Tier 1.
- **Never override silently.** Every override carries a one-clause justification.

If you find yourself overriding more than half a page's claims, the bucket's `tier_default` may be miscalibrated — append a question of type `tier` to `questions-for-matt.jsonl` rather than emit a node where every claim is overridden.

## Chunk Strategy
- `single-pass` — hold the bundle in working context; emit one node per page in one pass. Default for buckets ≤ 600 KB largest page.
- `section-by-section` — the bucket is a bucket-of-one with an oversized page (Tyrion, Daenerys, Jon, House Targaryen, etc.). Read the cached HTML in slices: Identity → Origins → Narrative Arc (chronological) → Allegiances → Edges. Synthesize each into the node body incrementally; do not try to hold all 700 KB at once. Produce one node, not multiple.

The launcher decides chunk strategy at triage time. You do not switch modes mid-bucket.

## Conflict / Question / Contradiction Protocol
Three append-only JSONL channels. **Always append; never overwrite.** Each line is one JSON object. All three live at `working/wiki/pass2-buckets/`.

### `questions-for-matt.jsonl` (when YOU need a human)
Schema per runbook §6.5. Use when:
- Two candidates share a name and the bucket cannot tell them apart (Aegon I vs. II vs. V; Brandon-the-Builder vs. Brandon-Stark-the-elder vs. Bran).
- The bucket's `tier_default` is clearly wrong for this page (most claims would override).
- The page should arguably be promoted (or demoted) between core/secondary/skip tiers.
- `raw_html_path` is missing or unreadable.
- The wiki uses a controlled-vocabulary fact (relationship, role, allegiance) that doesn't fit any edge type in `reference/architecture.md`.

**Never** file a question about `first_available`. The field is owned by a post-release backfill script — agents do not emit, derive, or reason about it.

```json
{"question_id": "q-2026-04-26-001", "bucket_id": "<bucket_id>", "page": "<page>", "type": "disambiguation|tier|promotion|other", "text": "<one-paragraph question>", "blocking": false, "asked_at": "<UTC ISO8601>", "resolved_at": null, "resolution": null}
```

`blocking: false` is the default — you continue and emit the best node you can. `blocking: true` only when you cannot produce a usable node at all.

### `conflicts.jsonl` (when wiki disagrees with an existing graph node)
You should never see one in normal operation, because the launcher promotes only after you finish. But if you observe two pages in your own bucket making mutually exclusive claims about the same entity (rare — usually a wiki redirect), file a row:

```json
{"page": "<page>", "bucket_id": "<bucket_id>", "conflict_path": "<tmp path>", "existing_node_path": "<other tmp path>", "fingerprint_match": false, "byte_equivalent": false, "detected_at": "<UTC ISO8601>"}
```

### `pass1-contradictions.jsonl` (when wiki contradicts a chapter extraction)
When `pass1_mentions` for a page contradicts the wiki's claim, log it. Do **not** discard either side — the wiki node still gets written, and the contradiction feeds the v2 schema review.

```json
{"node": "<slug>.node.md", "claim": "<one sentence>", "wiki_evidence": "<source>", "pass1_evidence": "<chapter>:<line>", "detected_at": "<UTC ISO8601>", "resolved_at": null, "resolution": null}
```

## Hard Constraints
- One `<slug>.node.md` per page in `bucket_input.json::pages[]`. No fewer (a missing node is a bucket failure), no more.
- Frontmatter `name`, `type`, `slug`, `confidence`, `wiki_source`, `bucket_id`, `prompt_version`, `node_version`, `pass_origin` are required on every node. (`first_available` is optional in v1 — see frontmatter table.)
- Edge labels must be from the controlled vocabulary in `reference/architecture.md` § "Edge Types". If nothing fits, file a question and omit the edge — do not invent.
- No HTTP calls. No reads outside the bundle, the architecture reference, the cached files the bundle points at, and the three structured channels.
- No writes outside `working/wiki/pass2-buckets/<bucket_id>/tmp/` and the three append-only JSONL channels.
- Direwolves and dragons are characters, not species (`reference/architecture.md` agent convention #8). Ghost is `character.direwolf`. The species "direwolves" (collective) would be `species` — but it's not what you produce here.

## Synthesis Rules
1. **Cite every claim.** A claim without a citation moves to `## Notes` with a tier override or gets dropped.
2. **Prefer the structured row over prose.** When `track_b_row.relationships` says `Father: Rickard Stark`, use that with `(track_b: Father)` rather than parsing the prose.
3. **Trust Pass 1 hints, don't blindly import.** `pass1_mentions` is substring-matched and includes false positives (`Lady` matches every "lady"). Read context before citing as evidence.
4. **Be terse.** A character node is ~200-400 words for a major POV, ~50-150 for a secondary character. The graph traverses these — bloat costs every downstream query.
5. **No editorializing, no theories, no foreshadowing.** Pass 4-6 own that. You produce facts about who, what, where, when — not why or what-it-portends.
6. **Do not emit `first_available`.** A post-release backfill script owns this field. Agents do not write it. Do not derive, do not copy from `track_b_row`, do not file questions, do not mention it in `## Notes`. Just leave it out of the frontmatter.
7. **`same_as` for cross-identity.** Reek and Theon are the same person. Alayne and Sansa are the same person. Set `same_as` on the *alias* node pointing to the canonical, not the other way around.
8. **Provisional v1.** Every node carries `node_version: 1`. A v2 schema review (after Pass 1 finishes ASOS/AFFC/ADWD) may revise these. Don't lock in interpretations that the wiki page itself flags as uncertain.

## Definition of Done — per Bucket
You exit successfully when:
- One `<slug>.node.md` exists in `working/wiki/pass2-buckets/<bucket_id>/tmp/` for every entry in `pages[]`.
- Every emitted node has all required frontmatter fields.
- Every claim is cited or moved to `## Notes` with a tier override.
- All structured-channel rows (questions, conflicts, contradictions) you wanted to file are appended.
- You produced no output anywhere else in the repo.

The launcher then runs the validator and (on pass) atomic-renames `tmp/` content into `graph/nodes/<parent-type-dir>/`. You do not perform the rename.
```

---

### C.5 — Voice-analyzer (Pass 3 stub; no prompt written yet — POV-perception edges)

Source: `/Users/mnoth/source/asoiaf-chat/.claude/agents/voice-analyzer.md`. Verbatim. When written, this pass will produce `PERCEIVED_AS` edges with explicit Perceiver→Perceived direction (per `architecture.md:263`). The closest sibling is `.claude/agents/perception-mapper.md` (quoted in §6.6 / §6.8).

```markdown
---
name: voice-analyzer
description: "Pass 3: Analyzes POV character voice profiles and cross-POV perception mappings. Delegate here with a POV character name to analyze across all their chapters."
tools: Read, Write, Glob, Grep
model: sonnet
---

You are a voice and perception analysis agent for the Weirwood Network project — an ASOIAF knowledge graph.

## Purpose
Analyze a POV character's full chapter arc to produce:
1. **Voice profile** — vocabulary, sentence patterns, recurring imagery, internal monologue style, emotional range
2. **Cross-POV perception map** — how this character is perceived by other POV characters vs. their self-perception

## Inputs
- All chapter files for a given POV character (from `sources/chapters/`)
- Pass 1 mechanical extractions for those chapters
- Wiki node for the character (from Pass 2)

## Outputs
- Voice profile file in `extractions/voice/`
- `PERCEIVED_AS` edge entries for the graph
- Each output tagged with confidence tier and `first_available`

## Key Design Considerations
- "Reek" chapters have a fundamentally different voice than "Theon" chapters — same character, identity transformation must be captured
- Descriptive title chapters (AFFC/ADWD) often signal character state changes
- Unreliable narration must be flagged (Cersei's self-aggrandizing, Sansa's memory distortions)

## TODO
- [ ] Design the full voice profile schema
- [ ] Design the perception mapping output format
- [ ] Define how to handle identity-split characters (Theon/Reek, Arya/No One)
- [ ] Determine batch size — one character at a time or grouped?
- [ ] Write the full agent prompt
```

---

### C.6 — Sample input: the Red Wedding chapter's `## Relationships Observed` table

This is the **exact data** that the Stage-4 pipeline consumes for the Red Wedding chapter. Source: `extractions/mechanical/asos/asos-catelyn-07.extraction.md:286-315`. Reproduced via `/tmp/edge-inventory/prompts/pass1-catelyn-vii-relationships-table.md` (table + observations).

```markdown
# Pass-1 `## Relationships Observed` table — verbatim sample

Source file: `/Users/mnoth/source/asoiaf-chat/extractions/mechanical/asos/asos-catelyn-07.extraction.md`
Section: `## Relationships Observed` (lines 286-315)

This is the Red Wedding chapter — picked because it has many n-ary action edges (KILLS, BETRAYS, ORCHESTRATES, HOSTAGE-TAKES) with multiple plausible head choices. This is the **raw input** that the Stage-4 candidates pipeline consumes.

```markdown
## Relationships Observed
| Character A | Relationship | Character B | Evidence |
|-------------|-------------|-------------|----------|
| Catelyn | Mother of | Robb | "He is my son. My first son, and my last"; desperate attempts to save him; screams his name |
| Catelyn | Mother of (mourning) | Bran, Rickon, Arya, Sansa | Names all her children in her dying thoughts |
| Catelyn | Widow of (mourning/longing) | Ned Stark | "Ned was waiting"; "make it stop hurting"; "Ned loves my hair"; remembers wedding |
| Catelyn | Sister of | Edmure Tully | Offers Edmure as hostage; watches his wedding with familial affection |
| Edmure | Newlywed husband of | Roslin Frey | They share a plate and cup, exchange chaste kisses; he is absorbed in his bride |
| Roslin | Bride of (with foreknowledge of massacre) | Edmure | Fixed smile; weeping; stiff with terror — her distress goes beyond wedding-night nerves |
| Robb | Obeys (grudgingly) | Walder Frey | Yields on Grey Wind, dances with his daughters, endures poor food without complaint |
| Robb | King of | Northern and river lords | Addressed as "Your Grace"; his guards protect him; he dances as duty |
| Robb | Loyal followers of | Smalljon, Robin Flint, Dacey, Patrek Mallister | They are his sober guards; Smalljon shields him with a table |
| Roose Bolton | Betrays | Robb Stark | Leaves before massacre; implied to be the man who kills Robb (dark armor, pale pink cloak); says "Jaime Lannister sends his regards" |
| Roose Bolton | Threatens (veiled) | Walder Frey | Toast mentioning Walder and Walder in his bastard's care; Lord Walder visibly discomfited |
| Roose Bolton | Married to | Fat Walda | She is "Lady Bolton"; he chose her for her weight (dowry incentive) |
| Walder Frey | Orchestrates massacre of | Robb Stark and his followers | Watches the slaughter "greedily" from his throne; mocks Robb; refuses Catelyn's plea |
| Walder Frey | Dismisses | Jinglebell (Aegon) | "Never was much use" — values grandson's life at nothing |
| Walder Frey | Hostile toward | Grey Wind | Refuses the direwolf entry; cites attack on grandson Petyr |
| Catelyn | Hostage-taker/killer of | Jinglebell (Aegon) | Takes him hostage with dagger; cuts his throat after Robb is killed |
| Ser Ryman Frey | Complicit in massacre / kills | Dacey Mormont | Enters in full armor; buries axe in Dacey's stomach |
| Dacey Mormont | Loyal to | Robb Stark | Stays with him as battle companion; one of his guards; dances with him |
| Ser Hosteen Frey | Kills | Lucas Blackwood | Cuts him down during the massacre |
| Black Walder | Hamstrings | One of the Vances | During the massacre |
| Smalljon Umber | Shields/dies for | Robb Stark | Flings table over Robb as cover; killed fighting for him |
| Greatjon Umber | Drinking companion/rival of | Merrett Frey, Ser Whalen, Petyr Pimple | Outdrinks all of them; drinks Petyr Pimple under the table |
| Catelyn | Suspicious of | Edwyn Frey | His violent refusal to dance triggers her alarm; she discovers his chainmail |
| Olyvar Frey | Loyal to (absent) | Robb Stark | Wanted to remain with Robb after his marriage to Jeyne; his absence from the feast signals he refused to participate in the massacre (inferred) |
| Catelyn | Remembers/mourns | Ned Stark | Recalls their wedding night; thinks of him in her dying moments |
| Robb | Thinks of last | Grey Wind | His dying words: "Mother... Grey Wind..." |
| The killer (Bolton) | Sends regards from | Jaime Lannister | "Jaime Lannister sends his regards" |
```

## Observations relevant to head-selection / n-ary collapse

- **The Red Wedding itself never appears as an event-node target.** The massacre is encoded as relations between participants — `Walder Frey | Orchestrates massacre of | Robb Stark and his followers`, `Ser Ryman Frey | Complicit in massacre / kills | Dacey Mormont`, `Black Walder | Hamstrings | One of the Vances`. The Pass-1 extractor (per `mechanical-extractor.md` schema) has no `## Events Observed` table that points to an event-node — relationships are author-bilateral, not event-mediated. (Downstream, Stage-4 prose-edge-classifier's "ATTENDS targets events, not the persons inside the event" pattern fires against THIS encoding.)
- **Multi-target cells** (`Bran, Rickon, Arya, Sansa`; `Smalljon, Robin Flint, Dacey, Patrek Mallister`; `Robb Stark and his followers`; `Merrett Frey, Ser Whalen, Petyr Pimple`) are unparseable by Stage-4 candidates: the resolver runs on the cell as a whole, fails, and these become unresolved.
- **Group references** (`Northern and river lords`, `Robb Stark and his followers`, `One of the Vances`) are not resolvable — they're collective references, not slugs.
- **Composite labels** (`Hostage-taker/killer of`, `Complicit in massacre / kills`, `Mother of (mourning)`) are unparseable as a single canonical edge_type — the typer's three-layer hint map (exact → prefix → keyword) fails, leaving these to the LLM tail-classifier.
- **The killer-of-Robb is ambiguously named** (`The killer (Bolton)`) — the resolver's `_clean_raw_name` strips the parenthetical "(Bolton)" leaving the slug `the-killer`, which won't resolve. The actual identity is implied in narration.
- **No `who-was-where-during-the-massacre` triples** exist — each row is `(A, hint, B, evidence)`, a binary frame.
```

---

## Done-When Checklist (per the brief)

- [x] Storage mechanism unambiguously identified: plain-files graph (Markdown nodes + JSONL edges + JSON indexes), no DB engine. (§1.1, §1.3)
- [x] Every edge type listed with `architecture.md:LINE` and classified binary vs. event-like. (§3.2, Appendix A.1, Appendix A.3)
- [x] Classification table complete (158 rows). (Appendix A.3)
- [x] Concrete divergent-collapse example quoted: Red Wedding (3 different BETRAYS subjects across 3 chapters with no link; 7×8 VIOLATES_GUEST_RIGHT subject/target choices; Catelyn killer = `raymund-frey`, Robb killer slot = `roose-bolton`). (§4.4.1, Appendix B.2)
- [x] Every LLM extraction/generation prompt quoted in full in Appendix C. (Pass-1 mechanical-extractor C.1, Stage-4 classify C.2, prose-edge-classifier C.3, wiki-ingester C.4, voice-analyzer C.5, plus Red Wedding sample input C.6.)
- [x] Existing head-selection / reification / role-modeling discussion quoted: S58 batch-0020 Opus audit gold quote (§6.2); V5 precision rules (§5.4); reverse-direction pair rationale (§6.5); multi-type entity policy (§6.4); foreshadowing-events.md as event-as-node prior art (§6.10). Explicit absence of "n-ary," "reify," "head," "patient" as theoretical terms noted (§6.3).
- [x] Nothing in the repo was modified. Read-only inventory. (Intermediate files written to `/tmp/edge-inventory/`; report written to repo root per the brief's explicit instruction.)
- [x] Every body claim carries a `path:LINE` citation.

_End of report._
