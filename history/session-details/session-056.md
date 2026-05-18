---
session: 56
date: 2026-05-18
model: Opus 4.7
shape: apply + planning (mixed)
parent: session-055 (vocab-lock decisions)
---

# Session 56 — Stage 4 Vocab Apply + Qualifier Vocab Lock-Down Planned

## Goal at start

Execute the apply phase of Session 55's locked vocab decisions: 17 new edge types into `reference/architecture.md`, classifier prompt switched to "vocab FINAL," 68 questions-for-matt.jsonl rows closed, Haiku smoke-test spec written for already-completed batches.

## What actually happened

The apply work landed cleanly, but mid-session Matt caught a drift pattern that re-scoped the back half of the session: the agent (me) had been extrapolating "note X in `notes`" guidance from the Session-55-locked `MANIPULATES` decision into three additional new-type rows. Matt's flag: "I thought sub qualifier for edges were gonna be tighter, not just 'notes'? Will the agent start creating a lot of those?" — and from there the conversation pivoted into a deeper design question: how do you constrain the prose-edge-classifier from freestyling on the qualifier surface the way it had been about to freestyle on the type surface before Session 55 locked the vocab?

That conversation produced a new track: **HAIKU-CUTOVER STEP 1.5 — Qualifier vocab lock-down**, with a three-tier framing locked, a plan written, and a continue prompt for the next session. Haiku smoke (STEP 5) deferred until the qualifier surface is also locked.

## Phase 1 — Architecture.md applies (17 new edge types)

Sequential Edit calls into `reference/architecture.md`. All 17 types placed in the subsections agreed in Session 55:

- **Kinship & Family**: `COURTS`, `PROPOSED_AS_BRIDE`
- **Factional & Diplomatic**: `CONTRACTED_WITH`
- **Military & Conflict**: `ATTACKS`, `ASSAULTS`, `PARTICIPATES_IN`
- **Knowledge & Information** (next to `HEALS`): `AFFLICTED_BY`, `DIED_OF`
- **Emotional & Perceptual**: `COMPANION_OF`, `REPUTED_AS`
- **Possession & Ownership**: `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`
- **Magic & Supernatural**: `PRACTICES`
- **Cultural & Religious**: `OFFICIATES`
- **Hospitality & Custom**: `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`

Plus the 2 description modifications:
- `FIGHTS_IN` → extended to "battle, war, or tournament as a combatant"
- `MANIPULATES` → mechanism-note added ("via bribe", "via flattery", etc.)

Plus the master-vocab callout: 132 → 149, Session-55-second-wave historical note appended, gap-filing default rewritten from "file vocabulary-gap question" to "vocab FINAL; reject as `no-fitting-type-vocab-locked`."

## Phase 2 — The "notes" drift catch

When writing the `CONTRACTED_WITH`, `ASSAULTS`, and `PROPOSED_AS_BRIDE` rows, the agent (me) appended sentences like "Note the contracted service in `notes`," "Note victim agency / context in `notes` when meaningful," "Proposer → Proposed bride (note recipient in qualifier)."

Matt halted: "I thought sub qualifier for edges were gonna be tighter, not just 'notes'? Will the agent start creating a lot of those?"

The catch was sharp and exactly right. Going back to Session 55 Phase 5/6, only `MANIPULATES` had a locked qualifier-mechanism decision. The other three were extrapolations the agent made while writing — soft expectations layered on top of a locked enum vocabulary. If every new-type row says "note X in `notes`," the classifier ends up producing inconsistent freeform notes for hundreds of edge types, with no query surface and no way to enforce the lock mechanically.

**Reverted the three drifted additions** (kept MANIPULATES, which was locked).

## Phase 3 — The bigger conversation

Matt then named the real architectural concern: "we need to be locked in, so the edge prose analyzer cannot improvise." He proposed using everything we already have — Pass 1 corpus (all 5 books, 344 chapters), wiki cache + infoboxes, the 21 already-completed Sonnet batches' actual notes-content, ASOIAF series knowledge — to lock the qualifier vocabulary before any long prose-analysis pass runs.

The general rule that emerged:

> Before any long-running agent prose-analysis pass (~20+ min, no Python in the loop), invest aggressively in upfront lockdown using every existing output. The default failure mode has been launching passes with too much agent freedom and too little leverage on data we've already paid for. Reduce freestyle surface BEFORE the run, not during.

This is now a project memory at `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_lockdown_before_long_passes.md`. Companion to `feedback_drift_detection_mandatory.md`. MEMORY.md index updated.

## Phase 4 — Three-tier qualifier framing locked

Matt agreed to the three-tier proposal:

