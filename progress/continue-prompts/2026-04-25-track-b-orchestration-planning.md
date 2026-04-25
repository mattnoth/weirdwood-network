# Continue Prompt: Track B — Orchestration Planning Session

> Created: 2026-04-25 | Predecessor: `2026-04-24-track-b-wiki-infobox-parser.md`
> Mode: **PLAN ONLY** — design the orchestration before writing code or running anything

## Why This Prompt Exists

The single-script Track B continue prompt (`2026-04-24-track-b-wiki-infobox-parser.md`) describes *what* to extract from the wiki cache. It assumes a single Python script processes all 17,657 JSON files end-to-end. That's fine for the deterministic infobox/cite_ref parsing, but Pass 2 of the pipeline — **wiki ingestion into structured graph nodes** — is much larger:

- ~5,279 pages with infoboxes (deterministic parsing)
- ~17,000+ pages with cite_refs (deterministic regex)
- An unknown subset that needs **agentic** processing: classification, disambiguation, summarization, confidence-tier assignment, deciding whether to promote into `graph/nodes/`

The agentic subset is where this orchestration plan matters. Single-shot processing of thousands of pages will drift, lose context, and waste tokens. The extraction pipeline solved this for chapters via `weirwood`'s wave-based parallel terminal model. Pass 2 needs an analogous design.

## Goal of the Planning Session

Produce a written orchestration plan in `working/runbooks/wiki-pass2-orchestration.md` covering all of:

1. **Work decomposition** — what is deterministic (Python only) vs. what is agentic? What are the natural batch units (per-page, per-category, per-entity-type, per-letter)?
2. **Concurrency model** — multiple iTerm tabs, each running an agent? Subagents inside a parent agent? Mixed (parent dispatches batches, sub-agents process)? What's the analog of a "wave" for wiki ingestion?
3. **Drift prevention** — wiki is much larger than chapter extraction. What logging, checkpoints, and validation gates prevent silent corruption or partial output?
4. **Process metadata schema** — same observability as `working/extraction-stats/`: per-batch token usage, duration, input/output/cache tokens, cost. CSV format consistent with `extraction-stats-{book}-pass1-v3.csv`.
5. **Resumption** — wave-equivalent for wiki: how does a relaunch detect what's done and pick up the rest? What's the on-disk state machine?
6. **Failure modes** — rate limits, malformed pages, classification ambiguity, network issues. Rules for halt vs. skip vs. mark-and-continue.
7. **Storage decision (revisit)** — current lean is markdown + JSONL (no DB). Confirm or escalate based on the access patterns Pass 2 actually needs. See worklog "OPEN: Storage Format" decision.

## Constraints to Respect

- **No code in this session.** Plan only. Code happens in a follow-up session against the resulting runbook.
- **Don't run anything against the wiki cache yet.** No exploratory scripts, no agent dispatches.
- **Stay within the existing pipeline shape.** `weirwood` is the extraction launcher pattern. Pass 2 should feel like its sibling, not a one-off bespoke flow. If a deviation is justified, name it explicitly.
- **Process metadata must mirror extraction-stats.** Same column shape (timestamps, durations, token counts, cost) so existing tooling and reporting habits transfer. CSV is `working/extraction-stats/wiki-pass2-{batch-id}.csv` (or similar — finalize in plan).
- **No relational database for now.** Track B (parser) outputs JSONL. Pass 2 outputs markdown nodes + JSONL/CSV process logs. Revisit DB only if a Pass 2 access pattern is genuinely painful without one — and document the trigger.

## What to Read First

1. `worklog.md` — full project state, especially:
   - DECIDED: "Track B (Wiki Parser) Before v3 Schema Review" (2026-04-25)
   - DECIDED: "Wiki Ingestion Scope — Full Crawl, Then Triage"
   - OPEN: "Storage Format — Pure Markdown vs. Graph DB"
2. `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` — the deterministic-parser scope
3. `reference/architecture.md` — entity hierarchy, edge taxonomy, wiki-infobox→edge mapping, spoiler gating
4. `scripts/extract.sh` — extraction launcher: waves, stats CSV emission, rate-limit detection, soft-stop, resumption — this is the model to mirror
5. `scripts/weirwood.zsh` — shell-function wrapper for `extract.sh`. Same pattern likely applies to wiki Pass 2.
6. `working/extraction-stats/extraction-stats-agot-pass1-v3.csv` — column shape to copy
7. `.claude/agents/wiki-ingester.md` — current stub for the Pass 2 agent (prompt not written yet)
8. `sources/wiki/_raw/` directory listing only — do NOT process pages in this session

## Deliverable

A single file: `working/runbooks/wiki-pass2-orchestration.md` covering each of the 7 numbered items above. Each section should answer "what's the design?" *and* "why this over the alternative?" Plan should be concrete enough that a follow-up session can implement it without re-deciding.

When the plan is written, update `working/todos.md` with a new actionable item: "Implement wiki Pass 2 orchestration per runbook" and create the implementation continue prompt.

## What NOT to Do

- Don't write Python or shell scripts.
- Don't dispatch agents or scrape the wiki cache.
- Don't design the wiki-ingester agent prompt itself — that's downstream of the orchestration plan.
- Don't pick a relational DB. The default is no DB; only escalate with explicit justification tied to a Pass 2 access pattern.
- Don't expand scope: this plan covers Pass 2 wiki ingestion orchestration. It does NOT cover Pass 3+ orchestration, even if patterns will be reused.

## Open Questions for Matt (Surface in the Plan, Don't Pre-Decide)

- Are sub-agents inside a parent agent worth the context cost vs. multiple iTerm tabs each running a fresh agent? (extraction uses tabs; pros/cons differ for wiki because batch sizes are smaller and more numerous)
- What's the right batch granularity? Per-page is too small (orchestration overhead dominates), per-category may be uneven (wiki has huge category-size disparities). Probably a hybrid.
- Confidence tiering: wiki mixes canon (Tier 1), inferred-by-fans (Tier 3), and theory (Tier 4) on the same page. Is that a per-page agent decision or driven by category metadata?
- How do we decide what gets promoted into `graph/nodes/` vs. left in the cache? Density signals (length, infobox richness, cite_ref count) are mechanical, but final promotion may need human-in-the-loop curation.
