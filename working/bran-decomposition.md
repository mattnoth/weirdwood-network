# BRAN Decomposition: Trigger-Tree, Scorecard, Build Rank

> **Created:** 2026-06-22 (S129)
> **Purpose:** Map the BRAN container's internal causal trigger-tree — the fall (catspaw + the three-eyed-crow's summons) → coma/warging → Theon's sack forces Bran's flight → journey beyond the Wall (Reeds, Hodor, Rickon splits, Coldhands) → Bloodraven's cave → Bran becomes a greenseer; mark what's built vs dark; rank buildable arcs.
> **Read-only:** no graph writes (0 nodes minted, 0 edges added). Local cache only (no HTTP, no wiki refetch).
> **Session:** bran-decomp dip. BRAN is the 5th and last of Matt's approved containers (`{essos, wo5k, north, aegon, bran}`) to get a decomposition dip. It is **greenfield** — Bran added by Matt's S122 override; container-sized journey arc, but almost no causal scaffolding exists.

> **⊗ CROSS-CONTAINER SEAMS.**
> - **`jaime-pushes-bran-from-the-tower`** = BRAN ∩ WO5K (already `[bran, wo5k]`). The fall is BRAN's origin AND a WO5K trigger (it sets Catelyn's southern ride → the catspaw → Tyrion's arrest → the war). Built. ATTACH, never rebuild.
> - **`bran-s-direwolf-kills-the-assassin`** = BRAN ∩ WO5K, currently **UNTAGGED**. It owns the outgoing `CAUSES` into the WO5K Tyrion-accusation chain (→ `littlefinger-names-the-dagger-as-tyrion-s` → `catelyn-seizes-the-moment-and-arrests-tyrion`). This is the seam where Spine 1 forks into WO5K. At build: add `[bran, wo5k]` tag (do NOT rebuild the downstream WO5K chain).
> - **`sack-of-winterfell` / `capture-of-winterfell`** = BRAN ∩ NORTH ∩ WO5K. Theon's taking, already built and WO5K-owned (dual-tagged `[wo5k, north]`). **Bran's flight ATTACHES to `sack-of-winterfell`; do NOT rebuild the Theon thread.** At build: add `[bran]` → `sack-of-winterfell` becomes `[wo5k, north, bran]`.
> - **`robb-receives-false-news-of-brans-death`** (`[wo5k]`, minted S123) — the false death is a consequence of the sack (Theon mounts the boys' burned bodies). It cross-links BRAN→WO5K: Bran's *actual survival in the crypts* is the BRAN-side counterpart to this already-wired WO5K node. Note the seam; the WO5K node is built — do NOT touch it.
> - **The three-eyed-crow / greenseer cosmology** (Night-King / time-travel / hodor-origin / Bloodraven-succession) is GATED THEORY — never a causal node or edge. The greenseer material that is *textual fact* (Bran reaches the cave, eats the paste, sees through the trees) is IN scope; what it *means* is not.

---

## 1. Current Causal State — Verified Against Live Graph

All states verified with `python3 scripts/graph-query.py --container bran`, `--neighbors <slug>`, `--causal-chain <slug>`, and direct node + `edges.jsonl` reads. **Node prose was NOT trusted for edge-state — every causal claim checked against `graph/edges/edges.jsonl`.**

### Container membership (verified)

`--container bran` returns **exactly 3 nodes**:
- `bran-witnesses-jaime-and-cersei` — event.incident, `[bran]`
- `jaime-pushes-bran-from-the-tower` — event.incident, `[bran, wo5k]` (seam)
- `six-wildling-deserters-ambush-bran` — event.incident, `[bran]`

### Spine 1 (THE FALL) — partially BUILT, the only causal structure in the container

The S105 "Bran's fall" smoke-test chain is live and wired (verified via `--causal-chain jaime-pushes-bran-from-the-tower`):

```
bran-witnesses-jaime-and-cersei --[TRIGGERS]--> jaime-pushes-bran-from-the-tower
jaime-pushes-bran-from-the-tower --[CAUSES]--> bran-s-direwolf-kills-the-assassin
  bran-s-direwolf-kills-the-assassin --[CAUSES]--> littlefinger-names-the-dagger-as-tyrion-s
    littlefinger-names-the-dagger-as-tyrion-s --[CAUSES]--> catelyn-seizes-the-moment-and-arrests-tyrion
      catelyn-seizes-the-moment-and-arrests-tyrion --[CAUSES]--> gregor-raids-the-riverlands
      catelyn-seizes-the-moment-and-arrests-tyrion --[MOTIVATES]--> tywin-lannister
```

This is the WO5K fork — from `bran-s-direwolf-kills-the-assassin` onward the chain belongs to the WO5K war-ignition, already built (S105/S105-advisory). **The BRAN-internal gap in Spine 1 is the middle:** the fall → **coma → the three-eyed-crow's "fly or die" summons → Bran wakes (the gift activates)** is entirely UNbuilt. The push is the last built BRAN beat before a hole.

### Spine 2 (THE FLIGHT & JOURNEY) — entirely DARK / MISS

This is the container's reason to exist (Matt's S122 override: the flight-to-the-north journey arc). **It has ZERO event nodes.** Verified by event-node sweep of `graph/nodes/events/` — no node exists for: Bran's coma, the wolf-dreams beginning, the three-eyed-crow dream, Bran waking, the warg-gift naming, hiding in the crypts, emerging to burned Winterfell, the party split (Rickon/Osha vs Bran/Reeds), the journey beyond the Wall, the Black Gate/Nightfort, meeting Coldhands, the wight attack, reaching Bloodraven's cave, the weirwood paste, or becoming a greenseer.

### Node state table — verified

