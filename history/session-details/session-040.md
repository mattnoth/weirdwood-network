---
session: 40
date: 2026-05-11
model: claude-opus-4-7 (1M context)
type: design + execution
title: "Catch-up synthesis, surgical merges, alias backfill"
---

# Session 40 — Catch-up synthesis, surgical merges, alias backfill (2026-05-11)

## Frame

Matt returned after a brief gap and wanted a status read on where the project stands. The session split into two halves: (1) an extended catch-up synthesis that surfaced architecture clarifications and a richer-Stage-4 scope, and (2) execution on three small cleanup/cleanup-adjacent commits plus the alias-resolver backfill from Session 38's mention-index unresolved list.

## Track / Stage merge — explained

Matt asked whether "Tracks" (A = Pass 1 chapter text, B = Pass 2 wiki) could be merged now that initial book passes are done. Answer: yes — Stage 4 (prose-derived edge discovery) is exactly the planned merge. Pass 1 is done across all 5 books (344/344), Pass 2 Stages 1-3 are done (~7,584 nodes promoted). Stage 4 is the first work that consumes both tracks together.

## "We have no edges" — corrected

Matt observed `graph/edges/` is empty. Correction: edges live in `## Edges` sections inside each node file (not in a separate edges directory). Eddard Stark has HOLDS_TITLE, SWORN_TO, BORN_AT, PARENT_OF, SPOUSE_OF, etc. — all derived from wiki infoboxes by the parser. The "unpromoted edges" Matt remembered are:
- `working/wiki/data/cross-references.jsonl` — 91,381 candidate edges (Stage 4 input)
- `working/wiki/data/chronology-events.jsonl` — 2,245 year-page rows (waiting on v2 temporal-edges schema)

The 22-type edge vocabulary is locked at the parser level. Last full audit (Session 29) confirmed 0 violations across 1,562 edges.

## Architecture.md drift — found and fixed

Matt asked for a reference file showing locked entity types and edges. Pointed to `reference/architecture.md` § Entity Type Hierarchy (line 38) and § Edge Types (line 109). On reading it, found three issues:

1. **Dead reference:** line 42 pointed to `working/taxonomy-candidates.md` which doesn't exist anywhere (likely lost in the Session 39 working/ reorg).
2. **Missing entity type:** `event.tournament` is in the parser's `TYPE_DIR_MAP` and used by 35 graph nodes, but never made it into the Type Reference Table or the hierarchy diagram. Added during Session 28's Path B promotion but never backported to spec.
3. **Stale todo:** `working/todos.md` line 108 said "Religion node type drift — normalize to `religion`" but architecture.md now declares `organization.religion` canonical and all 63 religion nodes match. Todo was written 2026-04-28 when architecture said bare `religion`; spec was updated since.

Bundled into commit `9da98e97`: removed dead reference, added `event.tournament` row + hierarchy entry, marked religion todo OBSOLETE.

**Separate typo flagged but not fixed:** line 56 has "cred sites" instead of "sacred sites" — kept out of this commit for scope, added as a future tiny fix.

## Surgical merges of 3 high-traffic duplicate nodes (commit `794bf52c`)

Inventory check of `graph/nodes/_conflicts/` and cross-dir duplicates found:
- **248 `_conflicts/` files** (rejected re-emit attempts, all dated 2026-04-26 to 2026-05-01 — no new conflicts being generated, the script is idempotent)
- **Only 2 actual cross-dir duplicates** out of 7,584 nodes: `battle-of-the-blackwater-song` (in both artifacts/ and texts/) and `caltrops` (in both factions/ and events/)
- Plus 1 high-profile `_conflicts/` orphan: `battle-of-the-blackwater`

Three nodes merited surgical merge because they're high-traffic (each named in 20+ chapters):

### The Battle of the Blackwater (song)
- `artifacts/` (Stage 1 agent, v1, tier-1): rich Identity, Narrative Arc, Quotes, Notes, **`WRITTEN_BY: Galyeon of Cuy` edge** — but wrong dir (object.text should route to texts/)
- `texts/` (Stage 3 Python, v1-python, tier-2): stub Identity, empty Edges, deterministic Narrative Arc with wiki cite_refs — right dir but lossy content

