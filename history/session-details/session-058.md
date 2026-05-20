---
session: 58
date: 2026-05-18 → 2026-05-19
title: Stage 4 Lockdown Completion — Vocab Round 2, Validator/Flagger/LINK, batch-0020 Audit Spawned
orchestrator_model: claude-opus-4-7
worker_models: [claude-sonnet-4-6, claude-opus-4-7]
---

# Session 58 — Stage 4 Lockdown Completion

## Frame

This session closed the Haiku-cutover lockdown surface. Started by executing the STEP 1.6 encode that Session 57 had specced. Mid-session, Matt's probing questions ("could you have recorded relationships on that same pass?", "sub qualifiers?", "did we miss anything?") surfaced two adjacent surfaces the count-driven Session-57 survey hadn't covered: vocabulary completeness and sub-qualifier dimensions. An audit pass was launched and verdicted; 10 new edge types adopted (vocab 149 → 159); zero sub-qualifiers adopted (audit confirmed the lockdown was right). Parallel-launched STEPS 2/3/4 landed clean. batch-0020 Opus audit spawned to a fresh iTerm2 window. Continue prompt for STEP 5 Haiku smoke written.

## What landed (chronological)

### Phase 1 — STEP 1.6 Encode (Sonnet 4.6, background)
Mechanical translation of Session 57's `working/qualifier-vocab/decisions.md` into runnable artifacts. Wrote `reference/edge-qualifier-vocab.md` (8 Tier-1 + 9 Tier-2 enum table). Added one cross-reference line to `reference/architecture.md` `## Edge Types` intro (15 tables left untouched per Option C). Updated `.claude/agents/prose-edge-classifier.md` — deleted `notes` field from emit_edge schema, added `qualifier` field with tier-dependent rules, added qualifier-lookup workflow step, added Pattern 4 prohibition. The worker caught a continue-prompt typo ("16 Tier-1 + Tier-2" vs actual 17 = 8+9) and deferred to decisions.md.

### Phase 2 — Matt's reframing questions
After STEP 1.6 verified clean, Matt prompted: *"could you have recorded the entity / node's relationships on that same pass?"* — the orchestrator had just described the Session 57 corpus survey as count-driven, and Matt's intuition was that the same scan could have harvested per-row records.

Orchestrator's initial answer: yes, propose a Pass-1 deterministic edge harvester. Matt pushed back: *"python might miss what the word means though if it doesn't, so we get these, but then does that lock in our edges?"* — surfaced the false-positive risk for regex-emitted edges.

Reframed: harvester architecture should NOT lock edges. **Step A** (markdown-parse Pass 1 tables to JSONL) + **Step B** (Haiku closed-vocab classify each row) + **Step C** (Opus stratified sample audit, diagnostic not gate). Matt then asked *"Doesn't it seem like Step A should just be subsumed into Step B?"* — orchestrator agreed Step A is trivial 30-line parsing prep, not semantic work; the actual classification happens in Step B's closed-vocab Haiku pass.

**Decision:** Harvester deferred — not built this session. Architecture settled. Will revisit AFTER Haiku smoke verdict; if Haiku is viable, the harvester becomes attractive as a gentler closed-vocab task.

### Phase 3 — STEPS 2/3/4 parallel launch (Sonnet 4.6 × 3, background)

**STEP 2 — `[LINK]` substitution sub:** Investigation found 351 `[LINK]` tokens in completed-batch evidence_snippets (control arm, preserved) + 121,310 `[LINK]` tokens in 4,744 queued candidate files. Architecture chosen: post-processing script `scripts/stage4-resolve-link-placeholders.py` (plan/apply/idempotent) + inline patch to `scripts/wiki-pass2-build-edge-candidates.py` for future generations. Substitution marker: `[LINK]` → `«anchor_text»` (angle quotes to avoid collision with `[text](wiki:Page)` links).

**STEP 3 — Validator extension:** Three new check classes added to `scripts/wiki-pass2-validate-edge-jsonl.py`: (1) type contracts (22 edge-type → target-type constraints, slug resolution via 8,050-node `build_node_type_index()`), (2) qualifier enums (Tier-1/Tier-2/Tier-3 enforcement per `reference/edge-qualifier-vocab.md`), (3) notes-rejection (any decision type). Self-test on 21 Sonnet control-arm batches: **2,528 new violations** surfaced (1,757 tier-3 qualifier emission, 380 not-in-enum, 193 notes, 149 missing required, 49 type-contract). Old 9-violation costayne subset still caught unchanged — no regression.

