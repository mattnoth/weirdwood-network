# Continue: Wiki prose extraction backfill (close the 79% stub-only gap)

**Created:** 2026-05-11 (end of Session 41)
**Track:** Graph depth — wiki prose attachment to nodes
**Status:** Ready, but starts with investigation
**Estimated effort:** One session, pure Python, $0
**Memory rules in play:** `feedback_python_before_agent.md`, `feedback_no_external_wiki_fetch.md`, `feedback_check_existing_knowledge_first.md`

---

## What this work is

Of the 7,583 graph nodes, **5,975 (79%) have stub-only Identity sections** — `"X is a character.human from the AWOIAF wiki."` with no real prose body. The wiki pages exist locally in `sources/wiki/_raw/`. The deterministic prose extractor exists at `scripts/wiki-pass2-extract-prose.py`. The work was never run end-to-end for most Path B promotions (Session 28-29).

This is the single biggest depth improvement available right now and costs nothing.

## Critical: investigate first, then act

There's an apparent contradiction in the current state:
- **6,509 `.prose.md` files** exist across `working/wiki/pass2-buckets/*/prose/`
- But only **1,608 graph nodes** show real prose in their body (79% are still stub-only)

So prose was extracted for many pages, but the **promotion step** (which concatenates `skeleton/<slug>.node.md + prose/<slug>.prose.md` into `graph/nodes/<type>/<slug>.node.md`) either didn't run for those pages, OR ran but the prose was empty/thin and got skipped.

**Step 0 — diagnose the gap.** Before running anything destructive, answer:
1. For a sample of 10 stub-only graph nodes (e.g., from Bucket A misses or random pick), check whether a `.prose.md` exists in any `working/wiki/pass2-buckets/*/prose/<slug>.prose.md`.
2. If yes → why wasn't it promoted? Look for the promotion script (probably mentioned in `working/runbooks/wiki-pass2-pipeline.md`) and check its exclusion criteria.
3. If no → run the extractor against the bucket containing those slugs, then promote.
4. For each "yes but never promoted" case: read the `.prose.md` content. Is it empty (no H2 sections matched the schema), or has real content?

This is a 15-minute investigation; don't skip it. The shape of the gap dictates the fix.

## Decisions to make before acting

1. **Promotion strategy** — overwrite-in-place vs staging:
   - In-place: write directly to `graph/nodes/<type>/<slug>.node.md`, replacing the stub Identity with the extracted prose sections. Faster, but harder to roll back.
   - Staged: write to `graph/nodes-staged/<type>/<slug>.node.md`, diff against current, promote good ones manually. Safer, slower.
   - Lean: **in-place** (the script is deterministic; re-running produces the same output; rollback is `git checkout`).
2. **Stage 1 agent-rich nodes** — DO NOT TOUCH. 874 nodes have `pass_origin: pass2-wiki` (Stage 1 agent emissions). These are richer than what the deterministic extractor would produce. Scope the work to `pass_origin: pass2-wiki-deterministic` ONLY. Use a frontmatter filter at the top of any iteration loop.
3. **Empty-prose detection** — for nodes where the wiki page genuinely has no extractable prose (very short pages, lists, disambiguations), leave the stub Identity in place. The fallback should preserve the existing skeleton, not blank-out the Identity to nothing.
4. **Bucket scope** — Stage 3a ran the extractor against secondary-tier buckets. Path B promotion (Session 28-29) added ~3,000 more nodes from `tier3-characters/`, `tier3-cultures/`, etc. These tier-3 buckets may or may not have ever seen the extractor.

## Existing pieces to reuse

| Resource | Path | Notes |
|---|---|---|
| Prose extractor | `scripts/wiki-pass2-extract-prose.py` | Deterministic, writes to `working/wiki/pass2-buckets/<bucket>/prose/<slug>.prose.md`. Has `--apply` and `--bucket` flags. |
| Pass 2 pipeline runbook | `working/runbooks/wiki-pass2-pipeline.md` | Documents Stage 3a + 3b + promotion. Authoritative on what should have happened. |
| Bucket manifests | `working/wiki/pass2-buckets/<bucket>/manifest.json` | Each bucket lists its pages; the extractor's source of truth for slug→page mapping. |
| Wiki HTML cache | `sources/wiki/_raw/<Page_Name>.json` | 17,657 cached pages. **DO NOT REFETCH** (memory: `feedback_no_external_wiki_fetch.md`). Note: 125 of these have only redirect HTML on disk due to the case-collision crawl bug — separate problem, queued in `working/todos.md` under "Case-collision wiki crawl bug". Skip those gracefully. |
| Stub detection regex | n/a | Body match: `is a (character\|place\|organization\|concept\|object\|event\|species\|title)(\\.[a-z]+)? from the AWOIAF wiki\\.` Single-line, anchored. |

