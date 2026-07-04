# SESSION 189 — Query & traversal layer: the master design document
> **This is Session 189.** Stamp your worklog entry `### Session 189` at endsession.

**Track:** meta/graph (design). **Recommended model: Opus 4.8 at the HIGHEST reasoning effort
available (xhigh/max).** Matt's explicit call: "a super high reasoning model for designing." This
is a THINKING session — reason deeply, consider options, surface things we haven't thought of.

**Mandate (Matt, S188 endsession):** analyze the plans and produce a **thorough design document**
that plans the query/traversal layer so **mechanical agents know EXACTLY what to do**. Not limited
to the two markdown files — create whatever document structure serves the design best (a proper
design doc under `reference/design/`, a new top-level plan, restructured MDs — your call). The
plan should be **thorough**: weigh options, think ahead to where this is going, cover the graph-
traversal **script library**, the **missing pieces**, all of it. Design still — **do NOT build**
(no graph mutation, no feature code, no bundle rebuild). The deliverable is documentation/plan.

---

## What exists going in (read these FIRST)

- **`GRAPH-QUERY-ROADMAP.md`** (top level) — the forward-looking analysis: gaps **G1–G10**,
  directions **D1–D8**, the "two apertures / essential-vs-incidental shrink" framing, the LIVE-
  EVIDENCE exhibit (the meals question → 13 fuzzy/no-match resolves → loop-bound), the query-mode
  **divergence** table (chat exposes ~5 of `graph-query.py`'s ~11 modes), §4 script-org/interview
  framing, §8 prior-art.
- **`GRAPH-STATE.md`** (top level) — current state: census, the **descriptive-layer census §2a**
  (food 96% islanded; quotes 73% on characters / 3% descriptive; containers 100% events), the
  **harvest-mechanism root cause §2b** (descriptive material captured but never wired), §4 parked
  tracks, §4b backlog salvage, §5 live/next incl. the chronology/event-ordering status.
- **`history/session-details/session-188.md`** — the full narrative + all 7 findings.
- The actual code: `scripts/graph-query.py` (~11 modes), `scripts/event_alias_resolver.py`,
  `web/src/lib/*` (the TS port — ~5 modes), `web/netlify/edge-functions/lib/agent.ts` (the 5 chat
  tools + system prompt). `working/todos.md` Track 7.

## What the design must cover (be exhaustive; add what's missing)

1. **Vision / where this is going.** Frame the whole thing: the graph + its query layer as a
   first-class, documented, portfolio-grade system that BOTH a CLI and the chat-UI speak. What is
   the end state in 1 / 3 / 6 moves? This anchors every decision below.

2. **The content-first retrieval axis (roadmap D1 — the #1 lever).** Design the quote/passage
   search that would have answered the meals question in one step. Options: build-time inverted
   index over the 6,053 node quotes vs. over the 344 chapter files vs. both; keyword vs. embeddings
   (and can embeddings even live in the Edge runtime, or must they be build-time?); the new chat
   tool shape (`search_quotes`/`search_passages`). Weigh cost, latency, the 50 ms Edge CPU budget.

3. **The traversal script library — organization + unification (§4).** Where should it live
   (`graph/query/` vs top-level `query/` vs a packaged module)? Design the ONE documented query
   API that both `graph-query.py` and the chat-UI's TS tools become thin adapters over. Address the
   **divergence**: port `--container` / `--expand-beats` / `--path` / `--event-participants` to the
   chat; reconcile the two implementations so they can't drift again. This is Matt's interview
   centerpiece — make it legible.

4. **The descriptive-layer wiring (the orphan ring).** Design the fix for the 96%-islanded food /
   customs / materials layer. A descriptive **edge grammar** (candidates: `SERVED_AT` food→feast-
   event, `DESCRIBED_IN` →chapter, container tags on non-event nodes) + how the wiring pass runs
   (deterministic? the deferred Python food-grep? an enrichment dip?). Vocabulary must land in
   `reference/architecture.md` first (no invented edge types).

5. **Resolver / discoverability (G2/G10).** The fuzzy-fallback event-bias + alias holes. Verify
   whether the TS bundle carries the Python resolver's victim-indexing. Design the alias-coverage
   backfill + a de-biased fallback (prominence/type-weighted).

6. **The slim-projection problem (G9).** The bundle drops `## Narrative Arc` prose. Decide what the
   bundle should ship and why (size vs. coverage trade-off).

7. **Chronology / event-ordering.** There WAS an ordering bug (out-of-order chains) — diagnosed as
   a render bug, mostly fixed (Steps A/B/D done, deployed). **Step C remains** (deterministic wiki-
   date backfill of ~50 undated causal events → Haiku residue, gated on Matt). Fold it in: is the
   sort_keys model complete? Should Step C run, and how, deterministically first? See GRAPH-STATE §5.

8. **The charter'd-but-unbuilt + missing pieces.** Braid/convergence primitives (D7,
   `graph/convergence-maps/` = README only), the trigger table / routing index (D8), TWOIAF
   ingestion (1.5 MB on disk, never extracted), prophecy layer (4 nodes/0 edges), an MCP server for
   programmatic access. Which belong in this arc vs. parked?

9. **Options & trade-offs, explicitly.** For each major item: ≥2 approaches, the recommendation,
   and why. Don't present a single path as inevitable.

10. **Novel ideas / what we haven't considered.** Use the reasoning budget. What retrieval shapes,
    data-model moves, or portfolio angles haven't surfaced yet?

## Output requirements

- **Mechanical-agent-executable.** Every work item spec'd so a downstream Sonnet/Haiku agent can
  execute without re-deriving: concrete steps, exact files/scripts touched, inputs/outputs, success
  criteria, DO-NOTs, recommended model per item. Sequence them (dependencies, what's parallel-safe).
- **A recommended roadmap** — phased, with a clear first move.
- Keep the vocabulary rules (Pass/Track/Tier + lowercase `step`); new capitalized terms need a
  worklog Active Decision. Paste the glossary terms into any subagent you spawn.
- Update the appendix logs of whatever docs you touch; leave the doc set internally consistent.

## At endsession
- Worklog entry `### Session 189` (worklog.md, meta/graph).
- Update `working/todos.md` Track 7 to point at the new design doc + the sequenced plan.
- Commit docs only.

## DO NOT
- Mutate the graph (`graph/`), rebuild the bundle, or change `web/` / `scripts/` **code**. Design
  only — the output is documentation/plan.
- Invent edge types or vocabulary without routing through `reference/architecture.md` + a worklog
  Active Decision.
- Run any Haiku/extraction pass (incl. Step C) without Matt's explicit OK.
- Run `/endsession` without Matt's permission. Do not touch the top-level `scratch`/`scr` file.
