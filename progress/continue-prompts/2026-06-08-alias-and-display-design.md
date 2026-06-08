# Continue — Alias resolution + chat-UI display name policy (design)

> **Recommended model:** Opus 4.7 — these are design questions about how the graph
> serves downstream consumers (edge resolvers + future chat UI). Need world-model
> reasoning, not bulk LLM work. No new code expected; deliverable is a design doc.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9). Two related but
> separable design questions surfaced at the end of session 2026-06-07/08.

## Context — where these questions came from

Last session built Plate 4 wiki-cluster (a Plate-3 follow-up) to bridge the
wiki-vs-chapter taxonomy gap. Along the way, two related infrastructure questions
came up that need their own treatment:

1. **Alias-as-edge-resolver:** the wiki cache holds 176 aliases for 88 of 371
   event-nodes (e.g. `red-wedding` has redirect aliases `wedding-at-the-twins`,
   `slaughter-at-the-twins`, etc.). These were never integrated into the edge
   resolver. Should they be? What about non-event nodes?

2. **Chat UI display name policy:** every node has both `slug: red-wedding`
   (lower-case kebab, the join key) and `name: "Red Wedding"` (human-readable).
   A future chat UI needs an explicit policy for which surface goes where.

Neither of these is blocking Plate 5 (the graph merge). Both are design-level
work that improves how the graph SERVES queries — agent traversal in particular.

## Files & data this session should read

**Existing alias-resolver code:**
- `scripts/stage4_name_resolver.py` — current person/house/location alias resolver
- `working/wiki/data/event-node-aliases.json` — 176 wiki event aliases just
  harvested (created 2026-06-07; not yet wired in)
- `working/wiki/data/alias-resolver.json` — older alias product from Pass 2 Stage 0
- `scripts/wiki-event-alias-harvester.py` — the script that built the 176 aliases

**Node schema:**
- `reference/architecture.md` — frontmatter spec for `slug:` + `name:` + `aliases:`
- `graph/nodes/events/red-wedding.node.md` — concrete example with both fields
- Any node under `graph/nodes/characters/` — see the typical alias usage

**Edge-creation flow (where aliases get consulted):**
- `scripts/stage4-pass1-extra-tables.py` — emits Pass-1 candidate edges, calls the resolver
- `scripts/edge-reify-backfill.py` — Plate 3, the latest LLM-using edge work
- `graph/edges/edges.jsonl` — current 3,811-edge spine; check `source_slug` /
  `target_slug` form

**Memory entries to consult:**
- `project_real_goal_graph_for_agents` — primary deliverable is graph for agent
  traversal; chat UI framing in the older docs is stale sketch
- `project_pipeline_not_fixed` — passes 2-6 are still negotiable; alias design
  fits in here
- `feedback_python_before_agent` — deterministic Python first

## Question 1 — alias-as-edge-resolver: scope + integration

Pass 1 extractions name entities many ways: "Catelyn Stark" / "Lady Stark" /
"the Tully woman" / "Cat". The edge builder needs every variant to resolve to
the canonical slug. `stage4_name_resolver.py` already handles person/house/location
aliases reasonably well (it's the resolver behind the deterministic spine's
~78% strict precision).

**What's missing:** event-node aliases were never harvested or wired in. The 176
just-built aliases (`working/wiki/data/event-node-aliases.json`) sit unused.

**Three sub-questions to answer:**

1. **Should event-node aliases be plumbed into the edge resolver, and where?**
   - Pass 1 sometimes mentions canonical events by name (e.g. "the Red Wedding",
     "Battle of the Blackwater"). When that happens, the resolver should map the
     mention → `red-wedding` / `battle-of-the-blackwater`. Currently it can't
     (no event-node alias support).
   - Estimate the value: scan a sample of Pass 1 extractions for canonical event
     mentions; count how often they occur. If meaningful frequency, wire it in.

2. **Should alias harvesting be extended to OTHER node types?**
   The wiki cache (`sources/wiki/_raw/`) has redirect data for every page type
   (characters, houses, locations, etc.). The current `alias-resolver.json`
   covers persons via a different pipeline; the systematic
   wiki-redirect harvest may add 1000s of additional aliases across the
   character/house/location nodes. Worth quantifying.

3. **Distinguish alias from sub-event.** The Plate-3 work showed that Pass-1
   chapter-beat mints (`lord-walder-calls-for-the-bedding`) are NOT aliases for
   `red-wedding`; they're sub-events. The architecture needs a clear policy:
   - aliases = different *names* for the same entity
   - sub-events = different *components* of a larger event (use `SUB_BEAT_OF` edge,
     not the aliases array)
   Currently this distinction is implicit. Make it explicit in `architecture.md`.

**Deliverable:** a short design memo at
`reference/alias-resolver-design.md` (new file) covering:
- Decision on extending the resolver to event-nodes
- Decision on systematic wiki-redirect harvest for non-event types
- Clarified `aliases:` vs `SUB_BEAT_OF` policy in architecture.md
- Concrete next-step (script to build / code to add / nothing-now-defer)

## Question 2 — chat UI display name policy

