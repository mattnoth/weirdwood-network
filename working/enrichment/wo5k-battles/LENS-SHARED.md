# Shared lens instructions — A2.5 WO5K-battles enrichment (S163, PASS 1)

You are one of four parallel "lens" subagents enriching the **Weirwood Network**, a structured knowledge graph
for A Song of Ice and Fire. We are doing an **enrichment dip** on the **A2.5 WO5K-battles arc** — the military
arc that makes Robb Stark the Young Wolf. **THIS IS PASS 1** of a multi-pass mini-track. PASS-1 scope = **Robb's
Riverlands-relief rise**: the **Whispering Wood** (Robb's night-trap; **Jaime Lannister captured**) → the **Battle
of the Camps** (the Lannister siege of Riverrun broken; Riverrun relieved) → the seam into **Robb proclaimed King
in the North** at the Riverrun war council. The battles are **NON-POV — reported through Catelyn Stark's AGOT
chapters.** This is a **BUILD + ENRICH with a HEAVY dedup**: the cast's dyad web is saturated (Catelyn 119 core-out
edges, Jaime 157) and the Camps / Green-Fork / siege-of-Riverrun / king-in-the-north hubs are already built — but
the **WHISPERING WOOD BATTLE HAS NO EVENT NODE** and the **causal spine is empty** (only 2 causal edges in the whole
cluster). Aim your proposals at the **GAPS** in `baseline.md`, NOT the dense dyadic web — **the dedup WILL kill many
proposals.**

**YOU PROPOSE — YOU DO NOT MINT.** Your output is a proposal file. An Opus orchestrator will synthesize all four
lenses, decide what to mint, line-check every quote, and a separate fresh-verify subagent will adjudicate the
interpretive/causal edges. Over-propose slightly; the gate is downstream.

## FIRST: read these (they are the ground truth — dedup against them)
1. `working/enrichment/wo5k-battles/baseline.md` — the scope, the PASS-1 cut, the DEDUP hot zones (the live
   S100/S113/S159 web + the saturated dyad web), the GAPS (your targets — the Whispering Wood node + the causal
   spine), the chapter map, the suspicious-existing-edges flags, and the DO-NOT list. **Every node/edge you propose
   MUST be deduped against the existing web.** If an edge already exists, do NOT re-propose it.
