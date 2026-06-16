# Next Sessions — Triage State (2026-05-13)

> **What this is:** Matt's personal roadmap AND the readable home for open continue prompts. Gitignored. Same rule as `scratch` — agents don't read this during normal work. Designed so Matt can walk away and return without forgetting where things stand. The `progress/continue-prompts/` directory mirrors the actionable Tracks below so `/continue` works, but THIS file is the canonical readable copy.

---

## ★ NEXT RECOMMENDATION (2026-05-13)

**Launch Stage 4 wiki-prose edge classifier (Track 5).**

The conversation that surfaced this:

- Today's graph (~7,967 nodes, 4,930 with edges) is genuinely good at **factual/structural** questions — genealogy, feudal hierarchy, who-rules-where. That's because the edges came from wiki infoboxes, which only encode that kind of structure.
- The locked master vocabulary has ~96 edge types, of which **~37 are entirely unpopulated**: perception (`FEARS`, `RESENTS`, `MOURNS`, `DISTRUSTS`, `HATES`, `RESPECTS`), identity (`IMPERSONATES`, `DISGUISED_AS`), prophecy (`FULFILLS`, `APPEARS_TO_FULFILL`, `SUBVERTS_PROPHECY`), narrative (`FORESHADOWS`, `PARALLELS`, `ECHOES`, `CONTRASTS`), causal (`MOTIVATES`, `TRIGGERS`, `ENABLES`, `PREVENTS`). The graph today is *blind* to the entire story-layer of ASOIAF.
- Stage 4 wiki-prose classifier reads the wiki prose body already on each node and emits typed edges from the master vocabulary. **No book passes required.** Pass 1 is done (344/344). This is cheap downstream work on data we already have.
- Even within the existing 26-type infobox subset, prose surfaces edges infoboxes don't tag — `MANIPULATES`, `BETRAYS`, `ADVISES`, `NEGOTIATES_WITH`. A character like Tyrion has 17 infobox edges today; prose probably yields 40-60 more.
- **Tier-difference, not polish.** Today: structured feudal wiki with a search bar. After Stage 4: a graph that knows the story.

**Open question — run shape:**
- Option (a) **Single Claude Code session, sequential bucket processing.** Simplest. Matt babysits one window. Smoke-test on 3 buckets, decide, run bulk. Predictable cost.
- Option (b) **Watcher + many concurrent workers (mission protocol).** Multi-window or subagent-orchestrated. Faster wall-clock. Builds on the mission-protocol patterns Sessions 45-46 established. First test of the protocol at multi-bucket scale. More moving parts.

Recommendation: **smoke-test on Option (a)** for the 3-bucket evaluation (deterministic candidates → 3 buckets → reviewer verdict). If the smoke test passes and we move to bulk run across 100+ buckets, *that* is when Option (b) earns its keep.

Pre-flight (free, deterministic):
1. Re-run cross-references index — `python3 scripts/wiki-pass2-build-cross-refs.py` (~30 sec)
2. Generate edge candidates — `python3 scripts/wiki-pass2-build-edge-candidates.py` (minutes; outputs per-bucket JSONL)
3. **THEN look at candidate volume** before committing to (a) vs (b).

Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`

---

## Where we are today (2026-05-13)

- **Pass 1**: 344/344 chapter extractions across all 5 books. ✅
- **Graph**: 7,967 nodes (was 7,583 on 2026-05-12 pre-orphan-batch; sessions 49/49b/50 added new nodes)
  - 4,930 nodes (62%) have at least one edge populated
  - 3,000 nodes (38%) have a `## Edges` header but no edges yet — Tier-B/C thin-infobox pages
