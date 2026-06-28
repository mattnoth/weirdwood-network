# Shared lens instructions — A2.5 WO5K-battles enrichment (S164, PASS 2 — the Westerlands raid)

You are one of four parallel "lens" subagents enriching the **Weirwood Network**, a structured knowledge graph
for A Song of Ice and Fire. We are doing an **enrichment dip** on the **A2.5 WO5K-battles arc** — the military
arc that makes Robb Stark the Young Wolf. **THIS IS PASS 2 — THE WESTERLANDS RAID.** PASS-2 scope = after Robb is
crowned and relieves Riverrun (PASS 1, already built), he **carries the war west** past the Golden Tooth into the
Lannister heartland: **Oxcross** (the night victory over Stafford Lannister's green host raised at Casterly Rock)
→ **the raid** (Ashemark, the gold mines, the burning coast) → **the storming of the Crag** (Gawen Westerling's
seat) → **(ALREADY BUILT)** the **Jeyne-Westerling marriage blunder** → **(ALREADY BUILT)** the Red-Wedding-upstream
spine. The battles are **NON-POV — reported through Catelyn / Sansa AGOT-ACOK-ASOS chapters.** This is a **WIRE +
ENRICH with a HEAVY dedup**: the cast's dyad web is saturated (Robb 79 core-out, Jaime 165, the Westerling household
fully wired) AND the whodunit is already wired (`grey-wind OPPOSES rolph-spicer` + `sybell-spicer CONSPIRES_WITH
tywin-lannister` BOTH EXIST) AND the marriage spine is built. Aim your proposals at the **GAPS** in `baseline.md`:
**the causal raid spine** (3 islanded hubs: Oxcross / Ashemark / the Crag) and **the roster-empty Crag node** —
NOT the dense dyadic web. **The dedup WILL kill many proposals.**

**YOU PROPOSE — YOU DO NOT MINT.** Your output is a proposal file. An Opus orchestrator will synthesize all four
lenses, decide what to mint, line-check every quote, and a separate fresh-verify subagent will adjudicate the
interpretive/causal edges. Over-propose slightly; the gate is downstream.

## FIRST: read these (they are the ground truth — dedup against them)
1. `working/enrichment/wo5k-battles-pass2/baseline.md` — the scope, the PASS-2 cut, the DEDUP hot zones (the BUILT
   marriage spine + the ALREADY-WIRED whodunit + the saturated household web), the GAPS (your targets — the causal
   raid spine + the Crag roster + `jeyne HEALS robb`), the chapter map, and the slug-resolution flags (Black Walder
   twins → target `walder-frey-son-of-ryman`; the Smalljon = `jon-umber-son-of-jon`). **Every node/edge you propose
   MUST be deduped against the existing web.** If an edge already exists, do NOT re-propose it.
