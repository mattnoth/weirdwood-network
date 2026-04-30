# Worklog Archive 005 — Sessions 22–24

> Archived from worklog.md at end of Session 26 (2026-04-28). These sessions cover the Wiki Pass 2 Stage 1 run through the Stage 2 cold review and the Stage 3 pipeline redesign. The narrative arc: Session 22 hit rate limits mid-Stage-1; Session 23 drained the remaining buckets and surfaced cost overruns; Session 24 ran Stage 2 cold review (returned `remediate`) which Matt overturned same-session by deferring `first_available` and pivoting to a Python-first pipeline for Stage 3+.

---

### Session 24 — Stage 2 Review + Stage 3 Pipeline Redesign (2026-04-27)
**Detail:** `working/session-details/session-024.md`
**Changes made:**
- `progress/continue-prompts/2026-04-27-wiki-pass2-core-review.md` → archived (Stage-2 review delegated to fresh general-purpose subagent; returned `remediate` with 2 HIGH findings).
- `progress/continue-prompts/2026-04-27-wiki-pass2-core-remediation.md` → archived (superseded by Matt's spoiler-gating deferral decision same-session).
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md` — NEW. Python-first pipeline (priority script + Stage 3a Python emit + mid-stage agent review + Stage 3b agent prose-fill on Tier A only).
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — NEW skeleton. Sequential to Stage 3, never parallel.
- `working/runbooks/wiki-pass2-pipeline.md` — NEW canonical runbook for Stage 3+. Defines tiers, Python-first rule, bucket preservation, mid-stage review.
- `working/runbooks/{wiki-pass2-orchestration-review,wiki-pass2-orchestration-build-self-review}.md` → moved to `working/runbooks/archive/` (reviewed obsolete agent-does-everything design).
- `working/runbooks/wiki-pass2-{orchestration,tier-handoff}.md` — SUPERSEDED-FOR-STAGE-3 banners added; mechanics still apply.
- `reference/architecture.md` § Spoiler Gating → DEFERRED status banner; Matt-direction language. Wiki data sources kept for backfill script.
- `CLAUDE.md` — `first_available` softened from architectural-required to optional/deferred. **NEW** Critical Rule: "The Wiki Is Already Local — Never Re-Fetch" alongside copyright rule.
- `worklog.md` Active Decisions — "DECIDED: Spoiler Gating Architecture" flipped to "DEFERRED: Spoiler Gating to Post-First-Release (2026-04-27)" with full supersession context.
- `.claude/agents/wiki-ingester.md` — `first_available` directives softened: do not emit, do not derive, do not file questions. (v2 prose-only rewrite is a sub-task before Stage 3b launch.)
- `.claude/commands/endsession.md` — NEW Step 9: copy/paste handoff block for fresh-Claude resumption.
- `graph/nodes/characters/{tyrion-lannister,varys}.node.md` — `first_available` nulled (parser bug class — both characters AGOT POVs but parser emitted ADWD).
- `working/todos.md` — Stage 3 entry rewritten for Python-first pipeline; Stage 4 added; wiki-ingester v2 prose-only sub-task added; spoiler-gating-backfill todo expanded.
- Memory: NEW `project_first_available_deferred.md` + `feedback_python_before_agent.md`. MEMORY.md index updated.
- Verified: Playwright fully uninstalled (no pip3 listing, no binary, no browser cache).

**Decisions:** **Two foundational rule changes.** (1) `first_available` / spoiler gating shelved entirely until post-first-release backfill. Reverses long-standing "architectural, not optional" position. Reason: every session reasoning about the field burns context for diminishing v1 value; wiki cite_ref data is rich enough that one deterministic backfill script after Pass 1 completes 5 books does the whole corpus. (2) **Python before Agent — project-wide default rule.** Whenever a deterministic step can produce part of the output, it runs first. Stage 1's 5.83 edges/node mean came mostly from infobox fields — deterministic data. Running an agent across 5,000+ secondary pages to extract that is wasted cost. Stage 3 redesigned: Python emits skeleton + edges for all Tier A+B; agent fills prose body for Tier A only; mid-stage agent review between 3a and 3b as quality gate. Tier C (no infobox + no cite_refs) deferred. Hard rule: never drop anything from sources. Edge discovery (prose-derived + cross-page) becomes Stage 4, sequential to Stage 3, never parallel. Wiki-cache-is-local rule promoted to CLAUDE.md Critical Rule severity.

**What's next:**
- `/continue 2026-04-27-wiki-pass2-stage3-prep` — fresh agent picks up the priority-bucket script + Stage 3a Python emit + mid-stage review + wiki-ingester v2 prose-only rewrite. Read `working/runbooks/wiki-pass2-pipeline.md` first for the canonical pipeline.
- Stage 4 (`2026-04-27-wiki-pass2-stage4-edge-discovery.md`) is a skeleton; flesh out only when Stage 3 finishes.

### Session 23 — Wiki Pass 2 Stage 1 Drain Complete (2026-04-27)
**Detail:** `working/session-details/session-023.md`
**Changes made:**
- `working/wiki-pass2/*/manifest.json` — 28 buckets flipped from pending/fail to `complete` (cumulative 37/37). All validator-report.json `passed: true`.
- `graph/nodes/{characters,houses,factions}/` — ~674 new node files (now 591 characters + 264 houses + 3 factions = 858 total).
- `graph/nodes/_conflicts/` — 52 files total (was 27 after Session 22; +25 from new bucket overlaps in this session).
- `working/wiki-pass2/questions-for-matt.jsonl` — 67 questions resolved in bulk (Session 22's first_available rule covered ~60; type-classification questions for Dragonkeepers/Brotherhood of Winged Knights/Order of the Green Hand resolved as `organization.faction`; House Sweet region overlap accepted as-is). 5 remain OPEN for Matt: House Donnerly, House Sarwyck, House Westford (video-game-only non-canon — keep/demote/exclude?); Arya Stark SPOUSE_OF Ramsay (Jeyne-as-Arya impersonation — edge handling); Aegon Targaryen Young Griff (parser used baby-Aegon's AGOT cite_refs for Young-Griff disambiguation).
- `working/extraction-stats/wiki-pass2-stats-core-v1.csv` — 28 new ok rows + 1 new skip-rate-limit (houses-reach-h hit cap mid-run at 11:34, succeeded on second try).
- `progress/continue-prompts/2026-04-27-wiki-pass2-core-review.md` — NEW Stage-2 cold-review handoff prompt per `working/runbooks/wiki-pass2-tier-handoff.md` §"Stage 2 prompt template". Carries forward the cost overrun + 5 open questions as data points for the fresh Claude to decide on.
- `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md` → moved to `progress/continue-prompts/archive/`.

**Decisions:** **Cost-per-bucket is 2-3× the original estimate.** Session 23 spent $68.10 across 28 ok buckets ($2.43/bucket); cumulative Stage 1 is $95.33 / 37 buckets = $2.58/bucket. The continue prompt's "$20-40 ballpark for the rest" assumed $0.71-1.43/bucket — actual is roughly 2× higher. Token mix shows cache_read dominance (1.5-3M tokens/bucket); the agent prompt + page bundle is heavier than the planning estimates. **Tier-secondary projection at this rate: ~$1,200 across 472 buckets.** Flagged as a Stage-2 decision input rather than a unilateral remediation call — the cold-review session decides whether bundle audit is a Stage-3 prereq. Bulk question-resolution strategy: 67/74 questions fit into 4 canned templates (first_available rule per Session 22, type-classification reclass, House Sweet region overlap, agent self-correction accepted); the 5 truly Matt-needs questions are surfaced in the Stage-2 prompt for explicit attention. Did NOT auto-resolve the 5 — those are domain calls. The launcher's `cmd_run` correctly retried the orphan `fail` buckets from prior sessions (iron-islands-h, lannister-j-q, targaryen-t-y, reach-h all recovered without a manual relaunch).

**What's next:**
- Stage-2 cold review per `progress/continue-prompts/2026-04-27-wiki-pass2-core-review.md`. Fresh Claude session, no carry-over context. Decision: proceed / remediate / escalate.
- All 74 questions now resolved (5 final ones answered by Matt at end of session). Zero open.
- Cost question is the live tension: $1,200 secondary projection deserves an audit pass before launch.

**Precedent decisions (Session 23, end-of-session) — apply going forward:**
- **Video-game-only entities are EXCLUDED from the graph.** Specifically: pages where the wiki disclaims the content as deriving solely from the Cyanide Studio "Game of Thrones" RPG (2012) or other licensed-derivative media not written by GRRM. Three nodes deleted this session: `house-donnerly.node.md`, `house-sarwyck.node.md`, `house-westford.node.md`. Tier-secondary triage should pre-filter these rather than emit-then-delete.
- **Impersonation edges redirect to the impersonator's node, not the victim's.** Arya Stark's `SPOUSE_OF Ramsay Bolton` edge was removed from arya-stark.node.md and reassigned to a future `jeyne-poole.node.md` (Jeyne was the actual bride, impersonating Arya). Pattern applies to other in-universe identity-fraud cases (Mance's son swap, Faceless Men identity changes, etc.) — the graph encodes who actually did the thing, not who was claimed to.
- **Disambiguated-name nodes can retain ambiguous first_available** for v1. Aegon Targaryen (Young Griff) keeps the parser's AGOT cite_refs even though many of those refs are about baby-Aegon (son of Rhaegar) — disambiguation precision is a v2 concern.

### Session 22 — Wiki Pass 2 Stage 1 Run, Partial (2026-04-26 → 2026-04-27)
**Detail:** `working/session-details/session-022.md`
**Changes made:**
- `.claude/agents/wiki-ingester.md` — slug rule rewritten (line 62): now strips every non-`[a-z0-9-]` char after lowercase + hyphenate-spaces, collapses runs of `-`. Fixes paren-page validation failures (e.g., `Alys Arryn (wife of Rhaegel)`). `first_available` override rule added at lines 81 + 170: if agent has positive evidence the parser value is wrong, set to `"always available"` and file question; otherwise default `null`.
- `graph/nodes/characters/sansa-stark.node.md` — `first_available` patched to `"always available"` (parser bug seed example).
- `progress/scratch-notes.md` — appended paren-slug finding.
- `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md` — fully rewritten with Session 22 state for next-session resume.
- `working/wiki-pass2/questions-for-matt.jsonl` — Sansa question marked resolved.
- 136 new node files under `graph/nodes/{characters,houses,factions}/` from 9 completed buckets (8 new + direwolves baseline).
- 27 conflict files under `graph/nodes/_conflicts/` (26 from stark-h-q overlap, 1 from stark-q-w).
- `working/extraction-stats/wiki-pass2-stats-core-v1.csv` — 18 rows: 9 ok, 8 skip-rate-limit, 1 direwolves baseline.
- `wiki-logs-` at repo root (untracked) — Matt's iTerm tab dump, 875 lines, referenced from continue prompt for diagnostics.

**Decisions:** Hit Anthropic Pro Max **7-day rate limit** (`rateLimitType: seven_day`, limit:100) after 9 successful buckets. Two retry attempts ~30 min apart both failed identically — burned ~$3-4 each on first-bucket-attempt-then-rate-limited. **Multi-letter character bucket overlap** confirmed: `stark-h-p ∩ stark-h-q = 26/27 pages`; same pattern likely for stark-{a-b, b-h, q-w, r-w}, greyjoy-{g-r, s-w}, martell-{a-m, m-t}, tyrell-{a-l}. Matt chose option (a) — accept the wasted runs, defer triage-script fix to post-Stage-1. Houses-X-Y vs Houses-X buckets are NOT overlapping (verified). **Launcher wave-math gotcha:** `weirwood wiki core 4 9` only opens 1 tab — `WAVE_SIZE=4` makes 36 buckets = 9 waves, and the loop's bound check rejects wave numbers > total_waves, leaving Terminals 2-4 with empty assignments. Workaround: use `3 3` for clean 3-tab parallelism. **Stats race conditions** in CSV `questions_filed`/`conflicts_filed` columns and **question ID collisions** (parallel agents all generated `q-2026-04-26-001`) noted; JSONL `bucket_id` is canonical.

**What's next:**
- Continue prompt (UPDATED, not archived): `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md` — resume after 7-day rate-limit window clears. 9/37 complete, 28 to go (21 pending + 7 fail). DoD unchanged.
- Verify `rateLimitType` via cached JSON before next launch attempt: `ls -t /tmp/wiki-pass2-*.json | head -1 | xargs grep -oE '"rateLimitType"|"resetsAt"'`
- Wipe `tmp/` for the 7 fail buckets before relaunching (script in continue prompt).
