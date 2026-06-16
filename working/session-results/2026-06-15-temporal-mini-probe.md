---
date: 2026-06-15
probe: temporal-mini-probe
model: claude-sonnet-4-6
---

# Temporal Mini-Probe — Weirwood Network

Consumer-agent simulation: answer each temporal question using ONLY the query layer
(`event_alias_resolver.py` + `graph-query.py`), then grade against ground truth.

---

## Query Results Table

| # | Query | Resolver (phrase → status) | Graph's answer | Ground truth | Grade | Why |
|---|-------|---------------------------|----------------|--------------|-------|-----|
| 1 | What year (in-world AC) did Battle of the Trident take place? | `"Battle of the Trident"` → **HIT** (`battle-of-the-trident`) | **No year data.** Node exists with edges (FIGHTS_IN: Robert's Rebellion, DEFEATS: Decisive rebel victory) but frontmatter has no `year`, `occurred`, `ac_year`, or `date` field. Body text does not expose year structurally. | **283 AC** (wiki infobox, 283_AC.json events list: "Battle of the Trident" listed explicitly) | **FAILED** | Node discoverable; year completely absent from graph |
| 2 | Which happened first — Sack of King's Landing or Battle of the Trident? | `"Sack of King's Landing"` → **HIT** (`sack-of-kings-landing`) | **No ordering data.** Both nodes exist; neither has sequence/year fields. No PRECEDES/FOLLOWS/BEFORE edges between them. The Trident node's ## Aftermath text mentions the Sack as a consequence ("resulting in the Sack of King's Landing") but that's prose in the body, not a structured edge. | **Battle of the Trident first** (283 AC), **Sack of King's Landing immediately after** (same year, 283 AC). Causal sequence: Trident → Aerys opens gates → Sack. | **FAILED** | Both nodes hit but no temporal ordering edges; agent cannot derive sequence structurally |
| 3 | What major events were happening during the War of the Five Kings (contemporaneous)? | `"War of the Five Kings"` → **HIT** (`war-of-the-five-kings`) | **Partial structural answer.** `--neighbors war-of-the-five-kings` returns 69 INCOMING `PART_OF` edges listing sub-events (Battle in the Whispering Wood, Battle of Oxcross, Battle of the Blackwater, Red Wedding, etc.). No dates on those sub-events, but the "contemporaneous" question is answerable via PART_OF membership. | War of the Five Kings: 298–300 AC. Sub-battles listed in the graph match the canon list (Whispering Wood, Green Fork, Blackwater, etc.). | **PARTIAL** | Structural membership (PART_OF) answers "what battles were part of the war" but cannot answer contemporaneous events *outside* the war (e.g., events in Essos, Night's Watch movements) due to missing year indexing. |
| 4 | What notable events happened in the year 283 AC? | `"283 AC"` → **HIT-CHARACTER** (node exists but typed as character node, not year-index node) | **FAILED to answer.** The resolver returns `283-ac` with status `HIT-CHARACTER`, suggesting the 283 AC node exists but is mistyped. `--neighbors 283-ac` would be needed next, but a deployed agent has no indication this is worth pursuing after the HIT-CHARACTER warning. No year→event index exists in the graph. | **283 AC events** (from 283_AC.json): Battle of the Bells, Battle of the Trident, Sack of King's Landing, Wildfire Plot, Coronation of Robert, Siege of Storm's End lifted, Tower of Joy combat. Rich list available in wiki. | **FAILED** | No year→event index in graph; 283_AC node is mistyped as character; agent has no path to discover 283 AC events |
| 5 | How long before Robert's Rebellion was the Tourney at Harrenhal? | `"Tourney at Harrenhal"` → **HIT** (`tourney-at-harrenhal`); `"Robert's Rebellion"` → **HIT** (`roberts-rebellion`) | **Cannot compute.** Both nodes exist. `--path tourney-at-harrenhal roberts-rebellion` returns 0 direct edges and 0 2-hop bridges. Tourney node frontmatter has no year. Robert's Rebellion node has no year. No PRECEDES/temporal edges between them. | Tourney at Harrenhal: **281 AC**. Robert's Rebellion: **282–283 AC**. Gap: **~1–2 years** (rebellion began shortly after the tourney, triggered by events at it). | **FAILED** | Both nodes discoverable; neither carries year data; no ordering edges; agent cannot compute or even estimate the gap |

---

## Tally

| Grade | Count |
|-------|-------|
| Correct | 0 |
| Partial | 1 (Q3 — PART_OF membership answers sub-event listing but not full temporal context) |
| Failed | 4 (Q1, Q2, Q4, Q5) |

**Overall: 0/5 correct, 1/5 partial, 4/5 failed.**

---

## Check A — Do Event Nodes Carry Date/Year Fields?

```
grep -rlE "^(occurred|ac_year|year|date):" graph/nodes/events/ | wc -l
→ 0
```

**Zero event nodes have any date or year field in frontmatter.**

Inspected two nodes directly:
- `graph/nodes/events/battle-of-the-trident.node.md`: frontmatter fields are `name`, `type`, `slug`, `aliases`, `confidence`, `wiki_source`, `bucket_id`, `prompt_version`, `node_version`, `pass_origin`. No date field.
- `graph/nodes/events/sack-of-kings-landing.node.md`: identical frontmatter structure, no date field.
- `graph/nodes/events/tourney-at-harrenhal.node.md`: same. Text body mentions "281 AC" in prose but it is not captured as a structured field.

**Conclusion: no event in the graph is dated today.**

---

## Check B — Does `chronology-events.jsonl` Already Hold the Answers?

**Row count (event-typed entries):**
```
grep '"target_type": "event' working/wiki/data/chronology-events.jsonl | wc -l
→ 158
```

158 event-typed rows out of 2,245 total (the rest are characters, locations, factions, etc.).

**Key findings:**

| Question | In chronology-events.jsonl? | Year present? | Quality? |
|----------|----------------------------|---------------|---------|
| Battle of the Trident (Q1) | YES — `"Battle_of_the_Trident"` at **283 AC** (1 row) | YES | Strong: direct hit |
| Sack of King's Landing (Q2) | YES via Sack's inbound reference from chronology crawl (found as `event.battle` mention in 283 AC context from Battle of Trident row) | YES (283 AC, same year as Trident) | Moderate: ordering requires inference from same-year grouping |
| War of the Five Kings (Q3) | NOT directly (no `War_of_the_Five_Kings` row); sub-events at 298–300 AC are present (e.g., Battle in the Whispering Wood at 299 AC, others) | Partial (sub-events dated) | Moderate: parent war undated, but sub-battles are |
| 283 AC events (Q4) | YES — 3 event rows at 283 AC: `Battle_of_the_Bells`, `Battle_of_the_Trident`, `Wildfire_plot` | YES | Moderate: only 3/7+ canon events captured; the 283_AC.json wiki page is much richer |
| Tourney at Harrenhal (Q5) | YES — `Tourney_at_Harrenhal` appears **3 times** at **281 AC** | YES (281 AC, 3 confirmations) | Strong: high confidence, 3 independent year-page mentions |
| Robert's Rebellion year (for Q5 gap) | Partial: `Robert_I_Baratheon` at 282 AC (start) and 283 AC (end), no `Roberts_Rebellion` event row | YES (indirect) | Weak: must infer from character page mentions |

**Reliability assessment:**

The chronology-events.jsonl is a year-page→entity MENTION index, not a "this event occurred in year X" assertion. A year page mentions an entity because something happened that year — but the same event can appear under 2 different year pages (e.g., Tourney at Harrenhal announced 280 AC, held 281 AC → appears in both). Noise sources:
- Duplicate entries for the same event under adjacent years (e.g., Tourney at Harrenhal 3× at 281 AC from different page sections)
- Characters mentioned on year pages for peripheral reasons (e.g., being born, dying, attending) are mixed with events
- War of the Five Kings itself absent from chronology data despite being the dominant event of 298–300 AC

Despite this noise, the year assignments for clean event nodes (Tourney at Harrenhal = 281 AC, Battle of the Trident = 283 AC) look reliable and corroborate wiki infobox data. The data is sufficient for a deterministic ingestion pass: filter for `target_type` starting with `event`, pick the modal year per event slug, ingest as `ac_year` frontmatter.

---

## Bottom Line

### (1) Does the graph fail temporal queries today?

**Yes, almost completely.** 4 of 5 questions return zero temporal information. The 1 partial credit (Q3) is structural (PART_OF membership), not temporal. No event node carries a date. A deployed agent querying "when did X happen" or "what happened in year Y" or "how much time between X and Y" gets nothing from the graph.

### (2) Is the fix cheap (data already on disk) or expensive (needs extraction)?

**Cheap — data is already on disk, twice over:**

1. **`working/wiki/data/chronology-events.jsonl`** (2,245 rows): 158 event-typed rows with year values. Covers key events (Tourney at Harrenhal 281 AC, Battle of the Trident 283 AC). A Python script can filter these, deduplicate by slug, take modal year, and write `ac_year` to each matching node's frontmatter. Estimated: ~1 hour of scripting, <1 min runtime.

2. **`sources/wiki/_raw/283_AC.json`** (and other year pages): the wiki year pages have much richer events lists. The 283_AC page alone lists 7+ events for that year in plain text. A parser targeting these structured year pages would yield higher recall than the chronology-events.jsonl.

No LLM extraction needed. This is a deterministic backfill from existing data.

### (3) One-paragraph verdict on whether dating events is worth doing

Dating events is a high-value, low-cost improvement. The 5 temporal queries tested represent the most natural questions a reader or agent would ask about ASOIAF history — "when did this happen," "which came first," "what was happening in year X" — and the graph currently answers none of them. The fix requires only a Python script that reads `chronology-events.jsonl` (already on disk), filters to event rows, resolves slugs against the graph, and writes `ac_year` to node frontmatter. The ordering question (Q2: Trident before Sack?) would then become answerable by comparing `ac_year` values. The year-index question (Q4: events in 283 AC) would require a separate year-bucket index (one file or edge layer per year → events), which is also a pure Python task against existing data. Total estimated effort: one scripting session, no new API calls. Given that the graph's primary purpose is agent traversal for ASOIAF research queries, temporal anchoring is foundational infrastructure rather than a nice-to-have.

---

## Methodology Notes

- All queries used the two-tool query layer only (`event_alias_resolver.py --lookup` then `graph-query.py`), simulating a deployed agent without filesystem access
- Ground truth established via `sources/wiki/_raw/<Page>.json` and `working/wiki/data/chronology-events.jsonl` (fs-grep, not available to a deployed agent)
- Discoverability failures: Q4 (283 AC returns HIT-CHARACTER, not a year-event index) counts as a query-layer failure even though data exists on disk
