# WO5K Decomposition: Trigger-Tree, Scorecard, Build Rank

> **Created:** 2026-06-20 (S112 decomposition dip)
> **Purpose:** Map the War of the Five Kings internal causal trigger-tree; mark what's built vs dark; rank buildable arcs.
> **Read-only:** no graph writes. Local cache only.

---

## 1. Current Causal State — Verified Against Live Graph

All states verified with `--neighbors`, `--causal-chain`, and `event_alias_resolver.py --lookup`.

### Root: `death-of-robert-baratheon`

**Causal chain (verified):**
```
death-of-robert-baratheon
  --[CAUSES]--> arrest-of-eddard-stark
    --[CAUSES]--> execution-of-eddard-stark     ← B3 built (S108)
  ned-confesses-to-treason
    --[TRIGGERS]--> execution-of-eddard-stark   ← B3 built (S108)
```

**Outgoing dark side (CONFIRMED NOT WIRED):**
- `death-of-robert-baratheon` has **1 CAUSES** edge only → `arrest-of-eddard-stark`
- The succession-fracture chain (Robert dies → Joffrey illegitimate claim → Stannis/Renly/Robb/Balon all declare) is **entirely DARK**
- The upstream of `battle-of-the-blackwater` is **entirely DARK** (confirmed 0 causal antecedents)
- `shadow-assassination-of-renly` has **0 causal edges** in both directions (DARK)

### Five-King Entry Triggers — Verified Status

| King | Entry Event | Node Exists? | Causal State |
|------|-------------|-------------|--------------|
| Joffrey | `joffrey-demands-coronation` | YES | DARK — 0 causal outgoing, 0 causal incoming |
| Robb | `execution-of-eddard-stark` → North secedes → Robb proclaimed | Ned-exec YES; **Robb-proclamation NO** | DARK downstream of ned-exec |
| Stannis | Joffrey's bastardy + Robert's death → Stannis declares right | No proclamation node | DARK |
| Renly | Robert's death → flees to Highgarden → Tyrell marriage → self-crowns | `wedding-of-renly-baratheon-and-margaery-tyrell` YES | DARK (no causal edges in or out) |
| Balon | Opportunism in power vacuum → invades North | No "Balon declares" or "ironborn invasion" node | DARK |

### Major Downstream Beats — Verified Status

