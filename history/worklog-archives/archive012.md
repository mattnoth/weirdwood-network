# Worklog Archive 012

> Sessions 53 (and forward up to 5). Archived from main worklog per CLAUDE.md rule #8 (Session Log holds at most 5 entries).

---

### Session 53 — Stage 4 1-Tab Smoke + Throttle Calibration (2026-05-15)

**Detail:** `history/session-details/session-053.md`

**Changes made:**
- `scripts/stage4.sh` — three edits: (1) added `STAGE4_SLEEP_BETWEEN` env var (default 5400s/90 min) replacing prior 30s inter-batch sleep; (2) fixed `set -e` + `pipefail` bug that was silently terminating the worker on non-zero claude exits (the explicit error-handling block was dead code) — pipeline now wrapped in `set +e` / `set -e`; (3) ported rate-limit detection from `extract.sh` — checks tmp_json for `"status":"rejected"` + `"rateLimitType"`, writes `rate-limit-events.jsonl` + `next-eligible.txt`, breaks cleanly. Status command updated to surface rate-limit events + next-eligible countdown. Help text documents the new env var.
- 6 stale lock files cleaned across two waves (initial 4 + post-2-tab smoke 2).

**Decisions:** Multi-tab parallelism dropped — Max 5h cap saturates faster than wall-clock benefit (2 tabs hit wall ~60 min; 6 tabs ~30 min). 1-tab + 90-min throttle is the working config. Detection blind spot uncovered: Max-plan session walls appear as plain-text `"You've hit your org's monthly usage limit"`, not as stream-json `rate_limit_event` — current grep doesn't catch them. Filed as future polish (extend grep patterns). Empirical surprise: batch-0012 ran at $3.42 / 23.8 min / 1.3M cache_read — **16x lower cache_read** than multi-tab batches, projected 5-7 batches per 5h window with ~50% headroom for Matt's other Claude use. Hypothesis: 1-tab serial keeps Anthropic's prompt cache warm; multi-tab fragments it.

**Mission state at session end:** 12/201 batches done, $50.09 cumulative, 0 stuck, 189 queued. Final worker is in 90-min sleep with `/tmp/stage4-stop` set — will exit cleanly on wake.

**What's next:**
- **Spot-check batch-0012 quality + Haiku comparison** (NEXT). → continue: `progress/continue-prompts/2026-05-15-stage4-batch-quality-check.md` (**Opus 4.7** — cross-model audit; auditing Sonnet output with Sonnet misses Sonnet-systematic biases; verdict gates ~$700 of bulk-run downstream). Verdict gates bulk resumption.
- **Resume bulk run** after quality check passes — `weirwood stage4 1` (90-min throttle); stop file auto-clears on launch.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 54 — Stage 4 Schema Lockdown + 21-Batch Bulk Run (2026-05-15 → 2026-05-16)

**Detail:** `history/session-details/session-054.md`

