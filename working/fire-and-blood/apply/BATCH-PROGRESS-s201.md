# S201 batch-apply progress

Pre-mint sweep (P1–P7) COMPLETE. S200 residue cleaned (11 VICTIM_IN→PARTICIPATES_IN + 1 dup).
Global dispute auto-inject applied (66 edges + 155 prose across 35 units). Gate baseline PASS.

Per-batch rhythm: fresh-verify → surgery (folds/renames; PART_OF needs a **locatable verbatim quote** —
reuse a child role-edge quote or drop) → mint (per unit) → merge (0 skipped/0 not-found) →
`weirwood refresh` → `fab-semantic-gate.py --baseline-orphans 67` (PASS) → `test-fab-reconcile.py` → commit.

Dispute adjudication: 63 needs-read/romance rows total, ALL in the Dance batches (4–7). Batches 1–3 have 0.

## Batches
- [x] **Batch 1** (04–07) — reign-04, sons-05-p02/p03, prince-06, year-07. DONE, committed `3348a66b26`.
      ~261 edges, ~30 event nodes. FOLD qhorin→volmark-conspiracy; 4 PART_OF landed, 2 dropped
      (murmison, aegon-uncrowned-seizes — no locatable quote; re-add later if grounded). Gate PASS.
- [x] **Batch 2** (08–11) — surfeit-08-p01/p02, time-of-testing-09, birth-death-10, jaehaerys-dragonstone-11.
      DONE, committed `344af9979d`. 174 edges + 35 nodes. 33 KEEP / 2 RENAME (brandon-stark-father-of-walton,
      daenerys-daughter-of-jaehaerys-i disambiguations) / 0 FOLD. Gate PASS.
      **Also removed 18 orphan junk .node.md files** (pre-junk-screen reconcile residue that tripped the mint
      manifest guard) — this cleanup already applied to ALL 35 units, so later batches won't hit it.
- [x] **Batch 3** (12–14) — triumphs-12-p01/p02, long-reign-13, long-reign-cont-14-p01/p02.
      DONE, committed `57a825d1fe`. 149 edges + 44 nodes. 40 KEEP / 3 FOLD / 4 RENAME. 1 dispute cleared
      (Eustace Hightower MEMBER_OF = false-positive: "eustace" matched a character name). Gate PASS.
      **← BATCHES 1–3 DONE = all pre-Dance (sec 04–14). RESUME AT BATCH 4.**

## Reusable surgery tool (built S201)
`scratchpad/fab-apply-surgery.py --spec <spec.json> [--apply]` — auto-locates each slug's unit; handles
FOLD (drop CREATE + retarget edges + delete node file) and RENAME (rename slug + node file + retarget).
Spec = `[{"action":"FOLD"|"RENAME","old":"<slug>","new":"<slug>"}]`. Dry-run default. Used for batches 2 & 3.

## Learnings for the Dance batches (4–7)
- **PART_OF needs a locatable verbatim quote** — reuse a child's role-edge quote (from candidates.json edges
  whose `target` is the child + has a `quote`), else drop the ADD_PARENT.
- **Orphan-node cleanup already done** across all 35 units (the junk .node.md files).
- **Disambiguation traps**: this era has many same-named Targaryens/Starks; verify birth-/death-of char slugs.
- **Dispute adjudication** (62 remaining needs-read/romance rows, all in batches 4–7): per the S200 pattern,
  fresh subagent verdicts BUT orchestrator verifies tags vs primary text (2 of 4 S200 subagent clears were
  wrong). Watch the "eustace"/"mushroom" false-positive class (chronicler name == a character's given name).
  Use `fab-dispute-inject.py --verdicts <file>` to apply verdicts (clear/disputed/drop).
- [ ] **Batch 4** (14–16, Dance opens) — long-reign-cont-14-p03/p04, heirs-15-p03, blacks-greens-16-p01/p02.
      DISPUTE-HEAVY (heirs-15-p03 alone has many needs-read incl. "Secret marriage of Rhaenyra & Daemon").
- [ ] **Batch 5** (17, Dance war) — red-dragon-17-p01/p02/p03/p04. Dispute-heavy. Also verify the odd
      "Aegon (nephew of Maegor)" char CREATE in 17-p01.
- [ ] **Batch 6** (18–21, Dance end) — rhaenyra-18-p01/p02, short-sad-19, hour-of-wolf-20, hooded-hand-21. Dispute-heavy.
- [ ] **Batch 7** (22–25, aftermath+appendix) — war-peace-22-p01/p02, voyage-alyn-23, lysene-24-p01/p02, lineages-25.

## Close-out (after batch 7)
Lineages-appendix validation diff; review-bucket triage; harvest-queue drain; un-park strip track;
worklog S201 entry; deferred-events (37 rows in dispute-events-deferred.jsonl) triage; chat-bundle rebuild rides next deploy.