| Tier | Behavior | Validator |
|---|---|---|
| **Tier 1 — REQUIRED enum** | Edge MUST emit a `qualifier` field from a small closed set (e.g., `SIBLING_OF ∈ {full, half, step, milk}`) | Rejects edges missing or out-of-enum |
| **Tier 2 — OPTIONAL enum** | `qualifier` may be null; if emitted, must match the enum | Rejects out-of-enum |
| **Tier 3 — no enum** | No `qualifier` field; `notes` is freeform, explicitly non-queryable | None |

The implementation work is genuinely its own session — 149 edge types to verdict, corpus distributions to query, encoding strategy to choose, validator extension to design.

## Phase 5 — Format-of-artifact discussion

Matt pushed back on my framing of "design doc": "What do you mean by design doc? is that something you use? because I am looking at agent fleet specs and that's so much to read for me lol."

Honest answer: I park decision artifacts in `working/agent-fleet-specs/` because that's where the Session-55 vocab-lock doc lives, but the folder has bloated into a directory that's painful to scan. Lighter approach for the qualifier work: small new folder `working/qualifier-vocab/`, with a 1-screen scannable `plan.md` (this session) and a tabular `decisions.md` (next session). No narrative; verdict-per-row format like the Session-55 decision doc.

## Phase 6 — Background-agent parallelism

After scope confirmation, Matt stepped away and I dispatched the back half in parallel:

- **`general-purpose` (background)**: updated `.claude/agents/prose-edge-classifier.md` — vocab-FINAL flip + 5 `~149` references + 17 new types in category list + reverse-direction section extended (both-sided list adds KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON + NURSED_BY/WET_NURSE_OF; one-sided list adds 6 common-mistake reverses).
- **`script-builder` (background, then handed back, then re-dispatched as general-purpose)**: wrote `scripts/stage4-close-vocab-gaps.py`, surfaced 3 uncovered types + 4 edge-case questions, received dispositions from orchestrator (derivable from Session-54/55 framework — no new vocab invented), then ran the script.

## Phase 7 — Three new uncovered types resolved during apply

The gap-close agent flagged three proposed types not covered by the Session-55 decision map. All resolved without inventing new vocab:

- `COMPETES_IN` (tournament participation) → **rejected**; duplicate of post-Session-55 `FIGHTS_IN` (now covers "tournament as a combatant").
- `SOLD_TO` → **rejected**; reverse-direction of `PURCHASED_FROM`, one-sided per Session-55 reverse-direction discipline.
- `TRANSACTS_WITH` → **rejected**; too-generic, use `PURCHASED_FROM`.
- `SLAIN_BY_WEAPON` / `KILLED_WIELDING` → **resolved-pre-adopted** under Session-54 `KILLED_WITH` (architecture.md row 217 covers "slain by Orphan-Maker" pattern exactly).

## Phase 8 — Agent judgment on row 68

