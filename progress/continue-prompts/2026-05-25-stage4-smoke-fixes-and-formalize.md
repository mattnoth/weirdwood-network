# Stage 4 — Smoke fixes → re-smoke → scoped full run → formalize into graph/edges

> **Recommended model:** **Opus 4.7** for the session — it's decisions (A/B/C below) +
> review/coordination. Use **Sonnet 4.6** for the deterministic fixes (prompt/generator
> edits, dedup, merge) and delegate the LLM typing to `claude -p` (Sonnet) as usual.
> Never use Opus for per-item work.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9). Authoritative
> state: worklog Session 69 + the Stage-4 Current-State line.
>
> **Two companion docs, read both before doing anything:**
> - `STAGE4-SMOKE-REVIEW.md` (repo root) — Matt's plain-language review of the smoke
>   findings + the three decisions. Matt may have annotated it or answered A/B/C.
> - `working/wiki/data/pass1-derived-smoke-report.md` — the technical smoke report.
> - The S66/S67 *finishing* prompt `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md`
>   is STILL OPEN — its merge/dedup/resolver-lever work is folded into this prompt's
>   "formalize" track.

## Where things stand (end of Session 69, 2026-05-24/25)

Session 69 mined the four remaining Pass 1 tables and SMOKE-TESTED the LLM typing before
committing to the full run. The smokes worked and **caught systematic, fixable problems —
so the ~$270 full run was deliberately NOT launched.** Nothing irreversible happened;
canonical data is untouched.

**Edge inventory (all still in staging — `graph/edges/` is EMPTY):**
- Deterministic spine: 2,834 `book-pass1` edges (`pass1-derived/{book}/*.edges.jsonl`).
- S67 Sonnet typed tail: 2,385 edges (`pass1-derived/_tail-typed/{book}/` — the
  canonical typed tail; row counts agot 482 / acok 475 / asos 588 / affc 353 / adwd 487).
- S68 Hospitality: 460 `GUEST_OF` + 69 `VIOLATES_GUEST_RIGHT` = 529 (in `_extra-tables/`;
  NOT yet endpoint-filtered, NOT merged).
- S69 NEW candidate rows (untyped, regenerable, gitignored): 32,194 across the four
  tables — Dialogue 4,422 / Events 20,321 / Info 6,653 / Food 798 — in
  `pass1-derived/_extra-tables/{book}/{chapter}.extra-tables.jsonl`.

**What the two smokes (200 rows each, ~$3.60 total, Sonnet) showed:**
- Dialogue: 144 typed (72%) / 56 rejected. Strict precision **~60%**, reject ~89%.
- Events/Info/Food: 123 typed (61%) / 77 rejected. Strict precision **~66%**, reject
  ~91%. **Direction-error ~7%, fan-out spurious-pair ~18%, bare/garbled slugs ~15%.**
- Both reviewer verdicts: **SYSTEMATIC** (patterned, reproducible — not random noise).
- Re-baselined cost: full run ≈ **$270-290** (not the old ~$100); per-row ~$0.009.
- Wall-clock: ~5-7 min / 40-row batch → ~805 batches ≈ **3-4 days sequential** → needs
  the parallel `run-forever` wrapper, not one chain.

## The three decisions (Matt's — may already be answered in STAGE4-SMOKE-REVIEW.md)
- **A. Restricted typing vocabulary.** Keep relationship-revealing types (`SIBLING_OF`,
  `SPOUSE_OF`, `PARENT_OF`, `KILLS`, `DUELS`, `VOWS_TO`, `DISTRUSTS`, `REVEALS_TO`,
  `CONSPIRES_WITH`, `BANISHES`, `FIGHTS_IN`, `BETRAYS`, …); drop/tightly-gate the noisy
  ones (`INFORMS`, `ADVISES`, `MANIPULATES`, `SUPPORTS`, `ALIAS_OF`). Recommended: yes.
- **B. First-run table scope.** Events + Dialogue only; defer Information Revealed (its
  multi-entity rows drive the fan-out noise); Food as a separate small audit.
  Recommended: yes (matches reviewer).
- **C. Full run.** Approve only AFTER the $0 fixes + a ~$4 re-smoke confirm ≥~80% strict
  precision. Decide from the re-smoke numbers, not blind.

## Tracks

### Track 1 — The three $0 fixes (do before any re-smoke; Sonnet/deterministic)
1. **Classifier prompt restriction + anti-patterns** (Decision A). Edit
   `scripts/stage4-tail-classifier.py` `_PROMPT_PREAMBLE` (~line 190) and/or add a
   `--allowed-vocab`/restriction mechanism. Add explicit DO-NOT examples:
   - `INFORMS` — only spy/agent → handler ongoing reporting; NOT generic "told someone"
     (use `REVEALS_TO` for one-time disclosure).
   - `ADVISES` — only genuine counsel from an institutional advisor role; NOT rebukes /
     arguments / objections.
   - `MANIPULATES` — target must be UNAWARE; NOT overt threats/coercion/provocation.
   - `SUPPORTS` — evidentiary/theory layer ONLY; NOT interpersonal political backing.
   - `ALIAS_OF` — NOT title forms of address ("King Robert", "Ser X").
   - Add tier-assignment guidance (stop defaulting 100% Tier-1).
