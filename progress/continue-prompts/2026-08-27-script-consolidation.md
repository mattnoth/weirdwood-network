# SESSION 158 — Enrichment script consolidation (kill the disposable-mint clutter)

> **This is Session 158.** Stamp your worklog entry `### Session 158` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Sonnet 4.6 for the mechanical refactor/moves; Opus 4.8 for the parameterized-mint design call + the reproduce-an-old-dip validation.
> **This is a CLEANUP/REFACTOR session, NOT an enrichment dip.** No new edges minted. `/endsession` is NOT pre-authorized here — OFFER it.

## Why this session exists (Matt, S157)
Matt flagged real drift: `scripts/` has accumulated **~33 disposable per-dip `mint_*_enrichment_sNNN.py` + `finalize_*_sNNN.py` scripts** (plus an older pile of `mint_*_arc.py` from S106–S132). They are **prescribed by the machine** (`working/arc-enrichment-backlog.md` "The enrichment-pass machine" step 3 says "mint via `scripts/mint_<unit>_enrichment.py`") — so not rogue — but they are **copy-paste debt**: each is ~95% identical boilerplate (re-grep quotes, backup, re-run guard, slug pre-check via `mint_arc_lib`, append edges, stamp verified_by). The only genuinely per-dip content is **data**: the edge list (`candidates.json`) + any new-node bodies. **Matt: "I cannot stand disposable script clutter... why aren't there generic/reusable scripts? or do one-offs make more sense? if so, organize them into a sub folder."**

The answer (worked out S157): one-offs do NOT make more sense — it's accreted duplication. The fix is a parameterized tool + an archive.

## The task
1. **Audit** — list every per-dip script in `scripts/` (`ls scripts/ | grep -iE 'mint_.*(enrich|arc)|finalize_|stamp_.*arc'`). Confirm the REUSABLE machine you must NOT move/break: `mint_arc_lib.py`, `weirwood-refresh.sh`, `verify-edge-quotes.py`, `graph-query.py`, `build-entity-indexes.py` (these stay in `scripts/`).
2. **Build the parameterized pair** (the real fix):
   - `scripts/mint_enrichment.py` — reads a `--candidates <path>` JSON (the `{_meta:{run_id, new_node_slugs, ...}, edges:[...]}` schema already used by every dip's `candidates.json`) + optional node-body files; does the SHARED steps (slug pre-check, re-run guard, quote re-grep/fail-fast, backup, append edges, create nodes). New-node bodies become DATA (e.g. a `nodes/` array in candidates.json or sibling `.node.md` templates), not embedded Python.
   - `scripts/finalize_enrichment.py` — reads a `--verdicts <path>` JSON (drops by candidate_id, note patches, verified_by stamp, optional edge re-points/bug-fixes) so the fresh-verify adjusts are data too.
   - **Validate by reproduction**: pick a recent dip (e.g. S157 euron `working/enrichment/euron/candidates.json`, or S156 dorne) and confirm the parameterized mint produces **byte-identical** edge rows to what's already in `edges.jsonl` for that run_id (diff the JSON objects, ignoring order). This proves the generic tool is faithful before you trust it. Do NOT re-mint into the live graph — validate against the existing rows / a temp copy.
3. **Archive the disposables** — `git mv` the ~33 enrichment `mint_*`/`finalize_*` + the older `mint_*_arc.py` pile into **`scripts/enrichment/archive/`** (KEEP them — they're frozen records, never delete; same "keep everything" rule as extraction archives). Leave a short `scripts/enrichment/README.md` pointing to the parameterized pair as the going-forward path + noting the archive holds the historical per-dip scripts.
4. **Update the machine docs** so future dips use the generic tool: `working/arc-enrichment-backlog.md` "The enrichment-pass machine" step 3 (mint via `scripts/mint_enrichment.py --candidates …` instead of a fresh per-dip script) + any dip continue-prompt template language. This stops the clutter from re-accreting.
5. **Worklog + commit.** Update `worklog.md` S158 entry; this is a refactor (no graph mutation). Stage by path.

## DO NOT
- Delete any disposable script (archive, don't delete — frozen records).
- Move/rename the reusable machine (`mint_arc_lib.py`, `weirwood-refresh.sh`, `verify-edge-quotes.py`, `graph-query.py`, `build-entity-indexes.py`).
- Mint or mutate any graph edges/nodes (validation is diff-only against existing rows / a temp copy).
- `git add -A` (D&E Pass-1 still PARKED — stage your own files by path).
- Touch the SIFT track (DEFERRED until after enrichment — `project_sift_deferred`).

## Read first
- `working/arc-enrichment-backlog.md` "The enrichment-pass machine" + the Ledger · `scripts/mint_euron_enrichment_s157.py` + `scripts/mint_dorne_enrichment_s156.py` (two recent exemplars — see how identical they are) · `scripts/mint_arc_lib.py` (the one shared helper already extracted) · `working/enrichment/euron/candidates.json` (the data schema the generic tool consumes).

## After this session
Resume the 🅰 A-roundup at **A2.6 Jaime / Riverlands** (the next enrichment dip — Harrenhal, the Riverrun siege resolution, Edmure's surrender, the Blackfish's escape, the burning-of-Cersei's-letter rupture; overlaps RW pass-2 Riverrun-siege). Then A2.4 Tyrion-Essos → A2.5 WO5K-battles [LAST, multi-pass] → A2.8 Davos/Sam residual.
