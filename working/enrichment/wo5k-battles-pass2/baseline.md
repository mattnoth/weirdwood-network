# Baseline — A2.5 WO5K-battles (S164, PASS 2 of the multi-pass mini-track)

**Unit:** A2.5 WO5K-battles — the military arc that makes Robb Stark the Young Wolf. The LAST 🅰 A-roundup
unit, explicitly **multi-pass**. **THIS IS PASS 2 — THE WESTERLANDS RAID.**

**PASS-2 cut = Robb carries the war west (the victory that breeds the marriage blunder):**
After being crowned and relieving Riverrun (PASS 1), Robb takes the war past the Golden Tooth into the
Lannister heartland: **Oxcross** (the night victory over Stafford's green host) → **the raid** (Ashemark, the
gold mines, the burning coast) → **the storming of the Crag** (Gawen Westerling's seat) → **(EXISTING)** the
**Jeyne-Westerling marriage blunder** → **(EXISTING)** the Red-Wedding-upstream spine.
- **PASS 1 (S163, DONE):** Robb's relief rise (the Whispering Wood → the Battle of the Camps → king-in-the-north).
- **PASS 3 (deferred):** the unravelling (the Fords / Duskendale → the Red-Wedding upstream / the Spicer betrayal mechanism).

**Source chapters (PASS 2 — the battles are NON-POV, reported; read IN FULL, cite `chapter:line`):**
- `acok-sansa-03` — **THE marquee Oxcross account.** Tyrion's full retelling at court (the night raid, Grey Wind
  among the horse lines, the destriers maddened, Stafford slain by Rickard Karstark's lance, the dead lords, the
  captives incl. Martyn Lannister); Lancel's "army of wargs" / "feasted on the flesh of the slain" propaganda.
- `acok-catelyn-06` — the Crag/Ashemark reporting (Robb "marching toward the Crag, the seat of House Westerling");
  Rymund's Oxcross victory song; the victory roll-call ("At Stone Mill, at Oxcross, in the Battle of the Camps…").
- `acok-catelyn-07` — Robb's **conquest of the Crag** celebrated at Riverrun; "he had taken the Crag from the Westerlings."
- `asos-catelyn-01` — Robb returns to Riverrun (the homecoming; the wound; married).
- `asos-catelyn-02` — **THE Crag/marriage chapter.** The storming (Black Walder + the Smalljon scaling parties; Robb
  breaks the gate with a ram; the arrow wound; Ser Rolph yields), the wound festering, Jeyne nursing him, the
  false-news-of-Bran's-death trigger, Grey Wind's kills (the Crag / Ashemark / Oxcross), the Westerling household
  introduced (Sybell, Rolph Spicer the castellan, Raynald, Jeyne, Gawen captured at the Whispering Wood).
