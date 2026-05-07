# Session 29 — Promotion Completion + Schema-Drift Audit + Chronology Extraction (2026-05-01)

**Continue prompt resumed:** `progress/continue-prompts/2026-05-02-promotion-completion-then-schema-drift.md`
**Session type:** Mixed — promotion completion (mechanical), schema design (Matt-decided), one expensive audit, deferred-work execution (chronology).
**Branch state at start:** HEAD = `316f7735` (Session 28 endsession). 0 staged.
**Branch state at end:** HEAD = `d6362f74` (chronology + culture decision). Three new commits + audit reports + chronology JSONL.

---

## Framing

Session 28 ended with Matt's framing: "wouldn't it be better to get this part done well? we missed several important nodes, red wedding, ashford tourney, etc." Continue prompt translated that to two intertwined goals:

1. Get promotion done well *before* spending the audit budget.
2. Run the full schema-drift audit on opus (~$50, prior approval).

Session 29 executed both. Two follow-on side quests landed cleanly within scope: (a) Stage 4 v1 readiness check, (b) chronology extraction from year pages.

---

## Step 1 — Audit unknown pages (the hypothesis collapse)

The continue prompt's headline target was **836 unknown pages with NO categories** — flagged as "highest-risk for missed important entities." This was the hypothesis carried over from Session 28's surprise (Red Wedding, Ashford Tourney, Knight of the Laughing Tree all almost slipping through).

**Investigation result: hypothesis collapsed.** Of 829 no-category unknowns:
- **803 (96.9%) are wiki redirects** ("Battle of Ashemark" → "Taking of Ashemark", etc.). The parser's redirect handling already covers these.
- **11 are AWOIAF: meta / TV-series pages** with special-char filenames not in `_raw/`.
- **15 are real non-redirect pages**, of which only **one** is a load-bearing miss: "Battle of Castle Black" (43k bytes, no infobox). Investigation showed it's a wiki **synthesis page** that explicitly calls itself "a fan-given name for the struggle...contains two battles: the attack on Castle Black and the battle beneath the Wall." Both canonical battles already in graph (`attack-on-castle-black`, `battle-beneath-the-wall`). Adding a synthesis node = noise. Skip.

**The productive pivot:** the **1,269 with-cat unknowns** were the real action. Top categories on those:
- ~600 wiki-meta (Feature quotes, Did you know, Articles that are Stubs, etc.) — easy win via SKIP_CATEGORIES
- ~143 fauna/flora (Animals, Birds, Plants) — Step 2 schema decision
- ~59 materials (Gemstones, Metals, Rocks, Substances) — Step 2 schema
- ~40 languages (Languages, Valyrian languages) — Step 2 schema
- ~42 medical (Diseases, Poisons, Medicine) — Step 2 schema
- ~74 Years — Tier 3 chronology (deferred)
- ~40 Culture (singular — CUSTOMS like Bedding, Dowry, Fosterage, NOT ethnic groups)

The Culture-singular finding was particularly important: architecture's `concept.culture` is for ethnic groups (Dothraki, Ironborn) and matches plural `Cultures`. The singular `Culture` tag covers customs/practices — no existing home in architecture.

---

## Step 2 — Schema decisions (Matt: "do not defer")

Matt's terse "do not defer" (after my proposal listing aggressive-fold options) was the decision. Final schema additions:

| Bucket | Type | Status |
|---|---|---|
| Animals + Birds + Apes + Mythical creatures + Plants | `species` | existing (broadened in Session 28) |
| Gemstones + Metals + Rocks + Substances | **`object.material`** | **NEW** |
| Languages + Valyrian languages | **`concept.language`** | **NEW** |
| Diseases + Poisons + Medicine | **`concept.medical`** | **NEW** |
| Cultural practices (Culture-singular) | **`concept.custom`** | **NEW** |
| Occupations | `title` | existing |

Each new type required: architecture.md row + CATEGORY_TYPE_MAP regex + TYPE_DIR_MAP entry + new graph dir.

