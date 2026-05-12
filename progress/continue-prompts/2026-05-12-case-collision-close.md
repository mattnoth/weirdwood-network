# Continue — Close the Case-Collision Gap (next session)

---

## TL;DR — what to do right now

**Step 1.** Open a fresh Claude Code session, **Sonnet 4.6**.

**Step 2.** Paste this:
```
/continue 2026-05-12-case-collision-close
```

**Step 3.** Walk away. That session runs **Track A** (promote 60 reconstructed outputs into `graph/nodes/`). ~60-90 min. Single window. NO watcher. NO subagent dispatching to other windows.

**Step 4 (optional).** When Track A lands, decide if you want Track B (the 65-slug tail). If yes:
- Track A session writes a new mission file `working/agent-fleet-specs/missions/2026-05-13-case-collision-tail.md` before closing
- Open a fresh **Opus 4.7** window, paste: `/watcher case-collision-tail`
- Open 2-3 fresh **Sonnet 4.6** windows, paste in each: `/worker case-collision-tail <wave-id>` (the watcher will tell you the wave ids)
- This is the only point at which the watcher pattern kicks in this whole track

If you don't want Track B, skip step 4 — the remaining 65 are mostly dregs (real-world books, disambig pages, hound names) and skipping them is fine.

---

**Created:** 2026-05-12 (Session 46)
**Recommended model:** Sonnet 4.6 for Track A (promotion — deterministic-ish session-task); Opus 4.7 + Sonnet workers for Track B (tail mission with watcher).
**Parallel-safe with:** alias-backfill round 2 (`progress/continue-prompts/2026-05-12-alias-backfill-round-2.md`) — different file write-sets.
**Sequential prerequisite:** none.

This handoff has **two tracks**. Track A is the value (closes the 60 reconstructed outputs into the graph). Track B is optional (closes the 65 tail slugs — 15 canonical + 50 droppable). Run Track A first.

---

## State at handoff

- **Mission 1 (case-collision top-10):** archived. Postmortem + outcome in `working/agent-fleet-specs/missions/done/2026-05-12-case-collision-top-10.md`. Outputs in `working/missions/case-collision-top-10/worker-<slug>/` (10 dirs).
- **Batch 2 (next 50 slugs):** subagent-orchestrated, complete. Outputs in `working/missions/case-collision-batch-2/worker-<slug>/` (50 dirs). All schema-validated PASS.
- **Tail (remaining 65 slugs):** NOT done. Listed at bottom of this prompt.
- **Protocol v1:** landed in `working/agent-fleet-specs/mission-protocol.md`. Worker snippet at `working/agent-fleet-specs/worker-snippets/case-collision-template.md`.
- **Architecture/protocol edits queued:** multi-type policy in architecture.md; subagent-vs-multi-window trigger rule in mission-protocol.md.

---

## Track A — Promotion (mandatory, do first)

**Goal:** Take 60 reconstructed Identity+Edges outputs from `working/missions/` and write them into the actual graph at `graph/nodes/<type>/<slug>.node.md`. Apply type fixes, multi-type policy, alias merges, and deduplication.

**Mode:** Single session-task. Sonnet 4.6. No watcher needed (deterministic enough; orchestrator session does the work). Run in a fresh Claude Code window.

**Inputs:**
- `working/missions/case-collision-top-10/worker-*/output.md` (10 files)
- `working/missions/case-collision-batch-2/worker-*/output.md` (50 files)

**Outputs:**
- New/updated files in `graph/nodes/<type>/<slug>.node.md` (~60 nodes)
- Architecture.md edit (multi-type policy section — see Phase 3 below)

### Promotion steps

1. **Read each output.md.** Extract slug, type, Identity, Edges, aliases. Combine with batch-1 + batch-2 status.json for confidence + notes.