| Node | Type | State |
|---|---|---|
| `bran-witnesses-jaime-and-cersei` | event.incident | `[bran]`; **causal ✓** (TRIGGERS push); AGENT_IN bran-stark |
| `jaime-pushes-bran-from-the-tower` | event.incident | `[bran, wo5k]` seam; **causal ✓** (CAUSES direwolf-kills); AGENT_IN jaime, VICTIM_IN bran |
| `bran-s-direwolf-kills-the-assassin` | event.death | **UNTAGGED** (needs `[bran, wo5k]`); **causal ✓** (CAUSES littlefinger-lie — the WO5K fork); AGENT_IN brans-direwolf + catelyn, VICTIM_IN catspaw-assassin |
| `six-wildling-deserters-ambush-bran` | event.incident | `[bran]`; **0 causal** (DARK); 5 role edges (Stiv/Osha/Wallen/Hali AGENT_IN, bran VICTIM_IN). AGOT Bran IV (agot-bran-05) — Osha proposes taking Bran to Mance. See §4 (sequence trap candidate). |
| `sack-of-winterfell` | event.battle | `[wo5k, north]` (needs `+[bran]`); **0 causal** (PART_OF wo5k + PRECEDES purple-wedding only — see edge-flag); the **flight pivot** |
| `capture-of-winterfell` | event.battle | `[wo5k, north]`; **causal ✓** (CAUSES robb-receives-false-news); WO5K-owned, built |
| `robb-receives-false-news-of-brans-death` | event.incident | `[wo5k]`; **causal ✓** (built S123); the BRAN→WO5K false-death seam |

### Character nodes (HITs) — role-edge targets at build, slug-verified

| Beat-role | Verified slug | Note |
|---|---|---|
| Bran | `bran-stark` | ✅ 127 edges |
| Bran's direwolf | `summer` | ✅ — **note:** the built catspaw edges use the slug `brans-direwolf`, but **no `brans-direwolf` node exists**; the direwolf node is `summer`. Slug-trap — see §7. |
| Hodor | `hodor` | ✅ |
| Jojen Reed | `jojen-reed` | ✅ |
| Meera Reed | `meera-reed` | ✅ |
| Osha | `osha` | ✅ |
| Rickon | `rickon-stark` | ✅ |
| Coldhands | `coldhands` | ✅ |
| Leaf / child of the forest | `leaf` | ✅ |
| **Bloodraven / the three-eyed crow** | **`brynden-rivers`** | ✅ — **EMPTY aliases** (no "Bloodraven"/"Three-eyed crow"/"Lord Brynden"/"The last greenseer"). Discoverability gap — see §7. ALL greenseer/crow causal+role edges target **`brynden-rivers`**. |
| (the dream-crow entity) | `three-eyed-crow` | ⚠ typed **`species`**, NOT a character. **Slug-trap:** the three-eyed crow of Bran's dreams = Bloodraven (`brynden-rivers`). Do NOT wire greenseer edges to the `three-eyed-crow` species node. |

### ⚠ DECOYS — keep OUT of the BRAN spine (verified)

| Node | Why it is NOT a Bran-flight beat |
|---|---|
| `battle-of-winterfell` | 0 edges, fully isolated wiki node = the **TWOW "Battle of Ice"** (Stannis vs Boltons). Out of scope (unwritten). Not Bran. |
| `battle-of-the-reeds` | Historical/legendary **crannogmen** battle (wiki). NOT Jojen/Meera Reed joining Bran. Pure decoy — the name collides. |
| `lightning-strikes-the-tower-direwolf-attacks` | `SUB_BEAT_OF attack-on-castle-black` (ASOS Jon, the Wall) — the direwolf is **Ghost**, killing a Thenn. A NORTH/Jon node, NOT Summer/Bran. |
| `battle-outside-the-gates-of-winterfell` | Ser Rodrik's relief force vs Theon (`PRECEDES capture-of-winterfell`). WO5K/NORTH, not a Bran-internal beat. |

---

## 2. Trigger-Tree — Full BRAN Internal Map

Like NORTH, BRAN has **two spines** that share Bran's character + the warg/greenseer gift as the through-line. Spine 1 (the fall) roots in WO5K and is partially built; Spine 2 (the flight + journey) attaches to the WO5K/NORTH sack seam and is entirely dark.

### Spine 1 — The Fall, the Coma, and the Crow's Summons (AGOT)

```
[BUILT] bran-witnesses-jaime-and-cersei --[TRIGGERS]--> jaime-pushes-bran-from-the-tower
   |                                                          |
   |                                                          +--[CAUSES, BUILT]--> bran-s-direwolf-kills-the-assassin
   |                                                          |     (untagged; FORKS into the WO5K Tyrion-accusation chain — ATTACH, built)
   |                                                          |
   v  [TRIGGERS, DARK — the fall opens the door to the dream; NOT a blunt CAUSES]
[BR1] bran-s-coma-and-the-three-eyed-crow   [MISS — needs mint]
   (agot-bran-03:107 — "Now, Bran, the crow urged. Choose. Fly or die.")
   The fall breaks Bran; in the coma the three-eyed crow (Bloodraven, reaching through the
   weirwood net) summons him. This activates the warg/greenseer gift that drives the whole arc.
   |
   v [ENABLES, DARK — the dream-choice resolves the coma]
[BR1b] bran-wakes-from-his-coma   [MISS — needs mint, may fold into BR1 as terminus]
   (agot-bran-03:125 — "A pair of yellow eyes looked into his own" — Summer on the bed at waking)
   |
   v [ENABLES, DARK — gradual; a RECOGNITION not a CAUSE]
[BR2] jojen-reed-names-bran-a-warg   [MISS — needs mint]
   (acok-bran-05:97 — "Warg," said Jojen Reed; :113 — "A warg is what you are … the winged wolf,
    but you will never fly. Unless you open your eye.")
   The gift, latent since the coma, is named and pointed north toward the crow.
```