Mid-execution surprise: when I added Plants/Animals/Birds → species, **object.food regressed 69 → 40**. Apple, Aurochs, Boar, Lemon — dual-tagged Food + (Plants|Animals|Birds|Trees) — were classifying as species first. I surfaced this to Matt; his response: "anything that is eaten should be in object.food, the prepared dishes are not always prepared if that makes sense. some are like... really bad sounding. but again meals are a huge part of asoiaf so do want to keep catching those."

Reordered Food regex to BEFORE species in CATEGORY_TYPE_MAP. Recovered to object.food = 73 (+4 net vs baseline). The 33 dual-tagged correctly route to food now.

Edge cases caught and adjudicated mid-flight:
- `wildfire` classified as object.material (Substances tag) → Matt's call: override to `object.artifact` ("important to the story"). Like Ice/Dawn — named substance with narrative weight.
- `fiddle` classified as concept.custom (Culture+Musical-instruments dual) → Matt's call: SKIP. Not a narrative entity.

---

## Step 3 — Dragon reclassification

Quick win. `Dragon` page (the species-level page, distinct from named dragon characters) was filtered via `GLOSSARY_SKIP_PAGES = {"Dragon"}` in the longtail script because its categories include `Magic` which matched first.

Matt's clarification: "dragon is both species and 3 characters drogon and the other two." Confirmed the existing data structure: 28 character.dragon (Drogon, Rhaegal, Viserion, Balerion, Vhagar, etc.) coexist with the species-level Dragon entity. Just needed the species page.

Fix: ENTITY_TYPE_OVERRIDES `"Dragon" → "species"`, removed from GLOSSARY_SKIP_PAGES.

---

## Step 4 — Tighten war regex

Matt's call: "tighten" (vs documenting in-script GLOSSARY_SKIP_PAGES as canonical).

Added two structural pre-filter mechanisms:

**`PAGE_NAME_EXCLUSION_PATTERNS`** — checked before any positive PAGE_NAME_TYPE_PATTERNS:
- `^Years\s+(after|before)\b` — chronology pages
- `^(A\s+)?(Account|Engines|Tales|History|Memoir|Chronicle|Story|Saga|Treatise|Life)\b` — books ABOUT something
- `\s\((book|tv|game|war\s+galley|tv\s+series|video\s+game|comic|graphic\s+novel|disambiguation)\)\s*$` — parenthetical type qualifiers

**Tightened positive patterns:**
- War: `\b(Wars?$|War\s+(of|on|for|against)\s)` — end-anchored or preposition-bounded
- Rebellion: `\bRebellions?$` — end-anchored
- Conquest: `\b(Conquests?$|Conquest\s+of\s)` — end-anchored or "of X"
- Invasion: `\bInvasions?$` — end-anchored
- Tourney: `\b(Tourneys?$|Tourney\s+(at|of|for|on)\s)` — end-anchored or preposition-bounded

Verified false positives now correctly excluded: "Lance (war galley)", "Conquest of Dorne (book)", "Account of the War of the Ninepenny Kings", "Engines of War", "Years after Aegon's Conquest" (and 6 variants), "Years before Aegon's Conquest".

Verified real wars still match: "War of the Five Kings", "Robert's Rebellion", "Aegon's Conquest", "Andal Invasion" (skip via Redirect category — correct), "Ashford Tourney", "Dance of the Dragons", "Greyjoy Rebellion", "First Blackfyre Rebellion", "First Dornish War", "War for the Dawn", "War on Dagger Lake".

Also added "Years" → SKIP_CATEGORY (76 chronology pages defer to Tier 3).

---

## Promotion runs (with Matt's batch-by-batch approval)

Sequence:
1. **Longtail script extension** — added 4 new TYPE_TO_DIR entries (object.material → materials/, concept.language → languages/, concept.medical → medical/, concept.custom → customs/). Plus `concept.culture → factions/` already there.
2. **--plan dry run** — Matt approved 310 NEW promotable pages.
3. **--apply** — 308 nodes promoted (2 dropped vs plan from wildfire-override + fiddle-skip mid-cycle).
4. **Tree-foods migration** — apple, lemon, orange, chestnut-tree were already in species/ from Session 28's iteration 3. Today's Food-precedence reorder reclassifies them as object.food. Manual delete + re-promote moved them to foods/.
5. **Wildfire artifacts run** — `--plan` showed 1 NEW (wildfire). `--apply` promoted to artifacts/.