Every node already has `slug:` (the kebab-case join key — `red-wedding`) and
`name:` (the human-readable form — `"Red Wedding"`). The chat UI work has been
DEFERRED per `project_real_goal_graph_for_agents` (the "shared-password D&D chat
UI" framing in older docs is stale sketch). But IF or WHEN a chat layer ships
(or agents return graph results in conversation), there should be a clear policy.

**Sub-questions:**

1. **What does the agent see in prose vs in tool-call results?**
   - In free-text reasoning: `name` ("the Red Wedding"). Prevents the agent from
     leaking slugs into user-visible text.
   - In tool calls / structured outputs: `slug` (`red-wedding`). Preserves
     join-ability.
   - This should be enforceable at the prompt layer.

2. **How do nodes WITHOUT a name field get rendered?** The Plate-3 mints
   (`graph/nodes/events-pass1-beats/` if Plate 5 promotes them) have a `title:`
   field but no canonical `name:`. Promote `title:` → `name:` on minting, or
   require both?

3. **Where does this policy live?** Probably `reference/architecture.md` under a
   new "Display Names" section, with example showing the slug/name pair on
   `red-wedding.node.md`.

**Deliverable:** an additional section in `reference/architecture.md` —
"Display Names: slug as identifier, name as surface" — with the policy.

## Bonus — 4 structural issues to add to the design memo

The 2026-06-07/08 session surfaced 4 issues during the 23-mint human triage
that fit this design conversation:

1. **Wiki node type misclassification — 27 found, corrections STAGED.**
   - **Root cause:** the wiki ingestion (`scripts/wiki-pass2-triage.py`) only
     knew `event.battle`, `event.tournament`, `event.war` as event sub-types.
     Everything categorized under "events" defaulted to `event.battle`. Missing
     vocabulary → forced into the one type it knew.
   - **27 corrections staged** at
     `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl`
     — apply at Plate 5. Includes `red-wedding`, `purple-wedding`,
     `feast-in-honor-of-king-roberts-visit-to-winterfell`,
     `coronation-of-robert-i-baratheon`, `sandor-cleganes-trial-by-combat`,
     and 22 other weddings. New types used: `event.wedding`, `event.coronation`,
     `event.feast`, `event.trial`. The feast-honor-of-Robert node alone caused
     7 of 23 triage false-positives.
   - **3 prevention fixes (next session):**
     1. Expand event sub-type vocabulary in `reference/architecture.md` —
        add `event.wedding`, `event.feast`, `event.coronation`, `event.trial`,
        `event.assassination`, `event.execution`, `event.conspiracy` as
        first-class types.
     2. Update `scripts/wiki-pass2-triage.py`'s entity-type map to assign
        these from slug/title patterns (e.g. `wedding-of-X` → `event.wedding`).
     3. Write `scripts/wiki-event-type-validator.py` — scans every event-node
        for slug/title-vs-type mismatches; run as a hook after any future
        wiki-pass2 run. Would have caught all 27.

2. **IDF-style downweighting for participants.** The narrowing function in
   `scripts/plate4-wiki-cluster.py` currently scores +1 per participant overlap
   (cap 5). High-frequency participants (Robert, Cersei, Tyrion) appear in many
   wiki events and produce false overlap. Inverse-document-frequency weighting:
   participants who appear in fewer wiki events score higher. Cheap fix.

3. **Historical-pre-series event filter — add `era:` frontmatter going forward.**
   Events like `battle-above-the-gods-eye` (Dance of Dragons),
   `battle-on-the-river-slayne` (Coming of Andals), `aegons-conquest`,
   `roberts-rebellion` keep showing up as candidates for current-narrative mints
   (ASOS/ADWD). Matt's call: **add an `era:` property to nodes going forward,
   don't backfill retroactively.** Suggested values: `era: pre-conquest |
   age-of-heroes | targaryen-conquest | targaryen-rule | dance-of-dragons |
   roberts-rebellion | current-narrative`. The narrowing function then weights
   `era=current-narrative` higher when classifying current-narrative mints.

4. **Missing canonical event-nodes — partial list confirmed via wiki cache grep:**
   - ✓ **`fight-at-the-holdfast` ALREADY EXISTS** in `graph/nodes/events/` — the Yoren death scene. The Plate 4 classifier correctly linked 4 mints to it (arya-captured, arya-frees-the-prisoners, gendry-captured, lommy-yields-and-is-killed). False alarm.
   - ✓ `Inn_at_the_Crossroads.json` exists as a LOCATION page (not event). The "capture of Tyrion at crossroads" event could be minted FROM that location's context.
   - ✗ **No wiki page for Robert's boar-hunt assassination** — genuine canon gap. Wiki's `Death_of_Robert_I_Baratheon` may exist as a sub-section of `Robert_I_Baratheon`'s biography but not as its own page.
   - ✗ **No wiki page for the Stannis-approach Winterfell murders** (`Yellow_Dick` and `Little_Walder_Frey` exist as character pages but no event page).
   - Mountain_clans_of_the_Vale exists as a faction page. The specific "Tyrion's Vale clansmen attack" beat has no event page.

   For the 2-3 genuine gaps: either (a) define a workflow for promoting
   well-attested Plate-3 mints to canonical event-nodes (different from the
   chapter-beat sub-tier), OR (b) accept them as the "chapter-beat" tier and
   live with it.

These 4 should be folded into the alias-resolver-design memo as related
infrastructure improvements, or carved out as a separate "wiki-layer cleanup"
follow-on prompt.

## Out of scope

- Don't actually implement the alias-resolver extension in this session (that's
  follow-on Python work). Decide first, code later.
- Don't build the chat UI itself. This session just defines the display policy.
- Don't touch `graph/` files. Schema docs only.

## Sequence

1. Read the listed files + memory entries.
2. Sample 30-50 Pass-1 extraction files for canonical event-name mentions; count.
3. Sample the wiki cache for redirect counts per category (persons, houses,
   locations) to estimate alias-harvest payoff.
4. Write `reference/alias-resolver-design.md` (~300-500 words) answering Q1.
5. Append "Display Names" section to `reference/architecture.md` answering Q2.
6. Update worklog with one-paragraph entry covering the design decisions.

If either question turns out to be much bigger than expected, write the design
memo first and queue implementation for a follow-on prompt.
