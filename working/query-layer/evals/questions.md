# Query-Layer Eval Question Set (v1)

> Part of the **query-layer Track** (design: `working/query-layer/design.md`), **step 3**
> (session B). Fixed set of ~20 questions used to score retrieval before/after every
> retrieval-touching step. IDs are stable across the Track — do not renumber; if a question
> is retired, mark it "RETIRED (reason)" in place rather than reusing its number.
>
> **Tier** = confidence 1–5 only (not used in this doc). **Track**/**step** per
> `reference/glossary.md`.
>
> Columns:
> - **id** — Q1..Q20, stable.
> - **question** — the natural-language question a consumer (chat visitor or in-repo agent)
>   would ask.
> - **archetype** — one of `traversal` (causal/relational walk), `quote-hunter` (wants a
>   specific verbatim line), `thematic` (descriptive/aggregative — "tell me about X kind of
>   thing"), `researcher` (claim-check / verification-style question).
> - **key phrases** — the natural-language entity phrases a model would need to resolve to
>   answer the question at all. These are the exact strings fed to `resolve` in both profiles.
> - **target slugs** — the node slug(s) that, if reached, would let a model answer the
>   question (hand-identified by reading the graph, per the Track's runner design — the
>   runner checks these for existence + quote count; it does not discover them itself).
> - **expected-answerable-via** — which ops (per `graph/query/spec/operations.md`) could
>   answer this if fully wired, whether or not that op exists yet in the bounded profile
>   today. `search`/`list`/`theme` are named even though PLANNED (step 5/8a) — the runner's
>   tool-call heuristic treats them as unavailable in the bounded profile until they ship.
> - **notes** — provenance (which requirement seeded this row) + anything a runner/human needs
>   to know when scoring it.

---

## Source note on the 10 Mode-3 dip questions

`working/session-results/2026-06-14-mode3-dip-results.md` has exactly **10** questions
(§1, rows 1–10). No adaptation needed — all 10 are usable as-is and become **Q1–Q10** below,
preserving the dip's own numbering order. Q1–Q10 also already carry a `graph's answer` /
`ground truth` / `grade` from that manual dip; the runner does NOT re-derive those grades — it
computes fresh mechanical resolve/content/tool-call metrics, which is a different (and
reproducible) measurement than the dip's hand-graded verdicts. Where useful, this doc notes
the dip's original grade for cross-reference.

---

## The 20 questions

| id | question | archetype | key phrases | target slugs | expected-answerable-via | notes |
|---|---|---|---|---|---|---|
| Q1 | Who killed Robb Stark? | traversal | `Robb Stark's death`, `Robb Stark` | `robb-is-killed`, `roose-bolton`, `walder-frey` | resolve → neighbors (or chain) | Mode-3 dip #1. Dip grade: correct, but only after a filesystem-search workaround — resolver MISS on the natural phrase at dip time. Runner checks: does `Robb Stark's death` resolve today (G19 fix target)? |
| Q2 | Who ordered the Red Wedding? | traversal | `the Red Wedding` | `red-wedding`, `walder-frey`, `roose-bolton`, `tywin-lannister` | resolve → participants (full) / neighbors (bounded) | Mode-3 dip #2. Dip grade: partial — on-page orderers (Frey, Bolton) present; Tywin's off-page causation has no edge (dark-historical, not a query-layer fix). `tywin-lannister` target slug is included for completeness but is NOT expected to be reachable via graph edges from `red-wedding` — a known, accepted gap. |
| Q3 | Who crowned Lyanna Queen of Love and Beauty? | traversal | `Lyanna crowned queen of love and beauty`, `Lyanna Stark` | `lyanna-stark`, `rhaegar-targaryen` | resolve → neighbors | Mode-3 dip #3. Dip grade: correct, but only after resolver MISS + filesystem search. The `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edge sits directly on `lyanna-stark`/`rhaegar-targaryen`, not on `tourney-at-harrenhal` (see Q5). |
| Q4 | What weapon killed Robb Stark? | quote-hunter | `Robb Stark's death` | `robb-is-killed` | resolve → neighbors / read | Mode-3 dip #4. **Post-dip re-grade (2026-06-14, §6): not-applicable, not a graph defect.** The killing weapon is a generic unnamed longsword — `WIELDED_IN`'s target must be a named `object.artifact` node, so no edge is expected here. Runner should report this as content-present-but-unnamed, not as a failure, per the dip's own correction. |
| Q5 | Who fought at the Tourney at Harrenhal? | traversal | `Tourney at Harrenhal` | `tourney-at-harrenhal` | resolve → neighbors (full) / theme (bounded, planned) | Mode-3 dip #5. Dip grade: failed — hub has 0 edges (confirmed again this session: `tourney-at-harrenhal` carries 0 quotes in the live bundle). Reframed post-dip (§6) as the poster child for historical-hub attachment (a separate, non-query-layer track) — the Rhaegar/Lyanna dyad (Q3) already holds the fact, just not attached to this hub. |
| Q6 | How are Tywin Lannister and Gregor Clegane connected? | traversal | `Tywin Lannister`, `Gregor Clegane` | `tywin-lannister`, `gregor-clegane` | resolve → path (full only — bounded has no `path` yet, step 6b) | Mode-3 dip #6. Dip grade: correct, best-in-class (4 direct edges + 9 2-hop bridges in the full profile). Bounded profile has no `path` op today — this row also measures the port gap (G-table, step 6b). |
| Q7 | Who attended Ned Stark's execution? | traversal | `Ned Stark's execution`, `Eddard Stark` | `execution-of-eddard-stark`, `eddard-stark` | resolve → participants / neighbors | Mode-3 dip #7. Dip grade: partial — perpetrators (Ilyn Payne, Joffrey) + weapon (Ice, WIELDED_IN) captured; the watching crowd (Sansa/Arya/Cersei) has no `ATTENDS` edges (dark-vocab, not a query-layer fix). |
| Q8 | What is Jon Snow's relationship to Ned Stark, who is he sworn to, and where was he born? | traversal | `Jon Snow`, `Eddard Stark` | `jon-snow`, `eddard-stark` | resolve → neighbors / family_tree | Mode-3 dip #8. Dip grade: correct (PARENT_OF, SWORN_TO nights-watch all present); `BORN_AT` deliberately absent — treated as correct restraint, not a defect, per the dip. |
| Q9 | What set the incident at the Trident (Joffrey/Mycah/Nymeria) in motion? | traversal | `incident at the Trident`, `Mycah` | `incident-at-the-trident`, `mycah` | resolve → chain (once hub exists) | Mode-3 dip #9. Dip grade: failed (EXPECTED baseline) — `incident-at-the-trident` does not exist as a node yet; `mycah` exists but is unconnected to any incident hub (0 quotes live). Pre-mint gap, not a query-layer defect. |
| Q10 | What were the consequences of the Battle of the Trident? | traversal | `Battle of the Trident` | `battle-of-the-trident` | resolve → chain (causal) | Mode-3 dip #10. Dip grade: failed — hub only carries `PART_OF roberts-rebellion`, no `CAUSES`/`TRIGGERS` edges radiate out (dark-vocab / causal-edge gap, a data track, not this Track's fix — though `chain`'s existence is exactly the op this question needs once the edges exist). |
| Q11 | Describe some detailed meals in the books. | thematic | *(no single entity phrase — this is the S188 live-failure case)* | `lemon-cake`, `honeyed-ham`, `bowl-of-brown`, `fish-stew`, `guest-right` (feast context) | search (planned, step 5) / list (planned, step 5d) / theme (planned, step 8a) | **The S188 live failure**: 13 fuzzy/no-match resolves, loop-bound, no answer. This is the row the meals-question improvement metric (design doc §2b/D-I) must show flipping after step 5. Today: no content-first op exists in either profile, so this is fundamentally unanswerable via resolve+read alone — it requires guessing food-node names, which is not a real strategy. Marked loop-bound (∞) in the baseline by construction. |
| Q12 | Who is Aegon the Conqueror? | quote-hunter | `Aegon the Conqueror` | `aegon-i-targaryen` | resolve → read | S177 marquee resolve. Confirmed live 2026-07-04: exact-lookup MISS, falls to the character-name-exact path → `hit-character` (full) / would need equivalent bounded handling — the bounded TS resolver has no `hit-character` status (see operations.md `resolve` §"Semantics" appendix note 2); it would land this via the exact alias-map hit today (`aegon the conqueror` IS a key in `web/data/alias-map.json` → `aegon-i-targaryen`, verified). Both profiles currently succeed on this phrase. |
| Q13 | Trace the Targaryen dynasty. | traversal | `Targaryen dynasty`, `House Targaryen` | `house-targaryen`, `aegon-i-targaryen` | resolve → family_tree | S177 marquee resolve. Confirmed live 2026-07-04: `"targaryen dynasty"` is a MISS in both the full all-node index and the bounded `alias-map.json` (no exact key) — falls to fuzzy in both profiles. `"House Targaryen"` (an alternate, more natural phrasing) resolves cleanly to `house-targaryen`. This row specifically measures the bare `"Targaryen dynasty"` phrasing's fuzzy-fallback quality, which is the marquee failure S177 flagged. |
| Q14 | How did Robb Stark die? | quote-hunter | `Robb Stark's death` | `robb-is-killed` | resolve → read | Explicit required question ("Robb Stark's death"). Distinct from Q1 (who) — this row targets the quote/manner-of-death content (`read`'s `quotes[]`), not the perpetrator edges. Same resolve mechanics as Q1/Q4 apply (G19: fuzzy-not-exact in the bounded bundle as of 2026-07-04). |
| Q15 | What are lemon cakes and who eats them? | quote-hunter | `lemon cakes` | `lemon-cake` | resolve → read (today: MISS/near-miss); search (planned) | Explicit required question ("lemon cakes"). Confirmed live 2026-07-04: `"lemon cakes"` has no exact alias-map key; the live node is singular `lemon-cake` (0 quotes in the bundle) — this is **G2**, the design doc's own worked example. A correct answer requires either a variant-expansion fix (step 4b, plural "lemon cakes" → "lemon cake") or content search reaching the quote text directly (step 5) — resolve-by-name alone is expected to underperform even after 4b, since the node itself currently carries 0 quotes. |
| Q16 | What does the graph say about hospitality customs (guest right, welcoming guests)? | thematic (hospitality) | `guest right`, `hospitality` | `guest-right`, `catelyn-secures-guest-right` | resolve → read; theme (planned, step 8a) hospitality seed theme | Required hospitality thematic question. `guest-right` resolves exactly today (2 quotes) and `catelyn-secures-guest-right` is a related event node — a reasonable traversal answer exists now via resolve+read, unlike Q11; this row is the "thematic archetype that already mostly works" control, useful for contrast against Q11's total failure. |
| Q17 | Does the graph support the claim that Tywin Lannister orchestrated the Red Wedding? | researcher | `Tywin Lannister`, `the Red Wedding` | `tywin-lannister`, `red-wedding` | resolve → neighbors/chain (both resolve fine; the connecting edge does not exist) | Required researcher claim-check question. This is a genuine claim-verification task: both entities resolve cleanly, but (per Q2 / the dip's dark-historical finding) no edge connects `tywin-lannister` to `red-wedding` in the live graph — the correct researcher answer is "the graph does not support this claim directly; the on-page orderers are Walder Frey and Roose Bolton," which requires the model to reason about an *absence* of an edge, not just report one. Tests whether a consumer can distinguish "not found" from "not supported." |
| Q18 | Is it true that Ned Stark was executed with a named ancestral sword, and if so which one? | researcher | `Ned Stark's execution` | `execution-of-eddard-stark` | resolve → neighbors (WIELDED_IN → Ice) | Researcher claim-check question, paired with Q7/Q4's WIELDED_IN contrast: this hub DOES carry `WIELDED_IN → ice` (a named artifact), unlike Q4's Robb hub. A correct researcher answer confirms the claim and names Ice. Tests the resolver + neighbors path on a hub the dip already validated as working (Q7). |
| Q19 | What connects Jaime Lannister's confession about Tysha to later events? | traversal | `Jaime Lannister`, `Tysha` | `jaime-reveals-the-truth-of-tysha` | resolve → chain (causal) | Fills the `chain`/causal-traversal archetype slot with a node the design doc itself names as a live fork-hub example (operations.md `braid` section: `jaime-reveals-the-truth-of-tysha`, out=3, reach=11) — a good positive-control causal-chain case, complementing Q10's negative control (Trident has no causal edges) and Q9's pre-mint negative control. |
| Q20 | Walk the Targaryen family tree from Aegon the Conqueror down to Daenerys. | traversal | `Aegon the Conqueror` | `aegon-i-targaryen`, `daenerys-targaryen` | resolve → family_tree | Positive-control `family_tree` archetype case — operations.md documents this exact pair (`aegon-i-targaryen` → `daenerys-targaryen`, 12 `PARENT_OF` hops) as the deep-main-line-spine behavior that only fires under `family_tree`'s **default** generationsDown, not a shallow explicit window. Pairs with Q13 (bare "Targaryen dynasty" phrasing) using a fully-specified phrasing instead. |
| Q21 | What was served at the Purple Wedding? | thematic | `Purple Wedding` | `purple-wedding`, `leche-of-brawn`, `chickpea-paste`, `wedding-feast-at-the-red-keep` | search → read | Added session B step 5 (post-step4 gate task) — the SERVED_AT board's settle-question. **This is the 8d trigger metric** — a content-first control question that, unlike Q11 (zero key phrases, generic "meals" framing), names the event directly, so its literal phrasing is both a resolve phrase AND a strong search_quotes query. Confirmed live 2026-07-04: searching `"What was served at the Purple Wedding?"` against the bundle's compact `search-index.json` returns `purple-wedding` at rank 1 and both `leche-of-brawn` and `wedding-feast-at-the-red-keep` in the top 12 (`chickpea-paste` does not land in this run — 3/4 target slugs hit). Reported as INFORMATION, not a pass/fail gate. |

---

## Archetype split

| archetype | ids | count |
|---|---|---|
| traversal | Q1, Q2, Q3, Q5, Q6, Q7, Q8, Q9, Q10, Q13, Q17, Q19, Q20 | 13 |
| quote-hunter | Q4, Q12, Q14, Q15 | 4 |
| thematic | Q11, Q16, Q21 | 3 |
| researcher | Q17, Q18 | 2 |

(Q17 double-counted: it is both a traversal-shaped question — resolve two entities and walk
between them — and a researcher claim-check in intent. Left in both rows above rather than
forcing a single-bucket split; the archetype-split table's total (13+4+3+2=22) is 21 unique
questions with Q17 counted twice by design.)

---

## Appendix — session log

- **2026-07-04 (S189, step 3 / session B):** v1 written. All 10 Mode-3 dip questions used
  verbatim as Q1–Q10 (no adaptation needed — the dip file had exactly 10 usable rows). Q11
  is the meals question (S188 live failure, verbatim). Q12/Q13 are the S177 marquee resolves
  ("Aegon the Conqueror" / "Targaryen dynasty" — confirmed live against `web/data/alias-map.json`
  and the full-profile all-node index this session: Q12 currently succeeds in both profiles,
  Q13 currently misses-to-fuzzy in both). Q14/Q15 are the explicitly required "Robb Stark's
  death" and "lemon cakes" questions. Q16 is the required hospitality thematic question
  (`guest-right`, confirmed 2 live quotes). Q17/Q18 are the required researcher claim-check
  questions (one negative control — claim NOT supported by an edge — one positive control).
  Q19/Q20 round out the traversal/family_tree archetypes with cases already named as
  verification anchors elsewhere in the query-layer Track (operations.md's `braid` and
  `family` sections) — reusing already-grounded slugs rather than hand-picking new ones.
- **2026-07-04 (session B, post-step4 exit-gate task):** Added **Q21** ("What was served
  at the Purple Wedding?") — the SERVED_AT board's settle-question, and the 8d trigger
  metric. `run_evals.py`'s tool-estimate heuristic was updated the same session to model
  the shipped `search_quotes` tool (step 5) instead of treating all content-first ops as
  absent — search-reachability is now checked DETERMINISTICALLY (an actual `search()` call
  against the live bundle index, not an assumption) per question. See
  `post-step5-2026-07-04.md` for the re-run.