- **Per-chapter mention index** (`graph/index/chapters/`): 344 files; resolution rate ~72.9% after Session 49's alias backfill
- **Per-character index** (`graph/index/characters/`): 3,910 files; 31 POVs resolve cleanly across all 344 chapters
- **Wiki cache**: 17,657 pages on disk
- **Edge vocabulary** (post-Session-52 cleanup, 2026-05-13):
  - Master `## Edge Types` section in architecture.md: **96 distinct edge types** across 14 subsections
  - Wiki-infobox subset: 26 types (the parser's `FIELD_EDGE_MAP`)
  - **Zero orphan emissions** (was 5: `DECEIVED_BY`, `KILLED_BY`, `HELD_BY` now documented as reverse-direction notes; `LOCATED_IN` normalized to `LOCATED_AT` across 21 files; `WRITTEN_BY` added to master Narrative subsection)
  - Stale "22-type lock" claim removed from architecture.md, design-philosophy.md, schema-drift-auditor.md, prose-edge-classifier.md (3 places)
  - Prose-edge-classifier now correctly points at the master 96-type vocabulary (was incorrectly restricted to the 26-type infobox subset)

---

## What's running RIGHT NOW (2026-05-13)

*(Nothing running. Edge-vocab cleanup landed; Stage 4 launch is the next decision.)*

---

## Policy reminders (so this doesn't drift)

1. **The wiki is local. Period.** 17,657 files are already in `sources/wiki/_raw/`. Agents must read from disk, not refetch. The narrow-exception clause in CLAUDE.md is for completion-of-original-crawl edge cases only, and requires explicit per-use approval, and outputs CANNOT write to `sources/`.
2. **For the case-collision losses: try reconstruction-from-cross-references first.** Free Folk has 141 backlinks; Children of the Forest has 51; Known World has 42. Other wiki pages already quote and describe these entities. Synthesizing Identity sections from cross-refs is a no-fetch path that should be exhausted before any refetch question.
3. **Standing rules from memory:** `feedback_no_external_wiki_fetch.md`, `feedback_check_existing_knowledge_first.md`, `feedback_python_before_agent.md`, `feedback_model_selection_at_session_start.md`, `feedback_continue_prompts_include_model.md`. Agents have repeatedly violated some of these — guard against drift.
4. **Every continue prompt declares a recommended model.** Don't paste a /continue command without first switching to the recommended model in the new session.

---

## ✅ Track 1 — Wiki prose extraction backfill (DONE 2026-05-12, Session 42)

Attached prose to 990 nodes. See worklog Session 42 entry and `working/audits/wiki-prose-coverage-2026-05-12/execution/{coverage.jsonl,summary.md,attach-prose-summary.json}` for full audit trail. Tooling: `scripts/audit-prose-coverage.py` + `scripts/wiki-pass2-attach-prose.py`. Both idempotent — safe to re-run if more prose files appear.

---

## Track 2 ★ — Missing-node backfill (138 Bucket A pages)

**Mirror file (for `/continue`):** `progress/continue-prompts/2026-05-12-missing-node-backfill-bucket-a.md`

**Recommended model:** Sonnet 4.6 (`claude-sonnet-4-6`). Pure Python script work — no agent reasoning, no extraction. Opus wasteful here. Haiku 4.5 also viable if budget tight.

**Status:** RUNNING (2026-05-12) in a separate Claude Code session.

### What this work is

Promote the 138 wiki pages that Pass 1 actively references but were never given a graph node. Highest-signal slugs (by Pass-1 mention count):

| Slug | Pass-1 hits | Likely type |
|---|---|---|
| `godswood` | 36 | place.location (or new place.feature) |
| `flea-bottom` | 31 | place.location |
| `old-gods` | 22 | organization.religion |
| `seastone-chair` | 14 | object.artifact |
| `chatayas-brothel` | 12 | place.location |
| `black-cells` | 11 | place.location |
| `queens-men` | 9 | organization.faction |
| `unsullied` | 9 | organization.faction |
| `cinnamon-wind` | 8 | object.artifact (ship) |
| `valyrian-steel-dagger` | 8 | object.artifact |

Full Bucket A list: `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.{md,json}`.

### Why they were missed

Path B's categorizer (`scripts/wiki-infobox-parser.py` + the `CATEGORY_TYPE_MAP` constant) routed them to `unknown`. The Stage 3 Python emitter skips `unknown`-typed pages. The result: wiki page exists in `sources/wiki/_raw/`, but no graph node was emitted.

### Investigate-first step (15 minutes)

1. **Verify wiki cache** — for the top-10 slugs above, check `sources/wiki/_raw/<Capitalized_Page>.json` exists. Most should.
2. **Check page-index entries** — grep `working/wiki/data/page-index.jsonl` for each one. If `entity_type_guess: unknown`, the categorizer rule is the bug source.
3. **Check infobox-data** — grep `working/wiki/data/infobox-data.jsonl`. Does the page have an infobox? If not, the page is text-only and the emission path must handle that.
4. **Slug-collision check** — grep `graph/nodes/` for any existing file with that slug or related slugs (e.g., `godswood` might collide with `winterfell-godswood`).

### Decisions to make

1. **New entity types?** `godswood` is generic. Lean: force `place.location` with `aliases: ["the godswood"]`; defer type-system invention to Stage 4.
2. **`old-gods` taxonomy** — `organization.religion` (like `the-faith-of-the-seven`) or `concept.theological`? Lean: religion.
3. **Promotion strategy** — all new nodes, no overwrites. Write-if-not-exists; atomic-rename via staging temp file.
4. **Two-script approach** — (a) categorizer fix + global re-emit, or (b) targeted 138-slug emitter? Lean: (b) for speed, file (a) as follow-up.

### Existing pieces to reuse

- `scripts/wiki-pass2-emit-deterministic.py` — skeleton renderer.
- `scripts/wiki-pass2-extract-prose.py` — prose extractor.
- `scripts/wiki-pass2-attach-prose.py` (NEW Session 42) — appends prose to existing body.
- `working/wiki/data/page-index.jsonl`, `infobox-data.jsonl`, `cross-references.jsonl`.
- `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.json`.

### Smoke-test slugs (verify after)

- `godswood` → `graph/nodes/locations/godswood.node.md`
- `flea-bottom` → `graph/nodes/locations/flea-bottom.node.md`
- `seastone-chair` → `graph/nodes/artifacts/seastone-chair.node.md`
- `old-gods` → `graph/nodes/religions/old-gods.node.md`
- `unsullied` → `graph/nodes/factions/unsullied.node.md`

Smoke-test post-action: re-run `scripts/audit-missing-nodes.py`; Bucket A should drop 138 → near-zero.

### DO NOT

- Refetch any wiki pages. Hard rule.
- Touch Stage 1 agent-rich nodes (`pass_origin: pass2-wiki`).
- Overwrite existing graph nodes on slug-collision — log instead.
- Try to fix the 125 case-collision pages here (separate todo / Track 4).
- Auto-run `/endsession`.

### After this lands

- Mark `working/todos.md` HIGH "Missing-node backfill: 138 Bucket A unpromoted wiki pages" as `[x] DONE`.
- Mark Track 2 ✅ in this file.
- Re-run `scripts/build-mention-index.py --all` — resolution rate should jump past 75%.
- Re-run `scripts/build-character-indexes.py --all` — richer `mentioned_in` lists.
- Add Session entry to worklog.

---

## Track 3 ★ — Per-LOCATION + per-ARTIFACT index roll-ups

**Mirror file (for `/continue`):** `progress/continue-prompts/2026-05-12-location-artifact-index-rollup.md`

**Recommended model:** Sonnet 4.6 (`claude-sonnet-4-6`) or Haiku 4.5 (`claude-haiku-4-5-20251001`). Pure Python — script parameterization + smoke-testing. Opus wasteful. Sonnet preferred for the design-decision moments; Haiku fine if decisions are pre-made.

**Status:** RUNNING (2026-05-12) in a separate Claude Code session.

### What this work is

Extend the per-character-index pattern (Session 41) to other node types. Parameterize `scripts/build-character-indexes.py` into `scripts/build-entity-indexes.py --type <type-prefix>`. Output: `graph/index/locations/`, `graph/index/artifacts/`, `graph/index/houses/`. Schema mirrors character-index. Stage 4 component (b) prerequisite for non-character node types.

### Read first

- `scripts/build-character-indexes.py` — reference implementation; read end-to-end.
- `graph/index/characters/_summary.json` — output schema to match.
- `worklog.md` Session 41 entry — design rationale.

### Decisions to make

1. **One script or several?** Lean: parameterize into `build-entity-indexes.py --type <prefix>`. POV resolution gated to `character.*`.
2. **Which node types?** Tier 1: `place.*` + `object.artifact*`. Tier 2: `organization.house`. Defer factions/religions/events/titles/species/concepts.
3. **Semantic model for non-characters** — single flat `chapters.referenced_in` OR section-aware `chapters.in_<section>_section` + `chapters.in_raw_list`? Lean: section-aware (preserves Pass-1 semantics).
4. **`out_edge_count`** — same logic as characters: count `- EDGE_TYPE:` lines in `## Edges` block.

### Pieces to reuse

- `scripts/build-character-indexes.py` — copy and parameterize.
- `graph/index/chapters/{book}/*.mentions.json` — input data; already tags section + node-type for locations + artifacts.
- `working/wiki/data/backlink-counts.json` — `in_edge_count` baseline.

### Smoke-test slugs

- **Locations:** `winterfell` (100+ chapters), `kings-landing` (densest), `the-wall`, `meereen`, `oldtown`.
- **Artifacts:** `iron-throne`, `heartsbane` (Sam chapters), `lightbringer` (Stannis/Melisandre), `longclaw` (Jon), `oathkeeper` (Brienne/Jaime).
- **Houses:** `house-stark`, `house-lannister`, `house-targaryen`, `house-frey`, `house-mormont`.

Smoke-test post-action: spot-check 5 location indexes + 5 artifact indexes. Confirm chapter counts make sense.

### Expected delta

- ~7,000 new index files across `graph/index/{locations,artifacts,houses}/`.
- Stage 4 component (b) unblocked for these node types.

### DO NOT

- Touch existing `graph/index/characters/` (correct from Session 41).
- Modify Pass-1 extractions.
- Try to canonicalize aliases at this layer (mention-index already handles).
- Add type-specific logic that doesn't generalize.
- Auto-run `/endsession`.

### After this lands

- Mark a new todo in `working/todos.md` as `[x] DONE`.
- Mark Track 3 ✅ in this file.
- Stage 4 component (b) is fully unblocked for primary node types.
- Add Session entry to worklog.

---

## Track 4★ — Case-collision crawl-bug remediation (125 pages)

> **NEW (2026-05-12):** Track 4 is now the **first real test of the mission protocol** (`working/agent-fleet-specs/mission-protocol.md`). Top-10 subset extracted as a concrete mission file at `working/agent-fleet-specs/missions/2026-05-12-case-collision-top-10.md`. Remaining 115 pages = follow-up mission(s) after the top-10 mission lands and the pattern is validated.

**Mission file (top-10 subset):** `working/agent-fleet-specs/missions/2026-05-12-case-collision-top-10.md`

**Recommended for top-10 mission:** Sonnet 4.6 workers + Opus 4.7 watcher (per locked protocol). Watcher agent at `.claude/agents/watcher.md` (v0 DRAFT, written Session 45). First mission run validates BOTH the protocol AND the watcher prompt.

**Status:** Top-10 mission file QUEUED; full Track 4 remains QUEUED for follow-up.

### Original Track 4 framing (kept for reference)

**Recommended model:** Sonnet 4.6 for path (a) reconstruction (light reasoning per page). Opus only if Matt approves path (b) refetch AND wants tighter cross-reference synthesis.

**Status:** QUEUED. No continue prompt file yet — write one when this track activates.

### Goal

Restore canonical content for the 125 wiki pages whose body got overwritten by redirect HTML during the original crawl.

### Two paths, in priority order

- **(a) Reconstruction from cross-references** — try this FIRST. For each affected page, gather all wiki pages that link to it (via `working/wiki/data/cross-references.jsonl`), extract the sentences that mention the entity, and synthesize an Identity section. No fetch. Lower fidelity than canonical content but probably good enough for most entries. The Pate-novice node (Session 41) was hand-crafted from Pass 1 content using a similar pattern.
- **(b) Narrow-exception refetch** — only if reconstruction proves inadequate AND Matt explicitly approves. 125 `cloudscraper` API calls to the MediaWiki action=parse endpoint. Output lands in `working/wiki/data/recrawl-case-collisions/` for review. Promoting verified-good files into `sources/` is a manual Matt-only step.

### Major entities at stake

Free Folk (141 backlinks), Children of the Forest (51), Known World (42), Red Priest (40), Valar Morghulis, House Words, Beyond the Wall (book), POV Character. Many are foundational worldbuilding pages.

### DO NOT

- Path (b) without Matt's explicit per-use approval.
- Write directly to `sources/` — CLAUDE.md forbids this even for exception fetches.

---

## Track 5 ★★ — Stage 4 v1 prose-edge-classifier (NEXT RECOMMENDED, 2026-05-13)

**Continue prompt:** `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`

**Recommended model:** Sonnet 4.6 for the orchestrator session. Classifier agent itself is Opus 4.7 by default — downgrade to Sonnet **only after** a 3-bucket smoke test passes `prose-edge-reviewer` CLEAN or CONCERNS-low.

**Status:** READY. Tracks 2 + 3 + edge-vocab cleanup (Session 52, 2026-05-13) all landed. No remaining blockers.

### Goal

Generate typed graph edges from prose narrative. Today's graph reflects wiki *infobox* structure (genealogy, feudal hierarchy); Stage 4 surfaces the *narrative* layer the wiki prose describes — perception, identity, prophecy, narrative parallels, causal chains.

### Why this is a tier-change, not polish

- 37 of the 96 master edge types are entirely unpopulated today (the perception/identity/prophecy/narrative/causal verbs). The graph is *blind* to the story-layer of ASOIAF.
- Even within the populated 26-type infobox subset, prose finds edges infoboxes don't tag — `MANIPULATES`, `BETRAYS`, `ADVISES`, `NEGOTIATES_WITH`. Edge density per node could grow 3-5x.
- A chat UI on today's graph = structured feudal wiki with search. A chat UI on the Stage 4 graph = something that can answer "what does Tyrion fear?" or "which characters mourn Robb Stark?" with sourced edges.

### No book passes required

- Pass 1 is done (344/344 across 5 books). The chapter extractions live in `extractions/mechanical/{book}/` and aren't going anywhere.
- Stage 4 wiki-prose classifier reads **wiki prose** (already in `graph/nodes/.../*.node.md`), not book prose.
- The richer Stage 4 components (chapter-evidence backfill, cross-identity rewrites) read **Pass 1 output**, not raw chapters. Mechanical lookup, not re-extraction.
- The only thing that would require new book passes is the separate Pass 1.5 dialogue/mention-index track (`progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md`) — NOT Stage 4.

### Open question — run shape

- **Option (a) — Single Claude Code session, sequential bucket processing.** Simplest. Matt babysits one window. Smoke-test on 3 buckets, decide, run bulk. Predictable cost. Default for the smoke phase.
- **Option (b) — Watcher + many concurrent workers (mission protocol).** Multi-window or subagent-orchestrated. Faster wall-clock. Builds on the mission-protocol patterns Sessions 45-46 established. First test of the protocol at multi-bucket scale. More moving parts.

**Recommendation:** Smoke-test on Option (a). The 3-bucket evaluation is small enough that orchestrating workers is overkill. If the smoke passes and we move to bulk across 100+ buckets, *that* is when Option (b) earns its keep — at bulk scale, the wall-clock savings dominate the orchestration overhead.

### Pre-flight (free, deterministic)

```bash
# 1. Re-run cross-references index (~30 sec, $0)
python3 scripts/wiki-pass2-build-cross-refs.py

# 2. Generate edge candidates (minutes, $0; per-bucket JSONL output)
python3 scripts/wiki-pass2-build-edge-candidates.py

# 3. THEN inspect candidate volume — that determines bulk-run shape
ls -la working/wiki/pass2-buckets/*/prose-edge-candidates/*.candidates.jsonl | wc -l
wc -l working/wiki/pass2-buckets/*/prose-edge-candidates/*.candidates.jsonl | tail -1
```

### Effort + cost

- Smoke phase (3 buckets, Opus classifier + Sonnet reviewer): ~$5-15
- Bulk phase (Sonnet if smoke clean, Opus if not): ~$40-80 (Sonnet) / ~$100-200 (Opus)
- Multi-session work — not finished in one sitting

### Critical reminders (from continue prompt)

- **NEVER modify Python-emitted infobox edges.** Prose edges go under a SEPARATE `## Edges (prose-derived)` subheading. Never touch existing `## Edges`.
- **NEVER touch Stage-1 character nodes (`prompt_version: v1`) without carve-out.** Stage-3 nodes (`prompt_version: v1-python`) same rule. Carve-out for Stage 4: read prose, emit prose-derived edges under new subheading, do not modify existing prose or existing `## Edges`.
- **NEVER drop anything from `sources/`.** Hard rule.
- **NEVER auto-launch the bulk run.** Each phase (Step 2 generation, Step 3 classification, Step 4 promotion) confirmed separately with Matt.
- **NEVER run `/endsession` without explicit permission.**
- Sequential, never parallel — across the 4 pipeline steps. Parallelism is an option WITHIN Step 3 only.

---

## Track 6 — Mission protocol + watcher refinement (NEW 2026-05-12)

**Status:** DRAFTs in repo — `working/agent-fleet-specs/mission-protocol.md` (v0) + `.claude/agents/watcher.md` (v0). Both written Session 45. Not locked. The first real mission (Track 4 top-10) is the smoke test for both.

**What this track is:** After the first mission lands, redline both DRAFTs based on observed friction. Decide answers to the 5 open questions in the protocol's "Open questions" section. Tighten the watcher's escalation-surface format if it proved verbose or vague. Not a session you sit down to do until at least one mission completes.

**Recommended model:** Sonnet 4.6 for the doc edits + agent prompt refinement.

---

## Defer / low priority

- **Year-page type bug** (10 nodes mis-typed `character.human`) — bundle with Stage 4 temporal-edges work.
- **Audit Pass 1 short-stem pov_character values** — only 1 chapter had `pov_character: Catelyn` without surname. Cosmetic.
- **2nd round of alias-backfill** (`the-vale`, `maester-aemon`, `prince-aemon-the-dragonknight`) — would push mention-index resolution past 75%. Cheap but not urgent.
- **Quotes-as-evidence surfacing** (Session 42 idea, Matt aside) — `## Quotes` sections on attached nodes carry chapter cite_refs and could feed a future query UI. Not actionable until there's a query UI.

---

## What can run in parallel

| Group | Tracks | Why parallel-safe |
|---|---|---|
| Group A (running NOW) | 2 + 3 | Different scripts, different output directories. Track 2 writes new nodes in `graph/nodes/<type>/`; Track 3 writes new index dirs in `graph/index/<type>/`. Zero overlap. |
| Group B | 2 + 3 + 4(a) | Add Track 4(a) — it only reads cross-references and writes to specific case-collision slugs not in Bucket A. No conflict. |
| Conflict | 4(b) refetch | Requires Matt's approval gate. Don't queue concurrently. |
| Conflict | 5 (Stage 4) | Best AFTER 2+3 (richer source data). Not strictly required but classifier sharpness improves. |

---

## Sequencing decisions to make

1. **Case-collision policy** — which of (a) reconstruction or (b) refetch? Default (a). Decide whether (b) is on the table at all.
2. **Per-LOCATION/ARTIFACT index scope** — Track 3's tier-1 (locations+artifacts) is fixed; tier-2 (houses) decided yes per lean. Tier-3 (factions, religions, events, titles, species, concepts) deferred unless Stage 4 hits a wall.
3. **Stage 4 smoke-test gating** — when Track 5 starts: Sonnet smoke-test on 3 representative buckets; `prose-edge-reviewer` checks CLEAN/CONCERNS-low. If fails, fall back to Opus.

---

## Long-term horizon (don't lose sight of)

- **Goal:** graph quality for agent traversal (`project_real_goal_graph_for_agents.md`). Every track above improves agent retrieval depth or breadth.
- **Stage 4 components** per memory `project_stage4_richest_form.md`:
  - (a) prose-inferred edges from `cross-references.jsonl`
  - (b) chapter-evidence backfill — needs per-character (✅ done Session 41) + per-location + per-artifact indexes (Track 3, running)
  - (c) rich Identity rewrites for top-N high-traffic nodes — needs prose extraction done first (✅ Session 42 closed the deterministic-Python gap; agent-rich rewrites remain a separate scope)
- **D&E Pass 1** (THK/TSS/TMK) — deferred enrichment pass, not on critical path. Decision 2026-05-06.
- **first_available / spoiler gating** — deferred entirely until post-first-release backfill. Don't reason about it per-node.

---

## How to use this file

- Step away from the project? You don't have to remember any of this. Come back, read this file, decide which Track to pick.
- Each Track has its FULL continue-prompt content embedded above. Equivalent file in `progress/continue-prompts/` exists for the `/continue` command's lookup — they're mirrors.
- To kick off a Track: switch to the recommended model FIRST, then `/continue <prompt-filename-without-.md>` in a fresh session.
- When a Track lands, mark ✅ here, then add a worklog Session entry, then update todos.md.
- This file is gitignored — overwrite freely as priorities shift.
