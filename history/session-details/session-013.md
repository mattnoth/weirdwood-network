# Session 013 — Remote Added, Track B Sequencing Decision, Orchestration Planning Continue Prompt (2026-04-25)

## Type

Mostly **decisions / planning** — short execution but two strategic calls (sequencing Track B before v3 schema review; deferring relational DB) that needed durable persistence across sessions.

## Arc

### 1. Remote setup
Matt asked to add `https://github.com/mattnoth/weirdwood-network.git` as origin. No prior remote configured. Single command, verified with `git remote -v`. Repo now publishable.

### 2. Worklog size — confirm keep
Matt flagged worklog at 261 lines and asked whether to keep it that large. Breakdown:
- Header + intro: ~28 lines
- Current State: ~60 lines (lines 29-89)
- Active Decisions: ~32 lines (lines 91-122)
- Ideas & Backlog: ~30 lines (lines 124-154)
- Session Log: ~91 lines (lines 156-247) — sessions 8-12 only, sessions 0-7 already archived
- Principles: ~12 lines (lines 251-262)

CLAUDE.md's archiving threshold (~150 lines) is for the Session Log section specifically, not the whole worklog. Session Log is at 91 — under threshold. The bulk of the file is persistent context that loads every session and is load-bearing for orchestration. Confirmed: keep as-is.

### 3. README sources note
Matt: "For the instructions on sources folder, assume user will have access to the completed chapter splits, raw, wiki." Interpretation: the README walks through placing `.txt` files (step 2) and running the splitter (step 3), but for users provisioned out-of-band with the full sources tree, those steps are noise.

Decision: don't remove steps 2-3 (still correct for first-run users), but add a skip-ahead note at the top of step 2: *"Already have `sources/raw/`, `sources/chapters/`, and `sources/wiki/` populated? Skip to step 4 (`weirwood check`)."* Single-line addition. Preserves both audiences.

### 4. Next-step decision — Track B vs. schema review
Matt offered three options:
1. Examine latest AGOT v3 mechanical extraction, dig into schema
2. Compare v3 against archived v1/v2 mechanical extractions
3. Switch to Track B (wiki infobox parser)

Initial recommendation: combine 1+2 (open one chapter side-by-side across versions, ~15 min). Logic was: cheap validation before scaling v3 to 272 more chapters.

Matt pushed back: "why that before the wiki work?" — first-pass answer was about cost asymmetry (cheap schema check before expensive Track B sprint).

Matt followed up: "will the wiki pass inform the schema review?" — this reframed everything. The question wasn't "which is faster," it was "which produces more decision-relevant signal."

The honest answer: yes, Track B materially informs schema review. Building the wiki parser surfaces:
- **Entity type boundaries**: wiki categories are an external taxonomy. Mismatch with the 12 Pass 1 categories is a schema signal.
- **Relationship/edge shape**: infobox fields (`spouse`, `father`, `liege`, `culture`, `religion`) define the graph's relationship vocabulary. Gaps in Pass 1's relationship extraction surface here.
- **`first_available` mechanics**: `cite_ref` chapter anchors are the spoiler-gating primitive. The parser proves whether the encoding is reliable.
- **Schema redundancy**: if the wiki provides house words / sigils / seats reliably, Pass 1 doesn't need to extract them. Track B can *shrink* the Pass 1 schema.

Schema review in isolation only answers "did the agent follow the prompt." Track B answers "is the prompt asking for the right things."

Cost asymmetry flips when you account for re-runs: schema-first risks discovering Track B reshapes it → 272 chapters re-extracted. Track-B-first costs queued work that was on the roadmap regardless.

**Decision: Track B first, schema review after, then scale v3.** Persisted to:
- `worklog.md` Active Decisions: new DECIDED entry "Track B (Wiki Parser) Before v3 Schema Review"
- `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`: "Why Track B Before v3 Schema Review" rationale section prepended
- `working/todos.md`: AGOT v3 schema review item flagged as sequenced-after-Track B

Big call, multiply persisted so future sessions discover it from any entry point.

### 5. /install-github-app and relational DB questions
Matt asked about both during endsession prep.

