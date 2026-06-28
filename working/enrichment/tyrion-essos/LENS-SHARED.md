# Shared lens instructions — A2.4 Tyrion / Essos enrichment (S161)

You are one of four parallel "lens" subagents enriching the **Weirwood Network**, a structured knowledge graph
for A Song of Ice and Fire. We are doing an **enrichment dip** on the **A2.4 Tyrion / Essos arc** — Tyrion's
ADWD journey from the murder of Tywin to the gates of Meereen: the Pentos sojourn with Illyrio, the Shy Maid
river-voyage down the Rhoyne with Young Griff / Jon Connington (Griff) / Haldon / Lemore / Duck, the stone men
of the Bridge of Dream and the greyscale scare, the capture by Jorah Mormont, Volantis, the slaver's sale to
Yezzan zo Qaggaz with the dwarf **Penny**, the **pale mare** (bloody flux) sweeping the Yunkish camp, and
joining the **Second Sons** at the Meereen siege lines. **The POV is Tyrion throughout.** This is a
**BUILD + ENRICH with a HEAVY dedup**: Tyrion's dyad web is saturated (224 core-out edges) and the Shy-Maid
household + Meereen destination are ALREADY built (S147 AEGON, S144 Daenerys/Meereen). Aim your proposals at the
**GAPS** in `baseline.md` (the islanded event hubs + the beats that exist only as bare dyad edges), NOT the dense
dyadic web — **the dedup WILL kill many proposals.**

**YOU PROPOSE — YOU DO NOT MINT.** Your output is a proposal file. An Opus orchestrator will synthesize all four
lenses, decide what to mint, line-check every quote, and a separate fresh-verify subagent will adjudicate the
interpretive/causal edges. Over-propose slightly; the gate is downstream.

## FIRST: read these (they are the ground truth — dedup against them)
1. `working/enrichment/tyrion-essos/baseline.md` — the scope, the DEDUP hot zones (the live S147/S144/S109 web),
   the GAPS (your targets), the chapter map, and the DO-NOT list. **Every node/edge you propose MUST be deduped
   against the existing web.** If an edge already exists, do NOT re-propose it.
2. Your assigned chapter files (listed in your specific prompt). Read them IN FULL. **Quotes must be VERBATIM and
   carry a `chapter:line` cite** (e.g. `adwd-tyrion-07.md:218` → cite as `adwd-tyrion-07:218`). A quote must be a
   single contiguous substring of ONE line's text — never splice across a `," said X, "` attribution, never
   stitch two lines together. (Chapter files live at `sources/chapters/adwd/<chapter>.md`; lines are numbered —
   read with line numbers so you can cite exactly.)

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
  choice / third party actually produces B (the relief valve for the "sequence trap"). `MOTIVATES` = drives an
  *actor's* decision; **target is a CHARACTER, never an event.** Use MOTIVATES to route Tyrion's choices (his
  drunken self-destruction, his decision to slip the leash at Selhorys, his scheming his way into the Second
  Sons), Jorah's decision to seize Tyrion (to win back Daenerys's favour), Penny's grief — instead of collapsing
  them into a false event-CAUSES-event.
- **The journey is a SEQUENCE, not a causal chain.** Tyrion moving Pentos → Rhoyne → Volantis → the slave camp →
  Meereen is mostly travel. Do NOT mint a false `arrival-at-X CAUSES arrival-at-Y` ladder. Use `ENABLES` only
  where a beat genuinely makes the next *possible* (the shipwreck ENABLES the slaver capture; the pale mare
  killing Yezzan ENABLES the escape-to-the-Second-Sons). Use `TRAVELS_TO` (person → destination) for the moves.
  Prefer reifying the few CONSEQUENTIAL beats (the Jorah capture, the sale, the flux, the joining) as their own
  `event.incident` nodes with a LOCATED_AT + at least one causal in/out, and leave pure travel as node-prose.