2. Your assigned chapter files (listed in your specific prompt). Read them IN FULL. **Quotes must be VERBATIM and
   carry a `chapter:line` cite** (e.g. `agot-catelyn-10.md:88` → cite as `agot-catelyn-10:88`). A quote must be a
   single contiguous substring of ONE line's text — never splice across a `," said X, "` attribution, never stitch
   two lines together. (Chapter files live at `sources/chapters/agot/<chapter>.md`; lines are numbered — read with
   line numbers so you can cite exactly.)

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
- **Causal ladder (honor it — load-bearing; this is the high-value work this pass):**
  - `TRIGGERS` = immediate spark, B is the very next beat, nothing decisional between.
  - `CAUSES` = A produces B, mediation allowed.
  - `ENABLES` = A is a **precondition** that makes B *possible* but a free choice / third party actually produces B
    (the relief valve for the "sequence trap"). **This is the right edge for the relief-rise spine** — the
    Green-Fork feint ENABLES the Whispering Wood (Robb *chose* to spring the trap); the Whispering Wood ENABLES the
    Camps (the leaderless host *was* overrun, but by Robb's free assault); the Camps ENABLES the King-in-the-North
    proclamation (the lords *chose* to crown him). Do NOT use CAUSES for these — they are military preconditions,
    not forced consequences.
  - `MOTIVATES` = drives an *actor's* decision; **target is a CHARACTER, never an event.**
- **Reification roles on an event hub** (use these to BUILD the Whispering Wood node and to add missing roles):
  `AGENT_IN` (performed the act), `VICTIM_IN` (had it done to them — Jaime captured, Lannister knights cut down),
  `COMMANDS_IN` (commander / orderer — Robb sprang the trap, the Blackfish led the van/screen), `FIGHTS_IN`
  (combatant — the northern lords, Grey Wind), `WITNESS_IN` (load-bearing PERCEPTION of a charged incident — emit
  ONLY when the prose shows the character actually SEES it; Catelyn waits OUTSIDE the wood and only HEARS it, so she
  is NOT a witness to the battle itself), `PARTICIPATES_IN` (non-combat involvement). When you propose the NEW
  `battle-of-the-whispering-wood` node, give it its participant roles + a `LOCATED_AT whispering-wood` + at least
  one causal in (green-fork ENABLES) and one causal out (ENABLES camps).
- **`CAPTURES` / `PRISONER_OF`** — the Jaime-capture dyads ALREADY EXIST (see baseline; some may be WRONG — e.g.
  `roose-bolton CAPTURES jaime` looks wrong, Roose was at the Green Fork). If you build the Whispering Wood node,
  attach `jaime VICTIM_IN battle-of-the-whispering-wood` + `robb AGENT_IN/COMMANDS_IN` rather than re-proposing a
  bare CAPTURES dyad. FLAG the suspicious existing CAPTURES edges (don't silently re-mint over them).
- **`DEFEATS`** (victor → defeated) for the battle outcome (robb DEFEATS jaime, or robb's host DEFEATS the Lannister
  host). **`BESIEGES`** (besieger → location) for Jaime besieging Riverrun (check if it already exists first).
- **`MANIPULATES`** (Tier-1, REQUIRES a qualifier: `via_bribe / via_flattery / via_false_information / via_threat /
  via_seduction / unknown`). Probably not load-bearing this pass; use only if the text genuinely supports a
  using-as-a-tool (it usually does not for a clean military victory).
- **`SUSPECTED_OF`** (Tier-2, NEVER Tier-1) = a character suspected of being the agent/cause of an event the
  published text does NOT prove. **The Whispering Wood / Camps are clean military victories — the whodunit here is
  THIN.** (The deliberate-Bolton-sacrifice question belongs to **Duskendale, which is PASS 3** — do NOT reach for it
  now.) Be HONEST: propose a SUSPECTED_OF only if the text genuinely plants pointed-but-unproven agency. Default to
  proposing none.
- Tier-1 REQUIRED-qualifier types (only if you propose them): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,
  HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO. Tier-3 types must NOT carry a qualifier.

## HARVEST (split the bar WIDE OPEN on food — Matt's standing rule)
While reading, drop one-line pointers to notable-but-not-an-edge finds into your proposal's `## Harvest` section:
`| kind | book | chapter:line | note |`. Capture EVERY meal/eating/food/drink moment — **camp provisioning, a host's
rations on the march, any victory-feast or hospitality at Riverrun, the dreamwine / milk-of-the-poppy Hoster is
given.** Also capture: load-bearing verbatim quotes (for node `## Quotes` — the Greatjon's "King in the North", the
hush of the Whispering Wood, "Riverrun is free again", Grey Wind at the kill, the dying Hoster watching the torches
from the battlements), vivid physical descriptions (the moonlit wood and the carpet of dead leaves, the night march,
the three Lannister siege camps, the burning siege towers, Jaime brought in irons, Grey Wind's red eyes). POINT,
don't extract — a later harvest pass attaches them.

## OUTPUT — write your proposal to `working/enrichment/wo5k-battles/lens-<X>.md`
(where `<X>` is your lens letter, given in your prompt). Structure:

```
# Lens <X> — <name> — A2.5 WO5K-battles proposal (S163, PASS 1)

## Proposed NEW nodes
For each: slug (kebab-case) · name · type (from the entity hierarchy, e.g. event.battle / event.incident /
character.human / object.artifact / place.location) · 1-2 sentence body summary · the verbatim anchor quote +
chapter:line.

## Proposed NEW edges
A table or list, each row:  source_slug  [EDGE_TYPE]  target_slug  | Tier-N | qualifier(if Tier-1 type) |
verbatim quote "<...>" + chapter:line | one-line rationale.
Mark any edge you are UNSURE about as **[BORDERLINE]** so the gate scrutinizes it.

## Dropped / considered-but-rejected
What you considered and why you did NOT propose it (already exists / show-only / theory-gated / agency-collapse /
TWOW-only / pure-travel-not-causal / PASS-2-or-3-scope).

## Harvest
The | kind | book | chapter:line | note | table.
```

Return a SHORT summary as your final message (counts + your 2-3 highest-value proposals). The file is the deliverable.

## HARD RULES (violating these = your proposal gets dropped at the gate)
- **Dedup** against baseline.md's live web — do not re-propose existing edges or the dense dyadic web. The dedup is
  EXPECTED to kill many proposals; aim at the GAPS (the Whispering Wood node + the causal spine).
- **Verbatim quotes only**, single contiguous substring of one line, with `chapter:line`. If you can't find the line,
  don't propose the edge.
- **No theory assertions (GATED):** no theory readings. Evidence/act/MOTIVATES→character edges only.
- **No TWOW / unpublished material.** Only the 5 published books.
- **No container tag** in your proposal (the synthesis decides). NOTE: `wo5k` IS an approved container and these
  battles ARE WO5K-trigger-tree beats — but you still leave the tagging to synthesis.
- **No show-canon** — only beats in the BOOK text (quote it from your assigned chapter files or don't propose it).
- **PASS 1 ONLY** — do NOT reach into Oxcross (PASS 2) or the Fords/Duskendale (PASS 3). If you notice a strong
  PASS-2/3 thread, NOTE it in `## Dropped` for the later pass; do not propose it.
- Honor the ENABLES-vs-CAUSES contract; route human choices through MOTIVATES(→character), not a false A-CAUSES-B.