## Implementation sketch

1. **Audit script** (`scripts/audit-prose-coverage.py`) — for each graph node:
   - Read frontmatter (slug, type, pass_origin)
   - Read body — is it stub-only?
   - Look up corresponding `.prose.md` in any `working/wiki/pass2-buckets/*/prose/`
   - Look up corresponding wiki cache file in `sources/wiki/_raw/`
   - Emit a JSON row: `{slug, pass_origin, is_stub, has_prose_file, prose_byte_size, has_wiki_cache, wiki_cache_redirect_only}`
   - Surface counts: how many stub-only nodes have a non-empty prose file ready to promote? How many need fresh extraction? How many have neither (case-collision losses)?

2. **Promotion script** (probably already exists — find it in `scripts/` or in the runbook) — for each stub-only node with a non-empty prose file, concatenate skeleton + prose and overwrite the graph node. Idempotent.

3. **Fresh extraction** — for stub-only nodes WITHOUT an existing prose file, run `wiki-pass2-extract-prose.py --bucket <bucket-id>` scoped to the relevant bucket. Then promote.

4. **Rebuild dependent indexes** — after content changes land:
   - `python3 scripts/wiki-pass2-build-alias-resolver.py --apply` (new aliases may have been captured in extracted prose's `## Quotes by X` headers etc.)
   - `python3 scripts/build-mention-index.py --all` (mention resolution may improve)
   - `python3 scripts/build-character-indexes.py --all` (out_edge_count may change as `## Edges` sections get added; in_edge_count may change as cross-references shift)
   - Re-run backlink-counts? — check whether `working/wiki/data/backlink-counts.json` derives from wiki HTML directly (no rebuild needed) or from node bodies (rebuild needed).

## Smoke-test slugs (verify before/after)

Pick 5-10 currently-stub-only nodes that should clearly have rich wiki content. Suggested:
- `walgrave` (Citadel archmaester from AFFC prologue)
- `mollander` (Citadel novice, AFFC prologue group)
- `armen` (Citadel acolyte, AFFC prologue)
- `alleras` (the Sphinx, AFFC prologue)
- `leo-tyrell` (AKA Lazy Leo, AFFC prologue)
- A random sample of 5 character nodes with `pass_origin: pass2-wiki-deterministic` and stub-only body

Before: read each node's body, confirm it's the stub one-liner.
After: read each node's body, confirm Origins / Appearances / Narrative Arc / Quotes sections now exist with real wiki text. Note coverage gaps (which slugs still stub-only? why? short wiki page? case-collision? extractor bug?).

## Expected delta

- Best case: ~5,500 of the 5,975 stub-only nodes get real prose. The other ~475 are genuinely-short wiki pages (lists, disambiguations, redirects, case-collisions) — leave as-is.
- Worst case: discover the promotion script has a bug class that needs fixing. Even then, the work to do is captured in the audit output and unblocks a future session.

## What this work unblocks downstream

- **Stage 4 prose-edge-classifier** becomes more accurate — richer source text means better edge classification.
- **Agent retrieval queries** (the project's actual goal per `project_real_goal_graph_for_agents.md`) return real content instead of "X is a character.human from the AWOIAF wiki."
- **Per-character / per-location index roll-ups** gain richer mentioned_in context (more prose = more cross-references = better backlink counts).

## DO NOT

- Refetch any wiki pages. The wiki is local. (`feedback_no_external_wiki_fetch.md` — hard rule.)
- Touch Stage 1 agent-rich nodes (`pass_origin: pass2-wiki`). These are 874 of 7,583 — filter them out.
- Modify the alias-resolver builder's bare-disambiguation filter as a "side fix" — that exists for good reasons; if you hit a case where it blocks resolution, handle the case inside whichever downstream script is consuming the alias-resolver (Session 41 set this pattern).
- Auto-run `/endsession` — Matt's standing rule (`feedback_endsession_requires_permission.md`).
- Try to fix the 125 case-collision pages here — that's queued as a separate todo with its own approach (reconstruction-from-cross-references as default). Skip those slugs gracefully if encountered.

## After this lands

Mark the corresponding todo in `working/todos.md` (under HIGH section: "Wiki prose extraction never completed for 5,975 graph nodes") as [x] DONE with the actual delta count. Update `worklog.md` with a Session entry. Then consider whether Tracks 2 (138 missing-node backfill) or 3 (per-LOCATION/ARTIFACT indexes) should be next.
