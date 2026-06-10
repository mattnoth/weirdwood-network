# Continue — Use the graph for validation (post-Plate-5)

> **Recommended model:** Opus 4.7 — this is exploratory/scoping work over a freshly merged graph, with downstream design implications for agent-grounding. The actual query execution is `graph-query.py` (deterministic). Reasoning depth + judgment is in interpreting results, not in running queries.
>
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9). Plate 5 shipped 2026-06-09 (S87, commit `435330d69`); `edges.jsonl` is at 4,757 rows, `events/` at 583 nodes. The merge is irreversible-without-backup (backup: `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`).

## Context — what S87 unlocked

Plate 5 was the gated write that turned the reification design into a live graph capability. The graph can now answer questions it structurally couldn't answer before:
- **Participant queries on events.** AGENT_IN / VICTIM_IN / COMMANDS_IN / WIELDED_IN / ATTENDS role edges hang off event hubs. "Who participated in the Red Wedding" is now a graph query, not a chapter re-read.
- **Beat-level temporal queries.** 51 SUB_BEAT_OF edges connect chapter-beat mints to their parent canonical event (e.g. `lord-walder-calls-for-the-bedding` SUB_BEAT_OF `red-wedding`). Combined with S76 temporal-scoping (every edge carries `evidence_book`+`evidence_chapter`+chapter line), beats can be traversed in temporal order within a parent event.
- **Cross-character traversal via event hubs.** Person → event → person is the new connectivity pattern. Tywin → COMMANDS_IN → red-wedding → AGENT_IN → walder-frey is a 2-hop traversal that didn't exist pre-Plate-5 (the spine had only person↔person dyads).

Matt's stated next track (end of S87): "actually using the graph to do some validation. With 4,757 edges + 583 event nodes + reified hubs + role-typed participants + SUB_BEAT_OF traversal, the graph can now answer questions it couldn't before — e.g., 'who participated in event X,' 'who ordered whom to do what at the Red Wedding,' 'what beats happened before the slaughter,' cross-character traversals via event hubs. Worth scoping which validation questions matter most to you so we pick the right query patterns."

## Four validation modes (pick where to start)

The S87 wrap-up conversation surfaced four distinct senses of "validate the graph":

### Mode 1 — Capability validation (does the new structure work?)
Cheapest. Pick 5-10 queries the reification design was specifically built to enable, run them, see what comes back. Misses feed the 6 follow-up TODOs with specific symptoms.