- **WHODUNIT-AWARENESS ONLY (gate hard — mostly PASS-3 / AFFC-late):** `affc-jaime-05` / `affc-jaime-07` — the
  Sybell-Spicer pact revealed (Tywin's terms, the pardon, Rolph made Lord of Castamere, Jeyne made barren). **This
  is the RW-upstream BETRAYAL MECHANISM = PASS 3.** Read for awareness; do NOT mint the trap this pass (see below).

---

## THE GAPS (aim here)

### 1. THE CAUSAL RAID SPINE IS EMPTY — three islanded hubs. **WIRE IT.** (the high value)
The whole raid cluster has **6 causal edges and they are ALL the already-built marriage spine.** The three battle
hubs of the raid itself are **causally ISLANDED** (rich in roles or prose, zero in/out causation):
| hub | total edges | causal edges | note |
|-----|------------|--------------|------|
| `battle-of-oxcross` | 10 | **0** (cOut=0 cIn=0) | ISLANDED — only PART_OF + PRECEDES(noise) |
| `taking-of-ashemark` | 3 | **0** (cOut=0 cIn=0) | ISLANDED — the raid beat |
| `storming-of-the-crag` | 4 | 1 out (ENABLES marriage) | **no causal IN**; roster-EMPTY |

Propose the **westward-raid spine** (honor ENABLES-vs-CAUSES — these are military preconditions opened by Robb's
free offensive choices, so **ENABLES**, not CAUSES):
- the **relief-rise → the westward offensive**: `robb-proclaimed-king-in-the-north` (or `battle-of-the-camps`)
  **ENABLES** `battle-of-oxcross` — being crowned + relieving Riverrun freed Robb to carry the war west past the
  Golden Tooth and fall on Stafford's raw levies. (Pick the cleaner antecedent from the text; ENABLES.)
- `battle-of-oxcross` **ENABLES** `taking-of-ashemark` — Stafford's green host destroyed → the Westerlands lay
  open; Robb's host swept on to take Ashemark and the gold mines.
- `taking-of-ashemark` **ENABLES** `storming-of-the-crag` — the raid rolled on through Ashemark to the Crag
  (the Crag node's own wiki prose: "After the Battle of Oxcross … takes castles … including Ashemark … move on to the Crag").
- `storming-of-the-crag` **ENABLES** `robb-weds-jeyne-westerling` — **ALREADY EXISTS. DEDUP. The seam closes here.**

### 2. `storming-of-the-crag` — roster-EMPTY content-rich shell. **ENRICH IT.** (the marquee — PASS-1 Whispering-Wood pattern)
The Crag node has rich **wiki-cited** prose (Smalljon + Black Walder scaling parties; Robb's ram + arrow wound; Grey
Wind's kill; Rolph Spicer the castellan yields) but **ZERO participant roles and NO `LOCATED_AT`.** Convert the
wiki prose → **BOOK-cited** edges from `asos-catelyn-02:143` + `:185`:
- `robb-stark` COMMANDS_IN / AGENT_IN (led the storm, broke the main gate with a ram).
- `jon-umber-son-of-jon` (**the Smalljon**) AGENT_IN — led a scaling party over the walls.
- `walder-frey-son-of-ryman` (**Black Walder**; NOTE the `black-walder-frey` twin — target the alias-bearing
  `walder-frey-son-of-ryman`) AGENT_IN — led the other scaling party.
- `grey-wind` FIGHTS_IN — "Grey Wind killed a man at the Crag" (`asos-catelyn-02:185`).
- `rolph-spicer` COMMANDS_IN (the defending castellan who yielded the castle) — note "which side" in the rationale.
- `storming-of-the-crag` **LOCATED_AT** `crag` (the node has NO location edge — gap).
- `jeyne-westerling` **HEALS** `robb-stark` — "she nursed me until the fever passed" (`asos-catelyn-02:143`). Gap.
- (Robb's arrow wound itself = node-prose / harvest, not an edge — no named attacker.)

### 3. `battle-of-oxcross` roster gaps (DEDUP HARD vs the 7 existing roles, add only the missing)
EXISTING (do NOT re-propose): `robb-stark COMMANDS_IN`, `grey-wind AGENT_IN`, `rickard-karstark AGENT_IN`,
`stafford-lannister VICTIM_IN` + `DIED_AT oxcross`, `stevron-frey VICTIM_IN` + `DIED_AT oxcross`,
`martyn-lannister VICTIM_IN`, `LOCATED_AT oxcross`. Candidates to ADD only if text-anchored + a live node exists:
- `lymond-vikary VICTIM_IN battle-of-oxcross` — "Ser Lymond Vikary is also dead" (`acok-sansa-03:153`); node EXISTS, core_in=0. Gap.
- (Rubert Brax / Lord Crakehall / Lord Jast / Jast's sons — NO clean live single-character nodes; skip or node-prose.)

---

## DEDUP HOT ZONES (LIVE — do NOT re-mint)
- **THE MARRIAGE SPINE IS BUILT** — `storming-of-the-crag ENABLES robb-weds-jeyne-westerling`,
  `robb-receives-false-news-of-brans-death TRIGGERS robb-weds-jeyne-westerling`, `robb-weds-jeyne-westerling
  TRIGGERS red-wedding-conspiracy`. **DO NOT rebuild the marriage→RW chain.** PASS-2 value = wire the battle/raid
  half INTO it.
- **THE WHODUNIT IS ALREADY WIRED** — `grey-wind OPPOSES rolph-spicer` (tier-1) AND `sybell-spicer CONSPIRES_WITH
  tywin-lannister` (tier-1) **BOTH EXIST.** The Spicer-trap betrayal mechanism is already in the graph. Do NOT
  re-mint it. (The full Tywin-pardon/Castamere/barren reveal is AFFC = PASS-3 detail anyway.)
- **The Westerling household web is SATURATED** — gawen PARENT_OF jeyne/raynald/rollam + SPOUSE_OF sybell + RULES
  house-westerling; sybell PARENT_OF…/COMMANDS jeyne; rolph FOUNDED/RULES house-spicer + SWORN_TO; jeyne SPOUSE_OF
  robb + LOVES (robb→jeyne) + FEARS grey-wind; etc. Kinship/allegiance dyads almost all exist. **The dedup WILL kill
  most household-dyad proposals — aim at the GAPS (the raid spine + the Crag roster + jeyne HEALS robb).**
- **PASS-1 hubs** (`battle-in-the-whispering-wood`, `battle-of-the-camps`, `robb-proclaimed-king-in-the-north`) are
  the causal ANTECEDENT — wire FROM them, do NOT rebuild. `gawen-westerling VICTIM_IN battle-in-the-whispering-wood`
  (the PASS-1 seam) already exists.
- **`harrying-of-the-stony-shore`** is the IRONBORN raid on the North (Theon) — the `battle-of-oxcross PRECEDES
  harrying-of-the-stony-shore` edge is temporal noise. **EXCLUDE it from the Westerlands raid.**

## NODE-DUP / RESOLUTION FLAGS (use the right slug; the dup itself is a small-fix, NOT this dip)
- **Black Walder** has twins: `black-walder-frey` (no aliases) AND `walder-frey-son-of-ryman` (alias "Black
  Walder"). **Target `walder-frey-son-of-ryman`** (wiki-canonical, alias-bearing). Flag the dup for small-fixes.
- **The Smalljon** = `jon-umber-son-of-jon` (aliases "The Smalljon" / "Smalljon Umber"). NOT `jon-umber` (= the Greatjon, his father).

## HARD RULES
- **EXCLUDE TWOW** — only the 5 published books. **No theory assertions (GATED)** — evidence/act/MOTIVATES→character
  edges only; the Spicer-trap *reading* stays node-prose (and its act-edges already exist). **No container tag**
  outside the approved 5 — `wo5k` IS approved; tag genuine WO5K-trigger-tree beats `[wo5k]` (Oxcross/Ashemark/the Crag).
- **Verbatim quotes**, single contiguous substring of ONE line, with `chapter:line`. **PASS 2 ONLY** — do NOT reach
  into the Fords / Duskendale (PASS 3). If you see a strong PASS-3 thread (the Spicer betrayal payoff, the Karstark
  rupture's later cost), NOTE it for PASS 3; do not propose it.
