---
session: 201
date: 2026-07-09
track: graph
model: Opus 4.8 (orchestrator) + Sonnet subagents (advisory board, fresh-verify, script-builders)
graph_mutation: YES — Matt's explicit apply-go (AskUserQuestion); batches 1–3 of 7 applied
---

# Session 201 — F&B bulk reconcile-apply: advisory-board pre-mint sweep + batches 1–3

## Setup
The 35-unit Fire & Blood bulk extraction (Matt-fired `claude -p` + longrun.sh) completed overnight
(all 39 units drained on v1; 4 were the S200 smoke units). Task: reconcile + apply the 35 new units
per the S200 pattern. Continue prompt: `2026-07-07-fab-bulk-reconcile-apply.md`.

## First wrinkle — re-extracted smoke units
The bulk `--resume` re-extracted the 4 already-applied smoke units (it keys off the manifest, not
file existence, and S200's "install at canonical paths" never wrote them to the manifest). Their
graph edges were already applied from the S200 versions, so the throwaway re-extractions were
restored to HEAD (`git checkout`) — provenance preserved. 35 units to apply.

## Systemic health gate (§7a) — PASS
Reconciled all 35 deterministically → run-summary. Every Dance unit showed dispute activity (no
disp≈0 AND held≈0 combo = no silent prompt failure). CREATE ~6.7/unit. 4 units <90% quote-located
(row-level quarantine, tolerated). 234 CREATEs, 1,504 edges total. Vocab: 3 needs-vocab holds only.

## The advisory board (Matt-requested)
Convened a 3-lens board at the mint boundary:
- **Mint-safety (READY-WITH-CONDITIONS):** mint is skip-if-exists + run_id-idempotent + manifest-guarded;
  merge hard-errors on not-found + atomic. Flagged: 5 disputed edges missing in_universe_source; 142
  cross-unit dup triples (mostly intended multi-cite); post-batch graph validator needed.
- **Vocab-governance:** DISINHERIT/REGENT/BOUNTY → all LEAVE_HELD (don't block mint). REGENT's tell:
  only 1 dyadic hold in F&B's most regency-dense material → demand absorbed by event-node reification
  + HOLDS_TITLE. Don't add an edge type mid-bulk (heavier than S199's event-subtype adds).
- **Process-skeptic (PROCEED-WITH-GUARDRAILS):** the 4-unit smoke measured the easy case. Two
  systematic bugs would ship ~65–95 bad elements: (1) VICTIM_IN on non-harm events (162 edges, ≥35
  wrong, invisible to dispute-review); (2) junk character.human CREATEs (~15/19). Plus: 320 dispute
  rows are ~95% proximity false-positives → over-tag risk; deterministic pre-classify shrinks to ~60.

**Matt's decisions (AskUserQuestion):** run all 6 fixes then batch-apply; non-harm patient edges →
PARTICIPATES_IN (not drop).

## The pre-mint sweep (P1–P7, all deterministic)
- **P1** VICTIM_IN harm-gate (HARM_EVENT_SUBTYPES const; non-harm→PARTICIPATES_IN; unknown→PARTICIPATES_IN;
  `assassination_attempt` caught via generic attempt-marker strip). **P2** junk character.human screen
  (18/19 rejected; +leading-article predicate). **P3** disputed⇒in_universe_source writer-enforced.
  153 reconciler tests.
- **P4** mint edge-level same-quote dedup (skip-if-exists on type+src+dst+norm-quote). Analytic: of the
  142 cross-unit triples, only **1** true same-quote dup — the rest legit multi-cite.
- **P5** dispute pre-classify (extended to prose+event kinds): 320 → **257 auto / 63 human** (54 needs-read
  + 9 romance). 68 tests.
- **P6** semantic per-batch gate (0 book-fab VICTIM_IN-on-non-harm / junk / dup / new-orphan). 33 tests.
- **P7** dispute-inject (resolved rows → candidates/merge-plan; name→slug via matched.jsonl; DISP-ids;
  events deferred to a sidecar). 38 tests. Dry-run: 66 edges + 155 prose + 37 events + 0 leftover.

Re-reconciled all 35 with the patched reconciler: 52 VICTIM_IN→PARTICIPATES_IN, 18 junk rejected, 216
CREATEs (only 1 char.human — the real "Aegon (nephew of Maegor)").

## Orchestrator error caught by verification
I twice queried "0 book-fab VICTIM_IN residue" and was WRONG both times — my one-liners used
`source`/`target` but the real edges.jsonl schema is `source_slug`/`target_slug`/`edge_type`, so
everything came back null. The P6 agent held its ground with 3 independent verifications + a verbatim
match to the documented todos.md S200 residue. Ground truth: **11 book-fab VICTIM_IN-on-non-harm** +
1 dup — the queued S200 sweep. Cleaned via `fab-s200-residue-fix.py` (backup + 11 re-types + 1 dup drop).
Lesson: learn the real schema before asserting a count; the gate/verification is load-bearing.

## Batches 1–3 applied (15 units, sec 04–14 = all pre-Dance)
Global auto-inject first (66 edges + 155 prose, 0 leftover). Then per batch: fresh-verify → surgery →
mint → merge (0 skipped/0 not-found) → refresh → semantic gate PASS → tests → commit.
- **B1** (`3348a66b26`): reign-04/sons-05-p02·p03/prince-06/year-07. FOLD qhorin→volmark-conspiracy;
  4 PART_OF landed, **2 dropped** — the batch's key learning: **mint quote-validates every edge**, so a
  structural PART_OF needs a locatable verbatim quote (reuse a child role-edge quote, else drop).
- **B2** (`344af9979d`): surfeit-08-p01·p02/time-09/birth-death-10/dragonstone-11. 2 RENAME
  (brandon-stark-father-of-walton, daenerys-daughter-of-jaehaerys-i — disambiguation). Hit + fixed the
  **orphan-node-file** class: pre-junk-screen reconcile wrote junk .node.md files; re-reconcile dropped
  them from the manifest but not disk → mint manifest guard aborted. Cleaned 18 orphans across all 35 units.
- **B3** (`57a825d1fe`): triumphs-12-p01·p02/long-reign-13/14-p01·p02. 3 FOLD + 4 RENAME (same-named
  Targaryen births). 1 dispute cleared — "Eustace Hightower MEMBER_OF House Hightower" was a
  false-positive (chronicler-name "eustace" matched a *character's* given name).

Built a reusable `scratchpad/fab-apply-surgery.py` (auto-locates unit; FOLD + RENAME) for batches 4–7.

## State at wrap
847 book-fab edges (from S200's 264), 868 event nodes. Batches 4–7 (Dance, 20 units) remain — they
hold ALL 62 dispute-adjudication rows (incl. "Secret marriage of Rhaenyra and Daemon"). Wrapped here:
clean pre-Dance boundary; the Dance adjudication needs fresh context + careful primary-text verification.

## What's next
`progress/continue-prompts/2026-07-07-fab-bulk-reconcile-apply.md` (updated): resume at Batch 4. The
sweep tooling + reusable surgery + `--verdicts` inject path are all built and committed.
