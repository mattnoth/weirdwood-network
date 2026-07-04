# Hygiene proposal — G18 data-hygiene classes (S190, side-step H)

**Status: PROPOSAL ONLY. Nothing under `graph/` has been touched.** Every number below was
re-derived this session directly against the live graph (8,727 files under `graph/nodes/**`,
23,099 lines in `graph/edges/edges.jsonl`), not inherited from the S189 census. Where my count
disagrees with the census, both numbers are shown and the disagreement is called out — I did not
force a match.

Read first: `working/query-layer/design.md` §2c G18 and the "gated side-step H" card (§5).

Vocabulary used below per project convention: this is one **Track** deliverable (side-step H);
each fix below is a **step**; **Tier** below always means the 1–5 confidence rating, never a
grade of this work.

---

## Class 1 — YAML-broken node files

**Census claim:** 5 files, malformed doubled-quote aliases.
**Verified:** ✅ **Exact match.** Ran a full YAML-parse sweep over all 8,727 `.node.md` files
(split on `---` frontmatter delimiters, `yaml.safe_load` each). Exactly 5 fail, all in
`graph/nodes/characters/`, all on the `aliases:` line, all the same bug shape (a stray doubled
`"` inside a quoted list item breaks YAML flow-sequence parsing):

| File | Line 5 (broken) |
|---|---|
| `graph/nodes/characters/blood-butcher.node.md` | `aliases: [""Blood""]` |
| `graph/nodes/characters/cheese-ratcatcher.node.md` | `aliases: [""Cheese""]` |
| `graph/nodes/characters/jacaerys-velaryon.node.md` | `aliases: ["Jace", "Jacaerys "Strong""]` |
| `graph/nodes/characters/shepherd-reborn.node.md` | `aliases: ["The Shepherd reborn (I)", "The "reborn" Shepherd"]` |
| `graph/nodes/characters/tyrion-tanner.node.md` | `aliases: [""of the hundred fathers""]` |

These are invisible to every current parser (graph-query's pyyaml+regex fallback, the resolver,
build-chat-export) because each independently swallows the exception and treats the node as
alias-less — so today it's silent data loss, not a crash. A strict engine (G11's contract-first
plan) would need to decide: hard-fail on bad YAML, or degrade gracefully. Either way the
underlying quoting bug should just be fixed.

**Root cause:** the alias value itself contains an unescaped `"` (a nested epithet/nickname:
`"Blood"`, `"Cheese"`, `Strong"` as part of a name, `"reborn"`, `"of the hundred fathers"`).
Whatever wrote these frontmatter blocks wrapped the alias in `"..."` without escaping the inner
quote marks.

**Recommended action:** repair quoting in place — re-serialize each `aliases:` line so the
inner quote marks are properly escaped (`\"`) or the outer wrapper uses single quotes. This is a
pure syntax fix; the alias *content* (the words themselves) is unchanged, so it doesn't cross
into "alias content changes" (out of scope, see Not Proposed below).

**Alternative considered:** drop the offending inner quote marks entireley (e.g. `"Blood"` →
`Blood`) instead of escaping. Rejected as the recommendation — the inner quotes are meaningful
(they mark the nickname/epithet as a quoted nickname in-universe, e.g. Blood *is* an epithet).
Escaping preserves that signal; stripping loses it.

**Risk:** essentially none — 5 files, mechanical, verifiable by re-running the same YAML-parse
sweep afterward (should return 0 broken).