2. **For each slug, decide promotion target:**
   - Does a node with this slug already exist in `graph/nodes/`?
     - If yes: this is an UPDATE (Identity overwrite into existing stub, edges merged).
     - If no: this is a CREATE.
   - Does an *aliased* node exist? Examples this run: `old-gods` → existing `old-gods-of-the-forest.node.md` already aliases `old-gods`. Don't create new node; UPDATE the existing aliased one.
   - Does the slug have a known alias-merge candidate? See "Alias merges" below.

3. **Apply type fixes during write:**
   - Workers proposed `event.conflict` (drift); correct to `event.war`. Slugs affected this batch: `ghiscari-wars` (worker said event.conflict).
   - `event.war` already exists in architecture.md (line 97); the worker didn't load the spec. Use the correct existing type.
   - Bonus existing-graph bug to fix during this pass:
     - `graph/nodes/events/war-of-the-five-kings.node.md` is mistyped `event.battle`. Change to `event.war`.
     - Duplicate node: `graph/nodes/events/war-of-five-kings.node.md` (correct type, wrong slug). Merge into `war-of-the-five-kings.node.md` and delete the duplicate. Confirm no edges point to `war-of-five-kings` first (`grep -r "war-of-five-kings" graph/nodes/` excluding the duplicate node itself); rewrite any inbound to the canonical slug.

4. **Apply multi-type policy** (see Phase 3 for the architecture.md edit that ratifies this):
   - **free-folk** — existing node at `graph/nodes/factions/free-folk.node.md` is typed `organization.faction`. Correct to `type: concept.culture`. Move file: `graph/nodes/factions/free-folk.node.md` → `graph/nodes/concepts/free-folk.node.md` (or wherever `concept.culture` lives — check `graph/nodes/cultures/` first). Faction-ness preserved via existing/new edges (MEMBER_OF from individual free-folk character nodes; INVOLVES from war/battle nodes).
   - **children-of-the-forest** — existing at `graph/nodes/factions/children-of-the-forest.node.md` typed `organization.faction`. Correct to `type: species`. Move file: `graph/nodes/factions/` → `graph/nodes/species/`.

5. **Alias merges (resolve at promotion, not as separate todos):**
   - `red-priest` + `red-priestess` — `red-priestess` is the feminine form, not a separate entity. Keep `red-priest` as canonical. Add `red-priestess` to its aliases list. If `red-priestess.node.md` exists, delete it and rewrite any inbound references.
   - `inn-at-the-crossroads` + `crossroads-inn` + `two-crowns` — same inn. Keep `inn-at-the-crossroads` as canonical. Add the others as aliases. Delete duplicates if present.
   - `valar-morghulis` — already on todos.md; promotion writes the reconstructed Identity into the canonical node.
   - Watch for other slug-variant collisions during promotion — grep before each write.

