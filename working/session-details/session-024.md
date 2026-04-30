# Session 24 — Stage 2 Cold Review + Stage 3 Pipeline Redesign (2026-04-27)

**Type:** Design session — overturned a remediation decision mid-session, redesigned Stage 3 pipeline from agent-does-everything to Python-first / Agent-prose-only.

**Outcome:** Stage 3 plan now has a clean Python-before-Agent split. `first_available` is fully shelved. Edge discovery is its own future pass. Two new continue prompts (stage3-prep, stage4-edge-discovery) and one new canonical runbook (wiki-pass2-pipeline.md) replace the prior strategy.

---

## Arc

### Phase 1: Stage 2 cold review (delegated)

Matt opened the session with the queued pickup: run `progress/continue-prompts/2026-04-27-wiki-pass2-core-review.md` as a fresh-Claude cold review of Wiki Pass 2 core output, no carry-over context. I had read the worklog narrative as part of CLAUDE.md's "First Steps" orientation, which biases the cold-read. Flagged that explicitly to Matt with three options: delegate to a fresh general-purpose agent, do it here despite bias, or have Matt start a new conversation. Matt chose delegate.

Spawned a general-purpose subagent with a tight prompt: read continue prompt + handoff runbook + architecture spec, do NOT read worklog or session-detail files, sample 15-20 nodes, score, decide proceed/remediate/escalate, write the corresponding handoff prompt. Bias-resistance instructions made the launching Claude's framing ($1,200 cost projection, 67 bulk-resolved questions, 52 conflicts) explicitly subject to the agent's judgment rather than facts to accept.

Agent came back **`remediate`** with three findings:

1. **HIGH — `first_available` schema drift.** 4 different shapes across 855 nodes (block-object 453, null 239, "always available" 69, string-form 21, prefixed 15, **absent entirely 58**). Validator explicitly excludes the field from checks.

2. **HIGH — Silent parser-bug propagation.** Tyrion and Varys both have `first_available: ADWD chapter 1`. Both are AGOT POVs from chapter 1. The agent self-correction rule (set to "always available" when notice parser is wrong) misses cases. 67 of 74 filed questions were this same bug pattern; an unknown number of major characters have wrong values silently.

3. **GOOD — Cost-per-bucket framing was misleading.** Per-node cost is $0.111, *better* than the direwolves baseline ($0.19/node). The "$2.58/bucket vs $1 projected" framing was bucket-size scaling, not waste. Slug rename rate 0%, conflict mechanism worked, edge yield 5.83/node mean. Independent verification of the launching Claude's framing.

Agent wrote `progress/continue-prompts/2026-04-27-wiki-pass2-core-remediation.md` with three mechanical fixes: canonicalize `first_available` shape, audit-and-fix wrong values via cite_ref comparison, validator enforcement.

### Phase 2: Matt overturns the remediation decision

Matt's response shifted the entire strategy: **shelve spoiler gating until post-first-release.** Reasons compressed: the field has been a problem the whole project, every session reasoning about it burns context for diminishing returns, and the wiki cite_ref data is rich enough that a deterministic backfill script can populate the field across the whole corpus in one pass after Pass 1 finishes all 5 books.

This contradicted the long-standing "DECIDED: Spoiler Gating Architecture" position from project inception ("`first_available` field is required on every node from the start. Not retrofittable."). Matt's reasoning: that decision was made before we knew how thin the consumer of the field actually was in v1, and the wiki data is structured enough that retrofitting deterministically is cheap.

I clarified the Tyrion/Varys "parser-bug class" framing — the wiki-infobox-parser derives `first_available` from the lowest-numbered cite_ref anchor; for some pages (footnotes reordered during wiki edits) that produces a wrong answer. Not Tyrion's data being wrong on the wiki — our parser misreading the wiki's footnote structure on a page class.

Matt's directive: don't fix Tyrion/Varys manually. Don't reason out individual values. Null them, document in `## Notes` for the future backfill script, move on.

### Phase 3: Cost reduction framing

Matt's bigger concern was time/cost on the 472 secondary buckets, not schema correctness on a deferred field. He asked: can we triage by titles? Use the wiki HTML structure to organize buckets and create a priority order?

I confirmed Track B already has the data (`page-index.jsonl` 17,657 lines + `infobox-data.jsonl` 5,279 lines) — no re-scrape needed. Proposed three tiers:
- **A** — page named in any Pass 1 extraction OR ≥5 chapter cite_refs
- **B** — has infobox but no chapter mentions
- **C** — no infobox + no cite_refs

Estimated Tier A is ~30-40% of pages, cuts cost dramatically.

Matt's response added: keep Tier B/C, never drop sources, label Tier B with `has_infobox: true`, route Tier C to a "remaining" bucket. **Hard rule: never drop anything from sources.** Asked me to clean up first_available context/memory before starting any script.

