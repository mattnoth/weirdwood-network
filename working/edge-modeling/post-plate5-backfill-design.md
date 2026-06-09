# Post-Plate-5 Edge Backfill — Design

> **Status:** DESIGN — captured 2026-06-08 (Session 86, end-of-session fork). NOT for execution until Plate 5 lands. Three discrete backfill tracks, each independently shippable.
>
> **Why this exists:** The Plate 0-5 reification work focused on EVENT modeling — minting event hubs, role-edge reification, schema fixes on event nodes. Some of that work is retroactively applied to existing edges at Plate 5 (~50 edges). But the edge-modeling lessons (head rule, reification thinking, vocab expansion) generalize beyond the ~50 already-queued edges. This memo captures the rest — work that **should** be applied to the existing 3,811-edge graph, sequenced after Plate 5 lands so the graph layer stabilizes before being retouched.
>
> **Resolved during S86 conversation:** S74 was NOT a permanent "no LLM enrichment" ban — I framed it that way and Matt corrected me. S74's actual decision was narrower: the specific Events+Dialogue Haiku enrichment that ran came in at 74.5%/62.5% precision, below the 75% gate, so THAT specific run was shelved. **S75 explicitly amended:** "enrichment is DEFERRED, not abandoned — Events is the next surface, gated behind precision changes landing first." The standing rule is: any LLM enrichment passes the precision gate before it ships. Backfill work in this memo is subject to the same gate, not exempt from it.
>
> Backfill differs from enrichment in scope (retype existing edges with already-verified evidence vs. emit new edges in uncertain territory) — which tends to make the precision-gate math easier — but it doesn't escape the gate.

---

## Track A — Vocab-drift retype (Phase 1 deterministic + Phase 2 Haiku fallback)

**Problem:** The existing 3,811 edges were emitted under older vocabulary. Several newer types were added since (S55 second wave, S58, S61, S83, S86). Existing edges that should now use the more-specific type are stuck with the older/fuzzier type.

**Empirical scope** (S86 sample scan of `edges.jsonl`):

| Newer type (added) | Hint-phrase matches in existing edges, currently mistyped as |
|---|---|
| `GUARDS` (S61) | 12+ as PROTECTS / COMMANDS / SWORN_TO / COMPANION_OF / SERVES |
| `SPIES_ON` / `INFORMS` (S58) | small but real — MEMBER_OF / SERVES / ALLIES_WITH / DISTRUSTS |
| `TORTURES` (S58) | ~3+ as ATTACKS / HATES / IMPRISONS |
| `RESCUES` (S58) | 6+ as LOVES / PROTECTS / TRUSTS / COMPANION_OF |
| `IMPRISONED_AT` (S61) | ~3+ as LOCATED_AT / COMPANION_OF |
| `TRAVELS_WITH` (S61) | unknown — needs scan |
| `ENCOUNTERS` (S61) | gate violations under FEARS / LOVER_OF |
| `PRISONER_EXCHANGE_FOR` (S61) | unknown — needs scan |
| `AFFLICTED_BY` / `DIED_OF` (S55) | likely emitted as KILLED_BY against the disease |
| `STEP_PARENT_OF` / `STEP_CHILD_OF` / `IN_LAW_OF` (S58) | likely emitted as PARENT_OF / SIBLING_OF |
| `COUSIN_OF` / `UNCLE_OF` / `MILK_BROTHER_OF` (S55) | likely emitted as SIBLING_OF |
| `OFFICIATES` (S55) | likely emitted as ATTENDS / CLERGY_OF |
| `KNIGHTED_BY` / `BESTOWS_KNIGHTHOOD_ON` (S55) | likely TUTORS / APPOINTS |
| `BUILT` (S55) | likely FOUNDED / OWNS |

Floor estimate: **100-200+ deterministic retype candidates** across the full vocab-drift set.

### Phase 1 — deterministic dictionary sweep ($0)

Build `scripts/edge-vocab-drift-retype.py` consuming a dictionary structured as:

