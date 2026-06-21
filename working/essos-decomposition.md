# ESSOS Decomposition: Trigger-Tree, Scorecard, Build Rank

> **Created:** 2026-06-21 (S119 ESSOS decomposition dip)
> **Purpose:** Map the Essos internal causal trigger-tree (Daenerys thread + Westeros↔Essos bridges); mark what's built vs dark; rank buildable arcs.
> **Read-only:** no graph writes. Local cache only.

---

## 1. Current Causal State — Verified Against Live Graph

All states verified with `--neighbors`, alias resolver `--lookup`, and direct `edges.jsonl` grep.

### Drogo / Dragon-Birth Cluster (AGOT)

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Drogo's westward vow | NO NODE | MISS | 0 edges in or out |
| Blood magic ritual (Mirri performs it) | NO NODE | MISS | 0 edges |
| Death of Khal Drogo | NO NODE | MISS | 0 edges |
| Dragon hatching on pyre (birth of Drogon/Rhaegal/Viserion) | NO NODE | MISS | 0 edges |
| Wine merchant attempts to poison Dany | `the-wine-merchant-attempts-to-poison-dany` | HIT | 3 role edges (COMMANDS_IN robert-baratheon, AGENT_IN wineseller, VICTIM_IN daenerys-targaryen); **0 causal edges out** |
| Bloodriders attack Mirri | `bloodriders-attack-mirri` | HIT | 3 role edges; **0 causal in or out** |

### Robert's Assassination Order Cluster

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Robert orders Daenerys assassination | NO NODE | MISS | 0 edges (worklog S112 "STILL OPEN: mint `robert-orders-daenerys-assassination`") |
| Ned cancels assassination | `ned-orders-daenerys-s-assassination-cancelled` | HIT | 3 role edges (COMMANDS_IN eddard-stark, AGENT_IN varys, VICTIM_IN daenerys-targaryen); **0 causal edges out** — the wine merchant has no upstream causal attach |

**Gap confirmed:** `robert-orders-daenerys-assassination` (NO NODE) is the bridge between Robert's decision and the wine merchant; `ned-orders-daenerys-s-assassination-cancelled` has 0 outgoing. The chain `robert's-order → wine-merchant-attempt → drogo-westward-vow` is entirely DARK causally.

### Illyrio/Varys Conspiracy

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Illyrio/Varys conspire (AGOT dungeon scene, Arya ch.3 witness) | NO NODE | MISS | 0 edges |

Note: Arya witnesses the Varys/Illyrio conversation (agot-arya-03:73–97); she is later named Arya's POV witness to its consequences in Ned's arc. The conspiracy is unmodeled as an event node; only character nodes for varys and illyrio exist.

### Slaver's Bay Campaign

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Fall of Astapor | `fall-of-astapor` | HIT | 1 edge: PART_OF targaryen-campaign-in-slavers-bay; **0 causal edges in or out** |
| Siege of Astapor (later Yunkai'i siege of Cleon's Astapor) | `siege-of-astapor` | HIT | PART_OF campaign; PRECEDES ← battle-on-the-green-fork (wrong-context chronology spine); **0 causal** |
| Battle of Yunkai | `battle-of-yunkai` | HIT | **COMPLETELY DARK: 0 edges of any type** |
| Battle near Yunkai | `battle-near-yunkai` | HIT | PART_OF campaign; PRECEDES → red-wedding (spurious chronology hop); SUB_BEAT_OF ← night-attack-planned; **0 causal** |
| Siege of Meereen | `siege-of-meereen` | HIT | PART_OF campaign; **0 causal in or out** |
| Second Siege of Meereen | `second-siege-of-meereen` | HIT | **COMPLETELY DARK: 0 edges of any type** |
| Targaryen campaign (container hub) | `targaryen-campaign-in-slavers-bay` | HIT | 7 PART_OF incoming; **0 outgoing** — dark terminus |
| Sons of the Harpy kill twenty-nine | `sons-of-the-harpy-kill-twenty-nine` | HIT | 4 role edges; LOCATED_AT meereen; **0 causal in or out** |

**Key finding:** The Slaver's Bay campaign hub and all its sub-events are structurally related only via PART_OF links. No causal chain exists anywhere in this cluster. The entire ASOS–ADWD Daenerys spine is causally DARK.

### Meereen Occupation / Political Stalemate

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Sons of the Harpy insurgency (as an ongoing condition) | NO NODE (only `sons-of-the-harpy-kill-twenty-nine` one incident) | MISS | — |
| Dany's political marriage to Hizdahr | `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` | HIT | 1 PRECEDES outgoing → landing-of-the-golden-company (spurious); 1 PRECEDES incoming; 1 SUB_BEAT_OF; **0 causal** |
| Hizdahr orders Drogon killed | `hizdahr-orders-drogon-killed` | HIT | 3 role edges; **0 causal out** |
| Drogon kills more attackers | `drogon-kills-more-attackers` | HIT | 3 role edges; **0 causal out** |
| Daario offers to kill Jorah | `daario-offers-to-kill-jorah` | HIT | 3 role edges; **0 causal out** |

### ADWD Endpoint

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Quentyn orders the attack | `quentyn-orders-the-attack` | HIT | 5 role edges; **0 causal in or out** |
| Quentyn burned to death by dragon | NO NODE | MISS | 0 edges |
| Drogon's flight from Daznak's Pit | NO NODE | MISS | 0 edges |
| Dany lost on Dothraki sea | NO NODE | MISS | 0 edges |

### Bridges (Westeros↔Essos)

| Node | Slug | Exists? | Causal State |
|------|------|---------|--------------|
| Euron commissions Victarion to fetch Daenerys | `euron-commissions-victarion-to-fetch-daenerys` | HIT | 3 edges: CAUSES ← taking-of-the-shields (upstream BUILT S116), AGENT_IN victarion, COMMANDS_IN euron; **0 causal out** — downstream DARK |
| Doran's "Fire and blood" pact reveal | NO NODE | MISS | 0 edges (2 harvest rows parked pending this build) |
| Slaver galley Willing Maiden captured | `slaver-galley-willing-maiden-captured` | HIT | LOCATED_AT + 3 role edges; **0 causal out** |

---

## 2. Trigger-Tree — Full Essos Internal Causal Map

Root: **Drogo's death** (enables the pyre → dragon hatching, prime mover of the entire arc).

```
ESSOS SPINE ROOT (AGOT):
─────────────────────────────────────────────────────────────────────
robert-orders-daenerys-assassination  [NO NODE — needs mint]
  --[CAUSES, DARK]--> the-wine-merchant-attempts-to-poison-dany  [EXISTS, 0 causal out]
                            |
                   [CAUSES/MOTIVATES, DARK]
                            ↓
                drogo-westward-vow  [NO NODE — needs mint]
                            |
                   [MOTIVATES drogo-stark / ENABLES, DARK]
                            ↓
        ┌── mirri-blood-magic-ritual  [NO NODE — needs mint]
        │         (AGOT Dany VIII: Drogo wounded; Mirri offers healing)
        │
        └── death-of-khal-drogo  [NO NODE — needs mint]
                   |
            [CAUSES/TRIGGERS, DARK]
                   ↓
        dragon-hatching-on-drogo-pyre  [NO NODE — needs mint]
                   ← ENABLES / TRIGGERS: bloodriders-attack-mirri [EXISTS, 0 causal]
                     (Mirri's betrayal is the mechanism that kills Rhaego,
                     leaves Drogo vegetative → Dany smothers Drogo → pyre)
                   |
                [CAUSES, DARK]
                   ↓
        dany-acquires-unsullied-at-astapor  ← fall-of-astapor [EXISTS, 0 causal]
                   |
               [CAUSES, DARK]
                   ↓
        dany-marches-to-yunkai  ← battle-of-yunkai [EXISTS, DARK 0 all]
                   |             battle-near-yunkai [EXISTS, 0 causal]
               [CAUSES, DARK]
                   ↓
        siege-of-meereen  [EXISTS, 0 causal]
                   |
        [CAUSES, DARK — occupation triggers insurgency]
                   ↓
        sons-of-the-harpy-insurgency  [NO NODE as ongoing condition]
              ← sons-of-the-harpy-kill-twenty-nine [EXISTS, 0 causal]
                   |
        [MOTIVATES dany, DARK — stalemate drives political marriage]
                   ↓
        wedding-of-hizdahr-zo-loraq-and-daenerys  [EXISTS, 0 causal]
                   |
        [CAUSES, DARK — opens fighting pits as peace concession]
                   ↓
        daznak-pit-incident  [cluster of existing nodes: DARK]
            ← hizdahr-orders-drogon-killed [EXISTS, 0 causal]
            ← drogon-kills-more-attackers [EXISTS, 0 causal]
            ← unnamed-spearman-attacks-drogon [EXISTS, 0 causal]
                   |
        [TRIGGERS, DARK]
                   ↓
        drogon-flees-daznak-with-dany  [NO NODE — needs mint]
                   |
        [CAUSES, DARK]
                   ↓
        dany-lost-on-dothraki-sea  [NO NODE — needs mint]


