# Shared lens instructions — D5 Arya/Harrenhal enrichment (S154)

You are one of four parallel "lens" subagents enriching the **Weirwood Network**, a structured knowledge graph
for A Song of Ice and Fire. We are doing an **enrichment dip** on the **D5 "Arya's flight & Harrenhal" event
cluster** — deepening an already-built skeleton with the side-plots, revelation-events, descriptive/object depth,
and causal wiring that the first pass missed.

**YOU PROPOSE — YOU DO NOT MINT.** Your output is a proposal file. An Opus orchestrator will synthesize all four
lenses, decide what to mint, line-check every quote, and a separate fresh-verify subagent will adjudicate the
interpretive/causal edges. Over-propose slightly; the gate is downstream.

## FIRST: read these (they are the ground truth — dedup against them)
1. `working/enrichment/d5-arya-harrenhal/baseline.md` — the scope, the 146 existing internal edges, the dead-ends/
   gaps, and the DO-NOT list. **Every node/edge you propose MUST be deduped against the existing web in baseline.md.**
   If an edge already exists, do NOT re-propose it.
2. Your assigned chapter files (listed in your specific prompt). Read them in full. **Quotes must be VERBATIM and
   carry a `chapter:line` cite** (e.g. `acok-arya-09:212`). A quote must be a single contiguous substring of one
   line's text — never splice across a `," said X, "` attribution, never stitch two lines together.

## Canonical vocabulary (use these words in your prose; they are project terms — subagents don't load CLAUDE.md)
- **Pass** = a big numbered sweep over the whole corpus. **Track** = a named chunk of work. **step** (lowercase) =
  an ordered piece inside a track. **Tier** = confidence rating 1–5 ONLY (never used for work/process).
- Confidence Tiers: **Tier 1** = verified canon (verbatim book quote proves it); **Tier 2** = strong inference /
  cross-book deduction / unproven-but-load-bearing; **Tier 3** = looser structural/temporal. Tag every proposed edge.

## The LOCKED edge-type vocabulary (170 types — use ONLY these; inventing a type = rejected)
ADVISES, AFFLICTED_BY, AGENT_IN, ALIAS_OF, ALLIES_WITH, ANCESTOR_OF, ANCESTRAL_WEAPON_OF, APPEARS_TO_FULFILL,
APPOINTS, ASSAULTS, ATTACKS, ATTENDS, BANISHES, BESIEGES, BESTOWS_KNIGHTHOOD_ON, BETRAYS, BETROTHED_TO, BONDED_TO,
BORN_AT, BREAKS_VOW, BUILT, BURIED_AT, CADET_BRANCH_OF, CAPTAIN_OF, CAPTURES, CAUSES, CITED_BY, CLAIMS, CLERGY_OF,
COMMANDS, COMMANDS_IN, COMPANION_OF, CONSPIRES_WITH, CONTEMPORARY_WITH, CONTRACTED_WITH, CONTRADICTS, CONTRASTS,
COURTS, COUSIN_OF, CREW_OF, CROWNS_QUEEN_OF_LOVE_AND_BEAUTY, CULTURE_OF, CURSES, DECEIVED_BY, DECEIVES, DEFEATS,
DEPICTED_IN, DEPOSES, DIED_AT, DIED_OF, DISGUISED_AS, DISTRUSTS, DREAMS_OF, DUELS, ECHOES, ENABLES, ENCOUNTERS,
EXECUTED_WITH, EXECUTES, FEARS, FIGHTS_IN, FORESHADOWS, FORGED_BY, FOUNDED, FULFILLS, GIFTED_TO, GRANTS_SAFE_CONDUCT,
GUARDS, GUEST_OF, HATES, HEALS, HEIR_TO, HELD_BY, HOARDS, HOLDS_TITLE, HONORED_AT, IGNORANT_OF, IMPERSONATES,
IMPRISONED_AT, IMPRISONS, INFORMS, INHERITED_BY, INVESTIGATES, IN_LAW_OF, KILLED_BY, KILLED_WITH, KILLS, KNIGHTED_BY,
LOCATED_AT, LOOTED_BY, LOVER_OF, LOVES, MADE_OF, MANIPULATES, MARRIES_OFF, MEMBER_OF, MILK_BROTHER_OF, MOTIVATES,
MOURNS, NAMED_AFTER, NEGOTIATES_WITH, NEPHEW_OF, NURSED_BY, OFFICIATES, OPPOSES, OVERLORD_OF, OWNS, PARALLELS,
PARENT_OF, PARTICIPATES_IN, PART_OF, PERCEIVED_AS, POISONS, PRACTICES, PRECEDES, PREVENTS, PRISONER_EXCHANGE_FOR,
PRISONER_OF, PROPHESIED_BY, PROPOSED_AS_BRIDE, PROTECTS, PURCHASED_FROM, RANSOMS, REFORGED_INTO, REGION_OF,
REPUTED_AS, RESCUES, RESENTS, RESPECTS, RESURRECTS, REVEALS_TO, RULES, SACRED_TO, SACRIFICES, SAME_AS, SEAT_OF,
SEEKS, SERVES, SIBLING_OF, SPIES_ON, SPOUSE_OF, STEP_CHILD_OF, STEP_PARENT_OF, SUBJECT_OF_PROPHECY, SUBVERTS,
SUBVERTS_PROPHECY, SUB_BEAT_OF, SUCCEEDS, SUPPORTS, SUSPECTED_OF, SWORN_TO, TEACHES, TORTURES, TRAVELS_TO,
TRAVELS_WITH, TRIGGERS, TRUSTS, TUTORS, UNCLE_OF, VICTIM_IN, VIOLATES_GUEST_RIGHT, VOWS_TO, WARD_OF, WARGS_INTO,
WET_NURSE_OF, WIELDED_IN, WIELDS, WITNESS_IN, WORSHIPS, WRITTEN_BY