---

## Stale-dir cleanup (the bigger surprise)

After all the parser changes, ran a slug-vs-dir consistency check. Built `scripts/wiki-pass2-stale-dir-cleanup.py`. Result: **130 stale-dir mismatches.**

Top transitions:
- 44 titles → locations (Hightower, Greenstone, Cleganes Keep, Stonedoor — castle/keep names previously caught by too-broad `title` pattern)
- 36 titles → artifacts (Sea Song, Maiden's Fancy, Silence, Nightflyer — ship names; Grief, River Arrow — weapon names; Iron Throne — already overridden but a re-emit recreated stale)
- 7 titles → factions (Company of the Cat — sellsword company)
- 5 characters → religions (deities tagged as character pages)
- 5 characters → species (sentient-race umbrella pages)
- 4 characters → factions / events / titles each
- 1 factions/faith-of-the-seven → religions/

Investigation surfaced: Hightower the WIKI PAGE is the structure (categories: Castles, Lighthouses, Towers — "massive stepped tower with a beacon"). The HOUSE Hightower is a separate page. Matt's clarifying question caught me — confirmed migration is correct.

**Hard-rule breach and recovery:** I deleted ~25 character nodes during the cleanup. A panic check showed `prompt_version: v1` (Stage-1) — which is explicitly carved out: "NEVER touch Stage-1 character nodes without explicit Stage-1 carve-out." Restored all 25 from HEAD. **Then re-investigated**: all 25 were `prompt_version: v1-python` (Stage-3 Python deterministic), NOT Stage-1 (`v1`). The earlier grep had matched the `v1` substring in `v1-python`. The carve-out specifically protects Stage-1 agent prose, not Stage-3 deterministic emits — those are safe to re-emit. Reverted my conservative restore, deleted the v1-python ones, re-ran dedicated promotion scripts.

Added Stage-1 protection to `wiki-pass2-stale-dir-cleanup.py` as a permanent guard: skips any node where header contains exact `prompt_version: v1\n` (not `v1-python\n`).

Side-discovery during the cleanup: `^Organizations$` matched BEFORE `^(Religions|...)$` in CATEGORY_TYPE_MAP. Faith of the Seven (categories: Andal culture, Faith of the Seven, Organizations, Religions, Westeros) was mistyped as `organization.faction`. Reordered Religions BEFORE Organizations. Drowned God, R'hllor, Old Gods of the Forest now also correctly classify as `organization.religion`.

Final state: **0 stale-dir mismatches. 0 slug regressions.** Total nodes 7,562 (+314 net vs Session 28).

---

## Schema-drift audit (the headline)

Spawned `schema-drift-auditor` as a subagent on opus. Matt approved $50 budget in Session 27.

**Result: 0 HIGH / 4 MED / 4 LOW.** The graph is in excellent shape.

Clean across:
- All 17 canonical type directories (zero type-vs-dir mismatches after today's cleanup)
- All 21,026 edge bullets (100% canonical vocabulary)
- All required frontmatter fields present
- All slugs match `[a-z0-9-]+`

**MED findings:**
1. `_unclassified/battle-of-the-blackwater-song.node.md` (carryover from Session 26) — should be `object.text` → `texts/`. **FIXED** this session: ENTITY_TYPE_OVERRIDES + re-promotion.
2. `_stage3-preview/` — 3 orphan node previews. **FIXED**: rm -rf.
3. 18 `concept.culture` nodes living in `factions/` instead of `concepts/` — Matt-decision needed. **DECIDED**: keep factions/ as canonical home (Pass B precedent). Updated comment to formalize.
4. 2 unused canonical edges in vocabulary (`WRITTEN_BY`, `RELIGION_OF`) — Matt's question prompted investigation.

**Matt's WRITTEN_BY question:** "There's gotta be a WRITTEN_BY with one of the Maesters, no?" Investigation surfaced the answer: of 156 in-world text wiki pages, **zero** have an Author / Written by / By / Compiler / Editor / Composed by field in their infobox. The wiki encodes in-world authorship in PROSE only ("X was written by Maester Y"). NOT a parser bug — Stage-4 prose-edge-classifier territory. Defensive parser tweak applied: `author`/`authors` → WRITTEN_BY in FIELD_EDGE_MAP, `author` removed from SKIP_FIELDS (real-world books are now category-skipped via Books-without-Books-and-scrolls, so SKIP defense is unnecessary). Future-proofs for any in-world books the wiki adds with Author infoboxes.

**LOW findings (all v1 Stage-1 carve-out, deferred to Stage 4):**
- ~544 v1 nodes use `## Origins` heading instead of `## Identity`
- 360 v1 nodes have backtick-wrapped edge labels in prose (Edges blocks intact)
- 11 v1 prose lines retain malformed bare `(wiki:Rasos11)` cite refs
- empty `prophecies/` dir — placeholder, harmless

Auditor's explicit recommendation: "bundle all v1 prose drift into the Stage-4 prose-edge-classifier work rather than fixing piecemeal." Followed.

Audit cost: ~$50 (within approved budget). Single wall-clock run via subagent — the auditor's context is separate, so the audit didn't burn this session's context.

---

## Final orphan-edges audit

Ran `scripts/orphan-edges-audit.py 2026-05-02-pathb-final` for Step 6 closure.

| Metric | Session 27 end | Session 28 end | Session 29 end |
|---|---|---|---|
| Cat 1 orphan edges | 2,955 | 1,973 | **1,963** |
| Cat 2 alias-mismatch | 268 | (unrecorded) | 291 |
| Stale religion-bleed | 24 | 0 | 0 |
| Date-bleed | 199 | 41 | 42 |
| Unknown edge types | 0 | 0 | 0 (lock holds) |
| Malformed lines | (unrecorded) | (unrecorded) | 25 |

Cat 2 increase (+23) reflects new node arrivals (more ground for slugs to slip on); not a regression.

---

## Chronology extraction (bonus, end-of-session)

After Step 6 closure committed, Matt asked "what's next?" and I surfaced the next-up items. He greenlit chronology extraction "now if you can if it's not too big."

Built `scripts/wiki-pass2-extract-chronology.py`. Walks 74 in-world year pages (1 AC - 300 AC), extracts internal links + 200-char surrounding context, filters (target must exist, not skip, not self-reference, not year-to-year nav), dedups per page. Output: `working/wiki-parsed/chronology-events.jsonl` with row shape `{year_page, year_value, year_era, target_page, target_slug, target_type, anchor_text, snippet}`.

**Result: 2,245 chronology events extracted.** 373 broken links (targets not in page-index — likely redirects).

By target type: 1,512 character.human, 275 place.location, 119 event.battle, 74 title, 50 organization.house, 33 event.war, 41 character.dragon, 12 object.artifact, 9 species, 6 concept.medical, etc.

Year coverage: 74 distinct years. Top dense years:
- 299 AC (305 events) — the Red Wedding year
- 300 AC (277 events) — main series climax
- 298 AC (109 events) — AGOT main events
- 130 AC (73), 133 AC (60), 135 AC (43) — Dance of the Dragons
- 281-283 AC (140 combined) — Robert's Rebellion

**Critical design decision:** NOT graph edges (yet). The locked 22-type vocabulary doesn't include OCCURRED_IN_YEAR. The v2 temporal-edges design (Session 26 TODO) plans structured `start_year` / `end_year` / `precision` per-edge fields rather than a dedicated edge type. This JSONL becomes input for that future backfill — `chronology-extractor` agent stub can consume this data when the v2 schema is ready.

---

## Three commits, all merged to main

1. **`896c5a3d` Path B promotion completion: 4 new entity types + 314 net nodes**
   - 1,351 files changed, 29,213 insertions, 2,752 deletions
   - Schema additions, parser changes, longtail extension, 130-stale-dir cleanup, dedicated-script reruns, stale-cleanup script (NEW)

2. **`e6e206fd` Step 6 closure: schema-drift audit + cleanups + WRITTEN_BY parser fix**
   - 14 files changed, 2,518 insertions, 1,747 deletions
   - Audit reports, _stage3-preview removal, song reclassification, parser tweak

3. **`d6362f74` Year-page chronology extraction + concept.culture canonical-home decision**
   - 3 files changed, 2,445 insertions, 3 deletions
   - Chronology extractor (NEW), 2,245 events JSONL, concept.culture comment formalization

---

## What this session learned

1. **Hypothesis-first investigation pays off.** The "836 no-cat unknowns are highest-risk misses" hypothesis was wrong (96.9% redirects). Pivoting to "with-cat unknowns" surfaced the productive work and uncovered the customs/materials/languages/medical schema gaps.

2. **Stage-1 vs Stage-3 (`v1` vs `v1-python`) distinction matters.** I conflated them mid-cleanup, panicked, and over-restored. The carve-out is specifically about Stage-1 AGENT prose (which Stage 4 will reprocess), NOT Stage-3 deterministic prose (which is regenerable from wiki HTML at any time). The cleanup script now has a permanent Stage-1 guard.

3. **Mid-flight regression detection saved the food classification.** Adding species patterns dropped object.food 69→40. Surfacing this to Matt got the right call (food precedes species in pattern order). The fix changed object.food to 73 (+4 net), and the 33 dual-tagged correctly routed.

4. **Subagent-based audits decouple cost from context.** The schema-drift-auditor running on opus produced a 7,619-node audit while my session context stayed clean. Pattern repeatable for any expensive read-only task.

5. **Architecture decisions shouldn't outpace data.** OCCURRED_IN_YEAR didn't get added to the locked vocabulary even though Matt approved chronology extraction; the v2 temporal-edges design (Session 26 TODO) already planned a structured-fields approach. JSONL output preserves the work without committing to a specific edge type prematurely.

6. **The graph is now ready for Stage 4.** Schema-drift clean. Cross-references index built (Session 26). Alias resolver built (Session 26). Chronology data extracted. The four agent prompts (prose-edge-classifier, entity-merge-resolver, disambiguation-resolver, chronology-extractor) are the remaining design work.

---

## Counts

| Metric | Session start | Session end | Δ |
|---|---|---|---|
| Total graph nodes | 7,248 | 7,563 | +315 |
| `unknown` page-index | 2,098 | 1,257 | -841 |
| `skip` page-index | 8,592 | 9,167 | +575 |
| Cat 1 orphan edges | 1,973 | 1,963 | -10 |
| Edge vocab violations | 0 | 0 | 0 (lock holds) |
| New entity types | 21 | 25 | +4 |
| New graph dirs | 14 | 18 | +4 |
| Schema-drift HIGH | (untested) | 0 | clean |

New types: `object.material`, `concept.language`, `concept.medical`, `concept.custom`. New dirs: `materials/`, `languages/`, `medical/`, `customs/`.

---

## What's next (in priority order)

1. **Stage 4 v1 — prose-edge-classifier** (the big one, mostly unblocked). Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` (created this session; detailed). AGOT-only Pass-1 dependency for contradiction sweep; full corpus for prose-edge discovery + cross-identity. Cost ~$50-100, 3-5 hrs wall-clock.

2. **Pass 1 mechanical extraction on remaining books** (in parallel with Stage 4 if desired). 271 chapters (ACOK + ASOS + AFFC + ADWD). Runs through `weirwood` pipeline in iTerm. Pre-requisite for chat UI.

3. **v2 temporal-edges design + backfill** — uses `working/wiki-parsed/chronology-events.jsonl` (NEW this session). Architecture decision pending: structured per-edge `start_year`/`end_year`/`precision` fields vs dedicated `OCCURRED_IN_YEAR` edge type.

4. **Stage 4 follow-on agents** — entity-merge-resolver, disambiguation-resolver, chronology-extractor (all stubs in `.claude/agents/`).

5. **Two-repo split + chat UI** (deferred until Pass 1 multi-book complete).
