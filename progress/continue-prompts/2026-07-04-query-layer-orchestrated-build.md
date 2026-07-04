# SESSION 190 — query-layer Fable-ORCHESTRATED BUILD (design.md sessions A → B → C, rolled)

> **This is Session 190.** Stamp your worklog entry `### Session 190` at endsession.
> (If you complete multiple bundles, it is still ONE session — one worklog entry covering
> every bundle you finished.)

**Recommended model: Fable as ORCHESTRATOR.** You conduct; **Sonnet subagents build; Haiku
subagents do mechanical verification** (diffs, greps, variant checks). Matt's directive: get
through the design doc **as far as context sensibly allows in one session**, then hand off at
a clean boundary. Every bundle you finish must land COMPLETE and verified — no half-finished
states, ever (Matt, S189b).

**Track:** graph/meta — the query-layer track.

## Read first (orchestrator only — do not fan this out)
1. **`working/query-layer/design.md`** — the master design (S189, amended S189b/S189c). It is
   the spec; this prompt is only the pointer. Read §0 (reframe), §3 (decisions), §4 (target
   architecture), §5 (step cards + execution model), §6 (sequence).
2. `worklog.md` Current State. Trust it over this prompt if they disagree — flag contradictions.
3. Do NOT re-survey the code — the S189 survey facts are in design.md §2a.

## Mission
Execute the design doc's orchestrated bundles **in order, each to completion**:

1. **Session A — the engine** (steps 0 + 1; step 7 braid only if room): scaffold
   `graph/query/` (S189b: NOT top-level), one package/one loader/one parser/one normalizer,
   absorb graph-query.py + the resolver's resolution half + build-chat-export.py, port
   familyTree TS→Python, compat shims (keep `from event_alias_resolver import normalize,
   name_to_normalized` importable), update weirwood.zsh / weirwood-refresh.sh /
   scripts/README.md. Zero behavior change. ALSO land `spec/operations.md` v1 + first golden
   cases + `web/src/lib/spec_cases_test.ts` (the drift alarm goes live here).
   **Exit gate:** old CLI ≡ new CLI (Haiku-diffed across every mode, ~20 real slugs); full
   `pytest` green; `cd web && deno task test` green with a field-identical rebuilt bundle.
2. **Session B — retrieval** (steps 3 + 4 + 5): eval baseline FIRST (deterministic metrics —
   resolve hit/miss per question — need no API spend; **live-model eval columns are GATED on
   Matt's OK**, leave them empty rather than spend), then resolver hardening (victim-phrase
   bundle fix G19, variant expansion, fuzzy de-bias G10, telemetry miner), search index +
   `search` op both runtimes + `search_quotes` chat tool, routing-table prompt rewrite, and
   the **S189c loremaster persona reframe** (researcher/thought-experimenter frame — voice
   only, SHARED_RULES safety block untouched; draft in repo, Matt reviews before any deploy).
   **Exit gate:** parity cases green both runtimes; eval table shows the meals question
   answerable in ≤3 tool calls on the deterministic metrics; no causal-path regression.
3. **Session C — reach + close-out** (steps 6 + 8a–c + side-step H propose-only + 9), plus
   the **advisory-board fan-out** on the open forks (read_passage-to-chat / SERVED_AT timing /
   MCP / shim retirement): Sonnet board per fork, synthesize decisions-with-rationale into
   design.md §8, Matt overrules on read.

## Context discipline (how far to go)
- Delegate ALL heavy reading and building to subagents; keep your own context for
  adjudication, contract-holding, and verification synthesis.
- **Stop only at a bundle boundary** (A done, or A+B done, or A+B+C done) — never mid-bundle.
  When your remaining context makes the next full bundle unsafe, STOP: update the design
  doc's step-card statuses, write the worklog entry, mint the continue prompt for the
  remaining bundles (same shape as this one), archive this prompt, commit.
- Paste the canonical vocabulary into every subagent prompt: **Pass** = numbered corpus
  sweep; **Track** = named work chunk; lowercase **step** = ordered piece of a Track;
  **Tier** = confidence 1–5 ONLY. Also paste the relevant DO-NOTs below.

## Hard gates (regardless of how far you get)
- **No mutation of `graph/nodes|edges|index`** without Matt's explicit go (`graph/query/` code
  is fine; side-step H stays propose-only; step 8d does NOT run).
- **No LLM bulk pass** (Haiku *verification* subagents are fine; the 8d Haiku wiring pass is
  gated on Matt).
- **No prod deploy** — deploys are manual per `DEPLOY.md`; prompt/persona changes are drafts
  in the repo until Matt reviews.
- **No pytest traversal suite** — deferred to the Track's final session, Matt-paired.
- `sources/` read-only; never fetch the wiki; don't touch top-level `scratch`/`scr`;
  don't run `/endsession` without Matt's permission (the per-bundle close-out above is
  worklog+commit housekeeping, not /endsession).

## At handoff
Worklog entry (next S-number, graph/meta) per bundle reached; design.md step-card statuses
updated; `working/todos.md` Track 7 line updated; next continue prompt minted + this one
archived; commit (code + docs produced by the bundles you completed).