**STEP 4 — Suspicious-edges flagger:** Built/extended `scripts/wiki-pass2-flag-suspicious-edges.py` with 6 pattern classes: `knows_as_fallback`, `attends_non_event`, `fights_in_non_event`, `killed_by_non_person`, `tier3_weak_evidence`, `contemporary_with_char_pair`. Full run across 72 done batches / 4,075 emits: **288 flagged (7.1%)**. Dominant pattern: **KNOWS-as-fallback at 82.3% of all KNOWS emits** (163 flags; 140 from batch-0020 alone — Frey-cluster co-presence trap). Session 54's "~37%" was understated. Output: `working/wiki/data/stage4-suspicious-edges.jsonl`.

### Phase 4 — Vocab completeness audit (Opus 4.7, background)

Matt: *"i don't want to harvest pass 1, I want to look for any missing edge vocabulary, and sub qualifier. I wanted to lock in sub qualifiers. did we miss anything?"*

Honest framing of the orchestrator's prior position: when it said "no sub-qualifier layer; the enum value IS the leaf," it described the schema as-built, not as audited. Session 57's survey was count-driven, not coverage-driven. Audit launched.

**Audit inputs:** 4,805 distinct relationship phrases (Session 57 survey count), 7,398 P1 rows from 344 files, 4,207 Stage-4 emits across 21 Sonnet batches (Sonnet was using `qualifier` as a freeform description string at 53% — rich latent enumeration signal), 4,786 wiki infobox records × 25 fields, plus 135 `no-fitting-type-vocab-locked` rejections from Session 56's gap-closure.

**Audit verdicts:**
- **Sub-qualifiers: 0 adopt.** Every candidate floated (`SWORN_TO=former by_X`, `HOLDS_TITLE=former by_X`, `SPOUSE_OF=widowed by_cause`, etc.) audited as either zero-corpus-signal OR already-captured-elsewhere via separate edges. The lockdown was right: enum value IS the leaf.
- **Edge vocab gaps: 8 STRONG ADOPT** (resolved to 10 new types because two adopts were paired edges): `SPIES_ON` + `INFORMS`, `NAMED_AFTER`, `STEP_PARENT_OF` + `STEP_CHILD_OF`, `IN_LAW_OF` (Tier-2 with `{by_marriage_of_self, by_marriage_of_child, by_marriage_of_sibling, by_marriage_of_parent, unknown}`), `RESCUES`, `BANISHES`, `TORTURES`, `CONSPIRES_WITH`.
- **8 MEDIUM ADOPT → DEFER all** (THREATENS, ACCUSES, BLAMES, SUMMONS, FREES/PARDONS, HAUNTED_BY, REWARDS, ESTRANGED_FROM — all have ≥1 existing edge covering most of the semantic).
- **11 REJECT** (LEGITIMIZES, DISINHERITS, BULLIES, BLESSES, FAVORS, RIDES, INTERROGATES, WITNESSES, MAINTAINS, REACTS_TO_EVENT, REQUESTS_SONG/PERFORMS_AT).
- **3 borderlines:** SHADOWBINDS deferred, SOLD_TO deferred (covered by CONTRACTED_WITH=slavery or BETRAYS), MADE_OF a prompt-clarity issue not vocab gap.

**Audit deliverable:** `working/qualifier-vocab/audit-completeness-2026-05-19.md` (229 lines, 3 sections + recommendations + followups).

### Phase 5 — STEP 1.7 Vocab Round 2 encode (Sonnet 4.6, background)

