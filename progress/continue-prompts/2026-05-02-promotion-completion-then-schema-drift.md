# Promotion Completion → Schema-Drift Audit

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-05-01 end of Session 28. All Session 28 work committed (verify with `git log --oneline -16` — top should be `1e258b71 Path B iteration 3: foods + trees`).

---

## Matt's framing for this session

> "wouldn't it be better to get this part done well? we missed several important nodes, red wedding, ashford tourney, etc."

Two intertwined goals:
1. **Get promotion done well** before running the expensive schema-drift audit. Several load-bearing entities slipped past Path B sub-tasks 1-6 — only got recovered in iteration 2 because Matt pushed back. Don't repeat that pattern.
2. **Run schema-drift audit on opus** (~$50, prior approval) once promotion stabilizes — but only after promotion is done well.

The "do it well" framing means: surface the missing-important-entities BEFORE running schema-drift, so the audit isn't critiquing an incomplete graph.

---

## What was done in Session 28 (the prerequisite)

`unknown` 12,434 (Session 28 start, 70.4%) → **2,118 (12.0%)**. Graph 5,008 → 7,248 (+2,240). Cat 1 orphan edges 2,955 → 1,973.

**Verified files:**
- All 7 promotion scripts at `scripts/wiki-pass2-tier3-pathb-*.py`
- `working/wiki-parsed/page-index.jsonl` (latest classification distribution; check with the inventory command below)
- `reference/architecture.md` — `object.food` row added; `species` description broadened to cover flora
- 5 new graph dirs: `texts/`, `theories/`, `concepts/`, `species/`, `foods/`

**Bootstrapped types/dirs:**
- `texts/`: 150 in-world books/songs/scrolls
- `theories/`: 45 fan theories (R+L=J, Azor Ahai, etc.)
- `concepts/`: 31 magic concepts
- `species/`: 38 (sentient races + trees including weirwood)
- `foods/`: 69 (foods + drinks)
- `event.tournament`: 35 nodes (Ashford Tourney, Tourney at Harrenhal, etc. — routed to `events/`)

**Hard constraints (still apply):**
- `sources/wiki/` is read-only. Outputs go to `working/wiki-parsed/` and `graph/`.
- Re-fetch rule: still default-NO. The 2026-04-30 categories backfill was a per-occasion exception. New gap → ask Matt FIRST.
- NEVER touch Stage-1 character nodes (`prompt_version: v1`) without explicit Stage-1 carve-out.
- Atomic-rename invariant for all writes to `graph/nodes/`.
- Slug-correctness check after every sub-task (`grep '^slug: .*\.node$' graph/nodes/**/*.node.md` should return 0).

---

## What's still in the 2,118 unknowns

Top categories on unknown pages (run the inventory command for current):

```
278  Feature quotes              [WIKI META — defer]
148  Did you know                [WIKI META — defer]
136  Terms                        [glossary — partial schema decision]
 95  Animals                      [SCHEMA DECISION — Matt deferred]
 74  Years                        [Tier 3 chronology-extractor]
 61  Feature articles             [WIKI META — defer]
 58  Food                         [done — empty after iter 3]
 46  Culture                      [investigate — may already be promoted]
 45  Theories                     [done — promoted as concept.theory]
 34  Plants                       [SCHEMA DECISION — Matt deferred]
 32  Birds                        [SCHEMA DECISION — Matt deferred]
 32  King's Landing               [TAG — relates pages, not type]
 32  House Targaryen              [TAG — relates pages, not type]
 28  Pages using hatnote template directly
 27  Occupations                  [investigate — title-like?]
 27  Gemstones                    [SCHEMA DECISION — material types?]
 26  Westeros                     [TAG]
 26  Halls                        [done — place.location]
 26  Languages                    [SCHEMA DECISION — concept.language?]
 25  Events                       [done — event.battle]
 22  Diseases                     [investigate]
 21  Faith of the Seven           [TAG]
 20  Trees                        [done — species]
 20  Deities                      [done — organization.religion]
 16  Drinks                       [done — object.food]
 16  Poisons                      [SCHEMA DECISION — concept.medical?]
 13  Metals                       [SCHEMA DECISION]
 11  Rocks                        [SCHEMA DECISION]
```

**Plus 836 pages with NO categories at all** — these are the highest-risk misses. Many are stubs but some are real entities the categorizer simply doesn't know about (Ashford Tourney was one — empty categories, but caught by `\btourney\b` page-name pattern).

---

## What this session needs to do

### Step 1 — Audit unknown pages for missed important entities (PRIORITY)

The Session 28 retro flagged this: Red Wedding, Ashford Tourney, Knight of the Laughing Tree all almost slipped past. Be more rigorous before declaring promotion "done":

