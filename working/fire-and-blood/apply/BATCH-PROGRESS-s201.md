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
- [x] **Batch 4** (14–16, Dance opens) — long-reign-cont-14-p03/p04, heirs-15-p03, blacks-greens-16-p01/p02.
      DONE S202, committed `d6db5999ae` (surgery checkpoint `5eff1e3ac3`). +322 edges (book-fab 847→1,169),
      26 nodes. 2 FOLD (both Myrish fragments → myrish-bloodbath, extends the S200 fold precedent) + 3 RENAME
      (daella/daeron/alyssa disambiguations). 13 dispute rows: 12 clear / 1 disputed (larys-strong MEMBER_OF
      the-greens, gyldayn-synthesis — the book itself frames his loyalty as unknowable). Saera LOVER_OF ×3 =
      clear via her direct confession (14-p03:217), NOT the "favorites" euphemism class. Orchestrator rejected
      one subagent flag (viserys AGENT_IN tongue-removal is book-correct — the show timeline was the confusion).
      fab-apply-surgery.py promoted scratchpad→scripts/. Gate PASS. 153 tests.
- [x] **Batch 5** (17, Dance war) — red-dragon-17-p01/p02/p03/p04. DONE S202, committed `08c94d699b`
      (checkpoint `pre-batch-5`). +191 edges (book-fab 1,169→1,360), 14 nodes. 1 FOLD: the flagged
      "Aegon (nephew of Maegor)" char CREATE = Aegon the Uncrowned → aegon-targaryen-son-of-aenys-i
      (resolver missed the parenthetical name-form). 14 dispute rows: 12 clear / 2 drop (Addam/Alyn
      SAME_AS = self-loops; both Hull names already alias to the -velaryon slugs). 1 inject-leftover
      (unresolvable CREATE name) wired manually as DISP-M1 with final slugs. **Haiku A/B PASS** for both
      subagent roles (fresh-verify caught the fold + Hull identity; all excerpts verified verbatim) →
      batches 6–7 run on Haiku. Residue noted for close-out: KNIGHTED_BY direction convention is
      knighter→knightee in 4/5 existing edges; rickard-redwyne edge is the inversion outlier. Gate PASS.
- [x] **Batch 6** (18–21, Dance end) — rhaenyra-18-p01/p02, short-sad-19, hour-of-wolf-20, hooded-hand-21.
      DONE S202, committed `6768e67679`. +256 edges (book-fab 1,360→1,616), 21 nodes. 2 FOLD accepted
      (flight-of-queen-rhaenyra→flight-to-dragonstone; formation→selection-of-the-regency-council);
      **2 subagent FOLDs REJECTED** (Hugh Hammer coronation+death stay as beat nodes — the agent invented a
      "sub-events stay in battle nodes" convention that contradicts beat-reification; coronation also predates
      the battle). 26 dispute rows → 23 clear / 2 disputed / 1 drop, with 3 orchestrator overrides:
      R4 garth BETRAYS →clear (Mushroom zone over-extended), R23 benjicot ALLIES_WITH →clear (joining is flat,
      only motive contested), R9 larys KILLS aegon-ii →DROP (hand explicitly unknowable; behest = inference).
      **Event-residue queued for close-out: mint death-of-aegon-ii + larys SUSPECTED_OF whodunit** (no death
      event node exists; not in deferred sidecar either). Eustace-as-character rows map correctly to
      eustace-dance-of-the-dragons. Gate PASS. 153 tests.
- [ ] **Batch 7** (22–25, aftermath+appendix) — war-peace-22-p01/p02, voyage-alyn-23, lysene-24-p01/p02, lineages-25.

## Close-out (after batch 7)
Lineages-appendix validation diff; review-bucket triage; harvest-queue drain; un-park strip track;
worklog S201 entry; deferred-events (37 rows in dispute-events-deferred.jsonl) triage; chat-bundle rebuild rides next deploy.
