# Stage 3a Mid-Stage Review

**Date:** 2026-04-28T01:33Z
**Reviewer:** general-purpose subagent
**Scope:** 21 skeletons read in detail across Tier A characters (5), Tier B characters (5), battles (3), places (3), organization.faction (3), and Tier-B-from-entity empty-edge cases (2). Plus corpus-wide audits over all 3,315 skeletons for: edge vocabulary, slug rule, edge-count fidelity, edge format/order fidelity, bucket-vs-type alignment, and unicode passthrough.

## Summary
- HIGH issues: 0
- MED issues: 4
- LOW issues: 4
- Verdict: **clean (proceed) with one explicit pre-3b decision needed on the Religion-on-locations edge type**

## Corpus-wide audit results (all 3,315 skeletons)

| Audit | Result |
|---|---|
| Edge types observed | **Exactly 22**, all in the locked `WIKI_22` vocabulary. **Zero unknown edge types.** |
| Slug pattern compliance (`[a-z0-9-]+`) | **3,315 / 3,315 pass** |
| `slug` frontmatter == filename | **3,315 / 3,315 pass** |
| Edge count fidelity (sample 50, vs JSONL) | **0 mismatches** |
| Edge format/order fidelity (sample 30, vs JSONL `render_edge_line`) | **0 mismatches** |
| Bucket vs entity_type alignment | 0 character-bucket misclass; 0 house-bucket misclass; 0 location-bucket misclass; 1 `unknown` in `battles-b` |
| Empty `## Edges` sections | 78 total (well-formed in every spot-check; the 9 promoted-from-entity cases referenced in the task brief are all present and clean) |

The two contracts the task identifies as load-bearing — the edge vocabulary lock and the JSONL → skeleton passthrough — are both intact across the entire corpus.

## Per-skeleton findings

### characters-house-baratheon-of-dragonstone/skeleton/melisandre.node.md  [TIER A — character.human]
- All 3 edges match JSONL exactly (Allegiances→SWORN_TO ×2, Culture→CULTURE_OF). Aliases preserved. Frontmatter clean.

### characters-house-baratheon-of-dragonstone/skeleton/shireen-baratheon.node.md  [TIER A — character.human]
- LOW: `BORN_AT: 289 AC` target contains `\u00a0` non-breaking space (verbatim from JSONL — known unicode passthrough). Otherwise all 7 edges match.

### characters-house-baratheon-of-dragonstone/skeleton/salladhor-saan.node.md  [TIER A — character.human]
- LOW: `SPOUSE_OF: Wives` — target is the literal word "Wives" (parser passthrough; the wiki page lists "Wives" as the field-value when no individual name is given). Not a real entity reference. 8 edges match JSONL exactly (including the `direction: symmetric` → forward render, which matches `render_edge_line`).

### characters-other-l-m/skeleton/maegor-i-targaryen.node.md  [TIER A — character.human]
- LOW: `BURIED_AT: 48 AC` and `DIED_AT: 48 AC` — date strings are emitted as targets alongside the location targets. The wiki "Buried" / "Died" infobox slot in this page has both date and location, parser splits them into two edges with the same edge_type. Parser passthrough. 22 edges total, all match JSONL byte-for-byte.

### characters-other-a/skeleton/anguy.node.md  [TIER A — character.human]
- All 4 edges match. Aliases preserved.

### characters-other-b/skeleton/bloodbeard.node.md  [TIER A — character.human]
- LOW: `HOLDS_TITLE: Company of the Cat (track_b: Title)` — "Company of the Cat" is a faction, not a title. The wiki's Title field on this page contains a faction name. Parser passthrough; future-pass agents will normalize.

### characters-house-frey-m-t/skeleton/perwyn-frey.node.md  [TIER B — character.human]
- LOW: Three `BORN_AT` edges including `BORN_AT: 269` (no "AC" suffix) and `BORN_AT: 278 AC`. The wiki Born field stores a date range; parser emits each token as its own edge. Parser passthrough.

### characters-house-frey-m-t/skeleton/queen-o-whores.node.md  [TIER B — character.human]
- Slug rule check: `Queen o' whores` → `queen-o-whores` matches the documented transform (apostrophe stripped, spaces → hyphens). All 3 edges match. URL preserves apostrophe via `urllib.parse.quote(safe="...'...")`.