**Run a focused audit:**
```bash
python3 -c "
import json
unknowns = []
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if r.get('entity_type_guess') == 'unknown':
            unknowns.append(r['page'])

cats_per_page = {}
with open('working/wiki-parsed/page-categories.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if r['page'] in set(unknowns):
            cats_per_page[r['page']] = r.get('categories', [])

# Pages with NO categories — highest risk for misses
no_cat_pages = sorted([p for p in unknowns if not cats_per_page.get(p, [])])
print(f'Pages with NO categories: {len(no_cat_pages)}')
# Print first 100 alphabetically — Matt can spot-check
for p in no_cat_pages[:100]:
    print(f'  {p}')
"
```

**Triage process:**
1. Read the 836 no-category pages. Spot-check 10-15 against the wiki to see what they actually are.
2. For any page that's clearly load-bearing (named character, named event, named place, named theory), add to `ENTITY_TYPE_OVERRIDES` in `scripts/wiki-infobox-parser.py`.
3. For any page-name pattern that catches multiple (e.g. `\btourney\b`, `\bfeast\b`?), add to `PAGE_NAME_TYPE_PATTERNS`.
4. Re-run parser, re-run affected promotion scripts.
5. Loop until the no-category bucket has been triaged.

### Step 2 — Schema decisions on punted categories

Before schema-drift audit, decide:

**Animals + Birds + Fish (~142 pages):**
- Option A: Add to `species/` with subtype `species.animal`. Broadens species dir again.
- Option B: New `creatures/` dir, type `creature.animal` etc. Splits flora (species/) from fauna (creatures/).
- Option C: Skip entirely. Most are real-world animals (boar, wolf, eagle) tagged for context, not narrative entities.

Recommend asking Matt before doing this — he said "we don't have to get into species right now" but if we want a complete graph for schema-drift, decide one way or the other.

**Plants (~34 pages):** mirror animals decision. Often overlap with Trees-already-promoted.

**Languages (~26):** new type `concept.language`? Or fold into existing `concepts/`?

**Gemstones / Metals / Rocks (~51 combined):** material types. New type `concept.material`? Or fold into `object.artifact` (named gemstones like Heart of Winter)?

**Poisons / Diseases (~38 combined):** new type `concept.medical`? Or `object.substance`?

**Occupations (~27):** title-like (blacksmith, septon, maester). Fold into `title`?

**RECOMMENDATION:** for v1, fold aggressively into existing types rather than adding more. Each new type is a new dir + architecture.md row + parser map + promotion script branch. Defer fine-grained taxonomy to a later polish phase.

### Step 3 — `Dragon` page reclassification

The `Dragon` species page is currently filtered via `GLOSSARY_SKIP_PAGES = {"Dragon"}` in `scripts/wiki-pass2-tier3-pathb-longtail.py`. It has categories `['Animals', 'Dragons', 'Magic', 'Transport', 'Valyria']` — `Magic` matches first → `concept.magic`. Wrong; Dragon is a species.

Fix: add ENTITY_TYPE_OVERRIDES `"Dragon": "species"`. Then re-run parser + longtail script; remove from GLOSSARY_SKIP_PAGES. Also check `Dragons (species)` and similar variants don't already exist.

### Step 4 — `\bwar\b` / `\bconquest\b` regex tightening

Session 28 logged these false positives: Lance (war galley), Conquest of Dorne (book), Engines of War, Brothel Queens, Coronation of X, Wedding of X, Years after Aegon's Conquest. Currently filtered via in-script `GLOSSARY_SKIP_PAGES` in events script.

Decide: tighten the regex (e.g., `\bwar\b` only at end of name, exclude common prefix patterns), OR document the in-script approach as canonical. Lean: document and move on; the in-script approach works.

### Step 5 — Run schema-drift audit (opus, ~$50)

After Steps 1-4 stabilize promotion:

```bash
# Use the schema-drift-auditor agent (already-written prompt at .claude/agents/schema-drift-auditor.md)
# Run on the FULL graph corpus (NOT a sample) — Matt approved the cost in Session 27.
```

Audit checks:
- `type:` strings against `architecture.md` Type Reference Table
- Edge-vocabulary violations (locked at 22 types in architecture.md)
- Frontmatter schema violations (required fields present, formats correct)
- Slug format violations
- Cite_ref format consistency
- Type-vs-target-dir mismatches (e.g., `type: place.location` in `graph/nodes/houses/`)

Output goes to `working/audits/schema-drift-{date}.md`. Sample-based audit ran clean in Session 27; full-corpus run is the sign-off.

### Step 6 — Final orphan-edge audit + commit

Run `python3 scripts/orphan-edges-audit.py 2026-05-02-pathb-final` and tally. Commit + update worklog.

---

## Recommended execution order