Mechanical translation of audit verdicts. 10 new rows added to `reference/architecture.md` across 6 subsections:
- Kinship & Family: `STEP_PARENT_OF`, `STEP_CHILD_OF`, `IN_LAW_OF`
- Political & Authority: `BANISHES`
- Factional & Diplomatic: `CONSPIRES_WITH`
- Military & Conflict: `RESCUES`, `TORTURES`
- Knowledge & Information: `SPIES_ON`, `INFORMS`
- Cultural & Religious: `NAMED_AFTER` (worker's judgment call — Westeros dynastic name-recycling is cultural transmission, not identity/disguise)

`reference/edge-qualifier-vocab.md` gained `IN_LAW_OF` as 10th Tier-2 row. Count-check line bumped: Tier 1 (8) + Tier 2 (10) + Tier 3 (~141) = ~159 total.

`.claude/agents/prose-edge-classifier.md` vocab-count references bumped in 5 places (149 → 159). Reverse-direction section extended: `STEP_PARENT_OF` / `STEP_CHILD_OF` as one-sided pair; `IN_LAW_OF` and `CONSPIRES_WITH` as symmetric.

`working/qualifier-vocab/decisions.md` got a new `## Round 2` section appended (Round 1 content untouched per append-only rule). Round 1 count-check line 107 still reads "149 ✓".

### Phase 6 — batch-0020 Opus audit spawned (fresh iTerm2, Opus 4.7)

Continue prompt at `progress/continue-prompts/2026-05-19-batch-0020-opus-audit.md`. Spawned via osascript to fresh iTerm2 window. Output destinations: `working/session-results/2026-05-19-batch-0020-opus-audit.md` (audit doc) + `…-audit-stdout.log` (tee'd transcript fallback). Audit was still running at session close. Verdict will gate STEP 5 Haiku smoke (either "ready" → fire smoke, or "needs prompt change first" → encode change then fire).

### Phase 7 — STEP 5 continue prompt
`progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md` written. Two-branch logic at the top: read audit verdict first; if ready proceed to methodology, if prereq apply then proceed. Methodology covers smoke target selection (batch-0020 recommended), validator + flagger application to Haiku output, semantic diff vs. Sonnet control arm + Opus audit ground truth, verdict structure.

## Decisions

- **Vocab is FINAL at 159 types / 18 enumerable** (8 Tier-1 + 10 Tier-2 + ~141 Tier-3). No further additions expected for Stage 4 v1.
- **Sub-qualifier dimension: not adopted.** Audit verdict: enum value IS the leaf; the corpus does not justify a second axis.
- **Pass-1 deterministic harvester: deferred.** Architecture settled (markdown-parse + Haiku closed-vocab classify + Opus stratified audit). Revisit AFTER Haiku smoke verdict.
- **batch-0020 = canonical smoke target.** It's the hot zone (153/437 flagged, 35% flag rate) and the most informative cross-model diff once the Opus audit lands as ground truth.
- **Haiku smoke launch via watcher pattern** (Matt's call): watcher = Opus 4.7 read-only synthesis; worker = Haiku 4.5 doing classification; verdict-gating mandatory per drift-detection rule.
- **Entity-page enrichment via extractions** — Matt surfaced as future work; explicitly deferred to after this pass (smoke verdict + Stage 4 bulk Haiku decision).

## Cumulative cost / count

Background subagents this session:
- STEP 1.6 encode (Sonnet 4.6) — ~?
- STEPS 2/3/4 parallel (Sonnet 4.6 × 3) — ~?
- Vocab completeness audit (Opus 4.7) — ~$5-15 estimated
- STEP 1.7 Round 2 encode (Sonnet 4.6) — ~?
- batch-0020 audit (Opus 4.7, iTerm2 separate process) — ~$10-25 estimated, still running

Orchestrator (Opus 4.7 in this session): ~89.8k / 1M context at session close.

## What's next

Three queued tracks:

1. **Verify batch-0020 audit completion** (separate iTerm2 process; verify before next session).
2. **STEP 5 Haiku smoke fire** (next session, watcher + worker pattern). Continue prompt: `progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md`.
3. **After smoke verdict:** decide on Pass-1 deterministic harvester + Stage 4 bulk Haiku resume + entity-page enrichment.

## Files created/modified

**New:**
- `reference/edge-qualifier-vocab.md` (Session 58 morning)
- `working/qualifier-vocab/audit-completeness-2026-05-19.md` (audit deliverable)
- `scripts/stage4-resolve-link-placeholders.py`
- `working/wiki/data/stage4-suspicious-edges.jsonl` (288 rows)
- `progress/continue-prompts/2026-05-19-batch-0020-opus-audit.md`
- `progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md`
- 6 session-results docs under `working/session-results/`
- 4,744 queued candidate files rewritten (`[LINK]` → `«anchor»` — 121,310 substitutions)

**Modified:**
- `reference/architecture.md` (cross-ref line + 10 new edge type rows + vocab callout 149 → 159)
- `.claude/agents/prose-edge-classifier.md` (notes deleted; qualifier field added; 5 vocab-count refs bumped; reverse-direction list extended)
- `scripts/wiki-pass2-build-edge-candidates.py` (inline `[LINK]` sub patch)
- `scripts/wiki-pass2-validate-edge-jsonl.py` (3 new check classes)
- `scripts/wiki-pass2-flag-suspicious-edges.py` (6 pattern classes)
- `working/qualifier-vocab/decisions.md` (Round 2 section appended)
- `working/todos.md` (STEPS 1.6 / 1.7 / 2 / 3 / 4 marked done; STEP 5 status updated)

**Deleted:**
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` (STEP 1.6 completed)
- `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` (superseded by smoke-fire continue prompt)