**GitHub app:** Helpful for collaboration (@claude in PRs/issues from GitHub UI), low immediate value for solo CLI work. Skip for now; revisit when collaborators arrive.

**Relational DB:** Not needed. Reasoning:
- Pass 2 output is ~5,279 wiki entities + ~17K cite_ref records. Fits trivially in JSONL/markdown.
- Current access patterns ("find entity X", "find edges of type Y", "filter by `first_available`") are served by JSONL + Python or markdown + grep.
- Graph DB (Neo4j) becomes useful for traversal queries ("characters within 3 hops of Jon Snow appearing before AGOT Bran III") — still 1-2 passes away.
- The Active Decision in worklog (`OPEN: Storage Format`) already leans markdown-first.
- Migration cost from JSONL → SQLite → Neo4j is low because parser output is structured. Defer the choice without painting into a corner.

Decision documented inside the new orchestration planning continue prompt as a constraint: "no relational database for now" with explicit revisit trigger ("only escalate if a Pass 2 access pattern is genuinely painful without one — and document the trigger").

### 6. Track B orchestration planning continue prompt
Matt's framing for next session: "PLAN the multi agent orchestration of the wiki analysis (as it is quite large) - we can use a combination of multiple terminals for concurrent agents, sub agents for those, log files, etc. I want similar functionality that the extraction stats uses - token usage, time, interleaving (if necessary) - all the metadata about the PROCESS organized to prevent drift as much as possible."

This is a real concern. The 17,657-page wiki cache dwarfs the chapter extraction (344 chapters). Single-shot processing will drift, lose context, waste tokens. The extraction pipeline's wave model (`weirwood`) solved this for chapters; Pass 2 needs an analog.

Created `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` as a **PLAN-ONLY** prompt. Constraints:
- No code, no scraping, no agent dispatch this session
- Output: `working/runbooks/wiki-pass2-orchestration.md` covering 7 numbered design areas
- Mirror extraction-stats CSV shape (timestamps, durations, token columns, cost) — same observability transfers
- Stay within `weirwood`-style pipeline shape — Pass 2 should feel sibling to extraction, not bespoke
- No DB unless explicitly justified by a painful access pattern

The 7 design areas the runbook must cover:
1. Work decomposition (deterministic vs. agentic)
2. Concurrency model (tabs vs. subagents vs. hybrid)
3. Drift prevention (logging, checkpoints, validation gates)
4. Process metadata schema (mirroring extraction-stats)
5. Resumption (wave-equivalent state machine)
6. Failure modes (rate limits, malformed pages, classification ambiguity)
7. Storage decision revisit (markdown + JSONL default)

Open questions surfaced for Matt in the prompt rather than pre-decided:
- Sub-agents vs. fresh-agent-per-tab
- Batch granularity (per-page too small, per-category uneven, hybrid likely)
- Confidence tiering: per-page agent call vs. category metadata heuristic
- Promotion criteria: density signals + human-in-the-loop?

This explicitly *gates* the existing Track B parser continue prompt — implementation can't start until orchestration is designed.

Linked from `working/todos.md` under Wiki / Pass 2 Prep, ahead of the parser todo.

### 7. Three additional notes added (post-endsession round)

After the first endsession pass, Matt added three items to capture before commit:

**(a) Relational DB reasoning → scratch-notes.md.** The DB-deferred decision was already inside the orchestration planning continue prompt as a constraint, but Matt wanted the reasoning surfaced separately in `progress/scratch-notes.md` so future-Matt or a collaborator can find the *why* without reading a continue prompt. Same content as the prior decision, formalized as a scratch entry.

**(b) Collaborator may join → schema lock-in becomes a hard gate.** New context: a collaborator may join to share extraction load — effectively running concurrent extraction agents from another machine. They have less ASOIAF depth than Matt, don't remember the books in detail, and haven't done the theory research. Implication: the schema must produce correct output without lore knowledge to second-guess it.

This reinforces Track B sequencing (schema review *after* wiki parser is more important when a non-expert will run the schema across more books) and raises the value of `/install-github-app` (Claude tagging in PRs becomes the natural review surface for collaborator-produced extractions).

