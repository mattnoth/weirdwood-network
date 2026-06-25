# Bran / greenseer arc enrichment — DEDUP BASELINE (S146)

> **PROPOSE, don't mint.** Everything in the "EXISTS" sections below ALREADY EXISTS in the graph.
> Do NOT re-propose it. Verify any node you want to propose:
> `find graph/nodes -name "<slug>.node.md"` (exists → don't mint) and check `graph/edges/edges.jsonl`
> (grep the source+target) before proposing an edge. When in doubt, dedup-check.
>
> **This is the BRAN/greenseer ARC enrichment** (the spine was built S130). It PAIRS with — but is NOT —
> the separate Bloodraven character dip. Cave-cluster Bloodraven *substrate* that falls out naturally
> (mentorship, the children, the weirwood net) is in scope; a full Bloodraven kin/Blackfyre/D&E sweep is NOT.

## The built BRAN spine (8 event beats — DO NOT re-mint; clean ENABLES chain)
From `--container bran` + `--full-chain bran-becomes-a-greenseer`:
1. `bran-witnesses-jaime-and-cersei` →TRIGGERS→ `jaime-pushes-bran-from-the-tower` (`[bran,wo5k]` seam)
2. `jaime-pushes-bran-from-the-tower` →TRIGGERS→ `bran-s-coma-and-the-three-eyed-crow` (brynden-rivers MOTIVATES it: "Fly or die")
3. `bran-s-coma-and-the-three-eyed-crow` →ENABLES→ `jojen-reed-names-bran-a-warg`
4. `sack-of-winterfell` →CAUSES→ `bran-and-rickon-survive-the-sack-in-the-crypts` (osha AGENT_IN+ENABLES; rickon VICTIM_IN)
5. `…survive-the-sack…` →ENABLES→ `bran-s-party-splits-from-rickon` (jojen MOTIVATES; meera/osha/bran AGENT_IN)
6. `…party-splits…` →ENABLES→ `bran-passes-the-black-gate` (samwell-tarly ENABLES — the Watch oath)
7. `bran-passes-the-black-gate` →ENABLES→ `bran-meets-coldhands`
8. `bran-meets-coldhands` →ENABLES→ `bran-reaches-the-cave-of-the-three-eyed-crow` (bran/meera/coldhands/leaf AGENT_IN the wight fight; brynden-rivers AGENT_IN "you will fly")
9. `bran-reaches-the-cave…` →CAUSES→ `bran-becomes-a-greenseer` [TERMINUS, 0 outgoing] (bran/leaf/brynden-rivers AGENT_IN)

Also tagged `[bran]`: `six-wildling-deserters-ambush-bran` (0 causal — a dead-end incident, KEEP, do NOT force into the spine);
`bran-s-direwolf-kills-the-assassin` (`[bran,wo5k]`, the WO5K fork).

## Existing substrate around the arc (DO NOT re-propose)
- **Warging (already wired):** `bran-stark WARGS_INTO summer` (acok-bran-03:39) · `bran-stark WARGS_INTO hodor` (asos-bran-03:23) · `bran-stark BONDED_TO summer` · `bran-stark OWNS summer` · `summer COMPANION_OF/PROTECTS bran-stark`.
- **Reeds:** `jojen-reed TUTORS bran-stark` · `jojen-reed PROTECTS/COMPANION_OF/TRAVELS_WITH bran-stark` · `meera-reed PROTECTS bran-stark` · `jojen SIBLING_OF meera-reed`.
- **Cave cluster:** `leaf AGENT_IN cave + greenseer`, `leaf PROTECTS + RESCUES bran-stark` · `brynden-rivers AGENT_IN cave + greenseer`, `brynden-rivers MOTIVATES coma`, `bran-stark SEEKS brynden-rivers` · `hodor/jojen/meera/bran GUEST_OF children-of-the-forest` (the cave).
- **Bloodraven wiki kin (already present):** `aegon-iv-targaryen PARENT_OF brynden-rivers` · `melissa-blackwood PARENT_OF brynden-rivers` · `aegor-rivers LOVER_OF shiera-seastar` · `brynden-rivers LOVER_OF shiera-seastar` · titles (Hand, Master of Whisperers, LC Night's Watch) · `brynden-rivers SWORN_TO nights-watch/house-targaryen`.

## THE GAP this dip fills (THIN / MISSING — propose here)
1. **The greendream catalogue (marquee).** Jojen's green dreams are UNWIRED. Use `DREAMS_OF` (Dreamer→Subject; the type explicitly names Jojen) and/or `FORESHADOWS`:
   - **"The sea came to Winterfell"** (acok-bran-05:77/:81; named drowned men = Alebelly, Septon Chayle, Mikken — all die in the sack) → **`jojen-reed DREAMS_OF sack-of-winterfell`** — a **BRAN→WO5K/NORTH cross-container seam** (the salt sea = the ironborn).
   - **"A winged wolf bound with grey stone chains, a crow pecking through"** (acok-bran-04:79/:93 — "The crow sent us here to break your chains") → **`jojen-reed DREAMS_OF bran-becomes-a-greenseer`** (the arc's own terminus, foreseen).
   - **"Reek skinning your faces, you and your brother lay dead"** (acok-bran-05:169) → foreshadows the miller's-boys deception / `robb-receives-false-news-of-brans-death` (another BRAN→WO5K seam — VERIFY the target slug & whether to use DREAMS_OF vs FORESHADOWS).
2. **`greensight` concept node is DEAD (0 edges).** Light it: `bran-stark PRACTICES greensight` · `brynden-rivers PRACTICES greensight` (the last greenseer) · possibly `jojen-reed PRACTICES greensight` (greendreams) — `PRACTICES` = Character→Magic discipline, in-vocab.
3. **Bloodraven mentorship substrate (cave, textual — NOT theory).** `brynden-rivers TUTORS bran-stark` (he teaches Bran to slip his skin & enter the weirwoods — adwd-bran-03; distinct from the existing jojen TUTORS) · `brynden-rivers BONDED_TO weirwood` (enthroned in the roots / the weirwood net, textual) — verify wording/anchor.
4. **The children-of-the-forest / Leaf substrate.** `leaf MEMBER_OF children-of-the-forest` (clean, missing) · Leaf TEACHES/explains the singers to Bran (adwd-bran-03:15/:25). (NB the species node carries some JUNK GUEST_OF edges to cersei/sansa from acok-sansa-07 — a mis-extraction of human "children"; out of scope to fix, do NOT build onto them.)
5. **Object/place depth.** `weirwood-paste` EXISTS (foods/) — the instrument of transformation; consider a descriptive attach on `bran-becomes-a-greenseer` and/or a graph tie (no clean "ingested-in" type — likely a `## Quotes`/Narrative-Arc attach, not a forced edge). The cave / weirwood throne descriptive depth.
6. **Lens-4 structural fixes (highest value):**
   - **The `three-eyed-crow` SLUG TRAP (S130-flagged, still live).** `three-eyed-crow` is typed **`species`** but IS Bloodraven. Three edges mis-point at it: `three-eyed-crow TEACHES bran-stark`, `coldhands SERVES three-eyed-crow`, `coldhands SWORN_TO three-eyed-crow`. Bloodraven = `brynden-rivers`. Assess retargeting these → `brynden-rivers` (a post-verify modification; do NOT assert SAME_AS — that's a higher-stakes cross-identity call, leave it).
   - **`wight-ambush` (legacy event, 0 outgoing, islanded)** = the cave-approach attack, duplicating the fight already on `bran-reaches-the-cave…`. Clean de-island: `wight-ambush SUB_BEAT_OF bran-reaches-the-cave-of-the-three-eyed-crow`. (Do NOT re-mint the fight; just wire the orphan.)

## Slug traps (use these EXACT slugs)
- Bloodraven / the three-eyed crow (as a CHARACTER) = **`brynden-rivers`** — NOT the `three-eyed-crow` species node.
- Bran's direwolf = **`summer`** — the catspaw edges use a phantom `brans-direwolf` slug (no node); new wolf edges → `summer`.
- `black-gate` (NOT the-black-gate) · `bran-stark` (127 edges) · `meera-reed` (the canonical; a stray `meera` node also exists — prefer `meera-reed`) · `weirwood-paste` lives in `foods/`.
- `bran-becomes-a-greenseer` is the TERMINUS (0 outgoing — leave it a terminus; do NOT invent TWOW downstream).

## Theory gate (HARD)
The greenseer **cosmology** stays GATED — Night's King / time-travel / Hodor-origin / the "Jojen paste" theory / Bran-as-future-architect / Bloodraven-manipulates-everything readings are **NOT** nodes or edges. Only the **textual fact** is in scope: Bran reaches the cave, eats the paste, opens the third eye, sees through the weirwoods; Jojen green-dreams events that then happen. The green dreams are modeled as DREAMS_OF/FORESHADOWS of the *events*, never as proof of a cosmological theory.