### Spine 2 — The Flight and the Journey North (ACOK → ADWD)

```
[SEAM, BUILT — WO5K/NORTH] sack-of-winterfell   [HIT, [wo5k,north], 0 causal]
   (Theon/Ramsay take & burn Winterfell — ATTACH, do NOT rebuild)
   |
   v [CAUSES/ENABLES, DARK — Bran's side of the sack]
[BR3] bran-and-rickon-survive-the-sack-in-the-crypts   [MISS — needs mint]
   (acok-bran-07:47 — "Here in the chill damp darkness of the tomb his third eye had finally opened.")
   They hide in the crypts (revealed RETROSPECTIVELY, not a real-time scene), then emerge to
   find Winterfell burned and Maester Luwin dying beneath the heart tree (acok-bran-07:147).
   |
   v [TRIGGERS, DARK — Luwin's dying counsel triggers the split]
[BR4] bran-s-party-splits-from-rickon   [MISS — needs mint]
   (acok-bran-07:191-207 — Osha: "I'll take Rickon"; Jojen: "Our road is north")
   Rickon + Osha (+Shaggydog) break south/east; Bran + Hodor + Jojen + Meera (+Summer) strike north.
   MOTIVATES driver = Jojen's green dreams (predate the sack — acok-bran-05).
   |
   v [ENABLES, DARK]
[BR5] bran-passes-the-black-gate / bran-meets-coldhands   [MISS — needs 1-2 mints]
   (asos-bran-04:317 — "'Then pass,' the door said." — Sam, a sworn brother, opens the weirwood
    Black Gate beneath the Nightfort; only the Watch oath opens it → Sam is structurally required;
    adwd-bran-01:211 — Coldhands: "A friend. Dreamer, wizard, call him what you will. The last greenseer.")
   |
   v [ENABLES, DARK]
[BR6] bran-reaches-the-cave-of-the-three-eyed-crow   [MISS — needs 1-2 mints]
   (adwd-bran-02:91 wights rise; :123 Leaf's torch rescue; :195 Bloodraven's first words)
   Wights attack on the final approach; Bran wargs Hodor to fight (agency); Leaf/the children
   bring them into the cave; Bran meets Bloodraven (brynden-rivers).
   |
   v [CAUSES, DARK — the transformation]
[BR7] bran-becomes-a-greenseer   [MISS — needs mint — CONTAINER TERMINUS]
   (adwd-bran-03:157 — "Your blood makes you a greenseer. This will help awaken your gifts and wed
    you to the trees." — Bran eats the weirwood paste, opens the third eye, sees through the weirwoods)
   The arc terminus as of ADWD (a deliberate open cliff-hanger; the TWOW expansion is out of scope).
```

### The through-line (why the two spines are one container)

The coma-crow summons (BR1) **activates the gift** that BR2 names and that BR7 fulfils. Spine 1's fall does not merely fork into WO5K — it plants the greenseer seed that Spine 2 harvests. This is the container's spine identity: **the making of the last greenseer**, from the tower window to the weirwood throne.

---

## 3. Juncture Scorecard

Scoring rubric (from `causal-arc-strategy-2026-06-18.md`; 0–2 each axis, max 12):
- **Q (Query-value):** dip failed = 2, plausible = 1, never asked = 0
- **S (Salience):** major chain = 2, minor = 1, trivia = 0
- **X (Cross-POV reach):** 3+ POVs = 2, 2 POVs = 1, 1 POV = 0
- **C (Causal load):** real consequence = 2, mixed = 1, pure sequence = 0
- **B (Beat-readiness / cost):** all/most nodes exist = 2, some = 1, none = 0
- **G (Grounding):** in-saga POV = 2, mixed = 1, wiki-only = 0

**Gate: ≥ 7/12 AND not (G=0, Q<2).** Note: BRAN is greenfield, so **B is uniformly low (0–1)** — every juncture needs ≥1 mint. The cost axis barely discriminates; ranking (§5) leans on clean-attach + value instead.

---

### BR1. Coma → the Three-Eyed Crow's "Fly or Die" → Bran Wakes (the gift activates)

**Description:** The fall breaks Bran; in the coma the three-eyed crow (Bloodraven, reaching through the weirwood net) commands him to *choose — fly or die* (agot-bran-03:107). The choice resolves the coma; Bran wakes to find Summer on the bed (agot-bran-03:125). This is the **origin of the warg/greenseer gift** that powers the entire container.

