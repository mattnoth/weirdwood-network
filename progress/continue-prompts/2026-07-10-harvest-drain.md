# SESSION 205 — Harvest-queue drain (66 open rows, bar tripped at S204 endsession)

> **This is Session 205.** Stamp your worklog entry `### Session 205` at endsession.
> **Recommended model:** **Sonnet 4.6** orchestrator + Sonnet attacher subagents (the
> S152/S165 drain machine — routing + attachment, no deep causal judgment) + Haiku or
> Sonnet fresh-verify on a sample.
> **PRE-REQ:** S204 committed+pushed (causal spine complete, deployed). If `git log`
> disagrees with worklog.md S204, STOP and reconcile.

## Why

The endsession step-0 bar (≥30 open rows) tripped at S204 close: **66 open rows** in
`working/harvest-queue.md` — 48 dropped by the S204 causal-spine proposer subagents +
10 pre-S204 F&B strays canonicalized at endsession + 8 older rows. Rule: never let it
grow silently (S153–S156 precedent). Matt's sequencing puts **cross-era seams** right
behind this drain — keep the drain tight, don't scope-creep into seam work.

## The task (the S152/S165 drain machine)

1. Count + route: `grep -c '^| open ' working/harvest-queue.md`. Python pre-pass to
   locate each row's cite (verbatim line-check) and route rows to **disjoint node-dir
   owners** (events/ vs characters/ vs artifacts/ etc.) so parallel attachers never
   collide. Most S204 rows are `fab` kind=quote/appearance/description/food.
2. Parallel Sonnet attachers (2–4, write-only-named-files): attach quotes to node
   `## Quotes` blocks / description fields / `object.food` mints where warranted; POINT
   rows that need a mint the drain shouldn't do → park with reason.
3. Fresh-verify a sample (the S152 pattern caught real cite-drift), orchestrator
   re-checks flags.
4. Flip attached rows `| open |` → `| done |` (or `| parked |` with reason); run
   `python3 scripts/verify-quotes.py` equivalent (the book-cited quote verifier — S203
   ran 1079/1079) + `weirwood refresh` + gate + pytest/deno if graph mutated.
5. Record count open→0 in the worklog entry.

## Inputs
- `working/harvest-queue.md` — the 66 `| open |` rows (S204 block starts at the
  `S204 causal-spine session drop` comment marker).
- Drain machinery + history: `working/arc-enrichment-backlog.md` harvest section;
  memory `feedback_harvest_queue`; S152/S165/S203 worklog entries.

## Success criteria
- Open rows 66 → 0 (done/parked, each park justified).
- Quote verifier green; gate PASS; suites green if graph mutated.
- No new mints beyond obvious `object.food`-class nodes (drain ≠ enrichment).

## DO NOT
- Do NOT start cross-era seams (that's the NEXT session — Matt-sequenced), theories, or
  the strip track (Matt-gated). Do NOT re-run extraction. Do NOT auto-run /endsession.

## After this drain (queued next, for awareness only)
**Cross-era seams session**: wire the F&B/Targaryen-history layer to the main-series
era both directions (Blackfyre, Dark Sister, Dragonstone, dragon skulls, "the dragons
danced and men died" references; CONSIDER D&E which has no Pass 1 — read tmk/tss/thk
directly). Also absorbs S204 residue flags (todos): lord-rogars-war/third-dornish-war
suspected dup · mistyped maidens-day-ball/regency-of-aegon-iii/archon-of-tyrosh nodes ·
backwards `assault-on-harrenhal DEFEATS blacks` wiki edge · unminted Prince-Daeron-death
/ Gaemon-birth-death beats.
