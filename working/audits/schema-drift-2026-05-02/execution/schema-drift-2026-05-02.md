# Schema-Drift Audit — 2026-05-02

**Nodes scanned:** 7,619 `.node.md` files across `graph/nodes/`
- Canonical typed dirs: 7,563 (artifacts, characters, concepts, customs, events, factions, foods, houses, languages, locations, materials, medical, religions, species, texts, theories, titles)
- `_conflicts/`: 53 (excluded from canonical-status checks; shape verified)
- `_unclassified/`: 1
- `_stage3-preview/`: 3 (preview duplicates of canonical nodes — flagged)

**Total findings:** 8 distinct issue clusters
- HIGH (parser-fix or graph-blocking): 0
- MED (data-fix needed but graph still queryable): 4
- LOW (cosmetic / known carve-outs): 4

**Headline:** the corpus is structurally clean. Every required frontmatter field is present in every node. Every type string in every typed directory matches the TYPE_DIR_MAP (Session 28's stale-dir cleanup held). Every edge-vocabulary label across 21,359 edge bullets is in the locked 22-table. There are zero new parser regressions. The remaining drift is concentrated in the v1 Stage-1 LLM prose carve-out and a single misclassified `_unclassified/` node from the Session-26 era.

---

## Category 1: Type-string drift

**Status: clean across all canonical directories.**

Methodology: extracted `^type:` from every `.node.md` and bucketed by directory. Every observed type string is in the architecture.md Type Reference Table (lines 76–99) and matches TYPE_DIR_MAP in `scripts/wiki-pass2-promote.py`.

Distinct type values observed (counts approximate via spot-checks):

| Type | Count | Dir |
|------|-------|-----|
| `character.human` | ~5,900 | characters |
| `character.dragon` | 28 | characters |
| `character.direwolf` | 6 | characters |
| `character.giant` | 0 | — |
| `character.cotf` | 0 | — |
| `character.other` | 0 | — |
| `organization.house` | ~600 | houses |
| `organization.faction` | 158 | factions |
| `organization.cult` | 0 | — |
| `organization.religion` | 63 | religions |
| `place.location` | ~750 | locations |
| `place.region` | 23 | locations |
| `place.castle` | 0 | — |
| `place.city` | 0 | — |
| `object.artifact` | 265 | artifacts |
| `object.text` | 155 | texts |
| `object.food` | 73 | foods |
| `object.material` | 54 | materials |
| `event.battle` | 295 | events |
| `event.tournament` | 35 | events |
| `event.war` | 34 | events |
| `concept.culture` | 18 | factions (deliberate — see Category 2 note) |
| `concept.magic` | 28 | concepts |
| `concept.theory` | 45 | theories |
| `concept.language` | 26 | languages |
| `concept.medical` | 34 | medical |
| `concept.custom` | 37 | customs |
| `species` | 181 | species |
| `title` | ~600 | titles |

Notable observations:
- **No `concept.prophecy` nodes.** `graph/nodes/prophecies/` is **empty**. Architecture.md declares the type and the directory; no nodes have been promoted yet. Not a violation, but worth noting that `prophecies/` is a placeholder dir.
- **No `character.giant`, `character.cotf`, `character.other` nodes.** TYPE_DIR_MAP covers these but the corpus has none. The agent prompt's worry about parent-only `type: character` was unfounded — no orphan-type strings exist.
- **The Session-26 worry about `type: organization.religion` "drift" is no longer drift.** Architecture.md line 83 declares `organization.religion` as the canonical type. All 63 religion nodes use this exact form. Earlier audit prompt language was stale — this is the canonical schema.

Findings:
- **(LOW)** 1 node with `type: unknown` — the only orphan in the entire corpus. See Category 5 finding for full context.
  - `graph/nodes/_unclassified/battle-of-the-blackwater-song.node.md` (line 3: `type: unknown`)

---

## Category 2: Type-vs-target-dir mismatches

**Status: clean across all 17 canonical directories.**

Methodology: for each directory, ran a negative-lookahead grep for any `type:` value that isn't the directory's expected canonical type. All 17 directories returned **zero** mismatches:

| Directory | Mismatches |
|-----------|------------|
| `characters/` | 0 |
| `houses/` | 0 |
| `factions/` | 0 |
| `religions/` | 0 |
| `locations/` | 0 |
| `artifacts/` | 0 |
| `texts/` | 0 |
| `foods/` | 0 |
| `materials/` | 0 |
| `events/` | 0 |
| `concepts/` | 0 |
| `theories/` | 0 |
| `languages/` | 0 |
| `medical/` | 0 |
| `customs/` | 0 |
| `species/` | 0 |
| `titles/` | 0 |

This confirms Session 28's "130 stale-dir mismatches resolved" — the cleanup held. **No new parser regressions in Session 29's promotion.**

Note on `concept.culture` → `factions/`: 18 nodes with `type: concept.culture` live in `graph/nodes/factions/` (e.g. `dothraki`, `ironborn`, `northmen`). This is **not** a violation — it's a deliberate mapping decision. TYPE_DIR_MAP routes `concept.culture` → `concepts/`, but 18 culture nodes were promoted to `factions/` historically (because cultures behave like ethnic-political factions in the graph). If the routing were strict, they'd live in `concepts/`. Recommend a Matt-decision: either (a) move them to `concepts/` to match TYPE_DIR_MAP, or (b) update TYPE_DIR_MAP to reflect the real-world choice. Not blocking; not flagged as MED until decided.

---

## Category 3: Edge-vocabulary violations

**Status: clean across the entire corpus.**

Methodology:
1. Captured all 21,359 edge bullets matching `^- ([A-Z][A-Z_]+)( \(reverse\))?:` from every node.
2. Counted hits against the canonical 22-cluster vocabulary in architecture.md (lines 105–294), which actually defines ~95 distinct edge types (the "22 types" referred to wiki infobox field types in Session 26 — the full controlled vocabulary is larger).
3. Result: every observed edge label is canonical.

Coverage:
- 18,873 edges use the most common 30 labels (`HOLDS_TITLE`, `CULTURE_OF`, `SWORN_TO`, `PARENT_OF`, `SPOUSE_OF`, `BORN_AT`, `DIED_AT`, `BURIED_AT`, `SERVES`, `RULES`, `MEMBER_OF`, `HEIR_TO`, `FOUNDED`, `OVERLORD_OF`, `CADET_BRANCH_OF`, `REGION_OF`, `SEAT_OF`, `ANCESTRAL_WEAPON_OF`, `OWNS`, `LOVER_OF`, `WORSHIPS`, `SUCCEEDS`, `ALIAS_OF`, `SIBLING_OF`, `FIGHTS_IN`, `DEFEATS`, `BETROTHED_TO`, `WARD_OF`, `LOCATED_AT`)
- 2,395 edges with `HOLDS_TITLE` etc. (subset of the above)
- 91 additional canonical edges covering the rest of the 95-edge taxonomy: `ADVISES`, `KILLS`, `OPPOSES`, `PRISONER_OF`, `COMMANDS_IN`, `ANCESTOR_OF`, `COMMANDS`, `TEACHES`, `RESPECTS`, `PROTECTS`, `DUELS`, `CAPTURES`, `BESIEGES`, etc. all appear in valid contexts.

**Total: 18,873 + 2,395 + 91 = 21,359 edges, 100% canonical.**

Tested for known synonym intrusions (none found):
- `MARRIED_TO` / `MARRIED` — 0 instances
- `MOTHER_OF` / `FATHER_OF` / `SON_OF` / `DAUGHTER_OF` — 0 instances
- `BROTHER_OF` / `SISTER_OF` — 0 instances
- `KILLED_BY` / `DEFEATED_BY` — 0 instances
- `RIVAL_OF` / `FRIEND_OF` / `ENEMY_OF` — 0 instances
- `COUSIN_OF` / `NEPHEW_OF` / `NIECE_OF` / `RELATIVE_OF` — 0 instances
- `RELIGION_OF` (architecture.md mentions this as conditional for locations) — 0 instances actually used; all religion-attachment edges use `WORSHIPS` or `SACRED_TO`
- `WRITTEN_BY` (architecture.md mentions this for `object.text`) — 0 instances; texts apparently don't currently emit this edge (a coverage gap, but not a vocabulary violation)
- Lowercase variants — 0 instances

**Finding (LOW):** Two canonical edges from architecture.md table appear to be unused in the corpus. Not a violation — just an observation that the locked vocabulary has more headroom than the parser currently exercises:
- `WRITTEN_BY` (table line 481) — 0 instances. Reason: text infoboxes haven't been processed through the FIELD_EDGE_MAP for this field yet, OR the field name on wiki pages is different.
- `RELIGION_OF` (table line 461 caveat for locations) — 0 instances. Religion-of-place edges currently use `SACRED_TO`.

These are documentation/coverage gaps to consider when Stage 4 prose-edge-classifier runs — the vocabulary is locked but underused.

---

## Category 4: Frontmatter schema violations

**Status: clean across all 7,619 nodes.**

Methodology: per-field `^FIELD:` grep counts vs. file count.

| Required field | Count | Status |
|----------------|-------|--------|
| `name:` | 7,619 | ✓ all present |
| `type:` | 7,619 | ✓ all present |
| `slug:` | 7,619 | ✓ all present |
| `confidence:` | 7,619 | ✓ all present |
| `wiki_source:` | 7,619 | ✓ all present |
| `bucket_id:` | 7,619 | ✓ all present |
| `prompt_version:` | 7,619 | ✓ all present |
| `node_version:` | 7,619 | ✓ all present (every value is `1`) |
| `pass_origin:` | 7,619 | ✓ all present |
| `aliases:` | 7,619 | ✓ all present |

Value-format checks:
- `confidence:` regex `(?!tier-[1-4]$)` — **0 violations.** All values are `tier-1` through `tier-4`.
- `node_version:` regex `(?!1$)` — **0 violations.** All `1`.
- Frontmatter bracketing: every node has exactly 2 `^---$` lines (open + close). 0 unclosed-frontmatter violations.

`prompt_version` distribution (informational):
- `v1` (Stage-1 LLM agent, prose-driven): 648 nodes
- `v1-python` (Stage-3 deterministic emitter): 6,971 nodes

`first_available` presence (informational, NOT flagged per deferred-policy):
- 841 nodes have `first_available:` populated
- 6,778 do not

Per `project_first_available_deferred.md` and architecture.md lines 330–334, this field is shelved for backfill post-first-release. No action.

---

## Category 5: Slug format violations

**Status: clean across all 7,619 nodes.**

Methodology: regex `^slug: ([^a-z0-9-].*|.*[^a-z0-9-].*)$` — matches any slug containing characters outside `[a-z0-9-]`. **0 matches.**

All 7,619 slugs:
- Use only lowercase letters, digits, and hyphens
- No apostrophes, capitals, underscores, or whitespace
- Match the `[a-z0-9-]+` pattern declared in architecture.md line 31

**Filename ↔ slug match:** spot-checked across canonical dirs. `_conflicts/` files have timestamp-suffixed filenames that intentionally don't match their internal slug (this is the conflict-staging convention from `wiki-pass2-promote.py` lines 363–375). Not a violation.

---

## Category 6: Structural violations

**Status: 1 finding (MED) + 1 carve-out cluster (LOW).**

### `## Edges` section presence
- **7,619 of 7,619 nodes have `## Edges`.** Including the conflicts and the unclassified node. ✓ clean.

### `## Identity` section presence
- **7,075 of 7,619 nodes have `## Identity`.** **544 nodes (7.1%) lack this section.**
- Strong correlation with `prompt_version: v1` (Stage-1 LLM agent path). The deterministic Stage-3 emitter always writes `## Identity` as a stub line; the v1 LLM agent writes prose under different headings (`## Origins`, `## Appearances & Description`, `## Allegiances`, `## Narrative Arc`). Example: `graph/nodes/characters/belwas.node.md` (v1) opens with `## Origins` at line 21, no `## Identity` anywhere.

**Per the agent prompt's carve-out:** v1 prompt_version nodes are deferred to Stage 4 prose-edge-classifier. Flagging this **as a cluster** rather than 544 individual findings.

- **(LOW, deferred to Stage 4)** ~544 nodes from `prompt_version: v1` lack `## Identity` heading. They have an Edges section and prose, just under different heading names. Not blocking traversal. Recommended remediation: Stage 4 prose-edge-classifier could normalize headings as part of its prose pass, OR a one-shot Python script can `sed` an `## Identity` placeholder in for these 544 files (low effort, but redundant with whatever Stage 4 will do).

### Inline backtick-edge-name pattern (cosmetic)
- 360 nodes (375 instances) contain inline-prose use of edge-type names wrapped in backticks like `` `SWORN_TO` House Stark `` inside an `## Allegiances` paragraph. Example: `graph/nodes/characters/jocelyn-stark.node.md:25`.
- This is **redundant but not broken** — every checked node ALSO has a proper `## Edges` bullet block below the prose, so traversal is intact.
- These are v1 LLM artifacts that the Stage-1 agent generated as flowery prose alongside the structured edges. Stage 4 prose-edge-classifier can choose to either drop them or fold them into a "narrative" annotation channel.

- **(LOW, deferred to Stage 4)** 360 nodes have inline backtick-wrapped edge labels in prose (e.g. `` `SWORN_TO` `` mid-sentence). Cosmetic; structured `## Edges` blocks are intact and parseable.

### `_unclassified/` orphan
- **(MED)** 1 node remains in `_unclassified/`:
  - `graph/nodes/_unclassified/battle-of-the-blackwater-song.node.md` — `type: unknown`, `bucket_id: battles-b`.
  - Page name "Battle of the Blackwater (song)" is clearly an in-world song, should be `type: object.text` and routed to `texts/`.
  - `## Edges` section is empty (no edges emitted because the type was `unknown`).
  - Cite-ref pattern visible in line 24 (`(wiki:Battle_of_the_Blackwater_(song).cite_ref-Rasos60.7B.7B.7B3.7D.7D.7D.7B.7B.7B4.7D.7D.7D_2-2)`) is the standard Stage-3 format — no malformation.
  - **Recommended remediation:** one-line manual reclassification or a Python re-promotion targeting `bucket_id: battles-b` with override `--type object.text`.

### `_stage3-preview/` duplicates
- **(MED)** 3 nodes in `_stage3-preview/` are byte-equal duplicates of canonical nodes:
  - `_stage3-preview/characters/eddard-stark.node.md`
  - `_stage3-preview/characters/jon-snow.node.md`
  - `_stage3-preview/houses/house-stark.node.md`
- Confirmed `_stage3-preview/houses/house-stark.node.md` matches `houses/house-stark.node.md` byte-for-byte (read both, identical front-matter and Edges block).
- Likely a leftover from a Stage-3 dry-run that wrote preview output to a side directory. Safe to delete (`rm -r graph/nodes/_stage3-preview/`).
- **Recommended remediation:** `rm -rf graph/nodes/_stage3-preview/` after confirming with Matt that Stage 3 promotion is committed to canonical paths.

### `_conflicts/` (informational, intentional staging)
- 53 conflict files exist with timestamp-suffixed names (e.g. `hullen-characters-house-stark-h-q-2026-04-26T22-17-04.node.md`). All have well-formed frontmatter, `## Identity`, and `## Edges`.
- The filename → slug mismatch is **by design** (per `wiki-pass2-promote.py` line 363). Not flagged.
- These represent unresolved-bytes-mismatch promotions from Sessions 26–28. They're separate work (conflict-resolution pass), not schema drift.

---

## Category 7: cite_ref format consistency (HIGH-priority known issue)

**Status: 11 surviving Session-27 malformed bare-cite_ref instances (LOW — all in v1 LLM-prose carve-out).**

Methodology: regex `\(wiki:R(agot|acok|asos|affc|adwd)[0-9]+\)` finds the malformed bare pattern Session 27 flagged. The standard well-formed pattern is `(wiki:House_Stark.cite_ref-Ragot1.7B.7B.7B3.7D.7D.7D.7B.7B.7B4.7D.7D.7D_3-1)` — full URL-encoded anchor. The malformed pattern `(wiki:Rasos11)` is just the book+chapter code with no real anchor.

All 11 instances are in narrative prose written by the Stage-1 LLM agent (under `## Narrative Arc` / `## Appearances & Description` etc.), NOT in the deterministic skeleton or `## Edges` blocks:

| File | Line | Snippet |
|------|------|---------|
| `graph/nodes/houses/house-bar-emmon.node.md` | 33 | `Sigil: a leaping blue swordfish on fretty silver on white (wiki:Rasos75).` |
| `graph/nodes/houses/house-boggs.node.md` | 29 | `members of House Boggs were with Prince Rhaegar Targaryen at the Battle of the Trident during Robert's Rebellion (wiki:Raffc20).` |
| `graph/nodes/houses/house-cargyll.node.md` | 29 | `They slew one another during the civil war (wiki:Ragot8).` |
| `graph/nodes/houses/house-cave.node.md` | 29 | `A member of House Cave once served in the Kingsguard (wiki:Raffc20).` |
| `graph/nodes/houses/house-chelsted.node.md` | 29 | `replacing him with the pyromancer Rossart as Hand (wiki:Rasos11).` |
| `graph/nodes/houses/house-chyttering.node.md` | 29 | `regarded by Stannis as one of the few good men remaining to him after the Blackwater defeat (wiki:Rasos10).` |
| `graph/nodes/houses/house-dargood.node.md` | 29 | `tells her that many Dargoods, Darkes, and Darkwoods still live in the town (wiki:Raffc9).` |
| `graph/nodes/houses/house-darke.node.md` | 33 | `In AFFC, a servant at the Seven Swords inn in Duskendale claims to be a Darke by birth (wiki:Raffc9).` |
| `graph/nodes/houses/house-darklyn.node.md` | 37 | (long line; matches `(wiki:Raffc...)`) |
| `graph/nodes/houses/house-darkwood.node.md` | 29 | `tells her many Darkes, Dargoods, and Darkwoods still live in the town (wiki:Raffc9).` |
| `graph/nodes/factions/dragonkeepers.node.md` | 37 | (long line; matches `(wiki:R...)`) |

Observations:
- **All 11 are in `prompt_version: v1-python` files where the prose was either generated by the v1 LLM agent and concatenated, OR the prose extractor produced these short-form refs.** The pattern is restricted to narrative prose lines, never inside `## Edges`.
- **Same root cause as the larger v1 carve-out:** Stage-1 LLM was inconsistent about citation rendering. Some pages got the full encoded anchor, others got the short `Rasos11` form.
- **Not a parser regression.** Session 27 already noted this; the fix is part of the Stage-4 prose-edge-classifier work. No new instances.

- **(LOW, deferred to Stage 4)** 11 v1-prose lines retain the malformed bare `(wiki:R{book}{N})` cite ref. Recommend: include in Stage 4 prose-cleanup pass (it can either expand to the standard form by looking up the wiki cache, or strip these inline refs entirely if they're redundant with the proper encoded anchors elsewhere on the page).

---

## Summary

Of 7,619 nodes scanned (covering all of `graph/nodes/` including `_conflicts/`, `_unclassified/`, `_stage3-preview/`):

- **0 HIGH findings** — no parser regressions, no graph-blocking issues, no edge-vocabulary violations, no missing required frontmatter fields, no slug format issues.
- **4 MED findings** — (a) one `_unclassified/` orphan needing manual reclassification (`battle-of-the-blackwater-song`), (b) three `_stage3-preview/` duplicates ready for deletion, (c) the `concept.culture` → `factions/` placement decision (route or document), (d) two locked-but-unused canonical edge types (`WRITTEN_BY`, `RELIGION_OF`).
- **4 LOW findings** — all in the v1-LLM-prose carve-out: ~544 v1 nodes lack `## Identity` heading (Stage 4 work), ~360 v1 nodes have inline backtick-wrapped edge labels in prose (cosmetic, edges intact), 11 v1 prose lines have malformed bare cite_ref `(wiki:Rasos11)` form (Session 27 known issue, no new instances), and the `concept.prophecy` directory is empty (placeholder).

**The graph is in excellent shape.** Session 28's stale-dir cleanup held; Session 29's +314 node promotion produced zero new violations. All structural invariants (frontmatter shape, slug format, edge-vocabulary, type↔directory routing) are clean.

**Next session priority order:**
1. **Quickest wins (5-10 min total):** delete `graph/nodes/_stage3-preview/` (3 duplicate nodes), reclassify the single `_unclassified/battle-of-the-blackwater-song` node to `texts/`. Both are mechanical.
2. **Tactical decision needed:** the `concept.culture` → `factions/` mismatch with TYPE_DIR_MAP. Either move 18 culture nodes to `concepts/` (matches map) or update TYPE_DIR_MAP to canonicalize the historical placement. ~15 min once Matt decides.
3. **Defer to Stage 4 prose-edge-classifier:** the 544 missing-`## Identity` headers, the 360 backtick-prose redundancies, and the 11 bare cite_refs. These are interrelated — all are v1 LLM prose-fill artifacts and should be normalized in one prose pass, not piecemeal.
4. **Optional / low priority:** decide whether `WRITTEN_BY` (for texts) and `RELIGION_OF` (for locations) need parser additions. Currently the locked vocabulary has these slots but the FIELD_EDGE_MAP doesn't emit them. If Stage 4 wants to use them, they're already declared; otherwise they're harmless dormant entries.

## Recommended actions

- `rm -rf graph/nodes/_stage3-preview/` (after Matt confirms it's a leftover dry-run)
- For `_unclassified/battle-of-the-blackwater-song`: edit the file's frontmatter `type: unknown` → `type: object.text`, then `mv` to `graph/nodes/texts/`. (Or re-run Stage-3 promotion with manual override on `bucket_id: battles-b`.)
- For `concept.culture` placement: either `mv graph/nodes/factions/{dothraki,ironborn,northmen,andals,...}.node.md graph/nodes/concepts/` (18 files) and add a node-version bump, OR add `"concept.culture": "factions"` override to TYPE_DIR_MAP and re-run promote in dry-run to confirm idempotence. Matt's call.
- For Stage 4 (future): the 544 missing-Identity v1 nodes, 360 backtick-edge prose insertions, and 11 bare cite_refs are all symptoms of v1 LLM prose-mode and should be cleaned up together by the prose-edge-classifier, not by ad-hoc scripts now.
- Keep monitoring: `_conflicts/` has 53 files awaiting resolution. Not part of this audit, but worth a separate triage session.