**Anti-signal check:** Genuine consequence — the dream is not idle color; it activates the faculty the whole arc depends on. But per the subagent's grounding, the fall→coma-dream edge is **TRIGGERS** (the fall *opens the door* to Bloodraven's reach), NOT a blunt CAUSES (the crow's intervention is the real agent). Real C.

**Agency-collapse check:** LOW. The crow MOTIVATES the waking; Bran's dream-choice (fly) is a textually-marked child's decision. No *human* agent hides in the arrow (the crow IS Bloodraven, modeled as the dream-summons, not a separate scene).

**Missing beats:** `bran-s-coma-and-the-three-eyed-crow` — **MISS** (event.incident; agot-bran-03). `bran-wakes-from-his-coma` — **MISS** (may fold into BR1 as the terminus beat rather than a 2nd node). The upstream `jaime-pushes-bran-from-the-tower` is **HIT** (clean attach).

**Container tags:** `[bran]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 0 | 2 | 1 | 2 | **8/12** |

**Verdict: HIGH VALUE.** Roots the greenseer gift; attaches to the BUILT fall spine (cleanest anchor in Spine 1). X=0 (pure Bran-interior coma) is the only weak axis. 1–2 mints + 1 TRIGGERS from the push.

---

### BR2. Jojen Reed Names Bran a Warg (the gift is recognised + pointed north)

**Description:** Jojen, a greendreamer himself, names Bran's wolf-dreams: *"Warg … you are the winged wolf, but you will never fly. Unless you open your eye"* (acok-bran-05:97, :113). This crystallises the latent gift and orients Bran toward the three-eyed crow in the north.

**Anti-signal check — KEY:** The subagent flags this as a **RECOGNITION, not a CAUSE** — the gift existed (the wolf was on the bed at waking; Bran says *"When I sleep I turn into a wolf"* at acok-bran-01:69, before Jojen). Jojen's naming does not *create* the gift. The causal load is genuinely low — this is closer to a node-that-should-exist than a causal juncture. C=1 (mixed).

**Agency-collapse check:** MEDIUM. The warg arc is gradual (agot-bran-03 → acok-bran-01 → acok-bran-03 → acok-bran-05). Modeling it as one event flattens months. The naming scene is the cleanest single anchor, but its edge to BR1 is `ENABLES`/recognition, not a tight cause.

**Missing beats:** `jojen-reed-names-bran-a-warg` (or `bran-s-warg-gift-emerges`) — **MISS** (event.incident; acok-bran-05; cite-chain back to agot-bran-03 + acok-bran-01).

**Container tags:** `[bran]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 0 | 1 | 1 | 2 | **7/12** |

**Verdict: PASS (borderline) — LOWEST priority.** Gates at exactly 7; C=1 because it's recognition not causation. Build it as a node-to-exist (the gift's named anchor), not as a high-value causal juncture. Slots in parallel to Spine 1, no dependency on Spine 2.

---

### BR3. Theon's Sack → Bran & Rickon Survive in the Crypts → Emerge to Burned Winterfell

**Description:** During Theon/Ramsay's sack (the built `sack-of-winterfell` seam), Bran and Rickon hide in the Winterfell crypts, then emerge to find the castle burned and Maester Luwin dying beneath the heart tree (acok-bran-07:47, :147). Theon mounts two miller's boys' burned bodies as Bran and Rickon — the deception that becomes the WO5K `robb-receives-false-news-of-brans-death`.

**Anti-signal check:** Genuine consequence — the sack ENABLES the hiding which ENABLES the flight; Luwin's death TRIGGERS the split. Real C.

**Agency-collapse check — HIGH (the richest in the arc).** The arrow hides ≥3 human decisions: **Osha switches sides** (acok-bran-06:173-185 — enables the hiding strategy), **Bran decides to hide** (in the narrative ellipsis — the crypt-hiding is a *retrospective reveal*, not a witnessed scene), and **Luwin counsels the split** (acok-bran-07). Model the agency as role edges on sub-beats, not one blunt CAUSES.

**Missing beats:** `bran-and-rickon-survive-the-sack-in-the-crypts` — **MISS** (1 mint covers hide+emerge; evidence is retrospective). Upstream `sack-of-winterfell` — **HIT** (clean seam attach; add `[bran]` tag).

**Container tags:** new beat `[bran]`; retag `sack-of-winterfell` → `[wo5k, north, bran]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 1 | 2 | 1 | 2 | **9/12** |

**Verdict: HIGHEST VALUE (tied). Build first.** X=1 (Bran POV + Theon POV cover the sack from both sides). Attaches to the BUILT sack hub — the single highest-leverage greenfield build (the NORTH-N5 analogue: extend a built hub one hop into the new container). Opens all of Spine 2.

---

### BR4. The Party Splits — Rickon + Osha South, Bran + Reeds North

**Description:** Over Luwin's body the group divides: *"I'll take Rickon"* (Osha) / *"Our road is north"* (Jojen) (acok-bran-07:191-207). Rickon + Osha + Shaggydog vanish (the Skagos thread); Bran + Hodor + Jojen + Meera + Summer strike for the Wall.

**Anti-signal check:** Real — the split ENABLES the journey; MOTIVATES driver is Jojen's green dreams (which predate the sack, acok-bran-05). Not pure sequence.

**Agency-collapse check:** MEDIUM. The decision foregrounds Jojen's agency (he says "our road is north"). Model Jojen AGENT_IN + his greendream as the MOTIVATES cause.

**Missing beats:** `bran-s-party-splits-from-rickon` — **MISS** (event.incident; acok-bran-07). All cast chars exist.

**Container tags:** `[bran]` (Rickon's onward thread is a separate, deferred Skagos sub-arc — TWOW, out of scope).

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 0 | 2 | 1 | 2 | **8/12** |

**Verdict: HIGH VALUE.** Clean next hop off BR3's emerge terminus. X=0 (no Rickon/Osha/Reed POV). 1 mint + MOTIVATES from Jojen.

---

### BR5. Journey Beyond the Wall — the Black Gate (Sam) → Coldhands

**Description:** The party reaches the abandoned Nightfort; Sam — a sworn brother of the Watch — speaks the oath and the weirwood **Black Gate** opens (*"'Then pass,' the door said"* asos-bran-04:317; only a Sworn Brother can open it, :217). Beyond the Wall they meet **Coldhands**, who names their destination: *"the last greenseer"* (adwd-bran-01:211).

**Anti-signal check:** Real dependency, not mere sequence — the Black Gate **requires** a sworn brother, so Sam's presence is structurally load-bearing (ENABLES the passage). Coldhands ENABLES the approach north.

**Agency-collapse check:** LOW for the gate (mechanical — Sam's oath opens it). MEDIUM for the journey's driver (Jojen's greendream MOTIVATES; Bran's own decision *"Take me to the crow"* asos-bran-01:216). Agency = Sam (ENABLES gate), Jojen (MOTIVATES), Coldhands (GUIDES).

**Missing beats:** `bran-passes-the-black-gate` + `bran-meets-coldhands` — **MISS** (1–2 mints; distinct locations/agents). `samwell-tarly`, `coldhands` exist; a Nightfort location node may exist (verify at build).

**Container tags:** `[bran]`. (NB: the Black Gate is *also* a NORTH/Wall locus — but the event is Bran-owned; the Nightfort scene is dual-POV with Sam, not a NORTH-spine causal beat.)

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 1 | 2 | 1 | 2 | **9/12** |

**Verdict: HIGHEST VALUE (tied).** X=1 — the Black Gate is **dual-POV**: Bran's chapter AND Sam's (asos-samwell — Sam emerges from the Nightfort well). Coldhands' identity is a canonical dip-class mystery. 1–2 mints.

---

### BR6. Wight Attack → the Cave → Bran Meets Bloodraven

**Description:** On the final approach, wights rise from the snow (adwd-bran-02:91); Bran wargs Hodor to fight; Leaf and the children of the forest rescue them with fire (adwd-bran-02:123) and bring them into the cave, where Bran meets **Bloodraven** (`brynden-rivers`), enthroned in weirwood roots (*"You will never walk again, Bran, but you will fly"* adwd-bran-02:205).

**Anti-signal check:** Real — survival of the attack ENABLES reaching the cave; the meeting is the journey's arrival. Not pure sequence.

**Agency-collapse check:** LOW (wights are undead, the children are external rescuers) — EXCEPT Bran's deliberate warging of Hodor to fight, which IS a human-agency beat (Bran AGENT_IN, via Hodor). Note for build.

**Missing beats:** `bran-reaches-the-cave-of-the-three-eyed-crow` — **MISS** (1–2 mints; the meeting is the load-bearing beat, the wight-attack an obstacle sub-beat). `brynden-rivers`, `leaf`, `summer`, `hodor`, `coldhands` exist.

**Container tags:** `[bran]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 0 | 2 | 1 | 2 | **8/12** |

