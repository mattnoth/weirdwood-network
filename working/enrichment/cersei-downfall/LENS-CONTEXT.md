# Shared lens context — Cersei's-downfall enrichment (S140)

You are ONE of four parallel PROPOSE-only lenses enriching the already-built **Cersei's-downfall**
arc (A Feast for Crows). You PROPOSE edges/nodes; you do NOT mint. The orchestrator (Opus) synthesizes,
line-checks every quote, mints, then a fresh independent verifier adjudicates. Output a markdown
proposal file ONLY.

## What "enrichment" means
Second-pass deepening of a built spine: the braided side-plots, secondary-character sub-arcs,
contemporaneous revelation-events, descriptive/quote/object depth, and unproven-but-load-bearing
edges that weren't on the first-pass spine. Do NOT re-propose what already exists (dedup against the
baseline below).

## The built spine (S114) — DO NOT re-propose these
- `assassination-of-tywin-lannister` --CAUSES--> `cersei-rearms-the-faith-and-forgives-the-debt`
  --CAUSES--> `cersei-is-captured-in-the-sept` --CAUSES--> `cersei-is-stripped-and-imprisoned`
- `cersei-plots-against-margaery` --CAUSES--> `cersei-confronts-and-arrests-the-blue-bard`
- `cersei-plots-against-margaery` --CAUSES--> `osney-kettleblack-confesses-to-high-sparrow`
  --TRIGGERS--> `cersei-is-captured-in-the-sept`
- Role edges already present: cersei/high-sparrow/qyburn AGENT_IN; margaery VICTIM_IN plot;
  blue-bard VICTIM_IN arrest; osney AGENT_IN + cersei VICTIM_IN confession; scolera AGENT_IN strip;
  faith AGENT_IN capture; high-sparrow COMMANDS_IN capture+strip+confession.
- `cersei-fills-in-the-arrest-warrants` exists with 10 VICTIM_IN + 2 AGENT_IN but is **causally
  ISLANDED** (0 causal edges) — wiring it in is fair game.
- `cersei-is-stripped-and-imprisoned` has **0 downstream** (dead-end) — fixing this is fair game.

## Key existing nodes you can wire to (already on disk — dedup, don't re-mint)
events: cersei-rearms-the-faith-and-forgives-the-debt, cersei-plots-against-margaery,
  cersei-confronts-and-arrests-the-blue-bard, osney-kettleblack-confesses-to-high-sparrow,
  cersei-is-captured-in-the-sept, cersei-is-stripped-and-imprisoned, cersei-fills-in-the-arrest-warrants,
  assassination-of-tywin-lannister, wedding-of-tommen-i-baratheon-and-margaery-tyrell
characters: cersei-lannister, high-sparrow, qyburn, robert-strong, maggy-the-frog, blue-bard,
  osney-kettleblack, osmund-kettleblack, osfryd-kettleblack, margaery-tyrell, taena-merryweather,
  orton-merryweather, kevan-lannister, tommen-baratheon, jaime-lannister, lancel-lannister
titles: high-septon       customs: walk-of-atonement
> NOTE: there is NO valonqar/Maggy-prophecy node, NO `cersei-s-walk-of-atonement` event node,
>   NO `murder-of-the-old-high-septon` node, NO `margaery-tyrell-arrested` node, NO `robert-strong`
>   creation-event node. If you think one should exist, PROPOSE it as a NEW node (give slug, type,
>   one-line identity, a verbatim anchor quote + chapter:line).
> WARNING — node trap: `faith-militant-uprising` is the HISTORICAL Aenys/Maegor war, NOT Cersei's
>   rearming. Do not wire to it.

## Source files
AFFC Cersei is POV across `sources/chapters/affc/affc-cersei-01.md` … `affc-cersei-10.md` (10 chapters).
READ the actual chapter files. Every quote you cite MUST be copied from the file.