```python
VOCAB_DRIFT = {
    'GUARDS': {
        'trigger_phrases': ['guard', 'watch over', 'keep watch', 'hold captive', 'gaoler', 'jailer'],
        'safe_to_retype_from': ['PROTECTS', 'COMMANDS', 'SWORN_TO', 'COMPANION_OF', 'SERVES'],
        'endpoint_contract': '(character, character)',
    },
    'SPIES_ON': {
        'trigger_phrases': ['spies on', 'spy on', 'eavesdrop', 'little birds', 'whisperer'],
        'safe_to_retype_from': ['MEMBER_OF', 'SERVES', 'ALLIES_WITH', 'DISTRUSTS'],
        'endpoint_contract': '(character, character)',
    },
    # ... 10-12 more entries, one per post-S55 newer type
}
```

For each edge: if `current_type IN safe_to_retype_from[new_type]` AND `hint_raw OR asserted_relation` matches a `trigger_phrase` AND `endpoint_contract` passes → stage a retype. Write to `working/edge-modeling/post-plate5/vocab-drift-track-a-phase1.jsonl` for Matt review.

**Gate before apply:** spot-check ~30 random staged retypes; if ≥90% are clean, apply at next merge. (Distinct from Plate 5 — its own gated mini-merge.)

Cost: $0. Estimated yield: 100-200 retypes.

### Phase 2 — Haiku fallback for ambiguous rows (~$5-15)

