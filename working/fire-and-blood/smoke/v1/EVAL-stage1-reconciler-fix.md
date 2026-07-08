# Stage-1 reconciler-fix verification — `fab-aegons-conquest-03` (S199)

Applied the 5 EVAL blockers to `scripts/fab-reconcile-candidates.py` (+ lockstep mint patch) and
re-ran the reconciler on the SAME Stage-1 proposal (deterministic, `--smoke`, no API $, nothing minted).
Fresh output: `working/fire-and-blood/smoke/v1/recon-after/`. Build-time tests: `scripts/test-fab-reconcile.py`
(**23/23 pass**, incl. the R1 trap + every fix).

## Before → after (same proposal, same `--smoke`)

| metric | before (S198 EVAL) | after (S199) | note |
|---|---|---|---|
| matched (UPDATE) | 39 | 39 | unchanged — clean hits still UPDATE |
| review | 108 | 134 | dupes/fuzzy now correctly deferred (smoke sends all uncertain → review) |
| **created** | **36** | **6** | **~19 were dupes/junk; all 6 remaining are genuinely-new `event.*`** |
| quotes located % | 89.6 | **96.7** | wrap-aware locator recovered 10 of 14 line-wrap false-negatives |
| quotes quarantined | 14 | 4 | 1 empty-quote edge + 3 genuine extractor punctuation deviations (NOT locator gaps) |
| edge candidates | 58 | 51 | composites/collectives no longer emit junk-target edges |
| disputed_rate | 0.034 | 0.020 | (fewer edges; same 2 real hedges) |
| **trap edges / merges** | **0** | **0** | R1 holds — `aegon-targaryen` appears 0×; 24 edges → `aegon-i-targaryen` |

## The 5 fixes (all in `fab-reconcile-candidates.py` unless noted)
1. **CREATE guard** — CREATE only on a confidently-empty `miss` (slug None AND no fuzzy candidates). Any
   `candidates`/`ambiguous` status → review (killed `daenys`→`daenys-targaryen`, `arrec`→`arrec-durrandon`).
   De-pluralize + `house-<singular>` probe → the **9 house dupes** (`blackwoods`→`house-blackwood`, …) now
   route to review with the existing house node as the candidate. Existing-slug backstop.
2. **Composite/collective split** — `;`/`/`/`&`/`and`-joined event agent/patient/location cells split into
   individuals before resolution (two role edges, not one joined node); collective military referents
   (`the Targaryen fleet`, `Aegon's host at …`) → review. **7 junk nodes gone.**
3. **Wrap-aware quote locator** — `locate_quote` joins up to 4 consecutive lines (blank-line paragraph gaps);
   **mirrored byte-identically in `mint_enrichment.authoritative_line`** (lockstep — else a reconciler-located
   quote aborts mint). Locator gap closed; residual 3 are genuine fidelity misses (below).
4. **Contradictions report** — added `MULTI_VALUED_TYPES` (a parent has many children; polygamous spouses):
   a *different target* is no longer flagged for those. Report is now **1 genuine flag** (`edmyn-tully SWORN_TO
   harren-hoare` per F&B vs `house-tully` per wiki — a real Conquest allegiance nuance), zero dupe-bug noise.
5. **Type guess carried** — roster `Type guess` → CREATE `type:` (was already wired; fixes 1–2 removed the
   place/collective-as-`character.human` mints). All 6 CREATEs are correctly-typed `event.*`.

## Event-type-aware routing (discovered during re-run — NOT in the original 5)
The resolver returns fuzzy `candidates` for most event names. For **characters** a fuzzy candidate = dupe risk
(→ review). For **events** the fuzzy matcher surfaces the persons/places an event merely involves. So event
routing now defers to review ONLY when a candidate is itself an existing `events` node (real dedup risk), else
CREATEs. This CAUGHT MORE DUPES than the EVAL: `Submission of Rosby`~`yielding-of-rosby`,
`Surrender of Storm's End`~`taking-of-storms-end`/`siege-of-storms-end`, `Battle at the Wailing Willows`~
`wailing-willows` are all **existing `event.battle` nodes** the old code would have duplicated. (The "~14 CREATEs"
estimate in the continue prompt assumed all events were new; several were event-vs-event dupes.)

## Residual quarantine (4) — all correct, none a bug
- 1 empty-quote edge: `Meria Martell OPPOSES Aegon I Targaryen` (extractor gave no evidence quote → not minted).
- 3 extractor punctuation deviations that break verbatim match (would abort mint — correctly flagged):
  `Dorne,”` quoted as `Dorne"` (dropped comma inside the close-quote, ×2); source OCR `Aegon’'s`
  (doubled apostrophe) normalized by the extractor to `Aegon's` (×1). Harvest/extraction note, not a reconciler
  or prompt blocker — 96.7% clears the 90% gate.

## Fresh-verify (general-purpose subagent, read-only) — 5 of 6 CREATEs safe, 1 semantic dupe
The slug-level dupe check is clean (0/6 collide). A fresh adversarial pass on **semantic** equivalence found:
- **`aegons-second-coronation` = DUPE-RISK of existing `aegons-coronations`** (that node's identity already
  covers BOTH crownings incl. the second / Oldtown anointing). The resolver didn't fuzzy-surface it, so it
  slipped through as a clean miss. **This is exactly why design §5.1 mandates the `duplicate-detector` agent
  over each CREATE batch before mint** — the deterministic reconciler cannot catch semantic dupes the resolver
  doesn't surface. Nothing minted (apply gated) → no harm. **Disposition at apply: fold into `aegons-coronations`
  (UPDATE), don't CREATE.**
- The other 5 are safe to create. Subagent note: `capture-of-loren-lannister`, `torrhen-starks-kneeling`,
  `rhaenyss-parley-with-meria-martell` are narrated inside broader nodes (`field-of-fire`, `conquest-of-dorne`)
  — safe as granular nodes per the per-event convention, but want `PART_OF`/`CAUSES` edges back to the parents.

## Gate for Stage 2 / apply
Reconciler blockers are **cleared**. Before any real mint: (a) run the `duplicate-detector` (or a fresh-verify)
over each unit's CREATE batch — it just caught a real one; (b) the architecture batch + both mint patches land
with Matt's apply-go (`working/fire-and-blood/architecture-batch-s198.md`). Extraction prompt untouched (it passed).