**Verdict: HIGH VALUE.** The arc's destination; Bloodraven revealed. X=0 (pure Bran POV north of the Wall). All greenseer/crow edges target `brynden-rivers` (NOT the `three-eyed-crow` species node — §7).

---

### BR7. Bran Eats the Weirwood Paste → Becomes a Greenseer (CONTAINER TERMINUS)

**Description:** Leaf feeds Bran the weirwood paste; Bloodraven instructs him to *go into the roots* (adwd-bran-03:167); Bran opens the third eye, slips into the weirwood, and sees his father in the Winterfell godswood — his first greenseer vision (*"Your blood makes you a greenseer … this will help awaken your gifts and wed you to the trees"* adwd-bran-03:157). The container's hard terminus as of ADWD.

**Anti-signal check:** Real CAUSES — the paste + instruction transform Bran into a greenseer; concrete consequence (Bran AGENT_IN; Leaf + Bloodraven instruct).

**Agency-collapse check:** LOW–MEDIUM — Leaf administers, Bloodraven instructs, but *"He ate"* (adwd-bran-03:161) is Bran's own choice. Tag Bran AGENT_IN the transformation.

**Missing beats:** `bran-becomes-a-greenseer` (or `bran-eats-the-weirwood-paste`) — **MISS** (1 mint; the terminus). Upstream BR6 meeting MISS (build BR6 first or co-mint).

**Container tags:** `[bran]`. **TERMINUS — do NOT model the TWOW expansion** (deeper visions, the Hodor/past-sight cosmology) — gated/unwritten.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 0 | 2 | 1 | 2 | **9/12** |

**Verdict: HIGHEST VALUE (tied) — the payoff.** Q=2: "how did Bran become a greenseer?" is the canonical arc-terminus dip question and it **fails on the dark graph today** (0 nodes for the transformation). X=0 (interior). The container's reason to exist.

---

## 4. Sequence-Only Traps (SKIP/DEFER)