### Phase 4: Cleanup pass (no script yet)

Executed a coordinated set of edits to bring the entire repo's representation of `first_available` in line with the deferral:

- Tyrion & Varys nodes: nulled `first_available` in frontmatter; updated `## Notes` on Tyrion to flag the parser bug for the future backfill script.
- `reference/architecture.md`: rewrote the Spoiler Gating section with a prominent DEFERRED status banner. Kept the wiki data sources documentation (Books field + cite_ref anchors) so the backfill script can use them.
- `CLAUDE.md`: replaced "every node/edge must have a `first_available` field — architectural, not optional" with a soft deferral note. **Also added** a new "Critical Rule: The Wiki Is Already Local — Never Re-Fetch" block at the same severity as the copyright rule, explicitly forbidding HTTP / WebFetch / curl / Playwright.
- `worklog.md`: flipped "DECIDED: Spoiler Gating Architecture" to "DEFERRED: Spoiler Gating to Post-First-Release (2026-04-27)" with full supersession context.
- `working/todos.md`: replaced Stage-2 remediation entry, expanded the spoiler-gating-backfill todo with concrete script design.
- `.claude/agents/wiki-ingester.md`: dropped the "agent self-corrects to `always available`" override rule. Field now: do not emit, do not derive, do not file questions.
- `progress/continue-prompts/2026-04-27-wiki-pass2-core-remediation.md`: archived (superseded).
- New memory: `feedback_first_available_deferred.md` (typed: project) with the deferral rule and rationale.

### Phase 5: Page-kind enum design

Matt asked about adding a `page_kind` enum to manifests so v2 can route stub/redirect/list pages deterministically. I scoped it to **Tier C only** — Tier A/B pages are dominantly `entity`, and adding a default-valued field to obvious entities adds zero query value while bloating the schema. Tier C gets `redirect / disambiguation / list_article / year_article / stub / entity` derived from cached HTML byte_size and pattern matching on body content. Flagged the redirect-detection feasibility question as a 5-minute task for the next agent (depends on whether the Playwright scraper preserved redirect markup or only followed redirects to destinations).

### Phase 6: Pipeline redesign — Python before Agent

Matt asked the question that reshaped Stage 3: "if we have infoboxes, won't a python script do for that?"

Reframing: the 5.83 edges/node mean from Stage 1 came mostly from infobox fields — deterministic data. Running an LLM agent against 5,000+ secondary pages to extract that is wasted cost. Paths considered:
- A: Keep agent-does-everything for Tier A, Python skeleton for Tier B
- B: Python skeleton for both tiers; agent fills prose body for Tier A only

I went with B as the recommendation. Cleaner separation, uniform skeleton, narrower agent role, byte-identical edges across runs, easy validator enforcement (edge byte-equality check between Python skeleton and agent output).

Matt asked the follow-up: "should we start with all Python before we kick in agent reasoning? I don't suggest we reason for both nodes and edges in the same pass, UNLESS you tell me that is a better strategy."

I confirmed: yes, Python-first for both tiers is the better strategy. The bucket-isolation argument doesn't apply to Python (the data is global JSONL); the agent's job becomes purely prose synthesis. **Edge discovery — both prose-derived single-page edges and cross-page edges — becomes its own later pass**, sequential to Stage 3, never parallel.

Matt added a missing step: **a mid-stage agent review between Stage 3a (Python emission) and Stage 3b (agent prose-fill).** Quality gate. Spot-check Python-emitted nodes for edge correctness, type-guess accuracy, citation format. Surface issues as a review report; do not modify nodes. This catches Python bugs before they propagate through Tier A's agent runs.

Matt also stated as a default rule: "Python before Agent." Everywhere going forward, not just Pass 2. Saved as memory entry `feedback_python_before_agent.md`.

### Phase 7: Old-strategy archival