| Beat | Slug | Causal Built? |
|------|------|---------------|
| Shadow kills Renly | `shadow-assassination-of-renly` | DARK (0 causal) |
| Tyrell realignment to Lannisters | No node (`fighting-at-bitterbridge` exists but 0 causal) | DARK |
| Robb proclaimed King in the North | **NO NODE** | DARK (need mint) |
| Gregor raids Riverlands | `gregor-raids-the-riverlands` | PARTIAL — has 1 CAUSES *incoming* from `catelyn-seizes-the-moment-and-arrests-tyrion` (Bran's arc); **no CAUSES outgoing** |
| Battle of Blackwater | `battle-of-the-blackwater` | PARTIAL — **3 downstream CAUSES built (S111)**, UPSTREAM = 0 causal |
| Stannis retreats to Dragonstone | `stannis-retreats-to-dragonstone` | BUILT — downstream of battle-of-the-blackwater (S111) |
| Capture of Winterfell | `capture-of-winterfell` | DARK (only PART_OF + PRECEDES) |
| Sack of Winterfell | `sack-of-winterfell` | DARK (0 causal both directions) |
| Robb weds Jeyne Westerling | `robb-weds-jeyne-westerling` | HAS 1 TRIGGERS outgoing → `red-wedding-conspiracy` |
| Red Wedding conspiracy | `red-wedding-conspiracy` | BUILT — 1 upstream TRIGGERS (Robb-Jeyne) + 2 downstream CAUSES |
| Red Wedding | `red-wedding` | BUILT (B1, S107) |
| Kingsmoot | `kingsmoot-on-old-wyk` | DARK (only PRECEDES) |
| Purple Wedding | `death-of-joffrey-baratheon` | BUILT (S106) — 1 upstream CAUSES + 8 downstream causal |

### Existing Causal Chains Summary (WO5K-Adjacent)

```
BUILT (already wired):
─ death-of-robert-baratheon → arrest-of-eddard-stark → execution-of-eddard-stark (B3)
─ ned-confesses-to-treason → execution-of-eddard-stark (B3)
─ robb-weds-jeyne-westerling → red-wedding-conspiracy → red-wedding / robb-is-killed (B1)
─ battle-of-the-blackwater → [stannis-retreats-to-dragonstone / joffrey-sets-sansa-aside / tywin-named-savior] (S111)
─ catelyn-seizes-the-moment-and-arrests-tyrion → gregor-raids-the-riverlands (Bran arc S105)
─ catelyn-releases-jaime-lannister → karstark-murders-prisoners → execution-of-rickard-karstark (B1 upstream)
─ storming-of-the-crag ← (PRECEDES) robb-weds-jeyne-westerling [NOT CAUSES — this is the Q5 gap]

DARK (not wired):
─ death-of-robert-baratheon → succession fracture → all 4 rival kings
─ shadow-assassination-of-renly → Stannis absorbs Renly's host → marches on KL
─ capture-of-winterfell → sack-of-winterfell → (North destabilized)
─ theon-greyjoy-taken-as-ward → (ironborn invasion via Balon's opportunism)
─ joffrey-demands-coronation → (no CAUSES outgoing at all)
```

---

## 2. Trigger-Tree — Full WO5K Internal Map

Root: **Robert's death** (causes the contested succession).

```
death-of-robert-baratheon  [BUILT as node; wires to arrest-of-eddard only]
│
├─ [CAUSES, DARK] succession-fracture / joffrey-demands-coronation [EXISTS, DARK]
│   ├─ [CAUSES/MOTIVATES, DARK] stannis-declares-himself-rightful-heir [NO NODE]
│   │     └─ [CAUSES, DARK] stannis-sails-for-storms-end [NO NODE — but
│   │           siege-of-storms-end-299 EXISTS as battle node]
│   │           └─ [TRIGGERS, DARK] shadow-assassination-of-renly [EXISTS, DARK]
│   │                 ├─ [CAUSES, DARK] stannis-absorbs-renly-s-host [NO NODE]
│   │                 │     └─ [CAUSES, DARK] battle-of-the-blackwater [EXISTS]
│   │                 │           ├─ [CAUSES, BUILT] stannis-retreats-to-dragonstone
│   │                 │           ├─ [CAUSES, BUILT] joffrey-sets-sansa-aside...
│   │                 │           └─ [CAUSES, BUILT] tywin-named-savior-of-the-city
│   │                 └─ [CAUSES, DARK] tyrell-realignment-to-lannister [NO NODE]
│   │                       └─ feeds battle-of-the-blackwater (Tyrell host flanks Stannis)
│   │
│   └─ [CAUSES/MOTIVATES, DARK] renly-flees-to-highgarden-and-crowns-himself [NO NODE]
│         exists: wedding-of-renly-baratheon-and-margaery-tyrell [EXISTS, DARK]
│         └─ [CAUSES, DARK] renly-assembles-army / siege-of-storms-end [battle node exists]
│
├─ [CAUSES, BUILT] arrest-of-eddard-stark  ← already built (B3)
│   └─ [CAUSES, BUILT] execution-of-eddard-stark
│         └─ [CAUSES, DARK] robb-proclaimed-king-in-the-north [NO NODE — needs mint]
│               └─ [MOTIVATES → Robb, DARK] robb-campaigns-in-westerlands [battles exist, 0 causal]
│                     └─ [CAUSES, PARTIALLY] storming-of-the-crag [EXISTS, PRECEDES only]
│                           └─ [CAUSES, DARK → Q5] robb-weds-jeyne-westerling [EXISTS, has outgoing]
│                                 └─ [TRIGGERS, BUILT] red-wedding-conspiracy → red-wedding (B1)
│
└─ [CAUSES, DARK] balon-greyjoy-declares-himself-king [NO NODE]
      └─ [CAUSES, DARK] ironborn-invasion-of-the-north [NO NODE]
            ├─ [CAUSES, DARK] fall-of-moat-cailin [battle node exists?]
            ├─ [CAUSES, DARK] harrying-of-stony-shore [EXISTS, PRECEDES only]
            └─ [CAUSES, DARK] capture-of-winterfell [EXISTS, DARK]
                  └─ [PRECEDES, BUILT] sack-of-winterfell [EXISTS, DARK]
                        └─ [CAUSES, DARK → Q13] north-destabilized [no node needed;
                              point is: sack-of-winterfell MOTIVATES robb to return north
                              which is upstream of the Frey re-negotiation]
```

**Tywin's deliberate provocation (cross-cutting):**
```
catelyn-seizes-tyrion [EXISTS]
  --[CAUSES, BUILT]--> gregor-raids-the-riverlands [EXISTS, PARTIAL]
    [No CAUSES outgoing — gregor-raids is a dark terminus]
    The wiki makes clear: Tywin DECIDES to use Catelyn's arrest as pretext;
    gregor-raids-the-riverlands needs a CAUSES edge → escalation-in-the-riverlands / 
    full-scale-lannister-invasion; agency: MOTIVATES tywin first.
```

---

## 3. Juncture Scorecard

Scoring rubric (0–2 per axis, from `causal-arc-strategy-2026-06-18.md`):
- **Query-value** (Q): dip fails it = 2, plausible = 1, never asked = 0
- **Salience** (S): major chain = 2, minor = 1, trivia = 0
- **Cross-POV** (X): 3+ POVs = 2, 2 POVs = 1, 1 = 0
- **Causal load** (C): real consequence = 2, mixed = 1, pure sequence = 0
- **Beat-readiness** (B, cost): all/most exist = 2, some = 1, none = 0
- **Grounding** (G, Tier): in-saga POV = 2, mixed = 1, wiki-only = 0

**Total max = 12. Gate: build if ≥ 7/12 AND not (G=0, Q<2).**

---

### J1. Succession Fracture: `death-of-robert-baratheon` → contested accession → all 4 rivals declare

**Description:** Robert dies → Joffrey's bastardy exposed only to Ned → Ned's coup fails → contested throne triggers Stannis+Renly+Robb+Balon all declaring. This is the single node that currently has ONLY 1 outgoing CAUSES edge (`death-of-robert → arrest-of-eddard`). The broader "his death fractures succession" is DARK.

**Anti-signal check:** This IS real causal logic — "Robert dies with a bastard heir → legitimacy crisis → rival kings" is GRRM's explicit setup, not mere sequence. The contested succession directly *enables* all 4 rival kings. Joffrey-bastardy was the ticking bomb; Robert's death was the trigger. Real CAUSES.

**Agency-collapse check:** Between `death-of-robert` and "4 kings declare," several human decisions sit:
- Ned's decision NOT to take the children hostage (as Renly suggested)
- Ned's decision to warn Cersei instead of seizing Joffrey
- Stannis's decision to flee to Dragonstone (not fight)
- Renly's decision to go to Highgarden
These are 4 distinct agency beats, each of which needs MOTIVATES(event→actor) modeling, not a blunt multi-arrow. **This juncture needs disaggregation — you can't model it as one edge.**

**Scope:** 3–5 mints (robb-proclaimed-king-in-the-north, stannis-declares-himself-rightful-heir, renly-self-crowns, balon-declares-himself-king) + likely 6–8 causal edges + agency-collapse handling = LARGE.

**Upstream attach-point:** `death-of-robert-baratheon` (HIT, built with 3 incoming role edges). Clean attach.

**Terminus:** Should terminate at concrete declarations (`robb-proclaimed-king-in-the-north`, etc.) — NOT at `war-of-the-five-kings`. Hard-stop holds.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 0 | 2 | **10/12** |

**Verdict: HIGH VALUE but LARGE. Beat-readiness = 0 (4 mint targets, none exist). Disaggregate into per-king sub-junctures before building.**

---

### J2. Renly's Death → Stannis Absorbs Host → Blackwater (Blackwater UPSTREAM)

**Description:** `shadow-assassination-of-renly` exists but has 0 causal edges. Consequence: Renly's 80k-man host splits — Loras takes 1/5 back to Highgarden, rest defect to Stannis. Stannis now has the force to march on King's Landing. **This is the UPSTREAM gap for `battle-of-the-blackwater`** (currently 0 upstream, 3 downstream built S111).

**Anti-signal check:** The Renly shadow → Stannis army absorption → Blackwater is genuine CAUSES logic. Without Renly dying, Stannis never has the army to threaten KL. The "Stannis absorbs host" beat is the mediating event.

**Agency-collapse check:** After shadow kills Renly:
- The storm-lords and Reach lords choose to defect to Stannis (group decision)
- Loras CHOOSES to return to Highgarden (key agency beat — models Tyrell realignment catalyst)
- Stannis DECIDES to march on KL now that he has numbers
These three decisions need MOTIVATES modeling, not blunt CAUSES arrows. Need intermediate beats.

**Missing beats:**
1. "Stannis-absorbs-renly-s-host" or "storm-lords-defect-to-stannis" — NO NODE (needs mint)
2. "Tyrell-realignment-to-Lannister" / Littlefinger brokers the deal at Bitterbridge — NO NODE
3. `fighting-at-bitterbridge` EXISTS but 0 causal

**Upstream attach-point:** `shadow-assassination-of-renly` (HIT, exists). Clean.

**Terminus:** `battle-of-the-blackwater` (HIT, built). Clean — 3 downstream already wired.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 1 | 2 | **11/12** |

**Verdict: HIGHEST VALUE. Clean attach + clean terminus (blackwater already built downstream). 2–3 new beats. Medium scope. This completes the "partial → complete" for Blackwater (#7 in foreshadowing list).**

---

### J3. Robb Proclaimed King in the North (Execution → North Secedes → Coronation)

**Description:** `execution-of-eddard-stark` has 0 causal outgoing. The consequence — North secedes, northern lords proclaim Robb King in the North — is DARK. This is a direct downstream consequence of the B3 arc already built (S108). Adding 1 node + 1–2 CAUSES edges extends the already-built chain.

**Anti-signal check:** "Ned dies → Robb is proclaimed king" is GRRM's explicit narrative. The Northern lords NAME Robb king *because* Ned was killed. Real CAUSES.

**Agency-collapse check:** The lords' collective decision to proclaim Robb is a group political act. Modeling this cleanly: `execution-of-eddard-stark MOTIVATES northern-lords` + `robb-proclaimed-king-in-the-north AGENT_IN [northern lords]`. The CAUSES arrow from ned-exec → robb-proclaimed is valid IF we also add the MOTIVATES(ned-exec → robb-stark) edge (Robb's grief + duty drives him to accept the crown). This is manageable — not a deep agency-collapse, just a 2-edge pattern.

**Missing beats:**
1. `robb-proclaimed-king-in-the-north` — **NO NODE** (needs mint)
   - Alternate slug check: resolver returns MISS for all natural phrases
   - Slug to mint: `robb-proclaimed-king-in-the-north`

**Upstream attach-point:** `execution-of-eddard-stark` (HIT, confirmed). Clean. B3 arc terminates here; this extends it one hop.

**Terminus:** `robb-proclaimed-king-in-the-north` (new node). Concrete. Clean.

**Further downstream (deferred):** `robb-campaigns-in-westerlands`, `storming-of-the-crag`, then Q5 already queued.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 1 | 2 | **11/12** |

**Verdict: VERY HIGH VALUE, LOW COST. 1 new mint + 2 edges. Extends the already-built B3 chain (ned-exec) one hop downstream. Cheap entry into the North thread.**

---

### J4. Balon's Opportunism → Ironborn Invasion → Capture of Winterfell

**Description:** Balon sees the power vacuum (Robb's army in the south, North stripped bare), dismisses Robb's alliance offer, declares himself King of the Isles and the North, sends the invasion fleet. This leads to the ironborn capture of Moat Cailin, Deepwood Motte, Stony Shore raids, and Theon's unauthorized seizure of Winterfell. The B2 arc (greyjoy-rebellion → theon-ward, S107) terminates before this — the invasion is dark.

**Anti-signal check:** Balon's invasion decision is CAUSED by the power vacuum + Robb's weakened position (the Ward → no hostage → free to rebel). This is genuine CAUSES + MOTIVATES, not sequence.

**Agency-collapse check:** Very high agency-collapse risk. The chain is:
- Power vacuum MOTIVATES balon-greyjoy
- Theon's ward-ending (greyjoy-ward being returned as envoy) ENABLES balon to invade
- Balon's declaration is a decision node
- Theon's unauthorized seizure of Winterfell (vs his orders to raid the Stony Shore) introduces a SECOND agency break mid-chain
  
**Two-level agency:** Balon decides; Theon sub-decides against orders. Modeling this cleanly requires MOTIVATES edges and careful scoping. A blunt "Balon invades → capture-of-winterfell" would be agency-collapse at both levels.

**Missing beats:**
1. "Balon-declares-himself-king-of-isles-and-the-north" — NO NODE
2. "Ironborn-invasion-of-the-north" (or "Balon-dispatches-three-invasion-forces") — NO NODE
3. "Fall-of-moat-cailin" — check: `ls events/ | grep moat` — need to verify
4. `capture-of-winterfell` EXISTS (PART_OF + PRECEDES, 0 causal)
5. `sack-of-winterfell` EXISTS (DARK, 0 causal)

**Upstream attach-point:** `theon-greyjoy-taken-as-ward` (HIT, built as B2 terminus with 1 upstream CAUSES from greyjoy-rebellion). Attach: B2 ends at ward; the ward ends when Robb sends Theon as envoy → Balon dismisses him → invades. Need 1–2 intermediate beats between the ward and the invasion.

**Terminus:** `capture-of-winterfell` or `sack-of-winterfell`. Both concrete nodes. Clean hard-stop.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 2 | 2 | 1 | 2 | **10/12** |

**Verdict: HIGH VALUE, MEDIUM SCOPE. 3–4 new beats + 4–6 edges. Two-level agency-collapse makes this more complex than J3. Good candidate after J2 and J3.**

---

### J5. Gregor's Riverlands Chevauchée → Full-Scale Lannister Invasion (Tywin's Provocation)

**Description:** `gregor-raids-the-riverlands` EXISTS with 1 incoming CAUSES from Catelyn's arrest (Bran arc). BUT: Tywin's INTENTIONAL decision to use Catelyn's arrest as pretext for the invasion — the deliberate provocation (he WANTS to lure Ned into the Riverlands where he can be captured, the wiki says this explicitly) — is NOT modeled. The chevauchée is a terminus; it needs outgoing CAUSES to the full invasion escalation.

**Anti-signal check:** This is borderline. The fact that Gregor raids → Tywin invades the Riverlands IS genuine causal consequence. But PRECEDES between battles in the Riverlands campaign (Golden Tooth → Mummer's Ford → Riverrun) is already handled by the `PRECEDES` chain. The causal VALUE here is specifically: Tywin's *deliberate* strategy decision — using Catelyn's provocation as pretext — is an agency beat worth modeling. The battle-sequence is PRECEDES; the *decision-to-invade* is CAUSES.

**Agency-collapse check:** High. The chain needs MOTIVATES(catelyn-arrest → tywin-lannister) + COMMANDS_IN(tywin → gregor-raids) already partially wired. The gap is the intermediate decision node: `tywin-decides-to-invade-the-riverlands` or similar. This is the missing beat.

**Missing beats:**
1. `tywin-musters-hosts-at-casterly-rock` or similar — NO NODE (but `battle-in-the-hills-below-the-golden-tooth` EXISTS as a battle)
2. A Tywin-decision beat node for the invasion authorization

**Upstream attach-point:** `gregor-raids-the-riverlands` (HIT, has 1 CAUSES incoming). OR: `catelyn-seizes-the-moment-and-arrests-tyrion` (already built as Bran-arc terminus). Double attach possible.

**Terminus:** `battle-in-the-hills-below-the-golden-tooth` or `battle-in-the-whispering-wood` — concrete. Or model just the "invasion decision" → "siege of Riverrun."

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 1 | 2 | 2 | 1 | 2 | **9/12** |

**Verdict: MEDIUM VALUE. The key sub-beat (Tywin's invasion decision as a strategic response to Catelyn's arrest) has real causal value but is largely covered by existing PRECEDES chains. Best treated as a 1–2 edge enrichment of the existing Bran-arc terminus rather than a full arc.**

---

### J6. Robb's Coronation → Military Campaign → Westerlands Raids (Battle Sequence)

**Description:** After Ned's execution and Robb's proclamation, Robb launches the westerlands campaign — Battle of Oxcross, Ashemark, Crag. This is a sequence of battles with PRECEDES links. The question is whether the battle-to-battle links carry CAUSES or just sequence.

**Anti-signal check:** SEQUENCE MASQUERADING AS CAUSE. Battle of Oxcross → Ashemark → Storming of the Crag is pure military sequence. Each battle does not *cause* the next in any meaningful consequence sense — Robb is conducting a campaign. PRECEDES already covers this. **This is the anti-signal #1 trap.** The only real CAUSE in this chain is: Storming of the Crag → (Robb wounded + false Bran/Rickon news) → Robb weds Jeyne (Q5, already queued). The battle sequence before that is SKIP.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 0 | 1 | 1 | 0 | 2 | 2 | **6/12** |

**Verdict: SKIP — sequence-only. PRECEDES already covers battle ordering. The ONE real causal juncture within this stretch (Storming-of-the-Crag → Robb-weds-Jeyne, Q5) is already queued separately.**

---

### J7. Catelyn Releases Jaime → Karstark Murders → Robb Isolated (Already Partially Built)

**Description:** This chain is PARTIALLY BUILT — `catelyn-releases-jaime-lannister → karstark-murders-prisoners → execution-of-rickard-karstark` is wired (3 edges). BUT: the downstream of Karstark's execution is DARK — Robb losing half his cavalry (the Karstark forces abandon him) directly causes his need to renew the Frey alliance, which sets up the Red Wedding.

**Anti-signal check:** `execution-of-rickard-karstark` → Karstark forces abandon Robb → Robb needs new Frey deal is genuine CAUSES. Not just sequence.

**Agency-collapse check:** After Karstark execution, the Karstark cavalry CHOOSE to abandon Robb. This needs `MOTIVATES(execution-of-rickard-karstark → rickard-karstark [collective forces])` + a CAUSES to "Robb-seeks-frey-reconciliation" or similar.

**Missing beats:**
1. `karstark-forces-abandon-robb` — NO NODE (may be optional if we use MOTIVATES directly)
2. `robb-seeks-frey-reconciliation` or `frey-reconciliation-required` — check: `robb-weds-jeyne` TRIGGERS the conspiracy, but the FREY re-negotiation beat doesn't exist as a node. The Red-Wedding-conspiracy ALREADY has robb-weds-jeyne as trigger; this extension would add upstream context: Karstark-exec → abandonment → needs Frey → Jeyne wedding (which broke Frey betrothal) → RW conspiracy.

**Note:** This juncture extends the already-built B1 upstream chain (catelyn-releases-jaime → karstark-murders → karstark-exec → [DARK] → robb-weds-jeyne → red-wedding-conspiracy). It JOINS the existing B1 chain. Only 1–2 edges needed.

**Upstream attach-point:** `execution-of-rickard-karstark` (HIT, confirmed). Clean.

**Terminus:** `robb-weds-jeyne-westerling` (HIT, existing node with 1 TRIGGERS outgoing). Clean.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 1 | 2 | 1 | 2 | **9/12** |

**Verdict: MEDIUM-HIGH VALUE. Closes the gap between two already-built segments of the B1 chain. 1–2 new edges, maybe 1 mint. Cheap. Best built after Q5 (storming-of-the-Crag → robb-weds-jeyne) since it slots between them.**

---

### J8. Balon's Death → Kingsmoot → Euron Wins (Iron Islands Succession)

**Description:** Balon falls from a bridge at Pyke during the storm. `kingsmoot-on-old-wyk` EXISTS with only 1 PRECEDES incoming (from `battle-on-the-green-fork`, which is wrong-context — chronology backbone). Euron wins the Kingsmoot (AFFC event, dark).

**Anti-signal check:** Is "Balon dies → Kingsmoot happens" CAUSES or just sequence? The Kingsmoot PRECEDES the Drowned God's decision process. But Balon's death directly *triggers* the Kingsmoot — that's TRIGGERS (immediate specific spark). And Euron's victory CAUSES the invasion of the Reach, Euron's campaigns. These are real causal edges.

**Agency-collapse check:** Low — the Kingsmoot is itself the mechanism for resolving the succession. No hidden agent; the group assembly is the event.

**Missing beats:**
- `death-of-balon-greyjoy` — check: exists? Need to verify. Alias lookup for "death of Balon Greyjoy" returns MISS.
  
**Grounding:** AFFC Drowned Man + Asha chapters — in-saga, Tier-1 quotes available.

**Upstream attach-point:** None built in WO5K tree (Balon's death is standalone). Would attach at: sack-of-winterfell CAUSES north-destabilized MOTIVATES robb-returns-north (DARK). The Balon arc would plug into after-capture-of-winterfell context, OR stand as its own isolated chain.

**Terminus:** `kingsmoot-on-old-wyk` (HIT, exists). Then optionally: Euron's victory CAUSES euron-plans-dragon-conquest (AFFC). 

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 1 | 2 | 1 | 2 | **9/12** |

**Verdict: MEDIUM VALUE. Satisfying to wire (it's a clean TRIGGERS chain) but no existing upstream attach-point in the causal graph. DEFER until after Balon's invasion arc (J4) is built, so there's an attach-point. Kingsmoot → Euron victory is its own mini-arc, not part of the WO5K spine.**

---

### J9. Tyrell Realignment: Renly Dies → Loras Returns → Littlefinger Brokers → Tyrells Join Lannisters

**Description:** After `shadow-assassination-of-renly`, Loras leads ~16k men back toward Highgarden. Littlefinger rides to Bitterbridge and brokers the Tyrell deal for Joffrey. Tyrells bring their host to join Tywin's force for the Blackwater. This is the mechanism that saves King's Landing and is narratively one of GRRM's central "turns" of ACOK.

**Anti-signal check:** Renly's death CAUSES the Tyrell realignment. The Tyrell realignment (Littlefinger's deal) CAUSES the Lannister-Tyrell combined force at the Blackwater. The Blackwater outcome is then already wired. Real CAUSES chain.

**Agency-collapse check:** High. Between shadow-kills-renly and tyrells-join-lannisters:
- Loras DECIDES to leave for Highgarden (grief + not-defect-to-Stannis choice)
- Littlefinger DECIDES to broker the deal (at Cersei/Tyrion's direction — but whose MOTIVATES?)
- Mace Tyrell DECIDES to accept the Joffrey betrothal
Multiple human decisions. Needs: MOTIVATES(shadow-assassination → loras-tyrell) + a decision beat for the Bitterbridge negotiation.

**Missing beats:**
1. `loras-leads-tyrell-forces-from-bitterbridge` or `tyrell-forces-disengage-from-stannis` — NO NODE
2. `littlefinger-brokers-tyrell-lannister-alliance` — NO NODE
3. `tyrells-march-to-join-tywin` or similar — NO NODE (fighting-at-bitterbridge EXISTS but 0 causal)

**Upstream attach-point:** `shadow-assassination-of-renly` (HIT, exists, DARK). Perfect attach.

**Terminus:** `battle-of-the-blackwater` (HIT, built, has 3 downstream consequences). Perfect terminus. This DIRECTLY completes the Blackwater upstream gap.

**Note:** This is almost a subset of J2 (Renly→Stannis→Blackwater). J2 focuses on Stannis's side (absorbing the remaining host, marching on KL). J9 focuses on the Tyrell side (Lannister-Tyrell alliance enabling the flank). Together J2+J9 form the complete Blackwater UPSTREAM arc.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 0 | 2 | **10/12** |

**Verdict: VERY HIGH VALUE but 3+ new beats. Best built as part of J2 (they share the upstream attach-point and the downstream terminus). Scope together = J2+J9 "Blackwater upstream complete arc."**

---

## 4. Sequence-Only Traps (SKIP/DEFER with reasons)

| Juncture | Why Skip/Defer |
|----------|----------------|
| **Battle sequence: Whispering Wood → Camps → (north campaign)** | Anti-signal #1: pure military sequence. PRECEDES already covers. No real consequence between battles, only cumulative strategic advantage. |
| **Robb's westerlands campaign battles** | Same — sequence. The ONE causal juncture (Crag → Jeyne) is already queued (Q5). |
| **Stannis's Narrow Sea campaign (pre-Renly)** | Stannis retreating to Dragonstone after Robert's death is DARK but is a *preparation* beat, not a causal chain. The causal link doesn't become active until the shadow-kill (J2). DEFER: build J2 first. |
| **Kingsmoot → Euron's Reach campaign** | Good causal chain but NO upstream attach-point in current graph. DEFER until after J4 (Balon invasion) is built. |
| **Robb's political isolation (multiple causes)** | "Robb wins battles, loses the war" is a PATTERN, not a single causal chain. The individual causes (Karstark, Frey, Ironborn) each deserve their own edge but can't be collapsed into one "political isolation" node. Build as separate J3/J7 extensions. |
| **WO5K war-hub as terminus** | HARD-STOP per policy. Never chain CAUSES into `war-of-the-five-kings` terminus. All arcs terminate at concrete sub-event nodes. |

---

## 5. Ranked Build Order

**Priority 1 (build first):** Cheapest real cause, best beat-readiness, clean attach + terminus, extends already-built chain.

### Rank 1 — J3: Robb Proclaimed King in the North
**1 mint, 2 edges. Extends B3 (ned-exec) one hop downstream.**
- Mint: `robb-proclaimed-king-in-the-north` (event.ceremony, AGOT Catelyn XI)
- Wire: `execution-of-eddard-stark --[CAUSES]--> robb-proclaimed-king-in-the-north`
- Wire: `execution-of-eddard-stark --[MOTIVATES]--> robb-stark` (his grief → accepting the crown)
- Scope: ~1 hour, minimal mint
- Attach-point: `execution-of-eddard-stark` (verified HIT)
- Terminus: `robb-proclaimed-king-in-the-north` (new, concrete)
- Agency: Low risk — lords' collective proclamation is the event; Robb's MOTIVATES edge handles his agency

### Rank 2 — Q5 (already queued): Storming of the Crag → Robb Weds Jeyne
**1–2 edges, existing nodes mostly ready.**
- Wire: `storming-of-the-crag --[CAUSES]--> robb-weds-jeyne-westerling`
- Intermediate beat: possibly `robb-receives-false-news-of-brans-death` (comfort → dishonoring Frey betrothal); check existence first
- Scope: likely 1 edge + maybe 1 mint
- Attach-point: `storming-of-the-crag` (verified HIT); upstream of `robb-weds-jeyne` (HIT)
- Terminus: `robb-weds-jeyne-westerling` (HIT, already has 1 TRIGGERS outgoing)
- **Note:** Dip confirm first per protocol before building (continue-prompt Step C)

### Rank 3 — J2+J9: Blackwater Upstream (Renly Death → Stannis Marches + Tyrell Realignment → Blackwater)
**3–4 mints, 5–7 edges. Completes the Blackwater upstream (foreshadowing event #7 PARTIAL → COMPLETE).**
- Mint candidates: `stannis-absorbs-renly-s-host`, `littlefinger-brokers-tyrell-lannister-alliance`, possibly `tyrell-forces-march-to-join-tywin`
- Wire: `shadow-assassination-of-renly --[CAUSES]--> stannis-absorbs-renly-s-host`
- Wire: agency beats (MOTIVATES edges for Stannis's decision, Loras's decision, Mace's deal)
- Wire: `stannis-absorbs-renly-s-host --[CAUSES]--> battle-of-the-blackwater` (upstream complete)
- Wire: `littlefinger-brokers-tyrell-lannister-alliance --[CAUSES]--> battle-of-the-blackwater` (flanking army)
- Scope: half-session, ~3–4 mints
- Attach-point: `shadow-assassination-of-renly` (verified HIT, DARK, clean)
- Terminus: `battle-of-the-blackwater` (verified HIT, already has 3 downstream consequences)
- **This is the single highest salience gap: Blackwater UPSTREAM has been DARK since S111 built the downstream. Completing this gives `--causal-chain shadow-assassination-of-renly` a fully walkable 5–6 hop chain through the Blackwater.**

### Rank 4 — J7: Karstark Execution → Robb Isolation (closes B1 gap)
**1–2 edges, possibly 1 mint. Closes the gap between two already-built B1 segments.**
- Check: `execution-of-rickard-karstark` → `robb-weds-jeyne-westerling` — what sits between?
- The mediating beat: Robb losing Karstark cavalry → needing to reconcile with Freys. Possible 1-edge: `execution-of-rickard-karstark --[CAUSES]--> robb-weds-jeyne-westerling` with MOTIVATES(karstark-exec → robb-stark) agency modeling.
- Scope: 1–2 edges, possibly 0 new mints
- Attach-point: `execution-of-rickard-karstark` (HIT, confirmed)
- Terminus: `robb-weds-jeyne-westerling` (HIT, already has 1 TRIGGERS outgoing)
- Build this AFTER Q5 to keep the focus on the same B1 extension territory

### Rank 5 — J4: Balon's Invasion → Capture of Winterfell (B2 Downstream Extension)
**3–4 mints, 4–6 edges. Extends B2 (greyjoy-ward) through the invasion chain.**
- Already queued as Q13 (sack-of-winterfell extension) in the continue-prompt
- Mint: `balon-declares-himself-king-of-isles-and-north`, `ironborn-invasion-of-the-north`, possibly `theon-receives-raid-orders`
- Two-level agency-collapse: Balon's decision + Theon's unauthorized seizure
- Scope: medium-large; build after J2+J9 to preserve momentum on simpler arcs

---

## 6. Cross-Book Attach-Points Map

For each dark juncture, the node it should root at (upstream) and the node it terminates at (downstream). These are the "stitching points" that integrate WO5K sub-arcs into the broader graph.

| Arc | Upstream Attach | Downstream Terminus | Status of attach-point |
|-----|----------------|---------------------|----------------------|
| J2: Renly→Stannis→Blackwater | `shadow-assassination-of-renly` | `battle-of-the-blackwater` | Both HIT |
| J3: Ned-exec → Robb proclaimed | `execution-of-eddard-stark` | `robb-proclaimed-king-in-the-north` (new) | Source HIT |
| Q5: Crag → Robb-Jeyne | `storming-of-the-crag` | `robb-weds-jeyne-westerling` | Both HIT |
| J7: Karstark-exec → Robb-Jeyne | `execution-of-rickard-karstark` | `robb-weds-jeyne-westerling` | Both HIT |
| J4: Balon invasion | `theon-greyjoy-taken-as-ward` (B2 terminus) | `capture-of-winterfell` / `sack-of-winterfell` | Ward HIT; Winterfell HIT |
| J9: Tyrell realignment | `shadow-assassination-of-renly` | `battle-of-the-blackwater` | Both HIT |
| J1: Succession fracture | `death-of-robert-baratheon` | Per-king declaration nodes (new) | Source HIT |
| J8: Kingsmoot | (needs J4 built first) | `kingsmoot-on-old-wyk` | Terminus HIT |

---

## 7. Nodes to Mint (Summary)

Required for ranked top-5 arcs:

| Node to Mint | Slug | Type | Source | For Juncture |
|---|---|---|---|---|
| Robb proclaimed King in the North | `robb-proclaimed-king-in-the-north` | event.ceremony | AGOT Catelyn XI | J3 |
| Stannis absorbs Renly's host | `stannis-absorbs-renly-s-host` | event.incident | ACOK multiple POVs | J2 |
| Littlefinger brokers Tyrell-Lannister alliance | `littlefinger-brokers-tyrell-lannister-alliance` | event.conspiracy | ACOK Tyrion X / ASOS | J9 |
| Tyrell forces march to join Tywin | `tyrell-forces-march-to-join-tywin` | event.incident | ACOK (optional, merge w/bitterbridge?) | J9 |
| Balon declares himself King | `balon-declares-himself-king` | event.ceremony | ACOK Theon II | J4 |
| Ironborn invasion of the North | `ironborn-invasion-of-the-north` | event.battle | ACOK Theon III | J4 |

Dedup-check every candidate via `event_alias_resolver.py --lookup` + manual `grep graph/nodes/events/` before minting. The ~200 verbose-slug Plate-3 beats are the primary collision surface.

---

## 8. Harvest Queue Additions

*(Collected incidentally during WO5K wiki + graph investigation — POINT, don't extract)*

| status | kind | book | ref | note | session |
|--------|------|------|-----|------|---------|
| open | quote | acok | wiki:War_of_Five_Kings / acok-theon-02 | Balon: "I will not be given a crown. I will pay the iron price." — exact dismissal of Robb's alliance; load-bearing for balon-declares-himself-king event node; no node yet | 2026-06-20 wo5k-decomp |
| open | quote | acok | wiki:War_of_Five_Kings / acok-catelyn-04 | After shadow kills Renly: "With Renly dead, the majority of the host that had accompanied him swears allegiance to Stannis" — wiki compression of a complex event; in-saga quote needed for stannis-absorbs-renly-s-host | 2026-06-20 wo5k-decomp |
| open | relationship | acok | wiki:War_of_Five_Kings | Renly's reason for going to Highgarden: Renly proposes seizing Cersei's children as hostages to Ned; Ned refuses; Renly flees — the "Ned's refusal" is the catalyst that allows Renly to self-crown; relevant for succession-fracture arc | 2026-06-20 wo5k-decomp |
| open | foreshadowing | acok | wiki:War_of_Five_Kings | Garlan Tyrell wears Renly's armor at the Blackwater — "many to mistake him for Renly's ghost" — strong Chekhov's-mirror moment; no foreshadowing edge exists; relevant for Renly-Tyrell relationship | 2026-06-20 wo5k-decomp |
| open | quote | agot | wiki:War_of_Five_Kings / agot-eddard-14 | After Robert's death Renly proposes seizing Cersei's children; Ned refuses: "Robert's true heir is Stannis." — exact framing of Ned's fatal loyalty-over-pragmatism; no quote on ned-discovers-the-truth-of-joffrey-s-parentage node yet (MOTIVATES edges have context, but main node lacks ## Quotes) | 2026-06-20 wo5k-decomp |
| open | other | affc | wiki:War_of_Five_Kings | Archmaester Benedict says "there are never technically five kings at once" because Renly is slain before Balon crowns himself — relevant for the naming controversy of the war; trivia but flavor note | 2026-06-20 wo5k-decomp |