Captured in:
- `progress/scratch-notes.md` — "Collaborator Onboarding — Schema Lock-In Before Handoff" entry
- `working/todos.md` — new Collaboration section: schema lock-in todo, GitHub app revisit todo, collaborator quick-reference doc todo
- Sequencing in worklog Session 13 "What's next"

**(c) Pass 4 (foreshadowing) prep — long-lead reminder.** Matt flagged: by the time we get to Pass 4 (many sessions away), we need (i) an expanded foreshadowing events list and (ii) a richer Chekhov's gun *pattern library* — not just a list of guns, but the textual patterns that signal "this matters later." The pattern library is what lets the scanner flag *unknown* candidate foreshadowing rather than only matching against named events.

Filed before forgetting:
- `progress/scratch-notes.md` — "Foreshadowing Pass Prep — Expand Event List & Chekhov's Guns" entry with concrete event categories (deaths, identity reveals, plot reveals, magic returnings, prophecy fulfillments) and the pattern-library design (setup → payoff shape → textual signal)
- `working/todos.md` — new reference-files-to-create entry pointing to the scratch note for full detail

## Files Changed

| File | Change |
|------|--------|
| `git remote` | Added `origin → https://github.com/mattnoth/weirdwood-network.git` |
| `README.md` | Added skip-ahead note at step 2 for users with pre-populated `sources/` |
| `worklog.md` | New DECIDED: "Track B (Wiki Parser) Before v3 Schema Review"; Session 13 entry |
| `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` | Prepended "Why Track B Before v3 Schema Review" rationale section |
| `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` | NEW — PLAN-ONLY orchestration design prompt |
| `working/todos.md` | New top-priority todo for orchestration planning; v3 schema review flagged as sequenced-after-Track B; parser todo flagged as gated on orchestration runbook; new Collaboration section (schema lock, GitHub app, quick-ref doc); new foreshadowing reference-expansion todo |
| `progress/scratch-notes.md` | Three new entries: "Relational DB Decision — Defer", "Collaborator Onboarding — Schema Lock-In Before Handoff", "Foreshadowing Pass Prep — Expand Event List & Chekhov's Guns" |

## Surprises / Process Notes

- The "will the wiki pass inform the schema review?" question was the inflection point. Without it, the recommendation would have stayed at "schema review first." It's a good example of a user question reframing a recommendation that was internally consistent but optimizing the wrong axis (speed of validation, not signal quality of validation).
- The orchestration planning continue prompt deliberately separates *planning* from *implementation*. Track B already had a continue prompt for the parser script, but that prompt assumed single-script execution. The orchestration question makes that assumption invalid for Pass 2 (the wiki ingestion that follows the parser). Two prompts now:
  - `2026-04-25-track-b-orchestration-planning.md` (next session, plan only)
  - `2026-04-24-track-b-wiki-infobox-parser.md` (gated, implements one piece of the plan)
- The DB-or-not question is the kind of upfront-architecture call that's tempting to over-engineer. Defaulting to "no DB, escalate when painful" is correct: the migration path is cheap from JSONL forward.

## What's Next

1. **Next session:** Run `2026-04-25-track-b-orchestration-planning.md`. Output the runbook.
2. **After runbook:** Implement deterministic Track B parser per the runbook's design (will probably reuse most of `2026-04-24-track-b-wiki-infobox-parser.md`).
3. **After parser:** Schema review of AGOT v3 (informed by what wiki actually covers).
4. **Then:** Scale v3 to ACOK / ASOS / AFFC / ADWD via existing `weirwood` pipeline.

## Open Threads (Carry Forward)

- Storage format (markdown vs. graph DB) — leaning markdown; defer until Pass 2 access patterns clarify; explicit reasoning saved to scratch-notes
- `/install-github-app` — skip for now, value rises when collaborator joins (PR review surface for collaborator-produced extractions)
- Descriptive chapter title mapping (THE PROPHET → Aeron etc.) — still OPEN, unblocked by Track B
- Collaborator onboarding — schema must be ironclad before handoff; sequence: Track B → schema review → schema lock → quick-ref doc → invite
- Pass 4 foreshadowing prep — long-lead, expand events list and build Chekhov's gun pattern library before running scanner
