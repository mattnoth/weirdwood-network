# SESSION 208 — F&B review-bucket triage (1,440 quarantined reconcile-review rows)

> **This is Session 208.** Stamp your worklog entry `### Session 208` at endsession.
> **Recommended model:** **Sonnet 4.6** — deterministic name→slug mapping + token-screen + create-or-skip
> triage reasoning; **Haiku** for residue disambiguation + fresh-verify. Opus not needed.
> **PRE-REQ:** S207 (event schema-drift + quote-dedup) committed+pushed. If `git log` disagrees with
> worklog.md S207, STOP and reconcile.

## Why
During the F&B bulk apply (S200–S202) the reconciler **quarantined 1,440 `reconcile-review.jsonl` rows** —
each a NAME it could not confidently route to a slug, so every candidate edge touching that name was
dropped (never landed). S203 wrote the policy plan but did NOT execute it. The high-value payload is a
**second deferred-events vein** — real missing canonical events currently absent from the graph.

**Read first (canonical):** `working/fire-and-blood/apply/REVIEW-BUCKET-TRIAGE-PLAN-s203.md` — the 11-class
keep/drop table + recommended sequencing. This prompt does NOT restate it; trust the plan.

## FIRST — resolve the open mechanics question (do this before any recovery; ~30 min, de-risked S207)
The quarantined edges are NOT persisted separately. Recovery = re-run `fab-reconcile-candidates.py`
per affected unit with the missing names now resolvable. S207 read the reconciler (read-only) and found:
- **`--redirect-map` is slug→slug** (applied *after* a slug is found, `fab-reconcile-candidates.py:1087`)
  — it is NOT a raw name→slug override for unresolved names.
- The router resolves names via **clusters + the alias resolver**. So the recovery path is:
  **add the missing names as node `aliases:` / cluster entries (or mint nodes for genuinely-missing
  events) → `weirwood refresh` → re-run the unit.** No new override CLI arg is strictly required.
- **THE REAL OPEN QUESTION = re-injection idempotency.** Re-running a unit re-processes ALL its rows,
  so edges that ALREADY landed must not double-apply. Before recovering anything, CONFIRM the
  `mint_enrichment` P4 exact-dup guard makes a re-run idempotent (same edge_type/source/target/quote →
  skipped), OR add a `--only-names` / row-filter to the reconciler+inject path (small script-builder job).
  Prove this on ONE unit with a git checkpoint before scaling.

## Sequencing (from the plan; deferred-events vein is the prize)
1. **Small classes first** (type-mismatch 16 + house-surname 13 + bare-first-name 6 + needs-vocab 5 +
   blocklisted 2 + in_universe_source `mellos` 1 = 43 rows): one deterministic sitting.
2. **`no-decisive-margin` (172):** disambiguator-aware micro-pass (each row carries a disambiguator
   string) — deterministic keyword rules first, Haiku for residue.
3. **`unresolved-status` head-map (147 entries → ~514 rows):** one curated name→slug map sitting +
   re-inject. **DROP the ~415-row long tail explicitly (log the drop count).**
4. **`event-dedup-risk` (221) + `composite-name` (57) = THE DEFERRED-EVENTS VEIN:** re-screen with the
   S203 token-screen (exact-token match vs the event-slug inventory), auto-clear no-real-dupe rows,
   then create-or-skip triage (same machinery as the S203 37-row sidecar). Fresh-verify (Haiku) every
   CREATE. Some names will now match nodes minted S201–S204. Marquee targets: Death of Queen Helaena,
   Dance principals' births, Battle of the Stepstones, Betrothal of Aegon III & Daenaera.

## Open design Qs that RIDE this session (Matt, S207)
- **Sanction `event.betrothal`? and maybe `event.betrayal`?** S207 folded both into `event.incident`
  (the `BETROTHED_TO`/`BETRAYS` edges carry the relations), but Matt is leaning yes on betrothal (and
  "might be worth the betrays part"). The review bucket will surface MORE dynastic betrothals → once the
  volume is visible, DECIDE, and if sanctioned, **retrofit the S207-folded incident nodes up** to the new
  leaf (they carry `betrothal`/`betrayal` in their slug/name). Needs a worklog Active Decision +
  architecture.md row (rule #6) if sanctioned.
- **Node-type promotion sweep** (todos, MED): S207's retype was conservative (ambiguous → incident).
  Promote `death-of-*`→`event.death`, `arrest-of-*`/`capture-of-*`→`event.capture`, etc. where the node
  genuinely is one. Can ride here or be its own slice.

## Success criteria
- The idempotency question RESOLVED + proven on one unit before scaling.
- Small classes + no-decisive-margin recovered; unresolved head-map applied, tail DROP logged.
- The deferred-events vein (278 rows) triaged: missing canonical events minted (fresh-verified) or
  skip-exists; edges recovered. Gate green (fab-semantic-gate + pytest + deno). Refresh + surgical index
  revert (S206 recipe). If nodes added → `weirwood refresh` (real, then keep only meaningful index files).

## DO NOT
- Do NOT scale re-injection before proving idempotency on one checkpointed unit.
- Do NOT mint an event whose NAME encodes a disputed cause (S200 precedent — e.g. "Daemon exiled after
  the Rhaenyra scandal"); the disputed edge carries it.
- Do NOT re-run extraction; do NOT start theories (gated) or the strip track (Matt-gated).
- Do NOT commit timestamp-only index churn (surgical revert per S206).
- Do NOT auto-run /endsession.

## Backlog (NOT this session unless Matt asks)
- **Edge-vocab retrofit** (the old "Part B", Matt-confirmed wanted): KNIGHTED_BY / role edges /
  SUSPECTED_OF where main-series/F&B text supports them — quote-grounded dip. Rides after the review bucket.
- **Strip "from the AWOIAF wiki" boilerplate** (6,739 nodes; un-park condition MET, Matt-gated).
- 10 TWOW-preview `meta.chapter` nodes misfiled in `graph/nodes/events/` (directory drift); the
  `greyjoys-rebellion`/`greyjoy-rebellion` near-dup pair (S207 finds).
