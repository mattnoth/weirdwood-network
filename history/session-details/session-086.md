---
session: 86
date: 2026-06-08
model: Opus 4.7 (orchestrator + writer; no agents delegated)
duration: extended design conversation, then commit/push/endsession
commits: c7b5c134c (S86 design work), f7667c5a1 (continue-prompt tweaks)
---

# Session 86 — Alias resolver + display-name design + post-Plate-5 backfill plan

## Purpose

Resolve the two open questions queued by S85 at end of session 2026-06-07/08:
1. Alias-as-edge-resolver scope + integration (event aliases harvested but never wired in; what about non-event types?).
2. Chat-UI display name policy (every node has `slug:` + `name:` — what surface goes where?).

Plus the 4 structural fixes Matt's 23-mint triage surfaced (27 wiki schema misclassifications, IDF downweighting, era property, missing canonical event-nodes).

## What actually happened

The session unfolded in three arcs:

**Arc 1 — Design conversation (initial pass).** Matt opened the continue prompt with inline annotations marked `--`. I worked through each annotation in order — explaining where I'd been overengineering (Q2.1 enforceability), debating where Matt pushed back (Q1.3 alias-vs-sub-beat), and showing empirical data where Matt asked for it (counting canonical event-name mentions in Pass 1: 174 "red wedding", 109 "battle of the blackwater", 293 "battle of"). The biggest exchange was Matt's pushback on my "alias = dashes-removed slug" framing — I argued (and Matt agreed) that the substitution test is the right rule: aliases preserve truth value under substitution, sub-beats are moments-within-event that do not.

**Arc 2 — Write the deliverables.** Wrote `reference/alias-resolver-design.md` (~1,200 words, the canonical design memo). Made 5 surgical edits to `reference/architecture.md`: 7 new event sub-types (event.wedding/feast/coronation/trial/assassination/execution/conspiracy), new "Node Frontmatter Conventions" section with `era:` enum, new "Display Names: slug as identifier, name as surface" section, ALIAS_OF row gets substitution-test rule, vocab count note 165→166. Updated the Plate 5 continue prompt to fold in S86 decisions. Archived Session 82 to `history/worklog-archives/archive017.md` (now full at 5/5).

Mid-write, Matt corrected me twice:
- "Sub beat definitely needs to be canonical" — I had initially folded sub-beats into the existing `PART_OF` edge type. Matt pushed for `SUB_BEAT_OF` as its own canonical type. Reasoning: `PART_OF` is event-in-war scope (battle is part of war); `SUB_BEAT_OF` is beat-in-event scope (bedding-call is sub-beat of Red Wedding). Collapsing them loses query granularity. I formalized `SUB_BEAT_OF` as canonical edge type (vocab 165 → 166), distinct from `PART_OF`.
- "What is PART_OF?" — Matt didn't remember. Gave a one-table explanation, confirmed the distinction.

**Arc 3 — The backfill reframe + the S74 correction.** This was the most important arc. Matt asked: "are we ready to promote? do we need to backfill existing edges with SUB_BEAT_OF?" I gave a too-clean "0 SUB_BEAT_OF backfill needed" answer. Matt pushed back: "the edge modeling work should be applied to the existing graph — why do you think it shouldn't? If not today, then soon."