## Locked edge-type vocabulary (170 — use ONLY these; never invent)
ADVISES AFFLICTED_BY AGENT_IN ALIAS_OF ALLIES_WITH ANCESTOR_OF ANCESTRAL_WEAPON_OF APPEARS_TO_FULFILL APPOINTS ASSAULTS ATTACKS ATTENDS BANISHES BESIEGES BESTOWS_KNIGHTHOOD_ON BETRAYS BETROTHED_TO BONDED_TO BORN_AT BREAKS_VOW BUILT BURIED_AT CADET_BRANCH_OF CAPTAIN_OF CAPTURES CAUSES CITED_BY CLAIMS CLERGY_OF COMMANDS COMMANDS_IN COMPANION_OF CONSPIRES_WITH CONTEMPORARY_WITH CONTRACTED_WITH CONTRADICTS CONTRASTS COURTS COUSIN_OF CREW_OF CROWNS_QUEEN_OF_LOVE_AND_BEAUTY CULTURE_OF CURSES DECEIVED_BY DECEIVES DEFEATS DEPICTED_IN DEPOSES DIED_AT DIED_OF DISGUISED_AS DISTRUSTS DREAMS_OF DUELS ECHOES ENABLES ENCOUNTERS EXECUTED_WITH EXECUTES FEARS FIGHTS_IN FORESHADOWS FORGED_BY FOUNDED FULFILLS GIFTED_TO GRANTS_SAFE_CONDUCT GUARDS GUEST_OF HATES HEALS HEIR_TO HELD_BY HOARDS HOLDS_TITLE HONORED_AT IGNORANT_OF IMPERSONATES IMPRISONED_AT IMPRISONS IN_LAW_OF INFORMS INHERITED_BY INVESTIGATES KILLED_BY KILLED_WITH KILLS KNIGHTED_BY LOCATED_AT LOOTED_BY LOVER_OF LOVES MADE_OF MANIPULATES MARRIES_OFF MEMBER_OF MILK_BROTHER_OF MOTIVATES MOURNS NAMED_AFTER NEGOTIATES_WITH NEPHEW_OF NURSED_BY OFFICIATES OPPOSES OVERLORD_OF OWNS PARALLELS PARENT_OF PART_OF PARTICIPATES_IN PERCEIVED_AS POISONS PRACTICES PRECEDES PREVENTS PRISONER_EXCHANGE_FOR PRISONER_OF PROPHESIED_BY PROPOSED_AS_BRIDE PROTECTS PURCHASED_FROM RANSOMS REFORGED_INTO REGION_OF REPUTED_AS RESCUES RESENTS RESPECTS RESURRECTS REVEALS_TO RULES SACRED_TO SACRIFICES SAME_AS SEAT_OF SEEKS SERVES SIBLING_OF SPIES_ON SPOUSE_OF STEP_CHILD_OF STEP_PARENT_OF SUB_BEAT_OF SUBJECT_OF_PROPHECY SUBVERTS SUBVERTS_PROPHECY SUCCEEDS SUPPORTS SUSPECTED_OF SWORN_TO TEACHES TORTURES TRAVELS_TO TRAVELS_WITH TRIGGERS TRUSTS TUTORS UNCLE_OF VICTIM_IN VIOLATES_GUEST_RIGHT VOWS_TO WARD_OF WARGS_INTO WET_NURSE_OF WIELDED_IN WIELDS WITNESS_IN WORSHIPS WRITTEN_BY

## THE LINE-CHECK RULE (most common failure — S139 caught a whole-chapter miscite)
- Every quote must be a VERBATIM CONTIGUOUS span copied from the file — including internal dialogue
  quote marks. NEVER splice across a `," said Cersei, "` attribution into one quote.
- Give the EXACT begin-line number (`affc-cersei-09.md:163`). Re-open the file and confirm the line
  before you write it down. If unsure, grep the anchor phrase. A quote on the wrong chapter/line is
  the recurring catch — be precise.

## AGENCY RULES (causal edges — the bar is TIGHT)
- **NO CAUSES between sibling/constitutive beats** — if B is part-of A or a co-constituent of the same
  happening, it's SUB_BEAT_OF, not CAUSES (agency-collapse). CAUSES needs a real distinct downstream state.
- **MOTIVATES targets a CHARACTER only**, never an event (a motive moves a person). Use it for the
  prophecy→Cersei psychological engine, the wine, the paranoia.
- **ENABLES = a door-opener / precondition**, not the proximate cause. Reserve for "made X possible."
- **SUSPECTED_OF** = unproven-but-load-bearing agency (Tier-2; never asserts the act). In-world false
  blame, contested attribution.
- **WITNESS_IN** needs a text anchor that the character was present and saw it.
- Do NOT assert facts the chapter leaves unconfirmed (S139 dropped `oberyn POISONS gregor` because ASOS
  only says "Oil? Or poison?"). If the text hedges, you hedge (SUSPECTED_OF or drop).

## SPLIT THE BAR
- **Edge bar = TIGHT.** Only propose edges you can ground in a verbatim line with a valid vocab type.
- **Harvest bar = WIDE OPEN.** Separately, as you read, drop one-line pointers for EVERY meal / food /
  drink (including the grim register — Cersei's wine, the sparrows' poverty, prison starvation),
  every vivid description, quote, foreshadowing, object — as `chapter:line / kind / note` rows in a
  `## HARVEST` section at the foot of your proposal. POINT, don't extract. A later harvest pass attaches them.

## Output format
Write `working/enrichment/cersei-downfall/proposal-lens-<N>-<name>.md` with:
1. `## NEW NODES` — slug / type / one-line identity / anchor quote + `chapter:line`
2. `## EDGES` — `SOURCE_SLUG --[TYPE]--> TARGET_SLUG` | Tier | `chapter:line` | verbatim quote | one-line rationale
3. `## HARVEST` — `chapter:line / kind / note` rows
4. `## NOTES` — anything you considered and rejected, dedup catches, uncertainties
Propose 6–15 high-confidence edges. Quality over volume. Dedup every node against the baseline.