- **Reification roles on an event hub:** `AGENT_IN` (performed the act), `VICTIM_IN` (had it done to them),
  `COMMANDS_IN` (orderer who didn't personally execute), `WIELDED_IN` (artifact→event instrument), `WITNESS_IN`
  (load-bearing PERCEPTION of a charged/violent incident — emit ONLY when the prose shows the character actually
  SEES it), `PARTICIPATES_IN` (non-combat involvement). When you mint a NEW event node, give it its participant
  roles + a LOCATED_AT + at least one causal in/out edge.
- **`CAPTURES` / `PRISONER_OF`** for the Jorah seizure (these dyads already exist — see baseline; if you mint a
  `jorah-captures-tyrion` event node, attach roles `jorah AGENT_IN`, `tyrion VICTIM_IN` rather than re-proposing
  the bare CAPTURES dyad). Same for the slaver capture (the slavers / Yezzan AGENT_IN; Tyrion + Penny + Jorah
  VICTIM_IN). `PURCHASED_FROM` (buyer → seller) if the sale-to-Yezzan names a seller.
- **`MANIPULATES`** (Tier-1, REQUIRES a qualifier: `via_bribe / via_flattery / via_false_information / via_threat /
  via_seduction / unknown`). Use ONLY for genuine using-as-a-tool, and ONLY if the text supports it (Tyrion talks
  his way into / cons the Second Sons; Tyrion plays Illyrio; etc.). `tyrion MANIPULATES aegon` already exists —
  do not re-propose.
- **`AFFLICTED_BY` greyscale** — `jon-connington AFFLICTED_BY greyscale` ALREADY exists (S147). The stone-men beat
  is *where* he was infected (pulling Tyrion from the river). Tyrion is NOT infected (he fears it, washes
  obsessively) — do NOT give Tyrion an AFFLICTED_BY edge. The seam to surface is causal/temporal: the attack →
  Jon Connington's affliction; surface it for the wiring lens, but mind that AFFLICTED_BY is a state, not an event.
- **`SUSPECTED_OF`** (Tier-2, NEVER Tier-1) = a character suspected (in-world or by reader) of being the agent/
  cause of an event the published text does NOT prove. Propose only for genuinely new pointed-but-unproven agency
  the text supports. Do not over-reach (the whodunit here is mostly Illyrio's true game + Jorah's motive — much of
  which is theory-gated; keep readings as node-prose, propose only act/evidence edges).
- **`SUB_BEAT_OF`** (beat → parent event) — for grouping new beats under a parent (e.g. the dwarf-show or the
  pale-mare beat under the Yunkish-siege/slave-camp event if you mint one). But consequential beats should also
  carry causal edges; prefer reifying them as their own `event.incident` nodes.
- Tier-1 REQUIRED-qualifier types (only if you propose them): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,
  HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO. Tier-3 types must NOT carry a qualifier.

## HARVEST (split the bar WIDE OPEN on food — Matt's standing rule)
While reading, drop one-line pointers to notable-but-not-an-edge finds into your proposal's `## Harvest` section:
`| kind | book | chapter:line | note |`. Capture EVERY meal/eating/food/drink moment — Illyrio's lavish Pentoshi
feasts (the spiced honeyed locusts, the lamprey pie, the suckling pig, the candied ginger), the cheesemonger's
wine, the shipboard rations on the Shy Maid and the Selaesori Qhoran, the salt beef and hardbread, the
slave-camp gruel and dog stew, the dwarf-show meals, what the flux does to the camp. Also capture: load-bearing
verbatim quotes (for node `## Quotes`), vivid physical descriptions (Illyrio's yellow beard and rings, the
fat man's litter, the Shy Maid's painted hull, the Bridge of Dream, the stone men's grey cracked flesh,
Tyrion's mushrooms in his boot, Penny's dog Pretty Pig and her sow, the pale mare's bloody stool, Tyrion's
nose-stump, the lord-of-the-ham cyvasse pieces). POINT, don't extract — a later harvest pass attaches them.

## OUTPUT — write your proposal to `working/enrichment/tyrion-essos/lens-<X>.md`
(where `<X>` is your lens letter, given in your prompt). Structure:

```
# Lens <X> — <name> — A2.4 Tyrion / Essos proposal (S161)

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
TWOW-only / pure-travel-not-causal).

## Harvest
The | kind | book | chapter:line | note | table.
```

Return a SHORT summary as your final message (counts + your 2-3 highest-value proposals). The file is the deliverable.

## HARD RULES (violating these = your proposal gets dropped at the gate)
- **Dedup** against baseline.md's live web — do not re-propose existing edges or the dense dyadic web. The dedup is
  EXPECTED to kill many proposals; aim at the GAPS.
- **Verbatim quotes only**, single contiguous substring of one line, with `chapter:line`. If you can't find the
  line, don't propose the edge.
- **No theory assertions (GATED):** Aegon-is-real / fAegon, Illyrio's true parentage game, any prophecy /
  Moqorro-fire reading. Evidence/act/MOTIVATES→character edges only — the readings stay node-prose.
- **No TWOW / unpublished material.** Only the 5 published books. ADWD ends with Tyrion JOINING the Second Sons —
  the turning-their-cloaks-BACK is TWOW; do NOT propose it as an edge.
- **No container tag** in your proposal (the synthesis decides). NOTE: unlike some arcs, `essos` IS an approved
  container and these beats ARE Essos-set — but you still leave the tagging to synthesis.
- **No show-canon** — only beats in the BOOK text (quote it from your assigned chapter files or don't propose it).
- Honor the ENABLES-vs-CAUSES contract; route human choices through MOTIVATES(→character), not a false A-CAUSES-B.
  The journey is mostly a SEQUENCE — do not fabricate a causal ladder out of travel.