2. Your assigned chapter files (listed in your specific prompt). Read them IN FULL. **Quotes must be VERBATIM and
   carry a `chapter:line` cite** (e.g. `asos-catelyn-02.md:143` → cite as `asos-catelyn-02:143`). A quote must be a
   single contiguous substring of ONE line's text — never splice across a `," said X, "` attribution, never stitch
   two lines together. (Chapter files live at `sources/chapters/<book>/<chapter>.md`; lines are numbered — read with
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
    (the relief valve for the "sequence trap"). **This is the right edge for the raid spine** — the relief-rise
    ENABLES the westward offensive → Oxcross (Robb *chose* to march west); Oxcross ENABLES the raid → Ashemark (the
    Westerlands lay open, but Robb's host *chose* to raid on); the raid ENABLES the storming of the Crag. Do NOT use
    CAUSES for these — they are military preconditions Robb's free offensive walked through, not forced consequences.
  - `MOTIVATES` = drives an *actor's* decision; **target is a CHARACTER, never an event.**
- **Reification roles on an event hub** (use these to fill the roster-EMPTY Crag node + the Oxcross gaps):
  `AGENT_IN` (performed the act — Robb broke the gate, the Smalljon/Black Walder led the scaling parties, Grey Wind
  among the horse lines), `VICTIM_IN` (had it done to them — Stafford slain, the Lannister dead/captives),
  `COMMANDS_IN` (commander / orderer — Robb led the storm; Rolph Spicer the *defending* castellan who yielded — note
  the side), `FIGHTS_IN` (combatant — Grey Wind killed a man at the Crag), `WITNESS_IN` (load-bearing PERCEPTION of a
  charged incident — emit ONLY when the prose shows the character actually SEES it). Give the Crag node a
  `LOCATED_AT crag` (it has none) and a causal in (the raid ENABLES it; its ENABLES-out to the marriage exists).
- **`HEALS`** (healer → healed) — Jeyne nursed Robb's festering arrow wound until the fever passed
  (`asos-catelyn-02:143`). A clean gap edge: `jeyne-westerling HEALS robb-stark`.
- **`DEFEATS`** (victor → defeated) for a battle outcome — use only if a clean, non-redundant outcome edge is supported.
- **`SUSPECTED_OF`** (Tier-2, NEVER Tier-1) = a character suspected of being the agent/cause of an event the
  published text does NOT prove. **HONEST GATE: the Oxcross/Ashemark/Crag are clean military victories, and the
  Spicer-trap whodunit is ALREADY WIRED** (`grey-wind OPPOSES rolph-spicer` + `sybell-spicer CONSPIRES_WITH
  tywin-lannister` exist) **— and the full trap-reveal (Tywin's pardon, Rolph made Lord of Castamere, Jeyne made
  barren) is AFFC-late = PASS 3, the RW-upstream betrayal mechanism.** Default to proposing ZERO new SUSPECTED_OF.
  If you find a genuinely-new in-text pointed-but-unproven agency, propose it as **[BORDERLINE]** and NOTE if it is
  really PASS-3 material.
- Tier-1 REQUIRED-qualifier types (only if you propose them): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,
  HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO. Tier-3 types must NOT carry a qualifier.

## HARVEST (split the bar WIDE OPEN on food — Matt's standing rule)
While reading, drop one-line pointers to notable-but-not-an-edge finds into your proposal's `## Harvest` section:
`| kind | book | chapter:line | note |`. Capture EVERY meal/eating/food/drink moment — **the casks of nut-brown ale
for Robb's conquest of the Crag, the supper in the Great Hall, the Oxcross victory feast, any Westerling hospitality
at the Crag, the wedding feast.** Also capture: load-bearing verbatim quotes (for node `## Quotes` — Tyrion's Oxcross
account "the northmen crept into my uncle's camp and cut his horse lines," Rymund's Oxcross song "and the stars in the
night were the eyes of his wolves," Robb's "I took her castle and she took my heart," "we took it by storm one
night," Grey Wind killing at the Crag/Ashemark/Oxcross), vivid physical descriptions (the maddened destriers
trampling knights in their pavilions, the burning Westerlands, the night storm of the Crag walls, the festering
wound, Jeyne's seashell banner). POINT, don't extract — a later harvest pass attaches them.

## OUTPUT — write your proposal to `working/enrichment/wo5k-battles-pass2/lens-<X>.md`
(where `<X>` is your lens letter, given in your prompt). Structure:

```
# Lens <X> — <name> — A2.5 WO5K-battles proposal (S164, PASS 2)

## Proposed NEW nodes
For each: slug (kebab-case) · name · type (from the entity hierarchy) · 1-2 sentence body summary · the verbatim
anchor quote + chapter:line. (Likely NONE this pass — the cluster's nodes all exist. Propose a node only if a
genuinely-missing load-bearing beat has no home.)

## Proposed NEW edges
A table or list, each row:  source_slug  [EDGE_TYPE]  target_slug  | Tier-N | qualifier(if Tier-1 type) |
verbatim quote "<...>" + chapter:line | one-line rationale.
Mark any edge you are UNSURE about as **[BORDERLINE]** so the gate scrutinizes it.

## Dropped / considered-but-rejected
What you considered and why you did NOT propose it (already exists / show-only / theory-gated / agency-collapse /
TWOW-only / pure-travel-not-causal / PASS-3-scope).

## Harvest
The | kind | book | chapter:line | note | table.
```

Return a SHORT summary as your final message (counts + your 2-3 highest-value proposals). The file is the deliverable.

## HARD RULES (violating these = your proposal gets dropped at the gate)
- **Dedup** against baseline.md's live web — do not re-propose existing edges, the BUILT marriage spine, the
  ALREADY-WIRED whodunit, or the dense household web. The dedup is EXPECTED to kill many proposals; aim at the GAPS
  (the raid spine + the Crag roster + jeyne HEALS robb + the Oxcross VICTIM_IN gap).
- **Verbatim quotes only**, single contiguous substring of one line, with `chapter:line`. If you can't find the line,
  don't propose the edge.
- **No theory assertions (GATED):** no theory readings. Evidence/act/MOTIVATES→character edges only.
- **No TWOW / unpublished material.** Only the 5 published books.
- **No container tag** in your proposal (the synthesis decides). NOTE: `wo5k` IS an approved container and these
  battles ARE WO5K-trigger-tree beats — but you still leave the tagging to synthesis.
- **No show-canon** — only beats in the BOOK text (quote it from your assigned chapter files or don't propose it).
- **PASS 2 ONLY** — do NOT reach into the Fords / Duskendale (PASS 3) or re-mint the Spicer-betrayal payoff. If you
  notice a strong PASS-3 thread, NOTE it in `## Dropped` for the later pass; do not propose it.
- Honor the ENABLES-vs-CAUSES contract; route human choices through MOTIVATES(→character), not a false A-CAUSES-B.
- Use the right slug: **Black Walder = `walder-frey-son-of-ryman`** (NOT the `black-walder-frey` twin);
  **the Smalljon = `jon-umber-son-of-jon`** (NOT `jon-umber`, who is the Greatjon).