2. **Generator direction-validation + slug-quality gate** in
   `scripts/stage4-pass1-extra-tables.py`. (a) Detect passive constructions / reverse or
   flag direction; (b) route bare titles (`ser`/`lord`/`king`/`maester`), bare surnames,
   nationality demonyms, and known aliases to escalation instead of emitting. **This IS
   the endpoint filter the S67 finishing prompt called for (the `all-for-joffrey` class)
   — it also cleans the 529 Hospitality edges' endpoints. Do it ONCE for everything.**
3. **Provenance fix:** `scripts/stage4-tail-classifier.py:502` hardcodes
   `"candidate_kind": "pass1_relationship"` in `build_emit_edge_row`. Preserve the input
   row's `candidate_kind` instead. (And consider an `evidence_kind` discriminator per the
   architecture's provenance discipline.)
   - Add/extend tests for all three. (Current: 273 green across the two test files.)

### Track 2 — Re-smoke (~$4, needs Matt's standing OK for the spend — it's an extraction)
Regenerate candidates (`python3 scripts/stage4-pass1-extra-tables.py --apply`), then
smoke Dialogue + Events (per Decision B) with the fixed prompt + generator:
```
python3 scripts/stage4-tail-classifier.py \
  --input-dir working/wiki/pass2-buckets/pass1-derived/_extra-tables \
  --candidate-kinds pass1_dialogue,pass1_events \
  --sample-n 200 \
  --output-dir working/wiki/pass2-buckets/pass1-derived/_smoke2 \
  --apply
```
**ALWAYS pass `--output-dir` to a scratch dir** — without it the script appends into the
canonical `_tail-typed/`. Re-audit with `prose-edge-reviewer`. Confirm strict precision
≥ ~80% before recommending the full run.

### Track 3 — Scoped full run (Decision C; ~$200-ish; parallel wrapper; drift-detection)
Only after Track 2 passes. Use `scripts/stage4-run-forever.sh` (survives rate-limit
walls; see memory `project_stage4_run_forever_wrapper` + `project_stage4_sleep_defaults`).
Drift-detection MANDATORY (schema validator + cross-model audit) per the standing rule.
Output to a dedicated typed dir (NOT canonical until reviewed).

### Track 4 — FORMALIZE into graph/edges (the actual milestone; $0; deterministic)
This is the long-pending step (S66/S67/S68/S69 all feed it). After the typed edges exist:
1. Endpoint-filter (Track 1.2) all edge sets including the 529 Hospitality.
2. Tail dedup (the spine emits some duplicate rows) + tail-violation cleanup (21/2,385
   from S67: HOLDS_TITLE→place re-types, ENCOUNTERS verb-gate, SPOUSE_OF qualifier).
3. Merge the spine + S67 `_tail-typed/` + 529 Hospitality + S69 typed tails into
   `graph/edges/` per the `reference/architecture.md` edge convention. Preserve
   `evidence_ref` (source-chapter file:line), `candidate_kind`/`evidence_kind`,
   `typed_by`, and qualifiers.
4. Spot-audit a random sample of the merged set (green tests are NOT correctness proof —
   they missed the `candidate_kind` hardcode, the `all-for-joffrey` class, and the S66/S67
   misresolution bugs). THEN `graph/edges/` is populated and the graph is traversable.

## DO NOT
- Launch the ~$270 full run before the re-smoke confirms ≥~80% precision.
- Run ANY typing pass without `--output-dir` pointing at a scratch dir (you will append
  into canonical `_tail-typed/`).
- Merge the 529 Hospitality edges (or any edges) into `graph/edges/` before the endpoint
  filter (Track 1.2) — you'll import `all-for-joffrey`-class junk endpoints.
- Re-run any LLM tail without the ENCOUNTERS Rule-6 verb-gate (now in the prompt) AND the
  Track-1.1 anti-patterns.
- Mutate `working/wiki/data/alias-resolver.json` (use the supplementary-alias path).
- Relaunch wiki-comention (DEPRECATED, 133 files stamped).
- Trust green tests as correctness — spot-audit random samples.
- Do a full source-chapter re-read pass (deferred enrichment, NOT this work).
- Run `/endsession` without explicit permission.

## Pointers
- Review doc: `STAGE4-SMOKE-REVIEW.md` (root).
- Smoke report: `working/wiki/data/pass1-derived-smoke-report.md`.
- Smoke output (gitignored, inspectable): `pass1-derived/_smoke-dialogue/`,
  `pass1-derived/_smoke-events-info/`.
- Finishing prompt (still open): `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md`.