Matt was right. I reframed:
1. SUB_BEAT_OF specifically — 0 backfill, confirmed empirically (0 event→event edges in the existing graph; only 5 edges total touch any event-node).
2. But the broader edge-modeling work HAS retroactive scope beyond what I'd acknowledged. Plate 5 already includes ~50 retroactive edges (Plate 0 flips, Aerys merge, S77 cleanups, 27 schema fixes). And there's MORE retroactive work surfaced indirectly: vocab-drift retypes (existing edges built under older vocab; ~25 deterministic candidates at a sample floor, full sweep ~100-200+), reification of existing person↔person edges into event hubs (cleanroom's main carry-over; 500-1,500 candidates across 5 families: killings-at-named-occasion, sieges, ceremonies, conspiracies, VIOLATES_GUEST_RIGHT), and head-rule retroactive cleanup beyond Plate 0's 10 flips.

Wrote `working/edge-modeling/post-plate5-backfill-design.md` — 3 tracks (A/B/C), sequenced after Plate 5, each with its own precision gate.

Then Matt caught a worse error in my framing: I'd written that the backfill memo was "exempt from the S74 no-LLM-enrichment ban." Matt corrected: "S74 was NOT a permanent ban — that was a specific gate failure on a specific run. S75 amended to 'enrichment wanted, gated on precision.'" I had the right memory (`project_enrichment_wanted_events_next.md` says exactly this) and failed to recall it correctly mid-fork. Updated 4 files to correct the framing: the backfill memo (3 spots), the alias-resolver memo (1 spot), the todos HIGH entry, the worklog Session 86 entry.

**Arc 4 — Commit/push/handoff.** Matt approved Plate 5 prompt model upgrade (Sonnet → Opus per his pushback that the irreversible step warrants strongest reasoning) and the Dialogue cross-reference. Two-edit commit `f7667c5a1`. Both commits pushed.

## Key decisions

- **SUB_BEAT_OF canonical, NOT folded into PART_OF.** Distinct scopes. Vocab 165 → 166.
- **7 new event sub-types** added to `event.*` family. Fixes the missing-enum root cause behind S85's 27 wiki schema misclassifications.
- **Mint schema rename `title:` → `name:` at Plate 5 merge.** Single-tier; chapter-beat mints in `graph/nodes/events/` alongside wiki-derived.
- **`scripts/event_alias_resolver.py` to be built as separate deterministic lookup.** Not folded into `stage4_name_resolver.py` (different problem shape: events lack the person/house/location collision risk).
- **`era:` frontmatter field forward-only.** No retroactive backfill on existing 7,000+ nodes.
- **Substitution test** is the canonical rule for alias-vs-sub-beat distinction. Dashes-vs-spaces test catches surface variants only.
- **No Haiku augmentation on event_alias_resolver.** Not because of any blanket ban, but because a ~70%-precision LLM tail over a ~95%-precision deterministic lookup has no precision-gate math to win.
- **Plate 5 stays tight as scoped.** ~50 retroactive cleanups; no backfill scope creep. Each backfill track gets its own gate after Plate 5 lands.
- **Plate 5 model upgraded Sonnet → Opus 4.7.** Stakes warrant the strongest reasoning (irreversible step, judgment calls, scope additions since prompt was originally drafted).
- **S74's "no LLM enrichment" was a specific gate failure on a specific run, NOT a permanent ban.** S75 amended to "enrichment wanted, gated on precision." All future LLM-touching backfill phases pass the same precision gate. Standing rule restated everywhere.
- **Post-Plate-5 backfill: 3 tracks (A vocab-drift, B reification of existing edges into event hubs, C head-rule cleanup).** ~$25-75 total for 300-850 edges touched (6-17× Plate 5's retroactive scope). Audit-loop discipline applies (Reporter + Auditor per track).
- **Dialogue v2.1 escalation pick MUST fold in S82-S86 edge-modeling lessons.** Cross-reference added to the existing escalation-pick continue prompt.

## Corrections I owe Matt this session

1. Initial "0 backfill needed for SUB_BEAT_OF" framing was technically correct but missed the bigger backfill question. Matt caught it.
2. Cited "S74 no LLM enrichment ban" as a standing rule. It wasn't. Matt caught it. Updated 4 files.
3. Initial alias-vs-sub-beat framing was muddled — Matt's "dashes test" pushback forced me to articulate the substitution test cleanly.
4. Sonnet recommendation for Plate 5 was a "cheapest viable" reflex without weighing stakes. Matt pushed back; upgraded to Opus.
5. "Plate" terminology — Matt asked why I picked it. I didn't; an S83 Opus orchestrator did. Honest answer: I was using an inherited name without thinking about whether it scaled.

## Files touched

**Created:**
- `reference/alias-resolver-design.md` (~1,200 words, canonical S86 design memo)
- `working/edge-modeling/post-plate5-backfill-design.md` (3-track backfill plan)
- `history/session-details/session-086.md` (this file)

**Edited:**
- `reference/architecture.md` (5 surgical inserts: 7 event sub-types in hierarchy + Type Reference Table; `SUB_BEAT_OF` row near `PART_OF`; `ALIAS_OF` substitution test; vocab count note; new Node Frontmatter Conventions + Display Names sections)
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` (S86 decisions folded; model upgraded Sonnet → Opus)
- `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` (prereq #4 added: fold in edge-modeling lessons)
- `working/todos.md` (new HIGH backfill entry + S86 line on alias-design)
- `worklog.md` (Session 86 entry + late-session fork addendum; Session 82 removed to archive)

**Archived:**
- Session 82 → `history/worklog-archives/archive017.md` (archive017 now full at 5/5)

## Graph state

Unchanged. `edges.jsonl` = 3,811. `graph/nodes/events/` = 371. `git status graph/` clean.

## What's next

→ Plate 5 merge (single-session, **Opus 4.7**, irreversible step). Existing prompt at `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` — updated with S86 decisions.

After Plate 5 lands, the post-Plate-5 backfill work begins per `working/edge-modeling/post-plate5-backfill-design.md`. 3 tracks, each with its own gate. Pass 1 chapter re-extraction stays off the table.

Other deferred items recorded:
- `scripts/event_alias_resolver.py` build (follow-on)
- Wiki-redirect harvest extension to non-event types
- IDF weighting in `plate4-wiki-cluster.py`
- `scripts/wiki-pass2-triage.py` entity-type map update + `scripts/wiki-event-type-validator.py` build (prevention for the 27-misclassification root cause)
- Dialogue v2.1 escalation pick (existing, now with edge-modeling lessons cross-ref)

## Note on `2026-06-08-alias-and-display-design.md`

Matt had this continue prompt open in the IDE and was editing it during the session (visible in git status as a modified file with ~200-line change). I did NOT commit those edits — they're Matt's WIP and not mine to commit. If the prompt was being retired (the diff suggests substantial trim), Matt can finalize that on his side. Otherwise it's preserved as-is in working tree.