Resolution: `git mv` the agent file to texts/ (overwriting the stub), preserving the WRITTEN_BY edge and rich synthesized prose. The deterministic version's hyperlinked Narrative Arc paragraph was the only loss, and it was a paraphrase of the same Purple Wedding event the agent already covered.

### Battle of the Blackwater (the battle)
- `events/` (Python, current canonical, 110 lines): stub Identity, but rich wiki-extracted Origins / Aftermath / Quotes (8 quotes, all properly cited)
- `_conflicts/` (agent, 51 lines): rich Identity ("The Battle of the Blackwater was the largest battle in the War of the Five Kings, fought in 299 AC at the mouth of the Blackwater Rush..."), Allegiances summary, Narrative Arc condensed synthesis

Resolution: kept events/ as base (it has more total content), surgically replaced the stub Identity with the agent's rich Identity, and inserted the Allegiances + Narrative Arc sections after Identity but before Edges. Best of both: agent synthesis upfront, Python wiki-extraction downstream.

### Caltrops — the interesting case (type disagreement)
- `factions/caltrops` (agent, v1): typed `organization.faction` with explicit Notes explaining the override: *"The wiki categorizes this page under 'Organizations' and 'Greens.' The track_b_row typed this as `event.war`, but the entity is more accurately an `organization.faction` — a conspiracy group of 13 named nobles, not a battle or war. Type overridden accordingly."*
- `events/caltrops` (Python, v1-python): typed `event.battle` because Python trusted the `battles-b-d` bucket assignment + Conflict infobox field