**Apply mechanism (deterministic Python, per Python-before-Agent):**
```python
# scripts/fix-yaml-broken-aliases.py (sketch)
import re, pathlib

FIXES = {
    "graph/nodes/characters/blood-butcher.node.md":
        ('aliases: [""Blood""]', 'aliases: ["\\"Blood\\""]'),
    "graph/nodes/characters/cheese-ratcatcher.node.md":
        ('aliases: [""Cheese""]', 'aliases: ["\\"Cheese\\""]'),
    "graph/nodes/characters/jacaerys-velaryon.node.md":
        ('aliases: ["Jace", "Jacaerys "Strong""]',
         'aliases: ["Jace", "Jacaerys \\"Strong\\""]'),
    "graph/nodes/characters/shepherd-reborn.node.md":
        ('aliases: ["The Shepherd reborn (I)", "The "reborn" Shepherd"]',
         'aliases: ["The Shepherd reborn (I)", "The \\"reborn\\" Shepherd"]'),
    "graph/nodes/characters/tyrion-tanner.node.md":
        ('aliases: [""of the hundred fathers""]',
         'aliases: ["\\"of the hundred fathers\\""]'),
}
for path, (old, new) in FIXES.items():
    p = pathlib.Path(path)
    text = p.read_text(encoding="utf-8")
    assert old in text, f"pattern not found in {path}"
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
# then re-run the YAML-parse sweep to confirm 0 broken files remain.
```
5 files, one line changed each. Verify-after: re-run the parse sweep (`scan_yaml_broken.py`
logic above), expect 0 failures.

- [ ] **Matt approves Class 1 (YAML repair)**

---

## Class 2 — dangling-endpoint edges (phantom slugs)

**Census claim:** 91 edges with dangling endpoints, 67 distinct phantom slugs.
**Verified:** ⚠️ **Does not reproduce exactly.** Built the full node-slug set (8,720 distinct
slugs from filenames; cross-checked against frontmatter `slug:` fields, no difference) and
checked every edge's `source_slug`/`target_slug` in `edges.jsonl` (23,099 rows, including the 40
rows that lack a `decision` field but have the same slug shape) against it:

- **My count: 67 edges have ≥1 dangling endpoint; 62 distinct phantom slugs.**
- **Census count: 91 edges / 67 distinct phantom slugs.**

I could not find a bundling/dedup/alias-resolution rule that bridges 67→91 edges or 62→67 slugs
(tried: filename-slug-only, frontmatter-slug-only, union of both — all three give the same
67/62). The qualitative characterization holds regardless of the exact count: the phantom slugs
are overwhelmingly **Pass-1 collective-noun / unnamed-entity references**, not real broken
links — e.g. `gold-cloaks`, `caged-northmen`, `mountain-clansmen`, `unnamed-soldier`,
`unnamed-toddler`, `prisoner-old-man`, `unknown-rose-banner-defender-1/2/3`, `sleeping-guards`,
`vision-bearded-man` (a House-of-the-Undying vision figure), `yunkai-slavers`, and named-but-
unminted bit-players like `kyle`, `raymund`, `alynne`, `ser-osfryd`, `lord-brax`, `lord-locke`,
`lord-stout`. A handful (`big-walder-frey` ×2, `little-walder-frey` ×2, `harrenhal-dungeon-
guards` ×2, `freedmen` ×2, `wat-the-blue-bard` ×2) account for more than one dangling edge each.
Full list of all 62 phantom slugs with edge-counts is in the scan output (reproducible via the
script below).

