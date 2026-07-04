---
session: 189
date: 2026-07-04
track: meta/graph
model: Fable 5 (handoff recommended Opus 4.8 at max reasoning; ran on Fable as orchestrator)
api_cost: 6 read-only survey subagents (Sonnet-class) + trivial local spot-checks; no live chat turns; no graph writes
---

# Session 189 — Query-layer MASTER DESIGN: contract-first plan, Fable-orchestrated execution

## Purpose

The S188 handoff mandated a master design session for the whole query/traversal layer:
pressure-test the S188 analysis (G1–G10 / D1–D8), find what it MISSED, and produce a design
document mechanical agents can execute. Explicit latitude to overturn the prior framing.
Matt reviewed mid-session and issued three amendments (S189b) plus one late addition (S189c).

## Method

Fanned out four parallel read-only Sonnet surveyors (per the model-fit rule — the expensive
model kept for design): (1) `graph-query.py` + `event_alias_resolver.py` mode-by-mode; (2)
`web/src/lib/*` + `agent.ts` + the bundle build; (3) full `scripts/` inventory (5-way
classification, import-coupling map) + repo-wide test inventory; (4) a quantitative graph
census (orphans, field coverage, edge payloads, index contents). Ran two decisive spot-checks
directly: probing `web/data/alias-map.json` for victim phrases, and opening
`graph/index/foods/acorn-paste.index.json`.

## The reframe (departing from S188)

S188 framed the work as "port missing modes + un-defer search + fix aliases." The surveys
showed those are symptoms: the project has **four accidental query surfaces with no shared
contract** — graph-query.py, the alias resolver (its own regex YAML parser, own normalizer),
48 MB of `graph/index/` that *nothing in the query path reads*, and the TS port. Fixing gaps
one-by-one inside that structure mints a fifth drift surface. The design is therefore
**contract-first**: one documented query surface (named ops, two profiles — full CLI vs
bounded chat), one Python engine, golden parity fixtures run by BOTH pytest and deno, then
capabilities land inside the contract, each gated by an eval harness.

## Hard findings (verified this session)

- **G19:** "robb stark's death" / "ned stark's execution" → MISS in the shipped
  `alias-map.json`. The S96 victim-phrase index never reached the bundle — the marquee
  resolver fix doesn't exist in the deployed product.
- **G13:** `graph/index/foods/acorn-paste.index.json` = 0 appearances / 0 chapters. The index
  layer is unrouted AND stale for harvest-minted nodes (resolution predates their aliases).
- Census: 27.8% of nodes are orphans (2,358/8,468); artifacts are edge-SINKS only (Iron
  Throne: 0 out-edges); 5 YAML-broken node files; 91 dangling edge endpoints; 28 duplicate
  edge rows; 84% of `aliases:` keys are empty stubs.
- G10's mechanism found: fuzzy scoring has no candidate-length penalty, so short queries
  score 1.0 against long event slugs — deterministic fix.
- Test estate: 26 pytest files (pytest-as-runner over unittest style, no conftest/CI), 41
  deno tests against the real bundle, one orphaned test pytest can't discover.
- The scripts survey mapped ~20 dynamic same-directory loads + 4 sibling imports +
  `tests/_helpers.py` hard-coding `SCRIPTS_DIR` → a full scripts/ reorg is high-blast-radius;
  extract only the query layer instead.

## New gaps beyond S188 (G11–G19)

G11 no contract/parity mechanism (the root cause); G12 intra-Python triplication (3
frontmatter parsers); G13 index layer unrouted+stale; G14 no telemetry loop over the live
usage logs; G15 no eval harness; G16 two edge serializations unreconciled; G17 doc drift on
the query surface's own docs; G18 data-hygiene traps; G19 the victim-alias portability gap.

## Deliverable

`working/query-layer/design.md` — destination vision, grounded findings, G-verdicts,
decisions D-A…D-I each with weighed options, target architecture (`graph/query/` package +
spec + builders + tests), step cards 0–9 + gated hygiene side-step H, sequence, out-of-scope
list, open forks. Companion pointer updates in GRAPH-QUERY-ROADMAP.md (now
diagnosis/history; design doc is plan of record), GRAPH-STATE.md (§4b verification answered),
todos.md Track 7.

## Matt's review (S189b) — amendments applied same session

1. Home = **`graph/query/`** (overruled my top-level `query/` pick; clarified the mutation
   gate covers data dirs, not query code).
2. **Pytest traversal suite DEFERRED TO LAST** — built over the finished layer, with Matt;
   no half-finished states. Golden spec cases still land in session A (drift protection).
3. **Project-first, not interview-first** — portfolio framing dropped as a design driver.
4. Execution model rewritten: **three Fable-orchestrated sessions** (A engine / B retrieval /
   C reach+close-out) fanning out Sonnet builders + Haiku verifiers; remaining forks
   (read_passage-to-chat, SERVED_AT timing, MCP, shim retirement) routed to a session-C
   **advisory-board fan-out** (the S133 finding: Sonnet board ≈ Opus proposer), Matt
   overrules on read. Matt also flagged the first draft as weaker than expected — the honest
   diagnosis: over-conservative session-per-step sequencing and inherited interview framing;
   both fixed by the amendments.

## S189c (at endsession)

Loremaster persona reframe added to step 5c: frame the persona around its actual user — a
researcher / thought-experimenter on the series — hypothesizing that the researcher frame
licenses fuller answers. Voice only; the SHARED_RULES safety block (theory-scope guardrail,
cite rules) is persona-independent and untouched; an A/B eval row rides the step-5 eval
re-run; Matt reviews before any deploy. Handoff consolidated to ONE rolled orchestrator
prompt (A→B→C, clean-boundary stop) instead of per-bundle prompts.
