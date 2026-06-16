# Design Opinion: Events, Time, and Causal Edges
**Lens: graph data-modeling & sequencing**
**Date: 2026-06-15**
**Author: independent advisor**
**Graph state at time of review:** 590 event nodes, 21,993 edges, 125 types; role edges (AGENT_IN / VICTIM_IN / COMMANDS_IN / SUB_BEAT_OF) live and populated; causal edges (CAUSES / TRIGGERS) defined in schema but zero instances; ATTENDS populated but thin (~986 instances, mixed event and non-event targets); no date fields on any event node frontmatter.

---

## 1. WHERE should time live?

**Recommendation: event-node frontmatter as the primary home; derived edges only for a narrow subset.**

### The concrete frontmatter block

Add an `occurred:` block to event node frontmatter. It is optional (unknown = omit the block entirely, not `null`). Two sub-fields, one per axis (see §2):

```yaml
occurred:
  in_world: "283 AC"          # in-world calendar date (string, free-form but anchored to AC/BC/pre-conquest)
  in_world_precision: year    # year | decade | era | approximate | contested
  narrative_first: "agot-3"  # book-chapter key of earliest reader encounter; format: {book}-{chapter_number}
```

`in_world` is a human-readable string, not a machine integer, because ASOIAF dating is inconsistently sourced and often approximate ("around 283 AC", "early in the year", "some years before the Conquest"). Forcing an integer invites false precision. The `in_world_precision` enum signals query consumers how hard to trust the value.

`narrative_first` is a simple dotted key (`agot-3`) pointing at the `meta.chapter` node where the reader first encounters evidence of this event — for narrated-in-the-present events this is the chapter they happen; for historical backstory this is the earliest chapter that mentions them. This field is derivable in many cases from the existing `evidence_book` / `evidence_chapter` fields on the edges pointing TO the event node — a Python script can bootstrap most of it without an LLM pass.

### What about derived edges?

Do NOT mint `OCCURRED_IN_YEAR` edges. There is no second node to attach them to (years are not graph citizens), so they would be dangling typed integers masquerading as relationships. They add traversal overhead with zero graph value.

DO mint `PRECEDES` / `FOLLOWS` edges — but **only as lazy fills where ordering is non-obvious and causally neutral**. Ninety-plus percent of ordering information is free once events are dated: a Python script can emit all `PRECEDES` edges mechanically from `in_world` values with matching precision. For events with the same `in_world` date (same year, different month), ordering remains uncertain and should not be silently invented. The tiny remainder that require actual sequencing knowledge belong to `CAUSES` / `TRIGGERS`, not `PRECEDES` — see §3.

**Summary: primary home is node frontmatter. Derived PRECEDES/FOLLOWS edges are auto-generated from dated nodes; they are not primary storage.**

---

## 2. The dual axis: in-world date vs. narrative position

**They are different properties of different things. They must not share a field.**

