# SESSION 189 — Query & traversal layer: the master design document
> **This is Session 189.** Stamp your worklog entry `### Session 189` at endsession.

**Track:** meta/graph (design). **Recommended model: Opus 4.8 at the HIGHEST reasoning effort
available (xhigh/max).** Matt: "a super high reasoning model for designing." This is a THINKING
session.

**Mandate (Matt, S188 endsession):** produce a **thorough design document** for the query/
traversal layer, planned so **mechanical agents know exactly what to do**. Be thorough, weigh
options, think ahead to where this is going, and **think of things we haven't** — the graph-
traversal script library, the missing pieces, all of it.

**Explicitly (Matt): a core part of your job is to find what we are MISSING** — gaps in the
analysis, node/edge/data-model coverage the graph lacks, use-cases nobody has designed for,
capabilities the query layer should have and doesn't, whole areas the prior session didn't see.
Don't just refine the existing list; hunt for its blind spots.

**How you may work (you don't have to do all the grunt-work yourself):** you are the expensive
reasoning model — spend your budget on DESIGN, and **fan out cheaper subagents (Sonnet, or Haiku
for the simplest jobs) for the mechanical parts** where it helps: reading `graph-query.py` and
enumerating every mode + exact behavior, verifying a claim in the docs against the real code,
censusing the graph, surveying what a node type actually contains, checking whether the TS bundle
carries a given field, etc. Delegate the reading/verification; keep the reasoning. (Model-fit
rule: cheapest model that can do the sub-task; paste the glossary terms into any subagent you
spawn — they don't load CLAUDE.md. Stay within the design-only guardrails below — subagents READ
and REPORT; they do not mutate the graph or build.)

## Your latitude — READ THIS FIRST

**Nothing below is settled. It is INPUT to pressure-test, not a spec to implement.** A prior
session (S188, Opus but a normal reasoning pass) produced the analysis in `GRAPH-QUERY-ROADMAP.md`
+ `GRAPH-STATE.md`: a gap list (G1–G10), a set of directions (D1–D8), and a framing ("two
apertures / essential-vs-incidental shrink"). **You are explicitly expected to find better
alternatives, reframe the problem, reprioritize, merge or discard items, and reject any diagnosis
you find weak.** Matt's words: *"the plan may think of better alternatives — the continue should
not force anything on the next model."* So:
- Treat G1–G10 / D1–D8 as one session's hypotheses. Confirm, revise, or overturn them against the
  real code + data. Where you disagree, say so and design your way, not mine.
- The list of "areas in play" further down is a **prompt for coverage, not a table of contents you
  must fill in order.** Restructure freely. Add areas nobody has named. Cut ones that don't earn
  their place — but say why you cut them.
- If a genuinely better shape for the whole thing exists, propose THAT. Don't anchor on the
  existing docs' structure; you may replace it.

The only things you may NOT change are the hard constraints at the very bottom. Those are
**governance** — what this session is permitted to DO (design vs. build, mutate the graph, spend
on an LLM pass, end the session). Governance is Matt's; the analysis is yours. Rewrite any
diagnosis or solution freely; don't touch what the session is allowed to do.

## Orient yourself (read, then judge for yourself)

- `GRAPH-QUERY-ROADMAP.md` + `GRAPH-STATE.md` (top level) — the S188 analysis. Read critically.
- `history/session-details/session-188.md` — the narrative + the live-UI failure it reproduced
  (a meals question → ~13 fuzzy/no-match resolves → loop-bound, no answer). Verify the claim holds.
- The actual code: `scripts/graph-query.py` (~11 query modes) · `scripts/event_alias_resolver.py`
  · `web/src/lib/*` (the TS port — exposes ~5 modes) · `web/netlify/edge-functions/lib/agent.ts`
  (the 5 chat tools + system prompt) · `working/todos.md` Track 7. **Ground your design in what the
  code and the graph actually are — not in the prior session's summary of them.**

## Areas likely in play (a checklist for *coverage*, not a script — reframe as you see fit)

Use these to make sure the design isn't blind to something, then organize however is best:
- **Where this is going.** The end-state vision — the graph + a documented query layer that both a
  CLI and the chat-UI speak. Anchor the plan to a destination, not just a gap list.
- **Content-first retrieval.** The chat can't search content, only resolve names — the root of the
  live failure. What's the right retrieval model? (index over quotes vs. chapters vs. both; keyword
  vs. embeddings; build-time vs. request-time given the Edge CPU budget.) Options + a call.
- **The traversal script library.** Its organization and whether the Python CLI and the TS chat
  tools should unify behind one documented API (they've drifted — CLI has modes the chat lacks).
  This is Matt's interview centerpiece — legibility matters.
- **The descriptive layer.** ~96% of food/customs/materials nodes are edge-less orphans (captured
  by harvest, never wired). Is a descriptive edge grammar the right fix, or something better?
- **Resolver / discoverability, the slim bundle projection, chronology (incl. the open Step C wiki-
  date backfill — see GRAPH-STATE §5), and the parked/unbuilt pieces** (braid/convergence
  primitives, a routing/trigger index, TWOIAF ingestion, prophecy layer, an MCP server). Decide
  what's in this arc vs. parked — and whether any is a red herring.
- **Novel ground.** Spend the reasoning budget on what nobody has proposed yet.

## What the output must be (this part IS the ask)

- **A design document mechanical agents can execute** — not restricted to the two existing MDs.
  Create whatever structure serves best (e.g. `reference/design/…`, a new top-level plan, or a
  restructure). For each item you land on: concrete steps, exact files/scripts, inputs/outputs,
  success criteria, DO-NOTs, recommended model — and a **sequence** (dependencies, parallel-safe vs.
  serial) with a clear first move.
- **Options, not edicts.** For each major decision, give the alternatives you weighed and why you
  chose as you did — so Matt can overrule at the fork, not just at the end.
- Leave the doc set internally consistent; update the appendix/log of anything you touch.

## At endsession
- Worklog entry `### Session 189` (worklog.md, meta/graph). Update `working/todos.md` Track 7 to
  point at whatever design doc you produced. Commit docs only.

## Hard constraints — GOVERNANCE, not analysis (do NOT change these; the ideas above are all yours to rewrite, these are not)
- **Design only. Do NOT build** — no graph (`graph/`) mutation, no bundle rebuild, no `web/` /
  `scripts/` code changes. The deliverable is documentation/plan.
- **No invented edge types or vocabulary** without routing through `reference/architecture.md` +
  a worklog Active Decision. Keep the canonical vocab (Pass/Track/Tier + lowercase `step`); paste
  the glossary into any subagent you spawn (they don't load CLAUDE.md).
- **No Haiku/extraction/LLM pass** (incl. chronology Step C) without Matt's explicit OK — you may
  *design* it, not run it.
- Do not run `/endsession` without Matt's permission. Do not touch the top-level `scratch`/`scr`.