For rows where:
- Multiple new types could fit (e.g., a hint matching both `GUARDS` and `IMPRISONS`), OR
- The hint is too vague for deterministic matching (e.g., "kept her safe" — could be GUARDS or PROTECTS), OR
- The endpoint contract is borderline (e.g., target node is a person who is ALSO a faction's leader)

→ Haiku reads the row's evidence_quote + endpoint context, picks the more-specific type from a constrained menu, or returns NO_RETYPE if no new type fits cleanly. Strictly retype-only, no new emissions.

**Gate:** standard cross-model audit if precision questionable. Bulk run with sleep-between rate-limit safety.

Cost: bounded by row count × ~$0.001-0.003 per Haiku call. Estimated <$15.

### Track A total: $0-15, deterministic-first, low-risk.

---

## Track B — Reification of existing edges into event hubs

**Problem:** Existing person↔person edges anchored to a named event (Red Wedding, Tower of Joy, Sack of King's Landing, Purple Wedding, etc.) sit as scattered binary edges. The event hub model (Plates 2-4) says these should be reified: `AGENT_IN`/`VICTIM_IN`/`COMMANDS_IN`/`WIELDED_IN` on the event node, with the binary person↔person edge marked `superseded_by: <hub-slug>` (not deleted — CLAUDE.md source-data rule).

**Cleanroom-identified eligible families** (S82, recorded in `working/edge-modeling/edge-modeling-reification-design.md`):

1. **Killings-at-named-occasion** — existing KILLS / POISONS / EXECUTES person→person edges where the act occurred at a named event. Examples: every Red Wedding kill, the Purple Wedding poisoning, every Tower-of-Joy combat death.
2. **Sieges** — scattered FIGHTS_IN / COMMANDS / PRISONER_OF / ATTACKS / BESIEGES around named sieges. Example: Siege of Storm's End, Siege of Riverrun, Siege of Meereen.
3. **Wedding / tourney ceremonies** — scattered ATTENDS / FIGHTS_IN / CROWNS_QUEEN_OF_LOVE_AND_BEAUTY / DUELS around named ceremonies. Example: Tourney at Harrenhal (Rhaegar crowns Lyanna), the Wedding of Joffrey and Margaery (Tyrell-Lannister combine).
4. **Conspiracies** — scattered ALLIES_WITH / NEGOTIATES_WITH / CONSPIRES_WITH for named plots. Examples: Grand Northern Conspiracy, Queenmaker plot, Faith Militant uprising, Joffrey-poisoning Tyrell-Lannister cabal.
5. **VIOLATES_GUEST_RIGHT** — scattered host↔guest hostility edges around named hospitality violations. Examples: Red Wedding, the Sack of Saltpans, Stannis at the Wall (offering bread-and-salt to wildlings).

**Why this is bigger than vocab-drift:** the existing graph has 404 GUEST_OF edges alone, and the deterministic Pass-1 pipeline targeted character-relationship extraction without event-hub awareness. Conservative estimate: **500-1,500 existing edges are reification candidates** across the five families.

### Phase 1 — deterministic anchor-match

For each event-node (post-Plate-5; that's why this comes after Plate 5), build a {participant_slug, role_hint} expectation from its wiki infobox + Plate-3 mint metadata. Walk `edges.jsonl` for person↔person edges where:
- Both endpoints appear in the event's expected participant set, AND
- The edge's chapter-evidence aligns temporally with the event, AND
- The edge type is in the reification-eligible vocabulary above.

High-confidence matches → emit role edges (AGENT_IN/VICTIM_IN/COMMANDS_IN), mark original `superseded_by`.

Cost: $0. Estimated yield: 200-600 reifications (the deterministic high-confidence subset).

### Phase 2 — Haiku review of borderline rows

For matches where (a) the role is ambiguous (which participant is agent vs. patient?), (b) the chapter alignment is loose, or (c) the participant set is partial — Haiku reads the evidence quote + parent-event description + candidate roles, picks AGENT_IN / VICTIM_IN / COMMANDS_IN / DECLINES_ROLE.

Cost: bounded by row count × Haiku rate. Probably $20-50 for the full borderline tail.

### Track B total: $20-50, mixed deterministic + LLM, medium-risk because it touches 500-1,500 edges.

**Critical preconditions for Track B:**
- Plate 5 must have landed (event hubs need to exist in `graph/nodes/events/`).
- The 219 Plate-3 mints need to be in-graph so they're matchable against Pass-1 chapter evidence.
- An audit-loop pass (Reporter + Auditor) BEFORE bulk Track B execution.

---

## Track C — Head-rule retroactive cleanup beyond Plate 0's 10 flips

**Problem:** Plate 0's normalizer caught **explicit** direction inversions where the relationship type's reverse-signal lexicon matched (e.g., "X is killed by Y" emitted as KILLS source=X). The Plate 1 head rule (S83) is broader: "Column A = semantic agent, never grammatical subject, never POV." Subtler direction errors than Plate 0's lexicon caught are likely still in the graph.

**Symptom signals:**
- Edges where the POV character is also the source on a state-receiving edge (PRISONER_OF, BETRAYS, etc.) — but the POV might be the patient, not the agent.
- Edges where the grammatical subject of the source sentence is the patient (passive constructions, "X was given Y's protection" → emits PROTECTS source=X-of-Y? wrong direction).
- Edges in Pass 1 emitted off the `## Relationships Observed` table where the table's Column A was filled by ergonomic ordering rather than semantic ordering.

### Phase 1 — extended normalizer

Extend Plate 0's reverse-signal lexicon to cover more verb patterns per edge type. Plate 0 currently has ~20-30 signal phrases; broaden to ~100+. Run the extended normalizer on the full 3,811-edge graph (post-Plate-5 — the merged graph, not the pre-merge). Stage flips for review.

Cost: $0. Estimated yield: 5-30 additional direction flips.

### Phase 2 — sample-and-review (no bulk LLM)

Take a stratified sample of edges by type — particularly the high-frequency types (GUEST_OF 404, SERVES 255, OPPOSES 265, COMMANDS 171). Hand-review or Haiku-review the sample for direction errors. If error rate <2%, accept; if higher, expand to bulk Haiku.

Cost: $0-10.

### Track C total: $0-10, low-risk because it only flips direction, doesn't change type.

---

## Plus — Future passes fold in edge-modeling lessons (forward-only, NOT backfill)

This isn't backfill, but it's the same conversation. Any future Pass-2+ work or Stage-4 retread should bake in:

1. **The Plate 1 head rule** — semantic agent, never grammatical subject, never POV. Already in `.claude/agents/mechanical-extractor.md` line 188. Should also be added to any Dialogue-tail prompt, any Pass-3 voice/perception prompt, any cross-identity-detector prompt that emits edges.
2. **Reification thinking** — when a candidate edge is anchored to a named event, prefer emitting against the event hub (AGENT_IN / VICTIM_IN / etc.) over emitting a person↔person binary. This affects the Dialogue v2.1 pipeline (currently halted at S81 NO-GO) — its REVEALS_TO emits, for instance, should distinguish "X reveals to Y privately" (binary) from "X reveals to Y during the Small Council meeting" (event-hub anchored).
3. **Post-S86 vocab** — `SUB_BEAT_OF`, `AGENT_IN`, `VICTIM_IN`, plus the 7 new event sub-types. Available to any future emitter.
4. **The substitution test for aliases vs sub-beats** (S86, `reference/alias-resolver-design.md`) — applies to any future entity-merger / disambiguation / cross-identity work that touches event-naming.

Adds a single TODO: "fold edge-modeling lessons into Dialogue v2.1 escalation pick + Pass 3 design + any future Stage 4 retread."

---

## Sequencing recommendation

```
Plate 5 lands (Opus session, first plate to write to canonical edges.jsonl)
         ↓
Track A Phase 1 (deterministic dictionary, $0, ~100-200 retypes)
         ↓
Track A Phase 2 (Haiku fallback, ~$5-15)
         ↓
Track C Phase 1 (extended normalizer, $0, ~5-30 flips)
         ↓
Track B Phase 1 (deterministic event-anchor match, $0, ~200-600 reifications)
         ↓
Audit-loop checkpoint — Reporter + Auditor verdict
         ↓
Track B Phase 2 (Haiku borderline review, ~$20-50)
         ↓
[Optional] Track C Phase 2 (sample-and-review, $0-10)
         ↓
Final graph state: ~5,000-6,000 edges, fully reified event hubs, vocab-current
         ↓
Dialogue v2.1 escalation pick (informed by edge-modeling lessons)
```

**Rationale for ordering:**
- Track A first because it's smallest, cheapest, lowest-risk, and shake out the post-Plate-5 graph for any unexpected state.
- Track C second because it's still deterministic and small — verifies direction-correctness before bigger touches.
- Track B last because it's the biggest scope and has the most precondition dependencies (event hubs must be in-graph, mints must be merged, schema must be settled).

**Each track has its own gate.** No Plate-5-style "one big merge" — these are independent passes, each with backup + before/after diff + Matt sign-off.

---

## Decisions captured

- **S74 was a precision-gate failure on a specific run, NOT a permanent LLM-enrichment ban.** Per S75 amendment, enrichment is wanted, gated on precision. All Track A/B/C LLM-touching phases must pass the same precision gate before they ship — same standard as any other enrichment.
- **Plate 5 stays as scoped.** ~50 retroactive cleanups (Plate 0 flips, Aerys merge, S77 cleanups, 27 schema fixes). The backfill work is NOT folded in; it's post-Plate-5.
- **Pass 1 chapter re-extraction is OFF the table** (matches your message). Backfill operates on the graph, not on the chapter prose.
- **Three tracks are independently shippable.** Tracks A and C can ship even if Track B is later deferred.

---

## Cost summary

| Track | Phase | Cost | Yield (estimate) | Risk |
|---|---|---|---|---|
| A | 1 deterministic | $0 | 100-200 retypes | low |
| A | 2 Haiku fallback | <$15 | tail | low |
| C | 1 extended normalizer | $0 | 5-30 flips | low |
| B | 1 deterministic anchor-match | $0 | 200-600 reifications | medium |
| B | 2 Haiku borderline | $20-50 | tail | medium |
| C | 2 sample-and-review | $0-10 | precision check | low |
| **Total** | | **$25-75** | **~300-850 edges touched** | |

For comparison, Plate 5 itself touches ~50 retroactive edges. Post-Plate-5 backfill is 6-17× the retroactive scope of Plate 5 — and at <$100 total.

---

## Cross-references

- `working/edge-modeling/edge-modeling-reification-design.md` — original design doc; §3 D3 + cleanroom analysis identify the reification-eligible families.
- `working/edge-modeling/SESSION-LOG.md` — Plate-by-plate history; cleanroom analysis lives in S82 entry.
- `reference/alias-resolver-design.md` — S86 design memo (alias/display + 4 fixes); the substitution test from there applies to any future entity-naming work.
- `reference/architecture.md` — current vocab (166 types as of S86); the dictionary in Track A keys off newer vs older types.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` — must run first (this memo is post-Plate-5).
- S74 worklog entry — the specific Events+Dialogue Haiku run that failed the 75% gate; S75 worklog entry — amendment confirming enrichment is wanted, gated on precision. Both apply to LLM-touching backfill phases here.