Suggested probe list:
- Red Wedding: full participant union + sub-beat traversal in chapter order (already partially smoked S87; expand)
- Purple Wedding: AGENT_IN/VICTIM_IN/COMMANDS_IN + ATTENDS list (does the Tyrell-Lannister conspiracy show via COMMANDS_IN?)
- Battle of the Blackwater: combatants + commanders + wielded weapons (does Wildfire show via WIELDED_IN?)
- Execution of Eddard Stark: AGENT_IN (Ilyn Payne), COMMANDS_IN (Joffrey), VICTIM_IN (Eddard), WIELDED_IN (Ice), ATTENDS (Sansa, Arya, others)
- Tourney at Harrenhal: champions, attendees, the Knight of the Laughing Tree thread (does CROWNS_QUEEN_OF_LOVE_AND_BEAUTY survive? does the Rhaegar/Lyanna anchor traverse?)
- "What event connects Tywin and the Mountain" — 2-hop via shared event hubs (Riverlands campaign? sack of King's Landing?)
- "Who ordered the Red Wedding" — COMMANDS_IN ∩ red-wedding (Walder Frey + Roose Bolton + Tywin should all show with different role anchoring)
- "What weapon was used to kill Robb Stark" — WIELDED_IN on the red-wedding hub (does the crossbow / dagger detail survive? probably not — this is a capability-floor probe)

### Mode 2 — Canonical accuracy validation (fact-check vs. books)
Mid-cost. Pick known canon claims + known contested points, ask the graph, compare. The 32 conflict-pair flags from S75 are an existing starting set (mostly temporal arcs, but cersei↔tyrion-class precision residue is real). Partially absorbed by the planned Track A backfill (vocab drift retype) — explicit Mode 2 pass is optional if Mode 1 doesn't surface precision concerns.

### Mode 3 — Agent-grounding validation (the actual project goal)
Highest-value, most expensive to set up. Per the standing project value (`project_real_goal_graph_for_agents`): graph exists so an agent can reason with it. Real validation = "hand an agent `graph-query.py` as a tool + a real ASOIAF question + see if the answer is defensible." Examples:
- "Did Stannis kill Renly?" (modal qualifier on KILLS; needs to surface the shadowbinding mechanism)
- "Who knew about the plan to kill Joffrey?" (CONSPIRES_WITH + REVEALS_TO traversal)
- "What links Tywin to Elia's death?" (COMMANDS_IN on sack-of-kings-landing → AGENT_IN to Gregor → VICTIM_IN to Elia)
- "What is Brienne's vow to Catelyn?" (VOWS_TO + qualifier + chapter anchoring)

Mode 3 mixes three error classes — bad graph, bad query interface, bad agent reasoning. Running Mode 1 first isolates the graph layer.

### Mode 4 — Surprise/discovery validation (what does the graph see?)
Aggregate queries that were embarrassingly hard pre-Plate-5:
- All weddings + who got killed at each
- All executions ordered by Cersei
- All events Tywin commanded but did not personally agent
- Every CROWNS_QUEEN_OF_LOVE_AND_BEAUTY in the series

Not about accuracy — about whether the graph surfaces patterns. Optional / discovery-mode.

## Recommendation

Start Mode 1, 30-60 min: 5-10 probe queries on the suggested list, document each as "expected / actual / delta." The misses cleanly route to one of the 6 post-Plate-5 follow-up TODOs (display bullets, empty-quote SUB_BEAT_OF, hub-review-queue, deferred collisions, mutual-kill reverse, backfill tracks A/B/C).

If Mode 1 lands clean: move to Mode 3 (agent grounding) as the real test. If Mode 1 surfaces precision concerns: detour into Mode 2 (or directly into Track A backfill) before Mode 3.

Mode 4 is for later — discovery is best done with a working query toolchain, which Modes 1+3 force into existence.

## Tools / data inventory

- **Primary query tool:** `scripts/graph-query.py` (S39 + S75 extensions: `--neighbors`, `--path`, `--health`, `--edges`). Reads `graph/edges/edges.jsonl` directly.
- **Conflict pair audit:** `working/wiki/data/graph-conflict-pairs.{md,jsonl}` (32 flags from S75)
- **Temporal-scoped edges:** `working/wiki/data/edges-temporal-scoped.jsonl` (S76 — every edge annotated with book_order + chapter_number)
- **Diff record for Plate 5:** `working/edge-modeling/plate5-merge-diff.md`
- **Backup:** `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`

## Decisions for this session

1. **Which mode to start with?** Recommendation: Mode 1. Matt may want to skip directly to Mode 3 (agent grounding) — push back unless Matt has a specific reason; Mode 1 first makes Mode 3's debugging tractable.
2. **Probe list scope.** The 8 Mode-1 queries above are a starting suggestion. Matt may have specific questions he's wanted to ask the graph for months — those should take priority.
3. **Output format.** Each probe: query command + expected result + actual result + delta. Probably a markdown table or per-probe sub-section in a session-results file.
4. **Where do failures route?** Each Mode-1 miss should be triaged into one of:
   - "Display bullets stale" → followup #1
   - "Empty-quote audit" → followup #2
   - "Hub-review queue" → followup #3
   - "Vocab drift / mistype" → backfill Track A
   - "Edge should reify but didn't" → backfill Track B
   - "Head direction wrong" → backfill Track C
   - "Genuinely missing edge" → Pass 1 / Pass 3 future work (NOT in scope)

## Out of scope (do NOT touch this session)

- `edges.jsonl` writes — Plate 5 already shipped; further edits require Matt sign-off + a new gated phase.
- LLM-based enrichment passes — gated on precision per S75 standing rule; the validation pass surfaces what's needed, doesn't run it.
- Pass 1 chapter re-extraction — explicitly off the table per S86 backfill design.
- The 2 in-progress IDE-edited files: `progress/continue-prompts/2026-06-08-alias-and-display-design.md` (Matt's WIP).

## End-of-session checklist

- Write `working/session-results/2026-06-09-graph-validation.md` with: mode chosen, probes run, headline findings, follow-ups routed.
- Update `worklog.md` Session Log (S88 entry; remember 5-entry cap — S82 archives if 6th lands).
- Update `working/todos.md` if any new TODOs surface OR if follow-up TODOs #1-6 get resolved.
- If Mode 3 was reached: capture the agent-grounding pattern as a reusable artifact (probably under `working/runbooks/` or `working/agent-fleet-specs/`).
- /endsession requires explicit permission per Matt's standing rule.
