# Worklog Archive 011

> Sessions archived from `worklog.md`. Newest first within this file. Each archive holds exactly 5 entries when full. This one is now FULL — start `archive012.md` for the next archive.

---

### Session 52 — Edge Vocabulary Drift Cleanup (2026-05-13)

**Detail:** `history/session-details/session-052.md`

**Changes made:**
- `reference/architecture.md` — rewrote vocabulary-lock callout (line 454-465) to distinguish master vocabulary (~96 types across 14 subsections) from wiki-infobox subset (~26 types). Added `WRITTEN_BY` to Narrative & Literary subsection. Added reverse-direction rows: `HELD_BY` (after HOLDS_TITLE), `KILLED_BY` (after KILLS), `DECEIVED_BY` (after DECEIVES). Added deprecation note on `LOCATED_AT` description noting `LOCATED_IN` as deprecated synonym.
- 21 graph files in `graph/nodes/_conflicts/` — normalized `LOCATED_IN` → `LOCATED_AT`. Final state: 0 LOCATED_IN, 59 LOCATED_AT.
- `reference/design-philosophy.md` (line 91) — "22 edge types" → "~96 edge types".
- `.claude/agents/schema-drift-auditor.md` (line 16) — updated to reference both master and subset tables.
- `.claude/agents/prose-edge-classifier.md` — 3 spots: First Steps (line 14) repointed at master section with explicit perception/narrative/prophecy verb expansion; Vocabulary Lock (line ~74) replaced 22-type hardcoded list with full 14-category expansion (~96 types) referencing architecture.md as source of truth; Definition of Done (line ~131) "22 edge types" → "master vocabulary (~96 edge types)".
- `next.md` — added top-of-file `★ NEXT RECOMMENDATION` callout for Stage 4 wiki-prose edge classifier. Updated "Where we are today" (date, current node/edge counts, vocab cleanup summary). Expanded Track 5 with "tier-difference not polish" framing + "no book passes required" clarification + Open Question on run shape (single-session vs watcher+workers).
- `history/session-details/session-052.md` — NEW. Long-form record of discovery + decisions.

**Decisions:** Edge vocabulary is the master `## Edge Types` section in architecture.md (~96 types). Wiki-infobox table is a parser-only subset (~26 types). Prose-edge-classifier emits from the master (it had been incorrectly restricted to the subset — a real bug, not just stale doc). Reverse-direction edges (HELD_BY/KILLED_BY/DECEIVED_BY) are documented as semantic equivalents — query layer treats `HELD_BY(a→b)` as identical to `HOLDS_TITLE(b→a)`. LOCATED_IN normalized to LOCATED_AT (was 21 instances all in _conflicts/). Stage 4 reframed: not "edges incrementally improve graph"; rather, 37 of the 96 master types are entirely unpopulated (perception/identity/prophecy/narrative/causal verbs) and Stage 4 turns "structured feudal wiki" into "graph that knows the story." Tier-difference. Run-shape question (single-session vs watcher+workers) deferred until candidate volume is known.

**What's next:**
- **Stage 4 wiki-prose edge classifier** (NEXT). Pre-flight: re-run cross-references + edge-candidates scripts (deterministic, free). Then 3-bucket smoke test. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- Per Matt's standing rule, /endsession was explicitly approved this session — not auto-triggered.

---

### Session 51 — Watcher-Day Orchestration + Session-Results Convention (2026-05-12)

**Detail:** `history/session-details/session-051.md`

**Changes made:**
- Spot-check of 10 Track B nodes; 2 in-place edge fixes: `damon-dance-for-me.node.md` + `henly-maester.node.md` (SERVES: ramsay-bolton → ramsay-snow).
- `scripts/orphan-edges-audit.py` rerun → `working/audits/orphan-edges-2026-05-12.md` + cat1-full.tsv (baseline before Session 50).
- `progress/continue-prompts/2026-05-12-orphan-batch-top-nodes.md` — drafted; used by Session 50; deleted at end-of-session.
- `working/session-results/README.md` — NEW. Convention doc for watcher-handoff result files.
- `working/session-results/2026-05-12-watcher-day-orchestration.md` — NEW. This session's result file (demo + handoff).
- `working/runbooks/general-watcher.md` — updated. First-steps checks `working/session-results/`; signal table + commands include it; "check first" guidance added.
- `working/todos.md` — three new entries: MED Track A spot-check; NEW bake-session-results-into-future-prompts; FUTURE session-state.jsonl upgrade.
- Three commits: `bc19163e4` (Sessions 43-49b, 2587 files), `c54719d40` (Session 50 + convention, 372 files), `4349a62e6` (worklog rotation, 2 files).

