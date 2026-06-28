# Baseline — A2.6 Jaime / Riverlands enrichment (S159)

**Dip shape: BUILD + ENRICH, HEAVY dedup.** Jaime is a saturated POV (156 out-edges) with a dense,
well-built dyad web (280 internal edges in the core set). But his AFFC Riverlands **command** has a
**thin/islanded event-causal layer** — only **8 causal internal edges**, and the Riverrun-siege
**resolution** (Edmure's surrender, the Blackfish's escape) is **entirely unbuilt**. The marquee value
is a small number of NEW nodes + wiring that lights the resolution, plus object/quote depth.

## The arc (5 published books only — NO TWOW)
Jaime takes over the inherited Riverrun siege (AFFC), coerces Edmure into surrendering the castle by
threatening to trebuchet his infant heir, takes Riverrun bloodlessly — but the Blackfish slips the
castle and escapes downriver. Jaime burns the siege engines and the Frey gallows, installs Emmon Frey,
and at the very end **burns Cersei's plea-for-help letter unread**, refusing to ride to her aid — the
marquee Jaime↔Cersei rupture. Backstory layer (ASOS): the hand-loss / Vargo Hoat / Brave Companions,
the Ice-reforged-into-Oathkeeper gift to Brienne, the kingslaying.

## DEDUP — these are LIVE, do NOT re-mint (verified in the baseline pull)
- **The dyad web is DONE.** Jaime↔Cersei (LOVER_OF/SIBLING_OF/CONTRASTS/PARALLELS/MOURNS/PROTECTS/
  DISTRUSTS/CONSPIRES_WITH), Jaime↔Tyrion, Jaime↔Brienne (S141: CAPTURES/DUELS/GUARDS/RESCUES/PROTECTS/
  VOWS_TO/LOVES/COMPANION_OF/TRAVELS_WITH/RESPECTS — **the whole Brienne dyad is built**), Jaime↔Edmure
  (CAPTURES/GUEST_OF/HATES/OPPOSES), the Frey kin web, the riverlord houses (Blackwood/Bracken/Tully).
  Do NOT re-propose any of these.
- **siege-of-riverrun hub** already has 13 incoming: COMMANDS_IN (jaime, daven, ryman, brynden),
  ENABLES (red-wedding, edmure-taken-hostage), PARTICIPATES_IN (emmon, edwyn, desmond-grell, robin-ryger,
  jeyne-westerling), VICTIM_IN (edmure), SUB_BEAT_OF (jaime-orders-siege-equipment-and-gallows-burned),
  LOCATED_AT riverrun, PART_OF wo5k. Do NOT re-mint these.
