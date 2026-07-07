# Strip "from the AWOIAF wiki" boilerplate from node Identity prose

> **Track:** graph cleanup (parallel-safe with the F&B build track — touches different code/nodes). Not S-numbered until you pick it up; stamp the worklog entry with the next free graph S-number.
> **Recommended model:** **Sonnet** — deterministic script work (a sweep + an emitter patch); no reasoning model. Haiku only if you choose to compose real lines for thin character stubs (reuse the composer's gated `--enrich-thin` path).
> **Gate:** building/dry-run is a go. **Node writes + emitter edits need Matt's explicit go on the dry-run** (`feedback_no_graph_mutation_without_goahead`).

## Why (Matt, S197): "this should be removed everywhere at some point"
The Pass-2 deterministic emitters stamp a boilerplate Identity line — `"<Name> is a <type> from the AWOIAF wiki."` **6,739 nodes across EVERY entity type still carry it** (2,975 characters, 1,081 locations, 528 titles, 344 chapters, 338 events, 297 houses, 281 artifacts, … 2 prophecies), and **1,079 have a wordier parenthetical gloss** (e.g. `"…is an artifact (named weapon, ship, or object) from the AWOIAF wiki."`). It **ships live in the chat-UI bundle**. **Safe to remove — no provenance loss:** wiki-origin is captured structurally in the `wiki_source` frontmatter + confidence tier + cite_refs, not the prose phrase.

## Scope check first (deterministic)
```
grep -rl "from the AWOIAF wiki" graph/nodes/ | wc -l          # current count (was 6,739 at S197; S197 already fixed clusters + 37 marquee singletons)
grep -rh "from the AWOIAF wiki" graph/nodes/ | sed 's#.*is a##' | sort | uniq -c | sort -rn | head   # the type-gloss variants
```

## Two-part fix
1. **Sweep existing nodes** (dry-run → Matt's go → apply → `weirwood refresh` + bundle rebuild):
   - **Characters / rich nodes with discriminators:** reuse `scripts/wiki-prose-identity-composer.py`. It already composes real Identity lines from infobox edges + `page-categories.jsonl`; S197 shipped `--compose` (clusters) + `--compose-singletons` (curated list). **Add a full-sweep mode** (all boilerplate/absent character nodes not in a cluster — the deferred "full singleton sweep") so the phrase is replaced by real content, not just stripped.
   - **The thin long tail across ALL types** (locations/titles/texts/… and character stubs with no infobox discriminators): a deterministic **strip** is the floor — remove the "… from the AWOIAF wiki" tail + the parenthetical type gloss. **DECISION FOR MATT (put it in the dry-run):** target shape — `"X is a <type>."` (strip only), or drop the contentless Identity line entirely, or leave a minimal composed stub? Recommend showing him 2–3 sample rows of each before applying.
2. **Patch the emitters** so future mints stop generating it — the phrase is hardcoded in ~8 Pass-2 scripts: `scripts/wiki-pass2-tier3-pathb-orgs.py`, `wiki-pass2-tier3-pathb-texts.py`, `wiki-pass2-tier3-pass-a-titles.py`, `stage3-preview-emit.py`, `wiki-pass2-bucket-a-backfill.py`, `wiki-pass2-chapter-promotion-migration.py`, `graph-cleanup-2026-06-14.py` (has a matcher, not an emitter — check), plus any others `grep -rn "from the AWOIAF wiki" scripts/` surfaces.

## Close
`weirwood refresh` (Identity text is searchable) + rebuild the chat bundle so the live UI drops the phrase. Update the worklog backlog item (HIGH, logged S197) to done. Additive/atomic writes; git-checkpoint before apply (graph/nodes clean at HEAD is the rollback point).

## DO NOT
- Do NOT write `graph/nodes/` or edit emitters without Matt's go on the dry-run.
- Do NOT touch `wiki_source`/tier/cite_refs (that's where provenance actually lives).
- Do NOT re-fetch the wiki. Do NOT auto-run /endsession.
