# SESSION 209 — Drain the 76 dispute-held recovery rows (last review-bucket step)

> **This is Session 209.** Stamp your worklog entry `### Session 209` at endsession.
> **Recommended model:** **Sonnet 4.6** orchestrator (adjudication reasoning is light; the
> machinery is deterministic); **Haiku** only if a fresh-verify sample is wanted. Opus not needed.
> **PRE-REQ:** S208 committed+pushed (`4a7224561f` + endsession commit). If `git log` disagrees
> with worklog.md S208, STOP and reconcile.

## Why
The S208 review-bucket recovery landed 995 edges + 201 event nodes, but **76 recovered candidate
edges were held by the standing dispute-proximity quarantine** (hedge-neighborhood / untagged
romance-class — §7.2) instead of landing. They sit in
`working/fire-and-blood/recovery-s208/out/*/dispute-review.jsonl` (per-unit). This is the LAST
open piece of the review-bucket track. S201 processed exactly this row-shape at scale
(320 → 63 human → adjudicate → inject).

## Steps (the S201 machine, small)
1. Concatenate the 76 rows (all `out/*/dispute-review.jsonl`) into one working file; note each
   row's unit (needed for the chapter path `sources/chapters/fab/<unit>.md`).
2. Run `scripts/fab-dispute-preclassify.py` over them (check its CLI first — it expects the
   S201 row schema; these rows match, they come from the same reconciler). Auto-classes clear
   the bulk; a small human-adjudication residue remains (S201 ratio suggests ~10-20 rows).
3. Adjudicate the residue against the PRIMARY TEXT (open the chapter at the row's `line`;
   S200/S202 precedent: orchestrator overrides must be primary-text-anchored). Verdicts:
   confirm-with-source (tag `in_universe_source` + `disputed` where hedged → tier-2) / drop.
4. Inject via `scripts/fab-dispute-inject.py` (again, check CLI/expected input first). Use a
   fresh run_id (e.g. `<unit>-<date>-recovery-disputes`) — mint's P4 same-quote dedup +
   `assert_disputed_invariant` (disputed ⇒ in_universe_source + tier ≤ 2) protect the landing.
5. Gates: `python3 scripts/fab-semantic-gate.py` (4/4 PASS) + pytest + deno. `weirwood refresh`
   ONLY if nodes changed (edges-only ⇒ skip per the S205 note); if refreshed, surgical
   index revert (S206/S208 recipe — revert timestamp-only `generated_at` churn).
6. Worklog S209 entry; check the todos `[OPEN] 76 dispute-held recovery rows` item done.

## Success criteria
- All 76 rows dispositioned (landed with proper source tags, or dropped with a logged reason).
- Disputed invariant holds on everything landed; gate green; suites green.

## DO NOT
- Do NOT re-run extraction or the S208 recovery (`--recover`) — the recovery is COMPLETE;
  this drains only its dispute-held sidecar.
- Do NOT land a disputed edge without `in_universe_source` (P3 invariant fails loudly anyway).
- Do NOT start theories (gated) or strip-boilerplate (Matt-gated).
- Do NOT auto-run /endsession.

## After this track (prose note, NOT this session)
The **edge-vocab retrofit** (old "Part B", Matt-confirmed wanted) is the next full graph track —
it was riding behind the review bucket, which this session closes. Quote-grounded KNIGHTED_BY /
role edges / SUSPECTED_OF where main-series/F&B text supports them. Needs its own continue
prompt when Matt greenlights. Also open, Matt's pick: node-type promotion sweep (todos MED),
prod deploy of the enlarged bundle, strip-boilerplate (un-park condition MET).
