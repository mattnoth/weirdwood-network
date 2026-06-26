# Baseline — A2.1 Theon / Reek BUILD+ENRICH pass 1 (S149)

> The descent's **second build+enrich** dip (after S148 Sansa/Vale). UNLIKE Sansa/Vale, much of the
> spine already EXISTS (built incidentally during the NORTH spine + Pass-1 overlays) — so this is
> **wire + enrich** more than pure build. The marquee is the **flagged cross-identity Reek tangle**
> (a key graph use case) + the unbuilt **captivity/torture sub-arc** + the **dead-ended escape**.
> Source chapters: ACOK Theon I–VI + ADWD Reek I–III / The Prince of Winterfell / A Ghost in
> Winterfell / Theon. **Container tag: NONE** (A2 arcs are not one of the 5 approved containers;
> do NOT tag — the events themselves may already carry NORTH/wo5k tags from prior builds, leave those).

## The Reek identity tangle — READ FIRST (the flagged cross-identity use case)

The name **"Reek" passes across THREE different people** in the books. The single `reek` node
(built from the AWOIAF "Reek" page) narrates ALL THREE in its body — it is effectively an overloaded
identity-name node. **Do NOT silently merge or break it.** The three bearers:

1. **Reek (I) — the original servant.** Roose Bolton's stinking man; Ramsay's tutor-in-cruelty.
   This is what the `reek` node IS (frontmatter: `character.human`, alias "Reek (I)", `DIED_AT north [299]`).
   Killed by Rodrik's men in ACOK while wearing Ramsay's clothes.
2. **Ramsay-as-Reek (ACOK).** After the original Reek dies wearing his clothes, **Ramsay smears himself
   in filth, dons the dead servant's clothes, and is captured posing as "Reek"** (gives his name as
   "Heke"). Found in Winterfell's dungeons during the capture; Theon frees him; "Reek" brings the
   Dreadfort garrison, betrays Rodrik's relief host, then reveals he is Ramsay and sacks Winterfell.
   → model `ramsay-snow IMPERSONATES reek` (ACOK; **first-use IMPERSONATES in graph**). `ramsay DECEIVES
   theon-greyjoy` ALREADY EXISTS (acok-theon-06:109).
3. **Theon-as-Reek (ADWD).** Ramsay breaks Theon by torture/mutilation at the Dreadfort and **renames
   him "Reek."** Theon's self dissolves; "only Reek remains," until he reclaims his name in ADWD Theon.
   This is the **"Reek = Theon" query case**: in ADWD context, "Reek" means Theon.

**MODELING RULE for the dip (propose; fresh-verify gates):**
- `SAME_AS` is **WRONG** for the multi-bearer name — it would transitively imply Theon = Ramsay = the
  servant. Do NOT use SAME_AS on `reek`.
- Ramsay's ACOK disguise = `ramsay-snow IMPERSONATES reek` (Tier-1, clean, time-bound).
- Theon's ADWD identity = **propose** the discoverability fix as a node-alias add ("Reek" / "Reek (III)"
  onto `theon-greyjoy`) + a disambiguation note, NOT an edge that asserts personal identity-equality.
  Lens B owns the recommendation; synthesis + fresh-verify decide. (Adding an alias needs `weirwood-refresh`.)
- The forcible renaming itself is part of the torture: capture it via the captivity edges + the node
  body, not a fabricated "RENAMES" type (not in vocab).

## The arc + chapter map

