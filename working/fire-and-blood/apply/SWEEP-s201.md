# S201 pre-mint sweep (P1–P6) — advisory-board-mandated deterministic fixes

Convened a 3-lens board at the mint boundary (mint-safety / vocab-governance / process-skeptic).
Verdict: pipeline is non-corrupting but the 4-unit smoke run measured the easy case; ~65–95 bad
elements would ship as-is. **Matt approved: run all 6 fixes, then batch-apply. Non-harm patient
edges → PARTICIPATES_IN.** All fixes deterministic (no LLM). Vocab: DISINHERIT/REGENT/BOUNTY all
LEAVE_HELD (don't block mint).

## Steps (each dry-run reviewed before the real mint)
- [x] **P1 — VICTIM_IN harm-gate** DONE (`HARM_EVENT_SUBTYPES` const; non-harm patient → PARTICIPATES_IN;
      unknown→PARTICIPATES_IN). 141/141 tests. Partition reviewed: 10 HARM / 52 NON-HARM subtypes; safe
      direction (miss→under-claim, never false harm). TWEAK in flight: +`assassination_attempt`→HARM.
- [x] **P2 — junk `character.human` screen** DONE: 17/19 rejected (section titles, locatives, collectives,
      objects/weapons, comma-lists, table artifacts). 2 KEEP: "Aegon (nephew of Maegor)" (real person, ok),
      "the Dragonkeepers, four dragons" (junk → TWEAK in flight: reject leading-lowercase-article names).
- [x] **P3 — disputed⇒in_universe_source** DONE: `derive_in_universe_source` + `assert_disputed_invariant`
      (sys.exit on violation). Cargyll twins backfilled `eustace` (verified vs text). 5 violators fixed.
- [ ] **RE-RECONCILE all 35** into apply dirs (after the 2 tweaks land).
- [x] **P4 — mint edge-dedup** DONE (`mint_enrichment.py` edge-level skip-if-exists on
      (type,src,dst,norm-quote); reuses `norm()`). Analytic: only **1** true same-quote dup across 35 units
      (`SERVES larys-strong→aegon-ii`); other 385 are legit multi-cite. 63/63 + 1457 pytest + 10 new green.
- [~] **P5 — dispute pre-classify** built (`fab-dispute-preclassify.py`, 47 tests). Edge subset cracked
      (67/127 auto). EXTENSION in flight: prose(156)+event(37) kinds → auto-clear flat / needs-read contested.
- [x] **P6 — semantic per-batch gate** DONE (`scripts/fab-semantic-gate.py`, 24 tests). Checks: 0
      VICTIM_IN-on-non-harm (book-fab), 0 junk char.human (book-fab; strips `(son of X)` disambiguator),
      orphan-edges (`--baseline-orphans 67`), dup-edges. Run per batch after `weirwood refresh`.
      **Baseline FAIL = KNOWN S200 residue** (from the 4 already-applied smoke units, pre-fix): 11
      VICTIM_IN-on-non-harm + 1 dup (`harren-the-red KILLS alyn-stokeworth`). All 35 NEW units clean.
- [ ] **S200-residue cleanup** (before batch 1, so gate baseline is green). CORRECTED (my earlier "0"
      query was buggy — used source/target; real schema is edge_type/source_slug/target_slug/evidence_kind):
      **11 book-fab VICTIM_IN-on-non-harm** (S200 smoke units, = the queued worklog-S200 sweep) → re-type to
      PARTICIPATES_IN: house-targaryen→aenars-exodus[migration]; loren/aegon/sharra→surrender×3; meria→parley
      [negotiation]; vaegon→summoning[council]; criston→appointments×2; aenys/maegor→births×2; maegor→exile.
      PLUS **1 book-fab dup** (`harren-the-red KILLS alyn-stokeworth`) → drop one row. (Gate was correctly
      book-fab-scoped all along; the pass1-reified AGOT VICTIM_IN edges are a separate out-of-scope dataset,
      informational-only.) Cleanup = deterministic edges.jsonl rewrite; needs Matt go (graph mutation).
- [ ] **P7 — dispute-inject** (NEW, discovered mid-sweep): held dispute rows are EXCLUDED from
      candidates.json (reconciler line 255 "never emitted"). Need `scripts/fab-dispute-inject.py` to
      feed RESOLVED rows back: AUTO_CLEAR→tier-1 edge, AUTO_DISPUTED→tier-2 edge, prose→merge-plan bullet;
      resolve src/dst names→slugs via each unit's `matched.jsonl` (+ reconciler resolver fallback);
      unresolvable→leftover-review (no dangling edge); reuse reconciler edge-build helpers for format
      lockstep. Run GLOBALLY for the 255 auto-resolved rows after re-reconcile; per-batch for the ~63
      needs-read/romance rows after their adjudication. (Book-cite overlay on flat genealogy = high value.)
- [ ] Then batch-apply (7 chronological batches; git checkpoint + mint + merge + refresh + gate per batch).

## Final workload after sweep
- Auto-resolved disputes (deterministic inject): 255 clear + 2 disputed = 257 rows, no human.
- Human/subagent adjudication: 54 needs-read + 9 romance ≈ **63 rows** (was 320).
- CREATE fresh-verify: batch 1 done (1 FOLD, 6 ADD_PARENT); batches 2–7 pending.
- VICTIM_IN flips, junk-node count, dup count: from the post-re-reconcile numbers (consolidated review).

## Board records
- Full board briefs/verdicts: this session's transcript. GATE table: `GATE-s201.md`.
- Already handled: 4 smoke units excluded from batch set; FOLD reign-04 (death-of-qhorin-volmark →
  volmark-conspiracy) confirmed vs primary text; per-batch git checkpoints in plan.