**Changes made:**
- `.claude/agents/prose-edge-classifier.md` — major patches: added `## Output Contract → Required fields per decision` table (mechanically validated), `evidence_kind` discriminator field on every emit_edge (`wiki-entity` / `wiki-chapter-summary` / `book-pass1`), `pass1_relationship` candidate-shape documentation (was wired in candidate generator but undocumented in prompt), `## Common failure patterns` top-level section with 3 concrete from-the-data examples (CONTEMPORARY_WITH-fallback / FIGHTS_IN-with-person / ATTENDS-with-person), `Reverse-direction edges` rule (PARENT_OF/GUEST_OF/RESURRECTS/TUTORS/WIELDS/OWNS/FORGED_BY are one-sided; KILLS/UNCLO_OF/WARD_OF are both-sided).
- `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` — validator-runs-before-marking-done step + `Two failure modes to avoid` section.
- `reference/architecture.md` — 11 new edge types across two passes: Session-54 added UNCLE_OF, NEPHEW_OF, KILLED_WITH, ATTENDS; Session-55 added COUSIN_OF, MILK_BROTHER_OF, NURSED_BY, WET_NURSE_OF, KNIGHTED_BY, BESTOWS_KNIGHTHOOD_ON, DEPICTED_IN. Vocab now ~132 types across 15 subsections.
- `scripts/wiki-pass2-validate-edge-jsonl.py` — NEW. Mechanical validator. Loads architecture.md vocab via regex (127 types found), checks per-decision required fields, checks shape rules (`confidence_tier` int 1-3, `evidence_snippet` verbatim ≥10 chars not section-header, `evidence_kind` matches `candidate_kind`, edge_type in canonical vocab). Self-tested against archived broken batch-0012 (caught 14/14 violations).
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_drift_detection_mandatory.md` — NEW memory rule. Every bulk LLM run includes mechanical validator + cross-model audit + verdict-gates-resumption, regardless of model.
- 6 session-results docs written: `2026-05-15-stage4-batch-0012-quality-check.md`, `2026-05-15-stage4-edge-provenance-explained.md`, `2026-05-15-stage4-haiku-smoke-verdict.md`, `2026-05-16-stage4-bulk-run-checkpoint.md`, `2026-05-16-stage4-current-status-and-open-questions.md`, `history/session-details/session-054.md`.
- 21 Sonnet batches completed (batch-0012 canonical re-run through batch-0021). Manifest: 12 → 21 done. ~600+ prose-edges JSONL files written under `working/wiki/pass2-buckets/<bucket>/prose-edges/`.
- 2 failed batch-0012 attempts archived for the comparison record: `_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/` (schema-broken Sonnet) and `_archive/batch-0012-haiku-failed-2026-05-15/` (Haiku semantic failure).

**Decisions:** Haiku 4.5 rejected for prose-edge classification (smoke test: validator-clean but ~80% semantic failure — SERVES-on-everything, KILLED_BY reversal, type-contract violations wholesale). Sonnet stays the bulk worker. Schema drift is a property of LLM-structured-output, not of any model — defense is mechanical validator + cross-model audit, not stronger prompts alone. **The durable answer to "schema lockdown" is to lock the audit, not the prompt** — build a suspicious-edges worklist (KNOWS without explicit "knew" language, ATTENDS-non-event, FIGHTS_IN-non-event, KILLED_BY-non-person, tier-3, CONTEMPORARY_WITH-on-character-pair) for later Opus review. Soft-fallback whack-a-mole pattern: patched CONTEMPORARY_WITH (Session 55 mid-stream), KNOWS-as-fallback emerged in batch-0020 (~37% of emits). Accept the 5-7% baseline; post-clean via the worklist. Sequential single-terminal bulk firing is safer than parallel (rate-limit failures cleaner, no stale-lock cascades).

**Mission state at session end:** 21/201 batches done, ~$37 cumulative spend, 180 queued. Stop file removed; locks dir empty. Worker not running.

**What's next:**
- **Resume Stage 4 bulk in one terminal** → continue: `progress/continue-prompts/2026-05-16-stage4-bulk-resume.md` (**Sonnet 4.6** workers via `/loop 20m /worker-stage4`). 180 batches × ~$3.42 ≈ $615 remaining.
- **BEFORE resuming if possible**: extend `scripts/wiki-pass2-validate-edge-jsonl.py` with the suspicious-edges flagging logic (Matt's idea) — flag schema-clean-but-semantically-suspicious patterns to `working/wiki/data/stage4-suspicious-edges.jsonl` for later Opus review. See continue prompt Step 4.
- **Vocab gaps pending review:** CROWNS_QUEEN_OF_LOVE_AND_BEAUTY (recommend reject); OFFERED_AS_BRIDE / CONSPIRES_WITH / HOSTAGE_OF may surface again at scale.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 55 — Stage 4 Vocab Lock Decisions + Pass 1 Staleness Incident (2026-05-18)

**Detail:** `history/session-details/session-055.md`

**Changes made:**
- `scripts/stage4-vocab-gap-analysis.py` — NEW. Normalizer for the 16-distinct-schema `questions-for-matt.jsonl` (68 rows). Outputs `working/agent-fleet-specs/stage4-vocab-gaps-{normalized.jsonl,rollup.md}` — 10 stale-resolved, 37 truly open, 7 untyped.
- `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md` — NEW. Decision doc bucketed A (12 stale rows close) / B (5 accepts) / C (9 rejects: reverse-direction + too-generic) / D (22 borderline → Matt's call). Updated through D verdicts with second-opinion-agent overrides.
- `working/todos.md` — added "Stage 4 — Haiku Cutover Prep" section with 5 numbered steps (vocab lock / `[LINK]` substitution / validator extension / suspicious-edges worklist / Haiku smoke).
- 4 staleness fixes applied via dispatched agent: `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/{project_pass1_prompt_v3_canonical.md,MEMORY.md,memory_staleness_policy.md (NEW)}` + `CLAUDE.md` (pipeline table row 4 → "✅ Done"; Orchestration Rule 9 added — worklog wins over continue-prompts when they conflict) + `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` ("Status from memory" passage corrected).
- `history/session-details/session-055.md` — NEW (full narrative).
- `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` — NEW (Shape B handoff for apply phase).

**Decisions:** 17 new edge types approved (vocab 132 → 149): `AFFLICTED_BY`, `DIED_OF`, `COMPANION_OF`, `PARTICIPATES_IN`, `OFFICIATES`, `ATTACKS`, `ASSAULTS`, `COURTS`, `CONTRACTED_WITH`, `PROPOSED_AS_BRIDE`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`, `PRACTICES`, `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`, `REPUTED_AS`. Plus 2 description mods: `FIGHTS_IN` (add "or tournament"), `MANIPULATES` (qualifier-mechanism note). Rejected: 9 reverse-direction violations (Bucket C), 5 generic/derivable (NAMED_AFTER, extended kinship, BRIBES standalone, USES_AS_SIGIL). **ATTACKS scoped as generic person→person OR creature→person physical violence; ASSAULTS specifically for sexual violence** (Matt's call). **CREW_OF locked at end of session as sibling to CAPTAIN_OF (Path B); both target `object.artifact` vessel.** Subsection placement locked: AFFLICTED_BY/DIED_OF → Knowledge & Information (next to HEALS); CAPTAIN_OF → Possession & Ownership. **Decisions are NOT yet applied** to architecture.md or the classifier prompt — apply work is the next session.

**Incident — stale Pass 1 belief:** Mid-session, orchestrator believed "ACOK/ASOS/ADWD Pass 1 incomplete" based on a 13-day-old memory file + the session's launching continue prompt's "Status from memory" passage. Ground truth: all 5 books complete (344/344) since 2026-05-06. Matt halted, dispatched root-cause investigator. Three stale sources fixed + one new memory rule (`memory_staleness_policy.md`) + CLAUDE.md Rule 9 added: trust worklog over continue prompts when they conflict on state.

**What's next:**
- **Apply the vocab lock + prepare Haiku smoke-test spec for already-done batches.** → continue: `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` (**Opus 4.7** — mechanical apply work + smoke-test architecture). Smoke-test candidate batches identified: 0066 (wyman-manderly, 168 cands), 0068 (bowen-marsh), 0072 (taena/hallis multi-page), 0001 (early-batch mix).
- Then HAIKU-CUTOVER STEPS 2/3/4 ([LINK] sub / validator type contracts / suspicious-edges flagger) — Matt's call whether they happen before the smoke fires or alongside.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 57 — Stage 4 Qualifier Vocab Lock-Down (2026-05-18)

**Detail:** `history/session-details/session-057.md`

**Changes made:**
- `working/qualifier-vocab/decisions.md` — NEW. Full verdict matrix: 17 enumerable types (8 Tier-1 REQUIRED + 9 Tier-2 OPTIONAL) + 132 Tier-3 (no qualifier, no notes). Open questions Q1–Q5 answered. Schema implications for STEP 1.6 + STEP 3 documented.
- `working/session-results/2026-05-18-stage4-qualifier-vocab-locked.md` — NEW.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` — NEW. Self-contained STEP 1.6 handoff with all 17 enums verbatim.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` — DELETED (this session's launching continue prompt, completed).
- `working/todos.md` — HAIKU-CUTOVER STEP 1.5 marked [x] (17 enums verdicted; notes field deletion decided); new STEP 1.6 (encode) inserted; STEP 3 updated to reference the new vocab file and `notes`-rejection.
- `history/session-details/session-057.md` — NEW.
- `history/worklog-archives/archive011.md` — Session 52 archived; archive011 now full at 5 entries.

**Decisions:** **Tier-1 (8):** SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO — REQUIRED enum from closed set. **Tier-2 (9):** BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH, DECEIVES, REVEALS_TO, ATTACKS, KNOWS, GUEST_OF — OPTIONAL enum. **Tier-3 (132):** all others — NO qualifier, NO notes. **`notes` field DELETED ENTIRELY from edge schema across all tiers** (Matt's "zero freeform" call — notes was the open drift surface qualifier-vocab is meant to close). **Encoding strategy: Option C** (new file `reference/edge-qualifier-vocab.md`; architecture.md tables untouched) — decided by fresh-context agent to avoid orchestrator bias. **21 already-emitted Sonnet batches preserved as freeform control arm** for the eventual Haiku enum-locked comparison; no normalizer.

**What's next:** (queued at session close — completed in Sessions 58-61)
- STEP 1.6 (encode), STEP 2 ([LINK] sub), STEP 3 (validator), STEP 4 (suspicious-edges flagger), STEP 5 (Haiku smoke).
- **Per Matt's standing rule, /endsession was explicitly authorized this session.**

---

### Session 56 — Stage 4 Vocab Applied + Qualifier Vocab Lock-Down Planned (2026-05-18)

**Detail:** `history/session-details/session-056.md`

**Changes made:**
- `reference/architecture.md` — 17 new edge-type rows applied across 8 subsections; 2 description mods; vocab callout 132 → 149; Session-55-second-wave historical note added; gap-filing default rewritten to "vocab FINAL — reject as `no-fitting-type-vocab-locked`."
- `.claude/agents/prose-edge-classifier.md` — vocab FINAL flip; 5 `~149` references; 17 new types appended to in-prompt category-expansion list; reverse-direction section extended; CONTEMPORARY_WITH STOP-block contradiction fixed.
- `scripts/stage4-close-vocab-gaps.py` — NEW. Decision-map for all 68 rows in `working/wiki/pass2-buckets/questions-for-matt.jsonl`. 63 rows newly closed, 5 pre-resolved skipped, 0 unresolved.
- `working/qualifier-vocab/plan.md` — NEW. 1-screen plan for HAIKU-CUTOVER STEP 1.5. Three-tier framing locked: Tier 1 REQUIRED enum / Tier 2 OPTIONAL enum / Tier 3 freeform notes.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` — NEW.
- `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` — DELETED.
- `working/todos.md` — HAIKU-CUTOVER STEP 1 marked [x]; new STEP 1.5 inserted.
- New memory: `feedback_lockdown_before_long_passes.md`.

**Decisions:** **Three-tier qualifier framing locked.** **Haiku smoke (STEP 5) BLOCKED on qualifier vocab lock-down (STEP 1.5)** — closing every freestyle surface is the lever for making Haiku viable, not stronger prompts. **Lockdown-before-long-passes is now a project memory rule.** Three additional uncovered types resolved during apply without inventing new vocab: COMPETES_IN (rejected, duplicate of FIGHTS_IN), SOLD_TO (rejected, reverse-of-PURCHASED_FROM), TRANSACTS_WITH (rejected, too-generic).

**What's next:** (queued at session close — completed in Sessions 57-61)
- Qualifier vocab lock-down → Session 57.
- **Per Matt's standing rule, /endsession was explicitly authorized this session.**

---

> archive012 — 5/5 entries (FULL). Sessions 53, 54, 55, 56, 57. Next archives go to archive013.md.