- **S141 Brienne→Stoneheart**: oathkeeper WIELDED_IN (brienne's two fights), vargo-hoat TORTURES jaime,
  brienne ATTACKS/PRISONER_OF vargo, the Saltpans/hound-helm thread. Do NOT re-touch.
- **S142 Sack-of-KL wildfire thread**: wildfire-plot ENABLES aerys-commands-the-city-burned, wildfire-plot
  MOTIVATES slaying-of-aerys, jaime PREVENTS aerys-commands-the-city-burned, jaime-found-seated-on-the-iron-throne,
  the kingslaying SUB_BEAT_OF sack. Do NOT re-mint.
- **S109 Tywin's-death**: jaime-frees-tyrion-from-the-black-cells CAUSES jaime-reveals-the-truth-of-tysha
  MOTIVATES tyrion; jaime AGENT_IN both. Do NOT re-mint.
- **Harrenhal node-tangle** (capture/assault/fall/burning/yielding-of-harrenhal, all causally islanded) —
  the alias-hygiene is a SEPARATE S154 small-fix, NOT this dip. Touch Harrenhal only for Jaime's command
  tenure if a clean book-cited edge exists; do NOT re-cut the tangle.

## THE GAPS (your targets — aim here)
1. **Edmure's surrender is NOT a node.** The trebuchet coercion (Jaime: "I will trebuchet your child
   into the keep" — affc-jaime-06) → Edmure yields Riverrun (affc-jaime-07:21,39 "hauling down the
   direwolf of Stark in token of surrender"). → MINT `edmure-yields-riverrun` (event.incident). The
   siege-of-riverrun hub has **cOut=0** — its resolution is the single biggest gap.
2. **The Blackfish's escape is NOT a node.** Brynden Tully slips under the boom downriver rather than
   yield (affc-jaime-07:39 "a black fish in a black river floating quietly downstream"; :39 "the
   Blackfish was not amongst the prisoners"). → MINT `blackfish-escapes-riverrun` (event.incident).
3. **The burning of Cersei's letter is NOT a node.** affc-jaime-07:291 (her plea "Come at once. Help
   me. Save me… I love you") → :295 Jaime "Put this in the fire." The marquee rupture — model as an
   act + a refusal (MOTIVATES → character), NOT an over-asserted edge. → MINT `jaime-burns-cerseis-letter`.
4. **Oathkeeper has ZERO incoming** (oathkeeper core_in=0). Missing: `jaime GIFTED_TO brienne`
   (the marquee gift, affc-jaime-01), `ice REFORGED_INTO oathkeeper` + `ice REFORGED_INTO widows-wail`
   (asos-jaime-08, Tywin melts Ice), jaime OWNS/WIELDS oathkeeper before gifting, MADE_OF valyrian-steel.
   `ice` core_in=0 too. This is the highest-value object cluster.
5. **The hand-loss has NO node** (vargo-hoat TORTURES jaime exists, but the maiming event is unbuilt).
   Consider `jaime-loses-his-hand` (event.incident) IF a clean asos-jaime quote anchors it — but this
   is secondary ASOS backstory; keep the AFFC Riverlands command as the marquee, dedup hard vs S141.
6. **Causally islanded Jaime-arc hubs** to consider lighting (only with clean book cites):
   `jaime-orders-siege-equipment-and-gallows-burned` (cOut=0), `hostage-negotiation` (the Raventree /
   Tytos Blackwood beat, cOut=0 cIn=0 causal), `jaime-demands-the-red-wedding-captives`,
   `jaime-lies-about-cleos-s-death`.

## Cross-arc seams (lens D)
- The Riverrun resolution completes the WO5K Riverlands pacification — the last Tully holdouts the Iron
  Throne mops up. `edmure-yields-riverrun` → the Frey installation (`emmon-frey RULES riverrun` exists).
- The Cersei-letter → Jaime's refusal to aid her (a MOTIVATES on Jaime's decision, the Kingsguard-vow arc).
- Jaime ↔ Brienne: Oathkeeper is the physical token of the Catelyn-vow (the sword he sends her to find Sansa).

## Chapter map (read in full; quotes VERBATIM, single contiguous line substring, `chapter:line`)
- **AFFC Riverlands command:** `affc-jaime-01` (Oathkeeper named/gifted to Brienne), `affc-jaime-02`
  (the march; Daven at Riverrun), `affc-jaime-03`/`affc-jaime-04` (Harrenhal command, restoration of
  order, Wylis/Pia), `affc-jaime-05` (arrival at Riverrun, Ryman's gibbet), `affc-jaime-06` (the parley
  with Edmure, the trebuchet threat), `affc-jaime-07` (Edmure yields, the Blackfish escapes, the gallows
  burned, **Cersei's letter burned**).
- **ASOS backstory (DEDUP vs S141/S142):** `asos-jaime-01`…`asos-jaime-09` (the capture, the hand-loss,
  the bath confession of the wildfire-plot/Aerys, the Brave Companions, the kingslaying, Ice reforged in
  `asos-jaime-08`). Pull in ONLY what S141/S142 left islanded — most of this is built.

## DO NOT
TWOW (no Lady Stoneheart-meets-Jaime, no TWOW Jaime) · re-mint the S100/S141/S142/S109 web above ·
re-cut the Harrenhal node-tangle · assert theory readings (Jaime-as-valonqar, prophecy) — evidence/act
edges only, readings stay node-prose · container tags (the Riverlands is NOT one of the 5 approved
containers — default NO tag; a genuine WO5K-campaign beat may take `[wo5k]` only if it truly is one) ·
over-assert the Cersei rupture (model honestly).
