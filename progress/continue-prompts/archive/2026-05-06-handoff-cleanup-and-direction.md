# Handoff — Cleanup, Scrubs, and Strategic Direction (2026-05-06)

**Type:** Stocktake + cleanup handoff. Self-contained — fresh agent should be able to pick up from this file alone, plus `CLAUDE.md` and `worklog.md`.

**Why this exists:** Pass 1 is complete across all 5 main books. Matt is exhausted of book passes (Dunk & Egg deferred but still on the list). Two cleanup tracks were started but not finished, and the strategic "what's next" question is open. Don't continue the prior agent's transcript — work from this file.

---

## 0. Hard rules for this session (read first)

- **Do NOT auto-launch extractions, wiki-pass2 runs, or any agent fleet.** Always confirm with Matt.
- **Do NOT run `/endsession`** without explicit permission from Matt.
- **Do NOT read top-level `scratch`** outside `/endsession` step 4(a).
- **Do NOT edit historical archives** (`working/worklog-archives/*`, `working/session-details/session-NNN.md`, `progress/continue-prompts/archive/*`). They are records of what was thought at the time. Out of scope for both scrubs.
- **Do NOT touch `sources/`** — anything in that tree is source data (book chapters, wiki JSONs with embedded copyright footers). Read-only and additive-only.

### Matt's notes (2026-05-06) — preserved verbatim

> "I've killed everything else. You are the boss now."

So: no other agent is active. The previous handoff bullet about waiting for a parallel `working/todos.md`-reorg agent is **resolved** — that work is done, `working/todos.md` is fair game. (Q2 below is now closed.)

> [On the no-edit-historical-archives rule] "this should actually be a hook probably. we cannot depend on a rule, apparently, for this type of behavior."

> [On the no-touch-`sources/` rule] "Another hook. Anything in the source folder, period, cannot be written to or overwritten."

**Hook follow-ups (not in scope for this session — add to `working/todos.md` as separate items):**

1. Add a `PreToolUse` hook in `.claude/settings.json` that blocks `Edit|Write|MultiEdit` on paths matching `working/worklog-archives/`, `working/session-details/session-*.md`, or `progress/continue-prompts/archive/`.
2. Add a `PreToolUse` hook that blocks `Edit|Write|MultiEdit` on any path under `sources/`.

These convert two rules-only protections into mechanical ones. Spec them properly in a follow-up session — do not freelance the hook config in this session.

---

## 0.5. Decisions awaiting Matt's review

Matt fills in `DECISION:` lines below. **Do not begin orchestration (§ 7) until every DECISION line marked _required_ is filled in.** If a required line is blank when the orchestrator agent reads this file, **abort and surface to Matt** — do not fall back to a default.

### Execution decisions (required before agents fire)

**Q1. Sketches-archive directory name** — where `working/chat-ui-architecture.md` (and possibly `working/diagrams.md`) lands.
- (a) `working/sketches-archive/`
- (b) `working/archive/sketches/`
- (c) other: ___________

DECISION (required): **(b) `working/archive/sketches/`** — Matt 2026-05-06

---

**Q2. ~~`working/todos.md` § 11 handling~~** — **CLOSED.** Matt killed the prior reorg agent; the reorg is done. `working/todos.md` no longer has a `§ 11`; the three chat-UI-framed items now live at lines 106-108 under `## Wiki / Pass 2 Prep` (wrong topical home, but findable by grep). Scrub A handles them per § 2 below.

---

**Q3. `STATUS.md`** — open question from session 36; ~2 weeks stale; duplicates `CLAUDE.md` + worklog Current State. Note: only **line 122** has a copyright-rule hit (the plan previously also cited line 148, which is stale — no such hit exists today).
- (a) Refresh to current state
- (b) Retire entirely (delete the file)
- (c) Leave alone — decide later

DECISION (required): **(b) Retire entirely** — Matt 2026-05-06. Note for orchestrator: handoff plan's claim that "only line 122 has a copyright hit (line 148 is stale)" is itself stale — live grep on 2026-05-06 shows BOTH line 122 and line 148 still contain copyright references. With (b) the whole file goes away regardless, so this point is moot — but flag it if Q3 ever gets revisited.

---

**Q4. `working/diagrams.md`** (352 lines) — Diagram #1 hard-codes "D&D group / behind auth" in the project-at-a-glance. Diagram #12 is titled "Friend-group deployment (chat UI v1)".
- (a) Surgical edit only — drop the chat-UI box from diagram #1, drop diagram #12, retitle if needed
- (b) Archive whole file alongside `chat-ui-architecture.md` (pre-decided: companion sketch)
- (c) Give Scrub A latitude to decide based on density — surgical edit if ≤2 diagrams stale, archive whole file if >2