| Juncture | Why Skip/Defer |
|----------|---------------|
| **`six-wildling-deserters-ambush-bran`** (AGOT Bran IV) | KEEP as `[bran]` scaffolding, but it is a **dead-end incident**, not a spine juncture — it has no clean outgoing causal edge into the flight arc (Grey Wind/Summer kill the deserters; Bran is rescued; nothing downstream changes). 5 role edges already cover it. Do NOT force a CAUSES into Spine 2. |
| **`battle-of-winterfell` / `battle-of-the-reeds` / `lightning-strikes-the-tower-direwolf-attacks` / `battle-outside-the-gates-of-winterfell`** | HARD SKIP — decoys (TWOW Battle of Ice / historical crannogmen battle / Jon's Wall (Ghost) / Rodrik-vs-Theon). Verified §1. Keep OUT of the Bran spine. |
| **The warg-gift "naming" as a CAUSE** | The gift predates Jojen's naming (acok-bran-01:69). Model BR2 as a recognition/`ENABLES` node-to-exist, NOT a `CAUSES`. Adding CAUSES would overclaim (the AEGON §4 "sibling-takings" trap, analogue). |
| **Rickon + Osha's onward thread (Skagos)** | DEFER (TWOW). The split (BR4) terminates Bran's side; Rickon's journey is unwritten. Do NOT mint Skagos beats. |
| **The crypt-hiding as a real-time scene** | It is a **retrospective reveal** (acok-bran-07), not a witnessed scene. Mint BR3 with retrospective evidence; do NOT invent a blow-by-blow crypt scene. |
| **Bloodraven's promise (adwd-bran-02:205) as the transformation** | The promise (BR6) is the *meeting*; the transformation (BR7) is the paste+instruction in adwd-bran-03. Two distinct beats — do NOT collapse them. |
| **Coldhands as a CAUSE / independent agent** | Coldhands is Bloodraven's instrument. Model him AGENT_IN the escort (ENABLES), with Bloodraven as the ultimate MOTIVATES driver — not `coldhands CAUSES arrival`. |
| **Greenseer cosmology / Night-King / time-travel / hodor-origin** | HARD SKIP — GATED THEORY. Never a causal node or edge. Only the *textual fact* (reaches cave, eats paste, sees through trees) is in scope. |
| **Two "third eye" openings** | acok-bran-07:47 (the **warg** third eye, in the crypts) ≠ adwd-bran-03 (the **greenseer** third eye, the deeper opening). Don't conflate — BR3's crypt-line is warg-sight; BR7 is greensight. |

---

## 5. Ranked Build Order

Priority = clean attach to an existing anchor + value, then natural spine order (BRAN is greenfield, so cost ≈ uniform; the two anchored junctures lead). Two existing anchors: the **built fall spine** (Spine 1) and the **HIT `sack-of-winterfell` seam** (Spine 2).

### Rank 1 — BR3: Sack → Crypts → Emerge (open Spine 2 off the built sack hub)

**Why first:** 9/12, cross-POV (Theon), and it extends a BUILT hub (`sack-of-winterfell`, HIT) one hop into BRAN — the highest-leverage greenfield move (NORTH-N5 analogue). Opens the entire journey spine.
- Mint: `bran-and-rickon-survive-the-sack-in-the-crypts` (event.incident; acok-bran-07:47/:147)
- Wire: `sack-of-winterfell --[CAUSES]--> bran-and-rickon-survive-the-sack-in-the-crypts` (Bran's side of the sack)
- Role/agency: `osha AGENT_IN` (the side-switch that enables hiding); model Luwin's dying counsel as the TRIGGERS into BR4
- Retag: `sack-of-winterfell` → `[wo5k, north, bran]`
- Note seam: this is the BRAN-side counterpart to the WO5K `robb-receives-false-news-of-brans-death` (Theon's fake-death deception) — do NOT touch the WO5K node
- Scope: ~40 min, 1 mint + 1-2 edges + retag

### Rank 2 — BR1: Coma → Fly-or-Die → Wakes (root the gift off the built fall spine)

**Why second:** 8/12, attaches to the BUILT fall spine (`jaime-pushes-bran-from-the-tower`, HIT) — the other clean anchor. Roots the warg/greenseer gift that BR7 fulfils. Independent of Spine 2, so buildable anytime.
- Mint: `bran-s-coma-and-the-three-eyed-crow` (event.incident; agot-bran-03:107) [+ optional `bran-wakes-from-his-coma`, agot-bran-03:125 — or fold waking in as the terminus beat]
- Wire: `jaime-pushes-bran-from-the-tower --[TRIGGERS]--> bran-s-coma-and-the-three-eyed-crow` (the fall opens the door — TRIGGERS not CAUSES)
- Role: `brynden-rivers` as the dream-summoner (the crow = Bloodraven) — model as a light MOTIVATES/role, NOT a separate tunnel-scene node
- Scope: ~40 min, 1-2 mints + 1 TRIGGERS. Tag `[bran]`. **Also tag `bran-s-direwolf-kills-the-assassin` → `[bran, wo5k]`** (the untagged Spine-1 seam — housekeeping, do at build-step 0).

### Rank 3 — BR7: Bran Becomes a Greenseer (the terminus payoff)

**Why third:** 9/12, **Q=2** (the canonical failed query), the container's terminus. Highest single query-value. Build the terminus anchor early so the journey hops (BR5/BR6) have a target to climb toward; it co-mints cleanly with BR6.
- Mint: `bran-becomes-a-greenseer` (event.incident; adwd-bran-03:157/:167)
- Wire: `bran-reaches-the-cave-of-the-three-eyed-crow --[CAUSES]--> bran-becomes-a-greenseer` (needs BR6 — co-build)
- Role: `bran-stark AGENT_IN`; `leaf` + `brynden-rivers` as instructors. **All edges target `brynden-rivers`, NOT the `three-eyed-crow` species node.**
- Scope: ~30 min, 1 mint + role edges (co-build with BR6)

### Rank 4 — BR5: Black Gate (Sam) → Coldhands (the threshold)

**Why fourth:** 9/12, dual-POV (Sam). Attaches to BR4's terminus; bridges the Wall into the magic North. Sam's oath is a real structural dependency.
- Mint: `bran-passes-the-black-gate` (event.incident; asos-bran-04:317) + `bran-meets-coldhands` (adwd-bran-01:211)
- Wire: BR4 → `bran-passes-the-black-gate`; `samwell-tarly --[ENABLES]--> bran-passes-the-black-gate` (the oath); `bran-passes-the-black-gate --[ENABLES]--> bran-meets-coldhands`
- Scope: ~45 min, 1-2 mints + edges

### Rank 5 — BR6: Wight Attack → Cave → Meets Bloodraven (the arrival)

**Why fifth:** 8/12, the destination. Attaches to BR5's Coldhands terminus; co-builds with BR7 (the meeting → the transformation).
- Mint: `bran-reaches-the-cave-of-the-three-eyed-crow` (event.incident; adwd-bran-02:195/:205; wight-attack as a sub-beat at :91)
- Wire: `bran-meets-coldhands --[ENABLES]--> bran-reaches-the-cave...`; role `leaf AGENT_IN` (rescue), `bran-stark AGENT_IN` (wargs Hodor)
- Scope: ~40 min, 1-2 mints + edges

### Rank 6 — BR4: The Party Splits (Spine-2 connective tissue)

**Why sixth:** 8/12 but pure connective — bridges BR3's emerge to BR5's journey. Build after its endpoints exist so it has a clean attach + terminus.
- Mint: `bran-s-party-splits-from-rickon` (event.incident; acok-bran-07:207)
- Wire: `bran-and-rickon-survive-the-sack... --[TRIGGERS]--> bran-s-party-splits-from-rickon` (Luwin's counsel); `jojen-reed MOTIVATES` (greendreams)
- Scope: ~25 min, 1 mint + 2 edges

### Rank 7 — BR2: Jojen Names Bran a Warg (node-to-exist, lowest causal load)

**Why last:** 7/12, C=1 (recognition not causation). A node-that-should-exist anchoring the named gift between BR1 and the journey. Lowest priority; slots in parallel to Spine 1 whenever convenient.
- Mint: `jojen-reed-names-bran-a-warg` (event.incident; acok-bran-05:97/:113)
- Wire: `bran-s-coma-and-the-three-eyed-crow --[ENABLES]--> jojen-reed-names-bran-a-warg` (the gift, now named); `jojen-reed AGENT_IN`
- Scope: ~25 min, 1 mint + 1-2 edges

### Build-step 0 (housekeeping, do at start of build session, NOT this dip)
- **Tag the untagged seam:** `bran-s-direwolf-kills-the-assassin` → add `containers: [bran, wo5k]`.
- **Retag the sack:** `sack-of-winterfell` → `[wo5k, north, bran]`.
- **Backfill `brynden-rivers` aliases** (empty today): add "Bloodraven", "Lord Bloodraven", "Lord Brynden", "Three-eyed crow", "The last greenseer" — THEN `weirwood refresh` (alias change → rebuild resolver). Without this every greenseer edge is mint-discoverable but the *node* is query-invisible by its common names.
- **Flag (do NOT fix here):** `sack-of-winterfell --[PRECEDES]--> purple-wedding` is a cross-theater PRECEDES (ACOK sack → ASOS wedding) that looks like a wiki-ingestion artifact, same class as the AEGON suspicious PRECEDES — review at build.
- **Slug discipline:** the catspaw edges use `brans-direwolf` but no such node exists; the direwolf is `summer`. New role edges for Bran's wolf target `summer`; flag the `brans-direwolf` orphan-slug.

**Batching recommendation (dip-driven small batches, per `causal-arc-strategy`):** Batch A = BR3 + BR1 + BR2 + build-step-0 housekeeping (the two anchored junctures + Spine-1 tail; ~4 mints, attaches to two built hubs). Batch B = BR4–BR7 (the journey spine; ~5-6 mints, builds top-down from the terminus). Verify each batch with a fresh subagent against the local cache before the next.

---

## 6. Cross-Container Attach-Points + Seams Map

| Arc | Upstream Attach | Downstream Terminus | Attach status | Container tag |
|-----|----------------|---------------------|---------------|---------------|
| BR1: coma → wakes | `jaime-pushes-bran-from-the-tower` (HIT, built) | `bran-s-coma-and-the-three-eyed-crow` (new) | source HIT; beat MISS | `[bran]` |
| BR2: warg named | `bran-s-coma...` (BR1) | `jojen-reed-names-bran-a-warg` (new) | BR1 MISS; beat MISS | `[bran]` |
| BR3: sack → crypts | `sack-of-winterfell` (HIT, built seam) | `bran-and-rickon-survive-the-sack...` (new) | source HIT; beat MISS | `[bran]` (retag sack `[wo5k,north,bran]`) |
| BR4: party splits | `bran-and-rickon-survive...` (BR3) | `bran-s-party-splits-from-rickon` (new) | both MISS | `[bran]` |
| BR5: Black Gate → Coldhands | `bran-s-party-splits...` (BR4) | `bran-meets-coldhands` (new) | both MISS; Sam/Coldhands chars HIT | `[bran]` |
| BR6: cave → Bloodraven | `bran-meets-coldhands` (BR5) | `bran-reaches-the-cave...` (new) | both MISS; brynden-rivers HIT | `[bran]` |
| BR7: becomes greenseer | `bran-reaches-the-cave...` (BR6) | `bran-becomes-a-greenseer` (new) | both MISS | `[bran]` TERMINUS |

**Cross-container seams (ATTACH, never rebuild):**
1. **`jaime-pushes-bran-from-the-tower`** — BRAN ∩ WO5K (already `[bran, wo5k]`). The fall is BRAN's origin AND the WO5K war-ignition trigger. Built. ATTACH.
2. **`bran-s-direwolf-kills-the-assassin`** — BRAN ∩ WO5K, **UNTAGGED**. Owns the `CAUSES` fork into the WO5K Tyrion-accusation chain. Tag `[bran, wo5k]` at build; do NOT rebuild the downstream (littlefinger-lie → catelyn-arrests-tyrion → gregor-raids, all WO5K, built).
3. **`sack-of-winterfell` / `capture-of-winterfell`** — BRAN ∩ NORTH ∩ WO5K. Theon's taking, WO5K-owned + NORTH-tagged, built. Bran's flight (BR3) ATTACHES to `sack-of-winterfell`; add `[bran]`. Do NOT rebuild the Theon/Reek thread.
4. **`robb-receives-false-news-of-brans-death`** — BRAN ↔ WO5K (`[wo5k]`, built S123). Theon's fake-death deception is the WO5K consequence of the same sack Bran survives in the crypts (BR3). The two are mirror beats across the seam. Note only; the WO5K node is built — do NOT touch.
5. **The Wall / Nightfort (BR5)** — a NORTH/Wall locus, but the Black-Gate passage is a Bran-owned event (dual-POV with Sam), NOT a NORTH causal-spine beat. Keep `[bran]`; do not retag into NORTH.

### Dyad candidate (surface to `dyad-queue.md`, do NOT force into the causal map)
- **Bran ↔ Jojen — the greendreaming bond.** Jojen guides, names, and shepherds Bran north on the strength of his green dreams; this is a *relationship*, best modeled as a `MENTORS`/`GUIDES`-class dyad on the two character nodes, not a causal event chain. Added as **D3** to `working/dyad-queue.md` (see that file). The greendreams themselves act as MOTIVATES *causes* on BR4/BR5 — the dyad is the standing relationship beneath those edges.

---

## 7. Nodes to Mint (Summary Table)

Required across the ranked 7 junctures. BRAN is greenfield — **every spine beat is a mint** (contrast AEGON=2, NORTH=6).

| Node to Mint | Slug | Type | Source | Juncture | Container Tag |
|---|---|---|---|---|---|
| Bran's coma & the three-eyed crow | `bran-s-coma-and-the-three-eyed-crow` | event.incident | agot-bran-03:107 | BR1 (Rank 2) | `[bran]` |
| Bran wakes from his coma | `bran-wakes-from-his-coma` | event.incident | agot-bran-03:125 | BR1 (Rank 2) | `[bran]` — *optional; may fold into BR1 as terminus* |
| Jojen names Bran a warg | `jojen-reed-names-bran-a-warg` | event.incident | acok-bran-05:97/:113 | BR2 (Rank 7) | `[bran]` |
| Bran & Rickon survive the sack in the crypts | `bran-and-rickon-survive-the-sack-in-the-crypts` | event.incident | acok-bran-07:47/:147 | BR3 (Rank 1) | `[bran]` |
| Bran's party splits from Rickon | `bran-s-party-splits-from-rickon` | event.incident | acok-bran-07:207 | BR4 (Rank 6) | `[bran]` |
| Bran passes the Black Gate | `bran-passes-the-black-gate` | event.incident | asos-bran-04:317 | BR5 (Rank 4) | `[bran]` |
| Bran meets Coldhands | `bran-meets-coldhands` | event.incident | adwd-bran-01:211 | BR5 (Rank 4) | `[bran]` |
| Bran reaches the cave of the three-eyed crow | `bran-reaches-the-cave-of-the-three-eyed-crow` | event.incident | adwd-bran-02:195/:205 | BR6 (Rank 5) | `[bran]` |
| Bran becomes a greenseer | `bran-becomes-a-greenseer` | event.incident | adwd-bran-03:157/:167 | BR7 (Rank 3) | `[bran]` TERMINUS |

**TOTAL NODES TO MINT = 8–9** (depending on the BR1 waking fold + BR5/BR6 granularity calls). The build session decides exact granularity — lean coarse where sub-beats add no causal value (the §4 granularity-overclaim discipline).

**Nodes that EXIST and only need wiring / retag (not mints):**
- `sack-of-winterfell` → incoming-attach point for BR3; retag `[wo5k, north, bran]`
- `jaime-pushes-bran-from-the-tower` → outgoing `TRIGGERS` into BR1 (HIT, built)
- `bran-s-direwolf-kills-the-assassin` → container retag `[bran, wo5k]` (build-step 0)

**Dedup / fix / slug checks required (run before/at build):**
- **`brynden-rivers` = Bloodraven = the three-eyed crow.** All greenseer/crow edges target `brynden-rivers`; the `three-eyed-crow` node is `species` (do NOT wire to it). **Backfill brynden-rivers aliases + `weirwood refresh`** (build-step 0).
- **`summer` vs `brans-direwolf`:** the catspaw edges use a `brans-direwolf` slug with no node; the direwolf node is `summer`. New wolf role edges → `summer`; flag the orphan slug.
- **Decoys** (`battle-of-winterfell`, `battle-of-the-reeds`, `lightning-strikes-the-tower-direwolf-attacks`, `battle-outside-the-gates-of-winterfell`) — keep OUT; do not accidentally wire BR-beats to them.
- **Suspicious edge:** `sack-of-winterfell --[PRECEDES]--> purple-wedding` — likely wiki-ingestion artifact; review at build (do NOT fix in this dip).
- **Pre-mint dedup gate** (the S105 hard rule): run every candidate beat-description through `event_alias_resolver.py --lookup` + the fuzzy index, eyeball every match ≥0.6, before minting — the ~200 Plate-3 verbose-slug beats are the collision surface.

---

## 8. Harvest Queue Additions

*(Collected during the BRAN chapter dip — POINTED into `working/harvest-queue.md`, append-only. POINT, don't extract. 20 rows added, tag `bran-dip`; 2 cite-drifts caught + fixed at the dip: BR2 `acok-bran-05:97` (was -04) and the Black Gate `asos-bran-04:317` (was :313).)*

The 20 rows (all `status: open`) live in `working/harvest-queue.md`. Spine anchors (line-checked at the dip): the "fly or die" crow (agot-bran-03:107), Summer at waking (:125), the warg naming (acok-bran-05:97/:113), the crypt third-eye (acok-bran-07:47), the party split (acok-bran-07:207), the Black Gate (asos-bran-04:317, +:209/:307), Old Nan's Long-Night story (agot-bran-04:41, foreshadowing), Coldhands names "the last greenseer" (adwd-bran-01:211), Bloodraven's first words + "you will fly" (adwd-bran-02:195/:205), Brynden's self-naming (adwd-bran-03:19), the paste ("your blood makes you a greenseer" :157; taste :163; instruction :167), and rich place/appearance rows for Bloodraven's cave + the children of the forest (adwd-bran-02:183/:191/:193; adwd-bran-03:115).

**These rows are the node `## Quotes` / `## Appearances & Description` source material for the build session** — each new BR-beat node gets its Tier-1 anchor quote from this set (the AEGON/NORTH pattern: ground every minted beat with a verbatim book cite). The Bloodraven appearance/place rows upgrade the `brynden-rivers` node when its aliases are backfilled.
