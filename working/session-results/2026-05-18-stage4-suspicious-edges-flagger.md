# Stage 4 Suspicious-Edges Flagger — Session Results
Date: 2026-05-18
Script: `scripts/wiki-pass2-flag-suspicious-edges.py`
Output: `working/wiki/data/stage4-suspicious-edges.jsonl`

---

## 6 Pattern Definitions

| # | Flag Reason | Logic |
|---|-------------|-------|
| 1 | `knows_as_fallback` | `edge_type == KNOWS` AND `evidence_snippet` contains no knowing-verb (knew/knows/know/known/knowing/informed/told/acquainted/aware of/recognized/met/heard of/discovered) |
| 2 | `attends_non_event` | `edge_type == ATTENDS` AND `target_type` does not start with `event` |
| 3 | `fights_in_non_event` | `edge_type == FIGHTS_IN` AND `target_type` does not start with `event` |
| 4 | `killed_by_non_person` | `edge_type == KILLED_BY` AND `source_type` is not `character.*`, `creature.*`, or `object.artifact` |
| 5 | `tier3_weak_evidence` | `confidence_tier == 3` AND `evidence_snippet.strip()` is shorter than 20 characters |
| 6 | `contemporary_with_char_pair` | `edge_type == CONTEMPORARY_WITH` AND both source AND target resolve to `character.*` in the slug index |

Type resolution uses the `graph/nodes/` directory structure (8,050 slugs indexed).
Schema variance handled: old batches use `source`/`target`/`confidence: "tier-N"` fields; new batches use `source_slug`/`target_slug`/`confidence_tier: N`. Both are normalized before checking.

---

## Run Statistics (Full — 72 done batches)

| Metric | Value |
|--------|-------|
| Batches scanned (done) | 72 |
| Output files found | 885 |
| Total rows scanned | 14,296 |
| emit_edge rows | 4,075 |
| Flagged edges | 288 |
| Flag rate (% of emits) | 7.1% |

---

## Flagged Edge Counts Per Pattern

| Pattern | Count | Notes |
|---------|-------|-------|
| `knows_as_fallback` | 163 | 82.3% of all 198 KNOWS emits lack knowing-verb in snippet |
| `contemporary_with_char_pair` | 73 | All character-to-character CONTEMPORARY_WITH edges |
| `attends_non_event` | 30 | Mostly ATTENDS targeting a character (wedding attendee listed with person, not event) |
| `fights_in_non_event` | 19 | FIGHTS_IN targeting character (15), concept (3), or other (1) |
| `tier3_weak_evidence` | 3 | All have empty or near-empty snippets |
| `killed_by_non_person` | 0 | No violations found in 72 batches |

---

## Top 5 Most-Flagged Batches

| Batch | Flagged Edges | Primary Pattern |
|-------|---------------|-----------------|
| batch-0020 | 153 | knows_as_fallback (140) — Frey character cluster |
| batch-0003 | 26 | contemporary_with_char_pair (22) — Beesbury/Blackfyre cluster |
| batch-0018 | 21 | knows_as_fallback (15), attends_non_event (6) |
| batch-0014 | 18 | attends_non_event (10), knows_as_fallback (8) |
| batch-0002 | 14 | contemporary_with_char_pair (13) — Baratheon of Dragonstone cluster |

---

## Sample Flagged Edges With Reasoning

### `knows_as_fallback` — batch-0020, Frey characters

```
walda-frey-daughter-of-merrett --KNOWS--> arya-stark
  snippet: "Roose allows his cupbearer 'Nan', actually an incognito Arya..."
  reasoning: snippet establishes presence/proximity, no "knew/knows/told" verb.
             KNOWS is the classifier's fallback when co-presence implied awareness.
```

```
petyr-baelish --KNOWS--> jeyne-poole  (batch-0001)
  snippet: [empty]
  reasoning: No snippet at all — classic null-evidence KNOWS emit.
```

### `contemporary_with_char_pair` — batch-0002, Dragonstone cluster

```
pylos --CONTEMPORARY_WITH--> melisandre
  snippet: "Cressen tries to kill [LINK] with the strangler..."
  reasoning: Both are characters. CONTEMPORARY_WITH is the session-54 soft-fallback
             when classifier couldn't determine direction or find a more specific
             edge. The actual relationship here is likely KNOWS or CONTEMPORARY_WITH
             which is technically valid but semantically vague.
```

### `attends_non_event` — batch-0014, tournament/wedding targets

```
ashara-dayne --ATTENDS--> barristan-selmy  (tier=2)
  snippet: "Ser Barristan Selmy recalls the tourney at Harrenhal..."
  reasoning: Target is a character (Barristan), not an event. The real target should
             be the Tourney at Harrenhal. Classifier attached the edge to the person
             mentioned in the same sentence as the tourney.
```

### `fights_in_non_event` — batch-0001 / batch-0003

```
aegon-ambrose --FIGHTS_IN--> trial-of-seven  (tier=1)
  reasoning: trial-of-seven is in graph/nodes/concepts/ (not events/). A real
             "trial by the Seven" is an event; the generic concept node is not.
             Could argue: FIGHTS_IN a concept is valid if no specific event node
             exists. Flag for review.

alan-beesbury --FIGHTS_IN--> daeron-targaryen-son-of-viserys-i  (tier=1)
  snippet: "Prince Daeron Targaryen joined the Battle on the Honeywine..."
  reasoning: Target is a character, not a battle. Classifier should have used the
             Battle on the Honeywine as the target.
```

---

## Open Questions for Opus Review

1. **KNOWS fallback concentration in batch-0020**: 140 of 163 KNOWS fallbacks come from a single batch (Frey characters). This suggests a systemic classifier drift on that bucket — the Frey characters are all co-present at Harrenhall/Red Wedding/Winterfell, and the classifier defaulted to KNOWS for every co-presence. Worth a focused Opus audit on that single batch.

2. **CONTEMPORARY_WITH legitimacy**: Some CONTEMPORARY_WITH on character pairs may be intentional (when the only evidence is that two characters lived in the same era without a specific interaction). The audit should distinguish: (a) CONTEMPORARY_WITH with no better alternative vs. (b) CONTEMPORARY_WITH where a more specific edge clearly applies.

3. **trial-of-seven (concept vs event)**: Multiple FIGHTS_IN edges target this concept node. The correct fix may be: create an event node for the specific Maegor-era Trial of Seven, or accept FIGHTS_IN-concept as a "participates in a ritualized combat form" pattern.

4. **attends_non_event targeting persons**: These are mostly cases where the classifier saw "X attended Y's wedding" and emitted ATTENDS with target=Y (person) instead of ATTENDS with target=wedding-of-Y (event). Pattern is consistent — audit can apply a heuristic fix.

5. **`killed_by_non_person` — zero hits**: Surprisingly, no KILLED_BY violations found across 72 batches. Either the classifier respected this contract well, or KILLED_BY isn't being emitted for non-obvious killer types yet. Will re-check when more batches complete.