DECISION (required): **(b) Archive whole file** alongside chat-ui-architecture.md — Matt 2026-05-06

---

**Q5. Two-repo split idea** — its only stated justification was copyright-isolation, which is being deleted in Scrub B.
- (a) Retire entirely — drop from `working/todos.md`, drop from memory, drop from any scope docs
- (b) Park for another reason: ___________ (e.g., private-extractions-repo? pure separation hygiene?)

DECISION (required): **(a) Retire entirely** — Matt 2026-05-06. Matt's literal phrasing was "park and delete reference to" — interpreted as: delete the explicit references in todos/memory/scope docs (the (a) action). Matt may revisit the concept later but it leaves the project's tracked state for now.

---

**Q6. Spoiler-gate "fully open for v1" framing**
- (a) Was a chat-UI-v1-only decision → retire with the rest of the chat-UI framing
- (b) Is a graph-level decision (the graph itself ships ungated) → keep, but reframe so it doesn't reference chat-UI v1
- (c) Defer — `first_available` is already deferred per `architecture.md`; this rides along

DECISION (required): **(c) Defer** — Matt 2026-05-06. "Too complicated for first pass; should remain relevant but deferred." Rides on the existing `first_available` deferral.

---

### Confirmations (yes/no)

**Q7.** Sub-agent dispatch mode for Phase 1 (Scrub A + Scrub B + citation-validator).
- (a) Parallel — fastest. Safe because the three sub-agents touch disjoint file sets (verified: Scrub A has no README.md edit work to do, see § 2).
- (b) Serial — Scrub A → Scrub B → citation-validator. Slower, lets Matt spot-check between steps.

DECISION (required): **(a) Parallel** — Matt 2026-05-06 ("you choose"). File sets are disjoint per § 2 (Scrub A doesn't touch README.md; Scrub B doesn't touch chat-ui-architecture.md or diagrams.md or todos.md lines 106-108).

---

**Q8.** Run model-fit audit (Phase 2) in the same session as scrubs?
- (a) Yes — same session
- (b) No — hold for another session

DECISION (required): **(a) Yes** — Matt 2026-05-06. Note: model-fit audit is **input** to a separate fleet-plan review (`working/fleet-orchestration-plan.md` + `working/fleet-runtime-architecture.md`) — capture that connection in the audit report so the fleet-plan review session can ingest it directly. Add a "Review fleet plan against model-fit recommendations" item to `working/todos.md` as part of Phase 4.

---

**Q9.** Confirm `.gitignore` + `.claude/settings.json` permission denials stay in place untouched. With the copyright rule deleted from docs, those are the **only** remaining protection for `sources/raw/`, `full-txt-files/`, `epubs/`. (The two hook follow-ups in § 0 would be a third layer if implemented.)
- (a) Yes — leave both files untouched
- (b) Also strip the protections (NOT recommended — would remove the only mechanical guard)

DECISION (required): **(a) Yes — leave both untouched** — Matt 2026-05-06

---

**Q10.** Output locations

DECISION (Matt 2026-05-06 — overrides defaults): **Adopt a structured per-audit folder layout going forward.** Each audit gets its own directory under `working/audits/` named `<one-line-audit-slug>-<YYYY-MM-DD>/`, with these subdirectories:
- `prompt-planning/` — the planning prompt that scoped the audit, plus any pre-audit notes
- `prompt/` — the actual prompt(s) handed to the executing sub-agent
- `execution/` — the audit's output artifacts (the report, raw data, intermediate files)
- `validation/` — independent validation artifacts (separate-session audits of the audit, like this validation prompt)

For this session:
- Model-fit audit → `working/audits/agent-model-fit-2026-05-06/execution/agent-model-fit-report.md` (with corresponding `prompt/` containing the dispatch prompt from § 7 Phase 2)
- Citation-validator → `working/audits/citation-corpus-rerun-2026-05-06/execution/citation-issues.md` (with `prompt/` containing the dispatch prompt)
- Validation artifacts (e.g., a future independent re-check of either audit) land in the same `<audit>/validation/` subdir

The orchestrator creates these directories before dispatching the sub-agents and tells each sub-agent its specific output path. **Note:** existing audits at older flat paths (`working/audits/citation-issues-*.md`, etc.) are NOT migrated — leave them where they are; the new layout applies to new audits only.

---

### Strategic / framing

**Q11. Dunk & Egg Pass 1**
- (a) Formally deferred indefinitely (move from "in progress" to "deferred" in `worklog.md` Current State and any other tracking)
- (b) Just "not now" — keep on the books, no urgency tag change
- (c) Drop entirely

