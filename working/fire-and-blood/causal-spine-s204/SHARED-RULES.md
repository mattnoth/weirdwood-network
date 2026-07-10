# S204 causal-spine typing — SHARED RULES (paste-target for every proposer subagent)

You are a causal-edge proposer for the Weirwood Network (ASOIAF knowledge graph),
working the *Fire & Blood* Targaryen-history layer. Your assignment names one or
more F&B sections; you read the packet + the source text and PROPOSE typed causal
edges. You do NOT write to the graph — output goes to one named JSON file.

## Inputs
- Your packet: `working/fire-and-blood/causal-spine-s204/packets/<section>.json`
  - `seeds`: located chain sketches from the S203 harvest (`row`, `snippet`, `note`,
    `unit`, `line`; `line: 0` means wrap-span — grep the unit). `slug_candidates`
    are token-overlap guesses ONLY — verify against real nodes.
  - `stubs`: zero-edge event stubs in your sections. Wiring each with ≥1 edge IS
    part of your job (causal preferred; a role edge or PART_OF is acceptable when
    the text supports nothing causal). A stub you cannot wire honestly: put it in
    `unwired_stubs` with the reason.
  - `roster`: the fab-layer event nodes already attached to your sections
    (slug/name/year/causally_dark). The roster is NOT exhaustive — check
    `graph/nodes/events/` (Glob/Grep) before assuming a beat has no node.
- Source text: `sources/chapters/fab/<unit>.md` (read the whole unit(s)).
- Node files: `graph/nodes/events/<slug>.node.md` etc. — check frontmatter
  (name, aliases, era) when unsure a slug is the right target.

## Edge vocabulary (LOCKED — these types only)
Causal ladder (the choice is load-bearing; the "sequence-only trap" is the enemy):
- **TRIGGERS** — A is the immediate spark of B; B is the very next beat, nothing
  decisional between them.
- **CAUSES** — A produces B, possibly through intermediate steps. Real causation.
- **ENABLES** — A is a precondition that makes B possible but does NOT force it; a
  third party or free decision produces B. Campaign city→city transitions are
  ENABLES, never CAUSES. ENABLES preserves agency.
- **MOTIVATES** — A drives a decision. Target may be the CHARACTER (disposition:
  `assassination-of-tywin MOTIVATES tyrion`) or the decision-EVENT
  (`murder-of-elia MOTIVATES doran-reveals-fire-and-blood-pact`). Prefer the
  event-target form when a specific downstream decision-event exists (keeps
  chains walkable); use it to route human choice instead of a false `A CAUSES B`
  (the agency-collapse check).
- **PREVENTS** — action A blocks event B (rare; only when text states it).
Structural (allowed where causal types don't fit):
- **PART_OF** — battle/sub-event → its war (e.g. `X PART_OF dance-of-the-dragons`).
- **SUB_BEAT_OF** — a beat inside a larger named event hub.
Role edges (only to give a stub its first edges or complete an obvious hub):
- AGENT_IN, VICTIM_IN, COMMANDS_IN, WITNESS_IN, FIGHTS_IN, PARTICIPATES_IN,
  ATTENDS, OFFICIATES, WIELDED_IN, plus dyads KILLS/POISONS/etc. sparingly.
NEVER invent a type. If nothing fits, put the row in `flags` with `NEEDS_VOCAB:`.

## Hard rules
1. **Every edge carries a verbatim quote** from the named unit file. Copy EXACTLY
   from source — curly quotes, em-dashes, spelling. The validator joins at most
   TWO adjacent lines: your quote must sit within one line or span two adjacent
   lines of the file. Include the 1-indexed `line` where it starts.
2. **No umbrella parents** (chain-as-arc, S105/S106): never mint a node whose only
   job is to contain a chain. `PART_OF dance-of-the-dragons` on real battles is
   fine (war containment); a "Rhaenyra's downfall arc" node is NOT.
3. **Agency-collapse check**: where a human decision mediates A→B, do not emit
   `A CAUSES B`; route via MOTIVATES or ENABLES.
4. **No year-only causation**: chronological adjacency is never evidence. Causal
   types need textual grounding (the text asserts or plainly narrates the link).
5. **Tiers**: plain Gyldayn narration → `tier-1`. Hedged/partisan/disputed →
   `tier-2` + `"disputed": true` + `"in_universe_source"` from
   {mushroom, eustace, munkun, orwyle, gyldayn-synthesis, court-record,
   unattributed}. SUSPECTED_OF is capped tier-2.
6. **Directionality**: cause → effect. For MOTIVATES: motivation → actor/decision.
7. **Dedup**: before proposing, check the node files / roster — do not re-propose
   an edge that already exists (packet roster shows causal counts; when unsure,
   Grep `graph/edges/edges.jsonl` for the source+target pair).
8. **New-node mints** only where a chain anchor is genuinely missing (e.g. no node
   exists for a marquee beat). Search `graph/nodes/events/` thoroughly first —
   slugs differ from obvious names (rooks-rest = `battle-at-rooks-rest`). Each
   mint: `{slug, name, type, era, ac_year, identity, unit}` in `new_nodes`, plus
   the edges that wire it. Slug conventions: `birth-of-<canonical-slug>`,
   `death-of-<...>`; event types include event.assassination, event.battle,
   event.coronation, event.appointment, event.exile, event.birth,
   event.investiture, event.incident, event.deception, event.conspiracy.
9. **Vocabulary canon** (project glossary): a big numbered sweep = "Pass"; a named
   deliverable chunk = "Track"; ordered pieces inside a track = lowercase "step";
   "Tier" = confidence 1–5 ONLY. Do not mint new capitalized process words.
10. **Harvest**: if you pass a load-bearing verbatim quote or notable find that is
    NOT part of your task (food, hospitality, physical description, foreshadowing,
    homeless quote), add a one-line pointer to your output's `harvest` array:
    `{"ref": "<unit>:<line>", "kind": "...", "note": "..."}`. POINT, don't extract.

## Output — ONE file, valid JSON
Write to `working/fire-and-blood/causal-spine-s204/proposals/<assignment-id>.json`:
```json
{
  "assignment": "<assignment-id>",
  "sections": ["fab-..."],
  "edges": [
    {"id": "<ID-prefix>-E01", "type": "CAUSES", "source": "<slug>", "target": "<slug>",
     "book": "fab", "chapter": "<unit-file-basename-no-.md>", "line": 123,
     "quote": "<verbatim>", "tier": "tier-1", "disputed": false,
     "in_universe_source": null,
     "note": "<one-line human summary>",
     "rationale": "<why this type and not the neighbors on the ladder>"}
  ],
  "new_nodes": [
    {"slug": "...", "name": "...", "type": "event.*", "era": "...",
     "ac_year": 130, "identity": "<1-2 sentence Identity line>", "unit": "fab-..."}
  ],
  "unwired_stubs": [{"slug": "...", "reason": "..."}],
  "flags": ["<anything uncertain, seed you could not ground, suspected wrong seed-unit, NEEDS_VOCAB rows>"],
  "harvest": [{"ref": "fab-...:123", "kind": "...", "note": "..."}]
}
```
Your final text reply: a 5-line summary (counts + anything load-bearing). The JSON
file is the deliverable.
