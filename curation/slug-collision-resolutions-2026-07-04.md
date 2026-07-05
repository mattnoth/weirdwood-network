# Slug collisions across graph/nodes/ category directories — resolution proposal

> **SUPERSEDED 2026-07-04 (same day):** the parallel S190 session produced the fuller
> `working/query-layer/hygiene-proposal-s190.md` (Classes 1–5, checkboxes), and the two
> Class-5 analyses are reconciled in
> `working/query-layer/hygiene-proposal-s190-reconciliation.md`. **Review THOSE two files;
> this one is kept only as the worktree scan record.** Both scans found the same 7
> collisions and identical edge counts.

**Date:** 2026-07-04 · **Status: PROPOSAL — nothing applied. Matt reviews, then a follow-up session applies.**
**Found by:** query-layer search-substrate step (build_search_index.py / build_chat_bundle.py work).

## Why this matters

`build_chat_bundle.py::load_nodes()` keys `nodes.json` by slug while walking
`sorted(nodes_dir.rglob("*.node.md"))` — so when the same slug exists in two category
directories, the **alphabetically-later directory silently wins** in the shipped chat
bundle, and the CLI sees a different node depending on which directory it reads.
Full scan (all 20 category dirs, 8,720 unique slugs): **7 collisions**, listed below
with what the bundle currently serves vs. what it should.

Two distinct classes:

- **Class A — same entity, duplicate nodes** (merge): sweetsleep, sourleaf, stallion-who-mounts-the-world, ASOS prologue, ASOS epilogue
- **Class B — different entities sharing a slug** (rename one): peach, porridge

Edge references were checked against `graph/edges/edges.jsonl` (`source_slug`/`target_slug`);
edge-churn counts below are exact.

---

## Class A — same entity duplicated (recommend MERGE)

### 1. `sweetsleep` — foods/ vs medical/

| | `foods/sweetsleep.node.md` | `medical/sweetsleep.node.md` |
|---|---|---|
| type / tier | object.food / tier-1 | concept.medical / tier-2 |
| origin | s152-harvest | pass2-wiki-deterministic |
| size | 2.4 KB | 6.2 KB |
| strengths | navigable book cites (AFFC Alayne I/II, ADWD Blind Girl), verbatim Colemon quote, aliases `["sweet sleep","sweetmilk","sweet milk"]` | broadest coverage: ACOK→TWOW + Fire & Blood (Jaehaera), Varys/black-cells escape, Pycelle, waif's "gentlest of poisons" |
| bundle currently serves | — | ✅ (medical > foods) |

**Recommendation:** canonical = **`medical/sweetsleep.node.md`** (a sedative/poison is
`concept.medical`, not `object.food`). Merge INTO it from foods/: the harvest Narrative-Arc
bullets with their `sources/chapters/...:line` cites, the Colemon block-quote, and the alias
list. Then delete `foods/sweetsleep.node.md`. This is exactly the book-citation-overlay
pattern (Tier-2 wiki prose + Tier-1 navigable book cites on the same node).
Also fix a latent bug while there: its Identity line reads "Sweetsleep is a **species** from
the AWOIAF wiki" (wrong generated type-word).
**Edge churn: 0** (no edges reference `sweetsleep`).
*Alternative:* canonical in foods/ if you want harvest food-lens nodes to always survive
merges — but sweetsleep isn't food; medical is the honest home.

### 2. `sourleaf` — foods/ vs species/

| | `foods/sourleaf.node.md` | `species/sourleaf.node.md` |
|---|---|---|
| type / tier | object.food / tier-1 | species / tier-2 |
| origin | s157-harvest-drain | pass2-wiki-deterministic |
| size | 1.2 KB | 4.1 KB |
| strengths | verbatim Yoren quote + navigable ACOK cite, aliases `["sourleaf","sour leaf"]` | coverage across all 5 books + TSS (Bennis), Masha Heddle, Marwyn, Emmon Frey |
| bundle currently serves | — | ✅ (species > foods) |

**Recommendation:** canonical = **`species/sourleaf.node.md`** (a chewed stimulant leaf —
"in a similar fashion to chewing tobacco" — is a plant/species, not a food). Merge the
harvest quote + cite + aliases in; delete the foods copy. **Edge churn: 0.**

### 3. `stallion-who-mounts-the-world` — concepts/ vs prophecies/

| | `concepts/...node.md` | `prophecies/...node.md` |
|---|---|---|
| type / tier | concept.prophecy / tier-2 | prophecy / tier-1 |
| origin | pass2-wiki-reconstruction-mission-batch-2 | curator-s95-prophecy-linkage |
| size | 1.6 KB — rich 3-paragraph Identity (dosh khaleen, Rhaego, MMD, HotU vision) | 0.5 KB stub, but `sources: ["agot-daenerys-05"]` + alias "khal of khals" |
| edges | — | anchors both existing edges: `rhaego -SUBJECT_OF_PROPHECY->` and `-PROPHESIED_BY-> dosh-khaleen` |
| bundle currently serves | — | ✅ the thin stub (prophecies > concepts) |

