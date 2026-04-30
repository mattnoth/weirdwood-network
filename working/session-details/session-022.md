# Session 22 — Wiki Pass 2 Stage 1 Run (partial: 9/37 buckets, hit 7-day cap)

**Date:** 2026-04-26 → 2026-04-27 (overnight session)
**Duration:** ~1.5 hours of active orchestration; multiple rate-limited stalls.
**Type:** Execution-heavy with two real findings.

## Goal

Drain the 36 pending core-tier wiki Pass 2 buckets per `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md`. This is Stage 1 of the 3-stage tier-handoff chain (`working/runbooks/wiki-pass2-tier-handoff.md`).

## Outcome

**Partial completion.** 9 of 37 core buckets `complete` (including direwolves from Session 20). 28 remain (21 pending + 7 rate-limit-fail). ~$25 burned. Hit Anthropic Pro Max **7-day rate limit** (`rateLimitType: seven_day, limit: 100`); cannot resume until weekly window clears.

The continue prompt at `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md` was **updated in place** with full Session 22 state so a future session can resume cleanly without rereading this file.

## Key findings (the only parts an agent needs)

### 1. Launcher wave-math bug

`weirwood wiki core <terms> <waves>` was called with `4 9` per the prompt's recommendation ("36 buckets at 1 bucket per wave"). Reality: `WAVE_SIZE=4` constant means 36 buckets = 9 waves, not 36. The launcher's loop assigned `[1..9]` to Terminal 1 and empty `[]` to Terminals 2-4 (wave numbers >9 silently rejected). Only ONE iTerm tab actually opened despite the "Launched 4 iTerm2 tabs" message.

**Workaround used:** `weirwood wiki core 3 3` for 3 terminals × 3 waves × 4 buckets/wave = clean 36-bucket coverage (T1=[1,2,3], T2=[4,5,6], T3=[7,8,9]).

The continue prompt was wrong about "1 bucket per wave"; updated. The bug itself (cmd_launch loop bound check rejects `tw > total_waves`) is real but low-priority — workaround works.

### 2. Multi-letter character buckets overlap heavily

`characters-house-stark-h-p` (Hodor → Poxy Tym, 27 pages) and `characters-house-stark-h-q` (Hullen → Quent, 27 pages) share **26/27 pages**. The triage script's alphabetical-split logic produces overlapping letter ranges. Same pattern likely applies to:
- stark-{a-b, b-h, q-w, r-w}
- greyjoy-{g-r, s-w}
- martell-{a-m, m-t}
- tyrell-{a-l}

The launcher's collision detection caught it — 26 of stark-h-q's 27 emitted nodes were routed to `graph/nodes/_conflicts/` rather than overwriting existing nodes from stark-h-p. Data integrity preserved.

**Decision (Matt):** Option (a) — accept the wasted runs, defer triage-script fix to post-Stage-1. Houses-X-Y vs Houses-X buckets are NOT overlapping (verified: `houses-crownlands-d-h` and `houses-crownlands-h` emitted disjoint house nodes).

### 3. Real validator rejection — paren-slug rule

`characters-house-arryn` validation-failed because three disambiguation pages emitted slugs containing parentheses:
- `alys-arryn-(wife-of-rhaegel)`
- `lord-arryn-(father-of-jeyne)`
- `ronnel-arryn-(son-of-jasper)`

Validator regex `[a-z0-9-]+` correctly rejected. Agent followed its prompt rule ("lowercase, strip apostrophes/commas, hyphenate spaces") which didn't include parens. **Fix landed:** `.claude/agents/wiki-ingester.md:62` slug rule rewritten to strip every non-`[a-z0-9-]` char after lowercasing+hyphenating, then collapse runs of `-`.

### 4. Track B parser bug — Sansa first_available

