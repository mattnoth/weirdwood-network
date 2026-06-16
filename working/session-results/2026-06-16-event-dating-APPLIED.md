# Event Dating — APPLIED (2026-06-16)

> Autonomous run while Matt was away. 4-stance panel weighed the move; risk auditor drew the
> apply/dry-run line; the safe deterministic subset was applied. **No commit, no /endsession** (await Matt).

> **FOLLOW-ON (same session) — `narrative_first` applied; ordering step found to be GATED.**
> Per "recommended next, execute": **`narrative_first` (reading-position axis) is now LIVE** on 29 of the 112
> dated events (the ones with chapter-cited edges; 83 pure-backstory events correctly get none). Built via
> `scripts/backfill-narrative-first.py` (+33 tests) — resolves both edge ref formats (`agot-eddard-01` ≡
> `AGOT Eddard I`) to absolute `(book_order, chapter_number)` via the chapter-file index; **resolve-all-or-skip,
> 0 unresolved**. Red Wedding → `asos-52` (ASOS Catelyn VII), verified. Frontmatter-only, idempotent, bodies
> preserved. pytest **1295 pass / 3 documented fails**. Report: `2026-06-16-narrative-first-dryrun.md`.
>
> **`PRECEDES`/`FOLLOWS` (the planned step 2) is GATED — NOT a deterministic step after all.** Recon found:
> (a) they are NOT in the locked edge vocab and are an *explicitly deferred* schema decision (roadmap D3 —
> "OCCURRED_IN_YEAR/PRECEDES/FOLLOWS are NOT in the schema"); minting them = making that decision. (b) 0 of the
> 112 dated events share a `PART_OF` parent, so there's no cluster structure to derive *meaningful* local ordering
> from. Needs YOUR vocab decision + a grouping strategy. Left untouched.

## What the panel decided
All 4 panelists (cheapest-win / measured-value / risk-auditor / sequencing) converged on the SAME move:
**deterministically date event nodes from `chronology-events.jsonl`** — schema is decided, data is on disk, $0, no LLM.
The risk auditor (Panel C) set the apply/dry-run boundary, which I followed.

## What was APPLIED (graph mutation — reversible, uncommitted)
- **112 `event.*` nodes** now carry an `occurred:` block in frontmatter: `ac_year` (signed int) + `precision: year`
  + `basis_source: wiki-year-page` + `basis_reliability: tertiary-fan` + `date_confidence: tier-3`.
- Source: single attested year + exact slug match in `chronology-events.jsonl`. Tier-3 capped, provenance-stamped.
- **Frontmatter-only, idempotent, bodies byte-preserved** (verified: Red Wedding `## Quotes` intact; 2nd `--apply` = no-op).
- Script: `scripts/date-event-nodes.py` (--dry-run default, --apply gated) + `tests/test_date_event_nodes.py` (31 tests).
- `reference/architecture.md` amended: `occurred:` row + block subsection documented (rule #6 sync).

### Verification
- 112 nodes with `occurred:` confirmed; `battle-of-the-trident → 283`, `red-wedding → 299`, `tourney-at-harrenhal → 281`.
- `--health` UNCHANGED: 8,528 nodes / 21,993 edges / 62 orphans (dating adds no edges/endpoints).
- pytest **1262 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2, cwd-is-tmp). Zero new failures.
- `git status`: exactly 112 files under `graph/nodes/events/`, nothing else in `graph/` touched.

## What was GATED / STAGED (NOT applied — needs your call)
1. **`long-night → 297 AC` — EXCLUDED** (wiki mention-index error: prehistoric event listed on the 297 AC page because
   its feared *return* is discussed then). Belongs as `precision: era` / `ac_year: null` per the canon-uncertainty rules.
2. **5 multi-year hubs (spans)** — staged, need `ac_year_end` or a split decision:
   `dance-of-the-dragons` [129–132], `war-of-the-five-kings` [298–300], `greyjoy-rebellion` [289–290],
   `regency-of-aegon-iii` [131–136], `first-blackfyre-rebellion` [196,212] (the 212 looks like a wiki page error).
3. **`narrative_first` (reading-position axis) — NOT written.** Blocked on edge chapter-ref format heterogeneity
   (`agot-arya-01` kebab vs `ASOS Catelyn VII` roman appear mixed on the same event's edges → naive min-sort wrong ~20%).
   Dry-run computed in the report; needs an `edges.jsonl` chapter-ref normalization pass first.
4. **`moon-of-the-three-kings` [130]** — chronology has the year but no node file exists (NOMATCH).
5. **3 blocklisted noise stubs** (`great-council` 3 distinct councils, `tourney`, `first-dornish-war`) — correctly excluded.
- Full tables: `working/session-results/2026-06-16-event-dating-dryrun.md`.

## Worth a glance
- `conquest-of-dorne → 161` is dated as an event, but an S96 cleanup note (A1) retyped a `conquest-of-dorne` to
  `object.text` (it's also an in-world book). Confirm the dated node is the event, not the book.

## Recommended NEXT (panel sequencing: dates → ordering → causal → arcs)
1. **Normalize `edges.jsonl` chapter-refs** (kebab vs roman) → then write `narrative_first` (the spoiler-gating substrate).
2. **Derive `PRECEDES`/`FOLLOWS`** from `ac_year` (free; cross-year is rock-solid, same-year needs `narrative_first`).
3. **Causal `TRIGGERS`/consequence edges** — the dip-measured gap, now cheaper (sequencing substrate exists).
   Start with the Robert's Rebellion chain (Harrenhal 281 → Trident 283 → Sack 283 → Tower of Joy). BLOCKED from
   auto-execution per the risk auditor — needs curation / your sign-off (causation is interpretive; pollution-sensitive).
4. Resolve the 5 spans + `long-night`-as-era + the year-page node mistype (10 `*-ac` nodes in `graph/nodes/characters/`).

## Not done (deliberately)
No commit, no worklog/todos update, no /endsession — all await your return. The 112-node change is uncommitted and
fully reversible (`git checkout graph/nodes/events/` reverts; the dry-run report is the manifest).