The agent was right. The Caltrops are a conspiracy/secret organization (the 13 nobles who plotted Hugh Hammer and Ulf White's deaths during the Dance of the Dragons), not a battle. Resolution: kept factions/ version (correct type + analytical Notes), replaced its 1-paragraph Narrative Arc with the Python version's richer 4-paragraph wiki extraction, added the Gyldayn quote as a Quotes section.

## The agent-vs-Python prose split — explained

Matt asked: "Will conflicts keep coming up? Why does artifacts/ have rich prose and texts/ has stub? Are there two versions of every node?"

Hard data unpacked:
- 864 nodes are `prompt_version: v1` (Stage 1 agent, Session 23)
- 6,968 nodes are `prompt_version: v1-python` (Stage 3 Python deterministic, Session 26+)
- Only 2 cross-dir duplicates exist
- 248 `_conflicts/` files (3.3% of graph), all dated Apr 26-May 1, none being regenerated

**The actual axis isn't "level of page" — it's "did the source wiki page have a body?"**
- Wiki page with body → Python extracted prose section
- Wiki page infobox-only → Python emitted stub Identity + empty body

The song asymmetry is the canonical example of why Stage 4 exists. Python doesn't infer edges from prose (only from infobox). Songs don't have infoboxes, so the song node had no edges. The agent read the prose, inferred `WRITTEN_BY: Galyeon of Cuy`, and synthesized rich content. **The agent already did this work for 864 nodes back in Stage 1; Stage 4 brings the same capability to the other 6,968.**

## Stage 1 was paused mid-stride (cost pivot)

Matt asked when Stage 1 happened and whether it was abandoned. Answer:
- Stage 1 (core) completed: 37/37 buckets, 855 nodes, $95.33 cost (≈$0.111/node)
- Stage 1 (secondary, originally planned): never ran — projected ~$1,217 if continued
- Pivot decision Session 24: Python-only for Stage 3, three reasons: (1) cost ($1,200 saved), (2) determinism (agent runs vary; Python is byte-stable), (3) single-writer-per-file invariant (made the rest of the pipeline safer to reason about)

So yes, Stage 1 paused mid-stride. The 855 agent-rich nodes are the only ones with synthesized Identity / Allegiances / Narrative Arc / Notes / prose-inferred edges.

## Stage 4 in its richest form — 3 components

Matt asked: "We have all this raw material now — will that save usage on a future agent-enrichment pass?" Answer: yes, substantially. The accumulated infrastructure (Pass 1 across 5 books, mention-index at 70% resolution, cross-refs.jsonl, Python prose on 6,968 nodes) makes a richer Stage 4 scope economical.

**Original scope:** prose-edge-classifier — read cross-references.jsonl + node prose, classify each as one of the 22 locked edge types or reject as just-a-mention.

**Richest-form scope (3 components):**
1. **Prose-inferred edge backfill** — original scope, already specced + smoke-gated
2. **Chapter-evidence backfill** — "see also: agot-bran-01, acok-tyrion-12" pointer for each node. Combines per-character index roll-up todo (pure Python, $0) with agent enrichment for ambiguous chapter mentions. Closes "give me everything about Eddard" without re-scanning all chapters.
3. **Rich Identity rewrites for top-N high-traffic nodes** — replace the canned "X is a Y from the AWOIAF wiki." stub on Python nodes. Pick top-N by `working/wiki/data/backlink-counts.json`. Haiku-cheap with Python prose + Pass 1 evidence in-context. Skip the 855 Stage-1 nodes (already rich).

Cost framing: naive Stage-4-as-Stage-1-reprise = $773 (6,968 nodes × $0.111). With deterministic pre-pass infrastructure done, agents do only irreducible reasoning. Session 37 model-fit audit projects $25-65 for the classifier work if Sonnet smoke passes. The $95 spent on Stage 1 wasn't wasted — it taught what an agent-synthesized node looks like, and the rest of the pipeline is engineered to reach that target cheaper.

Saved as memory: `project_stage4_richest_form.md`. Captured in `working/todos.md` under the existing Stage 4 entry.

## Alias-resolver backfill (commit `ace00ee0`)

Session 38's mention-index ran at 70.0% resolution. Top-20 unresolved had 6 cleanly-mappable cases where the canonical node exists but no alias entry connects Pass 1's raw name to it.

**Added 6 aliases** (durable path — node frontmatter, not just the JSON):
| Canonical | New alias | Chapter occurrences |
|---|---|---|
| `eddard-stark` | "Ned Stark" | 42 |
| `tormund` | "Tormund Giantsbane" | 21 |
| `eastwatch-by-the-sea` | "Eastwatch" | 23 |
| `blackwater-rush` | "The Blackwater" (river — battle has own node) | 23 |
| `brienne-tarth` | "Brienne" | 27 |
| `thoros` | "Thoros of Myr" | 28 |

The Blackwater disambiguation: sampled 10 chapters where `the-blackwater` appears unresolved. Pattern: Pass 1 puts it in the Locations section in every sampled chapter; bare "The Blackwater" is river context (explicit disambiguators like "The Blackwater (river)" / "The Blackwater (battlefield)" slugify differently). Battle was already resolving via the `battle-of-the-blackwater` slug directly.

Re-ran `scripts/wiki-pass2-build-alias-resolver.py --apply`, then `scripts/build-mention-index.py --all`. Resolution climbed **70.0% → 70.6%** (+209 newly-resolved mentions across 344 chapter files). Smaller than the "75%+" projection because remaining top-20 (`maester-aemon`, `joffrey`, `godswood`, `aegon`, etc.) are either ambiguous (multiple referents) or genuine missing-node cases.

## Other corrections during this session

- **"The team" → "Matt solo."** Matt corrected: the team is just him; Okey was a one-off Opus-account favor for ASOS Pass 1. Memory saved: `project_team_is_solo.md`.
- **Agent + graph clarification.** No agent (including this chat agent) automatically traverses the graph. Agents have file-reading tools and read `graph/nodes/*.node.md` like any markdown. There's no MCP server, no graph-query API. The per-character index roll-up is the first piece of agent-ready retrieval infrastructure.

## What this session didn't do

- Did NOT touch the 247 remaining `_conflicts/` files — bundled into Stage 4 work per existing todos.md line 101.
- Did NOT fix the "cred sites" typo on architecture.md line 56 (out of scope; tiny separate fix).
- Did NOT start Stage 4 work — alias backfill was the natural cheap-Python prep, not Stage 4 itself.
- Did NOT touch the `book-chapter-pages-defer` triage gap (todos.md line 234) — separate cleanup.

## Commits this session (4 total)

1. `9da98e97` — Schema doc cleanup: event.tournament, taxonomy-candidates reference, religion todo
2. `794bf52c` — Surgical merge: 3 high-traffic duplicate nodes
3. `ace00ee0` — Alias backfill: 6 nodes + regenerated mention-index (352 files)
4. `3e7bc1d5` — todos.md: Stage 4 in its richest form (3 components)
