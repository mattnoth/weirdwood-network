---
session_date: 2026-05-13
session_focus: Stage 4 prose-edge-classifier — Phase 1 (substrate completion)
status: complete
model_used: claude-opus-4-7[1m]
---

# Stage 4 — Phase 1 Substrate Completion

## Status

**Complete.** Phase 1 of Stage 4 v1 landed cleanly: chapter-summary layer added, meta entity type introduced, observability tooling built, vocabulary review surface created. Phase 2 (co-mention generator + Haiku smoke test + bulk classifier run) is the next session.

## Headline numbers

| Metric | Before | After |
|--------|--------|-------|
| `meta.chapter` nodes in graph | 0 (12 mis-typed as `event.battle`) | 344 (= Pass 1 chapter count exactly) |
| Total graph nodes | ~7,967 | 8,052 (delta accounts for 344 added - 12 deleted - extras) |
| Cross-references rows | 91,381 | 161,060 (+69,679 from chapter prose) |
| Edge-candidate survivors | 77,802 | 141,067 (+63,265) |
| Total edge instances in graph | 21,087 | 21,087 (unchanged — chapters land empty-edged; Stage 4 will fill) |
| Edge-type vocabulary | ~100 canonical (58 populated, 42 unpopulated) | **~114 canonical** (58 populated, 56 unpopulated) — 14 new types accepted post-Matt-review |
| Vocabulary subsections | 14 | **15** (new: Magic & Supernatural) |
| Vocabulary-gap questions filed | 0 | 0 (empty-state baseline established) |

Cost so far: **$0** — Phase 1 was all deterministic Python.

## What changed

### Architecture
- `reference/architecture.md` — added new top-level `Meta` parent type + `meta.chapter` leaf. Documents the in-world vs out-of-universe distinction. New Type Reference Table row for `meta.chapter`.

### Scripts
- `scripts/wiki-pass2-build-edge-candidates.py` (NEW, 323 lines) — Stage 4 candidate generator. Walks cross-references.jsonl, filters against existing edges + alias resolver + low-confidence rules. Emits per-source JSONL files. `--plan` / `--apply` modes.
- `scripts/wiki-pass2-chapter-promotion-migration.py` (NEW, ~500 lines) — one-off migration orchestrator. 10 sequential steps including triage, skeleton emission, prose extraction, deletion of mis-typed nodes, promotion, stale-artifact archive, cross-refs rebuild, alias-resolver rebuild, candidate generator re-run.
- `scripts/wiki-pass2-triage.py` — patched. New `CHAPTER_PAGE_RE` regex matches `-Chapter N`, `-Prologue`, `-Epilogue` patterns; high-priority override routes to `meta-chapters-{book}` buckets as `meta.chapter` type. Bypasses category-based fallback that previously mis-routed 12 ASOS chapter pages to `battles-a`.
- `scripts/wiki-pass2-emit-deterministic.py` — patched. Adds `book`, `chapter_number`, `pov_character` frontmatter fields for `meta.chapter` nodes. Two POV regex formats handled (numbered chapters use `--POV <Name>`; prologues/epilogues use `with the POV of <Name>`).
- `scripts/wiki-pass2-promote.py` + 4 other scripts — patched. `meta.chapter` and `meta` added to TYPE_DIR_MAP → routes to `graph/nodes/chapters/`.
- `scripts/build-edge-type-counts.py` (NEW, 530 lines) — observability tool. Parses architecture.md to extract canonical vocabulary, walks all node files, tallies edge-instance counts per type, surfaces drift (types in nodes not in vocab). Outputs `working/wiki/data/edge-type-counts.{json,md}`. **Zero drift currently.**
- `scripts/build-vocab-gap-log.py` (NEW, 468 lines) — review surface. Aggregates `vocabulary-gap` questions from `questions-for-matt.jsonl` files, renders `working/edge-vocabulary-gaps.md`. **0 gap questions filed yet** (baseline established).

### Graph state
- `graph/nodes/chapters/` — NEW directory, 344 nodes, all `type: meta.chapter`, empty `## Edges` sections (Stage 4 will populate). Frontmatter includes `book`, `chapter_number`, `pov_character`. Per-book breakdown matches Pass 1 exactly: AGOT 73 / ACOK 70 / ASOS 82 / AFFC 46 / ADWD 73.
- `graph/nodes/events/a-storm-of-swords-chapter-*` — 12 mis-typed nodes deleted (replaced by `chapters/` versions).
- `working/wiki/data/cross-references.jsonl` — rebuilt, +69,679 rows from chapter prose.
- `working/wiki/data/alias-resolver.json` — rebuilt.
- `working/wiki/data/edge-type-counts.{json,md}` — NEW baseline.
- `working/wiki/data/edge-candidates-{summary.md,stats.json}` — written from candidate generator `--plan` (not `--apply` yet — Phase 2 will re-run `--apply` after co-mention generator added).

### Documentation
- `curation/edge-vocabulary-candidates.md` (NEW + REVIEWED + RESOLVED) — proposed new edge types reviewed by Matt and adopted in-session. 14 new types accepted, 0 rejected. Matt's inline review notes preserved verbatim. Accepted summary table at bottom of file.
- `working/edge-vocabulary-gaps.md` (NEW, empty-state) — will populate as Stage 4 classifier files gap questions.

