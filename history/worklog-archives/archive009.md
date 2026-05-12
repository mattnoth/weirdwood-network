### Session 39 — Status check + working/wiki/ subtree reorg (2026-05-07)
**Detail:** `history/session-details/session-039.md`

**Changes made:**
- **Reorg:** `working/wiki-parsed/` split into `working/wiki/data/` (9 permanent reference files: alias-resolver, infobox-data, page-index, page-categories, cross-references, chronology-events, backlink-counts, parse-stats.md, cross-refs-summary.md) and `working/wiki/pass2-staging/` (7 run-specific staging files: triage-bucket-assignments, triage-manifest, draft-buckets, priority-summary, stage3-promote-summary, stage3a-emission-summary, stage3b-extraction-summary). `working/wiki-pass2/` → `working/wiki/pass2-buckets/` (all 536 buckets, 14,141 files via `git mv`). `working/wiki-parsed/` directory removed.
- `working/wiki/README.md` — NEW. Explains data/staging/buckets split. Notes that historical session details, archived continue prompts, and audit execution logs reference old paths and were intentionally not rewritten.
- 65 live files updated via three-step targeted sed (~32 scripts/, 14 .claude/agents/*.md, 4 reference/*.md, 3 working/runbooks/, 3 working/agent-fleet-specs/, 2 .claude/commands/, 2 active continue prompts, CLAUDE.md, worklog.md, working/todos.md, working/tier3-promotion-plan.md). Sed key trick: only match the **quoted** `"wiki-parsed"` and `"wiki-pass2"` to avoid breaking script filenames like `wiki-pass2-triage.py`.
- `CLAUDE.md` Directory Structure diagram updated (lines 119-120 now show `wiki/` parent with `data/`, `pass2-buckets/`, `pass2-staging/` children).
- `worklog.md` Session 35 corrected: ASOS Okey branch IS merged (commit `2eaf5c71`, verified via `git log`). Prior entry's "Branch not yet merged" was correct at Session 35 but stale by Session 39.
- Smoke verification: `python3 scripts/build-mention-index.py --book agot --dry-run` runs cleanly against new paths; final grep confirms only remaining `wiki-pass2` refs in live files are correct script filenames.

**Decisions:** **Naming reorg adopted as Option D** (Matt's instinct, beating my original A/B/C menu). `working/wiki/` as parent domain; pass-numbers as children of the domain rather than top-level siblings. Future passes (Stage 4 prose-edge, etc.) get a natural home. Frozen records (`history/**`, `working/audits/**`, `progress/continue-prompts/archive/**`, `working/runbooks/archive/**`, `scripts/archive/**`) **left untouched** — they describe what was true at the time. **`graph/index/chapters/` not renamed** — the path already says "chapters"; "mention" is fine as a concept once explained. README todo added. **Food/dialogue cost design discussion** (no execution): Python pre-pass makes the LLM pass substantially cheaper — targeting + tighter scopes + scene-level chunking + sampling-oracle pattern → ~$10-25/book on Sonnet vs ~$50/book for blind Pass 1. Reasoning still required for scene-level structure.

**What didn't get done:**
- **No commit.** Reorg sits in working tree as 14,141 renames + 65 modifications + 1 new README. Awaits explicit authorization.
- `graph/index/chapters/README.md` agreed but not written (added to todos).

**What's next:**
- **Commit the reorg** (single commit, suggested: `Reorg: working/wiki-{parsed,pass2}/ → working/wiki/{data,pass2-buckets,pass2-staging}/`).
- **Smallest unit-of-work next:** alias-backfill from Session 38 mention-index top-20 unresolved patterns; cheap edit to `working/wiki/data/alias-resolver.json` + re-run mention-index → expected resolution >75%.
- Other live tracks unchanged: Stage 4 prose-edge-classifier (`progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`); dialogue/meals/mention-index design (`progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md`); model-fit recommendations awaiting Matt's review; two PreToolUse hooks queued.
- **Per Matt's standing rule, no `/endsession` auto-run.**

### Session 40 — Catch-up synthesis, surgical merges, alias backfill (2026-05-11)
**Detail:** `history/session-details/session-040.md`

**Changes made:**
- `reference/architecture.md` — added `event.tournament` row to Type Reference Table + hierarchy diagram (was missing from spec despite 35 nodes using it); removed dead reference to `working/taxonomy-candidates.md` (file lost in Session 39 reorg).
- `working/todos.md` — marked religion type-drift todo OBSOLETE (architecture.md updated since the original Session 26 entry; current spec matches all 63 religion nodes); marked alias-backfill todo DONE; added Stage 4 richest-form 3-component expansion under existing Stage 4 entry; added Per-character Index Roll-up as READY-TO-DO with new continue-prompt link; added 3 tiny follow-up todos surfaced this session.
- `graph/nodes/events/battle-of-the-blackwater.node.md` — surgical merge: kept Python-extracted Origins/Aftermath/Quotes (110-line wiki body), replaced stub Identity with agent's rich version, inserted Allegiances + Narrative Arc sections from `_conflicts/`. Deleted `_conflicts/battle-of-the-blackwater-battles-b-2026-05-01T20-34-52.node.md`.
- `graph/nodes/texts/battle-of-the-blackwater-song.node.md` — replaced Python stub with agent-rich version via `git mv` from `artifacts/`. Preserves `WRITTEN_BY: Galyeon of Cuy` edge that Python had no way to infer (no infobox on songs). Deleted `artifacts/battle-of-the-blackwater-song.node.md`.
- `graph/nodes/factions/caltrops.node.md` — agent's `organization.faction` type was correct (the wiki entry is a 13-noble conspiracy from the Dance of the Dragons, not a battle); replaced 1-paragraph Narrative Arc with Python's richer 4-paragraph wiki extraction, added Quotes section. Deleted `graph/nodes/events/caltrops.node.md`.
- 6 character/location nodes — added missing aliases: `eddard-stark` ← "Ned Stark", `tormund` ← "Tormund Giantsbane", `eastwatch-by-the-sea` ← "Eastwatch", `blackwater-rush` ← "The Blackwater" (river), `brienne-tarth` ← "Brienne", `thoros` ← "Thoros of Myr". Durable path (frontmatter, not just JSON).
- `working/wiki/data/alias-resolver.json` — regenerated via `scripts/wiki-pass2-build-alias-resolver.py --apply`. 1,199 → 1,205 alias_to_canonical entries.
- `graph/index/chapters/{book}/*.mentions.json` — all 344 files regenerated via `scripts/build-mention-index.py --all`. Resolution rate **70.0% → 70.6%** (+209 newly resolved).
- `scratch` — triaged + emptied. Both items addressed by this session's discussion (Item 1 = Stage 4 component-b; Item 2 = superseded by existing Stage 4 continue prompt).
- Memory: added `project_team_is_solo.md` (team = Matt only; Okey was one-off), `project_stage4_richest_form.md` (3-component expansion of Stage 4 scope). MEMORY.md index updated.

**Decisions:** **Stage 4 reframed to 3 components, not 1.** Original scope was prose-edge-classifier alone (cross-references.jsonl → typed edges). Catch-up synthesis surfaced that accumulated raw material (Pass 1 across 5 books, mention-index at 70.6%, cross-refs.jsonl, Python prose on 6,968 nodes) makes a richer scope economical: (a) prose-inferred edges, (b) chapter-evidence backfill, (c) rich Identity rewrites for top-N high-traffic nodes. Each independently shippable. **Stage 1 was paused mid-stride** for cost reasons (Session 24 pivot from agent to Python-deterministic for secondary buckets; saved ~$1,200). The 855 agent-rich Stage-1 nodes are the only ones with synthesized rich Identity + prose-inferred edges. **The 247 remaining `_conflicts/` files are NOT being regenerated** (idempotent script, all dated Apr 26-May 1); deferred to bundled Stage 4 work per existing line 101. **The agent was correct on caltrops type-classification disagreement** (Python trusted bucket assignment as `event.battle`; agent read prose and correctly typed as `organization.faction` with explicit Notes explaining override).

**What's next:**
- **READY TO DO — Per-character index roll-up** — pure Python, $0, ~30-60 min. Continue prompt: `progress/continue-prompts/2026-05-11-per-character-index-rollup.md`. Unblocks Stage 4 component (b).
- **Stage 4 launch** — still queued at `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`. Alias-backfill prerequisite NOW MET as of this session.
- **3 tiny follow-ups** in `working/todos.md` under "Tiny Follow-ups (Session 40 surface)": architecture.md typo fix, second round of alias-backfill, conflicts cleanup (covered).
- **Per Matt's standing rule, /endsession was invoked explicitly** — handoff prompt below.

### Session 41 — Per-character index roll-up + POV canonicalization + missing-nodes audit (2026-05-11)
**Detail:** `history/session-details/session-041.md`

**Changes made:**
- `scripts/build-character-indexes.py` — NEW. Pure-Python (no LLM, no HTTP) script that walks 3,910 `character.*` graph nodes, parses each frontmatter for slug/name/type, joins against the per-chapter mention index (inverse maps for POV + mentioned-in), reads node-body `## Edges` section for out_edge_count, looks up `working/wiki/data/backlink-counts.json` for in_edge_count, and emits one `graph/index/characters/<slug>.index.json` per character + a `_summary.json` rollup. CLI: `--character <slug>` (test mode), `--all` (default), `--dry-run`. Idempotent. Runs in ~1.0s.
- `graph/index/characters/` — NEW directory. 3,910 character-index JSON files + `_summary.json`. Stats per file: `appearances_total`, `chapters_pov`, `chapters_mentioned_in`, `out_edge_count`, `in_edge_count`. Lists: `chapters.pov` and `chapters.mentioned_in` (each mention record carries chapter_id, book, pov_character_slug, mention_count, sections, resolved_via). POV chapters excluded from mentioned_in to avoid double-counting.
- **POV canonical resolution (Matt-requested expansion):** instead of guessing POV from the filename stem (which left Alayne/Reek/descriptive-title chapters with the wrong POV), the script now parses each Pass 1 extraction's `pov_character:` frontmatter field. Pass 1 already encodes truename canonicalization there: `Alayne (Sansa Stark)`, `Reek (Theon Greyjoy)`, `Theon Greyjoy (as "The Turncloak" / "Reek")`. A small parser handles both `(truename)` and `(as "alias")` idioms + disguise wording (`Arya Stark (disguised as "Arry")`). Slug resolution chain: kebab → direct → alias-resolver → honorific-strip (`Maester Cressen` → `cressen`) → unique-prefix-match → mention-disambiguated prefix-match (`Catelyn` → catelyn-stark beats catelyn-bracken because catelyn-stark appears in chapter's Characters Present). All but 1 of 344 chapter POVs now resolve (the remaining 1: AFFC prologue's Pate the Novice — wiki page exists at `Pate_(Novice).json` but was never promoted to graph, real missing-node case).
- `working/todos.md` — marked Per-character Index Roll-up DONE; added new Year-page Type Bug todo (10 wiki year-pages slipped through as `character.human`; faithfully emitted but flagged in `_summary.json.year_pages_emitted_as_characters`).

**Decisions:** Followed the continue-prompt's 4 leans verbatim: (a) include all `character.*` types — 3876 human + 28 dragon + 6 direwolf; (b) `in_edge_count` from `backlink-counts.json` (the existing prose cross-ref count); (c) POV chapters in separate list from mentioned_in (no double-counting); (d) alias resolution inherits from mention-index — no extra work. **Year-page handling: emit faithfully + log** (option a from the 3 choices), with a todo entry capturing the underlying type-classification bug for separate fix. **POV canonicalization done at the index layer, not the graph layer.** Alayne and Reek remain distinct graph nodes (POV=0 each, mentioned_in retained). The character INDEX treats them as Sansa/Theon for retrieval (correct narrative model). The graph-level SAME_AS merge is Stage 4 work — but the index doesn't need to wait for it. **POV roster grew 18 → 30** after this work: gained Quentyn (4), Barristan (4), Victarion (4), Asha (4), Aeron (2), Areo (2), Jon Connington (2), Arianne (2), Cressen, Will, Chett, Varamyr, Arys Oakheart, Melisandre, Kevan, Merrett Frey. Top-9 POV counts match canon: Tyrion 47 ✓, Jon 42 ✓, Arya 33 ✓ (was 31 — pre-fix missed Cat of the Canals + Blind Girl + Ugly Little Girl), Daenerys 31 ✓, Catelyn 25 ✓ (was 24 — pre-fix missed agot-catelyn-06 where pov_character was just "Catelyn" with no surname), Sansa 24 ✓ (was 21 — +Alayne ×2 + Sansa I), Bran 21 ✓, Jaime 17 ✓, Eddard 15 ✓, Theon 13 (was 7 — +Reek ×3 + 3 descriptive titles). Continue-prompt's smoke-test estimate of "30-50 chapters mentioned in" for Eddard was wrong — actual is 185 (referenced post-death throughout AFFC/ADWD).

**Session 41 addendum (post-commit `e737ba4e`):**
- `graph/nodes/characters/pate-novice.node.md` — NEW. Hand-crafted from Pass 1 (`affc-prologue.extraction.md`) content because the wiki crawl had only the redirect HTML for this page (case-collision bug, see below). Includes the impersonation edges (`KILLED_BY: alchemist` + `KILLED_BY: jaqen-hghar`) per memory rule `project_impersonation_edges_redirect.md`. Theory-relevant: Pate is murdered by Jaqen H'ghar disguised as the alchemist, and Jaqen takes Pate's face/identity at the Citadel — major Faceless Men plotline.
- `scripts/build-character-indexes.py` enhanced with a raw-name reverse-map tiebreaker: when prefix-match returns multiple candidates (e.g., POV "Pate" → 12 `pate-*` slugs), intersect with nodes that explicitly claim that raw name in their frontmatter aliases. Solves the "alias-resolver rightly refuses to pin a single-word bare-disambiguation alias" case without modifying the alias-resolver. Pate now resolves; all 344 chapter POVs resolve; **POV roster = 31** (up from 30).
- `scripts/audit-missing-nodes.py` — NEW. Audits the gap between cached wiki pages and graph nodes. Output: `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.{md,json}`. Findings:
  - **1,170 unpromoted wiki pages** (excluding pages flagged for `skip`)
  - **138 Bucket A** — Pass 1 references them, no graph node. Top: `godswood`/36, `flea-bottom`/31, `old-gods`/22, `seastone-chair`/14, `chatayas-brothel`/12, `unsullied`/9, `valyrian-steel-dagger`/8.
  - **83 Bucket B** — heavily wiki-backlinked but Pass 1 silent (mostly D&E/historical).
  - **949 Bucket C** — tail (defer).
  - **125 case-collision redirect crawl bugs** — pages whose canonical-content variant got overwritten on case-insensitive macOS HFS+. Major losses: `Children of the Forest`, `Free Folk`, `Red Priest`, `Valar Morghulis`, `House Words`, `Known World`. Per CLAUDE.md narrow-exception rule, fetching these requires explicit per-use approval and CANNOT write to `sources/` directly — fix is a dedicated session.
- `working/todos.md` — added 3 new HIGH-priority todos: case-collision crawl bug (125 pages), missing-node backfill (138 Bucket A pages), wiki prose extraction never completed (5,975 stub-only nodes).

**What's next:**
- **Stage 4 component (b) — chapter-evidence backfill** is now unblocked. The character index per slug provides the prerequisite "for character X, here are the chapters that reference them" lookup. Continue prompt for the larger Stage 4 work: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.
- **Year-page type fix** queued in todos.md (10 nodes; bundles naturally with Stage 4 temporal-edges work, since year pages are the natural `OCCURRED_IN_YEAR` anchors).
- **Case-collision crawl bug** queued in todos.md — major finding, 125 pages affected, requires dedicated session + per-use exception approval.
- **138 missing-node backfill** queued in todos.md — cheap Python work, $0, would close the highest-signal gap.
- **Wiki prose extraction** queued in todos.md — re-run `wiki-pass2-extract-prose.py` against the 5,975 stub-only nodes.
- **Per-LOCATION + per-ARTIFACT index roll-ups** are the natural next iteration of this work (continue prompt scoped to characters only). Pattern is reusable — same script structure with different node-type filter. Not yet a todo; flag if/when Stage 4 needs them.
- **Per Matt's standing rule, /endsession is NOT auto-run.**

### Session 43 — Bucket A missing-node backfill (2026-05-11)

**Changes made:**
- `scripts/wiki-pass2-bucket-a-backfill.py` — NEW. Pure-Python backfill emitter for the 138 Bucket A slugs (Pass 1 referenced, never got graph nodes). Three actions per slug: (1) alias-addition — redirect → existing node, add the slug to that node's `aliases:` list; (2) new node — content page in cache, emit skeleton + prose; (3) stub — circular redirect or no content, emit skeleton-only. Handles both inline `aliases: ["..."]` and YAML block `aliases:\n  - ...` formats. Uses `mw-headline` span for clean h2 extraction (bypasses `[]` edit-link bracket artifacts). `--dry-run` default, `--apply` to write, `-v` for verbose. All 138 changes: 53 alias additions, 68 new nodes with prose, 17 stubs.
- **68 new node files** emitted across locations/, factions/, artifacts/, concepts/, prophecies/, materials/, texts/, species/. Major: `flea-bottom` (11.8K prose chars), `unsullied` (12.5K), `black-cells` (11.4K), `godswood-of-winterfell` (13.9K), `godswood-of-the-red-keep` (8.75K), `the-prince-that-was-promised` (10.5K), `usurper` (7.6K), `myrish-lace` (5.1K), `seastone-chair` (5.6K).
- **17 stubs** for circular-redirect / no-content cases: queens-men, valar-morghulis, valar-dohaeris, crossroads-inn, red-waste, sky-cells, ruby-ford, spears-of-the-merling-king, naggas-hill, queen-of-love-and-beauty, all-for-joffrey, rolfe-the-dwarf, the-song-of-ice-and-fire, drowned-men, bethany-fair-fingers, goodwife-maerie, high-king.
- **53 alias additions** to existing nodes. Notable: `old-gods` → alias on `old-gods-of-the-forest.node.md` (22 mentions), `valyrian-steel-dagger` → alias on `littlefingers-blade.node.md` (8 mentions), `daenerys-stormborn` → alias on `daenerys-targaryen.node.md` (4 mentions).
- `working/todos.md` — marked Bucket A HIGH todo DONE with actual delta; added LOW categorizer-fix follow-up (CATEGORY_TYPE_MAP gaps that sent Bucket A to `unknown`).
- Graph total: 7,668 → 7,915 nodes (+247 total including this session's new files).

**Audit result:** `audit-missing-nodes.py` re-run: Bucket A 138 → 53. The 53 remaining are alias-resolution cases (audit checks slug-to-file, not alias fields). All 53 are properly resolved in the graph via `aliases:` on target nodes.

**Decisions:** Targeted emitter (option b from continue prompt) over categorizer-fix-then-re-emit. Slug overrides (`SLUG_TYPE_OVERRIDES`) for ambiguous cases (rookery, flea-bottom, red-temple, scribes-hearth, septry, wormways) where category signals were misleading. YAML block-format aliases handled in `add_alias_to_node()` to cover Stage-1 pass2-wiki nodes with block-sequence frontmatter. `mw-headline` span extraction fixes prose section mapping across all pages.

**What's next:**
- **Categorizer fix** (LOW) queued in todos.md — back-port CATEGORY_TYPE_RULES from backfill script to `scripts/wiki-infobox-parser.py`'s `CATEGORY_TYPE_MAP`.
- **Stage 4 prose-edge-classifier**: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.
- **Per Matt's standing rule, /endsession is NOT auto-run.**

### Session 42 — Wiki prose extraction backfill (Track 1) (2026-05-12)
**Detail:** `history/session-details/session-042.md`

**Changes made:**
- `scripts/audit-prose-coverage.py` — NEW. Read-only audit. For each graph node (excluding `_conflicts/_unclassified/`), emits one JSON row to `working/audits/wiki-prose-coverage-2026-05-12/execution/coverage.jsonl` with: slug, type, pass_origin, is_stub (body matches stub-only regex AND lacks `## Origins`/`## Narrative Arc`/`## Appearances`/`## Culture`/`## Organization`/`## Quotes`/`## Aftermath` section headers), has_prose_file, prose_byte_size, prose_bucket, has_wiki_cache, wiki_cache_redirect_only (small redirect-only HTML payload — the Session 41 case-collision losers). Plus `summary.md` with counts by pass_origin and promotion outlook. Stub regex: `is an? <type>(\.<sub>)? from the AWOIAF wiki\.`.
- `scripts/wiki-pass2-attach-prose.py` — NEW. Reads `coverage.jsonl`, filters to `pass_origin: pass2-wiki-deterministic` + `is_stub: true` + `has_prose_file: true`, then for each candidate appends `\n + prose_bytes` to the existing graph node body (preserving frontmatter + late-stage parser-fix Identity/Edges from Stage 3c re-emissions). Idempotent: re-running skips nodes whose current body already contains any prose section header. Atomic-rename writes. CLI: `--apply`, `--limit N`, `--slug X`, `-v`. Writes `working/audits/wiki-prose-coverage-2026-05-12/execution/attach-prose-summary.json` on full-run --apply.
- **990 graph nodes attached** with prose: 947 `characters/`, 10 `titles/`, 9 `locations/`, 7 `events/`, 7 `species/`, 3 `customs/`, 3 `languages/`, 2 `factions/`, 1 `artifacts/`, 1 `medical/`. (Filtered out: 874 Stage 1 agent-rich `pass_origin: pass2-wiki` nodes — never touched per continue-prompt hard skip rule.)
- Smoke test: `walgrave` 519 bytes → 4,688 bytes with full Origins / Appearances & Description / Narrative Arc (with `### A Feast for Crows` sub) / Quotes sections, all cite_refs preserved as `(wiki:Walgrave.cite_ref-X)`. 5 randomly-sampled character nodes all show clean section structure with book-boundary subheadings + per-character Quotes blocks.
- `working/todos.md` — marked the HIGH "Wiki prose extraction never completed for 5,975 graph nodes" todo DONE with the actual delta + the over-count explanation.

**Decisions:** **In-place overwrite** strategy. **Append-to-current-body** rather than rebuild-from-bucket-skeleton, because the current graph node carries late-stage parser-fix Edges. Stage 1 agent-rich nodes hard-skipped. The 1,019 remaining stub+no-prose nodes are LEFT AS STUBS — genuinely empty-prose wiki pages. Dependent index rebuilds yielded only timestamp churn — reverted.

**What's next:**
- Stage 4 prose-edge-classifier: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.
- Tracks 2 & 3: Track 2 = 138 Bucket A missing-node backfill; Track 3 = per-LOCATION + per-ARTIFACT index roll-ups.
- **Per Matt's standing rule, /endsession is NOT auto-run.**
