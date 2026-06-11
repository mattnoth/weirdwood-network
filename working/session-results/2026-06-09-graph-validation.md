---
date_started: 2026-06-09
date_finished: 2026-06-10
session: S88
mode: Mode 1 — capability probes (pre-Mode-3 graph-layer isolation)
status: complete (all 8 probes + writeup)
edges_state: edges.jsonl=4,757 (post-Plate-5, untouched this session)
---

# S88 — Mode 1 graph-validation probes

> All probes were read-only against `graph/edges/edges.jsonl` (4,757 rows post-Plate-5) + `graph/nodes/`. No writes to `edges.jsonl` or any canonical artifact.

## Headline findings (the surprises)

1. **Reification works at BEAT level only.** Parent hubs (`red-wedding`, `purple-wedding`, `battle-of-the-blackwater`, etc.) are structural shells: 0 direct participants. All participant role edges live on the SUB_BEAT children. Beat-union queries DO recover the participant set (Probe 7), but the query layer has to know to do the union — there's no `--event-participants <hub>` primitive yet.
2. **Beat coverage is wildly uneven across hubs.** Red Wedding 8 beats, Battle of the Blackwater 2, Purple Wedding 1 (and the one isn't even about Joffrey's death), Tourney at Harrenhal 0. The mining strategy is reactive to Pass 1 prose density, not normalized per canonical event.
3. **Pre-narrative historical events are a categorically dark zone — but the story is more nuanced than "all historical content is missing".** Of 10 major historical anchors probed (Tourney at Harrenhal, Trident, Sack of King's Landing, Tower of Joy, Robert's Rebellion, Greyjoy Rebellion, etc.), **5 exist as event nodes** but only 2 have **any** edges (1 each). `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` — a designed-into-vocab edge type for historical events — fires exactly **once** in the entire 4,757-edge graph. **Refinement (post-Probe 5):** the one CROWNS edge IS the canonical Rhaegar→Lyanna at the Tourney at Harrenhal — `rhaegar-targaryen` → `lyanna-stark`, cited verbatim from AGOT Eddard XV (Ned's memory). It's a Pass-1-direct edge (`evidence_kind=book-pass1`, line-precise ref) — Pass 1 caught it because Ned's POV reminiscence had clean subject-verb-object structure. **But the edge doesn't attach to the `tourney-at-harrenhal` hub.** A query starting from either person finds the edge; a query starting from the tourney hub finds nothing. The real gap isn't "extract relationships from retrospective mentions" (Pass 1 already does some of this) — it's **structural attachment**: connecting existing dyadic edges back to their parent historical-event hub. That refines NEW TODO #9 substantially (see Routing summary).
4. **Slug discoverability gap.** Three distinct `event.execution` hubs exist for "Ned's execution" (`the-execution` = AGOT-1 Will the deserter; `joffrey-orders-execution` = Ned's beheading; `ned-claims-the-execution` = Lady at Darry). The graph correctly distinguishes them. But an agent asked "Ned's execution" has no path to `joffrey-orders-execution` — action-named slugs don't match victim-phrased questions.
5. **Plate 4 quote-leak bug confirmed.** `fleet-forms-battle-lines → battle-of-the-blackwater` SUB_BEAT_OF evidence_quote contains a raw wiki-participant dump (`"participants (wiki-link): aerys-ii-targaryen, alchemists'-guild, alester-florent..."`) including Aerys (wrong era). `robb-is-killed → red-wedding` carries a wrong-class quote (`"DEFEATS: Warden of the North (track_b: Result)"`). Widens followup #2 (empty-quote backfill) to include wrong-quote class.
6. **Designed vocab types effectively dark.** `ATTENDS = 2` and `WIELDED_IN ≈ 10` across the entire 4,757-edge graph. "Who was present at X" and "what weapon was used in X" are not answerable. `robb-is-killed` has 3 role edges (AGENT/VICTIM/COMMANDS) and structural edges (SUB_BEAT_OF, LOCATED_AT) but **no WIELDED_IN** — the weapon (a dagger, per the books — Roose stabs him through the heart after the crossbow volleys, saying "Jaime Lannister sends his regards") is in the prose, not the graph. NB: WIELDED_IN dark-ness is the finding; the weapon class is incidental (named or unnamed, dagger or sword, none of it is reified).
7. **Strategic/architect chains don't surface.** Probe 6 (Tywin ↔ Mountain, 2-hop path) returns 4 direct edges + 6 2-hop bridges — **all person-mediated, zero event bridges**. The Sack of King's Landing (the canonical Tywin→Mountain bridge event) doesn't appear because it's in the dark historical zone (finding #3). Same story in Probe 7: Tywin doesn't appear as a COMMANDS_IN on any Red Wedding beat, even though the Lannister architecting is signaled in-prose ("Lannisters send their regards"). The reification only catches in-scene chapter agents, not off-page architects.
8. **Role-edge citation shape differs from Pass-1-direct edges.** Pass-1-direct edges carry line-precise `evidence_ref` (e.g. `sources/chapters/acok/acok-arya-07.md:21`). Plate 3 role edges (`evidence_kind=book-pass1-reified`) cite at chapter-scope: `evidence_book` + `evidence_chapter` + `evidence_source_file`, no line. Not a bug — a consequence of reifying chapter-scope assertions — but `graph-query.py --neighbors` output and any agent-facing display needs to render both shapes consistently. Worth a Pass-3 audit pass to harmonize.

## Per-probe table

| # | Probe | Expected | Actual | Delta | Route |
|---|-------|----------|--------|-------|-------|
| 1 | Red Wedding (`--neighbors red-wedding`) | Participants + commanders direct on hub | 0 outgoing, 8 SUB_BEAT_OF incoming, 0 direct participants. Beats well-formed (catelyn-is-killed, robb-is-killed) with AGENT_IN/COMMANDS_IN/VICTIM_IN/LOCATED_AT. | Hub-is-shell pattern confirmed; works at beat level. | Document pattern; route bad quote on `robb-is-killed → red-wedding` to followup #2. |
| 2 | Purple Wedding (`--neighbors purple-wedding`) | Joffrey-dies + arrest-tyrion beats + participants | 1 SUB_BEAT_OF (`tyrell-plot-revealed`, a `event.conspiracy` about Sansa→Highgarden — **not** Joffrey's poisoning). No joffrey-dies / joffrey-poisoned / tyrion-arrested hubs. 2 orphan event nodes (`wedding-feast-begins`, `the-wedding-feast-proceeds`) unlinked. | Vastly under-mined. House-Tyrell VICTIM_IN on tyrell-plot-revealed = wrong direction. | Backfill Track B; hub-review #3. |
| 3 | Blackwater (`--neighbors battle-of-the-blackwater`) | wildfire + Tyrion + Stannis fleet | 2 SUB_BEAT_OF (plate4-wiki-cluster), 0 direct participants. `wildfire` mentioned 0 times in edges.jsonl. | Quote-leak bug (Aerys + wiki-participant dump in evidence_quote). | followup #2 widened; Track B. |
| 4 | Ned's execution slug-discoverability | One unambiguous "Ned's execution" hub | 3 distinct execution hubs, all well-formed and correctly distinguished. But no slug-alias bridge from "Ned's execution" → `joffrey-orders-execution`. ATTENDS = 2 across whole graph. | Design works; agent-side query layer doesn't have the bridge. | NEW TODO #7 (event-participants primitive) + NEW TODO #8 (alias-resolver, S86 design exists). |
| 5 | Tourney at Harrenhal | Some non-zero participation (Rhaegar, Lyanna, Ashara, Howland) | **0 edges total. Isolated node.** Confirmed by batched check: 10 historical anchors, 5 exist as nodes, only 2 have any edges (1 each). `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY = 1` total. | Pre-narrative historical events = dark category. | NEW TODO #9 (design Q: historical-anchor mining strategy). |
| 6 | Tywin ↔ Mountain 2-hop path | Event bridges (Sack of KL, riverlands, Red Wedding chain) | 4 direct edges + 6 2-hop bridges, **all person-mediated** (Tyrion, Cersei, Oberyn, Sandor, Arya, Vargo Hoat). 0 event bridges. | Strategic/architect event bridges absent (same dark zone as #5). | Track B; revisit after #9 designed. |
| 7 | "Who ordered the Red Wedding" (beat-union) | Walder + Roose + Tywin | Walder Frey (7/8 beats), Roose Bolton (1 beat — crossbows). **Tywin absent.** 3 NEW wrong-direction role edges surfaced: `robb-stark` COMMANDS_IN `lord-walder-calls-for-the-bedding`; `greatjon-umber` AGENT_IN `the-bedding-ceremony-begins`; `catelyn-stark` AGENT_IN `the-wedding-feast-proceeds`. | Beat-union works (Walder/Roose canonical). Off-page architect (Tywin) missing — same dark zone. | hub-review #3 grows by 3 items; NEW TODO #7 (`--event-participants`) would automate this query. |
| 8 | Capability floor — weapons on `robb-is-killed` | WIELDED_IN edge for the dagger Roose uses (not a named weapon) | 3 role edges + 2 structural, **no WIELDED_IN**. Weapon class dark — whether the weapon is named or not doesn't matter; there's no reified weapon participation at all. | "What killed Robb?" unanswerable from graph. | Track B (edge-should-reify-but-didn't) or Pass 1 follow-up. |

## Routing summary — which follow-up TODOs grew

- **#1 display-bullet regen:** no new signal this session.
- **#2 SUB_BEAT_OF quote backfill:** WIDEN scope from empty-quote-only to include wrong-quote class (Plate 4 quote-leak — wiki-participant dumps + cross-event quote misattribution). Concrete examples: `fleet-forms-battle-lines → battle-of-the-blackwater`, `robb-is-killed → red-wedding`.
- **#3 hub-review queue:** add **4 wrong-direction role edges**:
  - `house-tyrell` VICTIM_IN on `tyrell-plot-revealed` (framed-conspirator, not victim) — Probe 2
  - `robb-stark` COMMANDS_IN on `lord-walder-calls-for-the-bedding` (Walder ordered the bedding, not Robb) — Probe 7
  - `greatjon-umber` AGENT_IN on `the-bedding-ceremony-begins` (Stark side; not an executor) — Probe 7
  - `catelyn-stark` AGENT_IN on `the-wedding-feast-proceeds` (she was a victim; mining picked up her direct-object Pass-1 mention) — Probe 7
- **#4 deferred collisions:** unchanged.
- **#5 mutual-kill reverse:** unchanged.
- **#6 backfill tracks A/B/C:** **Track B grows substantially.** Beat coverage for hub-class events (Purple, Blackwater, Harrenhal-class) needs targeted mining. Also weapon-class participation (`WIELDED_IN`) is effectively dark and would need its own pass.
- **NEW TODO #7:** `graph-query.py --event-participants <hub>` mode. Unions SUB_BEAT_OF children's role edges (AGENT_IN/COMMANDS_IN/VICTIM_IN/WIELDED_IN/ATTENDS/LOCATED_AT) and presents them as if attached to the hub. This is the missing query primitive — Probe 7 had to manually replicate it via `grep` + loop. Cheap script — read-only over `edges.jsonl`. Should be the next deterministic build.
- **NEW TODO #8:** event-alias-resolver build. S86 design at `reference/alias-resolver-design.md` (verify path). Needed to make slug-discoverability ergonomic: "Ned's execution" → `joffrey-orders-execution`; "the Trident" → `battle-of-the-trident`; "the Tourney at Harrenhal" → `tourney-at-harrenhal`.
- **NEW TODO #9 (category-level, design Q) — REFINED post-Probe 5 inspection:** pre-narrative historical events aren't *entirely* dark — Pass 1 catches some dyadic acts from POV reminiscence (the Rhaegar→Lyanna CROWNS edge from AGOT Eddard XV is the canonical example, cited verbatim, line-precise). The actual gap is **structural attachment**: those dyadic edges don't connect to their parent historical-event hubs. A query starting from the person finds the edge; a query starting from the hub doesn't. Three approaches to consider: (a) **structural-backfill pass** (cheap, deterministic) — scan existing Pass-1-direct edges whose evidence references a known historical event by name in the quote, and mint `SUB_BEAT_OF` / `LOCATED_AT` edges connecting them to the hub; this is the highest-leverage option because the dyadic data already exists; (b) wiki-only reification with explicit `evidence_kind=wiki-historical-anchor` for events that have no Pass-1 anchor at all (Tower of Joy, Sack of King's Landing); (c) targeted "retrospective-mention" extraction pass for what (a) and (b) still miss. Sequence is (a) first (zero LLM cost, immediate signal), then evaluate whether (b) and (c) are needed.
- **NEW TODO #10 (concrete, from Matt 2026-06-10):** rename `joffrey-orders-execution` → `execution-of-eddard-stark`. Action-named slug is the wrong shape for a recurring action (Joffrey orders executions constantly). Touches: (1) move `graph/nodes/events/joffrey-orders-execution.node.md` → `execution-of-eddard-stark.node.md` + update `slug:` + `name:` frontmatter, (2) update 5 rows in `edges.jsonl` (4 incoming AGENT_IN/COMMANDS_IN/VICTIM_IN/WIELDED_IN + 1 outgoing LOCATED_AT), (3) rebuild `graph/index/events/`, (4) check `working/wiki/data/cross-references.jsonl` + any display bullets in other node files. **GATED — requires explicit `apply` from Matt.** Build script with `--dry-run` first. Also do an action-slug pattern audit (`grep '^[a-z-]*-(orders|claims|demands|calls-for)-' graph/nodes/events/`) to surface other action-named risky slugs.
- **NEW TODO #11 (audit-class):** Plate 3 role-edge citation harmonization. Pass-1-direct edges carry line-precise `evidence_ref`; reified role edges cite chapter-scope (`evidence_book`+`evidence_chapter`+`evidence_source_file`) with no line. Pick a presentation convention (synthesize a "ref-equivalent" string for role edges, OR have `graph-query.py` render both shapes side-by-side, OR backfill line refs by string-matching the quote against the source file). Low-priority, cosmetic-class.

## Mode 1 → Mode 3 readiness call

**Recommendation: hybrid (b+a) — short Track B detour for the highest-leverage gaps before Mode 3.**

The probes prove the **capability is real but uneven**: where the graph has data, agent queries work cleanly (Probe 1 Red Wedding beat-level, Probe 6 direct dyads, Probe 7 beat-union for canonical orderers). Where the graph has gaps, the agent will have no signal at all (Probe 5 isolated nodes, Probe 6 missing event bridges, Probe 8 missing weapons). If Mode 3 launches now, the agent will succeed on chapter-resident events and fail silently on historical/strategic queries — and we won't be able to distinguish "agent is bad" from "graph has no data here" without re-running these probes against the failures.

The minimum-viable Track B detour before Mode 3:

1. **Build NEW TODO #7** (`--event-participants <hub>`). 1-2 hour script; eliminates the manual beat-union workaround; makes hub queries first-class. Highest leverage / lowest cost item on this list.
2. **Apply NEW TODO #10** (rename `joffrey-orders-execution` → `execution-of-eddard-stark`) once Matt signs off. Concrete, scoped, removes the most-cited slug-discoverability example.
3. **Resolve NEW TODO #9 as a design call** (pick a, b, or c). Don't necessarily execute — but decide whether the historical-anchor dark zone is acceptable as documented limitation or whether Mode 3 needs it filled first.

**What does NOT need to happen first:**
- Track B beat-coverage backfill for Purple/Blackwater — Mode 3 can document "this hub is sparse" as a known state. The capability works where data exists; we don't need 100% coverage to test agent grounding.
- Quote-leak backfill (followup #2) — cosmetic for prose display, not blocking for graph traversal.
- Citation harmonization (NEW TODO #11) — purely presentational.

**Argument against proceeding to Mode 3 right now (option a):** the slug-discoverability gap (NEW TODO #8) is fundamental to agent UX. Without the alias-resolver, every Mode 3 prompt that names an event in the way a reader would name it ("Ned's execution", "the Tourney at Harrenhal", "the Trident") will fail to find the hub even when the data exists. That's not a "data gap" failure — it's a "query layer" failure — and it would muddy any Mode 3 evaluation signal.

**Argument against the full Track B detour first (option b alone):** the unknowns about how agents actually use the graph compound the longer Track B runs. Build the query primitive (#7) and the alias bridge (#8) — both are deterministic scripts — then dip into Mode 3 to see what queries the agent actually generates, and let *that* drive subsequent Track B priorities.

**Hybrid recommendation, concretely:**

- **Phase 1 (this week, no LLM cost):** ship NEW TODO #7 + #8 + apply #10. All deterministic Python.
- **Phase 2 (next session):** light Mode 3 dip — 5-10 grounded agent queries against the graph as-is, observing failure modes. Use the failures to prioritize between Track B beat-coverage vs NEW TODO #9 vs going broader on Mode 3.
- **Decision point:** if Mode 3 dip surfaces ≥3 failure modes that map to NEW TODO #9 (historical dark zone), promote it to "must resolve before deeper Mode 3."

## Probe-by-probe artifacts (for re-running)

All commands re-run against `graph/edges/edges.jsonl` (4,757 rows) and `graph/nodes/`:

```bash
# Probe 1
python3 scripts/graph-query.py --neighbors red-wedding
python3 scripts/graph-query.py --neighbors catelyn-is-killed
python3 scripts/graph-query.py --neighbors robb-is-killed

# Probe 2
python3 scripts/graph-query.py --neighbors purple-wedding
python3 scripts/graph-query.py --neighbors tyrell-plot-revealed

# Probe 3
python3 scripts/graph-query.py --neighbors battle-of-the-blackwater
grep -c '"wildfire"' graph/edges/edges.jsonl

# Probe 4
python3 scripts/graph-query.py --neighbors the-execution
python3 scripts/graph-query.py --neighbors joffrey-orders-execution
python3 scripts/graph-query.py --neighbors ned-claims-the-execution
grep -c '"ATTENDS"' graph/edges/edges.jsonl

# Probe 5
grep -c '"CROWNS_QUEEN_OF_LOVE_AND_BEAUTY"' graph/edges/edges.jsonl
for slug in trident harrenhal-tourney roberts-rebellion sack-of-kings-landing tower-of-joy battle-of-the-trident greyjoy-rebellion; do
  echo "  $slug $(grep -c "\"$slug\"" graph/edges/edges.jsonl) edges"
done

# Probe 6
python3 scripts/graph-query.py --path tywin-lannister gregor-clegane

# Probe 7 (beat-union — until --event-participants exists)
python3 scripts/graph-query.py --neighbors red-wedding --json \
  | jq -r '.incoming[] | select(.edge_type=="SUB_BEAT_OF") | .other_slug' > /tmp/rw_beats.txt
while read slug; do
  echo "=== $slug ==="
  grep "\"COMMANDS_IN\".*\"target_slug\": \"$slug\"" graph/edges/edges.jsonl \
    | python3 -c "import sys,json;[print(' ',json.loads(l)['source_slug']) for l in sys.stdin]"
done < /tmp/rw_beats.txt

# Probe 8
grep '"target_slug": "robb-is-killed"' graph/edges/edges.jsonl \
  | python3 -c "import sys,json;[print(json.loads(l)['edge_type'], json.loads(l)['source_slug']) for l in sys.stdin]"
```

## End-of-session checklist (from continue prompt)

- [x] Write `working/session-results/2026-06-09-graph-validation.md` (this file)
- [x] Update `working/todos.md` — add NEW TODOs #7/#8/#9/#10/#11 (Matt /endsession 2026-06-10)
- [x] Update `worklog.md` Session 89 entry
- [x] /endsession granted 2026-06-10

## Overnight autonomous kickoff (Matt 2026-06-10)

Matt is heading to bed; greenlit Phase 1 to run autonomously. Three parallel `script-builder` agents launched in background to make as much progress as possible while he sleeps:

1. **Build `graph/graph-query.py --event-participants <hub>`** — adds beat-union primitive. Reads existing script, edges.jsonl, vocab from `reference/architecture.md`. Modifies `scripts/graph-query.py` only. Smoke-tests with `--event-participants red-wedding` and writes results to `working/session-results/2026-06-10-overnight-event-participants.md`. **No writes to `edges.jsonl`.**
2. **Build event-alias-resolver per S86 design (`reference/alias-resolver-design.md`).** Output: new script in `scripts/` + alias mapping artifact in `working/wiki/data/event-aliases.{jsonl,json}` (path per design). Smoke-tests "Ned's execution" / "the Trident" / "the Tourney at Harrenhal" → expected hub slugs. Writes results to `working/session-results/2026-06-10-overnight-alias-resolver.md`. **No writes to `edges.jsonl` or canonical node files.**
3. **Build `scripts/rename-event-node.py` + run DRY-RUN ONLY for `joffrey-orders-execution` → `execution-of-eddard-stark`**, plus the action-slug pattern audit. **`--apply` is NOT run autonomously — gated on Matt's wake-up sign-off.** Writes the dry-run diff + audit list to `working/session-results/2026-06-10-overnight-rename-dryrun.md`. **No writes to `edges.jsonl` or canonical node files** (dry-run is read-only output).

All three agents are constrained: read-only on canonical artifacts (`edges.jsonl`, `graph/nodes/`), write only to specified working/ paths, no auto-/endsession, no autonomous progression to the next phase. LLM reasoning is allowed within each script-builder agent's session — they can call sub-models as the script-building work requires.

Phase 2 (light Mode 3 dip) is NOT kicked off autonomously — Matt drives that one in a manned session after reviewing the overnight results.

## Hard rules honored

- ✅ `edges.jsonl` untouched (no writes; verified by git status before/after probes — should still show clean on `graph/edges/`)
- ✅ No LLM enrichment runs launched
- ✅ All probe commands read-only
- ✅ No auto-/endsession