Matt directed: "make sure all references to other strategies for this stage of Track B is archived." Audit:
- Two review docs (`wiki-pass2-orchestration-review.md`, `wiki-pass2-orchestration-build-self-review.md`) reviewed the now-superseded design. Moved to `working/runbooks/archive/`.
- `wiki-pass2-orchestration.md` (707 lines): kept in place. Bundle/validator/conflict mechanics still apply. Added a SUPERSEDED-FOR-STAGE-3 banner pointing to the new pipeline doc.
- `wiki-pass2-tier-handoff.md`: kept in place. Stage 1/2 history accurate. Added a SUPERSEDED-FOR-STAGE-3 banner.
- New canonical runbook: `working/runbooks/wiki-pass2-pipeline.md` (slim, focused on the Python-first pipeline + tier definitions + bucket preservation rules).
- New continue prompt: `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md` rewritten from scratch to reflect the new pipeline. The earlier draft (Tier A agent does everything) was overwritten.
- New continue prompt: `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — skeleton for the future prose-derived edge discovery pass with Matt's reasoning kept verbatim.

### Phase 8: Bucket preservation + Playwright cleanup

Matt asked whether the 37 core bucket bundles were preserved. Verified: all 37 have `bucket_input.json`, `manifest.json`, `tmp/<slug>.node.md` files, and `validator-report.json` intact. Codified the preservation rule into the new pipeline doc: launcher must keep these post-promotion. Reason: Stage 4 reads bundles + agent prose to find prose-derived edges; re-runs need bundles intact; post-release backfill needs track_b rows.

Matt asked whether Playwright was uninstalled (he ran `pip3 uninstall` earlier). Verified: gone. `pip3 list` returns no playwright, `which playwright` returns nothing, `~/.cache/ms-playwright` doesn't exist.

### Phase 9: /endsession customization

Matt asked to add a copy/paste handoff block to /endsession so he can pass it directly to a fresh agent without manually composing a handoff. Added as Step 9 to `.claude/commands/endsession.md`: a clearly-delimited block with `/continue {prompt-name}`, active work track, last session, key reads, open questions, and "DO NOT" rules. Self-contained for fresh-Claude pickup.

---

## Decisions made (durable)

1. **Spoiler gating deferred to post-first-release.** Field optional in v1; existing values may be wrong/missing/inconsistent. Backfill via deterministic Python script after Pass 1 completes all 5 books. (Memory: `project_first_available_deferred.md`. Architecture.md + CLAUDE.md updated.)

2. **Python before Agent — default rule.** Whenever a deterministic Python step can produce part of an output, it runs first. Agents only do reasoning work. Applies project-wide. (Memory: `feedback_python_before_agent.md`.)

3. **Stage 3 pipeline:** Priority script → Stage 3a Python emit (skeleton + edges) for all Tier A+B → mid-stage agent review → Stage 3b agent prose-fill on Tier A only. Tier C deferred. Tier C only gets `page_kind` enum.

4. **Edge discovery is its own pass (Stage 4).** Sequential to Stage 3, never parallel. Pipeline shape TBD; flesh out when Stage 3 finishes.

5. **Never drop anything from sources.** Tier C pages, redirect pages, stub pages, list articles all stay. Source data is read-only and additive-only. Bucket bundles preserved indefinitely.

6. **Wiki cache hardline elevated.** "Never re-fetch the wiki" promoted to a CLAUDE.md Critical Rule alongside the copyright rule. Same severity language. Explicit list of forbidden paths (HTTP / WebFetch / curl / Playwright / requests).

7. **/endsession outputs handoff block.** Step 9 added: copy/paste-ready text for fresh-Claude resumption.

---

## What surprised me

- **Bias from the orientation step.** Reading the worklog as part of standard project orientation primed me with the launching Claude's framing before the cold review. Flagging it openly let Matt route around it via subagent delegation. Worth documenting as a pattern: when a continue prompt explicitly asks for cold context, the orchestrator should delegate rather than try to "forget" what was just read.

- **The "$2.58/bucket vs $1 projected" framing was real but misleading.** The launching Claude's cost concern was honest but framed in a way that scared the wrong direction. Per-node cost is healthy. The independent agent verification was worth the delegation cost just to reset the framing.

- **The Stage-2 decision being overturned the same session it was made.** This isn't a process failure — Matt has more context about what's load-bearing for v1 than the agent. The deferral decision is correct because v1 doesn't expose spoiler gating to users; the architecture rule was forward-looking and outpaced the actual product. Worth noting that "agents propose, Matt decides" worked exactly as intended here.

- **The Python-first redesign came from a single Matt question.** "If we have infoboxes, won't a python script do for that?" reframed the entire Stage 3 pipeline. The 5.83 edges/node figure had been sitting in the Stage-1 stats the whole time but I'd been treating it as a quality metric rather than a redundancy signal. Worth remembering: high deterministic yield is a flag that the agent layer is doing data-extraction work that should be Python.

---

## Open items the next session inherits

- Build `scripts/wiki-pass2-prioritize.py` (priority labeling, Tier A/B/C + has_infobox + page_kind for C only)
- Build `scripts/wiki-pass2-emit-deterministic.py` (Stage 3a Python emission for all Tier A+B)
- Run a mid-stage agent review of Stage 3a output
- Rewrite `.claude/agents/wiki-ingester.md` to v2 prose-only role (forbidden from emitting/modifying edges or frontmatter)
- Update `scripts/wiki-pass2-validator.py` to enforce edge byte-equality between Python skeleton and agent output
- Verify whether Playwright preserved redirect markup or only followed redirects (5-minute task; affects Tier C `page_kind` distribution)
- Stage 4 detail design (edge discovery), to be written when Stage 3 finishes

All captured in `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md` for next-agent pickup.
