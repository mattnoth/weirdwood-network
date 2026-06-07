# Edge-Modeling — Cleanup Decisions RESOLVED (Matt-approved 2026-06-06)

This is the **authoritative** disposition for the pre-Plate-3 cleanups. It supersedes the
"needs human judgment" / "medium/low confidence" flags in the candidate files. The Plate 5
gated merge executes against THIS document. Nothing here is applied yet — all staging.

Every decision below was verified against the live repo / local wiki cache (read-only). All
have **zero affected edges** in `graph/edges/edges.jsonl` (independently confirmed), so they are
zero-risk to the current edge graph.

---

## 1. Drift reclassification — 12 nodes (from `drift-reclassify-candidates.jsonl`)

**Decision:** all 12 → **move** `graph/nodes/events/<slug>.node.md` → `graph/nodes/chapters/<slug>.node.md`
AND set `type: meta.chapter`. (`graph/nodes/chapters/` exists, holds the 344 real chapter nodes.)
These are POV-chapter / framing articles (TWoW samples + ASOS prologue/epilogue), not in-world events.

Slugs: `a-storm-of-swords-epilogue`, `a-storm-of-swords-prologue`, `alayne-i-the-winds-of-winter`,
`arianne-i-the-winds-of-winter`, `arianne-ii-the-winds-of-winter`, `barristan-i-the-winds-of-winter`,
`barristan-ii-the-winds-of-winter`, `mercy-the-winds-of-winter`, `the-forsaken-the-winds-of-winter`,
`theon-i-the-winds-of-winter`, `tyrion-ii-the-winds-of-winter`, `victarion-i-the-winds-of-winter`.

Affected edges: **0**. Source-data rule: move + retype, do not delete.

---

## 2. Collision merges — 4 high-confidence (from `collision-merge-candidates.jsonl`)

**Decision:** merge each non-canonical into the canonical; non-canonical node gets `SAME_AS` /
`ALIAS_OF` → canonical and is quarantined/redirected (NOT deleted, per CLAUDE.md). All four are
wiki-redirect stubs already carrying `same_as` frontmatter.

| Canonical (keep) | Merge in (redirect) |
|---|---|
| `battle-at-the-mummers-ford` | `battle-of-the-mummers-ford` |
| `battle-at-the-red-fork` | `battle-of-the-red-fork` |
| `battle-in-the-whispering-wood` | `battle-of-the-whispering-wood`, `battle-of-whispering-wood` |
| `battle-on-the-green-fork` | `battle-of-the-green-fork` |

Affected edges: **0**.

---

## 3. `conquest-of-dorne` — NOT a merge → reclassify the book (verified against wiki cache)

The two nodes are **distinct entities**, confirmed from `sources/wiki/_raw/`:
- `Conquest_of_Dorne` → *"...Date 157–161 AC, Location Dorne... Result Short-lasting conquest..."* = the historical **war/event**. Keep `conquest-of-dorne` as the event node (leave type as-is).
- `The_Conquest_of_Dorne` → *"is a **book** written by the Young Dragon, King Daeron I Targaryen, in which he recorded his version of his invasion of Dorne."* = a **text**, mis-minted as `event.war`.

**Decision:** reclassify `the-conquest-of-dorne` `type: event.war` → **`object.text`** (move
`graph/nodes/events/the-conquest-of-dorne.node.md` → `graph/nodes/texts/the-conquest-of-dorne.node.md`).
Do **not** merge the two. Affected edges: **0**.
*Future (not now):* an edge `WRITTEN_BY: the-conquest-of-dorne → daeron-i-targaryen` is warranted
(the wiki names the author) — defer to a later texts pass, not this cleanup.

---

## 4. `tourney-at/of-maidenpool` — merge, canonical resolved from wiki redirect

`sources/wiki/_raw/Tourney_of_Maidenpool.json` = *"Redirect to: Tourney at Maidenpool"*.
**Decision:** canonical = **`tourney-at-maidenpool`**; merge `tourney-of-maidenpool` → it
(SAME_AS/ALIAS_OF + redirect, not deleted). Affected edges: **0**.
(Both refer to the 208 AC tourney; the 103 AC tourney is a separate page — out of scope.)

---

## 5. Plate 3 modeling confirmation — group/faction actors

**CONFIRMED (Matt 2026-06-06):** `house.*` is a permitted `AGENT_IN` source for group actors
("Bolton men-at-arms" → `house-bolton AGENT_IN <event>`; "Frey crossbowmen" → `house-frey AGENT_IN`).
The Plate 1c validator contract already allows character.* OR house.* as AGENT_IN/VICTIM_IN source.
Do not drop group action for lack of a named individual.

---

## Execution location

All of §1–§4 are applied at the **Plate 5 gated merge** (with backup + before/after diff + sign-off),
alongside the Plate 0 normalizer + Aerys merge and the Plate 3/4 staged outputs. §5 is a standing
rule for the Plate 3 backfill run.
