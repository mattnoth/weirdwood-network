# SESSION 212 — Roles slice: role edges for the zero-role event heads

> **This is Session 212.** Stamp your worklog entry `### Session 212` at endsession.
> **Recommended model:** **Sonnet 4.6** orchestrator (the machine is proven, decisions are
> bounded) + Sonnet proposers + **Haiku 4.5** fresh-verifiers. No Fable/Opus needed.
> **PRE-REQ:** S211 committed+pushed. If `git log` disagrees with worklog.md S211, STOP and reconcile.

## Why (S211 continuation)

S211 shipped edge-vocab retrofit Part B (SUSPECTED_OF/KNIGHTED_BY + 2 role upgrades) and
found **313 event nodes carry ZERO role edges** (no AGENT_IN / VICTIM_IN / WITNESS_IN /
COMMANDS_IN / PARTICIPATES_IN / FIGHTS_IN / ATTENDS / OFFICIATES pointing at them) while
their prose names actors, victims, and commanders. Role edges are what make an event
node answer "who was involved?" in the chat — and S211's routing fix (relationship
questions → neighbors) means these edges are now REACHABLE the moment they exist.

## Scope — ranked, NOT all 313

Round 1 = the **top ~50 by value**. Rank deterministically first (Python): degree
(existing edge count), quote count, container tags, prominence if available. High-degree
events with rich prose but no roles are the wins; thin wiki stubs are NOT worth agent
passes (many of the 313 are stubs — let the ranking exclude them naturally).

## Machine (the S211/S133+ dip pattern — reuse `working/edge-retrofit-s211/` as template)

1. **Deterministic prep:** regenerate the zero-role list from `graph/edges/edges.jsonl`
   (S211's scan is stale the moment new edges land); rank; build per-event passage
   packets (node prose + quotes + existing edges as dedup context).
2. **Sonnet proposers** (3–5, disjoint packet ranges, write-only-named-files): propose
   role edges with verbatim quotes locatable in `sources/chapters/{book}/{chapter}.md`
   (book ∈ agot acok asos affc adwd tmk tss thk fab — quotecheck/mint ABORT on a missed
   quote). Role-type discipline: AGENT_IN (does the thing) vs VICTIM_IN (harm patient —
   the harm-gate checks the event subtype!) vs COMMANDS_IN (command tier) vs
   PARTICIPATES_IN (non-combat) vs FIGHTS_IN (combatant) vs WITNESS_IN vs ATTENDS vs
   OFFICIATES — paste the architecture.md row definitions into the proposer prompts.
   Paste the harvest rule + the vocabulary canon (Pass/Track/step/Tier) too.
3. **Haiku adversarial fresh-verify** on every candidate (S211 `VERIFY-RULES.md` pattern).
4. **Orchestrator adjudication with history checks** — S211's biggest lesson: the
   verifiers can't see session history. Grep prior fresh-verify records
   (`working/enrichment/*/fresh-verify.md`, ADJUDICATION files) before accepting
   anything that smells re-proposed.
5. `quotecheck_enrichment.py` → `mint_enrichment.py` DRY-RUN on scratch copies →
   **Matt's explicit go** → real mint → fab-semantic-gate + pytest + deno.
6. **Step-0 harvest consume** at endsession (S211 left 17 open; a dip adds ~25–40 —
   the ~30 bar will likely trip → drain or stage the drain).

## Watch-outs (from S211)

- **VICTIM_IN harm-gate:** `war`/`incident` are NOT in HARM_EVENT_SUBTYPES — a VICTIM_IN
  onto a war/incident-typed event FAILS the gate. Route those to PARTICIPATES_IN or
  retype the event first if it's genuinely mistyped.
- **Quote grounding:** single-line substrings from the chapter file, verbatim including
  OCR `|`-for-I artifacts; quotes spanning line-wraps fail the line-check.
- **No invented slugs, no node mints** — role edges onto EXISTING nodes only; missing
  people → `no_node` list for review.
- Small residue absorbable if trivially in-path: `death-of-queen-ceryse` carries
  `AGENT_IN maegor` while its prose says "rumored murder" (confidence mismatch, S211
  flag); the 3 parked wiki-only knighting facts stay parked.

## Success criteria

A bounded, quote-grounded, fresh-verified role-edge batch on the top-ranked events
(mint only on Matt's go); zero gate/suite regressions; the ranked remainder list saved
so later rounds don't re-rank.

## DO NOT

- Do NOT sweep all 313 — ranked top-~50 round, then stop and assess.
- Do NOT mint before Matt's explicit go (dry-run ≠ permission).
- Do NOT re-propose adjudicated drops (check S159/S211 records).
- Do NOT run /endsession without permission.