**Recommendation:** canonical = **`prophecies/stallion-who-mounts-the-world.node.md`**
(dedicated prophecies/ dir, tier-1 book-sourced, the S95 edge anchor). Merge the concepts/
copy's rich Identity prose in, union the aliases, and normalize its type to
**`concept.prophecy`** (the other 3 prophecies/ nodes use it; the stub's bare `prophecy` is
itself off-convention). Delete the concepts/ copy. **Edge churn: 0** (slug unchanged and
both edges already point here).

### 4 + 5. `a-storm-of-swords-prologue` / `a-storm-of-swords-epilogue` — chapters/ vs events/

Same wiki page ingested twice by two Pass-2 deterministic buckets: `meta-chapters-asos`
(→ chapters/, `meta.chapter`, with book/chapter_number/pov_character frontmatter) and
`battles-a` (→ events/, **`event.battle`** — a POV chapter is not a battle; its `sort_keys`
are all null / basis "none"). Bodies are byte-near-identical wiki chapter summaries.
Bundle currently serves the mistyped events/ copies (events > chapters).

**Recommendation:** **delete both `events/` copies**; keep `chapters/`. These are
misclassified duplicate ingests, same deletion precedent as other Pass-2 misfiles.
**Edge churn: 1 edge to review, 0 to rewrite:** `mormont-s-battle-plan -SUB_BEAT_OF->
a-storm-of-swords-prologue` (plate4-wiki-cluster). Slug survives, so post-delete it resolves
to the meta.chapter node. **Flag for Matt:** is `SUB_BEAT_OF → meta.chapter` acceptable
(beat anchored to its chapter), or should that beat be re-parented to a real event node
(e.g. the great-ranging arc)? No other book's prologue/epilogue collided — only the ASOS
pair landed in `battles-a`.

---

## Class B — different entities, same slug (recommend RENAME one)

### 6. `peach` — foods/ (Renly's peach) vs locations/ (the Peach, Stoney Sept brothel)

Genuinely distinct entities. All **7 edges** reference the brothel (`alyce/bella/cass/
helly/jyzene/lanna-peach/tansy-innkeep -SWORN_TO-> peach`, wiki-infobox). The wiki page
`Peach` IS the brothel, so the location keeps page-name alignment for the alias-resolver /
infobox machinery.

**Recommendation:** keep both nodes; **rename `foods/peach` → slug `renlys-peach`**
(the node is already named/aliased "Renly's peach" — the qualified name is natural).
Keep `locations/peach` as-is. Add spaced aliases on the food node ("Renly's peach",
"a peach" already present; consider "peach" too — but note a bare-"peach" alias re-collides
with the location's name in the resolver; decide the tie-break or omit it).
**Edge churn: 0** (no edges reference the fruit).
*Alternative:* rename the location → `the-peach` instead (costs 7 edge rewrites + a
wiki-page→slug remap in the alias resolver). Not recommended.

### 7. `porridge` — characters/ (Davos's Dragonstone gaoler) vs foods/

Genuinely distinct entities. All **4 edges** reference the CHARACTER
(`porridge -GUARDS-> davos-seaworth` book-pass1, + 3 wiki-infobox: SWORN_TO
house-baratheon-of-dragonstone, CULTURE_OF, BORN_AT). But the bundle currently serves the
FOOD (foods > characters) — so the live bundle's 4 character edges dangle onto a food node.

**Recommendation:** keep both nodes; **rename `characters/porridge` → slug
`porridge-gaoler`**, matching the established character-disambiguator pattern — his fellow
gaoler already lives at `characters/lamprey-gaoler.node.md`, alongside `tansy-innkeep`,
`lanna-peach`. Bare-word "porridge" queries mean the food, which keeps the plain slug
(there is no natural qualified slug for generic porridge).
**Edge churn: 4** — rewrite `source_slug` on the 4 edges above; remap wiki page `Porridge`
→ `porridge-gaoler` in the alias resolver; keep `name: "Porridge"` and add a spaced alias
like "Porridge the gaoler".
*Alternative:* rename the food instead (0 edge churn) — rejected: no good qualified slug,
and it inverts the natural bare-word meaning.

---

## After apply (whoever executes, post-approval)

1. Apply merges/renames/deletes above — **node files + the 4 porridge edge rows only**.
2. Rebuild derived artifacts (node ADD/RENAME rule): entity indexes + alias resolver
   (`weirwood refresh` path), then search index + chat bundle.
3. Redeploy per `DEPLOY.md` (manual `netlify deploy --prod --build` — push ships nothing).
4. Optional hardening (separate, code-side, no approval needed on graph data):
   make `load_nodes()` **fail loudly on duplicate slugs** instead of silently
   last-writer-wins, so this class can't recur unnoticed. Same guard belongs in
   `build_search_index.py`.