### Vocabulary expansion (Matt-reviewed and adopted same session)
- `reference/architecture.md` — added **14 new edge types** across 6 subsections + 1 reverse-direction note. New subsection **Magic & Supernatural** (after Identity & Disguise) contains: `WARGS_INTO`, `BONDED_TO`, `SACRIFICES`, `RESURRECTS`, `CURSES`. Existing subsections expanded: Kinship & Family (+`MARRIES_OFF`), Political & Authority (+`VOWS_TO`, `BREAKS_VOW`), Military & Conflict (+`POISONS`, `RANSOMS`, `IMPRISONS`), Knowledge & Information (+`TUTORS`, `HEALS`), Prophecy (+`DREAMS_OF`). Reverse-direction note: `FOSTERED_BY` ≡ reverse of `WARD_OF`. Locked-vocab callout updated (96/14-categories → 114/15-categories). All new types are prose-derived only — `scripts/wiki-infobox-parser.py` NOT modified (no infobox source for any of them).
- `.claude/agents/prose-edge-classifier.md` — vocabulary-expansion bullet list updated to include all 14 new types. Added disambiguation-guidance section for the trickier pairs: HEALS vs RESURRECTS, TEACHES vs TUTORS, VOWS_TO vs SWORN_TO, WARGS_INTO vs BONDED_TO, KILLS vs POISONS vs EXECUTES vs SACRIFICES, IMPRISONS vs CAPTURES, DREAMS_OF vs FORESHADOWS. Stale 96/14 counts updated to 114/15.
- `scripts/build-edge-type-counts.py` — re-run confirms 114 canonical types, 58 populated, 56 unpopulated, zero drift.

### Cleanup
- `working/wiki/pass2-staging/_archive/triage-bucket-assignments-2026-05-13-pre-chapter-migration.jsonl` — stale triage artefact archived (was showing chapter pages as `event.battle`).
- `working/wiki/pass2-buckets/battles-a/_archive/` — 24 stale chapter artefacts moved out of battles-a bucket.
- `working/wiki/pass2-buckets/battles-a/MIGRATION-NOTE.md` — explains the bucket's `validation-failed` status was resolved by the migration.

## What's next (Phase 2)

Continue prompt updated at `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` with Phase 2 instructions.

**Phase 2 components:**
1. **Co-mention candidate generator** — new script that walks chapter prose, emits entity-pair candidates `{entityA, entityB, chapter_evidence, snippet}` for pairs co-occurring in the same paragraph. Different shape from the existing edge-candidate generator (which is source→target).
2. **Pass 1 relationships candidate generator** — new script that walks Pass 1 extraction `Relationships Observed` tables, emits structured candidates with Pass 1 chapter evidence.
3. **Classifier prompt adaptation** — `.claude/agents/prose-edge-classifier.md` updated to accept 3 candidate shapes (self-referencing, co-mention, Pass 1 relations).
4. **Haiku 4.5 smoke test** — change classifier `model:` frontmatter to `haiku`, run on 3 representative buckets, run `prose-edge-reviewer`.
5. **Bulk run** — if smoke passes CLEAN/CONCERNS-low, run full corpus on Haiku.
6. **Promotion** — write `wiki-pass2-promote-prose-edges.py` to read JSONL output and append accepted edges to `## Edges (prose-derived)` subsections.

**Open question for Phase 2 start:** review `curation/edge-vocabulary-candidates.md` before classifier runs. Any types accepted → add to architecture.md before bulk run so the classifier can emit them.

## Notes / lessons

- **Chapter-summary substrate matters more than initially thought.** First instinct was "defer to v2"; Matt pushed back. The 337 (then 344 including prologues/epilogues) chapter pages add the *per-chapter narrative layer* that's structurally the right substrate for prose-derived edge extraction. Without this, Stage 4 would have run against character/house/location pages only — missing the where most causal/perception/narrative edges live in narrative summaries.
- **Type design**: `meta.chapter` (new `Meta` parent) is the right choice over forcing chapter-summaries into the `Event` hierarchy. Chapters are out-of-universe literary containers; battles are in-world singular happenings. The 12 mis-typed `event.battle` chapter nodes were proof of the type abuse.
- **POV resolution** for all 7 prologue/epilogue pages worked cleanly via wiki categories — those 7 are the famous one-shot POVs (Will, Cressen, Chett, Pate, Varamyr, Merrett, Kevan). Good signal that the category extraction is reliable.
- **Cost reality**: candidate count jumped 77.8k → 141k with chapter substrate. On Haiku 4.5 this is still budget-friendly (~$30-50). On Sonnet ~$300-500. On Opus ~$1500-3000. Haiku smoke test is the right starting point.
- **Vocabulary expansion is overdue**: 42 of 100 types are unpopulated. The unpopulated set is heavily concentrated in perception (`FEARS`, `RESENTS`, `MOURNS`), prophecy (`FULFILLS`, `APPEARS_TO_FULFILL`), narrative (`FORESHADOWS`, `ECHOES`, `PARALLELS`), and causal (`MOTIVATES`, `TRIGGERS`, `ENABLES`) — exactly the categories that need prose reading, not infobox extraction. Stage 4 is targeted precisely at these gaps.

## Watcher signal

This session's work was orchestrator + script-builder (3 delegations, all returned clean). No multi-window orchestration; sequential dispatch. Migration `--apply` ran in background while script-builder built observability tools in parallel.

**Phase 2 should NOT auto-start** — wait for Matt to review `curation/edge-vocabulary-candidates.md` first.
