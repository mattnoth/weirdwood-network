# Shared lens instructions — A2.6 Jaime / Riverlands enrichment (S159)

You are one of four parallel "lens" subagents enriching the **Weirwood Network**, a structured knowledge graph
for A Song of Ice and Fire. We are doing an **enrichment dip** on the **A2.6 Jaime / Riverlands arc** — Jaime's
AFFC command in the Riverlands: the inherited Riverrun siege and its resolution (Edmure's coerced surrender, the
Blackfish's escape), the Harrenhal command, the burning of Cersei's plea-for-help letter (the marquee Jaime↔Cersei
rupture), and the ASOS backstory layer (the hand-loss, the bath confession, the Brave Companions, Ice reforged into
Oathkeeper). **The POV is Jaime throughout the AFFC chapters.** This is a **BUILD + ENRICH with a HEAVY dedup**:
Jaime's dyad web is saturated (280 internal edges) but his event-causal layer is thin (only 8 causal edges) and the
**Riverrun-siege resolution is entirely unbuilt**. Aim your proposals at the GAPS in `baseline.md`, NOT the dense
dyadic web — **the dedup WILL kill many proposals.**

**YOU PROPOSE — YOU DO NOT MINT.** Your output is a proposal file. An Opus orchestrator will synthesize all four
lenses, decide what to mint, line-check every quote, and a separate fresh-verify subagent will adjudicate the
interpretive/causal edges. Over-propose slightly; the gate is downstream.

## FIRST: read these (they are the ground truth — dedup against them)
1. `working/enrichment/jaime-riverlands/baseline.md` — the scope, the DEDUP list (the live S100/S141/S142/S109 web),
   the GAPS (your targets), the chapter map, and the DO-NOT list. **Every node/edge you propose MUST be deduped
   against the existing web.** If an edge already exists, do NOT re-propose it.
2. Your assigned chapter files (listed in your specific prompt). Read them in full. **Quotes must be VERBATIM and
   carry a `chapter:line` cite** (e.g. `affc-jaime-07.md:295` → cite as `affc-jaime-07:295`). A quote must be a
   single contiguous substring of ONE line's text — never splice across a `," said X, "` attribution, never stitch
   two lines together. (Chapter files live at `sources/chapters/<book>/<chapter>.md`; lines are numbered.)

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
  *actor's* decision; **target is a CHARACTER, never an event.** Use MOTIVATES to route Jaime's choices (his
  refusal to aid Cersei; his bloodless-resolution intent), Edmure's surrender-under-duress, the Blackfish's
  defiance — instead of collapsing them into a false event-CAUSES-event.
- **Reification roles on an event hub:** `AGENT_IN` (the one who performed the act), `VICTIM_IN` (the one it was
  done to), `COMMANDS_IN` (orderer who didn't personally execute), `WIELDED_IN` (artifact→event instrument),
  `WITNESS_IN` (load-bearing PERCEPTION of a charged/violent/secret incident — emit ONLY when the prose shows the
  character actually SEES it), `PARTICIPATES_IN` (non-combat involvement). When you mint a NEW event node, give it
  its participant roles + a LOCATED_AT + at least one causal in/out edge.
- **`MANIPULATES`** (Tier-1, REQUIRES a qualifier: `via_bribe / via_flattery / via_false_information / via_threat /
  via_seduction / unknown`). Jaime coercing Edmure to surrender by threatening to trebuchet his unborn child →
  `jaime-lannister MANIPULATES edmure-tully` qualifier `via_threat` is a strong candidate (the threat is the
  mechanism that produces the surrender). Use ONLY for genuine using-as-a-tool, and ONLY if the text supports it.
- **`GIFTED_TO`** (artifact → recipient) for `oathkeeper GIFTED_TO brienne-tarth` (Jaime gives Brienne the
  Valyrian-steel sword to find Sansa — the marquee object beat). `REFORGED_INTO` (original → result) for
  `ice REFORGED_INTO oathkeeper` and `ice REFORGED_INTO widows-wail` (Tywin melts Ice in asos-jaime-08).
  `WIELDS`/`OWNS` (person → artifact) for Jaime bearing the new sword before he gives it away. `MADE_OF` (artifact →
  material) for `oathkeeper MADE_OF valyrian-steel`. **Note: oathkeeper + ice both have ZERO incoming edges — light them.**
- **`SUSPECTED_OF`** (Tier-2, NEVER Tier-1) = a character suspected (in-world or by reader) of being the agent/cause
  of an event the published text does NOT prove. Propose only for genuinely new pointed-but-unproven agency the text
  supports (e.g. did the riverlords help the Blackfish escape? Jaime suspects Vance/Piper "more like to help the
  Blackfish escape" — affc-jaime-07:45 — but this is suspicion, not proof). Do not over-reach.
- **`SUB_BEAT_OF`** (beat → parent event) — for grouping new beats under siege-of-riverrun if they are moments
  WITHIN the siege (the surrender, the escape, the gallows-burning). But the surrender/escape are consequential
  enough to also carry causal edges; prefer reifying them as their own `event.incident` nodes with CAUSES/ENABLES.
- Tier-1 REQUIRED-qualifier types (only if you propose them): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,
  HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO. Tier-3 types must NOT carry a qualifier.

## HARVEST (split the bar WIDE OPEN on food — Matt's standing rule)
While reading, drop one-line pointers to notable-but-not-an-edge finds into your proposal's `## Harvest` section:
`| kind | book | chapter:line | note |`. Capture EVERY meal/eating/food/drink moment — the Riverrun siege fare,
Jaime's camp meals, the feast Lady Genna lays, what the garrison eats, the wine at the parleys, the bleak siege
provisioning ("the Blackfish had left Riverrun amply provisioned"). Also capture: load-bearing verbatim quotes (for
node `## Quotes`), vivid physical descriptions (Jaime's golden hand, the stump of his sword hand, Oathkeeper's
red-and-black ripple & gold-lions pommel, the Tully water-gate / the boom across the Tumblestone, Riverrun rising
between the two rivers, Ryman Frey's gallows, the weirwood-and-river register of the godswood, the silent-sister
dream, the snowflake melting on Cersei's letter). POINT, don't extract — a later harvest pass attaches them.

## OUTPUT — write your proposal to `working/enrichment/jaime-riverlands/lens-<X>.md`
(where `<X>` is your lens letter, given in your prompt). Structure:

```
# Lens <X> — <name> — A2.6 Jaime / Riverlands proposal (S159)

## Proposed NEW nodes
For each: slug (kebab-case) · name · type (from the entity hierarchy, e.g. event.incident / event.battle /
character.human / object.artifact / place.location) · 1-2 sentence body summary · the verbatim anchor quote +
chapter:line.

## Proposed NEW edges
A table or list, each row:  source_slug  [EDGE_TYPE]  target_slug  | Tier-N | qualifier(if Tier-1 type) |
verbatim quote "<...>" + chapter:line | one-line rationale.
Mark any edge you are UNSURE about as **[BORDERLINE]** so the gate scrutinizes it.

## Dropped / considered-but-rejected
What you considered and why you did NOT propose it (already exists / show-only / theory-gated / agency-collapse /
TWOW-only).

## Harvest
The | kind | book | chapter:line | note | table.
```

Return a SHORT summary as your final message (counts + your 2-3 highest-value proposals). The file is the deliverable.

## HARD RULES (violating these = your proposal gets dropped at the gate)
- **Dedup** against baseline.md's live web — do not re-propose existing edges or the dense dyadic web. The dedup is
  EXPECTED to kill many proposals; aim at the GAPS.
- **Verbatim quotes only**, single contiguous substring of one line, with `chapter:line`. If you can't find the
  line, don't propose the edge.
- **No theory assertions (GATED):** Jaime-as-valonqar, any prophecy reading, the Tysha/Tywin moral readings as
  edges. Evidence/act/MOTIVATES→character edges only — the readings stay node-prose.
- **No TWOW / unpublished material.** Only the 5 published books.
- **No container tag** in your proposal (the synthesis decides; default none — the Riverlands is NOT an approved
  container; do not invent one).
- **No show-canon** — only beats in the BOOK text (quote it from your assigned chapter files or don't propose it).
- Honor the ENABLES-vs-CAUSES contract; route human choices through MOTIVATES(→character), not a false A-CAUSES-B.