| File | Book ch | Title | Arc content |
|------|:---:|---|---|
| acok-theon-01 | 12 | Theon | Arrives at Pyke; Balon's cold welcome; the Greyjoy invasion plan; Asha |
| acok-theon-02 | 25 | Theon | The raiding assignment (Stony Shore); chafes under Balon |
| acok-theon-03 | 38 | Theon | **The capture of Winterfell** ("I am a Greyjoy, and I mean to be my father's heir") |
| acok-theon-04 | 51 | Theon | Holds Winterfell; Bran & Rickon flee; the hunt; **"Reek" appears** |
| acok-theon-05 | 57 | Theon | **The fake deaths of Bran & Rickon** (the two miller's boys, tarred & hung); Kyra |
| acok-theon-06 | 67 | Theon | Rodrik's host; "Reek" brings the Dreadfort men, **betrays Rodrik**; **the sack**; Ramsay revealed |
| adwd-reek-01 | 13 | Reek | **The Dreadfort — Theon broken into "Reek"**; freed to retake Moat Cailin; Kyra-hunt |
| adwd-reek-02 | 21 | Reek | **Moat Cailin** — Reek talks the ironborn into surrender; Ramsay flays them |
| adwd-reek-03 | 33 | Reek | Barrowton; meets Roose; wedding prep; Harwood Stout |
| adwd-the-prince-of-winterfell-01 | 38 | The Prince of Winterfell | **Wedding of Ramsay & "Arya" (Jeyne Poole)**; Theon gives her away |
| adwd-a-ghost-in-winterfell-01 | 47 | A Ghost in Winterfell | The Winterfell murders; Theon as "the ghost"; Abel's washerwomen |
| adwd-theon-01 | 52 | Theon | Mance's spearwives; **Theon reclaims his name; the escape — the leap from the battlements with Jeyne** |

## The spine skeleton (EXISTS vs GAP)

ACOK (Greyjoy turn → fall):
1. `theon-greyjoy-taken-as-ward` ✓ (IN greyjoy-rebellion CAUSES) — the hostage origin
2. `balon-declares-himself-king` ✓ → `ironborn-invasion-of-the-north` ✓ (CAUSES fall-of-moat-cailin,
   harrying-of-the-stony-shore; ENABLES capture-of-winterfell)
3. `capture-of-winterfell` ✓ (theon AGENT_IN; "I am a Greyjoy…") — fairly dense (3 out / 5 in)
4. **GAP** → the fake deaths of Bran & Rickon (the miller's boys) — only the downstream
   `robb-receives-false-news-of-brans-death` ✓ + `bran-and-rickon-survive-the-sack-in-the-crypts` ✓ exist.
   The ACT is unbuilt. **MINT candidate.**
5. `battle-outside-the-gates-of-winterfell` ✓ (Rodrik's relief host) → `bolton-forces-attack` ✓
   (ramsay COMMANDS_IN; "Reek" brings the Dreadfort men) → `sack-of-winterfell` ✓ (dense: 4 out / 14 in;
   theon VICTIM_IN, luwin/rodrik/black-lorren VICTIM_IN, ramsay/house-bolton AGENT_IN, roose COMMANDS_IN)
6. **Cross-identity:** `ramsay-snow IMPERSONATES reek` (GAP, mint edge); `ramsay DECEIVES theon` ✓

ADWD (Reek → redemption):
7. **GAP** → the breaking at the Dreadfort: `ramsay TORTURES theon`, `ramsay IMPRISONS theon`,
   Theon→"Reek" identity destruction. **NO captivity/torture edge exists on ramsay→theon** despite being
   the core of the arc. **MINT candidate** (event node for the breaking + edges). First-use TORTURES/IMPRISONS.
8. `fall-of-moat-cailin` ✓ / `bolton-banner-raised-prisoners-killed` ✓ (Reek secures surrender → Ramsay
   flays the ironborn; ramsay COMMANDS_IN). Theon/Reek's negotiator role here is unbuilt.
9. `wedding-of-ramsay-bolton-and-arya-stark` ✓ (Jeyne-as-Arya; theon AGENT_IN gives her away; jeyne
   VICTIM_IN; roose COMMANDS_IN) — dense (1 out / 7 in). `jeyne-poole BETROTHED_TO ramsay` ✓
10. `wedding-guests-observed-in-torchlight` ✓ (carries the later Winterfell-murder victims as VICTIM_IN —
    roose/hother/stout/locke + the two Walders [orphan-targeted, no node]). The "Ghost in Winterfell"
    murders sub-plot may want its own node — lens A/B decide.
11. **DEAD-END** `theon-carries-jeyne-up-battlements-stairs` ✓ (0 out / 3 in) — the climactic escape leap.
    No downstream; the identity-reclaim ("Theon. My name is Theon") is uncaptured. **WIRE FORWARD + the
    reclaim beat.** Maybe broaden/parallel with a `theon-and-jeyne-escape-winterfell` node.
12. `pink-letter-delivered` ✓ (Ramsay's "Bastard Letter" demands "his Reek" + the bride back; jon OPPOSES
    ramsay ✓ adwd-jon). The escape MOTIVATES / ENABLES the pink letter — cross-arc seam into the NORTH/Jon spine.

## Existing nodes — dedup map (use these slugs verbatim)

**Characters:** `theon-greyjoy` (85 edges — already dense) · `reek` (the servant; 5 wiki edges) ·
`ramsay-snow` (44; NOTE Pass-1 uses ramsay-**snow** not ramsay-bolton) · `roose-bolton` · `jeyne-poole`
(aliases "Arya Stark"/"Lady Arya"; SPOUSE_OF ramsay) · `asha-greyjoy` · `balon-greyjoy` · `aeron-greyjoy` ·
`victarion-greyjoy` · `dagmer` (Cleftjaw) · `farlen` · `kyra` (kennelmaster's daughter — ramsay KILLS) ·
`wex-pyke` (Theon's mute squire) · `luwin` (NOT maester-luwin) · `osha` · `bran-stark` · `rickon-stark` ·
`rodrik-cassel` · `mance-rayder` (alias **"Abel"** — use mance-rayder) · the six spearwives:
`rowan` · `squirrel-free-folk` · `myrtle` · `willow-witch-eye` · `holly` · `frenya` · `stannis-baratheon` ·
`mors-umber` (Crowfood) · `wyman-manderly` · `hosteen-frey` · `aenys-frey` · `hother-umber` ·
`harwood-stout` (Lord Stout) · `damon-dance-for-me` · `yellow-dick` · `sour-alyn` · `skinner` · `ben-bones` ·
`black-lorren` · `qarl-the-maid`.

**Events (use as-is):** `theon-greyjoy-taken-as-ward` · `ironborn-invasion-of-the-north` ·
`capture-of-winterfell` · `harrying-of-the-stony-shore` · `battle-of-the-stony-shore` ·
`robb-receives-false-news-of-brans-death` · `bran-and-rickon-survive-the-sack-in-the-crypts` ·
`battle-outside-the-gates-of-winterfell` · `bolton-forces-attack` · `sack-of-winterfell` ·
`trail-followed-north-northwest` (the ACOK hunt for Bran/Rickon; SUB_BEAT_OF sack) · `fall-of-moat-cailin` ·
`siege-of-moat-cailin` · `bolton-banner-raised-prisoners-killed` (the Moat Cailin flaying) ·
`capture-of-torrhens-square` · `taking-of-deepwood-motte` · `fight-by-deepwood-motte` ·
`wedding-of-ramsay-bolton-and-arya-stark` · `wedding-guests-observed-in-torchlight` ·
`theon-carries-jeyne-up-battlements-stairs` · `pink-letter-delivered` · `stannis-march-on-winterfell`.

**Locations/factions:** `winterfell` · `dreadfort` · `moat-cailin` · `pyke` · `iron-islands` ·
`godswood-of-winterfell` · `great-keep-winterfell` · `crypt-of-winterfell` · `torrhens-square` ·
`deepwood-motte` · `house-greyjoy` · `house-bolton` · `house-bolton-of-winterfell` · `house-stark`.

**DEDUP TRAPS (critical):**
- `reek` = the original servant — the identity-tangle node. Do NOT merge with theon-greyjoy; do NOT
  SAME_AS. Use IMPERSONATES (ramsay→reek) + an alias add (propose) for theon's ADWD Reek.
- `ramsay-snow` is the canonical slug (Pass-1 era; legitimized to Bolton mid-ADWD but node slug stays `-snow`).
- `jeyne-poole` already carries aliases "Arya Stark"/"Lady Arya" + SPOUSE_OF/BETROTHED_TO ramsay — do NOT
  build a new "fArya" node; "Arya" in the Winterfell-wedding context resolves to jeyne-poole.
- `battle-of-winterfell` is a **redirect stub** (`same_as: battle-outside-the-gates-of-winterfell`) — 0/0
  by design. Do NOT wire it; use `battle-outside-the-gates-of-winterfell`.
- `kyra` (kennelmaster's daughter, ramsay's hunt-quarry) ≠ `kyra-frey`. Use `kyra`.
- `big-walder-frey`/`little-walder-frey` have **no nodes** (existing VICTIM_IN edges are orphan-targeted) —
  do NOT invent them this dip; if a Walder edge is load-bearing, flag it, don't mint the node.

## Likely mint candidates (lenses confirm/refine — keep the dip to ~30-45 edges, ~2-4 new nodes)

- **A.** `theon-fakes-the-deaths-of-bran-and-rickon` (event.deception, ACOK ch57) — the miller's boys
  passed off as the Stark boys; CAUSES robb-receives-false-news; the moral nadir of Theon's ACOK arc.
- **B.** the Dreadfort breaking → "Reek" (event; ADWD ch13) — the identity-destruction; ramsay
  TORTURES/IMPRISONS theon. (Or wire torture edges onto an existing node if one fits — check first.)
- **C.** the escape/reclaim (ADWD ch52) — wire the dead-end `theon-carries-jeyne` forward + the
  name-reclaim; maybe a `theon-and-jeyne-escape-winterfell` node.
- **D.** (maybe) the "Ghost in Winterfell" murders sub-plot node — only if lens A/B show it's load-bearing
  and not already covered by `wedding-guests-observed-in-torchlight`.

## Vocab + conventions (locked — paste into lens prompts)

- Locked vocab = the **170 canonical types** in `working/wiki/data/edge-type-counts.md`. edges.jsonl uses
  `edge_type`/`source_slug`/`target_slug` (NOT `type`). Relevant types all present:
  causal `CAUSES`/`TRIGGERS`/`ENABLES`/`MOTIVATES`/`PREVENTS`; roles `AGENT_IN`/`VICTIM_IN`/`WITNESS_IN`/
  `PARTICIPATES_IN`/`COMMANDS_IN`/`FIGHTS_IN`/`SUB_BEAT_OF`; captivity `IMPRISONS`/`IMPRISONED_AT`/
  `PRISONER_OF`/`TORTURES`/`RESCUES`/`CAPTURES`/`RANSOMS`; identity `IMPERSONATES`/`DISGUISED_AS`/`SAME_AS`/
  `ALIAS_OF`; betrayal/violence `BETRAYS`/`VIOLATES_GUEST_RIGHT`/`KILLS`/`ASSAULTS`/`POISONS`; revelation
  `REVEALS_TO`/`INFORMS`/`DECEIVES`/`MANIPULATES`/`SUSPECTED_OF`; reaction `FEARS`/`HATES`/`MOURNS`/
  `RESENTS`/`LOVES`/`PROTECTS`/`PERCEIVED_AS`. **No MUTILATES/FLAYS/RENAMES type** — use TORTURES/ASSAULTS.
- `MOTIVATES` target = the **person/actor**, not the event (route grievance through the human).
- `SUSPECTED_OF` (Tier-2) = unproven-but-load-bearing agency — never asserts the act.
- `IMPERSONATES`: X IMPERSONATES Y = X (the real actor) pretends to be Y (the assumed identity). Per S145
  glamour-swap convention (mance IMPERSONATES lord-of-bones).
- Check live edge-direction before emitting any artifact-transfer edge.
- **Theory gate:** Reek-redemption-as-destiny, Theon-as-Azor-Ahai, the "Winds" forward plot — all GATED.
  Evidence edges only; no fAegon/R+L/Azor-Ahai. No forward-dangling TWOW nodes (`theon-i-the-winds-of-winter`
  exists but is UNPUBLISHED — do NOT wire as canon spine).