| Axis | What it describes | Examples of divergence |
|------|------------------|------------------------|
| `in_world` | When the event occurred in story-world time | Trident: 283 AC |
| `narrative_first` | Where the reader first encounters evidence of the event | Trident: AGOT ch. 3 (Bran's execution scene backstory), not 283 AC |

These diverge maximally for historical events. The Battle of the Trident happened 283 AC but is narrated across all five books as background. Aegon's Conquest is 1-2 AC in-world but first introduced in AGOT. Conversely, a present-tense event like the Red Wedding has near-identical in-world (300 AC) and narrative-first (ASOS ch. 51) values — but that coincidence does not make them the same thing.

The confusion is deepest for query design. A query like "what events did Ned Stark witness?" needs `in_world` to arrange them chronologically in story-world time. A query like "what does the reader know about Robert's Rebellion by the end of AGOT?" needs `narrative_first` — it's a spoiler-gate and a knowledge-horizon question. Merging them into one field forces the caller to pick one interpretation; the graph picks for them and one query type always gives wrong answers.

**The `stage4-edge-temporal-scope.py` script already stamps edges with `(book_order, chapter_number)` — this is `narrative_first` for edges, not for events. The two are not the same thing: an edge's narrative position is when the *relationship* first appears in text; an event's `narrative_first` is when the *event itself* is first evidenced. They tend to correlate but are logically distinct.**

### Precision note

`in_world` values will range from exact ("300 AC, late autumn") to fuzzy ("before the Doom of Valyria"). Do not force them into a numeric index. Use the precision enum to let query code decide whether to trust the ordering.

`narrative_first` values are more deterministic — they can usually be bootstrapped from the lowest `(book_order, chapter_number)` among all edges that cite the event as their target.

---

## 3. How does dating interact with the causal-edge gap?

**Dating makes PRECEDES/FOLLOWS cheap and automatic. It does not substitute for TRIGGERS/CAUSES — it complements them by doing the chronology work that TRIGGERS should never be doing in the first place.**

The critical distinction:

- **Chronology** says A came before B. Cheap, mostly deterministic, derivable from `in_world`.
- **Causation** says A brought about B. Requires asserted narrative intent. Never derivable from dates alone.

The Trident (283 AC) precedes the Sack of King's Landing (283 AC, weeks later). That ordering is chronology. But the Trident *caused* the Sack — Rhaegar's death broke the royalist army, Aerys panicked, Tywin took his opportunity — and that causal chain cannot be read off dates. TRIGGERS needs to be minted by a human or an agent that reads the narrative.

**Three practical implications:**

1. Dating event nodes first means you can auto-generate PRECEDES edges via script, which removes the busywork from the TRIGGERS pass. The agent or human doing TRIGGERS can focus entirely on asserting causation rather than also working out sequencing.

2. Chronology ≠ causation also means PRECEDES alone is insufficient for questions like "what caused Robert's Rebellion?" Those queries require TRIGGERS/CAUSES chains. PRECEDES would return every event that predates it in Westeros, most of which are unrelated.

3. For historical events (pre-series), `in_world` dating is the only temporal anchor available — there are no `evidence_chapter` citations for an event happening 170 years before AGOT. Dating is therefore MORE valuable for historical hubs than for in-narrative events, which already have chapter-level evidence in their role edges.

**The causal gap is real and dates don't close it. They reduce the mechanical cost of the TRIGGERS pass, not the conceptual cost.**

---

## 4. Sequencing: ranked next-tracks

**Rank: (a) Date events → (c) ATTENDS coverage → (b) Mint TRIGGERS/CAUSES → (d) Narrative-arc reification.**

### Track (a): Date events — DO FIRST

**Why first:** Dating is the cheapest transformation with the highest downstream leverage. It is largely deterministic: wiki pages often carry explicit dates in their body prose; the local wiki cache at `sources/wiki/_raw/` is already available. A script can parse AC/BC years from the ## Origins and ## Aftermath sections of event node bodies and populate `in_world` fields for ~60-70% of nodes without an LLM. The remainder can be a small Haiku pass or a curation queue. Output: `narrative_first` can be bootstrapped mechanically from the lowest `(book_order, chapter_number)` pair in edges that point at each event.

Dating also unblocks auto-generation of PRECEDES/FOLLOWS, making the TRIGGERS pass cheaper. No downstream track is blocked by (a).

**Effort:** Low-to-medium. Mostly Python + a small cleanup pass.

### Track (c): ATTENDS coverage — DO SECOND

**Why second:** ATTENDS is already in the vocab and already partially populated (986 instances). It is a simpler edge than TRIGGERS — it asserts presence, not causation, so it does not require narrative reasoning. It is also query-critical: "who attended the Tourney at Harrenhal?" is a question the graph should answer cleanly. Coverage gaps here affect GRRM's most plot-pivotal set-piece scenes (tournaments, feasts, weddings). Unlike TRIGGERS, ATTENDS has deterministic sources: infobox `attends` fields, Pass 1 "Characters Present" section, and wiki ## Narrative Arc sections. A Python pipeline using the existing wiki cache can fill a large fraction of these.

**Effort:** Low-to-medium. Infobox merge track (already greenlit, dry-run done) will inject many GUEST_OF / ATTENDS instances as a side effect — check infobox merge completion state before launching a separate ATTENDS pass.

### Track (b): Mint TRIGGERS/CAUSES edges — DO THIRD

**Why third, not second:** Causal edges require narrative judgment. Unlike dating or ATTENDS, you cannot derive TRIGGERS mechanically from Pass 1 extractions or wiki infoboxes — it requires reading the causal chain in prose and asserting it. That cost is real, and the pass benefits from having dates first (so the sequencing work is already done and the agent focuses on causation) and from ATTENDS coverage (so the event nodes have richer participant context that helps the agent reason about who caused what).

The priority sub-list within this track:
1. Historical event hubs (Robert's Rebellion chain: Tourney at Harrenhal → Rhaegar crowns Lyanna → Lyanna abduction → Robert's Rebellion → Battle of the Trident → Sack of King's Landing → Tower of Joy → Robert's reign). These have zero causal edges today but form the single most-queried backstory chain.
2. War of the Five Kings chain.
3. Everything else.

**Effort:** High. Requires human curation or a carefully gated LLM pass with drift detection.

### Track (d): Narrative-arc reification — DEFER

**Why last:** Narrative arcs (conspiracy parent hubs over clusters of events) are a higher-order abstraction on top of the event layer. They become genuinely useful only when the events they aggregate are (a) dated, (b) richly populated with ATTENDS edges (so you know who was present in the arc), and (c) causally linked (so the arc has internal structure). Building arc hubs over events that lack dates, sparse ATTENDS, and no causal edges creates structure without content.

The prior de-prioritizations were correct for this reason: the pattern works, but the substrate isn't ready. Come back to this after (a), (c), and a first wave of (b) are done.

---

## Schema Summary

### Event node frontmatter additions

```yaml
occurred:
  in_world: "283 AC"
  in_world_precision: year    # year | decade | era | approximate | contested
  narrative_first: "agot-3"   # {book}-{chapter_number} of earliest reader encounter
```

### Edge types (all already in vocab — no new vocab additions needed)

| Type | Direction | How to populate | Notes |
|------|-----------|-----------------|-------|
| `PRECEDES` | Earlier event → Later event | Auto-generate from `in_world` via Python | Only emit when dates are known and precision allows; skip same-date events |
| `CAUSES` | Cause event → Effect event | Human curation or gated LLM | Broad causal chain (weeks/months) |
| `TRIGGERS` | Spark event → Result event | Human curation or gated LLM | Immediate spark (days/hours) |
| `ATTENDS` | Person → Event | Infobox merge + Pass 1 characters-present | Already partially populated |

### What is NOT recommended

- `OCCURRED_IN_YEAR` edges: no year nodes exist; creates dangling typed scalars
- Single merged field for in-world date + narrative position: they diverge maximally for historical events, breaking half of query types
- PRECEDES as a substitute for TRIGGERS: chronology ≠ causation

---

## Three-Sentence Recommendation

Date event nodes first — it is the cheapest intervention, largely Python-scriptable from the local wiki cache, and it unblocks automated PRECEDES generation that makes the later TRIGGERS pass cheaper and more focused. Follow with ATTENDS coverage, which leverages the already-greenlit infobox merge track and requires no narrative reasoning, giving the event layer its first real participant-attendance completeness. Only then invest in TRIGGERS/CAUSES, where the effort is genuinely high and benefits from both prior tracks being complete; narrative-arc reification stays deferred until events have dates, ATTENDS edges, and at least one wave of causal chains, because arc hubs aggregating sparse events produce structure without searchable content.
