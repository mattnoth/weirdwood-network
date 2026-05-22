# Session 65 — Stage 4 dual-run forensics → Pass-1-derived edge pipeline pivot (2026-05-22)

**Model:** Opus 4.7 (analysis + design conductor); script-builder (Sonnet) for the hint-inventory tooling.

**Shape:** Started as "resume the bulk + add a guard" (per the S64 handoff). Matt redirected to analysis ("how's Haiku doing, analyze edges, compare to previous runs, see how schema restrictions help"). That analysis surfaced real integrity bugs, then a design conversation that pivoted Stage 4's whole approach. This was a thinking/design session, not execution.

## 1. The "every time we add a clock, you report a bug" thread

Matt's framing was correct and is the through-line of the session. The bugs cluster in the **multi-invocation orchestration scaffolding**, not in Haiku's output:

- **`run-summary.json` is overwritten every invocation** (`stage4-haiku-run.py:1233`), and the loop calls the runner once per batch — so the "run summary" only ever reflects the *last* batch ($0.45 / 1 batch) while the real run was 60 batches / $55.66 (recoverable only by summing `results/*.json`). Monitoring read a file that structurally couldn't tell the truth → phantom alarms.
- **Stop-file delete-race** + **dual-run** (below) are the same class: state passed *between* invocations is the weak link.
- Contrast S63's "5 of 30 files missing!" which was a pure false alarm (batch spanned 3 buckets, I checked one).

Lesson reinforced: decompose before alarming.

## 2. Edge analysis + the comparison correction (Matt caught me asserting blind)

First-pass comparison (Sonnet `prose-edges/` 890 files vs current Haiku `prose-edges-haiku/` 201): emit rate "converging toward Sonnet." **Wrong** — I'd labeled dirs by name and compared *different bucket sets*. Matt: "that's exactly the kind of unverified assumption that could make my comparison garbage."

- Provenance verified by mtime: Sonnet 05-13→18, prior Haiku (v164) 05-20→21, current 05-22 — cleanly separated, no contamination.
- **Bucket-matched** (120 entities both classified): Sonnet 33.3% emit / KNOWS=150 (its #1) ; current Haiku **24.6% emit / KNOWS=0**. So Haiku is *more conservative* than Sonnet, not converging; KNOWS deprecation holds strongly; Haiku reallocates toward structural edges (LOCATED_AT 54→183).
- Saved a hard rule to memory: `feedback_verify_dataset_provenance` (verify by mtime/manifest, bucket-match, break out deprecated types, prefer a script over ad-hoc find-pipes).

Genuine violation rate on the current corpus decomposed to ~1% real semantic errors (the headline 5.2% was inflated by one malformed bucket + qualifier-backfill).

## 3. Integrity finding: 24 skipped files (Matt's instinct was right)

Reconciling the Sonnet manifest (authoritative file list) against disk for the 60 done batches: the batches map to 350 files; **326 exist, 24 are missing** — all source_target character files (Frey/Hightower/Tarly), all with real candidates (randyll-tarly @177 rows, ryman-frey @90), all reporting `failed: 0`. Cause: the **dual-run** — a second `run-forever` chain launched at 04:36 (Matt confirmed he didn't start it; no crontab/launchd) from `batch-0019` position 1, both chains writing the same output paths with no isolation, one SIGTERM'd mid-flight. Concurrent writes + kill = clobbered files; the accounting (overwritten result JSON + no manifest↔disk check) hid it.

Also discovered: my "201 files / 5,723 rows" was source_target-only — the glob `*.edges.jsonl` excluded 130 `*.comention-edges.jsonl`. True on-disk total 331; my entire edge analysis had silently excluded the comention shape. And the comention output had ~15% pair_a/pair_b shape drift.

## 4. Root cause: provenance is implicit, not architectural

Why archived runs keep getting mixed across schema versions (Matt's recurring pain):
- Output namespace keyed by entity slug only — every schema version writes the same `prose-edges-haiku/<slug>` path.
- No provenance stamped in the rows (no run_id/schema/model) — only mtime distinguishes runs.
- Separation depends on a manual pre-run archive `mv` (error-prone; archive dirs inconsistently shaped).
- `--skip-existing` (`stage4-haiku-run.py:614`) skips on mere existence → *preserves* stale-schema files on a partial/un-archived re-run.
Fix direction: stamp provenance **in the data** (run_id/schema_version/model/produced_at) + run-scoped dirs + schema-aware skip. Same fix dissolves the archiving-contention problem.

## 5. The breakthrough — and its honest recalibration

**Idea:** stop having the LLM *hunt* relationships in wiki prose; use the relationships we already extracted. Pass 1 extractions contain a `## Relationships Observed` table (pair + free-text hint + evidence) per chapter. Python parses + types most; the LLM only types the idiosyncratic tail; a deterministic locator attaches verbatim `file:line` citations. Deprecates the 29,259-candidate wiki chapter-summary comention pass.

**Measured (built `scripts/stage4-pass1-hint-inventory.py`, 151 tests green):**
- 344/344 chapters have the table; **7,348 relationships** (4.6× the old 1,597 pass1 feed).
- Deterministic coverage: **35.1% exact-phrase → 50.5% with a keyword/regex layer**. LLM tail = **49.5% (3,638 rows, 2,969 distinct phrases)**.
- Residue (`working/stage4-hint-residue.md`) is a genuine LLM job: 71% single-use free-form phrases needing the evidence sentence ("cautious greeting", "eagerness to fight") — not more keywords, and not a context-free phrase dictionary.

**Recalibration (Matt pushed; I had oversold):** the "Haiku barely runs / one-time phrase dictionary" framing is dead — the tail is context-dependent and ~per-row. AND "amortizes over future books" is mostly moot (we have all 5 published books; TWOW isn't out). What's *real*: primary-source edges, an LLM job ~8× smaller than the wiki path on tiny prompts, full citations, data we already paid for, ~50% of edges free. It's a quality/traceability/moderate-efficiency win — not LLM elimination.

**Model call:** Sonnet for the tail typing (smoke first); Opus only for a validation/review pass. Opus per-item is overkill.

## 6. Housekeeping

- Committed S64's long-pending work (1,008 data files: bulk output + archive move) + S65 design pivot in two clean commits; pushed (`24dcb812b`, `ac61ff2ee`).
- `git add -A` swept in `.claude/worktrees/` (embedded repos) + `scratch-2.txt` (Matt's private notes) + ~30 throwaway `classify_*` scripts. Excluded all; added `.claude/worktrees/` and `scratch*` to `.gitignore`. ~31 throwaway scripts left untracked (flagged for cleanup).
- Memory written: `feedback_verify_dataset_provenance`, `project_stage4_pass1_derived_pivot`.

## Next session
Build the deterministic spine (candidate generator + locator) → ~50% of book edges + citations at zero LLM cost; then the bounded Sonnet tail (needs Matt's OK) + Opus validation. Continue: `progress/continue-prompts/2026-05-22-stage4-pass1-derived-edges.md`.