6. **Fix `small-council` empty Edges block.** The batch-1 small-council worker emitted Identity but no edges (didn't reverse-lookup). Run reverse-lookup during this promotion: grep `working/wiki/data/infobox-data.jsonl` for entries with `MEMBER_OF: Small Council` or similar — emit the MEMBER_OF (people who served on the council) edges directly into the small-council node during write.

7. **Write `pass_origin: pass2-wiki-reconstruction-mission-batch-{1|2}`** in the promoted node's frontmatter (track provenance).

### Success criteria (Track A)

- 60 of 60 outputs promoted (or explicitly skipped with reason in worklog)
- 0 duplicates in graph (war-of-the-five-kings cleanup; alias-merge cleanups)
- 0 incorrect types for the multi-type cases (free-folk, children-of-the-forest)
- `small-council` node has non-empty Edges block
- Worklog Session 47 entry references this work

### Helpful one-liners

```bash
# Count outputs to promote
ls working/missions/case-collision-top-10/worker-*/output.md working/missions/case-collision-batch-2/worker-*/output.md | wc -l   # expect 60

# Audit current event.battle bloat (sanity check the type-drift problem)
find graph/nodes/events -name "*.node.md" | xargs grep -l "^type: event.battle$" | wc -l   # expect 348 (currently)

# Find duplicates
ls graph/nodes/events/war-of-*.node.md
```

---

## Phase 3 — Architecture.md + protocol edits (do during/after Track A)

Small edits; bundle with promotion in the same session.

### Edit 1: `reference/architecture.md` — multi-type entity policy

Add a section under the Entity Types table:

```markdown
### Multi-type entities

Some real-world entities span multiple of the type categories above. Free Folk are simultaneously a culture (`concept.culture`) and a polity/faction (`organization.faction`). Children of the Forest are simultaneously a species (`species`) and an ancient sentient faction. Wardens are titles, but the *role* of being a warden is also a behavior set.

**Policy: one node per real-world entity. The `type` field captures its primary identity. Other facets emerge through edges, not through a second node.**

- Free Folk → `concept.culture`. Polity-ness emerges via MEMBER_OF (character → free-folk), INVOLVES (war/battle → free-folk), HOLDS_TITLE (king-beyond-the-wall), INHABITED_BY (beyond-the-wall → free-folk).
- Children of the Forest → `species`. Faction-ness emerges via FOUGHT_IN (war-of-first-men), LOCATED_AT (isle-of-faces), POSSESSES (hammer-of-the-waters magic).

This avoids SAME_AS bookkeeping and ambiguous "which node?" queries. Retrieval naturally unions identity + behaviors via edge traversal.

**The `multi-type-entity-resolver` agent's job** under this policy: pick the right primary type + ensure edges capture the other facets. NOT split into multiple nodes.
```

### Edit 2: `working/agent-fleet-specs/mission-protocol.md` — execution-mode trigger

Add under "Roles" or as a new subsection:

```markdown
### Choosing execution mode (subagent vs multi-window)

**Subagent-orchestrated mode OK when:**
- Worker prompt fully inlines schema, types, vocabulary, and task strategy (no "consult X" / "read Y" indirection)
- Task is single-shot per item; stateless reasoning
- Total worker wall-clock < 10 min per worker
- No project context (CLAUDE.md, architecture.md) required at runtime

**Multi-window + watcher when ANY of the following are true:**
- Task requires loading project context (architecture.md TYPE_DIR_MAP, prior decisions, CLAUDE.md rules)
- Worker prompt cannot be made fully self-contained (e.g., must reference multiple inter-related spec files)
- Drift potential is high (multi-step reasoning per item, evolving strategy)
- Wall-clock per worker > 10 min — observability matters
- Matt wants to interrupt mid-flight or check intermediate outputs

**Default if uncertain: multi-window + watcher.** The cost of multi-window is operator overhead (Matt opens windows); the cost of subagent drift is post-mortem analysis time, which is higher.

Session 46's case-collision-batch-2 should have been multi-window — workers needed architecture.md TYPE_DIR_MAP awareness, drift surfaced (event.conflict, object.text framing) that watcher would have caught early.
```

---

## Track B — Tail (optional, multi-window+watcher mission)

**Goal:** Close the remaining 65 case-collision slugs. Most are dregs (real-world books, disambig pages, hound names, meta-wiki concepts). Hand-pick the ~15 canonical entries and dispatch as a multi-window mission per the v1 protocol.

**Mode:** Multi-window + watcher. Per the execution-mode rule above, drift potential is HIGH here (workers need TYPE_DIR_MAP awareness; many slugs require type judgment calls). This is the trigger case for multi-window mode — DO NOT default back to subagents.

### Slug filtering (Python pre-step)

Before launching workers, write a script to classify the 65 tail slugs:
- **Canonical (reconstruct):** parenthetical-suffix characters (`roone-(maester)`, `ronnel-arryn-(king)`, `rickard-stark-(king)`, `lyonel-tyrell-(lord)`, `damon-lannister-(lord)`, etc.), minor houses (`house-towers-(north)`, `house-lake-(north)`, etc.), specific named things (`tower-of-joy`, `ice-dragon`, `dragon-horn`, `bellegere-otherys-(courtesan)`).
- **Drop (status: fail with reason):** real-world books (`a-feast-for-crows`, `beyond-the-wall-(book)`), disambig pages (`*-(disambiguation)`), list articles (`list-of-*`, `timeline-of-*`), meta-wiki concepts (`pov-character`), too-generic phrases (`rule-of-thumb`, `trade-talk`, `horse-god`).

Expected outcome: ~15-20 canonical, ~45-50 dropped.

### Mission setup (Shape A handoff)

Create a new mission file: `working/agent-fleet-specs/missions/2026-05-1X-case-collision-tail.md` using the v1 protocol structure. 2-3 wave-sized workers, each handling ~5-7 slugs. Workers in separate Claude Code windows; watcher in its own window.

Each worker prompt: paste `working/agent-fleet-specs/worker-snippets/case-collision-template.md` body + the worker's slug list + the schema-validation step inlined with that slug list. Include the explicit "fail on real-world books / disambig pages / list articles / meta concepts" guidance.

### Full tail slug list (for filtering)

```
god-emperor, dragon-horn, conflict-beyond-the-wall, chief-undergaoler, across-the-narrow-sea,
wine-of-courage, trade-talk, timeline-of-major-events, rolfe-the-dwarf, list-of-rivers,
grazdan-mo-ullhor, grand-master, ghost-grass, fat-fellow, willow-(hound),
the-song-of-ice-and-fire, the-princess-and-the-queen,-or,-the-blacks-and-the-greens, the-princess-and-the-queen, stern-face, starved-man,
rule-of-thumb, roone-(maester), ronnel-arryn-(king), roland-crakehall-(lord), robert-brax-(disambiguation),
rickard-stark-(king), red-raven-(free-folk), pov-character, pate-(ranger), pate-(novice),
lyonel-tyrell-(lord), lymond-(disambiguation), lyman-(disambiguation), lyman-(archmaester), lucerys-velaryon-(master-of-ships),
luceon-(disambiguation), list-of-characters, kyra-(hound), ice-dragon, house-words,
house-towers-(north), house-lake-(north), house-holt-(north), house-brownhill-(stormlands), horse-god,
high-septon-(fat-one), high-king, henly-(maester), helicent-(hound), harmune-(archmaester),
handsome-man, gerold-(archmaester), garin-(orphan), fowler-twins, erryk-(guard),
damon-lannister-(lord), damon-dance-for-me, dake-(guard), beyond-the-wall-(book), bethany-fair-fingers,
bellegere-otherys-(courtesan), arryn-succession-conflict-(134-ac), arryk-(guard), all-for-joffrey, a-feast-for-crows
```

### Success criteria (Track B)

- ~15 canonical tail entries promoted to `graph/nodes/`
- ~50 explicit fails recorded (status.json with `fail` + notes) — preserves auditability of what was skipped and why
- `working/todos.md` HIGH item updated to 125/125 closed (or with explicit list of skipped slugs)
- Worklog Session 47/48 entry references this work

---

## DO NOT (both tracks)

- Refetch wiki pages
- Auto-run `/endsession`
- Invent edge types or entity types (use the locked vocab from `case-collision-template.md`)
- Default to subagent mode for Track B (drift potential too high; multi-window per v1 protocol rule)
- Promote outputs into `graph/nodes/` for any slug that should have been a fail (real-world books, disambig pages, etc.)
- Skip the schema-validation step in any worker prompt

---

## Self-contained for resumption

Files to read at start of next session:
- This file
- `working/agent-fleet-specs/worker-snippets/case-collision-template.md`
- `working/agent-fleet-specs/mission-protocol.md` (v1)
- `working/agent-fleet-specs/missions/done/2026-05-12-case-collision-top-10.md` (archived mission with postmortem)
- `history/session-details/session-046.md` (this session's full narrative)
- `reference/architecture.md` (TYPE_DIR_MAP + edge vocab — sanity check for Phase 3 edits)
- One sample worker output to see the shape: `working/missions/case-collision-batch-2/worker-tower-of-joy/output.md`

Estimated wall-clock for next session: Track A ~60-90 min, Phase 3 edits ~15 min, Track B (if pursued) ~45 min. Full closure of the 125-page case-collision gap is realistic in one focused session.
