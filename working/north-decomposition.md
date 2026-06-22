# NORTH Decomposition: Trigger-Tree, Scorecard, Build Rank

> **Created:** 2026-06-22
> **Purpose:** Map the NORTH container's internal causal trigger-tree; mark what's built vs dark; rank buildable arcs.
> **Read-only:** no graph writes. Local cache only (no HTTP calls).
> **Session:** north-decomp dip

> **⊗ CROSS-CONTAINER SEAMS.**
> - **`capture-of-winterfell` / `sack-of-winterfell`** = WO5K ∩ NORTH. Already tagged `containers: [wo5k, north]`. Built-once per WO5K-ownership rule. The Theon/Reek thread in these two nodes is owned by WO5K.
> - **Post-Ramsay-capture NORTH scope:** `wedding-of-ramsay-bolton-and-arya-stark`, `theon-carries-jeyne-up-battlements-stairs`, and the Bolton/Stannis political thread are `[north]`-only.
> - **`robb-proclaimed-king-in-the-north`** is currently tagged `[wo5k]`. It sits on the WO5K/NORTH seam — see §6 for the boundary-call Matt needs to make.
> - **`stannis-moves-to-the-wall`** (not yet minted) will be a NORTH-WO5K bridge (Stannis answers the Watch's plea after the Wall battle). Note as future bridge.
> - **Pink Letter (`bastard-letter` artifact) is NORTH-only**, not a bridge, despite mentioning WO5K characters.

---

## 1. Current Causal State — Verified Against Live Graph

All states verified with `--neighbors`, `--causal-chain`, and `event_alias_resolver.py --lookup`.

### Two Spines — Jon's Arc (Watch) + Bolton/Stannis Political Thread

**NORTH has two distinct narrative spines:**
1. **Jon's arc** — from the Watch oath (AGOT) through the Wall battle (ASOS) through his Lord-Commander era (ADWD) to the stabbing.
2. **Bolton/Stannis thread** — from Roose's betrayal at the Red Wedding → Warden of the North → Ramsay's hold on Winterfell → Stannis's northern campaign → the Pink Letter.

### Shared WO5K Attach-Point

The Jon spine and the WO5K container share root causality at `execution-of-eddard-stark`. The causal chain from that node currently walks:

```
execution-of-eddard-stark --[CAUSES]--> robb-proclaimed-king-in-the-north (HIT, [wo5k])
execution-of-eddard-stark --[MOTIVATES]--> robb-stark
```

This is a WO5K terminus; NORTH picks up independently via Jon's Watch oath (AGOT Jon VII) and the Bolton post-Red-Wedding arc.

### Jon's Arc — Verified Node/Edge State

| Beat | Slug | Node? | Causal State |
|------|------|-------|--------------|
| Joins the Watch (oath) | `jon-joins-the-nights-watch` | **MISS** | needs mint |
| Great Ranging (expedition departs) | `great-ranging` | HIT (tier-2, wiki) | **0 causal edges in edges.jsonl** (note: node's ## Edges section lists CAUSES text, but these are NOT wired in edges.jsonl — verified via `--neighbors`) |
| Fight at the Fist | `fight-at-the-fist` | HIT | PRECEDES-only (no causal). `battle-of-the-fist-of-the-first-men` is a redirect alias, `same_as: fight-at-the-fist` |
| Mutiny at Craster's Keep / death of Mormont | `mutiny-at-crasters-keep` | HIT | **0 causal both directions** |
| Qhorin commands Jon to yield | `qhorin-commands-jon-to-yield-if-captured` | HIT (role edges only) | 0 causal outgoing |
| Jon kills Qhorin Halfhand | `jon-kills-qhorin-halfhand` | HIT (3 role edges) | **0 causal outgoing** — dark terminus |
| Jon spares Ygritte | `jon-spares-ygritte` | HIT (role edges only) | 0 causal |
| Attack on Castle Black (Mance's assault) | `attack-on-castle-black` | HIT | PRECEDES + 5 SUB_BEAT_OF children; **0 causal in/out** |
| Night battle atop the Wall | `night-battle-atop-the-wall` | HIT | SUB_BEAT_OF attack-on-castle-black; **0 causal** |
| Battle beneath the Wall (Mance's ground assault) | `battle-beneath-the-wall` | HIT | PART_OF war-of-five-kings + PRECEDES; **0 causal** |
| Stannis arrives / routs wildlings | `stannis-defeats-wildlings` / `stannis-at-the-wall` | **MISS** | no node exists |
| Jon elected Lord Commander | `jon-elected-lord-commander` | **MISS** | no node exists |
| Execution of Janos Slynt | `execution-of-janos-slynt` | HIT (Plate 3 stub, role edges) | **0 causal in/out** |
| Jon allows free folk through the Wall | `hostage-boys-pass-through` | HIT (partial — this is the hostage exchange moment, ADWD Jon XII) | role edges, **0 causal** |
| Jon is stabbed repeatedly | `jon-is-stabbed-repeatedly` | HIT (Plate 3 stub, role edges) | **0 causal in/out** — terminus dark |

**Confirmed quotes grounding key Jon beats:**
- Oath swearing (AGOT Jon VII, line 147): "Night gathers, and now my watch begins... I am the sword in the darkness."
- Stannis to Jon after battle (ASOS Jon XI, line 57): "I know you held the gate here. If not, I would have come too late."
- Slynt execution (ADWD Jon II, line 385): "Longclaw descended." / "Jon glanced back at Stannis. For an instant their eyes met. Then the king nodded and went back inside his tower."
- Pink Letter (ADWD Jon XIII, lines 229–235): "Your false king is dead, bastard." / "I want my bride back."
- Jon announces march to Winterfell (ADWD Jon XIII, line 295): "I ride to Winterfell alone, unless … is there any man here who will come stand with me?"
- Stabbing (ADWD Jon XIII, line 323): "Bowen Marsh stood there before him, tears running down his cheeks. 'For the Watch.' He punched Jon in the belly. When he pulled his hand away, the dagger stayed where he had buried it."

### Bolton/Stannis Thread — Verified Node/Edge State

| Beat | Slug | Node? | Causal State |
|------|------|-------|--------------|
| Roose named Warden of the North (post-Red-Wedding) | no dedicated node | **MISS** | context lives in character edges; no event node |
| Bolton-Frey hold on the North | no node | **MISS** | referenced obliquely in roose-bolton edges |
| Ramsay-Arya fake wedding | `wedding-of-ramsay-bolton-and-arya-stark` | HIT | PRECEDES; **0 causal in/out** |
| Theon and Jeyne escape Winterfell | `theon-carries-jeyne-up-battlements-stairs` | HIT (partial — the staircase beat only) | role edges; **0 causal** |
| Taking of Deepwood Motte (Stannis) | `taking-of-deepwood-motte` | HIT | PART_OF WO5K + PRECEDES; **0 causal** |
| Fight by Deepwood Motte | `fight-by-deepwood-motte` | HIT | PART_OF WO5K + PRECEDES; **0 causal** |
| Stannis marches on Winterfell | no node | **MISS** | |
| Stannis's army stalls (crofters'-village march) | no node | **MISS** | |
| Karstark betrayal of Stannis (Arnolf Karstark) | no node | **MISS** | (different from Rickard Karstark execution, which is [wo5k]) |
| Pink Letter arrives at Castle Black | `bastard-letter` artifact exists; no *event* node for the receiving | **MISS** (event) | artifact node exists only |
| Battle of Ice / Stannis vs Bolton | no node | **MISS** | TWOW territory, but foreshadowed in Pink Letter |

**Additional relevant nodes found:**
- `wedding-of-roose-bolton-and-walda-frey` — HIT, PRECEDES-only, 0 causal
- `mance-rayder-brought-to-execution` — HIT, LOCATED_AT + role edges, 0 causal (ADWD Jon III)
- `jon-argues-against-the-dreadfort-attack` — HIT, 2 role edges, 0 causal outgoing
- `queen-s-men-push-stannis-harder-for-sacrifice` — HIT, 0 causal
- `cersei-s-plot-to-assassinate-jon-snow` — HIT, 3 role edges, 0 causal (AFFC)

### Ironborn Arc (seam with WO5K — DO NOT REBUILD)

Already wired by the WO5K work but relevant to understand the seam:

```
balon-declares-himself-king [HIT, wo5k]
  --[CAUSES]--> ironborn-invasion-of-the-north [HIT, wo5k]
    --[CAUSES]--> fall-of-moat-cailin [HIT]
    --[CAUSES]--> harrying-of-the-stony-shore [HIT]
      --[ENABLES]--> capture-of-winterfell [HIT, wo5k, north]
        --[CAUSES]--> robb-receives-false-news-of-brans-death [HIT, wo5k]
          --[TRIGGERS]--> robb-weds-jeyne-westerling [HIT, wo5k]
            --[TRIGGERS]--> red-wedding-conspiracy → red-wedding / robb-is-killed (all wo5k)
```

The `sack-of-winterfell` is dual-tagged `[wo5k, north]` but has **0 causal edges in or out** (verified). This is a NORTH build opportunity (see J4).

### Container Tag Hygiene Finding

Several NORTH-theater nodes are currently tagged only `[wo5k]` that should acquire `[north]` tags at build time (not now — these belong to the build session):
- `robb-proclaimed-king-in-the-north`: currently `[wo5k]` — boundary question (see §6)
- `ironborn-invasion-of-the-north`: currently `[wo5k]` — probably should be `[wo5k, north]` as it operates in NORTH theater; Matt to decide
- `great-ranging`, `fight-at-the-fist`, `mutiny-at-crasters-keep`, `attack-on-castle-black`, `battle-beneath-the-wall`: no `containers:` tag at all — all pure NORTH scope, should be tagged `[north]` or `[north, jon]` at build time

---

## 2. Trigger-Tree — Full NORTH Internal Map

Two root-entry-points into the NORTH container:

### Spine 1: Jon's Watch Arc

```
[SHARED ROOT with WO5K] execution-of-eddard-stark
  |
  v (NORTH ENTRY — no node, needs mint)
jon-joins-the-nights-watch  [MISS — needs mint]
  |
  +--[CAUSES, DARK]--> great-ranging  [EXISTS, untagged, 0 causal edges wired]
       |
       +--[CAUSES, dark in edges.jsonl]--> fight-at-the-fist  [EXISTS, PRECEDES only]
       |     --> survivors retreat → Craster's Keep
       |
       +--[CAUSES, DARK]--> mutiny-at-crasters-keep  [EXISTS, 0 causal]
             --> death of Jeor Mormont
             --> Sam and Gilly flee south

  (...mid-arc, Watch-internal personal beats, tag [jon] only...)
  
  qhorin-commands-jon-to-yield-if-captured [EXISTS, 0 causal out]
    --[CAUSES, DARK]--> jon-kills-qhorin-halfhand [EXISTS, 0 causal out]
      --> Jon accepted among the free folk
      --> Ygritte
      --> Styr / Mance's raiding party
      --> Jon deserts back to the Wall
      
  attack-on-castle-black [EXISTS, SUB_BEAT_OF structure, 0 causal]
    (sub-beat children: night-battle-atop-the-wall, wildlings-attack-the-gate,
     mammoth-attacks-gate-below, lightning-strikes-tower, deaf-dick-follard-killed)
  battle-beneath-the-wall [EXISTS, 0 causal]
  
  [STANNIS ARRIVES — NO NODE] stannis-defeats-wildlings / stannis-at-the-wall [MISS]
    |
    +--[BRIDGE, NORTH←WO5K] stannis-moves-to-the-wall [MISS, future bridge node]
    |
    +--[CAUSES, DARK]--> mance-rayder-brought-to-execution [EXISTS, role only]
    |
    +--[MOTIVATES, DARK]--> Jon offered Lordship of Winterfell / refuses
    
  jon-elected-lord-commander [MISS — needs mint]
    |
    +--[CAUSES, DARK, tag: north, jon]--> execution-of-janos-slynt [EXISTS Plate3, 0 causal]
    |
    +--[CAUSES, DARK, tag: north, jon]--> hostage-boys-pass-through (partial beat)
    |     The bigger NORTH-political decision: Jon allows free folk through the Wall
    |     Proper node needed: jon-allows-free-folk-through-the-wall [MISS]
    |
    +--[ENABLES, DARK]--> bastard-letter / pink-letter event [MISS event; artifact exists]
    |     (Ramsay's letter arrives → Jon reads it → Jon announces march)
    |
    +--[MOTIVATES, DARK]--> jon-is-stabbed-repeatedly [EXISTS Plate3, 0 causal]
```

### Spine 2: Bolton/Stannis Political Thread

```
[WO5K SEAM] red-wedding → roose-bolton kills robb
  |
  v (NORTH ENTRY — no node)
roose-named-warden-of-the-north [MISS]
  |
  +--[CAUSES, DARK]--> bolton-frey-hold-on-the-north [no node; context exists in edges]
       |
       +--[CAUSES, DARK]--> wedding-of-ramsay-bolton-and-arya-stark [EXISTS, PRECEDES only]
       |     --> Theon/Jeyne arc (post-Ramsay-capture = NORTH scope)
       |     --> theon-carries-jeyne-up-battlements-stairs [EXISTS, 0 causal]
       |           needs: [ENABLES or CAUSES]--> jeyne-escape-from-winterfell [MISS event]
       |
       +--[WO5K seam already built] capture-of-winterfell + sack-of-winterfell [wo5k, north]
       
  stannis-marches-on-winterfell [MISS]
    |
    +--[antecedent] stannis-at-the-wall → defeat of wildlings → Northern recruits
    +--[antecedent] taking-of-deepwood-motte [EXISTS, PRECEDES only]
    |
    +--[CAUSES, DARK]--> deaths-on-the-march (wrong — this is a Daenerys node)
    +--[CAUSES, DARK]--> karstark-betrayal-of-stannis (Arnolf Karstark) [MISS]
    +--[CAUSES/ENABLES, DARK]--> stannis-s-army-stalls-at-crofters-village [MISS]
    
  bastard-letter-delivered [MISS event node]
    |
    +--[TRIGGERS]--> jon-announces-march-to-winterfell [MISS event]
    +--[TRIGGERS]--> jon-is-stabbed-repeatedly [EXISTS Plate3, 0 causal upstream]
```

### Cross-spine Bridges

| Bridge point | From | To | Status |
|---|---|---|---|
| Stannis at the Wall | WO5K (`stannis-retreats-from-blackwater` chain) | NORTH (Jon's arc, Watch) | `stannis-moves-to-the-wall` not yet minted — future bridge |
| Ned's execution → North politicized | WO5K (`execution-of-eddard-stark`) | NORTH (`jon-joins-the-nights-watch` root) | Already exists as WO5K terminus; NORTH entry is the Watch oath |
| Red Wedding → Roose as Warden | WO5K (`red-wedding`) | NORTH (Bolton thread) | No bridge node yet; `roose-named-warden-of-the-north` needs mint |

---

## 3. Juncture Scorecard

Scoring rubric (verified from `causal-arc-strategy-2026-06-18.md`, 0–2 each axis, max 12):
- **Q (Query-value):** dip failed = 2, plausible = 1, never asked = 0
- **S (Salience):** major chain = 2, minor = 1, trivia = 0
- **X (Cross-POV reach):** 3+ POVs = 2, 2 POVs = 1, 1 POV = 0
- **C (Causal load):** real consequence = 2, mixed = 1, pure sequence = 0
- **B (Beat-readiness / cost):** all/most exist = 2, some = 1, none = 0
- **G (Grounding):** in-saga POV = 2, mixed = 1, wiki-only = 0

**Gate: ≥ 7/12 AND not (G=0, Q<2).**

---

### N1. Great Ranging → Fist of the First Men → Mutiny at Craster's Keep

**Description:** `great-ranging` exists as a wiki-tier-2 node with 0 wired causal edges; `fight-at-the-fist` exists with PRECEDES only; `mutiny-at-crasters-keep` exists with 0 causal. The node prose in `great-ranging.node.md` declares CAUSES edges to both — but these are NOT in `edges.jsonl`. Wiring is partially prepped (prose describes the consequences); edges need physical creation. The chain: Great Ranging → Fist battle (Others attack, Watch decimated) → survivors retreat → mutiny at Craster's Keep (death of Mormont).

**Anti-signal check:** This is genuine CAUSES logic. The Great Ranging's failure at the Fist is the *direct cause* of the Watch's retreat to Craster's Keep, which is the direct CAUSES/TRIGGERS of the mutiny that kills Mormont. Not sequence — consequence of catastrophe. Real CAUSES.

**Agency-collapse check:** Between Fist battle and mutiny:
- The men's grievances at Craster's Keep (resentment of Craster's selective food sharing, men starving while he eats) are the immediate human decision. MOTIVATES edges: `fight-at-the-fist MOTIVATES [the mutineers]` + `mutiny-at-crasters-keep AGENT_IN [mormont-enemies]`. The chain is manageable — the starvation conditions are the mediating beat, but a simple CAUSES is defensible because the Fist catastrophe IS the cause of being stranded at Craster's in weakened condition.

**Missing beats (from edges.jsonl perspective):**
1. The CAUSES edges themselves — both declared in node prose but NOT wired. These are "easy mint" — just wire what's already described.
2. Possible intermediate: a "survivors-retreat-from-the-fist" beat? The node prose covers this implicitly. A separate mint may not be needed.

**Upstream attach-point:** `great-ranging` (HIT, no causal tag needed — it IS the upstream). The chain starts here. The question is what attaches UPSTREAM to great-ranging: `jon-joins-the-nights-watch` (MISS) or just let great-ranging be the root of this juncture.

**Terminus:** `mutiny-at-crasters-keep` (HIT). Clean hard-stop at Mormont's death.

**Container tags at build:** `great-ranging → [north]`; `fight-at-the-fist → [north]`; `mutiny-at-crasters-keep → [north]`; these are Watch-internal pre-LC personal beats → the Jon sub-tag logic says `[north]` only if they intersect the political theater; Watch-internal = `[jon]` only OR no sub-tag (they predate Jon's LC authority, so likely `[north]` without `[jon]`).

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 1 | 2 | 2 | 2 | **10/12** |

**Verdict: HIGH VALUE, VERY LOW COST.** Beat-readiness = 2 (both nodes exist; the causal edges are prepped in node prose but not wired). Main work is 2–3 CAUSES edges + container tags. Cheapest juncture in the dip.

---

### N2. Stannis at the Wall: Wall Battle → Stannis Arrives → Watch/Wildling Truce Brokered

**Description:** `attack-on-castle-black` and `battle-beneath-the-wall` exist but have 0 causal edges. The narrative consequence is Stannis's timely arrival and routing of Mance's wildling host — but there is NO node for Stannis defeating the wildlings or arriving at the Wall. This is the load-bearing juncture that connects Jon's Watch-arc (Wall defense) to the Stannis/northern-politics arc (his presence at the Wall is what enables his offer to Jon, the Mance execution, the Lord Commander election pressure, and ultimately Stannis's northern campaign).

**Anti-signal check:** The Wall battle → Stannis defeats wildlings chain is genuine CAUSES/TRIGGERS, not just sequence. Stannis arrives at the Wall BECAUSE the Watch is besieged (Davos's counsel, the Watch's plea via Sam's ravens). The rout is the direct consequence of the battle. Real causal chain.

**Agency-collapse check:** Between battle-beneath-the-wall and stannis-arrives:
- Davos DECIDES to advise Stannis to answer the Watch's plea (MOTIVATES)
- Stannis DECIDES to sail north (MOTIVATES, a political choice)
- Melisandre's visions factor in (R'hllor's fire, the shadow)
These agency beats matter, but the load-bearing causal beat is: the Watch's desperate defense → Stannis's intervention. A `stannis-moves-to-the-wall` bridge node (already identified in the SHAPE map as a future WO5K/NORTH bridge) captures this agency.

**Missing beats:**
1. `stannis-defeats-wildlings-at-the-wall` or `stannis-routes-mance-s-host` — **MISS** (needed as the key consequence)
2. `stannis-moves-to-the-wall` — **MISS** (the WO5K→NORTH bridge identified in SHAPE map). This should be `[wo5k, north]` — seam node.

**Upstream attach-point:** `battle-beneath-the-wall` (HIT, 0 causal) OR `attack-on-castle-black` (HIT, 0 causal). Both are valid attach-points; `attack-on-castle-black` is the broader hub with 5 SUB_BEAT_OF children.

**Terminus:** `mance-rayder-brought-to-execution` (HIT) — Stannis's first act after arrival that leads into Jon's LC election pressure and the Mance arc. Or terminate at `stannis-moves-to-the-wall` (the bridge node), letting the NORTH-internal consequences be the next juncture.

**AXIS 4 container tag:** `attack-on-castle-black` → `[north, jon]` (Jon commands the defense; Watch-political). `stannis-moves-to-the-wall` → `[wo5k, north]` (bridge). `stannis-defeats-wildlings-at-the-wall` → `[north]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 1 | 2 | **11/12** |

**Verdict: HIGHEST VALUE JUNCTURE.** The Wall battle is the pivot of the NORTH container — it's the event that brings Stannis north, establishes Jon's credibility, enables the LC election, and catalyzes everything in ADWD. Clean attach (attack-on-castle-black HIT). The mint `stannis-defeats-wildlings-at-the-wall` + bridge `stannis-moves-to-the-wall` = 2 mints + ~3 edges. Very high narrative salience and cross-POV (Jon, Stannis, Melisandre, Davos, Sam).

---

### N3. Lord Commander Election → Slynt Execution → Jon's Authority Established

**Description:** After Stannis arrives and the wildling threat is defeated, the Watch elects a new Lord Commander. Jon is elected (ASOS Jon XII — Jon overhears the conspiracy backing Slynt, which leads the Watch to coalesce around Jon as the alternative). Then Jon's first major authority act is executing Slynt when he refuses orders (ADWD Jon II). `execution-of-janos-slynt` EXISTS (Plate 3 stub, verified role edges), but has **0 causal edges**. There is also NO node for the election itself.

**Anti-signal check:** The election → Slynt execution chain is genuine CAUSES. Jon CANNOT execute Slynt without being Lord Commander; the LC election is a prerequisite that ENABLES the execution. And the execution CAUSES downstream consequences: Stannis's approval (he nods — ADWD Jon II line 389), Alliser Thorne's increased enmity, the seeds of the mutiny. Real causal chain with real consequences.

**Agency-collapse check:** Between LC election and Slynt execution:
- Jon's DECISION to order Slynt to Greyguard (vs kill/exile/pardon) is an agency beat
- Slynt's REFUSAL ("I will not have it!") is the trigger event
Modeling: `jon-elected-lord-commander MOTIVATES jon-snow` + `AGENT_IN jon-snow, execution-of-janos-slynt VICTIM_IN janos-slynt`. Standard MOTIVATES pattern — manageable.

**Missing beats:**
1. `jon-elected-lord-commander` — **MISS** (needs mint; type: event.ceremony; source: ASOS Jon XII)
2. (Note: `jon-overhears-the-conspiracy` EXISTS with 5 edges including COMMANDS_IN tywin-lannister. This is the catalyzing plot beat; connects upstream to the election.)

**Upstream attach-point:** `stannis-defeats-wildlings-at-the-wall` (to be minted in N2) → election as downstream consequence. OR: `jon-overhears-the-conspiracy` (HIT, role edges) → election as downstream. Both are valid; the juncture is modular — buildable after or alongside N2.

**Terminus:** `execution-of-janos-slynt` (HIT, Plate 3 stub). Clean.

**Container tag:** `jon-elected-lord-commander` → `[north, jon]` (authority event at the intersection of political theater and Jon's arc, per AXIS 4).

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 1 | 2 | 1 | 2 | **10/12** |

**Verdict: HIGH VALUE.** 1 mint (`jon-elected-lord-commander`) + 2–3 edges. Extends naturally from N2 (Stannis-at-the-Wall) and terminates at a pre-existing Plate-3 stub. The Slynt execution is one of the most character-defining moments in ADWD Jon and currently has 0 causal connections.

---

### N4. Jon Allows Free Folk Through the Wall → Political Crisis → Pink Letter → Stabbing

**Description:** This is the terminal arc of the NORTH container. Jon's decision to let the free folk through the Wall (ADWD Jon XII — verified via `hostage-boys-pass-through` HIT and the chapter text: "four thousand wildlings would come pouring through the Wall") causes the Watch's internal fracture. Bowen Marsh and Alliser Thorne regard this as a betrayal. The Pink Letter arrives (Ramsay claims to have killed Stannis), Jon announces he will march to Winterfell, and the Watch mutineers stab him.

**Anti-signal check:** The chain Jon-lets-free-folk-through → Watch-fracture → Bowen-Marsh-decides-to-act → stabbing is genuine causal consequence. Jon's ADWD decisions (Slynt execution, free-folk passage, Mance's fake death, the march announcement) are the accumulating provocations that tip the mutineers into action. Not pure sequence — each decision *causes* increased resentment that eventually triggers the stabbing.

**Agency-collapse check:** Very high. The chain is:
- Jon's decision MOTIVATES Bowen Marsh and the mutineers
- The Pink Letter MOTIVATES Jon (announces march to Winterfell)
- The mutineers DECIDE to act (For the Watch)
This needs careful modeling: the MOTIVATES edges are the causal load-bearers here. A blunt CAUSES from "free-folk-through-wall → stabbing" would collapse multiple human agency beats.

**Missing beats:**
1. Proper event node for Jon's free-folk decision: `hostage-boys-pass-through` (HIT) captures the hostage exchange but not the primary decision. A node `jon-allows-free-folk-through-the-wall` (event.decree, ADWD Jon XII) may be needed — the actual gate opening, distinct from the hostage-taking.
2. `bastard-letter-delivered` or `pink-letter-arrives-at-castle-black` (event node for receiving/reading the letter) — **MISS**
3. `jon-announces-march-to-winterfell` (event.incident) — **MISS** (the Shieldhall speech)
4. `watch-mutiny-conspiracy` — check: `mutiny-at-castle-black` EXISTS (HIT, PRECEDES only, 0 causal). This is the event. But: is `mutiny-at-castle-black` the same as `jon-is-stabbed-repeatedly`? Check: the mutiny IS the stabbing. Probably redundant nodes. Need dedup check at build time.

**Upstream attach-point:** `execution-of-janos-slynt` (N3 terminus, HIT) → free-folk decision as downstream. Or `jon-elected-lord-commander` (to be minted in N3). Chains naturally from N3.

**Terminus:** `jon-is-stabbed-repeatedly` (HIT, Plate 3 stub, role edges, 0 causal). Clean — this IS the NORTH terminus identified in the SHAPE map.

**Container tag:** The ADWD LC-era authority beats → `[north, jon]` per AXIS 4. `pink-letter-arrives` → `[north]` (not a bridge per SHAPE map). `jon-is-stabbed-repeatedly` → `[north, jon]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 1 | 2 | 1 | 2 | **10/12** |

**Verdict: HIGH VALUE, LARGE SCOPE.** This is the NORTH terminus arc (stabbing) — very high query value. But scope is larger than N2/N3: 2–3 new mints + agency-collapse modeling = half-session. Build after N2+N3 have established the Jon spine infrastructure.

---

### N5. Red Wedding → Roose Named Warden → Bolton Hold on the North

**Description:** The Bolton/Stannis political thread. After the Red Wedding, Roose Bolton is named Warden of the North by Tywin Lannister. The Boltons hold Winterfell with ironborn cooperation until the Ramsay arc (wedding, Theon/Jeyne). This thread is entirely DARK — no causal edges exist from the Red Wedding into the NORTH political takeover.

**Anti-signal check:** The Red Wedding CAUSES Roose's elevation to Warden — this is GRRM's explicit causal chain (Tywin rewards Roose for betraying Robb). The Bolton hold on the North ENABLES Ramsay's Arya-Stark-fake-wedding. Real CAUSES, not sequence.

**Agency-collapse check:** Between red-wedding and bolton-hold-on-north:
- Tywin DECIDES to name Roose Warden (agency: MOTIVATES edge + AGENT_IN on the naming event)
- Roose DECIDES to accept and consolidate northern power
Both are agency beats but the events are well-documented. Manageable with MOTIVATES edges.

**Missing beats:**
1. `roose-named-warden-of-the-north` or `roose-bolton-appointed-warden` — **MISS** (event.ceremony; source: ASOS Catelyn chapter / wiki)
2. A broader "bolton-consolidate-the-north" beat may be needed to connect to Ramsay's wedding
3. `theon-and-jeyne-escape-winterfell` (the main escape event) — **MISS** (only `theon-carries-jeyne-up-battlements-stairs` exists as a sub-beat of a larger escape action)

**Upstream attach-point:** `red-wedding` (HIT, fully built). Clean — standard attach. `red-wedding → [CAUSES] → roose-named-warden-of-the-north`.

**Terminus:** `wedding-of-ramsay-bolton-and-arya-stark` (HIT, PRECEDES only, 0 causal) OR the escape scene. Both are concrete terminuses.

**Container tag:** The Bolton thread = pure `[north]`. `roose-named-warden-of-the-north` → `[north]`. `wedding-of-ramsay-bolton-and-arya-stark` should acquire `[north]` tag.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 1 | 2 | **11/12** |

**Verdict: VERY HIGH VALUE.** The Bolton/Stannis NORTH thread is entirely DARK. The Red Wedding is already built in WO5K; extending it one hop into the NORTH container via `roose-named-warden-of-the-north` is a high-leverage mint (1 node, 1–2 CAUSES edges) that opens the entire NORTH political spine. Cross-POV: Jon (learns of it via Stannis's intel), Theon/Reek, Davos (White Harbor mission), Bran (via Stark POV). Score equals N2 but slightly cheaper scope — 1 mint + 2 edges.

---

### N6. Stannis Marches on Winterfell → Deepwood Motte → The March → Pink Letter

**Description:** After being at the Wall, Stannis moves his forces south toward Winterfell. He takes Deepwood Motte (`taking-of-deepwood-motte` EXISTS, PART_OF WO5K, 0 causal), mountain clans join him (in stannis-baratheon edges: ALLIES_WITH alysane-mormont, mountain-clans). His army stalls at the crofters'-village in blizzard conditions. The Arnolf Karstark betrayal (Arnolf was secretly allied with Roose Bolton) sabotages his plans. Then the Pink Letter claims he is dead.

**Anti-signal check:** Stannis's march CAUSES the Pink Letter (Ramsay claims to have defeated Stannis and threatens Jon). The march itself is a genuine CAUSES chain: Stannis-moves-to-the-wall → Stannis-marches-on-winterfell → Deepwood-Motte-taken → army-stalls. Some of this is sequence (Deepwood Motte → march south), but the Karstark betrayal introduces real causal weight.

**Agency-collapse check:** High. The Karstark betrayal (Arnolf was feeding information to Roose) introduces a SUSPECTED_OF edge model. The `stannis-s-army-stalls-at-crofters-village` beat may be *caused* by the blizzard (weather, not human agency). The march itself is a CAUSES chain, but the stall's cause is ambiguous (weather + betrayal + logistics). The Pink Letter's relationship to the actual battle outcome is a TWOW spoiler — do not model the Battle of Ice here.

**Missing beats:**
1. `stannis-marches-on-winterfell` — **MISS** (event.battle/campaign)
2. `arnolf-karstark-betrays-stannis` — **MISS** (SUSPECTED_OF edge from Arnolf; deferred until TWOW confirmed, but the `SUSPECTED_OF` edge type exists in the model per arc-enrichment-backlog)
3. The receiving-of-Pink-Letter is modeled under N4, not here

**Upstream attach-point:** `taking-of-deepwood-motte` (HIT, 0 causal) — build N6 to attach CAUSES into the march. OR: `stannis-defeats-wildlings-at-the-wall` (to be minted in N2) → march south.

**Terminus:** `bastard-letter-delivered` (MISS event) — the Pink Letter as the downstream terminus of the march. OR: keep scope tight: terminate at `stannis-marches-on-winterfell` (new node) as a bridge to the N4 arc.

**Container tag:** `stannis-marches-on-winterfell` → `[north]`. Note: Stannis's ADWD presence is fully NORTH-theater; WO5K tag does not follow him north.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 2 | 1 | 1 | 2 | **9/12** |

**Verdict: MEDIUM-HIGH VALUE.** Real causal chain but more mixed C-score (some sequence elements in the march). Best built AFTER N2 and N5 so there are attach-points from both the Wall (N2) and the Bolton thread (N5). The Karstark-Arnolf betrayal edge (SUSPECTED_OF) is a nice add if it gates correctly. 2–3 mints + 3–4 edges.

---

### N7. Qhorin Commands Capture → Jon Kills Qhorin → Jon Among the Free Folk

**Description:** Jon's personal arc deep inside the Frostfangs. `qhorin-commands-jon-to-yield-if-captured` HIT, `jon-kills-qhorin-halfhand` HIT (3 role edges, 0 causal out). The chain: Qhorin commands Jon to infiltrate (yield if captured) → Jon kills Qhorin in staged combat → Jon is accepted by Mance's wildlings. This is the Watch-internal personal arc — Jon's arc, `[jon]`-only scope per AXIS 4.

**Anti-signal check:** Qhorin's command CAUSES the eventual betrayal/killing. Without the order, Jon cannot be accepted among the wildlings. Real CAUSES (not sequence — Qhorin's SPECIFIC ORDER is the seed of all that follows). TRIGGERS is the right type: "a specific spark."

**Agency-collapse check:** Low — Qhorin's order is the agency beat; it is already a node. Jon's execution of the order is AGENT_IN on `jon-kills-qhorin-halfhand`. The chain is clean.

**Missing beats:**
1. A "jon-accepted-by-mance-raiders" or "jon-among-the-free-folk" event — **MISS** (to serve as downstream terminus)
2. Alternatively, terminate at `jon-spares-ygritte` (HIT, role edges, 0 causal) — that node already has the capture-context

**Upstream attach-point:** `qhorin-commands-jon-to-yield-if-captured` (HIT, 0 causal). Clean.

**Terminus:** `jon-kills-qhorin-halfhand` (HIT, role edges). Or extend one hop to Jon-among-free-folk (MISS).

**Container tag:** Pure `[jon]` — Watch-internal personal arc, pre-LC, no NORTH political intersection.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 1 | 1 | 2 | 2 | 2 | **9/12** |

**Verdict: MEDIUM VALUE.** Both nodes exist; minimal minting needed. The causal chain is clean. But this is `[jon]`-only scope and doesn't intersect the NORTH political theater — lower cross-POV reach. Best treated as a `[jon]` sub-track rather than a full NORTH build priority.

---

### N8. Sack of Winterfell → North Destabilized → Robb Cannot Return North

**Description:** `sack-of-winterfell` exists with `[wo5k, north]` dual-tag but **0 causal edges in or out**. The causal consequence: Winterfell's destruction destabilizes the North. Robb cannot return to rebuild it (no castle to hold). This contributes (alongside the Frey betrayal and Karstark abandonment) to Robb's political isolation and his fatal dependency on Walder Frey's renewed alliance. Note: `capture-of-winterfell` already has a CAUSES edge to `robb-receives-false-news-of-brans-death` (WO5K chain). The SACK's consequences are separate.

**Anti-signal check:** CAUTION — this is borderline sequence. "Winterfell is sacked → North is destabilized" is more of a strategic consequence than a direct cause-chain. The sack does not directly CAUSE any specific downstream event node. The destabilization feeds into Robb's political fragmentation (which lives in the WO5K chain already). Better framing: `sack-of-winterfell` CAUSES `bran-stark-flees-winterfell` or `bran-stark-goes-north` (Bran container start) — but that is a Bran arc, not NORTH.

**Revised scope:** The NORTH-political consequence of the sack is Roose Bolton's consolidation — which is modeled better under N5. The sack-of-winterfell node is already dual-tagged `[wo5k, north]`; adding a CAUSES to `roose-named-warden-of-the-north` (N5's mint) would wire the sack into the NORTH political thread cleanly.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 1 | 2 | 1 | 2 | 2 | **9/12** |

**Verdict: SKIP AS STANDALONE — fold into N5.** The sack-of-winterfell is already dual-tagged. Its NORTH-political consequence (Bolton consolidation) is a single edge from sack → roose-named-warden (or via red-wedding → roose-named-warden). Build this 1 edge as part of N5, not as its own juncture.

---

## 4. Sequence-Only Traps (SKIP/DEFER)

| Juncture | Why Skip/Defer |
|----------|---------------|
| **Jon's ACOK personal arc through the Frostfangs (individual scouting scenes)** | Anti-signal: individual scouting beats (attack-on-the-wildlings, jon-spares-ygritte, etc.) are POV-sequence, not consequence-chain. The CAUSES juncture is only Qhorin's order → jon-kills-qhorin (N7). The rest is `[jon]` internal beats, PRECEDES if anything. |
| **Wall battle sub-beats (night-battle-atop-the-wall, wildlings-attack-the-gate, etc.)** | SUB_BEAT_OF structure is already correct — these are children of attack-on-castle-black. Adding CAUSES between sub-beats would be granularity overclaim. PRECEDES already covers ordering. The causal VALUE is the parent: attack-on-castle-black → stannis-arrives (N2). |
| **Mance Rayder's fake death / Melisandre switches Mance for Rattleshirt** | This is TWOW territory and R+L=J-adjacent (Mance rescues Arya-fake). Do NOT build — out of NORTH scope per the "no White Walkers/Others; no R+L=J" exclusion. |
| **Jon's romantic arc with Ygritte (personal beats)** | Watch-internal, [jon]-only. The CAUSES value is nil — Ygritte's death during the Castle Black attack is a consequence of the battle, not a cause of anything downstream. Use ygritte as a participant in battle-beneath-the-wall, not a causal node. |
| **Battle of Ice (Stannis vs Boltons, TWOW)** | TWOW territory. The outcome is disputed (Pink Letter claims Stannis died but is unreliable). Do NOT model — keep `stannis-marches-on-winterfell` as the terminus of the NORTH container at this stage. |
| **Stannis's offer to Jon / Jon refuses lordship** | Agency beat (Jon's refusal), but it is a character decision expressed via Stannis-character edges, not a graph event node. MOTIVATES edges between stannis-at-the-wall and jon-snow are sufficient. No event mint needed. |
| **Jon's death-and-resurrection (TWOW)** | TWOW. Out of scope entirely. `jon-is-stabbed-repeatedly` is the terminus. |

---

## 5. Ranked Build Order

Priority = cheapest real cause first, clean attach+terminus, extends a built chain.

### Rank 1 — N5: Red Wedding → Roose Named Warden (NORTH political thread entry)

**Why first:** cheapest real cause; opens the entire Bolton thread with 1 mint + 2 edges; directly extends the already-built WO5K Red-Wedding chain (`red-wedding` has 3 downstream CAUSES built); clean attach at `red-wedding` (HIT), clean terminus at the new mint `roose-named-warden-of-the-north`.

- Mint: `roose-named-warden-of-the-north` (event.ceremony; ASOS Catelyn VI or via Tywin's decision; also confirmed in stannis-baratheon ALLIES_WITH quote: "Tywin Lannister has named Roose Bolton his Warden of the North")
- Wire: `red-wedding --[CAUSES]--> roose-named-warden-of-the-north`
- Wire: `roose-named-warden-of-the-north --[MOTIVATES]--> roose-bolton` (consolidation decision)
- Optional: `sack-of-winterfell --[ENABLES]--> roose-named-warden-of-the-north` (Boltons sacked it to deliver it; precondition)
- Dedup: confirm no "Roose Bolton named Warden" node exists already
- Scope: ~45 min, 1 mint + 2–3 edges
- Attach: `red-wedding` (HIT, built)
- Terminus: `roose-named-warden-of-the-north` (new)
- Container tag: `[north]`

### Rank 2 — N2: Wall Battle → Stannis Arrives → Defeats Wildlings (NORTH spine entry)

**Why second:** Highest score (11/12); the Wall battle is the pivot of the NORTH container — it establishes Stannis's presence at the Wall, enables everything else in ADWD Jon. The `stannis-moves-to-the-wall` bridge node also settles the WO5K/NORTH seam identified in the SHAPE map.

- Mint: `stannis-defeats-wildlings-at-the-wall` (event.battle; ASOS Jon XI: "I know you held the gate here. If not, I would have come too late.")
- Mint: `stannis-moves-to-the-wall` (event.incident; ASOS Davos chapters — Stannis's decision to sail north; container: `[wo5k, north]` seam)
- Wire: `attack-on-castle-black --[CAUSES]--> stannis-defeats-wildlings-at-the-wall`
- Wire: `stannis-moves-to-the-wall --[CAUSES]--> stannis-defeats-wildlings-at-the-wall`
- Wire: `stannis-defeats-wildlings-at-the-wall --[CAUSES]--> mance-rayder-brought-to-execution` (Stannis captures Mance)
- Scope: ~1 hour, 2 mints + 3–4 edges
- Attach: `attack-on-castle-black` (HIT); `battle-beneath-the-wall` (HIT)
- Terminus: `mance-rayder-brought-to-execution` (HIT) or the new mint
- Container tags: `attack-on-castle-black → [north, jon]`, `battle-beneath-the-wall → [north]`, new mints as noted

### Rank 3 — N1: Great Ranging → Fist → Mutiny at Craster's Keep (Watch spine bootstrap)

**Why third:** Highest beat-readiness (B=2 — both nodes exist, prose declares the edges); almost zero cost; establishes the NORTH causal backbone for the Watch-internal arc. This connects the pre-NORTH-container Watch arc to the NORTH container proper.

- Wire: `great-ranging --[CAUSES]--> fight-at-the-fist` (this edge is declared in great-ranging's node prose but NOT in edges.jsonl — just wire it)
- Wire: `great-ranging --[CAUSES]--> mutiny-at-crasters-keep` (same — declared but not wired)
- Tag: `great-ranging → [north]`, `fight-at-the-fist → [north]`, `mutiny-at-crasters-keep → [north]`
- Scope: ~20 min, 0 mints + 2 CAUSES edges + 3 container tags
- Attach: `great-ranging` is self-contained root; no upstream needed for this juncture
- Terminus: `mutiny-at-crasters-keep` (HIT)
- Agency: Not required — the Fist catastrophe CAUSES the retreat which CAUSES the conditions for mutiny. Low agency-collapse risk.

### Rank 4 — N3: LC Election → Slynt Execution (Jon authority arc)

**Why fourth:** Extends naturally from N2 (Stannis-at-the-Wall creates the political pressure for the LC election). 1 mint + 2 edges. The Slynt execution (already Plate-3-stubbed with role edges) is a major ADWD Jon beat and deserves causal context.

- Mint: `jon-elected-lord-commander` (event.ceremony; ASOS Jon XII; "Jon Snow is the 998th Lord Commander of the Night's Watch")
- Wire: `stannis-defeats-wildlings-at-the-wall --[ENABLES]--> jon-elected-lord-commander` (Stannis's presence shifts the vote dynamics)
- Wire: `jon-elected-lord-commander --[CAUSES]--> execution-of-janos-slynt` (LC authority is prerequisite)
- Wire: `jon-elected-lord-commander --[MOTIVATES]--> jon-snow` (agency: Jon chooses to execute)
- Scope: ~45 min, 1 mint + 2–3 edges
- Attach: `stannis-defeats-wildlings-at-the-wall` (Rank 2 terminus)
- Terminus: `execution-of-janos-slynt` (HIT, Plate 3 stub)
- Container tags: `jon-elected-lord-commander → [north, jon]`, `execution-of-janos-slynt → [north, jon]`

### Rank 5 — N4: Free Folk Through the Wall → Pink Letter → Stabbing (NORTH terminus arc)

**Why fifth:** This is the climactic NORTH terminus (the stabbing is the container's hard terminus). Larger scope (2–3 mints + agency-collapse modeling). Best after N2–N4 establish the Jon LC infrastructure.

- Mint: `jon-allows-free-folk-through-the-wall` (event.decree; ADWD Jon XII — "four thousand wildlings would come pouring through the Wall")
- Mint: `pink-letter-delivered` or `ramsay-s-pink-letter-arrives` (event.incident; ADWD Jon XIII: "the letter was sealed with a smear of hard pink wax")
- Wire: `execution-of-janos-slynt --[MOTIVATES]--> bowen-marsh` (seeds the mutiny's motivation)
- Wire: `jon-allows-free-folk-through-the-wall --[MOTIVATES]--> bowen-marsh` (direct cause of mutiny planning)
- Wire: `pink-letter-delivered --[TRIGGERS]--> jon-is-stabbed-repeatedly` (Jon's announcement → mutineers act)
- Scope: half-session; 2 mints + 3–4 edges + agency-collapse care
- Attach: `execution-of-janos-slynt` (N3 terminus) + `hostage-boys-pass-through` (existing partial node)
- Terminus: `jon-is-stabbed-repeatedly` (HIT, Plate 3 stub)
- Container tags: all `[north, jon]`

### Rank 6 — N6: Stannis Marches South → Deepwood → Bolton Confrontation (political thread)

**Why sixth:** Depends on N2 (Stannis-at-the-Wall) and N5 (Bolton thread) both being built. Medium scope, good value, but the Arnolf Karstark SUSPECTED_OF edge and Battle of Ice ambiguity make this more complex. Build last in the NORTH set.

---

## 6. Cross-Book / Cross-Container Attach-Points Map

| Arc | Upstream Attach | Downstream Terminus | Status of attach-point | Container tag |
|-----|----------------|---------------------|----------------------|---------------|
| N1: Great Ranging chain | `great-ranging` (self-contained root) | `mutiny-at-crasters-keep` | Both HIT | `[north]` |
| N2: Wall battle → Stannis | `attack-on-castle-black` + `battle-beneath-the-wall` | `stannis-defeats-wildlings-at-the-wall` (new) | Source HIT, terminus MISS | `[north, jon]` / `[north]` |
| N2 bridge: Stannis moves to the Wall | `stannis-retreats-to-dragonstone` (WO5K) | `stannis-defeats-wildlings-at-the-wall` (N2) | Retreat HIT; defeats MISS | `[wo5k, north]` bridge |
| N3: LC election → Slynt | `stannis-defeats-wildlings-at-the-wall` (N2) | `execution-of-janos-slynt` | N2 to be built; terminus HIT | `[north, jon]` |
| N4: Free folk → stabbing | `execution-of-janos-slynt` (N3) | `jon-is-stabbed-repeatedly` | Both HIT (once N3 built) | `[north, jon]` |
| N5: Red Wedding → Bolton Warden | `red-wedding` (WO5K, built) | `roose-named-warden-of-the-north` (new) | Source HIT | `[north]` |
| N5 → Ramsay's fake wedding | `roose-named-warden-of-the-north` (N5) | `wedding-of-ramsay-bolton-and-arya-stark` | N5 MISS; terminus HIT | `[north]` |
| N5 → Theon/Jeyne escape | `wedding-of-ramsay-bolton-and-arya-stark` | `theon-carries-jeyne-up-battlements-stairs` | Both HIT | `[north]` |
| N6: Stannis marches | `stannis-defeats-wildlings-at-the-wall` (N2) + `taking-of-deepwood-motte` | `stannis-marches-on-winterfell` (new) | N2 MISS; Deepwood HIT | `[north]` |

**WO5K→NORTH bridges (existing or to mint):**
1. `execution-of-eddard-stark` (WO5K root) — causal ancestor of Jon's Watch arc entry. Connection is indirect (ned-exec → north-secedes → Jon's arc continues independently at the Watch). No direct bridge edge needed; they share a common causal ancestor.
2. `stannis-moves-to-the-wall` — to be minted as `[wo5k, north]` seam (N2 build).
3. `sack-of-winterfell` — already `[wo5k, north]`; add 1 edge to N5 bolt-on.
4. `red-wedding` — WO5K-owned; `roose-named-warden` will be the first NORTH-only downstream.

**Seam ambiguity — Matt's call:**
- `robb-proclaimed-king-in-the-north`: currently `[wo5k]`. This is the first NORTH-political event after Ned's execution. Should it also carry `[north]`? The SHAPE map says: the political North starts with Robb's proclamation. WO5K built it; NORTH should retag it `[wo5k, north]`. Recommend: add `north` tag to this node at build time.
- `ironborn-invasion-of-the-north`: currently `[wo5k]`. The invasion is entirely NORTH-theater (it operates in the North, even though it's WO5K-rooted). Recommend: `[wo5k, north]`. Same for `balon-declares-himself-king`, `fall-of-moat-cailin`, `harrying-of-the-stony-shore`.

---

## 7. Nodes to Mint (Summary Table)

Required for ranked top-5 arcs:

| Node to Mint | Slug | Type | Source | For Juncture | Container Tag |
|---|---|---|---|---|---|
| Roose named Warden of the North | `roose-named-warden-of-the-north` | event.ceremony | ASOS Catelyn VI + ASOS Jon XI (Stannis confirms) | N5 (Rank 1) | `[north]` |
| Stannis defeats wildlings at the Wall | `stannis-defeats-wildlings-at-the-wall` | event.battle | ASOS Jon XI | N2 (Rank 2) | `[north]` |
| Stannis moves to the Wall | `stannis-moves-to-the-wall` | event.incident | ASOS Davos II–III (Davos advises; Stannis decides) | N2/bridge (Rank 2) | `[wo5k, north]` |
| Jon elected Lord Commander | `jon-elected-lord-commander` | event.ceremony | ASOS Jon XII | N3 (Rank 4) | `[north, jon]` |
| Jon allows free folk through the Wall | `jon-allows-free-folk-through-the-wall` | event.decree | ADWD Jon XII | N4 (Rank 5) | `[north, jon]` |
| Pink Letter arrives at Castle Black | `pink-letter-delivered` | event.incident | ADWD Jon XIII (line 227) | N4 (Rank 5) | `[north]` |

**Nodes that EXIST but need causal wiring (not mints):**
- `great-ranging` → needs CAUSES edges to `fight-at-the-fist` + `mutiny-at-crasters-keep` (N1, Rank 3)
- `attack-on-castle-black` → needs CAUSES edge to `stannis-defeats-wildlings-at-the-wall` (N2, Rank 2)
- `execution-of-janos-slynt` → needs CAUSES incoming from `jon-elected-lord-commander` (N3, Rank 4)
- `jon-is-stabbed-repeatedly` → needs causal upstream from N4 builds

**Dedup checks required (run before minting):**
- "Stannis defeats wildlings" vs `battle-beneath-the-wall` (currently 0 causal; the wiki calls the battle "Battle beneath the Wall" — may need to use this existing node rather than mint new)
- "Jon elected LC" vs any wiki-tier-2 node that might exist for the election
- "Pink Letter delivered" vs event content in `bastard-letter` artifact node

---

## 8. Harvest Queue Additions

> **MIGRATED S125** — all 10 pointers below were migrated into `working/harvest-queue.md` during the S125 harvest
> consume-pass. The warden / Slynt-execution / stabbing / Stannis-held-the-gate quotes were ATTACHED to existing
> nodes; the Pink-Letter / Shieldhall / free-folk / Watch-oath / cart-before-the-horse rows were PARKED there
> (homes are N3/N4 nodes not yet minted). This table is now a frozen record — consume from the queue, not here.

*(Collected incidentally during NORTH wiki + graph + chapter investigation — POINT, don't extract)*

| status | kind | book | ref | note | session |
|--------|------|------|-----|------|---------|
| open | quote | asos | sources/chapters/asos/asos-jon-11.md:57 | Stannis to Jon after the Wall battle: "I know you held the gate here. If not, I would have come too late." — load-bearing Tier-1 quote for `stannis-defeats-wildlings-at-the-wall` node's ## Quotes block | 2026-06-22 north-decomp |
| open | quote | adwd | sources/chapters/adwd/adwd-jon-02.md:385 | "Longclaw descended." — the execution of Slynt; exact terminus for `execution-of-janos-slynt` node's ## Quotes block | 2026-06-22 north-decomp |
| open | quote | adwd | sources/chapters/adwd/adwd-jon-02.md:389 | "Jon glanced back at Stannis. For an instant their eyes met. Then the king nodded and went back inside his tower." — Stannis's wordless approval after Slynt execution; evidence for MOTIVATES/ALLIES_WITH edge pattern | 2026-06-22 north-decomp |
| open | quote | adwd | sources/chapters/adwd/adwd-jon-13.md:227 | Pink Letter arrival: "the letter was sealed with a smear of hard pink wax. 'You were right to come at once.'" — Tier-1 evidence for `pink-letter-delivered` event node | 2026-06-22 north-decomp |
| open | quote | adwd | sources/chapters/adwd/adwd-jon-13.md:295 | Jon's Shieldhall announcement: "The Night's Watch will make for Hardhome. I ride to Winterfell alone, unless … is there any man here who will come stand with me?" — Tier-1 quote for `jon-announces-march-to-winterfell` node | 2026-06-22 north-decomp |
| open | quote | adwd | sources/chapters/adwd/adwd-jon-13.md:323 | Stabbing: "Bowen Marsh stood there before him, tears running down his cheeks. 'For the Watch.' He punched Jon in the belly." — Tier-1 evidence for `jon-is-stabbed-repeatedly` node's ## Quotes block (quote currently absent from node) | 2026-06-22 north-decomp |
| open | quote | agot | sources/chapters/agot/agot-jon-07.md:147 | Watch oath: "Night gathers, and now my watch begins. It shall not end until my death." — Tier-1 evidence for `jon-joins-the-nights-watch` node at mint time | 2026-06-22 north-decomp |
| open | quote | asos | sources/chapters/asos/asos-jon-11.md:129 | Stannis to Jon: "Tywin Lannister has named Roose Bolton his Warden of the North, to reward him for betraying your brother." — Tier-1 evidence for `roose-named-warden-of-the-north` event node | 2026-06-22 north-decomp |
| open | description | adwd | sources/chapters/adwd/adwd-jon-12.md:23 | Jon's internal monologue before the free-folk passage: "Four thousand wildlings would come pouring through the Wall. Madness." — physical/decision description for `jon-allows-free-folk-through-the-wall`; harvest the full paragraph for the node's ## Description block | 2026-06-22 north-decomp |
| open | foreshadowing | asos | sources/chapters/asos/asos-jon-11.md:109 | Stannis's "cart before the horse" speech via Davos's counsel: "I was trying to win the throne to save the kingdom, when I should have been trying to save the kingdom to win the throne." — foreshadowing of Stannis's eventual shift to prioritizing the North over the throne; no foreshadowing edge exists | 2026-06-22 north-decomp |