CROSS-CHAIN: Quentyn Thread (ADWD)
─────────────────────────────────────────────────────────────────────
doran-reveals-fire-and-blood-pact  [NO NODE]
  [CAUSES, DARK] → quentyn-martell-travels-to-meereen  [NO NODE]
       ↓
  arrives + presents pact (dark) → dany refuses his suit (dark)
       ↓
  quentyn-orders-the-attack  [EXISTS, 0 causal]
       ↓  [TRIGGERS, DARK]
  death-of-quentyn-martell  [NO NODE — needs mint]


BRIDGES (Westeros↔Essos):
─────────────────────────────────────────────────────────────────────
death-of-balon-greyjoy [BUILT S116 as standalone]
  → euron-seizes-seastone-chair [BUILT]
    → kingsmoot-on-old-wyk [BUILT]
      → taking-of-the-shields [BUILT]
        → euron-commissions-victarion-to-fetch-daenerys [BUILT, 0 causal out]
             (attaches to the Essos arc via Victarion's journey; downstream DARK)

robert-orders-daenerys-assassination  [NO NODE — needs mint]
  --[CAUSES, BUILT via COMMANDS_IN]--> wine-merchant-attempt
  --[CAUSES, DARK]--> ned-orders-daenerys-s-assassination-cancelled [EXISTS, 0 causal out]

doran-reveals-fire-and-blood-pact  [NO NODE]
  (affc-the-princess-in-the-tower-01:325 "fire and blood" whisper)
  attaches upstream from: arrest-of-the-sand-snakes [S117 BUILT arc]
  (gregor-confesses CAUSES arrest MOTIVATES arianne → queenmaker → maiming → reveal)
```

**Built summary:**
```
BUILT (live wired edges):
─ taking-of-the-shields → euron-commissions-victarion-to-fetch-daenerys (1 CAUSES)
─ All S116 Kingsmoot→Euron spine (standalone root, separate from Essos spine)

DARK (causally unwired):
─ ENTIRE Daenerys Essos spine (AGOT through ADWD) — no causal edges anywhere
─ Both Westeros→Essos bridges except the Euron-Victarion commission itself
─ Quentyn thread entirely dark (0 causal edges)
```

---

## 3. Juncture Scorecard

Scoring rubric (0–2 per axis, max 12; gate: build if ≥7 AND not (G=0, Q<2)):
- **Q (Query-value):** dip fails without it = 2, plausible = 1, never asked = 0
- **S (Salience):** major chain = 2, minor = 1, trivia = 0
- **X (Cross-POV):** 3+ POVs = 2, 2 = 1, 1 = 0
- **C (Causal load):** real consequence = 2, mixed = 1, sequence = 0
- **B (Beat-readiness):** all/most nodes exist = 2, some = 1, none = 0
- **G (Grounding):** in-saga POV = 2, mixed = 1, wiki-only = 0

---

### E1. Dragon Birth Arc: Drogo's Wound → Mirri Ritual → Drogo's Death → Dragon Hatching

**Description:** The prime mover of the entire Essos arc. Drogo is wounded in the Lhazareen raid (agot-daenerys-07); Mirri Maz Duur offers blood magic healing; Drogo's wound festers; Mirri's ritual kills Rhaego in the womb and leaves Drogo a husk; Dany smothers Drogo; pyre → dragons hatch. This is the causal nucleus of everything that follows — without live dragons, there is no Slaver's Bay arc, no Meereen, no Victarion quest.

**Anti-signal check:** "Drogo dies → dragons hatch" is explicit in-text causation: Mirri's magic exchanges life for life; the pyre channels that magic; GRRM's narration is unambiguous. The textual causation is as direct as any in the series. "Only death can pay for life" (agot-daenerys-09:127). Real CAUSES, not sequence.

**Agency-collapse check:** High. The chain involves multiple distinct agency beats:
1. Drogo decides to ignore his wound / reject healers — MOTIVATES(infection-worsens, drogo)
2. Dany invites Mirri over Dothraki bloodriders' objections — COMMANDS_IN is already modeled (bloodriders-attack-mirri has 3 roles but 0 causal)
3. Mirri deliberately performs sabotaged healing (betrayal) — SACRIFICES edge type (or CAUSES pointing to both deaths)
4. Dany smothers Drogo — AGENT_IN(dany, death-of-khal-drogo) — this is the act, not a passive consequence

Modeling cleanly requires: CAUSES chain through the ritual hub + MOTIVATES(drogo-wound → mirri-blood-magic-ritual) + SACRIFICES(mirri → rhaego) + AGENT_IN(dany → drogo-death) + TRIGGERS(drogo-death → dragon-hatching).

**Missing beats (all need minting):**
1. `drogo-blood-magic-ritual` — event.ritual or event.incident; AGOT Dany VIII, the tent scene
2. `death-of-khal-drogo` — event.death; AGOT Dany IX (Dany smothers Drogo with cushion)
3. `dragon-hatching-on-drogo-pyre` — event.incident; AGOT Dany X (three cracks + dragons emerge)

**Upstream attach-point:** The wine merchant assassination attempt (`the-wine-merchant-attempts-to-poison-dany`, HIT) is upstream of Drogo's vow (see E4), but the pyre arc can be treated as standalone (the wounding at Qohor/Lhazareen is the direct enable, not the wine merchant). Declare standalone prime mover at `drogo-blood-magic-ritual` (the wounding ENABLES it but is not a separate event node). The bloodriders-attack-mirri node (EXISTS) should attach here as CAUSES or SUB_BEAT_OF.

**Terminus:** `dragon-hatching-on-drogo-pyre` (to mint). Concrete, clean hard-stop. Downstream (Dany acquires army) is a separate juncture.

**Verbatim quote:** "Only death can pay for life." — Mirri Maz Duur (agot-daenerys-09.md:127, confirmed)
**Pyre quote:** "When the fire died at last and the ground became cool enough to walk upon, Ser Jorah Mormont found her amidst the ashes, surrounded by blackened logs and bits of glowing ember and the burnt bones of man and woman and stallion." (agot-daenerys-10.md:121, confirmed)

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 1 | 2 | 0 | 2 | **9/12** |

**Verdict: HIGH VALUE. Beat-readiness = 0 (3 mints required), but this is the prime mover — nothing downstream can attach without it. Grounding = 2 (Dany is sole POV but text is richly verbatim-grounded). X = 1 (Dany POV only, though consequences are seen by Jorah + the khalasar). Build before the Slaver's Bay arcs since they depend on the dragons existing.**

---

### E2. Fall of Astapor (the "Dracarys" Turn)

**Description:** Dany arrives in Astapor, negotiates with Kraznys mo Nakloz through Missandei, conceals her Valyrian, trades a dragon for the Unsullied, then says "Dracarys" — dragons kill the Good Masters, Unsullied freed, city falls. The most consequential single scene in the Slaver's Bay arc. `fall-of-astapor` EXISTS but has 0 causal edges. The node needs upstream attach + downstream consequences wired.

**Anti-signal check:** The "Dracarys" scene is explicit CAUSES logic — Dany's deception plan CAUSES the slave-masters' deaths + the Unsullied acquisition. NOT mere sequence. The node `fall-of-astapor` has rich wiki prose (already in the graph node file) and verbatim book quotes. The fall CAUSES Dany's army that enables all subsequent battles. Real CAUSES.

**Agency-collapse check:** Moderate. The sequence is:
- Jorah suggests buying Unsullied → MOTIVATES(dany) — already a character edge, may not need event modeling
- Dany's deception plan (concealing Valyrian) is a decision beat built INTO the fall-of-astapor node
- The "Dracarys" command is the decisive act (Dany COMMANDS_IN + AGENT_IN the dragons)
- No hidden agency — Dany makes a decision and executes it; the node itself CAN carry this

What's missing is primarily: upstream MOTIVATES edges to Dany + downstream CAUSES to Yunkai and Meereen approach. The fall is a STANDALONE prime mover for the military arc (it precedes Yunkai/Meereen in the campaign sequence, but the campaign itself begins here as a causal node, not merely a sequence point).

**Missing beats:** None to mint — `fall-of-astapor` EXISTS. Need:
- 1–2 causal outgoing edges from `fall-of-astapor`: CAUSES toward `dany-marches-on-yunkai` (new beat) or CAUSES toward `battle-of-yunkai` (EXISTS, DARK). Direct CAUSES: `fall-of-astapor CAUSES battle-of-yunkai` is defensible (the army from Astapor enables the Yunkai confrontation), but the anti-signal check applies here: Astapor→Yunkai is campaign sequence as much as causal chain. The REAL causal consequence is: army acquired → Meereen occupation → stalemate. Chain through battles is PRECEDES; the causal VALUE is the stalemate downstream.

**Upstream attach-point:** Standalone prime mover for the military arc. Optionally: `dragon-hatching-on-drogo-pyre` (to mint per E1) CAUSES → army-building path, but that's a multi-hop stretch. Declare standalone at `fall-of-astapor`.

**Terminus:** `siege-of-meereen` (EXISTS, 0 causal) → CAUSES → `sons-of-the-harpy-kill-twenty-nine` (EXISTS, 0 causal) → MOTIVATES → Dany's political compromise.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 1 | 2 | 2 | **11/12** |

**Verdict: VERY HIGH VALUE, LOW COST — all nodes exist. Causal load = 1 because Astapor→Yunkai→Meereen is partially sequence (see SEQUENCE TRAP below). The real causal chain lives in the Meereen CONSEQUENCES, not the battle-to-battle transitions. Build a 2-edge chain: `fall-of-astapor CAUSES siege-of-meereen CAUSES sons-of-the-harpy-kill-twenty-nine` with agency MOTIVATES bridging. 0 new mints. Cheap.**

---

### E3. Meereen Stalemate → Political Marriage → Daznak's Pit → Drogon Flees

**Description:** The Meereen arc's internal causal chain. The Sons of the Harpy insurgency MOTIVATES Dany toward the political marriage to Hizdahr (buying peace); the marriage CAUSES the opening of fighting pits; the Daznak pit event (Drogon returns, chaos ensues) TRIGGERS Dany's escape on Drogon and the ADWD endpoint — Dany lost on the Dothraki sea.

**Anti-signal check:** MOTIVATES(harpy-insurgency → dany) is real — the text shows Dany's decision to marry Hizdahr is explicitly driven by the insurgency deaths (`sons-of-the-harpy-kill-twenty-nine` models one specific escalation). `wedding-of-hizdahr CAUSES daznak-events` is NOT a simple CAUSES — the opening of fighting pits is a peace concession required by Hizdahr, which then enables Drogon's return to Meereen. The causation is real but mediated.

**Agency-collapse check:** High. Multiple human decisions:
- Dany DECIDES to accept Hizdahr's terms (MOTIVATES)
- Hizdahr DEMANDS fighting pits as a condition — an event itself
- Drogon RETURNS unpredictably (dragon agency, not human)
- Dany DECIDES to run into the pit and mount Drogon

The Daznak cluster has 5 existing role-only nodes (hizdahr-orders-drogon-killed, drogon-kills-more-attackers, unnamed-spearman-attacks-drogon, drogon-kills-more-attackers, daario-offers-to-kill-jorah) — all DARK causally. These need causal coordination.

**Missing beats:**
1. `drogon-returns-to-daznak-pit` — NO NODE (this is the trigger for the cascade; Drogon descends on the boar, kills Barsena Blackhair, the hero throws a spear, chaos begins)
2. `dany-mounts-drogon-and-flees-meereen` — NO NODE; event.incident; ADWD Dany IX
3. `dany-lost-on-dothraki-sea` — NO NODE; event.incident; ADWD Dany X

**Upstream attach-point:** `sons-of-the-harpy-kill-twenty-nine` (HIT, 0 causal) → MOTIVATES dany-targaryen.
OR: `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (HIT, 0 causal out) → CAUSES daznak-opening.

**Terminus:** `dany-lost-on-dothraki-sea` (to mint). Clean ADWD terminus. Does NOT need to carry forward into TWOW territory.

**Verbatim quote:** "North they flew, beyond the river, Drogon gliding on torn and tattered wings through clouds… Then there was nothing beneath them but grass rippling in the wind." (adwd-daenerys-09.md:55, confirmed)

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 1 | 2 | **11/12** |

**Verdict: VERY HIGH VALUE. The ADWD endpoint is the published-series terminus of Dany's arc; completing this chain gives a walkable path from the pyre (E1) through to the Dothraki sea. 3 mints + 4–5 causal edges. Medium scope.**

---

### E4. Robert's Assassination Order → Wine Merchant → Drogo's Westward Vow (Bridge)

**Description:** Robert's assassination order (agot-eddard-08:13 "I want them dead, mother and child both") is currently modeled only via the COMMANDS_IN role edge on the wine-merchant-attempt node. The ORDER itself has no event node. Its consequence: the wine merchant attempt → Dany terrified → Drogo enraged → Drogo's vow at the Western Market (agot-daenerys-06:179 "I will take my khalasar west… This I swear before the Mother of Mountains"). The vow is the MOTIVATING cause for the entire "Dothraki cross the sea" threat — which is what pushed Ned to oppose the assassination, which cost him his position, which eventually led to his execution.

**Anti-signal check:** Robert's order CAUSES the assassination attempt (COMMANDS_IN already models the execution channel). The attempt CAUSES Drogo's vow (textually: Dany reflects "The Usurper has woken the dragon now" immediately after the attempt; Drogo's vow follows at the same market scene). Real CAUSES chain.

**Agency-collapse check:** Low on the assassination → attempt leg (direct command → execution). Higher on the attempt → vow leg: Drogo's vow is HIS decision, triggered by seeing Dany threatened. Model: `wine-merchant-attempt MOTIVATES drogo → drogo-westward-vow AGENT_IN drogo`. The MOTIVATES edge is the right type here (threat to Rhaego → Drogo's emotional decision to conquer Westeros).

**Missing beats:**
1. `robert-orders-daenerys-assassination` — event.assassination; AGOT Eddard VIII:13; the Small Council scene
2. `drogo-westward-vow` — event.ceremony (an oath before the Mother of Mountains); AGOT Dany VI:179

**Upstream attach-point:** `death-of-robert-baratheon` — NOT the right upstream here. Robert's assassination ORDER comes BEFORE his death (AGOT Eddard VIII, while Robert is still alive). The order is triggered by learning Dany is pregnant. The upstream enable is `daenerys-targaryen pregnant` (not a modeled event). Declare standalone prime mover at `robert-orders-daenerys-assassination`.

**Note on cross-book join:** `ned-orders-daenerys-s-assassination-cancelled` (EXISTS) should become the DOWNSTREAM terminus of `robert-orders-daenerys-assassination` via CAUSES. This creates a cross-book causal join: Robert's order → wine merchant attempt + Ned's cancellation (both consequences of the same order). The cancellation node then gets its 0 outgoing edge finally explained.

**Terminus (immediate):** `drogo-westward-vow` (new). Then CAUSES → drogo-blood-magic-ritual (E1) if E1 is built, since the westward march requires Drogo functional — the failed march is part of WHY Drogo's wound matters.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 2 | 2 | 1 | 2 | **11/12** |

**Verdict: VERY HIGH VALUE. This is the bridge that connects the WO5K assassination arc (Robert's death) to the Essos spine. 2 mints + 3–4 causal edges. Establishes the canonical Westeros→Essos causation. Build before E1 if possible since `drogo-westward-vow` enables E1's root.**

---

### E5. Doran's "Fire and Blood" Pact → Quentyn's Quest → Death of Quentyn Martell

**Description:** Doran reveals to Arianne the long-kept secret: he sent Quentyn to Meereen to present a marriage-contract pact (Viserys was promised to Arianne; now Daenerys is promised to Quentyn). The S117 Dorne arc rooted the arrest-of-sand-snakes chain, which ends with Arianne's imprisonment and Doran's reveal. This is the Dorne→Essos bridge. In Meereen, Quentyn arrives, is rejected, attempts to steal a dragon, and is burned alive — the death of Quentyn is the terminus.

**Anti-signal check:** `doran-reveals-fire-and-blood-pact CAUSES quentyn-martell-travels-to-meereen` is NOT a simple CAUSES — Quentyn was already traveling before the reveal (Arianne is kept ignorant; the reveal explains what has been happening). The causal structure is: Doran's decision (years earlier) CAUSES Quentyn's departure; the reveal is an exposition beat, not the triggering event. Better model: `doran-reveals-fire-and-blood-pact` is an event.incident where `doran-martell REVEALS_TO arianne-martell` — NOT a CAUSES node for Quentyn's journey. The Quentyn journey was triggered by Doran's long-standing plan (undated historical decision, hard to model causally). The pact-reveal IS real causation for Arianne's UNDERSTANDING and her future actions. The Quentyn chain (quest → rejection → dragon attempt → death) is its own internal chain.

**Agency-collapse check:** High in the Quentyn chain. Between "pact exists" and "Quentyn burned":
- Dany rejects the pact (her decision)
- Quentyn decides to attempt dragon theft anyway — `quentyn-orders-the-attack` EXISTS (already has 5 role edges, 0 causal out) — this is the decision node
- The dragons respond — dragon agency (Viserion burns Quentyn)
- Modeling: `quentyn-orders-the-attack TRIGGERS death-of-quentyn-martell` (dragon's response is the immediate consequence of Quentyn's unauthorized action)

**Missing beats:**
1. `doran-reveals-fire-and-blood-pact` — event.incident; AFFC Princess-in-the-Tower:325; already in the S117 harvest queue as parked
2. `death-of-quentyn-martell` — event.death; ADWD Dragontamer chapter; "charred bones and ashes" aftermath (the actual burning happens between chapters — confirmed in Barristan's subsequent POV)

**Upstream attach-point:** S117 built: `arrest-of-the-sand-snakes MOTIVATES arianne-martell` → queenmaker → reveal. The pact-reveal node should connect here (the imprisonment is what FORCES Doran to reveal). Clean attach at `arianne-collapses-and-is-captured` (built S117).

**Terminus:** `death-of-quentyn-martell` (to mint). Clean terminus: Quentyn's mission fails absolutely; the pact comes to nothing.

**Verbatim quote (pact reveal):** "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, 'Fire and blood.'" (affc-the-princess-in-the-tower-01.md:325, confirmed)

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 1 | 2 | 2 | 1 | 2 | **10/12** |

**Verdict: HIGH VALUE. Closes the Dorne arc built in S117 by extending it into Essos and providing a terminus. Salience = 1 (Quentyn is a significant character but a minor arc); Cross-POV = 2 (Arianne, Quentyn/Dragontamer, Barristan see the consequences). 2 mints + 3–4 edges. Depends on E3 being built first (Quentyn's death occurs during the Meereen occupation context).**

---

### E6. Euron → Victarion → En Route to Daenerys (Bridge Downstream Extension)

**Description:** `euron-commissions-victarion-to-fetch-daenerys` EXISTS and has 1 upstream CAUSES from `taking-of-the-shields` (S116 built). Its downstream is DARK: Victarion's voyage to Meereen (capture of the Willing Maiden, freeing of rowers, navigation to Slaver's Bay) has scattered role-only nodes but no causal arc. The Essos decomposition is the natural place to model this downstream.

**Anti-signal check:** `euron-commissions CAUSES victarion-sails-to-meereen` is real CAUSES (direct commission → journey). The Willing Maiden capture (`slaver-galley-willing-maiden-captured`, EXISTS) is an episode along the route — CAUSES or PRECEDES? The capture ENABLES the freeing of slave rowers who swell Victarion's crew; that's a CAUSES consequence, not mere sequence.

**Agency-collapse check:** Low. Victarion receives orders and executes them with operational decisions (the Willing Maiden capture is his tactical initiative). Model: `euron-commissions CAUSES victarion-iron-fleet-sails-east` (new beat) → `slaver-galley-willing-maiden-captured CAUSES slavers-killed-rowers-freed` (both exist, 0 causal).

**Missing beats:**
1. `victarion-iron-fleet-sails-to-meereen` — event.incident; ADWD Victarion I; the departure node

**Upstream attach-point:** `euron-commissions-victarion-to-fetch-daenerys` (HIT, 1 CAUSES upstream from taking-of-the-shields). Clean attach.

**Terminus:** `slaver-galley-willing-maiden-captured` → `slavers-killed-rowers-freed` (both HIT). OR hold at the departure node if the voyage-episode detail is secondary.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 1 | 1 | 1 | 2 | 2 | **8/12** |

**Verdict: MEDIUM VALUE, LOW COST. Beat-readiness = 2 (nodes exist), but salience and cross-POV are low (Victarion is a single POV). The main value is completing the Kingsmoot→Euron arc's downstream wire. Build after E1–E5 as cleanup.**

---

### E7. Illyrio/Varys Conspiracy Dyad (AGOT Arya III Witness)

**Description:** Arya witnesses Varys and Illyrio talking in the tunnels beneath the Red Keep (agot-arya-03:73–97). They discuss: the princess is pregnant (Dany), the Dothraki khal won't move until the son is born, Ned Stark "troubles my sleep," the need to delay. This is the conspiracy-as-process: Varys and Illyrio are actively managing the Targaryen restoration from King's Landing. The conversation is load-bearing: Arya tells Ned what she heard (partially), and Ned dismisses it ("they were mummers") — his failure to take it seriously is a factor in his downfall.

**Anti-signal check:** The dyadic relationship `CONSPIRES_WITH(varys, illyrio)` is real canon — the text shows them coordinating on protecting Dany, managing the Small Council, and trying to preserve Ned long enough for the Dothraki to cross. However, a single conversation event node is borderline: does the ACT of conspiring in this specific scene carry its own causal consequence? The answer is: Arya tells Ned, Ned dismisses it — which is the missed intelligence that contributes to his arrest. This IS a causal node (the conversation CAUSES the missed-intelligence, which MOTIVATES Ned's over-confidence). But the causation is weak and mediated by multiple further decisions.

**Agency-collapse check:** Very high. Between "they conspire" and any identifiable consequence, there are 4–5 human decisions (Arya tells Ned, Ned dismisses, Ned doesn't act on the warning…). This is NOT a clean CAUSES chain.

**Better modeling:** Not a full causal arc node — better as a relationship dyad edge `CONSPIRES_WITH(varys, illyrio)` on both character nodes, with `evidence_kind: book-curator` and cite at agot-arya-03.md:89. The `arya-stark WITNESS_IN` this scene is a WITNESS_IN edge on whatever event node models it.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 1 | 2 | 1 | 2 | 2 | **9/12** |

**Verdict: MEDIUM VALUE but WRONG SHAPE for a causal arc. Best modeled as character dyad edges + WITNESS_IN, NOT as a causal event node. A single event mint (`varys-illyrio-conspire-in-the-tunnels`) is defensible if the CONSPIRES_WITH dyad needs an anchor event (per architecture.md's dyadic reification policy). Flag for orchestrator: is a conspiracy-meeting event node the right shape, or just add the CONSPIRES_WITH relation to varys and illyrio's character nodes?**

---

### E8. Jorah as Informant for Varys/Robert (Information Channel Dyad)

**Description:** Jorah Mormont informs on Dany to the Small Council in exchange for a royal pardon for his slave-trading crimes. The intel channel is confirmed: Illyrio's letter (agot-daenerys-07:41: "Illyrio writes that they had a plague last year…" — Illyrio uses Jorah as a conduit). The wine merchant assassination attempt is Robert's response to Jorah's report of Dany's pregnancy. This is NOT a causal arc — it's an information channel dyad.

**Anti-signal check:** INFORMATION CHANNEL, not causal arc. Jorah INFORMS varys/robert; this is the vehicle by which Robert learns of the pregnancy. The causal consequence is `robert-orders-daenerys-assassination` (E4). The relationship between Jorah and Robert/Varys is a BACKGROUND CONDITION, not an event with its own causal chain. Best modeled as a `SPIES_ON(jorah, daenerys)` + `INFORMS(jorah, varys)` dyad.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 1 | 1 | 0 | 2 | 2 | **7/12** |

**Verdict: AT GATE but wrong shape. Causal load = 0 (pure information channel). Model as character dyads (SPIES_ON, INFORMS), not a causal event arc. The CAUSAL consequence of Jorah's spying is already captured in E4 (Robert's assassination order). No event mint needed.**

---

## 4. Sequence-Only Traps (SKIP/DEFER with reasons)

| Juncture | Why Skip/Defer |
|----------|----------------|
| **Astapor → Yunkai → Meereen battle sequence** | Anti-signal #1: pure military campaign sequence. Each battle does not *cause* the next — Dany is running a campaign. `battle-of-yunkai CAUSES siege-of-meereen` is wrong; PRECEDES already covers it. The only real CAUSE is Astapor → army acquisition → eventual Meereen occupation; that chain is modeled at the campaign-hub level, not battle-by-battle. |
| **Battle of Yunkai (the night battle)** | `battle-of-yunkai` is COMPLETELY DARK (0 edges of any type). It has zero causal value because Yunkai's internal sequence (night-attack-planned → battle-near-yunkai) is a tactical sub-sequence of the broader campaign. Model it as PART_OF the campaign hub rather than as a causal node. |
| **Second Siege of Meereen** | COMPLETELY DARK (0 edges). This is an ADWD military event (the Yunkish/Volantene fleet's siege) that occurs AFTER Dany has flown away. Causally, it is a CONSEQUENCE of the political stalemate Dany created but did not resolve. DEFER: it needs `dany-lost-on-dothraki-sea` (E3 terminus) built first, then the second siege can attach as a downstream consequence. |
| **Dany's rule in Meereen as a political arc** | The "Meereen governance" beats (the Unsullied patrol nodes, the freedmen enfranchisement, the pit-reopening negotiations) are a pattern of decision-making, not a causal chain. No single event CAUSES the next; these are parallel policy decisions. Skip as causal arc; the relevant causal node is the insurgency escalation (sons-of-the-harpy) and the political marriage response. |
| **Targaryen campaign hub as umbrella terminus** | `targaryen-campaign-in-slavers-bay` is a PART_OF container, NOT a causal terminus. Never chain CAUSES into it. All causal arcs bypass the hub and attach to specific sub-events or character nodes. |
| **Jorah's banishment from Meereen** | `daario-offers-to-kill-jorah` (EXISTS, 0 causal) and Dany's eventual decision to send Jorah away — this is character development, not a causal chain with clear consequences modeled in the graph. DEFER: it feeds into Jorah's ADWD storyline (greyscale, Tyrion transport) which is out of the Essos arc scope. |

---

## 5. Ranked Build Order

**Priority 1 (build first):** Establishes the prime mover; all other arcs root here.

### Rank 1 — E4: Robert's Assassination Order → Wine Merchant → Drogo's Westward Vow
**2 mints, 3–4 causal edges. Bridges WO5K into Essos; Tier-1 verbatim-grounded.**
- Mint: `robert-orders-daenerys-assassination` (event.assassination; AGOT Eddard VIII:13)
- Mint: `drogo-westward-vow` (event.ceremony; AGOT Dany VI:179)
- Wire: `robert-orders-daenerys-assassination CAUSES the-wine-merchant-attempts-to-poison-dany` (Tier-2)
- Wire: `robert-orders-daenerys-assassination CAUSES ned-orders-daenerys-s-assassination-cancelled` (Tier-2; both are downstream of the same order)
- Wire: `the-wine-merchant-attempts-to-poison-dany MOTIVATES drogo-stark` (Tier-2; the attempt enrages Drogo)
- Wire: `drogo-westward-vow AGENT_IN drogo-stark` (Tier-1 role)
- Attach-point: standalone root (the order precedes Robert's death)
- Terminus: `drogo-westward-vow` (concrete)
- Cross-graph bonus: `ned-orders-daenerys-s-assassination-cancelled` gets its first upstream CAUSES edge; `the-wine-merchant-attempts-to-poison-dany` gets its first upstream CAUSES edge

### Rank 2 — E1: Dragon Birth Arc (Drogo's Wound → Mirri Ritual → Drogo's Death → Dragon Hatching)
**3 mints, 5–6 causal/role edges. The prime mover of the entire Essos spine.**
- Mint: `drogo-blood-magic-ritual` (event.incident/ritual; AGOT Dany VII–VIII: Mirri's healing + sabotage)
- Mint: `death-of-khal-drogo` (event.death; AGOT Dany IX: Dany smothers Drogo; "If I look back I am lost")
- Mint: `dragon-hatching-on-drogo-pyre` (event.incident; AGOT Dany X: three cracks + dragons emerge)
- Wire: `drogo-westward-vow ENABLES drogo-blood-magic-ritual` (Tier-2; the westward march is derailed by the wound)
- Wire: `drogo-blood-magic-ritual CAUSES death-of-khal-drogo` (Tier-2; Mirri's sabotage leaves Drogo a husk)
- Wire: `death-of-khal-drogo TRIGGERS dragon-hatching-on-drogo-pyre` (Tier-2; Dany builds the pyre, places the eggs)
- Wire: `bloodriders-attack-mirri CAUSES drogo-blood-magic-ritual` (Tier-2; the attack interrupts the healing, motivating Mirri's revenge) — OR `bloodriders-attack-mirri PRECEDES drogo-blood-magic-ritual` if causal link is contested; flag for fresh-subagent verify
- Role edges: `mirri-maz-duur AGENT_IN drogo-blood-magic-ritual`, `daenerys-targaryen AGENT_IN death-of-khal-drogo` (Dany smothers him), `mirri-maz-duur VICTIM_IN dragon-hatching-on-drogo-pyre` (burned on the pyre), `daenerys-targaryen AGENT_IN dragon-hatching-on-drogo-pyre`
- Attach-point: `drogo-westward-vow` (from Rank 1; or standalone if E4 not yet built)
- Terminus: `dragon-hatching-on-drogo-pyre`

### Rank 3 — E2: Fall of Astapor → Meereen Occupation → Sons of the Harpy
**0 mints, 2–3 causal edges. All nodes exist; pure wire.**
- Wire: `fall-of-astapor CAUSES siege-of-meereen` (Tier-2; the Unsullied army enables the Meereen siege)
- Wire: `siege-of-meereen CAUSES sons-of-the-harpy-kill-twenty-nine` (Tier-2; the occupation creates the insurgency conditions)
- Wire: `sons-of-the-harpy-kill-twenty-nine MOTIVATES daenerys-targaryen` (Tier-2; the murders motivate her political compromise)
- Attach-point: `fall-of-astapor` (standalone prime mover for the military arc)
- Terminus: `sons-of-the-harpy-kill-twenty-nine` → downstream into E3

### Rank 4 — E3: Meereen Stalemate → Political Marriage → Daznak's Pit → Drogon Flees
**3 mints, 4–5 causal edges. The ADWD endpoint and series' published terminus for Dany.**
- Mint: `drogon-returns-to-daznak-pit` (event.incident; ADWD Dany IX — Drogon descends on the boar, kills Barsena; the trigger for the cascade; "the dragon turned, dark against the sun")
- Mint: `dany-mounts-drogon-and-flees-meereen` (event.incident; ADWD Dany IX — "the scarlet sands were falling away beneath her")
- Mint: `dany-lost-on-dothraki-sea` (event.incident; ADWD Dany X — barefoot in the grass, trying to find the river)
- Wire: `sons-of-the-harpy-kill-twenty-nine MOTIVATES daenerys-targaryen` (Tier-2) → Dany CAUSES `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (MOTIVATES arc)
- Wire: `wedding-of-hizdahr CAUSES drogon-returns-to-daznak-pit` (Tier-2; the wedding and pit-opening is the condition that allows Drogon back into the arena proximity — but mediated; flag for fresh-subagent verify)
- Wire: `drogon-returns-to-daznak-pit TRIGGERS dany-mounts-drogon-and-flees-meereen` (Tier-2; direct trigger)
- Wire: `dany-mounts-drogon-and-flees-meereen CAUSES dany-lost-on-dothraki-sea` (Tier-2)
- Attach-point: flows from Rank 3 (`sons-of-the-harpy`)
- Terminus: `dany-lost-on-dothraki-sea`

### Rank 5 — E5: Doran's Pact Reveal → Quentyn's Quest → Death of Quentyn Martell
**2 mints, 3–4 causal edges. Closes the S117 Dorne arc into Essos.**
- Mint: `doran-reveals-fire-and-blood-pact` (event.incident; AFFC Princess-in-the-Tower:325; Doran presses the onyx dragon into Arianne's palm)
- Mint: `death-of-quentyn-martell` (event.death; ADWD; Quentyn burned by Viserion after `quentyn-orders-the-attack`)
- Wire: `arianne-collapses-and-is-captured CAUSES doran-reveals-fire-and-blood-pact` (Tier-2; S117-built node; her imprisonment triggers Doran's decision to finally reveal the plan)
- Wire: `quentyn-orders-the-attack TRIGGERS death-of-quentyn-martell` (Tier-2; direct — the dragon's response kills him)
- Wire: `doran-reveals-fire-and-blood-pact AGENT_IN doran-martell`, `WITNESS_IN arianne-martell` (role edges; Arianne load-bearingly sees this revelation)
- Attach-point: `arianne-collapses-and-is-captured` (S117-BUILT; cross-book hinge)
- Terminus: `death-of-quentyn-martell`

---

## 6. Cross-Book Attach-Points Map

For each arc, the node it roots at (upstream) and the node it terminates at (downstream), with hit/miss status for each.

| Arc | Upstream Attach | Status | Downstream Terminus | Status |
|-----|----------------|--------|---------------------|--------|
| E4: Robert's order → Drogo vow | `death-of-robert-baratheon` (NO — Robert is alive when the order is given); declare STANDALONE at `robert-orders-daenerys-assassination` | STANDALONE | `drogo-westward-vow` (to mint) | NEW |
| E1: Dragon birth arc | `drogo-westward-vow` (E4 terminus, to mint) | E4-dep | `dragon-hatching-on-drogo-pyre` (to mint) | NEW |
| E2: Astapor → insurgency | `fall-of-astapor` (HIT, STANDALONE) | HIT | `sons-of-the-harpy-kill-twenty-nine` (HIT) | HIT |
| E3: Stalemate → Drogon flees | `sons-of-the-harpy-kill-twenty-nine` (HIT, E2 terminus) | HIT | `dany-lost-on-dothraki-sea` (to mint) | NEW |
| E5: Pact reveal → Quentyn death | `arianne-collapses-and-is-captured` (HIT, S117-BUILT) | HIT | `death-of-quentyn-martell` (to mint) | NEW |
| E6: Euron commission downstream | `euron-commissions-victarion-to-fetch-daenerys` (HIT, 1 upstream CAUSES) | HIT | `slavers-killed-rowers-freed` (HIT) | HIT |
| WO5K cross-join | `death-of-robert-baratheon` (WO5K arc terminus) | HIT | Joins E4 via robert-orders (same session but different events) | — |
| S117 Dorne cross-join | `arrest-of-the-sand-snakes` → `arianne-collapses-and-is-captured` (S117-BUILT) | HIT | `doran-reveals-fire-and-blood-pact` → E5 | NEW |

**Kingsmoot→Euron spine (S116)** is the upstream context for E6 but is structurally independent — the Kingsmoot arc is a STANDALONE root (prime mover = Balon's death). It attaches to the Essos arc via Victarion's commission, but the two arcs do NOT share a causal edge between them — the commission IS the join.

---

## 7. Nodes to Mint (Summary)

All candidates dedup-checked via `event_alias_resolver.py --lookup` + `ls graph/nodes/events/ | grep -i <stem>`. No collisions found.

| Node to Mint | Proposed Slug | Type | Source | For Juncture |
|---|---|---|---|---|
| Robert orders Daenerys assassination | `robert-orders-daenerys-assassination` | event.assassination | AGOT Eddard VIII:13 | E4 |
| Drogo's westward vow | `drogo-westward-vow` | event.ceremony | AGOT Dany VI:179 | E4 |
| Drogo blood magic ritual | `drogo-blood-magic-ritual` | event.incident | AGOT Dany VII–VIII | E1 |
| Death of Khal Drogo | `death-of-khal-drogo` | event.death | AGOT Dany IX | E1 |
| Dragon hatching on Drogo's pyre | `dragon-hatching-on-drogo-pyre` | event.incident | AGOT Dany X | E1 |
| Drogon returns to Daznak's Pit | `drogon-returns-to-daznak-pit` | event.incident | ADWD Dany IX | E3 |
| Dany mounts Drogon and flees Meereen | `dany-mounts-drogon-and-flees-meereen` | event.incident | ADWD Dany IX | E3 |
| Dany lost on the Dothraki sea | `dany-lost-on-dothraki-sea` | event.incident | ADWD Dany X | E3 |
| Doran reveals Fire and Blood pact | `doran-reveals-fire-and-blood-pact` | event.incident | AFFC Princess-in-the-Tower:325 | E5 |
| Death of Quentyn Martell | `death-of-quentyn-martell` | event.death | ADWD Dragontamer/Barristan II | E5 |
| Victarion iron fleet sails east | `victarion-iron-fleet-sails-to-meereen` | event.incident | ADWD Victarion I | E6 (optional) |

**Aliases must be natural SPACED phrases (not kebab slugs). Examples:**
- `death of Khal Drogo` · `Drogo's death` · `the khal dies`
- `dragon hatching` · `birth of the dragons` · `dragons born on the pyre`
- `Doran's pact reveal` · `fire and blood whisper` · `Doran tells Arianne`
- `Drogon flies from Daznak` · `Dany flees Meereen on Drogon`

---

## 8. Harvest Queue Additions

Collected incidentally while reading chapter text for this dip. Appended to `working/harvest-queue.md`.

| status | kind | book | ref | note | session |
|--------|------|------|-----|------|---------|
| open | quote | agot | agot-daenerys-06.md:179 | Drogo's westward vow verbatim: "I will take my khalasar west to where the world ends, and ride the wooden horses across the black salt water as no khal has done before… This I swear before the Mother of Mountains, as the stars look down in witness." — load-bearing oath; evidence_quote for drogo-westward-vow node | 2026-06-21 s119-essos-decomp |
| open | quote | agot | agot-eddard-08.md:13 | Robert's assassination order verbatim: "I want them dead, mother and child both, and that fool Viserys as well. Is that plain enough for you? I want them dead." — evidence_quote for robert-orders-daenerys-assassination node | 2026-06-21 s119-essos-decomp |
| open | quote | agot | agot-daenerys-09.md:127 | Mirri: "Only death can pay for life." / Dany: "The price was paid and paid and paid." — evidence_quote for drogo-blood-magic-ritual node; both sides of the exchange load-bearing | 2026-06-21 s119-essos-decomp |
| open | quote | agot | agot-daenerys-10.md:117 | Dany: "I am Daenerys Stormborn, daughter of dragons, bride of dragons, mother of dragons, don't you see?" — foreshadowing of dragon motherhood identity; no foreshadowing edge exists on dany's character node for this | 2026-06-21 s119-essos-decomp |
| open | quote | agot | agot-daenerys-10.md:121 | Post-pyre: "She was naked, covered with soot… yet she was unhurt." — evidence_quote for dragon-hatching-on-drogo-pyre node (Dany's fireproof quality grounded verbatim) | 2026-06-21 s119-essos-decomp |
| open | foreshadowing | agot | agot-daenerys-06.md:153 | After wine merchant attempt: "The Usurper has woken the dragon now" — Dany's internal framing that directly motivates Drogo's vow; foreshadowing of the Targaryen return; no foreshadowing edge | 2026-06-21 s119-essos-decomp |
| open | appearance | agot | agot-daenerys-09.md:163 | Drogo after Mirri's ritual: "His eyes were wide open but did not see… he was blind. When she whispered his name, he did not seem to hear. The wound on his breast was as grey and red and hideous." — physical state of Drogo as living dead; evidence for death-of-khal-drogo node | 2026-06-21 s119-essos-decomp |
| open | quote | affc | affc-the-princess-in-the-tower-01.md:325 | Doran's "Fire and blood" whisper with the onyx dragon: verbatim already confirmed; evidence_quote for doran-reveals-fire-and-blood-pact node once minted | 2026-06-21 s119-essos-decomp |
| open | place | adwd | adwd-daenerys-09.md:233 | Daznak's Pit physical description: tiered seating from black (highest) to red (arena level), bronze warrior archway, ten thousand voices; "the red will hide any blood spatters" — atmospheric place description; no appearance section on daznak-s-pit node | 2026-06-21 s119-essos-decomp |
| open | quote | adwd | adwd-daenerys-09.md:55 | Dany flying north on Drogon: "North they flew, beyond the river, Drogon gliding on torn and tattered wings… Then there was nothing beneath them but grass rippling in the wind." — evidence_quote for dany-mounts-drogon-and-flees-meereen node | 2026-06-21 s119-essos-decomp |
| open | quote | adwd | adwd-daenerys-10.md:49 | Dany's summary of the pyre sequence in retrospect: "the maegi Mirri Maz Duur had murdered Rhaego in her womb, and Dany had smothered the empty shell of Khal Drogo with her own two hands" — ADWD Dany's own framing of the AGOT events; useful as retrospective cite | 2026-06-21 s119-essos-decomp |
| open | witness | agot | agot-arya-03.md:73 | Arya witnesses Varys/Illyrio tunnel conversation: "She saw the light of a single torch, small as the flame of a candle. Two men, she made out." — Arya is WITNESS_IN whatever event node models the conspiracy meeting; text-anchored confirmation she saw them | 2026-06-21 s119-essos-decomp |
| open | food | adwd | adwd-daenerys-09.md:109 | Daznak's Pit concession food: "peddlers were selling dog sausages, roast onions, and unborn puppies on a stick" — local food culture + animal welfare contrast; no node; atmosphere harvest | 2026-06-21 s119-essos-decomp |
| open | appearance | adwd | adwd-daenerys-09.md:233 | Drogon described from below at Daznak's Pit: "scales were black, eyes and horns and spinal plates blood red. His wings stretched twenty feet from tip to tip, black as jet." — verbatim physical description of Drogon at ADWD scale; drogon character node needs this citation | 2026-06-21 s119-essos-decomp |
