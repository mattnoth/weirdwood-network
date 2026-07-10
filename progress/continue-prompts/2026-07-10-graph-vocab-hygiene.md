# SESSION 207 — Graph vocabulary / schema hygiene (F&B event schema-drift + edge-vocab retrofit)

> **This is Session 207.** Stamp your worklog entry `### Session 207` at endsession.
> **Recommended model:** **Sonnet 4.6** — mostly deterministic retypes + a schema design call + a
> quote-grounded edge-retrofit dip. Cheapest-viable; no Opus needed. Use Haiku for any fresh-verify.
> **PRE-REQ:** S206 (cross-era seams) committed+pushed. If `git log` disagrees with worklog.md S206, STOP and reconcile.

## Why (Matt-sequenced + S206 discovery)
Two related "make the graph speak the current vocabulary" jobs, both surfaced/sequenced by now:

**Part A — F&B event schema-drift (concrete; found S206).** The Fire & Blood bulk apply (S200–S204)
left the event layer type-noisy:
- **Marquee mistypes still live as `event.battle`:** `dance-of-dragons` (THE central F&B event — it's a
  *war*), `hour-of-the-wolf`, `lysene-spring`, and likely others. (S206 already fixed 4 flagged ones:
  `third-dornish-war`→war, `maidens-day-ball`→feast, `regency-of-aegon-iii`→council,
  `archon-of-tyrosh…`→character.human.)
- **~20 off-schema `event.*` subtypes NOT in `reference/architecture.md`'s type table:** `event.death`×141,
  `event.capture`×42, `event.other`×35, `event.ceremony`×24, `event.decree`×10, `event.council`×9,
  `event.voyage`/`negotiation`/`uprising`/`surrender`/`betrayal`/`progress`/`escape`/`disaster`/`raid`/
  `plague`/`famine`/`dismissal`/`construction`/`abduction`/… ×1–5. Scan:
  `grep -rhoE "^type: event\.[a-z]+" graph/nodes/events/*.node.md | sort | uniq -c | sort -rn`.

**Part B — edge-vocab retrofit (Matt's original backfill idea, [OPEN], rides after seams).** Older
extraction passes predate newer edge types (`KNIGHTED_BY`/`BESTOWS_KNIGHTHOOD_ON`, the reification role
edges, `SUSPECTED_OF`, …). Where main-series/F&B text supports them, retype/add so the whole graph
speaks the current vocabulary. This is a quote-grounded enrichment dip (the S133+ machine).

## OPEN QUESTION FOR MATT (resolve at session start, before mutating)
The ~20 off-schema event subtypes are a **design fork**, not a mechanical fix:
- **(a) Sanction** the useful ones in `architecture.md`'s Type Reference Table (they're already de-facto
  in use at scale — event.death ×141 is real signal), OR
- **(b) Retype** them down to the existing sanctioned leaves (event.death→? event.assassination/execution
  where they fit; event.capture→? etc.), OR
- **(c) Hybrid** — sanction the high-count justified ones (death/capture/council/ceremony/decree),
  retype the long tail of singletons.
Recommended: **(c) hybrid** — but this is Matt's call. Do NOT mass-retype before he picks. Present the
count table + a proposed disposition per subtype, get his go, THEN apply. (Adding a type needs a worklog
Active Decision + architecture.md update — CLAUDE.md rule #6 + the vocab-canon memory.)

## Machine
1. **Part A first (concrete):** produce the `event.*` count table + a proposed disposition per subtype
   (sanction / retype-to-X / hybrid) + the marquee mistype list (dance-of-dragons etc. → event.war).
   Get Matt's go on the design fork. Then apply retypes deterministically (a script like the S206 residue
   fixer), architecture.md update for any sanctioned types, `weirwood refresh` (**surgical index revert**
   — keep only meaningfully-changed index files, revert the ~8.4k timestamp-churn; see S206 detail for the
   exact recipe), gate + pytest/deno.
2. **Part B (dip):** scope with a grounded probe (which nodes have main-series text supporting a newer
   edge type), propose quote-grounded edges via `scripts/mint_enrichment.py`, fresh-verify (Haiku),
   `scripts/finalize_enrichment.py`. Dedup hard.
3. **STEP-0 harvest consume** any new rows; capture quotes while in the text (FIRM rule).

## Success criteria
- Part A: `dance-of-dragons`/`hour-of-the-wolf`/`lysene-spring` no longer `event.battle`; the off-schema
  subtypes reconciled per Matt's chosen disposition; architecture.md + graph in sync; gate + suites green.
- Part B: a bounded, quote-grounded, fresh-verified batch of retrofit edges (NOT a mass mint).

## DO NOT
- Do NOT mass-retype the event subtypes before Matt picks the design fork (a/b/c).
- Do NOT re-run extraction; do NOT start theories (gated) or the strip track (Matt-gated — separate un-park).
- Do NOT commit the 8.4k timestamp-only index churn (surgical revert, per S206).
- Do NOT auto-run /endsession.

## Backlog (NOT this session unless Matt asks)
- **Strip "from the AWOIAF wiki" boilerplate** (6,739 nodes; un-park condition MET, Matt-gated) →
  `progress/continue-prompts/archive/2026-07-06-strip-wiki-boilerplate-identity.md`.
- **~85 nodes carry duplicate `## Quotes` headers** (S205 finding; `parse_quotes` reads only the first) —
  scriptable schema-drift dedup; fits naturally into a hygiene pass.
- Dragon-skull → dragon typed edge: no in-vocab "remains-of" type exists (S206 left it prose-only); revisit
  only if a "physical remains" relation is wanted graph-wide.