Agent emitted Sansa Stark with `first_available: ASOS 1 Prologue` (parser value verbatim per rule), but flagged via question: cite_refs span AGOT chapters 4-16. Parser bug, not Pass 2 bug. **Rule update (Matt's call):** if agent has positive evidence the parser value is wrong, override to `"always available"`; otherwise default to `null`. File a question either way. Sansa's node was patched manually as the seed example. Rule landed in agent prompt at lines 81 and 170.

### 5. Stats-channel race conditions

Two known-unreliable patterns from parallel runs:
- **Question ID collisions** — all 3 questions filed during Session 22 used `q-2026-04-26-001`. Parallel agents generate IDs without coordination. JSONL `bucket_id` is the source of truth.
- **CSV `questions_filed` / `conflicts_filed` columns lie** — `cmd_run` snapshots JSONL line counts before/after each bucket, so cross-tab writes count toward whichever bucket holds the snapshot window. JSONL `bucket_id` field is canonical.

Neither blocks the run. Defer fixes.

## Files changed

- `.claude/agents/wiki-ingester.md` — slug rule rewritten (line 62), `first_available` override rule added (lines 81, 170).
- `graph/nodes/characters/sansa-stark.node.md` — `first_available` patched to `"always available"`.
- `progress/scratch-notes.md` — appended paren-slug-fix note.
- `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md` — fully rewritten with Session 22 state for next-session resume.
- `working/wiki-pass2/questions-for-matt.jsonl` — Sansa question marked resolved.
- 136 new node files under `graph/nodes/{characters,houses,factions}/` from 9 completed buckets.
- 27 conflict files under `graph/nodes/_conflicts/`.
- `working/extraction-stats/wiki-pass2-stats-core-v1.csv` — 18 rows total (9 ok + 8 skip-rate-limit + direwolves baseline).

Plus an artifact at repo root: `wiki-logs-` (Matt's iTerm tab dump, 875 lines / 29KB). Not committed; referenced from the continue prompt for diagnostic recipes.

## Process notes (worth remembering, not a rule)

- **First-pass throughput surprise:** when iTerm worked correctly with the 3×3 config, ~5 buckets landed in ~7 min wall before rate-limit started biting. Per-bucket cost was $1.15 (direwolves baseline) → $2.78 (largest bucket); cache reads dominate ~80% of tokens.
- **Killing a stuck iTerm tab:** `kill -KILL <zsh-pid>` works after `kill -TERM` is ignored. Children (bash + claude -p) die naturally. Then `weirwood wiki unstick <bucket>` for the in-progress manifest.
- **iTerm window count matters:** the launcher's osascript `tell current window` fails if iTerm has 0 windows. Pre-flight check: `osascript -e 'tell application "iTerm2" to count windows'`. If 0, `create window with default profile` first.
- **Rate-limit detection in `wiki-pass2.sh:684-688`** matches `"status":"rejected"` AND `"rateLimitType"` in the JSON. The actual response had `"status":"needs-auth"` AND `"rateLimitType":"seven_day"` — but the script still flagged skip-rate-limit. Implication: there's a second status entry somewhere in the JSON. Worked, but not documented.

## What surprised me

- I expected the rate-limit cap to be the 5-hour daily window. It was the **7-day weekly cap on Pro Max** (limit: 100). Two relaunch attempts ~30min apart both failed identically with $3-4 burned each on first-bucket-attempt-then-rate-limited. **Lesson:** when all 3 tabs hit `skip-rate-limit` immediately, don't relaunch repeatedly — verify the actual `rateLimitType` first via the cached JSON in `/tmp/wiki-pass2-{bucket}.json`.
- The bucket-overlap finding was much more contained than I initially feared. Houses (sigil/seat data) bucket cleanly; only the very large character houses (those >30 members) triggered the alphabetical splitter and got broken ranges.
- The agent's self-disclosure on Sansa's `first_available` — following the verbatim rule while flagging the value as suspect — was exactly the channel discipline the runbook called for. Validates that pattern.

## Continue prompt status

`progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md` — **kept and updated** with full Session 22 state. Next session reads this + worklog Session 22 entry and resumes. DoD unchanged.