### Edge-type usage notes that matter for THIS arc
- **Causal ladder (honor it — load-bearing):** `TRIGGERS` = immediate spark, B is the very next beat.
  `CAUSES` = A produces B, mediation allowed. `ENABLES` = A is a precondition that makes B *possible* but a free
  choice/third party actually produces B (the relief valve for the "sequence trap" — a journey's place→place
  transitions are ENABLES, never CAUSES). `MOTIVATES` = drives an *actor's* decision; **target is a CHARACTER, never an event.**
- **Reification roles on an event hub:** `AGENT_IN` (the one who performed the act), `VICTIM_IN` (the one it was
  done to), `COMMANDS_IN` (orderer who didn't personally execute), `WIELDED_IN` (artifact→event instrument),
  `WITNESS_IN` (load-bearing PERCEPTION of a charged/violent/secret incident — emit ONLY when the prose shows the
  character actually SEES it; present-but-shielded does NOT qualify), `PARTICIPATES_IN` (non-combat involvement),
  `LOCATED_AT` (event→place). `FIGHTS_IN` = combatant in a battle.
- `SUSPECTED_OF` (Tier-2, NEVER Tier-1) = a character is suspected (in-world or by reader) of being the agent/cause
  of an event the published text does NOT prove. Use for unproven-but-load-bearing agency.
- `SUB_BEAT_OF` = a finer beat is a moment within a larger event hub (beat→parent). NOT for surface aliases.
- `KILLED_WITH` = victim→named weapon (combat death by a named artifact, e.g. the stableboy KILLED_WITH needle).
  `WIELDED_IN` = artifact→event. `TORTURES` = torturer→tortured-person.

## HARVEST (split the bar WIDE OPEN on food — Matt's standing rule)
While reading, drop one-line pointers to notable-but-not-an-edge finds into your proposal's `## Harvest` section:
`| kind | book | chapter:line | note |`. Capture EVERY meal/eating/food/drink moment **including the grim register**
(starvation, rats, bark, weasel-soup, prison rations, what the Brave Companions eat) — Matt wants maximal food
capture. Also capture: load-bearing verbatim quotes (for node `## Quotes`), vivid physical descriptions (Harrenhal's
cursed melted towers, the bear pit, the dragon skulls, Needle, the iron coin), hospitality moments, and
foreshadowing. POINT, don't extract — a later harvest pass attaches them.

## OUTPUT — write your proposal to `working/enrichment/d5-arya-harrenhal/lens-<X>.md`
(where `<X>` is your lens letter, given in your prompt). Structure:

```
# Lens <X> — <name> — D5 Arya/Harrenhal proposal (S154)

## Proposed NEW nodes
For each: slug (kebab-case) · name · type (from the entity hierarchy, e.g. event.death / event.incident /
event.deception / event.battle / object.artifact) · 1-2 sentence body summary · the verbatim anchor quote + chapter:line.

## Proposed NEW edges
A table or list, each row:  source_slug  [EDGE_TYPE]  target_slug  | Tier-N | qualifier(if Tier-1 type) |
verbatim quote "<...>" + chapter:line | one-line rationale.
Mark any edge you are UNSURE about as **[BORDERLINE]** so the gate scrutinizes it.

## Dropped / considered-but-rejected
What you considered and why you did NOT propose it (already exists / show-only / theory-gated / agency-collapse).

## Harvest
The | kind | book | chapter:line | note | table.
```

Return a SHORT summary as your final message (counts + your 2-3 highest-value proposals). The file is the deliverable.

## HARD RULES (violating these = your proposal gets dropped at the gate)
- **Dedup** against baseline.md's 146 edges — do not re-propose existing edges or the dense cast relationship web.
- **Verbatim quotes only**, single contiguous substring, with `chapter:line`. If you can't find the line, don't propose the edge.
- **No theory assertions** (GATED): Faceless-Men cosmology / valar-morghulis-as-religion / Jaqen's true identity /
  Jaqen=alchemist-at-Oldtown / the coin-as-magic. The coin + "valar morghulis" + the face-change are TEXT EVENTS
  (propose the events + possession/agency edges); the theology/identity stays node-prose, evidence-only.
- **No show-canon** — only beats that are in the BOOK text (check every beat against your chapters; HBO invented things
  the books don't have — e.g. don't propose anything you can't quote from the chapter files).
- **No container tags** (the synthesis decides; default none for D5).
- Honor the ENABLES-vs-CAUSES contract; route human choices through MOTIVATES(→character), not a false A-CAUSES-B.