The gap-close agent caught a subtle mis-classification: row 68 was filed by an earlier classifier as `ASSAULTS` but the underlying evidence (Mandon Moore slashing Tyrion on the Blackwater; beating Sansa on Joffrey's orders) is non-sexual physical violence. Per Session-55's ATTACKS-vs-ASSAULTS scope split (ASSAULTS = sexual violence specifically; ATTACKS = generic physical), correct resolution is `accepted-as-ATTACKS`, not `accepted-as-ASSAULTS`. Resolution text records both the filing and the redirect rationale.

This is exactly the kind of audit pattern the suspicious-edges flagger (HAIKU-CUTOVER STEP 4) will produce post-emit.

## Phase 9 — Gap-close final numbers

- 63 rows newly closed with `resolved_at` + `resolution` fields.
- 5 rows pre-resolved from earlier sessions (22/23/27) — agent correctly skipped them (idempotency).
- 0 unresolved remaining.
- JSONL atomic-rewrite verified (68 valid lines).
- Disposition tally: 17 accept, 12 stale-resolved (already-canonical at filing time), 9 reverse-direction rejects, 6 too-generic/derivable/too-narrow rejects, ~6 not-vocab-decisions (infrastructure / cross-identity / parser-bug / reclassification rows).

## Phase 10 — One contradiction caught + fixed

The dispatched classifier-prompt agent reported a contradiction it left in place per its scope constraint: lines 173-174 of the classifier prompt's CONTEMPORARY_WITH STOP-block still said "Optionally file a `vocabulary-gap` question" — which contradicts the FINAL lock at lines 241-243. Orchestrator fixed in-place: now points at `no-fitting-type-vocab-locked` and the in-prompt example bullets updated to reflect the Session-55 accepted types (e.g., "Cersei presented to Robb Stark" → now correctly maps to `PROPOSED_AS_BRIDE`, not "file gap for OFFERED_AS_BRIDE").

## Files written / changed

- `reference/architecture.md` — 17 new edge-type rows + 2 description mods + vocab-callout bump (132 → 149) + Session-55-second-wave historical note + gap-filing default rewritten.
- `.claude/agents/prose-edge-classifier.md` — vocab FINAL; 5 ~149 references; 17 new types in category list; reverse-direction section extended; CONTEMPORARY_WITH STOP-block fixed.
- `scripts/stage4-close-vocab-gaps.py` — NEW; ran successfully; 63 rows closed in `working/wiki/pass2-buckets/questions-for-matt.jsonl`.
- `working/wiki/pass2-buckets/questions-for-matt.jsonl` — atomic in-place rewrite; 68 valid JSONL lines preserved.
- `working/qualifier-vocab/plan.md` — NEW; 1-screen scannable plan for the qualifier-lock session.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` — NEW continue prompt.
- `working/todos.md` — HAIKU-CUTOVER STEP 1 marked done; new STEP 1.5 inserted between STEP 1 and STEP 2; STEP 5 (Haiku smoke) flagged BLOCKED on STEP 1.5; STEP 3 (validator) notes folded qualifier-enum enforcement.
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_lockdown_before_long_passes.md` — NEW memory.
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/MEMORY.md` — index updated.
- `working/session-results/2026-05-18-stage4-vocab-applied-and-smoke-prepped.md` — NEW (session-results convention).
- `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` — DELETED (this session's continue prompt, completed).

## Decisions locked this session

1. **Three-tier qualifier framing.** Tier 1 (required enum), Tier 2 (optional enum), Tier 3 (no enum / freeform `notes` non-queryable). The qualifier surface IS a freestyle surface and will be locked before any long pass runs.
2. **Haiku smoke (STEP 5) deferred until STEP 1.5 lands.** Justification: Haiku drifts more than Sonnet; locking every freestyle surface is the actual lever for making Haiku viable.
3. **Lockdown-before-long-passes as a project rule.** Memory written.
4. **`working/qualifier-vocab/` as the artifact home** for this track — separate from `agent-fleet-specs/` to keep the readable surface lighter.
5. **COMPETES_IN / SOLD_TO / TRANSACTS_WITH all rejected** without new-vocab; resolvable from Session-54/55 framework alone.
6. **SLAIN_BY_WEAPON / KILLED_WIELDING resolved-pre-adopted** under Session-54 KILLED_WITH.
7. **Row 68 mis-classification redirected** (ASSAULTS filed → ATTACKS correct per Session-55 scope split). No prior session decision required.

## What worked

- **Parallel background-agent dispatch** for the mechanical pieces (classifier prompt + gap-close script) while the orchestrator continued the architecture.md edits in series. ~3 deliverables in flight at once.
- **Reading the dispatch agents' completion reports critically.** The classifier-prompt agent flagged the lines-173-174 contradiction it had left per scope; orchestrator fixed in-place. The gap-close agent flagged 3 uncovered types + 4 edge cases and waited for dispositions rather than inventing; orchestrator returned answers derivable from Session-54/55 framework.
- **Matt's drift-catch on "note in notes" extrapolation.** Without that catch, the qualifier surface would have leaked into architecture.md as informal English instructions, exactly the failure mode the agent-lockdown discipline is meant to prevent.

## What didn't

- **The agent's first-instinct extrapolation pattern.** Writing "note X in `notes`" after the locked-MANIPULATES-mechanism-note row was the agent applying a heuristic the human hadn't authorized. Pattern to watch: when one locked decision establishes a phrasing, the agent should NOT propagate that phrasing to adjacent decisions without explicit authorization.

## Open questions surfaced for next session

1. **Backfill strategy for the 21 already-emitted batches?** Their `notes` fields are freeform. Three options in `plan.md`: (a) leave-as-freeform-legacy, (b) post-hoc normalizer, (c) re-classify on Haiku.
2. **Tier-3 `notes` discipline.** Cap at 100 chars? Required as non-queryable? Pure freeform?
3. **Symmetric-edge qualifier semantics.** SIBLING_OF half-brother — both endpoints share the qualifier? (Lean: yes.)
4. **Combine type-contract column with qualifier column** in a single architecture.md change?

## What's next

→ continue: `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` (Opus 4.7).

Produces `working/qualifier-vocab/decisions.md` — per-edge-type qualifier verdicts using Pass 1 corpus + wiki infoboxes + 21 completed batches + series knowledge. Three-tier framing already locked.

After: STEP 1.6 (encode into architecture.md + classifier prompt), STEP 2 ([LINK] sub), STEP 3 (validator — type contracts + qualifier enums folded), STEP 4 (suspicious-edges flagger), THEN STEP 5 (Haiku smoke).

Per Matt's standing rule, `/endsession` was explicitly authorized this session — not auto-triggered.