**Recommendation (matches design's stance, and I agree with it):** **KEEP the edges. Do not
delete.** These are Pass-1 book-derived relationship data — deleting them would be a real data
loss for a cosmetic完整ness gain. Instead, have the query engine's `health`/`census` report
surface them explicitly (this is already on the step-9/`report.py` roadmap per design.md line
364). A strict engine should *know* about these 67 dangling targets and either (a) render them
as "referenced but not yet a node" placeholders, or (b) silently degrade the edge to a dead end
with a `health` warning — either way, visibly, not by crashing.

**Alternative considered:** mint stub nodes for the 62 phantom slugs so every edge resolves.
Not recommended for this pass — most of these are exactly the deliberately-unminted long-tail
Pass-1 references (unnamed extras, collective nouns) that the project has consistently NOT
promoted to nodes (see Pass 1/Pass 2 asymmetry — Pass 1 captures presence, node-minting is a
separate promoted decision). Minting them now would be a scope-creep data decision riding on a
hygiene pass. If Matt wants any specific ones minted (e.g. `gold-cloaks` as a collective node),
that's a separate proposal.

**Risk:** none from keeping as-is; the only risk is silent engine behavior if `health` isn't
wired up before the engine ships tolerance-free code that assumes every edge resolves.

**Apply mechanism:** no graph mutation. The "fix" here is a `graph/query` code change (health
reporting), not a data change — falls under the D-A carve-out (code under `graph/query/` is not
gated by the no-graph-mutation rule) but is flagged here since it's the direct disposition of a
G18 finding. Script used to produce the verified numbers (re-runnable, read-only):
```python
# scan_dangling.py (read-only, already run this session)
import json, glob, os
from collections import Counter
node_slugs = {os.path.basename(f)[:-len(".node.md")]
              for f in glob.glob("graph/nodes/**/*.node.md", recursive=True)}
edges = [json.loads(l) for l in open("graph/edges/edges.jsonl") if l.strip()]
phantom = Counter()
dangling = 0
for e in edges:
    src, tgt = e.get("source_slug"), e.get("target_slug")
    bad = src not in node_slugs or tgt not in node_slugs
    if bad:
        dangling += 1
        if src not in node_slugs: phantom[src] += 1
        if tgt not in node_slugs: phantom[tgt] += 1
print(dangling, len(phantom))
```

- [ ] **Matt approves Class 2 (keep + report via `health`, no deletion, no stub-minting)**

---

## Class 3 — duplicate edge rows

**Census claim:** 28 exact-duplicate edge rows.
**Verified:** ❌ **Does not reproduce under any definition I tried.** Results:

| Dedup key tried | Duplicate groups found | Extra rows |
|---|---|---|
| Full row, byte-identical | 0 | 0 |
| Full row minus `produced_at` + `run_id` (volatile run-identity fields) | 0 | 0 |
| `(source, target, edge_type, evidence_ref)` | 11 | 11 |
| `(source, target, edge_type, evidence_chapter, evidence_quote)` | 7 | 7 (inspected — all 7 are *not* true duplicates; see below) |

The 7 rows on the loosest key are same-pair `GUEST_OF` edges that happen to quote the same book
passage to substantiate two *different* hospitality beats (e.g. `robb-stark`→`walder-frey`
`GUEST_OF` appears twice: once for "Ser Stevron conveys the invitation," once for "Lord Walder
grants crossing" — same chapter, same quoted line, different `evidence_details`/
`evidence_event`). These are legitimate distinct edges, not accidental duplication — the
`dup_count` field (present on 3,795 edges, values 0–25) is the project's existing, intentional
corroboration counter, not a hygiene defect; it counts how many independent Pass-1 mentions
back an edge, and is a feature, not something to dedup away.

**I cannot verify the "28 exact-duplicate rows" claim and could not reconstruct a key that
produces it.** Recommend re-deriving this number before acting on it — it may have been computed
against a different edges snapshot (there are `_regrounding/` pre-mutation snapshots that could
have had transient duplicates a later mutation session cleaned up), or the original census used
a key/script that wasn't preserved. I checked `working/query-layer/` for a residual census
script and found none — the S189 census sweep was run inline in that session and not saved.

**Recommendation:** **no action** on this class until the claim re-verifies. If Matt wants,
a follow-up could diff `edges.jsonl` against the oldest `_regrounding/` snapshot to see if 28
duplicates existed at some point and were already cleaned — but that's forensics, not a live
hygiene fix, and shouldn't block the rest of side-step H.

**Risk of inaction:** none identified — I found 0 true exact-duplicate rows live in the graph
today.

- [ ] **Matt approves Class 3 (no action — claim unverified; optionally spawn a follow-up to
      audit `_regrounding/` history if the provenance matters)**

---

## Class 4 — empty `aliases: []` stubs

**Census claim:** 6,923 nodes with empty `aliases: []`.
**Verified:** ✅ **Confirmed, within rounding.** Literal `aliases: []` lines appear in **7,129**
node files graph-wide. Excluding the 208 files under `graph/nodes/_conflicts/` (unresolved
Pass-2 conflict copies with junk timestamped filenames — arguably not "real" nodes for this
census) gives **6,921** — 2 off the census's 6,923, almost certainly explained by graph growth
between the S189 census and now (new nodes minted this week) rather than a methodology
difference. Breakdown by category:

| Category | Empty-alias count |
|---|---|
| characters | 2,913 |
| locations | 1,073 |
| houses | 553 |
| titles | 527 |
| events | 354 |
| chapters | 344 |
| artifacts | 278 |
| _conflicts (excluded above) | 208 |
| species | 177 |
| factions | 172 |
| texts | 156 |
| foods | 72 |
| religions | 60 |
| materials | 58 |
| theories | 45 |
| concepts | 42 |
| customs | 36 |
| medical | 34 |
| languages | 25 |
| prophecies | 2 |

8,530 of 8,727 total node files carry an `aliases` field at all; 83.6% of those are empty
stubs. This is exactly the "84% of has-aliases is noise" figure design.md quotes.

**Recommendation: leave as-is (my call, per the brief).** Weighing it:
- **Cost of touching:** 6,921 file writes = 6,921 git-blame-churn lines across almost every
  category, for **zero functional change** — an empty `aliases: []` and an absent `aliases:`
  key behave identically to every parser I found (pyyaml gives `None`/`[]` either way; the
  resolver treats both as "no aliases to index"). Removing the key doesn't unlock any new
  matching behavior.
- **Cost of leaving:** cosmetic only — a `grep -c 'aliases: \[\]'` looks alarming, and any
  future stats like "X% of nodes have aliases" will over-report unless whoever runs that stat
  already knows to filter empty arrays (which G18's own census entry already does correctly).
- **A cheaper alternative if the cosmetic noise really bothers Matt:** don't touch 6,921
  existing files; just make future node-minting scripts omit the `aliases:` key entirely when
  there are no aliases, and treat "field absent" as canonical-empty going forward. That stops
  the noise from growing without a mass rewrite of history.

**Recommended action: NO bulk edit.** If Matt disagrees and wants it cleaned, mechanism would
be a one-line-per-file removal:
```python
# scripts/strip-empty-aliases.py (sketch, NOT run)
import glob, pathlib
for f in glob.glob("graph/nodes/**/*.node.md", recursive=True):
    p = pathlib.Path(f)
    text = p.read_text(encoding="utf-8")
    new = text.replace("aliases: []\n", "", 1)  # only first frontmatter occurrence
    if new != text:
        p.write_text(new, encoding="utf-8")
```
(This needs a frontmatter-boundary guard so it never touches an `aliases: []` line that might
appear in prose — none do today, but the guard should exist before running.)

- [ ] **Matt approves Class 4a: leave empty `aliases: []` stubs as-is (recommended)**
- [ ] **Matt approves Class 4b (alternative): bulk-strip the key from all ~6,921 files**
- [ ] **Matt approves Class 4c (alternative): stop emitting the key in future node-minting
      scripts only; no retroactive change**

---

## Class 5 — cross-category slug collisions

**Census claim (from the brief):** 4 known collisions — `sweetsleep`, `peach`, `porridge`,
`sourleaf` — each existing as a node file under two category directories.
**Verified: the 4 named collisions are real, AND there are 3 more the census/brief didn't
name.** Full graph-wide scan (every slug across all top-level `graph/nodes/*/` category dirs)
finds **7 total collisions**:

| Slug | Categories | Same entity or true collision? |
|---|---|---|
| `sweetsleep` | `medical/` + `foods/` | **Same entity** (the sedative drug) — duplicate typing |
| `sourleaf` | `species/` + `foods/` | **Same entity** (the chewed plant/stimulant) — duplicate typing |
| `peach` | `locations/` + `foods/` | **True collision** — two different entities: the Stoney Sept **inn** ("The Peach") vs. the literal **fruit** Renly eats at the Storm's End parley |
| `porridge` | `foods/` + `characters/` | **True collision** — two different entities: the **food** vs. the nicknamed Dragonstone **gaoler** ("Porridge") |
| `a-storm-of-swords-prologue` | `chapters/` + `events/` | **Same content, wrong typing** — identical prose, `chapters/` copy is `type: meta.chapter` (correct), `events/` copy is `type: event.battle` (wrong — it's Chett's prologue chapter, not a battle) |
| `a-storm-of-swords-epilogue` | `chapters/` + `events/` | Same pattern as above — identical prose, `events/` copy mistyped `event.battle` |
| `stallion-who-mounts-the-world` | `concepts/` + `prophecies/` | **Same entity** (the Dothraki prophecy) — duplicate typing, different confidence tiers (concepts copy tier-2, prophecies copy tier-1) and different `pass_origin` (wiki-reconstruction vs. curator-s95-prophecy-linkage) |

**This confirms a real, not cosmetic, engine risk.** I checked how the query engine currently
resolves a bare slug to a file: `graph/query/weirwood_query/load.py::find_node_file()` does
`for type_dir in nodes_dir.iterdir(): candidate = type_dir / f"{slug}.node.md"; if
candidate.exists(): return candidate` — **first match wins, and `iterdir()` order is
filesystem-dependent, not alphabetical or otherwise guaranteed.** For any of these 7 slugs,
which file the engine returns today is arbitrary and could change between machines or after a
directory re-listing. I also checked which copy is actually *referenced by edges* (a good proxy
for "which one the rest of the graph already treats as real"):

| Slug | Edges referencing it | Which copy the edges mean |
|---|---|---|
| `peach` | 7 (`alyce/bella/cass/helly/jyzene/lanna-peach/tansy-innkeep SWORN_TO peach`) | **Location** (workers sworn to the inn) — `foods/peach` (the fruit) is edge-orphaned |
| `porridge` | 4 (`porridge GUARDS davos-seaworth`, `SWORN_TO house-baratheon-of-dragonstone`, `CULTURE_OF westerosi`, `BORN_AT westeros`) | **Character** (the gaoler) — `foods/porridge` is edge-orphaned |
| `stallion-who-mounts-the-world` | 2 (`rhaego SUBJECT_OF_PROPHECY stallion-who-mounts-the-world`, `stallion-who-mounts-the-world PROPHESIED_BY dosh-khaleen`) | Ambiguous by slug alone, but semantically clearly the **prophecy** sense |
| `a-storm-of-swords-prologue` | 1 (`mormont-s-battle-plan SUB_BEAT_OF a-storm-of-swords-prologue`) | Ambiguous by slug alone |
| `a-storm-of-swords-epilogue`, `sweetsleep`, `sourleaf` | 0 | No edges reference either copy — lower urgency, no live ambiguity yet |

### Per-slug verdict

- **`sweetsleep`** — **merge into `foods/sweetsleep`, delete `medical/sweetsleep`.** The foods
  copy is tier-1, book-cited (4 chapter+line citations to `sources/chapters/`), harvest-sourced
  (`s152-harvest`) and carries real aliases (`sweet sleep`, `sweetmilk`, `sweet milk`). The
  medical copy is tier-2, wiki-only, `aliases: []`, and mistypes it (`concept.medical`, but the
  Identity line literally says "Sweetsleep is a **species**" — a leftover templating bug from
  the deterministic wiki pass). The medical copy's *content* — the wiki Origins/Narrative-Arc
  prose spanning Fire & Blood-era usage through TWOW — is richer in book-spanning wiki detail
  than the foods copy's harvest notes, so **before deleting, fold the medical copy's wiki
  Narrative Arc section into the foods node** rather than a pure delete. Net: one node,
  `foods/sweetsleep`, type `object.food`, tier-1, combined content.
- **`sourleaf`** — **merge into `foods/sourleaf`** by the same logic (foods copy is tier-1,
  book-cited harvest content; `species/sourleaf` is tier-2 wiki content with real spanning-book
  detail worth folding in, not discarding). Type `object.food` (it's consumed, not a species in
  the biological sense the `species/` dir implies — `species/` should hold creatures, not plant
  products; this was likely an automated wiki-category misclassification).
- **`peach`** — **keep both, retype/rename to remove the collision** — this is NOT a duplicate,
  it's two different entities. Recommend renaming the fruit node's slug to something
  disambiguating, e.g. `peach-fruit` or `renlys-peach` (an alias already lists `Renly's peach`),
  leaving `locations/peach.node.md` as the canonical `peach` slug (it has live edges and is the
  proper-noun "The Peach" inn). Do NOT delete either — both are good content.
- **`porridge`** — same shape as peach: **keep both, retype/rename**. Recommend the food node
  moves to `porridge-food` or similar, leaving `characters/porridge` (nicknamed gaoler, has 4
  live edges) as the canonical `porridge` slug.
- **`a-storm-of-swords-prologue` / `a-storm-of-swords-epilogue`** — **delete the `events/`
  copies, keep the `chapters/` copies.** These aren't two entities — they're the same chapter,
  double-typed. The `events/` copy's `type: event.battle` is simply wrong (Merrett Frey's
  epilogue and Chett's prologue are POV chapters, not battles; likely an artifact of a wiki
  ingestion pass that treated every "X-Prologue"/"X-Epilogue" wiki page as a battle-bucket
  default). `chapters/` (`type: meta.chapter`, with `book`/`chapter_number`/`pov_character`
  fields populated) is the correct, richer typing. Before deleting, re-point the one live edge
  (`mormont-s-battle-plan SUB_BEAT_OF a-storm-of-swords-prologue`) — it already resolves fine
  by slug since after deletion there's only one `a-storm-of-swords-prologue` file left, so no
  edge rewrite is actually needed, just delete the `events/` file.
- **`stallion-who-mounts-the-world`** — **merge into `prophecies/stallion-who-mounts-the-world`,
  delete `concepts/stallion-who-mounts-the-world`.** The prophecies copy is tier-1
  (curator-linked, `curator-s95-prophecy-linkage`, cites `agot-daenerys-05` directly) — higher
  confidence and it's typed correctly (`type: prophecy`, matching the `prophecies/` dir; the
  concepts copy uses `type: concept.prophecy`, a type string that isn't the category-matching
  convention). The concepts copy's prose is more detailed (Rhaego/Mirri Maz Duur/House-of-the-
  Undying vision detail) and richer — **fold that detail into the prophecies node** rather than
  losing it, same pattern as sweetsleep/sourleaf.

