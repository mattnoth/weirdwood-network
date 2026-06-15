# Stage 4 v1 — Prose-Edge Classifier + Cross-Identity Detection

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-05-01 end of Session 29. **Updated 2026-05-01 Session 30:** Pass 1 dependency now resolved up-front — Pass 1 across ACOK/ASOS/AFFC/ADWD is being completed BEFORE this work track per Matt-decision Session 30. The AGOT-only contradiction-sweep carve-out is dropped; this prompt now describes a full-5-book contradiction sweep. Pre-flight check: confirm `extractions/mechanical/{acok,asos,affc,adwd}/` are all populated to chapter-count parity before launching Step 3.
>
> **Updated 2026-05-12 (Session 51):** Added Step 13 — write session-results file at end (and at smoke-test→bulk-run transition). See `working/session-results/README.md`. Pass 1 dependency now fully met (344/344 across 5 books, including ASOS).
>
> **Updated 2026-05-13 (Session 53) — PHASE 1 COMPLETE.** Substrate work landed: 344 `meta.chapter` nodes added to `graph/nodes/chapters/` (new `Meta` parent entity type in architecture.md); 12 mis-typed `event.battle` chapter nodes deleted; cross-references rebuilt (91,381 → 161,060 rows); candidate generator built and run in `--plan` mode (141,067 survivors vs 77,802 pre-migration). Observability tooling built: `scripts/build-edge-type-counts.py` (baseline: 21,087 instances across 58/100 types; 42 unpopulated types are Stage 4's targets) and `scripts/build-vocab-gap-log.py` (empty-state baseline). Curation surface created at `curation/edge-vocabulary-candidates.md` with proposed new types (DREAMS_OF, WARGS_INTO, SACRIFICES, RESURRECTS, VOWS_TO, etc.). See `working/session-results/2026-05-13-stage4-prose-edge-classifier-phase1.md` for full session record. **Phase 2 starts below — do NOT re-run Phase 1 work.**
>
> **Recommended model:** **Sonnet 4.6 for the orchestrator session.** For the classifier agent itself: per Session 37 model-fit audit, prose-edge-classifier downgrades Opus → Sonnet 4.6 *gated on smoke test*. **Session 53 update**: smoke test target is now **Haiku 4.5 first** (per memory `feedback_model_selection_at_session_start.md` — default to cheapest viable). If Haiku CLEAN/CONCERNS-low → adopt for bulk. If SYSTEMATIC issues → upgrade to Sonnet, re-smoke. If Sonnet fails → keep Opus. Edit `.claude/agents/prose-edge-classifier.md` line 5 `model:` only after smoke verdict.

---

## Phase 2 — Co-mention generator + classifier adaptation + smoke test + bulk run

**Pre-flight (Phase 1 already complete — skip if migration verifiably ran):**
1. Confirm: `ls graph/nodes/chapters/ | wc -l` → 344.
2. Confirm: `find graph/nodes/events -name 'a-*-chapter-*'` → empty.
3. Confirm: `working/wiki/data/cross-references.jsonl` line count ~161k (was 91k pre-migration).
4. Read `working/session-results/2026-05-13-stage4-prose-edge-classifier-phase1.md` for full Phase 1 context.

**Phase 2 steps:**

### Step A — Matt review of vocabulary candidates ✅ COMPLETE (Session 53, 2026-05-13)

All 13 proposed types accepted + 1 reverse-direction note. New subsection **Magic & Supernatural** added to architecture.md. Vocabulary went from 100→114 types, 14→15 subsections. Classifier prompt updated with new vocabulary + disambiguation guidance. See `curation/edge-vocabulary-candidates.md` § "Session 53 Review Outcome" for the full record. **Skip this step on Phase 2 launch.**

### Step B — Build co-mention candidate generator

The existing `scripts/wiki-pass2-build-edge-candidates.py` produces `{source, target}` rows from cross-references — useful for character/house/location pages where source IS the entity. For chapter pages, the in-world edges we want live between TWO target entities co-mentioned in the chapter prose, not between the chapter and a target.

Build `scripts/wiki-pass2-build-comention-candidates.py`:
- Input: chapter-page prose files at `working/wiki/pass2-buckets/meta-chapters-*/prose/<slug>.prose.md`.
- For each chapter, walk the prose paragraph-by-paragraph. Find all `[anchor](wiki:Page)` links per paragraph. For each pair (A, B) co-occurring in same paragraph:
  - Emit a co-mention candidate `{source_slug: A, target_slug: B, evidence_chapter: <chapter-slug>, evidence_paragraph: <para-text>, source_section: <heading>}`.
  - Apply same filters as the edge-candidate script: drop if edge already exists between A and B, drop self-edges, alias-resolve.
- Output per-chapter JSONL files at `working/wiki/pass2-buckets/meta-chapters-<book>/comention-candidates/<chapter-slug>.candidates.jsonl`.

Estimated volume: each chapter prose has ~50-200 paragraph-level entity pairs. 344 chapters × ~100 pairs = ~30-70k co-mention candidates. **Run `--plan` first** to see actual count.

### Step C — Build Pass 1 relationships candidate generator (optional for v1; can defer to v1.1)

Walk `extractions/mechanical/{book}/*.extraction.md` files. Parse the "Relationships Observed" tables. Each row → structured candidate `{source_slug, target_slug, asserted_relation_text, evidence_chapter, evidence_paragraph}`. The "asserted_relation_text" is already in natural-language form — the classifier maps it to a vocabulary type.

This is high-signal because Pass 1 was Opus reading the actual chapter text. **Recommend deferring to v1.1** to keep Phase 2 scope manageable — the co-mention generator covers most of the same ground via wiki chapter summaries.

### Step D — Adapt classifier prompt for 2 candidate shapes

`.claude/agents/prose-edge-classifier.md` currently expects the source→target shape from `wiki-pass2-build-edge-candidates.py`. Add support for the co-mention shape (different field layout — `evidence_chapter` instead of source's own prose body).

Single agent prompt, two candidate-row formats, both produce the same 4 decision outcomes (`emit_edge` / `reject_just_mention` / `escalate_cross_identity` / `escalate_disambiguation`).

### Step E — Haiku 4.5 smoke test on 3 buckets

1. Edit `.claude/agents/prose-edge-classifier.md` line 5: `model: opus` → `model: haiku`.
2. Pick 3 representative buckets: 1 character-heavy (e.g., `characters-other-c-d`), 1 location-heavy (e.g., `locations-something`), 1 chapter bucket (`meta-chapters-asos`).
3. Run classifier on those 3 buckets (per-source-slug invocation).
4. Run `prose-edge-reviewer` against output.
5. **CLEAN/CONCERNS-low** → adopt Haiku for bulk. **SYSTEMATIC issues** → upgrade to Sonnet, re-smoke. **Sonnet fails** → keep Opus.

### Step F — Bulk run

Run classifier across all buckets at the smoke-tested model. Write per-source JSONL outputs. Don't promote yet.

### Step G — Build promotion script + promote

Write `scripts/wiki-pass2-promote-prose-edges.py`:
- Read each `prose-edges/<slug>.edges.jsonl`.
- For each `emit_edge` decision, append to source node's body under new `## Edges (prose-derived)` heading.
- Atomic-rename pattern. Validator confirms infobox `## Edges` section is byte-equal before/after.

Run promotion. Re-run `scripts/build-edge-type-counts.py` for the after-snapshot. The before/after delta tells us exactly which of the 42 unpopulated types Stage 4 filled.

### Step H — Cross-identity follow-on + contradiction sweep

Process the escalation queues (cross-identity candidates → cross-identity-detector; ambiguous → disambiguation-resolver). Run the Pass 1 contradiction sweep against AGOT extractions (Step 11 of the original v1 plan — still valid).

### Step I — Write session-results file

Per `working/session-results/README.md` convention. Headline numbers (candidates classified / accepted / rejected / escalated, vocabulary types newly populated, infobox edges touched = 0). Watcher handoff.

---

## Why this work, why now

Stage 4 v1 discovers the edges that infobox extraction couldn't see — prose-derived single-page edges, cross-page edges, and cross-identity merges (Reek=Theon, Alayne=Sansa). It is the highest-leverage unblocked work in the project once Pass 1 corpus completion lands.

**Readiness:** Stage 3 promotion stable (Session 28+29). Schema-drift audit clean (0 HIGH). Cross-references index built (Session 26: `working/wiki/data/cross-references.jsonl`). Alias resolver built (Session 26: `working/wiki/data/alias-resolver.json`). Locked master edge vocabulary (~96 types) in `reference/architecture.md` § "Edge Types (Relationship Categories)"; wiki-infobox subset (~26 types) is parser-only. Edge vocab drift cleaned up Session 52 (2026-05-13). 7,563+ graph nodes across 19 type directories.

**Pass 1 dependency** — corpus-complete before this work starts (per Session 30 sequencing decision; see `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`). All 5 books contribute to the contradiction sweep — no AGOT-only carve-out. **Hard pre-flight:** verify `extractions/mechanical/{agot,acok,asos,affc,adwd}/` extraction counts match `sources/chapters/{agot,acok,asos,affc,adwd}/` chapter counts (344/344 across all books). If short, this work is blocked — finish Pass 1 first.

Prose-edge discovery + cross-identity detection still don't strictly need Pass 1 (they read wiki node prose), but bundling all three components into a single Stage 4 v1 — now that Pass 1 isn't gating — gives the cleanest single deliverable.

---

## Hard constraints (carry-forward, non-negotiable)

These constraints have been re-emphasized across multiple sessions. Read them carefully:

- **NEVER modify Python-emitted infobox edges.** They are stable. Prose-derived edges go under a SEPARATE `## Edges (prose-derived)` subheading. Never touch the existing `## Edges` section.
- **NEVER touch Stage-1 character nodes (`prompt_version: v1`) without explicit Stage-1 carve-out.** The carve-out for Stage 4 is: **read their prose; emit prose-derived edges under the new subheading; do NOT modify their existing prose body or existing `## Edges`.** Stage-3 nodes (`prompt_version: v1-python`) follow same rule (treat as immutable).
- **NEVER modify the locked master edge vocabulary** (~96 types in `reference/architecture.md` § "Edge Types (Relationship Categories)") without going through formal procedure (architecture.md → parser FIELD_EDGE_MAP if infobox-derived → re-run parser). Stage 4 must operate within the master vocabulary; agents file `vocabulary-gap` questions for unfit relationships rather than invent.
- **NEVER drop anything from `sources/`.** All bucket bundles, all node files, all chapter files preserved.
- **NEVER auto-launch agent runs without confirming each batch with Matt.** Each phase (Step 2 generation, Step 3 classification, Step 4 promotion) confirmed separately.
- **NEVER run `/endsession` without explicit permission.** Hard rule — historically violated multiple times.
- **`first_available` not emitted on edges.** Same deferral rule as nodes — backfill via deterministic script post-first-release.
- **Sequential, never parallel.** Stage 4 candidate generation + classification + promotion run in sequence. Three parallel tabs is an OPTIMIZATION inside Step 3 only — not parallelism across steps.

---

## State at session start (verify before doing anything)

```bash
# Verify HEAD
git log --oneline -3
# Expected top: d6362f74 Year-page chronology extraction...

# Verify graph state
for d in graph/nodes/*/; do echo "  $(basename $d): $(ls $d 2>/dev/null | wc -l | tr -d ' ')"; done
# Expected total: 7,563 (with _conflicts/_unclassified/_stage3-preview)

# Verify cross-references index exists
ls -la working/wiki/data/cross-references.jsonl
# Expected: 81,090 lines, ~25 MB

# Verify alias resolver exists
ls -la working/wiki/data/alias-resolver.json
# Expected: thousands of aliases mapped

# Verify chronology data exists (Session 29 deliverable)
ls -la working/wiki/data/chronology-events.jsonl
# Expected: 2,245 lines

# Verify locked edge vocabulary
grep -c '^| `[A-Z_]*` |' reference/architecture.md
# Should match the master ~96-type vocabulary (all CAPS edge types in `## Edge Types` section)
```

---

## Pipeline shape (4 steps, each gated by Matt approval)

### Step 1 — Re-run cross-references index (deterministic Python, ~30 sec, $0)

Already built in Session 26. Re-run it to refresh against today's prose corpus:

```bash
python3 scripts/wiki-pass2-build-cross-refs.py
```

Output:
- `working/wiki/data/cross-references.jsonl` — 81,090 rows of `{source_slug, target_slug, anchor_text, section, snippet}`
- `working/wiki/data/backlink-counts.json` — inverted index `{target_slug: {in_count, out_count, ratio, sample_sources}}`
- `working/wiki/data/cross-refs-summary.md`

**Inspect** before Step 2: examine backlink-count distribution. Centrality is empirical — let the data drive the candidate-filter threshold (Step 2).

### Step 2 — Build candidate edge generator (deterministic Python, ~30 sec, $0)

**This needs writing.** No existing script — design and build it.

**Script:** `scripts/wiki-pass2-stage4-candidate-generator.py`

**Logic:**
1. Walk every `cross-references.jsonl` row.
2. For each (source_slug, target_slug) pair, check whether ANY edge of ANY type already exists between them in their `## Edges` sections (read both source.node.md and target.node.md frontmatter+edges).
3. If yes → drop (already-known edge from infobox).
4. If no → emit candidate row `{source_slug, target_slug, anchor_text, section, snippet, backlink_count: target.in_count}`.
5. Filter targets not in graph after alias-resolution → drop, log to summary as broken-link.
6. Filter low-confidence: `target.in_count < 2` AND `source.section in {Quotes, Notes}` → drop (probably trivia mention).
7. **Sort/group output by source_slug** — emit one JSONL file per source: `working/wiki/pass2-buckets/<source_bucket>/prose-edge-candidates/<source_slug>.candidates.jsonl`.

**Survivor set estimate:** 5K-15K candidates after filtering vs ~30K naïve pass.

**Run:**
```bash
python3 scripts/wiki-pass2-stage4-candidate-generator.py --plan
# Inspect distribution, expected counts, edge-section parsing accuracy.
python3 scripts/wiki-pass2-stage4-candidate-generator.py --apply
# Confirm with Matt before --apply.
```

**Critical correctness checks before --apply:**
- Sample-test edge-section parsing on 5 nodes — make sure existing edges aren't being missed (would create duplicate prose-edge proposals).
- Check that alias-resolver is consulted before declaring a target broken.
- Verify Stage-1 nodes' `## Edges` sections are read (their format may differ from Stage-3).

### Step 3 — Agent classification (LLM, 3-5 hrs wall-clock, $50-100)

**Agent:** `prose-edge-classifier` (stub at `.claude/agents/prose-edge-classifier.md`; full prompt needs writing).

**Agent prompt to write** (key requirements):
- Reads ONE source slug's candidates JSONL + the source's prose body + each candidate target's frontmatter (slug, type, aliases).
- For each candidate, decides exactly one of:
  - `emit` with `edge_type` from the locked master vocabulary (~96 types in `## Edge Types`)
  - `reject` as just-a-mention (anchor text in prose without relational meaning)
  - `escalate-cross-identity` — flag as `SAME_AS` candidate (e.g., Reek prose mentions Theon in same sentence with identity-equating phrasing)
  - `escalate-questions-for-matt` — ambiguous case
- Emits ONE output file: `working/wiki/pass2-buckets/<bucket>/prose-edges/<source_slug>.edges.jsonl`
- Single-writer-per-file: agent NEVER touches existing nodes, never modifies skeleton/, never modifies prose/.
- Forbidden: emit edge types not in the locked vocabulary.

**Agent prompt should reference:**
- `reference/architecture.md` for the master locked vocabulary (~96 types in `## Edge Types (Relationship Categories)`)
- The source slug's prose file at `working/wiki/pass2-buckets/<bucket>/prose/<slug>.prose.md`
- Each target's frontmatter from `graph/nodes/<type>/<slug>.node.md` (first 20 lines only — for type/aliases lookup)

**Run shape (3-5 parallel tabs in iTerm via weirwood-style launcher):**
- Stage 3 launcher pattern works: `wiki-pass2.sh stage4 <bucket-glob>` analog
- Bucket-by-bucket — one bucket per tab — never share state across tabs.
- Pre-flight cost projection: count survivors per bucket × $0.05/candidate ≈ total. Show Matt before running.

**Tier prioritization:** mirror Stage 3's Tier A/B split. Only run prose-edge classification on Tier-A nodes (prose-rich). Tier-B nodes have less prose anyway → defer to v2.

### Step 4 — Promote prose-edges to nodes (deterministic Python, $0)

**Script:** `scripts/wiki-pass2-stage4-promote.py`

**Logic:**
1. Read each `prose-edges/<slug>.edges.jsonl`.
2. For each accepted edge, append to the corresponding node's body under a new `## Edges (prose-derived)` heading (NEW heading, distinct from existing `## Edges`).
3. Atomic-rename pattern (same as Stage 3-promote).

**Validator update needed:** before/after byte-equality check on the existing `## Edges` section — confirm no infobox edges modified. If equal, promote; if different, conflict-bucket.

**Validator script:** extend `scripts/wiki-pass2-validator.py` OR write a Stage-4 specific validator.

---

## Cross-identity detection (sub-component of Step 3)

When the prose-edge-classifier flags `escalate-cross-identity`, those candidates feed `cross-identity-detector` (stub at `.claude/agents/cross-identity-detector.md`). The detector reads:
- Both candidate slugs' frontmatter (aliases, type)
- Wiki redirect chains for both pages
- Alias-overlap signal from the alias resolver
- Surrounding prose where both names appear

Decides: emit `SAME_AS` edge OR reject as coincidence.

For Stage 4 v1: route cross-identity flags to a queue file `working/wiki/pass2-buckets/cross-identity-queue.jsonl`. Decide later whether to run cross-identity-detector inline (during Step 3) or as a follow-on Step 3.5. Current lean: follow-on, smaller batch, lower volume → easier to review.

**Known cross-identity targets** (high-confidence):
- Reek = Theon Greyjoy
- Alayne Stone = Sansa Stark
- Knight of the Laughing Tree = Lyanna Stark (added in Session 28)
- Mance Rayder = Abel (ADWD)
- Daario Naharis (multiple-actor identity)
- The Pisswater Prince = Aegon ?

The detector's confidence threshold should be high — `SAME_AS` is a strong claim. Prefer to escalate to `questions-for-matt` over auto-emit when in doubt.

---

## Contradiction sweep (AGOT v1)

Pass-1 mechanical extractions for AGOT live at `extractions/mechanical/agot/agot-{pov}-{NN}.extraction.md` (73 chapters complete).

**Goal:** find cases where wiki node prose says X about a character/event, but Pass 1 extraction says Y. Surface for human review (`curation/candidates.md`), not auto-resolve.

**Pipeline:**
1. Python: build a (slug → AGOT-Pass-1-mentions) inverted index from extraction files' Raw Entity Lists + Relationships Observed sections.
2. Agent: per slug, read wiki node prose + AGOT mentions. Surface contradictions.

**Scope:** all 5 books. Pass 1 corpus completion is a hard pre-req for this prompt (see Session 30 dependency note above). The earlier "AGOT-only v1, back-fill v2" carve-out is dropped.

---

## Files to create / modify

**New scripts:**
- `scripts/wiki-pass2-stage4-candidate-generator.py` — Step 2
- `scripts/wiki-pass2-stage4-promote.py` — Step 4
- `scripts/wiki-pass2-stage4-launcher.sh` (or extend `wiki-pass2.sh`) — Step 3 driver
- `scripts/wiki-pass2-stage4-validator.py` (or extend existing) — Step 4 byte-equality check
- `scripts/wiki-pass2-stage4-contradiction-prep.py` — AGOT contradiction-sweep input prep

**New agent prompts:**
- `.claude/agents/prose-edge-classifier.md` — fill out (currently stub)
- `.claude/agents/cross-identity-detector.md` — fill out (currently stub)
- Possibly: `.claude/agents/contradiction-surfacer.md` — new agent for AGOT contradiction sweep

**New artifact directories** (will be created by candidate generator):
- `working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/`
- `working/wiki/pass2-buckets/<bucket>/prose-edges/`
- `working/wiki/pass2-buckets/cross-identity-queue.jsonl`

**Existing files to leave UNTOUCHED:**
- `graph/nodes/*/` — until Step 4 (promotion)
- `working/wiki/pass2-buckets/<bucket>/skeleton/` — IMMUTABLE
- `working/wiki/pass2-buckets/<bucket>/prose/` — IMMUTABLE
- `reference/architecture.md` § "Edge Types" — locked vocabulary

---

## Recommended execution order for the next session

1. **Re-confirm scope with Matt** before starting. Confirm: AGOT-only contradiction sweep (Stage 4 v1), full-corpus prose-edge discovery, cross-identity escalation queue. Confirm cost projection.

2. **Step 1 re-run** — refresh cross-references index (`python3 scripts/wiki-pass2-build-cross-refs.py`). 30 sec.

3. **Inspect distribution** — read backlink-counts.json. Look at top 50 by in_count, bottom 50 by out_count. Sanity check.

4. **Build Step 2 candidate generator** — write the script. Test on one bucket first. Show Matt sample candidates.

5. **Build Step 3 agent prompt** — `.claude/agents/prose-edge-classifier.md` full prompt. Reference the locked vocabulary, source-prose file path, target-frontmatter shape.

6. **Pre-flight cost projection** — count survivors per bucket. Tier-A nodes only. Show Matt projected total before launch.

7. **Step 3 launch** — Matt confirms; run via launcher. 3-5 parallel tabs. Watch for rate limits + question-ID collisions (Stage 3a/b lessons).

8. **Mid-flight review** — peer-review a stratified sample of one bucket's output before continuing to all buckets.

9. **Step 4 promotion** — Matt confirms; run promote script. Validator confirms infobox edges unchanged.

10. **Cross-identity follow-on** — flagged candidates go through cross-identity-detector. Smaller batch.

11. **AGOT contradiction sweep** — separate sub-pipeline against AGOT extractions only.

12. **Acceptance criteria for Stage 4 v1 complete:**
    - All Tier-A nodes have prose-edge-candidates evaluated
    - All accepted prose-edges promoted to `## Edges (prose-derived)` subheadings
    - All cross-identity escalations resolved or queued
    - All contradiction findings surfaced to `curation/candidates.md`
    - Validator: 0 infobox edges modified, 0 vocabulary violations, 0 conflicts

13. **Write session-results file** (convention introduced Session 51 — see `working/session-results/README.md`). At end of session, write `working/session-results/<date>-stage4-prose-edge-classifier.md` with: status (complete/partial/blocked), headline numbers (candidates generated / classified / accepted / rejected / escalated, infobox-edges-touched = 0), what's next, notes. This is the watcher-handoff signal — write it *before* the worklog entry so any watching session sees the result land in real time. Also: also write a mid-session result file if Step 3 enters bulk-run mode (after smoke-test verdict) — watchers care about that transition.

---

## Open questions for Matt

1. **Tier-B nodes:** skip in v1 (their prose is thin), or include? Recommendation: skip in v1; revisit if Tier-A yield disappoints.
2. **Cross-identity inline vs follow-on:** during Step 3 or as Step 3.5? Recommendation: follow-on (lower volume, higher stakes, easier review).
3. ~~**Contradiction sweep scope:** strict AGOT-only for v1, or include AGOT + Pass 1 partial coverage of any other book?~~ **RESOLVED Session 30:** all 5 books — Pass 1 is being completed corpus-wide before this work track starts.
4. **Cost ceiling:** Stage 3 was $95 for 855 Stage-1 nodes. Stage 4 v1 estimate is $50-100 for full-corpus prose-edge discovery. Confirm budget OK before Step 3 launch.

---

## Reference

- Session 29 detail: `history/session-details/session-029.md`
- Stage 3 pipeline runbook: `working/runbooks/wiki-pass2-pipeline.md` (canonical reference for Stage 3 conventions Stage 4 should follow)
- Architecture (locked vocabulary): `reference/architecture.md` § "Edge Types"
- Cross-references index: `scripts/wiki-pass2-build-cross-refs.py` + outputs under `working/wiki/data/`
- Alias resolver: `scripts/wiki-pass2-build-alias-resolver.py` + `working/wiki/data/alias-resolver.json`
- Chronology data: `working/wiki/data/chronology-events.jsonl` (Session 29; 2,245 events, awaits v2 temporal-edge schema)
- Original Stage 4 design draft (Session 24): `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` (DELETE this file once Stage 4 v1 ships — it's superseded by this prompt)
- AGOT extractions: `extractions/mechanical/agot/agot-{pov}-{NN}.extraction.md` (73 files; only book complete)
- Schema-drift audit baseline: `working/audits/schema-drift-2026-05-02/execution/schema-drift-2026-05-02.md` (the audit Stage 4 must not break)

---

## Don'ts (process)

- **Don't run `/endsession` without explicit permission.** Historically violated.
- **Don't auto-launch agent runs without confirming each batch with Matt.** Each step gets confirmed separately.
- **Don't modify Python-emitted infobox edges.** Immutable. Prose-derived go under separate subheading.
- **Don't touch Stage-1 character nodes' prose body or existing `## Edges`** outside the carve-out (which permits READING for prose-edge generation, not modifying).
- **Don't expand the locked master vocabulary (~96 types)** without architecture.md FIRST → parser FIELD_EDGE_MAP if infobox-derived → re-run procedure. File `vocabulary-gap` questions to `questions-for-matt.jsonl` instead.
- **Don't promote prose-edges before validator passes.** The byte-equality check on existing `## Edges` is the safety gate.
- **Don't conflate Stage-1 (`v1`) with Stage-3 (`v1-python`) prompt versions.** They are different — the Stage-1 carve-out is specifically about agent-emitted prose, not deterministic Python emits.
- **Don't re-fetch the AWOIAF wiki.** The cache at `sources/wiki/_raw/` is canonical.
- **Don't promote video-game / TV-only entities.** They're already SKIP via category filters.
