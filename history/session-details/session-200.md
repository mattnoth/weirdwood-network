---
session: 200
date: 2026-07-07
model: claude-fable-5 (orchestrator) + 1 Sonnet adjudication subagent
track: graph (fire-and-blood)
graph_mutation: yes — Matt's explicit in-session apply-go
---

# Session 200 — Fire & Blood first real apply: 4 smoke units into the graph

The milestone session of the F&B track: after S198 built the pipeline and S199 turned every §7
pre-bulk gate green, this session got Matt's explicit apply-go and performed the track's first
real graph writes. The concise record is the worklog S200 entry; this file keeps the reasoning.

## Order of operations

Deliberately did all free, non-mutating prep BEFORE asking for the go, so the go/no-go decision
had complete information: the step-0 re-reconcile + diff ran first, then the AskUserQuestion
(apply-go + the one open craghas question). Matt: **GO**, and **craghas = mint with PART_OF**
(over fold; the slaying carries its own `daemon KILLS craghas` role edges and matches the
reify-marquee-beats precedent — death-of-ygritte S153, victarion-slays S157).

## Step 0 — the validation-set diff held perfectly

Non-smoke reconcile of all 4 units into `working/fire-and-blood/apply/`. The diff against the
smoke runs was the cleanest possible outcome: 0 slug mismatches on shared rows, 0 regressions,
and the auto-accept sets matched the S199-validated populations EXACTLY — 23 discriminator
accepts (the 15 in-sample + 8 out-of-sample ground-truthed rows, to the row) and 188 exact-1.0
accepts (the 130 + 58 would-accept counts, to the row). Nothing outside the validated set
auto-routed. Dispute-held went 19→21, explained structurally: House Velaryon and Corlys were
smoke-review-held upstream, so their line-109 artifacts only reached the quarantine once the
exact-1.0/discriminator accepts routed them — the two new holds just joined the adjudication set.

## Disposition surgery — notable judgment calls

- **Fold prose skipped.** All four fold-source CREATE bodies were thin Events-table outcome
  fragments ("Myrmen driven into the sea", "Cole won the melee", "King's Hand slain") and every
  fold target is an already-rich wiki node — so folds were pure edge re-routes + node removal,
  no merge-plan noise.
- **Role-edge recasts at fold time** (touch-the-row-anyway principle): the coronation patient
  role became `aegon-i HONORED_AT aegons-coronations` (exact precedent: `lyanna-stark HONORED_AT
  crowning-of-lyanna-at-harrenhal`, the graph's only prior HONORED_AT); the melee agent role
  became `criston-cole PARTICIPATES_IN tourney-…` (S161 precedent); the Alyn Stokeworth pair was
  recast as the KILLS dyad + `alyn VICTIM_IN harren-the-reds-rebellion` — folding to the
  rebellion node without the dyad would have flattened the slaying.
- **Wrong-parent correction:** the S199 stage-1 note wanted Rhaenys's parley wired to
  `conquest-of-dorne` — that node is **Daeron I's 161 AC conquest**, wrong era entirely. Wired
  `PART_OF aegons-conquest` instead. (Lesson: eval-note slugs get verified against node
  frontmatter before minting.)
- **NOT done, deliberately:** a general re-type of the reconciler's patient-role→VICTIM_IN
  mapping (births, kneelings read oddly). It's a systematic extractor/reconciler convention; a
  hand-edit of one unit would create inconsistency with the coming bulk output. Queued instead
  as a deterministic post-bulk sweep (filter `evidence_kind: book-fab` + event type).

## Dispute adjudication — the subagent was good but not sufficient

Fresh Sonnet adjudicated all 21 held rows (verdicts: 17 clear / 4 tag / 0 drop) with a genuinely
useful pattern find: euphemistic romantic phrasing ("became his favorite", "the groom's
favorite", "found a new favorite") = tag disputed/unattributed, explicit terms ("his paramour
Mysaria") = clear tier-1; and the one true single-source catch (`lyonel-strong ADVISES` the
death penalty → eustace) came from noticing Eustace was a *participant* in the reported scene.

But Fable verification against the primary text caught **two wrong clears, both mine in origin** —
the adjudication guidance had used "that Daemon was exiled" as an example of a flat fact, and the
text says otherwise: p02 lines 113–125 open with "Here is where our sources diverge", Grand
Maester Runciter's version has a mere quarrel-and-departure (no decree), the exile-on-pain-of-death
exists only inside the Eustace/Mushroom tale zone, and Gyldayn's "Of the aftermath, these things
are certain" list pointedly includes the Stepstones return but NOT the decree. Overrides:
`viserys BANISHES daemon` and the Daemon scandal-prose bullet both tagged tier-2 /
`gyldayn-synthesis`. This is the S199 audit-v1 failure class (the exile cluster) resurfacing at
adjudication — the takeaway baked into the next continue prompt: **verify subagent clears against
the primary text before feeding them back; divergence zones where one chronicler's version lacks
the claim entirely are not flat facts.**

Also: one redundancy skip (p01's euphemistic Daemon–Mysaria LOVER_OF would have duplicated p02's
flat tier-1 same-triple), and the 2 held *event* candidates were residued rather than minted —
held events have no CREATE bodies, their substance is carried by the adjudicated edges (S200-D4
BANISHES, S200-D7 KILLS), and the Daemon-exile event's very name encodes the disputed cause.
Full row-by-row record: `working/fire-and-blood/apply/ADJUDICATION-s200.md`.

## The apply itself — uneventful, which is the point

Per-unit checkpoint → mint → merge, ×4. Everything the S198/S199 design promised held under real
writes: mint's run_id re-run guard aborts correctly; the merge writer reported 0 skipped / 0
not-found on all four units; the `-pMM` run_id fix proven live (Rhaenyra's node carries distinct
p01/p02 idempotency markers, both sections merged); exactly the 18 predicted boilerplate Identity
lines upgraded; +264 edges (23,099→23,363), all quote-located, 0 disputed+tier-1 invariant
violations; 14 disputed rows all carry `in_universe_source`.

## Incidents / friction (small)

1. **Test-fixture collision with the graph:** `test-fab-reconcile.py` asserted "Capture of Loren
   Lannister" routes CREATE — true until this session minted that exact node; the router's
   clean-hit→update on it is correct live behavior. Fixture moved to "Capture of Sharra Arryn"
   (person node exists, event doesn't). Same class as the S192 `cwd-is-tmp` lesson: tests that
   assert live graph state decay as the graph grows.
2. **Silent no-op `git add`:** `git add graph/ index/` with a nonexistent `index/` pathspec fails
   the WHOLE add (git is all-or-nothing on bad pathspecs) and stderr was suppressed — the 18 new
   per-node index files stayed untracked through the verify commit. Caught at close-out status
   check; committed separately. Worth remembering: never suppress stderr on a staging command.
3. **Bulk-resume gap found in prep:** the worker decides unit completion by output existence at
   `extractions/fire-and-blood/`, but the 4 smoke outputs lived in `smoke/v1/` — `--resume`
   would have re-extracted (and worse, re-applied) them. The 4 enrichment files were installed
   at their canonical paths; `--build-queue` re-run confirms 39 units with 4 satisfied.

## Bulk economics (from real telemetry)

pace.py on the 4 completed units: median 480 s / $1.80 / ~40K output tokens per unit. 35 units
≈ **$63**, ~10.5 h at `LONGRUN_SLEEP_BETWEEN=600` (16 h at the conservative 1200). Handed to Matt
as a single iTerm block; observability contract = `run-summary.jsonl` per design §7a.