1. **Spot-check inventory** of unknowns (5-10 min)
2. **Step 1: 836 no-category pages** — biggest impact-per-minute. Triage in batches of 50-100.
3. **Step 3: Dragon reclassification** — quick win.
4. **Step 4: regex documentation** — quick decision.
5. **Step 2: schema decisions** — pause + ask Matt before doing.
6. **Step 5: schema-drift audit** — run after Steps 1-4 land.
7. **Step 6: final tally + commit** — wrap up.

---

## Hard constraints (carry-forward)

- **The wiki cache and `sources/wiki/` are read-only.** No writes. Outputs go to `working/wiki-parsed/` and `graph/`.
- **Re-fetch rule still default-NO.** Per-occasion exceptions only.
- **NEVER touch Stage-1 character nodes** (`prompt_version: v1`) without explicit Stage-1 carve-out. Their edge sections are still preserved verbatim. Stage 4 prose-edge-classifier handles their edge format.
- **NEVER modify the locked edge vocabulary** in `reference/architecture.md`. Procedure: architecture.md FIRST → parser FIELD_EDGE_MAP → re-run parser.
- **Atomic-rename invariant** for all writes to `graph/nodes/`.
- **Slug-correctness check** after every sub-task — `grep '^slug: .*\.node$' graph/nodes/**/*.node.md` should return 0.
- **NO SOURCE TEXTS COMMITTED** — `sources/raw/` and `sources/chapters/` are gitignored.
- **`--plan` sample-check before `--apply`.** Session 28's chapter-page disaster (338 false positives) would have been caught in 30 seconds. Look at actual page names.

---

## Don'ts (process)

- **Don't run `/endsession` without explicit permission.** Historically violated multiple times.
- **Don't auto-launch promotion runs without confirming with Matt.** Each batch (Step 1 above) gets confirmed separately.
- **Don't promote variant duplicates as separate nodes.** Pass B precedent: `andal/andals`, `dornish/dornishmen/dornishman`, `lhazareen/lhazarene` were promoted then merged.
- **Don't extend `CATEGORY_TYPE_MAP` aggressively without checking what other types it might catch.** Session 28's `\bwar\b` over-match was the canonical failure.
- **Don't run the schema-drift audit (opus, $50) until promotion stabilizes.** Step 5 is the LAST step.

---

## Quick-reference investigation commands

```bash
# Current classification distribution
python3 -c "
import json, collections
d = collections.Counter()
total = 0
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        r = json.loads(line)
        d[r.get('entity_type_guess')] += 1
        total += 1
print(f'Total: {total}')
for k, v in d.most_common():
    print(f'  {k:30s} {v:>6}  ({100*v/total:5.1f}%)')
"

# Categories on unknown pages
python3 -c "
import json, collections
unknowns = set()
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if r.get('entity_type_guess') == 'unknown':
            unknowns.add(r['page'])
cat_counter = collections.Counter()
with open('working/wiki-parsed/page-categories.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if r['page'] in unknowns:
            for c in r.get('categories', []):
                cat_counter[c] += 1
for c, n in cat_counter.most_common(50):
    print(f'  {n:>5}  {c}')
"

# Pages classified type X not in graph yet
python3 -c "
import json, re, pathlib
def s(n):
    n = re.sub(r\"['\\\",]\", '', n.lower())
    n = re.sub(r'[ _]+', '-', n)
    n = re.sub(r'[^a-z0-9-]', '-', n)
    return re.sub(r'-+', '-', n).strip('-')
have = {f.name[:-len('.node.md')] for d in pathlib.Path('graph/nodes').iterdir() if d.is_dir() and not d.name.startswith('_') for f in d.glob('*.node.md')}
TARGET = 'object.text'  # change as needed
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if r.get('entity_type_guess') == TARGET and s(r['page']) not in have:
            print(s(r['page']), '->', r['page'])
" | head -30

# Run orphan-edges audit
python3 scripts/orphan-edges-audit.py 2026-05-02-WIP

# Spot-check a node
python3 scripts/graph-query.py <slug>

# Slug-regression check
grep -r '^slug: .*\.node$' graph/nodes/ | head
```

---

## Reference

- Session 28 detail: `working/session-details/session-028.md`
- Pipeline runbook: `working/runbooks/wiki-pass2-pipeline.md`
- Architecture (Type Reference + edge vocabulary): `reference/architecture.md`
- Parser: `scripts/wiki-infobox-parser.py` (CATEGORY_TYPE_MAP, ENTITY_TYPE_OVERRIDES, PAGE_NAME_TYPE_PATTERNS)
- 7 promotion scripts: `scripts/wiki-pass2-tier3-pathb-*.py` (template patterns differ — texts/artifacts use single DEST_DIR; orgs/longtail use TYPE_TO_DIR per-type routing)
- Stage 4 (separate continue prompt, do not start until this one finishes): `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md`
