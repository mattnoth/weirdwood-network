# Reconciliation — S190 hygiene proposal Class 5 vs. the parallel slug-collision scan

**Date:** 2026-07-04 · **Status: annotation for Matt's review — nothing applied.**
Two sessions independently scanned the same problem this week:

- `working/query-layer/hygiene-proposal-s190.md` (Classes 1–5, checkboxes)
- `curation/slug-collision-resolutions-2026-07-04.md` (Class 5 only, worktree
  `vigilant-chebyshev-9cacb3`; now marked superseded by this reconciliation)

**The scans fully cross-validate:** both found the same 7 collisions and identical edge
counts (peach 7, porridge 4, stallion 2, ASOS-prologue 1, others 0). They also found
complementary halves of the engine risk — the S190 session showed the CLI's
`find_node_file()` returns an **arbitrary, filesystem-dependent** copy (`iterdir()`
first-match), and the worktree session showed `build_chat_bundle.py::load_nodes()`
deterministically ships the **alphabetically-later** category's copy (so the live bundle
currently serves e.g. the food `porridge` while all 4 edges mean the gaoler).

**Use the S190 file's checkboxes as the single approval surface**, with the three
amendments below. Classes 1–4 were only assessed by the S190 session; no second opinion
offered there (its recommendations read sound).

## Class 5 items where both sessions agree — approve as written

- **5c peach** — rename the food node's slug to `renlys-peach`; `locations/peach` stays
  canonical. (Both sessions converged on `renlys-peach` over `peach-fruit` — it's already
  the node's alias.)
- **5e/5f ASOS prologue/epilogue** — delete the mistyped `events/` copies, keep
  `chapters/`. One added flag from the worktree scan: the surviving edge
  `mormont-s-battle-plan -SUB_BEAT_OF-> a-storm-of-swords-prologue` will then target a
  `meta.chapter` node — fine as "beat anchored to its chapter," or re-parent to a real
  event node; Matt's call, not blocking the delete.
- **5g stallion direction** — merge into `prophecies/`, fold the concepts/ copy's rich
  Identity prose in, delete concepts/ copy. (Type amendment below.)
- **5h rebuild** — agreed and mandatory; note the live chat bundle additionally needs the
  manual `netlify deploy --prod --build` per `DEPLOY.md` to actually ship the fix.

## Amendment 1 — 5g type: the merged node should be `concept.prophecy`, not `prophecy`

The S190 proposal keeps `type: prophecy` as "the category-matching convention." That's
backwards on the evidence: 3 of the 4 nodes in `graph/nodes/prophecies/` use
`concept.prophecy` (the stallion stub is the lone `prophecy`), and `architecture.md:99`
documents `concept.prophecy` as the schema type. The merge should normalize the stub TO
`concept.prophecy`.

## Amendment 2 — 5a sweetsleep: recommend the merge run the OTHER direction (medical/ canonical)

S190 says foods/ canonical (keep `object.food`, delete medical/). The worktree proposal
says medical/ canonical, and the schema supports it: `architecture.md:102` defines
`concept.medical` as "Disease, **poison**, treatment, or medical condition" with examples
**milk of the poppy** and **the strangler** — sweetsleep, "the gentlest of poisons"
(AFFC, the waif), is squarely in that class. `object.food` (line 106) is scoped to
"hospitality/feast/guest-right artifacts." Two points from the S190 rationale don't
survive scrutiny:

- *Tier is not a tie-breaker*: the merged node ends tier-1 either way once the harvest
  book-cites are folded in — tier travels with the merged content, not the surviving file.
- The S190 proposal itself agrees the merge is "fold both, not pick-one" — the only real
  decision is category/type, and the schema says medical.

Honest counterweight: architecture lists *dreamwine* under `object.food`, so the
food/drug boundary isn't perfectly clean, and the harvest passes deliberately minted
sweetsleep under the food lens. If Matt weighs harvest-lens continuity over schema fit,
foods/ is workable — but the recommendation here is **medical/ canonical, foods content
folded in, foods copy deleted**. Either way: fix the medical copy's Identity line bug
("Sweetsleep is a **species** from the AWOIAF wiki").

## Amendment 3 — 5b sourleaf: the "species = creatures" premise is false; recommend species/ canonical

S190's argument for foods/ rests on "`species/` should hold creatures, not plant
products." The live directory disagrees: `graph/nodes/species/` already holds weirwood,
heart-tree, ghost-grass, devilgrass, daggerleaf, nightshade, tansy-plant, spiceflower,
wormtree, and more — plants are first-class residents of species/. Sourleaf is chewed
"in a similar fashion to chewing tobacco," not eaten as food or served in hospitality.
Recommendation: **species/ canonical, fold in the foods copy's Yoren quote + cite +
aliases, delete the foods copy.** Zero edge churn either way.

## Genuine coin-flip left for Matt — 5d porridge rename direction

The sessions split and both directions are defensible; neither is an error:

| | S190: rename FOOD → `porridge-food` | Worktree: rename CHARACTER → `porridge-gaoler` |
|---|---|---|
| Edge churn | **0** (character keeps slug; 4 live edges untouched) | 4 edge `source_slug` rewrites + alias-resolver remap of wiki page `Porridge` |
| Naming precedent | none (`-food` suffix is novel) | matches existing `lamprey-gaoler` (his fellow Dragonstone gaoler!), `tansy-innkeep`, `lanna-peach`, `tansy-plant` |
| Bare-word "porridge" resolves to | the gaoler | the food (the overwhelmingly more common query intent) |
| Wiki-page alignment | character stays aligned with page `Porridge` | resolver needs one remap |

Pick one on the 5d checkbox; whichever wins, both nodes are kept.

## Net checkbox guidance

- 5c, 5e, 5f, 5h — approve as written in the S190 file.
- 5g — approve with `concept.prophecy` as the merged type (Amendment 1).
- 5a — approve direction per Amendment 2 (medical/ canonical) unless Matt prefers the
  harvest food lens.
- 5b — approve direction per Amendment 3 (species/ canonical).
- 5d — Matt picks a column above.
- Post-apply hardening (either session can do it, code-side, ungated): make
  `load_nodes()` / `build_search_index.py` **fail loudly on duplicate slugs**, and give
  `find_node_file()` a deterministic order + collision warning, so this class can't
  silently recur.