### characters-other-l/skeleton/likely-luke.node.md  [TIER B — character.human]
- LOW: `aliases: ["Likely Luke"]` equals the page name (parser self-alias). Benign but redundant.

### characters-other-l/skeleton/lily.node.md  [TIER B — character.human]
- All 7 edges match. Qualifier `[possibly]` rendered correctly.

### characters-other-q-r/skeleton/qyle-corbray.node.md  [TIER B — character.human]
- 2 edges, both match.

### battles-a/skeleton/aegons-conquest.node.md  [TIER A — event.battle]
- MED: `Aegon's Conquest` is a war (multi-battle), not a battle. The infobox has `FIGHTS_IN` edges to its sub-battles, which makes the war a participant in its own components — semantically odd. This is a parser/triage classification issue (the wiki's infobox class for this page leads to the `event.battle` guess). Stage 3a passthrough is faithful.
- LOW: `DEFEATS: Daemon Velaryon (track_b: Result)` — "Daemon Velaryon" is one of many defeated by Aegon's Conquest; parser extracted only one. Parser-level.

### battles-b/skeleton/battle-of-the-blackwater.node.md  [TIER A — event.battle]
- LOW: `DEFEATS: See below (track_b: Result)` — "See below" is wiki boilerplate, not an entity. Parser passthrough.

### battles-d-f/skeleton/fall-of-harrenhal.node.md  [TIER A — event.battle]
- LOW: `DEFEATS: Bolton (track_b: Result)` — ambiguous referent (House Bolton? Roose? Ramsay?). Parser passthrough.

### locations-other-a-b/skeleton/asshai.node.md  [TIER B — place.location]
- MED: `WORSHIPS: religions (track_b: Religion)` — target is the literal word "religions" (a placeholder). Plus see cross-cutting note on WORSHIPS-on-locations.

### locations-other-g-m/skeleton/harrenhal.node.md  [TIER A — place.location]
- 3 edges match. Qualifiers `[AGOT]` / `[ADWD]` rendered correctly.

### locations-other-g-m/skeleton/highgarden.node.md  [TIER A — place.location]
- 2 edges match.

### houses-other-h-w/skeleton/nights-watch.node.md  [TIER A — organization.faction]
- Type correct (post-Session-25 override). 3 edges match JSONL.

### houses-braavos/skeleton/faceless-men.node.md  [TIER A — organization.faction]
- Type correct. 4 edges match JSONL including `[formerly]` qualifier.

### houses-seven-kingdoms/skeleton/kingsguard.node.md  [TIER A — organization.faction]
- Type correct. 7 edges match JSONL.
- MED: `FOUNDED: Aegon I Targaryen (track_b: Founder)` is rendered forward — meaning the Kingsguard FOUNDED Aegon. The architecture table specifies `Founder, Founded → FOUNDED, Founder → Founded` (founder → org). On a faction page where the Founder field lists the founder, the parser should emit `direction: reverse` (so the edge reads `Aegon FOUNDED Kingsguard`). Parser-level direction bug, observed on 14 skeletons total. Not Stage 3a's contract — but worth flagging because it will need a fix or documented inversion convention before edges land in the graph.

### houses-other-b-h/skeleton/house-brune.node.md  [TIER B from-entity — organization.house]
- Empty `## Edges` section present, formatted correctly (`## Edges\n\n`). Frontmatter sound.

### houses-other-h/skeleton/house-shett.node.md  [TIER B from-entity — organization.house]
- Empty edges, frontmatter sound. Same pattern as House Brune.

## Cross-cutting issues

### MED-1: WORSHIPS used for locations' Religion field (vocabulary gap, not a bug per se)
112 skeletons use `WORSHIPS` for the Religion infobox field. Architecture.md § "Wiki Infobox Fields → Edge Type Mapping" says: `Religion → WORSHIPS for characters; RELIGION_OF for locations` — but `RELIGION_OF` does **not exist** in the locked edge taxonomy table (Cultural & Religious section only has WORSHIPS / SACRED_TO / CLERGY_OF). The parser took the safer route (WORSHIPS for everything) which means location skeletons read e.g. `Highgarden WORSHIPS Faith of the Seven`. Semantically off but vocabulary-locked. **Decision needed before Stage 3b finalization:** either (a) add `RELIGION_OF` to architecture.md and re-run parser, or (b) accept WORSHIPS on locations and update the architecture doc to drop the dangling `RELIGION_OF` mention. **This was not introduced by Stage 3a — it's an upstream taxonomy gap surfaced by the audit.**

### MED-2: FOUNDED direction bug on faction Founder field (~14 skeletons)
On organization.faction / organization.house pages, `Founder` field emits `FOUNDED` with `direction: forward`, producing edges like `Kingsguard FOUNDED Aegon I`. Direction should be reverse to match architecture's "Founder → Founded" rule. Affects 14 skeletons (per the 22-edge-type count above). Parser-level fix; rerunning emit-deterministic.py after parser fix would correct the skeletons.

### MED-3: Wiki chapter-index pages classified as event.battle (24 skeletons)
24 skeletons in `battles-*` buckets are wiki chapter-index pages (e.g., `A Storm of Swords-Chapter 71`, `Alayne I-The Winds of Winter`, `Barristan I-The Winds of Winter`). They're typed `event.battle` (either from infobox-data or from page-index entity_type_guess) and have empty edges. They're not battles — they're navigational page-stubs that index a single in-book chapter. This is a triage placement / parser classification issue; Stage 3a faithfully emits what upstream produced. Recommend triaging these out before Stage 3b runs against the battles buckets, OR re-typing them. List enumerated in audit log.

### MED-4: One `unknown`-typed skeleton, plus House-guards / Theories pages typed organization.house
- `battles-b/skeleton/battle-of-the-blackwater-song.node.md` typed `unknown` — actually `object.text` (a song). 1 instance.
- `houses-other-b-h/skeleton/house-bolton-guards.node.md`, `house-arryn-guards`, `house-stark-guards`, `house-tully-guards`, `house-targaryen-guards`, `house-tyrell-guards`, `house-towers`, `house-cassel-theories` — typed `organization.house` but they are descriptive page-stubs ("the guards employed by House Bolton") or `/Theories` disambiguation pages. ~8 instances.
- All have empty edges (so no graph corruption), but they will land in the wrong type-bucket if Stage 3b promotes them.

### LOW-1: Unicode passthrough (1,134 skeletons NBSP, 5 en-dash, 1 curly-quote)
Per task brief criterion 6, this is documented passthrough — Stage 3a's contract is verbatim, normalization happens at graph-build time. Counts logged here for the eventual normalization step.

### LOW-2: Date-as-target in BORN_AT / DIED_AT / BURIED_AT
Many character pages have date strings (e.g., `269 AC`, `48 AC`) emitted as targets of place edges, alongside the actual location target. Two-target pattern is consistent across the corpus. Future graph-build step can split target-is-date vs target-is-place by regex.

### LOW-3: Boilerplate / placeholder targets
Sporadic targets like `See below`, `religions`, `Wives` are wiki-text artifacts, not entities. Future entity-resolution pass needs a stop-list. Affects a small fraction (<20 across corpus).

### LOW-4: aliases-equals-page-name
A handful of skeletons (e.g., Likely Luke) have `aliases: ["<page_name>"]`. Benign redundancy from parser; deduplicating against `name` would be a one-line parser fix.

## Recommendation

**Proceed to Stage 3b launch prep.** The deterministic skeletons are clean against the contracts that matter:
- Edge vocabulary fully locked at 22 types.
- Slug rule clean across 3,315/3,315.
- Edge fidelity (count, format, order, qualifier preservation) clean across all sampled skeletons.
- The 624 Tier A skeletons specifically destined for Stage 3b are well-formed.

**Pre-launch one decision item for Matt:**
- **MED-1 (WORSHIPS on locations):** decide whether to add `RELIGION_OF` to the locked vocabulary or accept WORSHIPS on locations. This affects 112 skeletons but most are Tier B places, so it does NOT block the 624 Tier A Stage 3b run.

**Defer to post-Stage-3b cleanup (no need to gate the launch):**
- MED-2 FOUNDED direction (14 skeletons; parser fix + re-emit).
- MED-3 / MED-4 misclassified chapter-index and House-guards pages (~33 skeletons total; triage filter or type override). All have empty edges so they're not corrupting graph data, just sitting in the wrong type-bucket.
- All LOW issues — graph-build-time normalization per `working/todos.md`.

No HIGH issues. No vocabulary violations. No fidelity violations. The Python emitter did its job.
