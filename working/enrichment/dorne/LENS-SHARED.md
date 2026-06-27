# Shared lens instructions — A1.5 Dorne / Queenmaker enrichment (S156)

You are one of four parallel "lens" subagents enriching the **Weirwood Network**, a structured knowledge graph
for A Song of Ice and Fire. We are doing an **enrichment dip** on the **A1.5 Dorne / Queenmaker arc** —
deepening an already-built but thin skeleton with the conspiracy side-plots, the seduction/whodunit layer, the
descriptive/object depth, and the cross-arc causal seams the first pass (S117) missed. **No POV is Dornish-core;**
the arc is told across Areo Hotah / Arys Oakheart / Arianne Martell POVs. The Dorne spine was built S117 (the
Queenmaker plot) with **0 enrichment dips** — so this is **WIRE + ENRICH** on a thin 9-edge causal spine + an
under-wired conspirator web. The dedup pull found **196 internal edges but only 9 internal causal edges**. Aim
your proposals at the GAPS in `baseline.md`, **not** the dense dyadic web — **the dedup WILL kill many proposals.**

**YOU PROPOSE — YOU DO NOT MINT.** Your output is a proposal file. An Opus orchestrator will synthesize all four
lenses, decide what to mint, line-check every quote, and a separate fresh-verify subagent will adjudicate the
interpretive/causal edges. Over-propose slightly; the gate is downstream.

## FIRST: read these (they are the ground truth — dedup against them)
1. `working/enrichment/dorne/baseline.md` — the scope, the 196-edge existing web (the DEDUP list), the 9-edge
   causal spine, the GAPS (your targets), and the DO-NOT list. **Every node/edge you propose MUST be deduped
   against the existing web.** If an edge already exists, do NOT re-propose it.
2. Your assigned chapter files (listed in your specific prompt). Read them in full. **Quotes must be VERBATIM
   and carry a `chapter:line` cite** (e.g. `affc-the-queenmaker-01.md:267` → cite as `affc-the-queenmaker-01:267`).
   A quote must be a single contiguous substring of ONE line's text — never splice across a `," said X, "`
   attribution, never stitch two lines together. (Chapter files live at `sources/chapters/<book>/<chapter>.md`;
   lines are numbered. The 5 in-scope chapters are listed in baseline.md.)

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
  choice/third party actually produces B (the relief valve for the "sequence trap"). `MOTIVATES` = drives an
  *actor's* decision; **target is a CHARACTER, never an event.** Use MOTIVATES to route Arianne's grievance,
  Doran's long-game patience, Arys's shame, instead of collapsing them into a false event-CAUSES-event.
- **Reification roles on an event hub:** `AGENT_IN` (the one who performed the act), `VICTIM_IN` (the one it was
  done to), `COMMANDS_IN` (orderer who didn't personally execute), `WIELDED_IN` (artifact→event instrument),
  `WITNESS_IN` (load-bearing PERCEPTION of a charged/violent/secret incident — emit ONLY when the prose shows the
  character actually SEES it; present-but-shielded does NOT qualify), `PARTICIPATES_IN` (non-combat involvement).
- `MANIPULATES` (Tier-1, REQUIRES a qualifier from `via_bribe / via_flattery / via_false_information / via_threat /
  via_seduction / unknown`). **Arianne's seduction of Arys = `arianne MANIPULATES arys-oakheart` qualifier
  `via_seduction`** — there is NO `SEDUCES` type; this is how seduction-as-instrument is modeled. (The `LOVER_OF`
  edge already exists — MANIPULATES adds the using-him-as-a-tool layer.)
- `SUSPECTED_OF` (Tier-2, NEVER Tier-1) = a character is suspected (in-world or by reader) of being the agent/cause
  of an event the published text does NOT prove. **The informer-mystery lens lives here** — propose SUSPECTED_OF
  ONLY for what the text genuinely points at; do NOT assert an informer the text leaves unproven.
- `BREAKS_VOW` (vow-breaker → vow-recipient) for Arys breaking his Kingsguard oath. `MARRIES_OFF` (arranger →
  married-off person) for Doran marrying Sylva off to Greenstone. `CLAIMS` (claimant → claimed) for Myrcella's
  Iron-Throne claim under Dornish law. All Tier-3 except where noted (no qualifier).
- Tier-1 REQUIRED-qualifier types (only if you propose them): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,
  HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO. Tier-3 types must NOT carry a qualifier.

## HARVEST (split the bar WIDE OPEN on food — Matt's standing rule)
While reading, drop one-line pointers to notable-but-not-an-edge finds into your proposal's `## Harvest` section:
`| kind | book | chapter:line | note |`. Capture EVERY meal/eating/food/drink moment **including the Dornish
register** (blood oranges, the Water Gardens fountains, snake-and-scorpion venom, strongwine, the spiced/sour
Dornish wine, persimmons, pomegranates, Hotah's bread-and-salt, prison rations, Doran's gout-diet). Also capture:
load-bearing verbatim quotes (for node `## Quotes`), vivid physical descriptions (the spear-and-sun sigil, the
Old Palace & the Tower of the Sun, the Water Gardens' pink marble & blood-orange trees, Hotah's longaxe & cheek-
scars, Darkstar's silver hair & purple eyes & the Dayne black-sword sigil, the Spear Tower where Arianne is held,
Myrcella's ruined face). POINT, don't extract — a later harvest pass attaches them.

## OUTPUT — write your proposal to `working/enrichment/dorne/lens-<X>.md`
(where `<X>` is your lens letter, given in your prompt). Structure:

```
# Lens <X> — <name> — A1.5 Dorne proposal (S156)

## Proposed NEW nodes
For each: slug (kebab-case) · name · type (from the entity hierarchy, e.g. event.incident / event.death /
event.conspiracy / character.human / object.artifact) · 1-2 sentence body summary · the verbatim anchor quote
+ chapter:line.

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
- **Dedup** against baseline.md's 196 edges + the 9-edge causal spine — do not re-propose existing edges or the
  dense dyadic web. The dedup is EXPECTED to kill many proposals; aim at the GAPS.
- **Verbatim quotes only**, single contiguous substring of one line, with `chapter:line`. If you can't find the
  line, don't propose the edge.
- **No theory assertions (GATED):** Aegon-is-real / fAegon-is-a-Blackfyre; the full "fire and blood" Dornish-
  vengeance *prophecy* reading; any R+L-adjacent Elia/Rhaegar theory. Evidence/possession/MOTIVATES→character
  edges only — the readings stay node-prose.
- **No TWOW / unpublished nodes** (`arianne-i/ii-the-winds-of-winter`, `defenestration-of-sunspear`).
- **No show-canon** — only beats in the BOOK text (quote it from your 5 chapter files or don't propose it).
- **No container tags** in your proposal (the synthesis decides; default none — Dorne is not an approved container).
- The conspirator **GARIN HAS NO NODE** (the only `garin-*` node is the *legendary* Garin the Great — a wrong
  target). If you want to wire the conspirator Garin, PROPOSE A NEW `character.human` node for him and flag the
  existing `arianne CONSPIRES_WITH garin-the-great` edge as a bug to re-point. Do NOT silently reuse garin-the-great.
- Honor the ENABLES-vs-CAUSES contract; route human choices through MOTIVATES(→character), not a false A-CAUSES-B.