**General pattern across all 7:** wherever one copy is `pass_origin: pass2-wiki-deterministic`
(the mechanical Pass-2 promotion) and the other is a later harvest/curator pass
(`s139-harvest`, `s152-harvest`, `s157-harvest-drain`, `curator-s95-...`), the later pass is
consistently tier-1/book-cited and richer in book-grounded specifics, while the wiki-
deterministic copy is consistently tier-2 and richer in wiki-spanning breadth (multi-book
Narrative Arc coverage the harvest passes didn't revisit). **The right merge direction is
always "keep the harvest/curator copy's frontmatter + tier, fold in the wiki copy's additional
Narrative Arc content that isn't already covered"** — not a blind pick-one.

**Risk:** medium for the two true-collision renames (`peach`, `porridge`) — renaming a slug
means updating any inbound edges/aliases that pointed at the *old* combined slug meaning to
disambiguate, and the alias-resolver/search-index need rebuilding after (per the standing
"rebuild derived artifacts after node mutation" rule). Low risk for the 3 same-entity merges
and the 2 chapter/event dedups — these are content folds + deletes with no slug rename, so the
one existing live edge for `a-storm-of-swords-prologue` and the edges for `stallion-who-mounts-
the-world`/`sourleaf`/`sweetsleep` (0 currently) don't need rewriting.

**Apply mechanism:** no automated script recommended — these are 7 individual content-fold/
retype/delete decisions requiring judgment on which prose survives. A future session should
handle each by hand (or by agent under Matt's direct supervision), then run:
`scripts/build-entity-indexes.py` and the alias-resolver/search-index rebuild afterward per the
standing rebuild-derived-artifacts rule.

- [ ] **Matt approves Class 5a: merge `sweetsleep` (medical→foods, fold content, delete medical copy)**
- [ ] **Matt approves Class 5b: merge `sourleaf` (species→foods, fold content, delete species copy)**
- [ ] **Matt approves Class 5c: disambiguate `peach` (rename food node's slug, keep location as canonical `peach`)**
- [ ] **Matt approves Class 5d: disambiguate `porridge` (rename food node's slug, keep character as canonical `porridge`)**
- [ ] **Matt approves Class 5e: dedup `a-storm-of-swords-prologue` (delete `events/` mistyped copy)**
- [ ] **Matt approves Class 5f: dedup `a-storm-of-swords-epilogue` (delete `events/` mistyped copy)**
- [ ] **Matt approves Class 5g: merge `stallion-who-mounts-the-world` (concepts→prophecies, fold content, delete concepts copy)**
- [ ] **Matt approves Class 5h: after any of 5a–5g apply, rebuild indexes + alias-resolver + search-index (standing rule, not optional)**

---

## What is NOT proposed here

- No alias **content** changes anywhere (Class 1 only fixes broken quoting syntax around
  existing alias text; Class 4 only proposes removing an empty key, never touches populated
  alias lists).
- No retypes beyond the specific dup-slug pairs in Class 5 (the `event.battle`→`meta.chapter`
  collapse and `concept.prophecy`→`prophecy`/`species`→`object.food`/`concept.medical`→
  `object.food` normalizations are scoped to exactly the 7 colliding slugs, not a graph-wide
  retype sweep).
- Nothing under `sources/` is touched or proposed to be touched.
- No deletion of any Pass-1-derived edge (Class 2's dangling-endpoint edges are recommended
  to be *kept*, not removed).
- No bulk `aliases: []` strip is applied by default (Class 4's default recommendation is
  leave-as-is; bulk-strip is offered only as an approvable alternative).
- No change to `dup_count` semantics or any edge corroboration data (confirmed this is a
  working feature, not a bug, while investigating Class 3).
- This session made **zero writes** under `graph/` — every count above came from read-only
  scans; scratch scripts live under `/private/tmp/.../scratchpad/`, not the repo.

---

## Summary table for a fast read

| Class | Census claim | Verified | Recommendation |
|---|---|---|---|
| 1. YAML-broken files | 5 | ✅ 5 confirmed exactly | Repair quoting in place |
| 2. Dangling-endpoint edges | 91 edges / 67 slugs | ⚠️ 67 edges / 62 slugs (discrepancy unresolved, pattern confirmed) | Keep edges; add `health` reporting |
| 3. Duplicate edge rows | 28 | ❌ 0 found under any tested key | No action; claim unverified |
| 4. Empty `aliases: []` | 6,923 | ✅ 6,921 (excl. `_conflicts`) — within rounding | Leave as-is (default); alternatives offered |
| 5. Cross-category slug collisions | 4 named | ✅ 4 confirmed + 3 more found (7 total) | Per-pair: 3 merges, 2 renames, 2 dedups (see above) |
