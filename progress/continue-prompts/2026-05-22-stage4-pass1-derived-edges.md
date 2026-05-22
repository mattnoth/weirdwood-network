# Stage 4 — Pass-1-derived deterministic edge pipeline (build the spine, then the LLM tail)

> **Recommended model:** Sonnet 4.6 for the deterministic Python spine (parser/candidate-gen/locator) AND the LLM tail typing (smoke-test first). **Opus 4.7** only for a validation/weird-result review pass once edges exist. Do NOT use Opus for per-item typing.
> **Full design:** `working/stage4-pass1-derived-edges-design.md`. **Trust worklog.md over this prompt if they differ** (CLAUDE.md #9).

## The pivot (Session 65, 2026-05-22)

Stop having the LLM hunt relationships in wiki prose. Use our Pass 1 extractions, which already contain a `## Relationships Observed` table (pair + free-text hint + evidence sentence) per chapter. Python parses + types most of it; the LLM only types the idiosyncratic tail. Edges carry verbatim `file:line` citations. This deprecates the 29,259-candidate wiki chapter-summary comention pass.

## What was MEASURED this session (real numbers — don't re-derive)

Built + ran `scripts/stage4-pass1-hint-inventory.py` (151 tests green). Outputs: `working/stage4-hint-inventory.md` (all phrases), `working/stage4-hint-residue.md` (the LLM tail).

- **344/344 chapters** have a `## Relationships Observed` table (100%).
- **7,348 relationships** total = **4.6× the old pass1 feed** (was 1,597). We were badly under-mining our own extractions.
- Distinct hint phrases: 4,767; **85% appear exactly once** (idiosyncratic).
- **Deterministic coverage: 50.5%** (3,710 rows) — 35.1% exact-phrase map + 15.4pp from a keyword/regex layer.
- **LLM tail: 49.5%** = 3,638 rows / 2,969 distinct phrases.

## Honest recalibration (read before re-hyping)

- The "Haiku barely runs / one-time phrase dictionary" idea is **DEAD**. The tail phrases are context-dependent ("longing for" = MOURNS vs LOVES vs SEEKS depending on the object; "cautious greeting", "eagerness to fight" need the evidence). They need the LLM to **read the evidence sentence**, not just the phrase. So the LLM step is ~per-row, not per-distinct-phrase.
- The breakthrough that **IS** real: (1) primary-source edges (book text, not wiki summaries); (2) the LLM job is ~8× smaller than the wiki path (3,638 vs 29,259) on tiny prompts (phrase + one distilled evidence sentence, not prose); (3) full `file:line` citations; (4) using data we already paid for; (5) ~50% of edges for free.
- Net: a **quality + traceability + moderate-efficiency** win, NOT an LLM-elimination win.

## Build order

1. **Deterministic spine (no LLM, no permission, ~50% of edges + citations):**
   - `scripts/stage4-pass1-edge-candidates.py` — extraction `## Relationships Observed` → candidates `{source, target, hint, evidence_text, chapter_id, section}`; resolve names→slugs (alias-resolver); apply the exact+keyword typer (reuse the map already in `stage4-pass1-hint-inventory.py`).
   - `scripts/stage4-pass1-evidence-locator.py` — match candidate evidence+pair against `sources/chapters/{chapter}.md` → `evidence_quote` + `evidence_ref` (file:line). Fallback to chapter-level cite when no verbatim match.
   - Emit deterministic-typed edges with `evidence_kind: book-pass1` + provenance stamp (run_id/schema_version).
2. **LLM tail (optional, bounded, needs Matt's OK — it's an extraction):** ~3,638 rows, batch ~50-100/call → a few dozen **Sonnet** calls (minutes, modest $). Input per item = pair + hint + evidence sentence; output = locked-vocab type. Smoke-test ~50 first. Conform inline (normalizer + validator).
3. **Opus validation pass** over the combined edges — schema drift, weird mappings, citation spot-check.
4. **Deprecate wiki-comention:** stamp the 130 done files in-data (`status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`) — NOT dir-archiving.

## Carry-over fixes from Session 65 (real, but lower priority than the pivot)

- **24 skipped files** from a dual-run (Frey/Hightower/Tarly, randyll-tarly @177) — regenerate via this pipeline rather than re-running the wiki path.
- **run-summary.json overwrites per-invocation** (only shows last batch); needs cumulative stats + manifest↔disk reconciler.
- **single-instance guard + stop-file race fix** in run-forever.sh — only matters if any heavy LLM bulk run survives the pivot (unlikely).
- **Provenance stamp** (run_id/schema_version/model/produced_at) in every output row — now upstream of everything; also fixes the schema-mixing + archiving-contention class.
- ~31 untracked throwaway scripts (`scripts/classify-*`, `working/classify_*`, etc.) left uncommitted — candidate for `git clean`/rm (ask Matt).

## DO NOT
- Re-launch the wiki chapter-summary comention bulk (deprecated, 29K low-authority candidates).
- Use Opus for per-item typing (overkill); rely on directory names for "superseded" (stamp in-data).
- Refetch wiki. Write graph/nodes/. Run /endsession without explicit permission.
