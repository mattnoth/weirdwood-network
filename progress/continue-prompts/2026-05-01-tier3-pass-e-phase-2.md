# Tier 3 Pass E Phase 2 — Completeness on remaining residuals

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-04-30 end of Session 27. All Session 27 work committed (commits `5e25359` through `7ffeb34`). Working tree should be clean except for 2 typo'd debris files (`scratc`, `wiki-logs-`) — leave them.

---

## CRITICAL FIRST STEP — Books + Named Weapons + WRITTEN_BY edge gap

The single highest-priority unblocked work for Phase 2 is filling the `graph/nodes/artifacts/` directory and unlocking the WRITTEN_BY edge class. Right now:

- **`graph/nodes/artifacts/` contains exactly 1 node** (`iron-throne.node.md`).
- **0 WRITTEN_BY edges in the entire graph** despite WRITTEN_BY being in the locked vocabulary.
- **15+ named valyrian steel swords are MISSING** from the graph (Longclaw, Blackfyre, Ice, Heartsbane, Dawn, Oathkeeper, Widow's Wail, Lady Forlorn, Dark Sister, Red Rain, Nightfall, Lamentation, Orphan-Maker, Brightroar, Needle, etc.).
- **All major in-world books are MISSING** (Fire and Blood, The Seven-Pointed Star, A World of Ice and Fire, The Princess and the Queen, The Rogue Prince, The Dance of the Dragons, The Lineages and Histories, The Hedge Knight, The Sworn Sword, The Mystery Knight, etc.).

**Verified state (2026-04-30 investigation):**

| Page name | In wiki cache? | `entity_type_guess` | `has_infobox` |
|---|---|---|---|
| `Longclaw` | ✅ 26 KB | `unknown` | False |
| `Blackfyre` | ✅ 47 KB | `unknown` | False |
| `Ice`, `Dawn`, `Oathkeeper`, ... | ✅ all in cache | `unknown` | False |
| `Fire and Blood` | ✅ 1 KB | `unknown` | False |
| `The Seven-Pointed Star` | ✅ 34 KB | `unknown` | False |
| `A World of Ice and Fire` | ✅ 19 KB | `unknown` | False |

**Root cause:** the Playwright scraper got everything (whole AWOIAF wiki cached at `sources/wiki/_raw/`). The failure is in `wiki-infobox-parser.py`'s classifier — pages without a parser-recognized infobox signature classify as `unknown` and get triage-dropped. The wiki uses templates for swords/books that the parser's infobox-detection doesn't recognize.

I checked Longclaw's HTML directly: there's literally NO `class="infobox"` div in it. So extending the infobox detector won't help — these pages are prose-only with no structured infobox. The fix is name-pattern overrides, mirroring the Session 27 `Iron_Throne` override.

**Big-picture context:** 70.4% of all wiki pages (12,434 of 17,657) classify as `unknown`. Most are appropriately unknown (list pages, appendices, glossary stubs). But hidden inside that 70% are real entities like swords, books, individual gods, and song titles. The Tier 3 Passes A-D promoted what we could find via existing edge-target signals; this Phase 2 sub-task 1 reaches into the unknown bucket for the high-value categories that orphan-edges audits don't surface (because those entities aren't yet edge targets — once they're nodes, edges to them will appear naturally on next re-emission).

---

## Where we are at session start

The graph is at **5,495 nodes** (verify with `find graph/nodes -name '*.node.md' | wc -l` — adjust if Option C numbers shifted). Cat 1 orphan edges are at **2,955** (down from 7,784 pre-Tier-3, 62% reduction). Ran Tier 3 Passes A-D + Pass E Phase 1 + Option C this session.

Remaining 2,955 Cat 1 edges across 1,174 unique missing-target slugs split into:
- Locations / specific castles / towns / geographic features not yet promoted
- Smaller factions, mercenary companies, criminal organizations
- Events (battles, plots, councils) beyond Tier 1 coverage
- The books + weapons + artifacts gap above
- "Concepts" — Dance-of-the-Dragons faction names (`blacks`, `greens`), governance terms (`small-council`, `great-council`, `kingsmoot`, `tourney`, etc.) — currently flagged as DEFER per `working/todos.md`

---

## What to read first (in order)

1. **`worklog.md`** — current state checklist + last session entry; Session 27 summary.
2. **`working/audits/orphan-edges-2026-05-01.md`** — most recent audit; residual breakdown.
3. **`working/audits/orphan-edges-2026-05-01-cat1-full.tsv`** — every dangling edge as a row; filter by `edge_type` for sub-task targeting.
4. **`working/tier3-promotion-plan.md`** — original Tier 3 plan.
5. **`reference/architecture.md`** — TYPE_DIR_MAP + Wiki Infobox Fields → Edge Type Mapping (the locked vocabulary).
6. **Completed Tier 3 pass scripts** (these are your patterns to mirror):
   - `scripts/wiki-pass2-tier3-pass-a-titles.py` — most direct precedent for an override-driven entity-type promotion.
   - `scripts/wiki-pass2-tier3-pass-{b-cultures,c-religions,d-characters}.py` — variants.
   - `scripts/wiki-pass2-pass-e-phase1.py` — variant overrides + targeted re-emission.
7. **`scripts/graph-query.py`** — read-only investigation CLI; use it to spot-check any node.

---

## Phase 2 has 4 sub-tasks

### Sub-task 1a — Books / in-world texts pass [CRITICAL — DO FIRST]

**Goal:** populate `graph/nodes/artifacts/` (or new `graph/nodes/texts/` directory if you decide to split out text type — see decision below) with all in-world books and texts. Unlock WRITTEN_BY edges from Maester/Septon characters.

**Confirmed-present in wiki cache:**
```
Fire and Blood
The Seven-Pointed Star
A World of Ice and Fire
The Princess and the Queen
The Rogue Prince
The Dance of the Dragons
The Lineages and Histories of the Great Houses of the Seven Kingdoms
The Hedge Knight
The Sworn Sword
The Mystery Knight
Tales of Dunk and Egg
```
Plus discover more by grepping `working/wiki-parsed/page-index.jsonl` for entries where `cite_ref_books` is populated and `entity_type_guess: unknown`. Also check Septon Barth's works, Archmaester Gyldayn's chronicles, and the existing `battle-of-the-blackwater-song` in `_unclassified/`.

**Type decision needed at start:** `object.text` is in TYPE_DIR_MAP but maps to where? Check `architecture.md` and `wiki-pass2-promote.py`'s TYPE_DIR_MAP. If it routes to `artifacts/`, fine — books land alongside swords. If it routes to a separate `texts/` dir, create that dir and update the promote script. Lean toward `artifacts/` for v1 simplicity.

**Approach:**
1. Add `ENTITY_TYPE_OVERRIDES` entries for confirmed book pages → `object.text`.
2. Re-run `scripts/wiki-infobox-parser.py` end-to-end to regenerate `infobox-data.jsonl`.
3. Build one-off bucket at `working/wiki-pass2/tier3-books/`.
4. Run Stage 3 pipeline (mirror `wiki-pass2-tier3-pass-a-titles.py`).
5. After promotion, re-run `wiki-infobox-parser.py` on Maester/Septon character pages — the WRITTEN_BY edges from their infobox `Written by` field should now have resolvable target slugs. May need a targeted re-emission of those character nodes to land the new edges.

**Expected outcome:** 30-50 book nodes; first WRITTEN_BY edges in the graph; previously-invisible literary network surfaces.

### Sub-task 1b — Named weapons / artifacts pass [CRITICAL — DO SECOND]

**Goal:** promote named-sword nodes; resolve the 3 existing orphan WIELDS edges (`jon → Longclaw`, `arya → Needle`, `visenya → Dark Sister`); lay foundation for Stage 4 prose-edge-classifier to discover more WIELDS edges.

**Confirmed-present in wiki cache (verified 2026-04-30):**
```
Longclaw, Blackfyre, Ice, Heartsbane, Dawn, Oathkeeper, Widow's_Wail,
Lady_Forlorn, Dark_Sister, Red_Rain, Nightfall, Lamentation, Orphan-Maker,
Brightroar, Needle
```
Discover more by greping `page-index.jsonl` for `Vigilance, Hearteater, Truth, Lightbringer, Horn of Joramun`, plus any `(sword)` / `(weapon)` disambiguator pages.

**Approach:**
1. Add `ENTITY_TYPE_OVERRIDES` entries → `object.artifact` (already in TYPE_DIR_MAP, routes to `artifacts/`).
2. Same Stage 3 pipeline pattern.
3. After promotion, the 3 existing WIELDS edges resolve cleanly (jon-snow's Longclaw edge currently goes to `[ORPHAN]`; should become `[OK]`).

**WIELDS-from-infobox investigation (Part B):** spot-check 3-5 character infobox HTMLs (Targaryens with Dark Sister/Blackfyre, Stark with Ice, Tarly with Heartsbane) to see if any have a structured `Weapon` / `Wielder` infobox field. If yes: add `Weapon → WIELDS` to `FIELD_EDGE_MAP` per the vocabulary-lock procedure (architecture.md FIRST, then parser, then re-emit affected character nodes). If no: WIELDS is prose-only signal — Stage 4 prose-edge-classifier territory.

**Expected outcome:** 15-30 weapon nodes; 3 orphan WIELDS edges resolve; structured WIELDS field potentially added or formally deferred to Stage 4.

### Sub-task 2 — Locations / events / factions completeness

Filter `orphan-edges-2026-05-01-cat1-full.tsv` for non-character / non-title / non-religion / non-book / non-weapon edge types + target slugs that have wiki pages. Edge types to focus on: `REGION_OF`, `OVERLORD_OF`, `RULES`, `SEAT_OF`, `BORN_AT`, `DIED_AT`, `BURIED_AT`. Mirror Pass A pattern.

Expected scope: ~400-600 nodes. Pages with `unknown` entity-type that are clearly geographical (look for `place` / `region` / `castle` / `town` keywords in page name) → `place.location`.

### Sub-task 3 — Concept page decision

`small-council`, `great-council`, `kingsmoot`, `tourney`, etc. — glossary-style concept pages. Per `working/todos.md` Tier 3 todo, the recommendation was **option (iii) defer**. After 1-2 land, decide: defer permanently, promote with a `concept` type, or treat as `event`?

Lean: defer unless Stage 4 surfaces specific need.

### Sub-task 4 — Final verification

After 1-3 land:
- Re-run `python3 scripts/orphan-edges-audit.py 2026-05-XX`
- Re-run `python3 scripts/wiki-pass2-duplicate-detector.py` for any new variant duplicates
- Run `schema-drift-auditor` against the FULL corpus (we only ran samples this session — full sweep with opus is ~$50)
- Spot-check via `graph-query.py` on representative new nodes (e.g., `longclaw`, `fire-and-blood`, `blackfyre`)

**Acceptance criteria** from `tier3-promotion-plan.md`: Cat 1 drops to <500 edges / <100 slugs corpus-wide.

---

## Things explicitly DEFERRED (NOT in Phase 2 scope)

- **Stage-1 character cite-format divergence** (978 verbose-cite occurrences in 596 v1 character nodes) — handled by Stage 4 prose-edge-classifier; Option C addressed prose only.
- **42 BORN_AT/DIED_AT date-bleed remaining** — parser-floor cases (wiki has only dates, no location). Resolves when year-period nodes exist or via parser suppression in a future session.
- **Cultures-vs-factions directory mix** — many cultures live in `graph/nodes/factions/` (typed `organization.faction`) per Tier 2 convention. Future taxonomy split (proper `culture` type with own dir) is separate.
- **Year/era nodes** — `131 AC` etc. are referenced in Heir/Born/Died fields. Tier 3 plan calls these "Tier 3 chronology extraction"; they need their own dedicated pass with the `chronology-extractor` agent.
- **Pass 1 catch-up on books ACOK/ASOS/AFFC/ADWD** — 271 chapters of mechanical extraction pending. This unblocks the chat UI but is orthogonal to graph completeness. Track via `progress/pass1-*.md`.
- **Stage 4 prose-edge-classifier build** — designed but no agent run yet. Will discover WIELDS, SIBLING_OF, perception edges from prose. Continue prompt at `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md`.

---

## Hard constraints

- **The wiki cache is read-only.** Never re-fetch. No HTTP calls to awoiaf.westeros.org. Playwright scraper archived. Verified 2026-04-30: cache is complete; failures are in the parser, not in scraping.
- **70% of pages classify as `unknown`** — this is mostly correct (list pages, appendices). Don't try to bulk-promote everything. Surgical overrides only on confirmed-real entity categories.
- **NEVER touch Stage-1 character nodes** (`prompt_version: v1` in `graph/nodes/characters/`) unless their carve-out is explicitly documented as resolved in worklog. Option C did prose-only; their edge sections are still preserved verbatim. Stage 4 will handle their edge format.
- **NEVER modify the locked edge vocabulary** in `reference/architecture.md`. Procedure for adding a new edge type: architecture.md FIRST → parser FIELD_EDGE_MAP → re-run parser. No script invents edges out-of-band.
- **NEVER introduce new entity types** without first updating `reference/architecture.md`'s TYPE_DIR_MAP. The valid types are: `character.human`, `character.dragon`, `character.direwolf`, `organization.house`, `organization.faction`, `organization.religion`, `religion`, `place.location`, `place.region`, `event.war`, `object.artifact`, `object.text`, `title`. (Plus `concept.*` is defined but not actively used.)
- **Atomic-rename invariant** for all writes to `graph/nodes/`. Never write directly to a final-node path; build in a temp/tmp path and rename.
- **Slug-correctness check** after every sub-task — `grep '^slug: .*\.node$' graph/nodes/**/*.node.md` should return 0. (Session 27 introduced + fixed a `Path.stem` bug across 1,120 nodes; the fix is in `wiki-pass2-repromote-targeted-2.py:422,492` — `stem.removesuffix(".node")`. Audit any new re-promote scripts for the same bug.)
- **NO SOURCE TEXTS COMMITTED** — `sources/raw/` and `sources/chapters/` are gitignored; never override.

---

## Don'ts (process)

- **Don't run `/endsession` without explicit permission.** This rule has been violated multiple times historically.
- **Don't auto-launch agents without confirming with Matt.** Specifically: don't launch a re-emission run that will modify hundreds of nodes without first explaining scope, cost, and trade-offs.
- **Don't try to rebuild `alias-resolver.json` without `--apply`.** Default is dry-run.
- **Don't introduce parser changes without re-running `wiki-infobox-parser.py` end-to-end** + verifying `infobox-data.jsonl` regenerated. Parser changes that aren't applied to the data are silent failures.
- **Don't promote variant duplicates.** Pass B accidentally promoted `andal/andals/dornish/dornishmen/dornishman/lhazareen/lhazarene/lysene/lyseni/stormlander/stormlanders` as separate nodes; Phase 1 cleaned this up. Avoid recurrence — when a wiki has multiple page-name forms, pick one canonical and add the others as aliases.
- **Don't run audits on the FULL corpus with opus when sample audits suffice.** Schema-drift on full corpus is ~$50; samples are ~$5-7 and surface most categories.

---

## Recommended order

1. **Verify session-startup state.** `git log --oneline -10` should show this session's 7 commits. `git status` should show only typo'd debris (`scratc`, `wiki-logs-`). If working tree is dirty, investigate before proceeding.
2. **Sub-task 1a — Books pass** (highest novelty, unlocks WRITTEN_BY signal that's currently 0 edges). One commit.
3. **Sub-task 1b — Named weapons pass** (resolves 3 orphan WIELDS edges, populates `artifacts/` dir). One commit.
4. **Sub-task 2 — Locations / events / factions completeness** (largest scope, most mechanical). One commit.
5. **Sub-task 3 — Concept-page decision** (likely just confirm defer; documentation-only).
6. **Sub-task 4 — Full audits + commit** (re-run all audits; commit if any cleanup needed; otherwise just an audit-output commit).

Each sub-task = its own commit. Total expected: 4-5 commits, ~500-700 new nodes, Cat 1 drop to <500 edges meeting acceptance criteria.

---

## Quick-reference investigation commands

```bash
# Count current state
find graph/nodes -name '*.node.md' | wc -l

# Verify orphan edges still match audit
python3 scripts/orphan-edges-audit.py 2026-05-XX

# Inspect a single node end-to-end
python3 scripts/graph-query.py <slug>

# Find unknown-typed pages with books-like signals
python3 -c "
import json
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        rec = json.loads(line)
        if rec.get('entity_type_guess') == 'unknown' and rec.get('cite_ref_books'):
            print(f\"{rec['page']}: books={rec['cite_ref_books']}\")
" | head -30

# Find unknown high-byte pages (likely real entities not stubs)
python3 -c "
import json
unks = []
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        rec = json.loads(line)
        if rec.get('entity_type_guess') == 'unknown':
            unks.append((rec['byte_size'], rec['page']))
unks.sort(reverse=True)
for sz, name in unks[:40]:
    print(f'{sz:>7d}  {name}')
"

# Spot-grep for a specific edge type
grep -rh '^- WRITTEN_BY' graph/nodes/ 2>/dev/null | head
```

---

## Session 27 commit history (for reference)

```
7ffeb34 Option C: Stage-1 character prose-only re-emission (544 nodes)
7b723f8 Pass E Phase 1: surgical debt cleanup (4 tasks, 425 nodes)
3414635 Tier 3 Pass D: backfill 184 character nodes
3f5113b Tier 3 Pass C: 16 religion nodes + 6 aliases
dff149f Tier 3 Pass B: 52 culture nodes
54ce745 Tier 3 Pass A: 470 title nodes
5e25359 Wiki Pass 2 Stage 3 pipeline + Stage 3c audit cleanup + 27-agent fleet
```

If any of these are missing from the local git log, the session didn't end cleanly — investigate before proceeding.