**Decisions:** Session-results convention chosen as minimal unlock for watcher friction (per-session file vs shared log vs worklog). Worklog rejected — written too late and conflict-prone for parallel sessions. Per-file is append-by-different-actors, zero merge surface. Session 47 archived to `history/worklog-archives/archive010.md`.

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track (sequential per Matt). → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`. Pre-flight TODO: bake session-results write step into that prompt before firing.
- **MED — Track A 60-node spot-check** — partially absorbed by Session 50 audit improvement; residual remains. See `working/todos.md`.

---

### Session 50 — Orphan Edges Cat 1 Batch: Top-N Recovery (2026-05-12)

**Changes made:**
- **7 ALIAS-FIX** — added missing slug aliases to existing nodes: `crossroads-inn`→inn-at-the-crossroads (already had display-name forms but not the slug); `dragons`→dragon (species); `joffrey-i-baratheon`→joffrey-baratheon; `tommen-i-baratheon`→tommen-baratheon; `vale`→vale-of-arryn; `the-wall`→wall; `giant`→giants.
- **8 CREATE** — new nodes with `pass_origin: pass2-orphan-batch-2026-05-12`: `factions/blacks` (Rhaenyra's Dance of Dragons faction, tier-1); `factions/greens` (Aegon II's faction, tier-1); `events/age-of-heroes` (legendary era, tier-2); `locations/crypt-of-winterfell` (Winterfell burial vault, tier-1); `factions/two-betrayers` (Hugh Hammer + Ulf the White, tier-1); `events/andal-invasion` (Andal conquest of Westeros, tier-1); `factions/winter-wolves` (Cregan Stark's veterans, tier-1); `factions/bastards-boys` (Ramsay's hunters, tier-1).
- `working/wiki/data/alias-resolver.json` — rebuilt via `scripts/wiki-pass2-build-alias-resolver.py --apply` (1,433 entries).
- `graph/index/chapters/` — rebuilt via `scripts/build-mention-index.py --all`.
- `working/audits/orphan-edges-2026-05-12-post-orphan-batch.md` — post-batch audit snapshot.
- `working/todos.md` — orphan batch DONE item added; spot-check todo updated noting `bastards-boys` defect resolved.

**Delta:** Cat 1 orphan edges 1896→1673 (−223). Clean-resolving edges 18831→19055 (+224). Graph 7959→7967 nodes (+8).

**Decisions:** All 15 operations (7 alias + 8 create) completed in single window; no multi-window needed (deterministic, no classification ambiguity). Skipped `ship`, `betrothal`, `lads` (ambiguous noise — no single canonical target). Skipped date-pattern slugs per standing rule. Session 46 archived to `history/worklog-archives/archive010.md`.

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

---

### Session 49b — Case-Collision Tail Track B (2026-05-12)

**Changes made:**
- `scripts/filter-case-collision-tail.py` — NEW. Classifies all 65 remaining case-collision tail slugs into DROP / ALREADY_EXISTS / CANONICAL. Checks graph/nodes/ for exact and alias matches; applies drop rules (real-world books, disambig pages, list articles, hound names, meta-wiki, zero-source). Outputs `working/missions/case-collision-tail/canonical-slugs.txt` + `uncertain-slugs.txt`.
- **4 alias updates** to existing nodes: `arryk-cargyll` ← "Arryk (guard)", `erryk-cargyll` ← "Erryk (guard)", `dragonbinder` ← "dragon horn"/"Dragon Horn", `jeyne-fowler` ← "Fowler twins"/"the Fowler twins".
- **10 new nodes created** from chapter extraction evidence:
  - characters/: `handsome-man`, `stern-face`, `starved-man` (Faceless Men identifiers, AFFC Arya chapter), `damon-dance-for-me` (Ramsay's man, ADWD), `red-raven-free-folk` (Raymun Redbeard's brother, Free Folk), `henly-maester` (young maester at Bolton-occupied Winterfell), `grazdan-mo-ullhor` (Cleon's former owner in Astapor)
  - species/: `ice-dragon` (Old Nan's legendary creature), `ghost-grass` (Shadow Lands plant, Dothraki eschatology)
  - foods/: `wine-of-courage` (Unsullied pain-numbing training potion)
- `working/missions/case-collision-tail/drop-manifest.md` — NEW. Full record of 28 explicit drops + 27 ALREADY_EXISTS + 10 canonical created. Preserves auditability of the full 65 processed.
- `reference/architecture.md` — Fixed typo "cred sites" → "sacred sites" (line 56).
- `working/todos.md` — case-collision tail LOW item → DONE; architecture typo → DONE.

**Decisions:** Track B did NOT use multi-window+watcher as the continue prompt specified. Rationale: after filtering, the canonical list collapsed to 10 nodes (not ~15-20 expected), all with clear types and chapter evidence already in session context. The "drift potential is HIGH" rationale no longer applied. Filter step is the key finding: most "canonical" slugs were redirect-only wiki pages with zero backlinks — the script correctly identified them. 4 slugs classified as ALREADY_EXISTS turned out to need alias updates rather than new nodes (arryk, erryk, dragon-horn, fowler-twins).

**Graph total:** 7,949 → 7,959 nodes (+10).

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

---

### Session 49 — Alias-Backfill Round 2 (2026-05-12)

**Changes made:**
- `graph/nodes/locations/vale-of-arryn.node.md` — added alias `"The Vale"` to `aliases` field.
- `graph/nodes/characters/aemon-targaryen-son-of-maekar-i.node.md` — added alias `"Maester Aemon"`.
- `graph/nodes/characters/aemon-targaryen-son-of-viserys-ii.node.md` — added alias `"Prince Aemon the Dragonknight"`.
- `working/wiki/data/alias-resolver.json` — rebuilt via `scripts/wiki-pass2-build-alias-resolver.py --apply`. Three new entries in `alias_to_canonical`. Map now 1,403 entries.
- `graph/index/chapters/` — rebuilt via `scripts/build-mention-index.py --all`. 344 chapters re-indexed.

**Resolution delta:** 70.6% → **72.9%** (+2.3 pp, ~849 newly-resolved mentions). Beats the projected 72-74% range.

**Slug note:** Continue prompt expected canonical slugs `aemon-targaryen-maester` and `aemon-targaryen-dragonknight`; neither exists. The graph uses `son-of-*` naming convention. Aliases were added to the correct existing nodes (`aemon-targaryen-son-of-maekar-i` and `aemon-targaryen-son-of-viserys-ii`). Continue prompt slug expectations were stale.

**Decisions:** Aliases landed on correct existing nodes per the `son-of-*` slug convention — no new nodes created, alias-only operation as specified.

**What's next (at archive time):**
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Case-collision tail (65 slugs, optional)** — LOW priority. → continue: `progress/continue-prompts/2026-05-12-case-collision-close.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**
