# D5 — Arya's flight & Harrenhal — BASELINE (S154)

> Eighteenth major-arc enrichment dip; **SECOND Class-D event cluster** (D1 Battle of Castle Black was S153).
> Matt picked D5 at the STEP-0 fork. The natural S150/S153 follow-on: this is the **origin of the iron-coin
> seam** the Arya/Braavos arc (S150) hangs off, and the Harrenhal cluster wires into the Tywin/wartime-Riverlands
> material. **Scope:** AGOT Arya 04–05 (Syrio's stand → the flight from KL, Needle's first kill, Yoren) +
> ACOK Arya 01–10 (Yoren's band → the fight at the holdfast → capture → Harrenhal: the Tickler/Weese servitude,
> Jaqen's three deaths, the iron coin, the weasel-soup, the escape). The downstream Braavos arc (S150) is already
> built — do NOT re-touch it; only confirm the iron-coin → departs-for-braavos seam.

## Source chapters (the D5 span)
| file | lines | content |
|------|------:|---------|
| agot-arya-04 | 214 | Syrio Forel's last stand vs Meryn Trant in the Red Keep |
| agot-arya-05 | 192 | Arya flees the Red Keep — **kills the stableboy (Needle's first kill)** — dragon-skull cellars — streets — Sept of Baelor, Ned's execution, Yoren seizes & shears her |
| acok-arya-01 | 98 | Yoren's band on the kingsroad; "Arry"; Hot Pie; the three caged criminals (Jaqen/Rorge/Biter) |
| acok-arya-02 | 238 | the march; Praed dies; gold-cloaks come for Gendry; Yoren turns them away |
| acok-arya-03 | 120 | the holdfast; the night before the attack |
| acok-arya-04 | 220 | **fight at the holdfast** — Yoren dies; Arya frees the three caged men (the burning barn / the axe) |
| acok-arya-05 | 324 | aftermath; **captured** by Gregor/Amory's men; Lommy killed; marched to Harrenhal |
| acok-arya-06 |  94 | Harrenhal; the Tickler's interrogations & torture of captives |
| acok-arya-07 | 146 | Weese; **Jaqen's first death (Chiswyck)**; Arya as drudge/cupbearer |
| acok-arya-08 | 124 | **Jaqen's second death (Weese)**; the rats |
| acok-arya-09 | 394 | the Bloody Mummers take Harrenhal for Bolton (**fall-of-harrenhal**, Amory to the bears); **Jaqen's third "death" — the naming gambit & the weasel-soup dungeon massacre**; Roose Bolton arrives; Arya his cupbearer |
| acok-arya-10 | 316 | Roose departs for the Twins; Vargo Hoat holds Harrenhal; **the iron coin & valar morghulis (Jaqen's farewell)**; **Arya's escape** with Gendry & Hot Pie (kills the gate guard) |

## What's ALREADY built — the internal edge web (146 unique edges, both endpoints in the core set)

**The cluster has a DENSE dyadic/social layer** (Arya's HATES/FEARS/KILLS/MOURNS web; the cast's SERVES/COMPANION_OF
ties) **but a thin, causally-ISLANDED event-hub spine** — the S153 Castle Black profile exactly.

Built event hubs + their role edges:
- **`fight-at-the-holdfast`** (event.battle) — the central battle. Sub-beats: `arya-captured`, `gendry-captured`,
  `arya-frees-the-prisoners`, `lommy-yields-and-is-killed`. **0 causal edges** (only PART_OF war + junk year-page PRECEDES).
- **`arya-captured`** — arya VICTIM_IN; house-lannister AGENT_IN; gregor COMMANDS_IN.
- **`gendry-captured`** — gendry VICTIM_IN; house-lannister AGENT_IN; gregor COMMANDS_IN.
- **`lommy-yields-and-is-killed`** — lommy VICTIM_IN; gregor COMMANDS_IN. (`rafford KILLS lommy-greenhands` dyad exists.)
- **`arya-frees-the-prisoners`** — arya + rorge AGENT_IN; jaqen + biter VICTIM_IN.
- **`praed-s-death-and-burial`** — yoren + gendry AGENT_IN; dobber DIED_AT gods-eye.
- **`chiswyck-dies-three-days-later`** (event.death) — **Jaqen's 1st death.** jaqen AGENT_IN; arya COMMANDS_IN; chiswyck VICTIM_IN.
- **`guards-killed`** (event.death) — **the weasel-soup dungeon massacre.** jaqen + rorge + biter AGENT_IN; arya COMMANDS_IN; SUB_BEAT_OF fall-of-harrenhal; LOCATED_AT harrenhal.
- **`fall-of-harrenhal`** (event.battle) — the Bloody Mummers/Bolton takeover. Sub-beats `guards-killed`, `ser-amory-lorch-executed`.
- **`ser-amory-lorch-executed`** — amory VICTIM_IN; rorge + shagwell AGENT_IN; roose + vargo COMMANDS_IN; LOCATED_AT harrenhal.
- **`ser-amory-receives-the-prisoners`** — amory + vargo AGENT_IN; LOCATED_AT harrenhal.
- **`arya-gives-water-to-the-prisoners`** (ASOS arya-05 — **boundary node, NOT tight D5**) — arya/harwin/gendry AGENT_IN; caged-northmen VICTIM_IN. 0-outgoing.
- **`death-of-mycah`** + **`incident-at-the-trident`** (AGOT Trident — pre-flight; death-of-mycah SUB_BEAT_OF incident).
- Artifacts: **`needle`** (arya OWNS + WIELDS; **0 outgoing — no first-kill event**); **`iron-coin`** (arya OWNS; iron-coin GIFTED_TO arya; **already wired DOWNSTREAM to the Braavos arc S150** — ENABLES `arya-departs-for-braavos`, WIELDED_IN arrives-at-HoBaW — do NOT re-touch the Braavos end).

**Cast relationship web (already rich — do NOT re-propose):** arya HATES {rorge, amory, chiswyck, dunsen, gregor,
polliver, rafford, tickler}; arya FEARS {gregor, weese, jaqen, shagwell, roose}; arya KILLS {tickler, chiswyck, polliver}
(NB these are her later-arc kills / the kill-list payoff — Chiswyck/Tickler via Jaqen; Polliver in ASOS); arya MOURNS
{mycah, yoren, lommy}; arya DISGUISED_AS {yoren, weese}; arya SERVES {yoren, roose}; jaqen TEACHES/VOWS_TO/KILLS arya
(the FM lesson); weese TORTURES arya; yoren PROTECTS arya+gendry, VIOLATES_GUEST_RIGHT amory; vargo BETRAYS amory,
SWORN_TO/SERVES roose; gregor KILLS vargo (ASOS, the ear-rot).

## DEAD-ENDS / GAPS — the dip targets (confirm each in-text; some may be node-prose, not edges)

1. **MARQUEE — `fight-at-the-holdfast` has 0 causal wiring.** The whole flight→attack→capture spine is un-walked.
   Candidate causal spine: Yoren-recruits/march → Tywin sends Gregor+Amory hunting Beric → fight-at-the-holdfast
   → arya-captured → marched-to-Harrenhal → Tickler/Weese servitude → Jaqen-deaths → weasel-soup/fall-of-harrenhal
   → escape. Lens A + Lens 4 should propose CAUSES/TRIGGERS/ENABLES/MOTIVATES hops (honor the ENABLES-vs-CAUSES contract).
2. **MARQUEE — Needle's first kill (the stableboy, agot-arya-05).** No node. `needle` is 0-outgoing. Candidate:
   an `event.*` for the stableboy killing (arya AGENT_IN, needle WIELDED_IN/KILLED_WITH, the boy VICTIM_IN if nameable);
   it MOTIVATES / shapes Arya. (Continue-prompt-named marquee.)
3. **MARQUEE — the iron-coin's ORIGIN (acok-arya-10): Jaqen's farewell — gives the coin + "valar morghulis" + changes
   his face + departs.** No event node. The coin's GIFTED_TO edge cites ASOS (a recollection), not the actual giving.
   Candidate: a `jaqen-gives-arya-the-iron-coin` event (jaqen AGENT_IN, arya the recipient, iron-coin WIELDED_IN/GIFTED;
   ENABLES the Braavos departure — completing the Harrenhal→Braavos seam from the origin end). This is THE seam Matt's pick targets.
4. **Jaqen's three-deaths thread is half-built.** Death 1 (Chiswyck) ✅ node. **Death 2 (Weese) has NO event** —
   only `weese DIED_AT harrenhal`. **Death 3 — the naming gambit** (Arya names Jaqen himself, then unnames in exchange
   for him freeing the caged Northmen = the weasel-soup) has no node tying the gambit to `guards-killed`. Candidates:
   `death-of-weese` (jaqen AGENT_IN, arya COMMANDS_IN, weese VICTIM_IN) + wire the naming-gambit → guards-killed
   (arya MANIPULATES/COMMANDS jaqen via the un-naming; CAUSES/ENABLES the dungeon massacre → fall-of-harrenhal).
5. **The escape from Harrenhal (acok-arya-10) — the terminus.** No node. Arya/Gendry/Hot-Pie flee the postern; Arya
   kills the gate guard with Needle. Candidate: `arya-escapes-harrenhal` (arya AGENT_IN, gendry+hot-pie TRAVELS_WITH/
   AGENT_IN; needle WIELDED_IN the guard-kill); it should be the downstream terminus that the iron-coin/Braavos arc
   eventually hangs off, and the post-fall consequence of the weasel-soup.
6. **`capture-of-harrenhal` (0-incoming dead-end) is a WIKI node that conflates the AFFC Lannister re-capture**
   (Jaime returns after Gregor's death) — it is NOT the ACOK Arya-era fall (that's `fall-of-harrenhal`). **Possible
   dup/tangle with `fall-of-harrenhal`/`yielding-of-harrenhal`/`assault-on-harrenhal`.** Lens 4: investigate, but
   do NOT aggressively wire — flag the tangle for a hygiene pass rather than mint into the confusion.
7. **The Tickler's torture (acok-arya-06).** The systematic village-interrogations ("is there gold, where is Lord
   Beric"). `tickler SERVES gregor` exists; `weese TORTURES arya` exists. Candidate: `tickler TORTURES` (villagers
   may not be nodes → node-prose); `arya WITNESS_IN` the torture if a node is minted. Likely descriptive/quote depth.
8. **Yoren's death isn't reified on the battle hub.** `yoren DIED_AT gods-eye` exists but no `yoren VICTIM_IN
   fight-at-the-holdfast`, and the hub has no `LOCATED_AT gods-eye`. Candidate role edges.
9. **`incident-at-the-trident` (0-outgoing).** The Mycah confrontation. Possible light touch: `incident-at-the-trident
   MOTIVATES arya-stark` (the origin of the kill-list / her vengefulness) — but AGOT-pre, keep tight; only if text-direct.

## DO NOT (this dip)
- Re-touch the Braavos arc (S150) — only confirm the iron-coin origin → departs-for-braavos seam from the AGOT/ACOK end.
- Re-propose any of the 146 existing internal edges (deduped above) or the dense cast relationship web.
- Mint show-canon beats not in the books (the S153 Grenn-gate lesson — check every beat against the chapter text).
- **Assert theory readings (GATED):** the Faceless-Men cosmology / valar morghulis-as-religion / Jaqen=Pate-at-Oldtown /
  Jaqen's true identity / the iron-coin-as-magic. The coin + "valar morghulis" + the face-change are TEXT EVENTS (mint the
  events + possession/agency edges); the FM theology and Jaqen's identity stay node-prose, evidence-only.
- Over-mint speculative seam/foreshadowing edges — node-prose when unsure; honor ENABLES-vs-CAUSES.
- Use a container tag outside the approved 5 (essos/wo5k/north/aegon/bran). **D5 nodes are Riverlands/journey — NO
  container tag** (like the S148–S150 A2 arcs; Castle Black got `[north]` only because it's a North-container battle).
  Harrenhal-cluster event nodes could arguably carry `[wo5k]` (Riverlands theater of the war) — DEFER that call to synthesis;
  default NONE unless the node is already wired into the WO5K spine.

## Vocab: locked 170-type list (load from working/wiki/data/edge-type-counts.json)
Use ONLY these. Qualifier rule (validator-enforced) applies at MINT, not propose: Tier-1 types
(MANIPULATES/WARD_OF/SIBLING_OF/SPOUSE_OF/PARENT_OF/HOLDS_TITLE/VOWS_TO/SWORN_TO) REQUIRE an enum-valid qualifier;
Tier-3 must NOT; event-role + causal types take none.
