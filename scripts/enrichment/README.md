# Enrichment minting — the going-forward path

**As of S158 (2026-06-27), enrichment dips no longer get a fresh per-dip mint/finalize script.**
Use the two parameterized tools (they live in `scripts/`, NOT here):

| Step | Tool | Reads | Does |
|------|------|-------|------|
| (pre-flight) | `scripts/quotecheck_enrichment.py <dip>/candidates.json` | the dip's `candidates.json` | OPTIONAL: locate every edge quote in its chapter via the mint's `norm()` (green here ⇒ the mint's own fail-fast line-check passes). Replaces the per-dip `working/enrichment/<unit>/quotecheck.py` clones — do NOT copy one per dip (S159). |
| mint | `scripts/mint_enrichment.py --candidates <dip>/candidates.json` | the dip's `candidates.json` (+ optional `<dip>/nodes/*.node.md`) | slug pre-check · re-run guard · quote re-grep (fail-fast) · backup · create new nodes · append edges |
| finalize | `scripts/finalize_enrichment.py --verdicts <dip>/verdicts.json` | the dip's `verdicts.json` | drop fresh-verify REJECTs · note patches · `verified_by` stamp on `pending` edges · pre-existing-edge bug drop/re-point · backup |

Everything that used to be hand-written Python is now **data**:
- **edges** → the `edges[]` array in `candidates.json` (the schema every dip already wrote).
- **new-node bodies** → `<slug>.node.md` files in a `nodes/` dir beside `candidates.json`; each file's
  `type:` frontmatter routes it to the right `graph/nodes/<dir>/` (no embedded Python).
- **fresh-verify adjustments** → `verdicts.json` (`drop`, `note_patch`, `verified_by`, `bug_drop`, `bug_repoint`).

See each tool's module docstring for the exact JSON schemas and a validation/usage example.

## Why this exists

Through S157 each dip got a copy-pasted `mint_<unit>_enrichment_sNNN.py` + `finalize_<unit>_sNNN.py`.
They were ~95% identical boilerplate — the only genuinely per-dip content was the data above. That
accreted into ~74 disposable scripts (copy-paste debt Matt flagged at S157). The fix: one
parameterized pair + this archive.

**Faithfulness was proven, not assumed.** S158 replayed two real dips through the generic tools and
diffed the output against the live graph **byte-for-byte**:
- **euron (S157)** — 37 edges, 0 new nodes: mint + finalize byte-identical.
- **dorne (S156)** — 39 edges, 3 new nodes, 1 drop, a 2-edge bug-repoint: mint edges + node routing
  + finalize all byte-identical.

## `archive/` — frozen historical per-dip scripts

`archive/` holds the 74 retired one-shot mint/finalize/stamp scripts (the enrichment dips S133–S157,
the older `mint_*_arc.py` spine builds S106–S132, and misc one-shot edge/cleanup mints). **They are
kept forever, never deleted** — same "keep everything" rule as `extractions/archives/`. They are
frozen records of exactly what each dip minted, not runnable tools (their re-run guards abort, and
they can no longer import `mint_arc_lib` from this subdir). To see what a past dip did, read its
script + its `working/enrichment/<unit>/` artifacts + the Ledger row in
`working/arc-enrichment-backlog.md`.

## The reusable machine stays in `scripts/` (NOT archived)

`mint_arc_lib.py` (slug pre-check helper, imported by `mint_enrichment.py`), `stamp_containers.py`,
`weirwood-refresh.sh`, `verify-edge-quotes.py`, `graph-query.py`, `build-entity-indexes.py`.