DECISION (required, lands in worklog Current State + `working/todos.md`): **(b) Just "not now"** — keep on the books, no urgency tag change — Matt 2026-05-06. Rationale: D&E content will eventually enrich existing main-arc nodes (Bloodraven, Egg/Aegon V, the Targaryen pre-history threads, etc.) — focus stays on the ASOIAF main timeline, but D&E is a known future enrichment pass, not a dropped track. Worklog Current State should reflect "deferred (enrichment pass for main-arc nodes)" rather than "in progress" or "deferred indefinitely."

---

**Q12. Strategic question surfacing (§ 4)** — after Phase 1+2 complete, does the orchestrator:
- (a) Surface the Stage-4-vs-mention-index question proactively in the same session (Phase 3 runs)
- (b) Stop after scrubs/audits and leave the strategic question for a separate fresh session (Phase 3 skipped)

DECISION (required): **(b) Skip Phase 3** — Matt 2026-05-06 ("hmmm, b?"). Strategic question stays open for a separate fresh session.

---

## 1. Strategic direction (the WHY correction)

The graph **for agent traversal** is the real product. Specifically: a graph dense and clean enough that an LLM agent can answer ASOIAF questions by walking it and citing back to chapters/wiki.

The "D&D-group chat UI / shared-password auth / two-repo split for friend-group preview" framing is **stale sketch** from when the project was just being scoped. Matt has confirmed:

- It will go on an unpublished, unlinked page.
- No auth.
- The chat layer is downstream and not load-bearing on the graph design.
- Don't grow the graph to chase chat-UI requirements.

**Reframe added 2026-05-06 (post-decisions):** Matt clarified the chat UI is **not** dead as a concept — he still plans to build it, but reframed as an **"ask-questions-and-get-detailed-answers" interface on top of the graph**, not a D&D-group preview. Rationale: it's the fastest way to demonstrate the graph's value outward-facing once the knowledge graph is solid enough. So the scrubs target the specific stale framing (D&D group / shared password / friend-group-only / cost-envelope-for-D&D-scale) — they do NOT delete the *concept* of a chat UI. If a future todo captures "ask-questions UI on top of the graph" cleanly, that's a NEW item, not a salvage of the old PROMINENT bullets.

This shift is captured in user memory `project_real_goal_graph_for_agents.md` (already written this session). That memory itself contains a "copyright-isolation" line that needs the copyright-scrub treatment in § 3 below.

---

## 2. Scrub A — D&D-framing artifacts

Two parallel agent investigations (this thread + a separate Claude Code window) converged on the same scope. Status:

| File | Status | Action |
|------|--------|--------|
| `working/chat-ui-architecture.md` (735 lines) | Stale sketch | Move to `<sketches-archive>/chat-ui-architecture.md` (per Q1) with a 2-line preamble explaining it's stale-sketch, not design. The directory does NOT yet exist; create it. |
| `working/diagrams.md` (352 lines) | Mixed (Diagram #1 + Diagram #12 are chat-UI-framed) | Per Q4 — either surgical edit OR archive whole file alongside `chat-ui-architecture.md`. |
| `working/todos.md` lines 106-108 | Three "PROMINENT" bullets with D&D/chat-UI framing | Edit per Q5 + Q6: retire the "Two-repo split" bullet entirely if Q5=(a); reframe the "Spoiler gate fully open" bullet per Q6; rewrite or delete the "Chat UI scope" bullet (the chat layer is unauthenticated/unlinked per § 1, so the auth/D&D/cost-envelope framing all goes). The bullets are NOT in a `§ 11` anymore — the prior reorg moved them under `## Wiki / Pass 2 Prep` (wrong topical home but find by line number or content anchor). |
| `README.md` | **Verified clean of D&D framing** (the only "chat" hits are the repo name `asoiaf-chat`). | **No Scrub A edit needed.** Scrub B still touches line 220 for the copyright-clause edit. |
| `STATUS.md` | Dated 2026-04-23, ~2 weeks stale | Per Q3. If Q3=(b) retire, the file goes away in Scrub B regardless. |
| `architecture.md`, `CLAUDE.md` | Verified clean of D&D framing | No edits needed. The "queryable knowledge graph" / "spoiler-gated queries that traverse connections" framing in both files is well-aligned with graph-for-agents. |
| `worklog.md` | Verified clean of D&D framing in current rolling-5 sessions | No Scrub A edit needed. Scrub B still edits line 35. |
| `working/worklog-archives/*`, `working/session-details/*`, `progress/continue-prompts/archive/*` | Historical | Do not edit. |

**Known false positives — do not edit:**
- `sources/chapters/agot-jon-09.md` contains the phrase "Jon's friend group" in GRRM's chapter prose (Sam/Pyp/Grenn at the Wall).
- `README.md` line 10/17/18/21/25/28/184 — `asoiaf-chat` is the repo name, not chat-UI framing.
- This handoff file itself contains the framing terms (will be archived in Phase 4).
- `working/sketches-archive/chat-ui-architecture.md` (after Scrub A) — intentionally archived.

---

## 3. Scrub B — Remove the "don't commit copyrighted content" rule entirely

**Decision (made by Matt 2026-05-06):** Delete the rule, not just rephrase it. The `.gitignore` continues to mechanically protect `sources/raw/`, `full-txt-files/`, and `epubs/` — that's enough. The textual rule across docs and memory is being retired.

**Implication:** with the rule gone from `CLAUDE.md`, `worklog.md`, `/endsession`, and memory, agents won't have a textual reminder that those directories are off-limits to commit. Mechanical protection (gitignore + per-path permission denials in `.claude/settings.json`) is the only line of defense going forward. That's the trade Matt is taking. (The hook follow-ups in § 0 would add a third layer.)

**Files to edit (10 confirmed hits — line numbers verified 2026-05-06; agent should still locate by string anchor since drift is possible):**

| File | Line(s) | What to do |
|------|---------|------------|
| `/Users/mnoth/source/asoiaf-chat/CLAUDE.md` | 22 + body | Delete the entire `## Critical Rule: Copyrighted Content` section (header + body, up to but not including the next `##` header) |
| `/Users/mnoth/source/asoiaf-chat/README.md` | 220 | Surgical edit — drop the clause `, and verifies \`.gitignore\` still protects copyrighted content` from the /endsession narrative; keep the rest of the sentence intact |
| `/Users/mnoth/source/asoiaf-chat/STATUS.md` | 122 | Per Q3. If Q3=(b) retire, delete the whole file and skip this row. Otherwise: surgical-edit line 122 to drop `(copyrighted content protection)` from the comment, keeping the path. **Note:** the previous version of this plan also cited line 148; that's stale, no such hit exists. Verify with `grep -n "copyright" STATUS.md` before editing. |
| `/Users/mnoth/source/asoiaf-chat/.claude/commands/endsession.md` | 29 | Delete step 7 entirely (the `**Verify .gitignore**` step) and renumber subsequent steps. **Verify by grep** — the step number could have shifted. |
| `/Users/mnoth/source/asoiaf-chat/worklog.md` | 35 | Delete the Current State checklist line `- [x] .gitignore protecting copyrighted content (sources/raw/, sources/chapters/, full-txt-files/, epubs/)` |
| `/Users/mnoth/source/asoiaf-chat/progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` | 44 | Delete the bullet `Never commit copyrighted source files (gitignore handles this; \`extractions/\` is private repo, OK)` |
| `/Users/mnoth/source/asoiaf-chat/working/runbooks/book-integration-done.md` | 321 | Delete the bullet `Confirmation that no copyrighted content is staged for git` |
| `/Users/mnoth/source/asoiaf-chat/working/scratch-design-review-stage3b.md` | 161 | Surgical edit — drop the parenthetical `(gitignored copyrighted content)`, keep the rest of the line (`Do NOT read sources/raw, sources/chapters` framing is still useful for token-cost reasons) |
| `/Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_never_commit_books.md` | whole file | **Delete the file entirely** (`rm`) |
| `/Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/MEMORY.md` | 2 | Delete the index line `- [Never commit copyrighted book content](feedback_never_commit_books.md) — sources/raw/ and sources/chapters/ must NEVER enter git history` |
| `/Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/project_real_goal_graph_for_agents.md` | 17 | Surgical edit per Q5. Current text: `The two-repo split (\`weirwood-network\` public / \`weirwood-corpus\` private) is still a sensible copyright-isolation move IF it's ever needed; it's not gated on a chat UI shipping.` If Q5=(a) retire, delete the line. If Q5=(b) park-for-other-reason, rewrite to capture that reason. |

(The table has 11 rows but the memory-file deletion + MEMORY.md edit are paired, so it's effectively 10 distinct file edits with one deletion.)

**Do NOT edit:**
- `sources/wiki/_raw/*.json` — wiki page source data (footer-text artifacts only; not project rules)
- `sources/**` — anything else in `sources/` is also off-limits per § 0
- `working/worklog-archives/*` — historical record
- `working/session-details/*` — historical record
- `progress/continue-prompts/archive/*` — historical (3 archived prompts, all dated 2026-05-02 or 2026-05-04)
- `working/chat-ui-architecture.md` — being archived as stale sketch in Scrub A; no point editing it first
- The (post-Scrub-A) archived copy of `chat-ui-architecture.md` in `<sketches-archive>/` — preserved as historical record

**After Scrub B is done, re-grep to confirm zero hits in tracked rules/runbooks/handoffs:**
```
grep -rEni "copyright|copyrighted" --include="*.md" \
  --exclude-dir=sources \
  --exclude-dir=working/worklog-archives \
  --exclude-dir=working/session-details \
  --exclude-dir=archive \
  /Users/mnoth/source/asoiaf-chat
```
Expected remaining hits (all OK):
- This handoff file itself (will be archived in Phase 4 — references survive in archive intentionally).
- The post-Scrub-A archived `chat-ui-architecture.md` if `<sketches-archive>` is not under an `--exclude-dir`-matched path. Add `--exclude-dir=sketches-archive` (or whatever Q1 names it) if so.

**Note on macOS grep:** Use `grep -E` with `|` for alternation. BSD basic regex does not reliably support `\|` — it can match the literal characters instead of acting as alternation. Both verification greps below use `-E`.

---

## 4. Strategic question (open, not yet decided)

> "What's next before the chat? Or in parallel — hardening the nodes/edges based on the books?"

Two concrete work tracks already have continue-prompts:

- **`progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`** — Build prose-edge classifier and cross-identity detector. Stage 4 v1 is unblocked now that Pass 1 is 344/344.
- **`progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md`** — Three new passes (1.5/1.6/1.7) for dialogue, meals, and mention-index. Has 7 open questions awaiting Matt.

Both predate the "graph-for-agents not chat-UI" framing correction. Re-read each through that lens before proposing execution. Specifically:

- The dialogue/meals/mention-index design was scoped to feed the chat UI's three-corpus retrieval. Some of that may still be the right shape (mention-index is graph-traversal value too), but the *justification* needs a re-frame and the priority may shift.
- The Stage 4 prose-edge-classifier work is pure graph hardening — exactly what "harden the graph" means. This is the most aligned with the corrected framing.

**Suggested order to discuss with Matt** (do not execute without approval):

1. Finish both scrubs above first (~15-30 min of careful work, plus Matt's decisions on the Q1-Q12 lines).
2. Re-read the two queued continue-prompts under the graph-for-agents lens. Surface what changes.
3. Likely-next work: Stage 4 prose-edge-classifier (most aligned). Mention-index can run in parallel if Matt wants.
4. Dunk & Egg Pass 1 still on the list but explicitly deferred — Matt is exhausted of book passes. Land Q11's decision into `worklog.md` Current State + `working/todos.md`.

---

## 5. Two READY-TO-DO items still valid (from session 36)

These were flagged as picked-up-from-todos.md-directly, no continue prompt needed. Both still align with graph-for-agents:

1. **Model-fit audit across `.claude/agents/*.md`** — resource-conservation pass; investigate Sonnet 4.6 / Haiku 4.5 viability for each agent; default to cheapest viable; document in prompt frontmatter. Output → `working/model-fit-audit-2026-05-06.md` (per Q10).
2. **Re-run citation-validator on full 5-book corpus** — Pass 1 now 344/344, so previously-deferred chapter-cite checks should resolve. Output → standard dated location (per Q10).

---

## 6. State snapshot at session end

- **Pass 1:** 344/344 across 5 main books (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73). All v3 schema. Dunk & Egg deferred.
- **Graph nodes:** 7,832 across 19 subdirs (characters 3,913, locations 1,056, houses 556, events 380, artifacts 266, titles 539, _conflicts 248, others smaller).
- **`graph/edges/`:** Empty (0 files). This is by design per `architecture.md` — edges live inline in node frontmatter, not as separate files. **Do not read the empty directory as evidence of missing work.**
- **Edge state — what is and isn't promoted:** Wiki **infobox** edges have been promoted into node frontmatter through the Stage 1-3 / Path B / Tier 3 campaigns (Sessions 22-29 drained Cat 1 orphan edges from 7,784 → 1,963 along the way). What is **not** yet promoted is **prose-derived** edges — edges that wiki article bodies (and Pass 1 chapter extractions) encode but infoboxes don't. That work is `Wiki Pass 2 Stage 4 — prose-edge discovery` and its continue prompt is `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`. Stage 4 was gated on Pass 1 reaching multi-book coverage; that gate is now met (344/344). Stage 4 is the last big wiki-side track and the most aligned with "harden the graph for agent traversal" — it is the strongest candidate for the work that follows these scrubs (see § 4 and Q12).
- **Continue prompts active:** 2 (`2026-05-02-stage4-v1-prose-edge-classifier.md`, `2026-05-05-dialogue-meals-mention-index-design.md`) + this file.
- **Continue prompts archived:** 3 (all 2026-05-02 / 2026-05-04, archived in session 36).
- **Worklog state:** 5 sessions in main worklog (the strict cap from session 36's rule). Next session lands → archive Session 32 (or oldest) into `working/worklog-archives/archive007.md` (which already has Sessions 30-31, room for 3 more).
- **Other-agent activity:** **None.** Matt killed all parallel agents before this handoff was finalized. The `working/todos.md` reorg referenced in earlier drafts of this plan is **done** — the file is fair game.

---

## 7. One-session orchestration plan (parallel sub-agent dispatch)

Goal: get Scrubs A + B and both READY-TO-DO items done in a single session.

### Phase 0 — Gates (orchestrator does these in main thread, ~5 min)

1. Read this file, `CLAUDE.md`, `worklog.md`.
2. **Verify every `DECISION (required):` line in § 0.5 is filled in.** If any required line is blank, **abort and surface to Matt**. Do not fall back to any default.
3. Translate § 0.5 decisions into runtime values for the sub-agent prompts below (e.g., substitute Q1's directory name into the Scrub-A prompt, branch on Q3/Q4/Q5/Q6/Q7/Q12).

### Phase 1 — Scrubs (3 sub-agents)

**If Q7 = (a) parallel:** Dispatch all three in a single message with three Agent tool calls. Safe because file sets are disjoint (Scrub A no longer touches `README.md`, see § 2).

**If Q7 = (b) serial:** Dispatch Scrub A first; await completion; spot-check; then Scrub B; spot-check; then citation-validator.

| Sub-agent | Type | Prompt summary |
|-----------|------|----------------|
| **Scrub A — D&D framing** | `general-purpose` | Execute § 2 of `progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md`. Create `<Q1-directory>`, move `working/chat-ui-architecture.md` into it with the preamble in the template below, handle `working/diagrams.md` per Q4, edit `working/todos.md` lines 106-108 per Q5+Q6. **Do NOT touch `README.md`** (Scrub B handles its only edit; § 2 confirms README.md has no D&D framing hits beyond the repo name `asoiaf-chat`). Report files-changed + a final re-grep result. |
| **Scrub B — Copyright rule removal** | `general-purpose` | Execute § 3 of `progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md`. Delete the rule from all 10 listed locations, branching on Q3 for STATUS.md and Q5 for `project_real_goal_graph_for_agents.md` line 17. DO NOT touch `sources/`, archives, or session-details. Report files-changed + a final re-grep result showing zero hits in tracked .md files (excluding the expected hits noted in § 3). |
| **Citation-validator re-run** | `citation-validator` | Re-run the audit on the full 5-book corpus now that Pass 1 is 344/344. Previously-deferred chapter-cite checks should now resolve. Standard dated report to the location specified in Q10. |

### Phase 2 — Sequential after Phase 1 (1 sub-agent, runs only if Q8 = (a))

| Sub-agent | Type | Prompt summary |
|-----------|------|----------------|
| **Model-fit audit** | `general-purpose` | Read every `.claude/agents/*.md`. For each agent prompt, assess whether Sonnet 4.6 or Haiku 4.5 could do the work the prompt describes (vs the current default Opus 4.7). Cheapest-viable rule applies. Output a markdown table to `working/model-fit-audit-2026-05-06.md`: agent name → current model assumption → recommended model → one-sentence rationale → smoke-test recommendation. Do NOT modify any agent prompts; this is a recommendation pass. Matt reviews before any prompt frontmatter changes. |

This depends on Phase 1 only insofar as you don't want to be modifying `.claude/agents/*.md` while the audit runs. Neither scrub touches those files, so Phase 2 could parallelize with Phase 1 — orchestrator's call, prefer sequential for cleaner reporting.

### Phase 3 — Strategic question (orchestrator surfaces to Matt, no sub-agent; runs only if Q12 = (a))

After Phases 1 (+ 2 if Q8=(a)) are done:
- Re-read both queued continue-prompts (`2026-05-02-stage4-v1-prose-edge-classifier.md`, `2026-05-05-dialogue-meals-mention-index-design.md`) under the graph-for-agents lens.
- Surface to Matt: which next? Stage 4 is most aligned with "harden the graph"; mention-index is graph-traversal value but the dialogue/meals scope was scoped for chat retrieval and may shrink under the corrected framing.

If Q12 = (b), skip Phase 3 entirely — leave the strategic question for a separate fresh session.

### Phase 4 — Session end

- Update `worklog.md` (session entry, ≤30 lines). Land Q11's decision into Current State.
- Create `working/session-details/session-037.md` only if the session contained design discussion or novel decisions worth long-form. Pure-execution scrubs do NOT need a session-details file (per session 36's revised rule).
- Add the two hook follow-ups from § 0 to `working/todos.md` as separate items (not action-now).
- This handoff file (`2026-05-06-handoff-cleanup-and-direction.md`) can be archived to `progress/continue-prompts/archive/` once scrubs are complete and Phase 3 has surfaced (or has been skipped per Q12).
- Do **not** auto-run `/endsession` — wait for Matt to invoke it.

### Sub-agent prompt templates (copy-pasteable)

**For Scrub A:**
```
You are executing Scrub A from /Users/mnoth/source/asoiaf-chat/progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md § 2 (D&D-framing artifacts).

Inputs from § 0.5 decisions (orchestrator fills these in before dispatch):
- Sketches-archive directory (Q1):       <FILL>
- diagrams.md handling (Q4):              <FILL: a/b/c>
- Two-repo split (Q5):                    <FILL: a/b — if b, also fill non-copyright reason>
- Spoiler-gate framing (Q6):              <FILL: a/b/c>

Steps:

1. Create the sketches-archive directory (Q1). It does not exist today.

2. Move /Users/mnoth/source/asoiaf-chat/working/chat-ui-architecture.md into <Q1>/chat-ui-architecture.md. Prepend a 2-line preamble at the top of the file before any existing content:
   ```
   > **STALE SKETCH (archived 2026-05-06).** The D&D-group chat UI / shared-password auth framing this doc describes was retired; the project's real goal is a graph for agent traversal. Preserved for historical reference only.
   ```

3. Handle /Users/mnoth/source/asoiaf-chat/working/diagrams.md per Q4:
   - If Q4=(a) surgical edit: read the file, drop the chat-UI box from Diagram #1 (lines ~9-20), drop Diagram #12 ("Friend-group deployment (chat UI v1)"), retitle Diagram #1's right-hand column from "Chat UI / D&D group / hosted web UI / behind auth" to something graph-for-agents-aligned (e.g., "agent traversal / unauthenticated, unlinked").
   - If Q4=(b) archive whole file: move to <Q1>/diagrams.md with the same preamble pattern as step 2.
   - If Q4=(c) latitude: read the file, count chat-UI-framed diagrams; if >2, archive whole file (option b); else surgical edit (option a).

4. Edit /Users/mnoth/source/asoiaf-chat/working/todos.md lines 106-108. The bullets are NOT in a "§ 11" anymore — they live under "## Wiki / Pass 2 Prep" (wrong topical home, but find them by content):
   - Line 106 ("PROMINENT — Spoiler gate defaults FULLY OPEN for v1") — handle per Q6:
     * Q6=(a): delete the bullet entirely.
     * Q6=(b): rewrite to remove "for v1 chat UI / retrieval layer" framing; reframe as "the graph itself ships ungated; first_available remains deferred."
     * Q6=(c): leave alone (rides on existing first_available deferral).
   - Line 107 ("PROMINENT — Chat UI scope shifted to deployable D&D-group preview") — DELETE entirely. The chat layer per § 1 is unauthenticated, unlinked; all the D&D / auth / cost-envelope framing in this bullet is retired.
   - Line 108 ("Two-repo split before chat-UI deployment") — handle per Q5:
     * Q5=(a): delete the bullet entirely.
     * Q5=(b): rewrite to capture the non-copyright reason Matt filled in; drop the "chat-UI deployment" framing.

5. Skip /Users/mnoth/source/asoiaf-chat/README.md entirely. The handoff doc § 2 confirms it has no D&D-framing hits — all "chat" matches are the repo name "asoiaf-chat". Scrub B handles README.md's only edit (the line 220 copyright clause).

6. Final verification: from /Users/mnoth/source/asoiaf-chat run:
   grep -rEni "D&D|friend group|shared password|chat UI|chat-ui" --include="*.md" \
     --exclude-dir=sources \
     --exclude-dir=working/worklog-archives \
     --exclude-dir=working/session-details \
     --exclude-dir=archive \
     --exclude-dir=<Q1-basename> \
     .

   Expected remaining hits (all OK):
   - this handoff file itself (will be archived in Phase 4)
   Anything else: report and stop. Do not auto-edit.

Report: files moved, files edited (with one-line summary per file), the final grep output, and whether anything unexpected surfaced.
```

**For Scrub B:**
```
You are executing Scrub B from /Users/mnoth/source/asoiaf-chat/progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md § 3 (copyright-rule removal).

Decision: DELETE the rule entirely. Do not substitute language. The .gitignore continues to mechanically protect source directories.

Inputs from § 0.5 decisions:
- STATUS.md handling (Q3):          <FILL: a/b/c>
- Two-repo split memory (Q5):       <FILL: a/b — if b, fill non-copyright reason>

For each edit below, locate the target by string anchor (grep for the quoted text), not by trusting line numbers — line numbers were verified 2026-05-06 but can drift.

Files to edit:

1. /Users/mnoth/source/asoiaf-chat/CLAUDE.md
   Anchor: "## Critical Rule: Copyrighted Content"
   Action: Delete the entire section — the header line, the body, up to but NOT including the next "## " header.

2. /Users/mnoth/source/asoiaf-chat/README.md
   Anchor (line ~220): the clause ", and verifies `.gitignore` still protects copyrighted content"
   Action: Surgical edit — drop only that clause. Keep the rest of the sentence intact.

3. /Users/mnoth/source/asoiaf-chat/STATUS.md
   Per Q3:
   - Q3=(a) refresh: surgical-edit line 122 to drop "(copyrighted content protection)" from the comment, keeping the path. Then update the rest of the file to reflect current state separately (out of scope here — flag as a follow-up).
   - Q3=(b) retire: rm the file entirely; skip line 122 edit.
   - Q3=(c) leave alone: surgical-edit line 122 to drop "(copyrighted content protection)" only.
   Note: the previous version of this plan also cited line 148 as needing an edit; that's stale (verified 2026-05-06 — only line 122 has a hit). Confirm with `grep -n "copyright" STATUS.md` before any edit.

4. /Users/mnoth/source/asoiaf-chat/.claude/commands/endsession.md
   Anchor: "**Verify .gitignore**" (currently step 7)
   Action: Delete the entire step. Renumber any subsequent steps.

5. /Users/mnoth/source/asoiaf-chat/worklog.md
   Anchor: "- [x] .gitignore protecting copyrighted content"
   Action: Delete the entire bullet from the Current State checklist.

6. /Users/mnoth/source/asoiaf-chat/progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md
   Anchor: "Never commit copyrighted source files (gitignore handles this"
   Action: Delete the entire bullet.

7. /Users/mnoth/source/asoiaf-chat/working/runbooks/book-integration-done.md
   Anchor: "Confirmation that no copyrighted content is staged for git"
   Action: Delete the entire bullet.

8. /Users/mnoth/source/asoiaf-chat/working/scratch-design-review-stage3b.md
   Anchor: "(gitignored copyrighted content)"
   Action: Surgical edit — drop the parenthetical only. Keep the surrounding "Do NOT read sources/raw, sources/chapters" framing intact.

9. /Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_never_commit_books.md
   Action: Delete the entire file (`rm`).

10. /Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/MEMORY.md
    Anchor: "- [Never commit copyrighted book content](feedback_never_commit_books.md)"
    Action: Delete the entire line.

11. /Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/project_real_goal_graph_for_agents.md
    Anchor: "still a sensible copyright-isolation move"
    Action per Q5:
    - Q5=(a): delete the entire bullet/line.
    - Q5=(b): rewrite to capture the non-copyright reason Matt filled in. Drop the "copyright-isolation" phrasing.

DO NOT touch:
- sources/ (anything — wiki source data, chapters, raw books all off-limits)
- /Users/mnoth/source/asoiaf-chat/working/worklog-archives/* (historical)
- /Users/mnoth/source/asoiaf-chat/working/session-details/* (historical)
- /Users/mnoth/source/asoiaf-chat/progress/continue-prompts/archive/* (historical)
- /Users/mnoth/source/asoiaf-chat/working/chat-ui-architecture.md (being archived in Scrub A — do not edit before or after)

Final verification: from /Users/mnoth/source/asoiaf-chat run:
grep -rEni "copyright|copyrighted" --include="*.md" \
  --exclude-dir=sources \
  --exclude-dir=working/worklog-archives \
  --exclude-dir=working/session-details \
  --exclude-dir=archive \
  --exclude-dir=<sketches-archive-basename-from-Q1> \
  .

Expected remaining hits (all OK):
- this handoff file itself (will be archived in Phase 4)
Anything else: report and stop. Do not auto-edit.

Report: files edited (one-line summary per file), files deleted, final grep output.
```

**For citation-validator re-run** (dispatch with `subagent_type=citation-validator`):
```
Re-run the citation audit on the full 5-book corpus. Pass 1 is now 344/344 across all 5 main books (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73). Previously-deferred chapter-cite checks for missing chapter files should now resolve. Standard dated report to <Q10-location-or-default>.
```

**For model-fit audit** (dispatch with `subagent_type=general-purpose`, only if Q8=(a)):
```
Audit /Users/mnoth/source/asoiaf-chat/.claude/agents/*.md. For each agent prompt, recommend the cheapest viable model (Opus 4.7 / Sonnet 4.6 / Haiku 4.5) for what the prompt actually does. Apply the model-fit policy: cheapest model that can do the job; Opus only when reasoning depth genuinely requires it; smoke-test before upgrading.

Output a markdown table to /Users/mnoth/source/asoiaf-chat/working/model-fit-audit-2026-05-06.md:
| agent name | current model assumption | recommended model | one-sentence rationale | suggested smoke test |

Do NOT modify any agent prompts. This is a recommendation-only pass; Matt reviews before any frontmatter changes.
```

---

Do not write a worklog entry or session-details file for this handoff session itself — Matt indicated traditional updates happen at session end via the normal flow.
