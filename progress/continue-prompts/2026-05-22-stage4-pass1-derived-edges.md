# Stage 4 — build the Pass-1-derived deterministic edge pipeline

> **Recommended model:** Sonnet 4.6 for the Python build (parser/locator/typer-map + tests). Haiku only for the novel-hint tail. Opus 4.7 for a validation/schema-drift/weird-result review pass once data exists.
> **Full design:** `working/stage4-pass1-derived-edges-design.md` (read this first — it has the schema, worked example, and rationale).

## What changed (Session 65, 2026-05-22)

Major pivot. We stop having the LLM hunt relationships in wiki prose and instead use the relationships **already extracted** in Pass 1's `## Relationships Observed` tables (one real Arya chapter has 14). Python does parsing + verbatim-locating + common-hint typing; the LLM only labels the novel free-text hint tail. This replaces the 29,259-candidate wiki-chapter-summary comention pass (lowest authority, biggest sink), grounds edges in primary text, adds `file:line` citations, and collapses LLM usage.

**Trust worklog.md over this prompt if they differ** (CLAUDE.md rule #9). See worklog Active Decisions: "Stage 4 pivots to Pass-1-derived deterministic edge pipeline (2026-05-22)."

## Build order

1. **PARSER** — `scripts/stage4-pass1-edge-candidates.py`: walk `extractions/mechanical/{book}/*.extraction.md`, parse `## Relationships Observed` → candidates `{source, target, hint, evidence_text, chapter_id, section}`. Resolve names→slugs via the existing alias-resolver. Start with Relationships Observed only; measure coverage before expanding to Dialogue/Food/Info/Events.
2. **HINT INVENTORY** — dump every distinct `hint` phrase across all 344 extractions; build the deterministic **phrase→vocab map**; measure % typed deterministically (this sizes the Haiku tail).
3. **LOCATOR** — `scripts/stage4-pass1-evidence-locator.py`: match candidate evidence+pair against `sources/chapters/{chapter}.md` → `evidence_quote` + `evidence_ref` (file:line). Fallback to chapter-level cite when no match.
4. **TYPER** — deterministic map first; Haiku (tiny prompt: pair + hint + snippet) only for unmapped hints. Reuse locked vocab + normalizer + validator (conform on write).
5. **DEPRECATE wiki-comention** — stamp the 130 done files in-data (`status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`). Do NOT just move to an archive folder.

## Carry-over fixes (still relevant, lower priority than before)

- **24 skipped files** from the dual-run (Frey/Hightower/Tarly) — regenerate via this pipeline rather than re-running the wiki path.
- **run-summary.json** overwrites per invocation (only shows last batch) → cumulative stats + manifest↔disk reconciler.
- **single-instance guard** + stop-file race fix in `run-forever.sh` — only matters if we keep any heavy LLM run; the pivot makes that unlikely.
- **provenance stamp** (run_id/schema_version/model/produced_at) in every output row — this is now upstream of everything; it also fixes the schema-mixing + archiving-contention class.

## DO NOT
- Re-launch the wiki-chapter-summary comention bulk (deprecated — 29K low-authority candidates).
- Rely on directory names for "archived/superseded" — stamp it in the data.
- Refetch wiki. Write to graph/nodes/. Run /endsession without explicit permission.
