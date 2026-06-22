# AEGON Decomposition: Trigger-Tree, Scorecard, Build Rank

> **Created:** 2026-06-22
> **Purpose:** Map the AEGON container's internal causal trigger-tree (Varys/Illyrio conspiracy seed → Aegon hidden & revealed → Golden Company crosses to Westeros → Stormlands conquest → KL endgame assassinations); mark what's built vs dark; rank buildable arcs.
> **Read-only:** no graph writes (0 nodes minted, 0 edges added). Local cache only (no HTTP, no wiki refetch).
> **Session:** aegon-decomp dip

> **⊗ CROSS-CONTAINER SEAMS.**
> - **`siege-of-storms-end-300`** = AEGON ∩ WO5K. Its node prose currently describes the *Cersei→Mace-Tyrell* siege (AFFC, removing Mace from KL), which the *Golden Company* then inherits/contests (ADWD). The Aegon campaign overlaps post-Blackwater Stormlands politics. Tag `[aegon, wo5k]` at build; never re-build the Tyrell siege — ATTACH to it.
> - **`assassinations-of-pycelle-and-kevan-lannister`** = AEGON ∩ (KL/WO5K endgame). The Kevan-regency / Cersei-Tommen thread it terminates is the already-built KL endgame. Treat the Kevan/Pycelle node as an AEGON-owned terminus that ATTACHES to the KL-endgame characters (kevan-lannister, pycelle, cersei-lannister), not a rebuild of KL politics. Varys's motive ("whilst Aegon raises his banner above Storm's End") is the seam edge.
> - **`stone-men-attack-the-shy-maid`** is AEGON-internal (the Rhoyne journey; Connington's greyscale seed). Not a bridge. Already has rich role edges (AGENT_IN stone-men; VICTIM_IN aegon/tyrion/duck/ysilla). Untagged → tag `[aegon]` at build.
> - **`landing-of-the-golden-company`** carries a SUSPICIOUS cross-theater `PRECEDES -> wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (Meereen). Almost certainly a bad edge — FLAG for deletion at build, do NOT fix in this dip.
> - **The Varys↔Illyrio conspiracy seed (AGOT tunnels)** straddles nothing structurally — it is AEGON's root, witnessed by Arya (a Stark POV). Resolved as a dyad, NOT a node (see §1/§6 dyad decision).

---

## 1. Current Causal State — Verified Against Live Graph

All states verified with `python3 scripts/graph-query.py --container aegon`, `--neighbors <slug>`, `--causal-chain <slug>`, and direct node reads.

### Container membership (verified)

`--container aegon` returns **exactly 2 nodes**:
- `landing-of-the-golden-company` (event.battle)
- `assassinations-of-pycelle-and-kevan-lannister` (event.battle)

### Scaffolding correction — 6 PART_OF children, NOT 8+

**The continue prompt's "8+ PART_OF children" is WRONG. Verified count = 6.** `landing-of-the-golden-company` has exactly 6 incoming `PART_OF` edges (the Stormlands takings), plus 1 `GUARDS` and 1 `PRECEDES`:

```
landing-of-the-golden-company  (event.battle, containers:[aegon])
  OUTGOING (1):  PART_OF -> war-of-the-five-kings          [EDGE BUG — see below]
  INCOMING (8):
    PART_OF  <- fall-of-mistwood          (wiki-infobox, tier-2)
    PART_OF  <- invasion-of-tarth         (wiki-infobox, tier-2)
    PART_OF  <- taking-of-crows-nest      (wiki-infobox, tier-2)
    PART_OF  <- taking-of-greenstone      (wiki-infobox, tier-2)
    PART_OF  <- taking-of-griffins-roost  (wiki-infobox, tier-2)
    PART_OF  <- taking-of-rain-house      (wiki-infobox, tier-2)
    GUARDS   <- gorys-edoryen   (book cite: adwd-the-griffin-reborn-01.md:93)
    PRECEDES <- wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen  [SUSPICIOUS — likely-bad cross-theater edge]
```

Note: `siege-of-storms-end-300` and `taking-of-storms-end` are NOT among the 6 PART_OF children (neither is wired to the landing). They float free — see decoy-trap table and A3.

### Causal layer is entirely DARK

Verified via `--causal-chain` and `--neighbors`: **every AEGON campaign node has 0 causal edges (CAUSES / TRIGGERS / ENABLES / MOTIVATES) in or out.** Confirmed for:
`fall-of-mistwood`, `invasion-of-tarth`, `taking-of-crows-nest`, `taking-of-greenstone`, `taking-of-griffins-roost`, `taking-of-rain-house`, `taking-of-storms-end`, `siege-of-storms-end-300`, `landing-of-the-golden-company`, `assassinations-of-pycelle-and-kevan-lannister`, `stone-men-attack-the-shy-maid`.

`--causal-chain landing-of-the-golden-company` = **0 upstream + 0 downstream**. The whole AEGON spine is scaffolding (PART_OF + role edges) with no causal wiring.

### THE EDGE BUG (note for BUILD step 1 — do NOT fix in this dip)

Exactly **2** rows mis-file AEGON nodes under WO5K:
- `landing-of-the-golden-company PART_OF war-of-the-five-kings`
- `assassinations-of-pycelle-and-kevan-lannister PART_OF war-of-the-five-kings`

Both should be re-parented (the GC invasion is its own conflict, not part of WO5K) or at minimum dual-tagged at build. Separately, `assassination-of-tywin-lannister PART_OF war-of-the-five-kings` is a DIFFERENT, **legitimate** WO5K edge — leave it.

### Event nodes (HITs) relevant to AEGON — verified

| Node | Type | State |
|---|---|---|
| `landing-of-the-golden-company` | event.battle | `[aegon]`; 6 PART_OF children; 0 causal; edge bug + suspicious PRECEDES |
| `assassinations-of-pycelle-and-kevan-lannister` | event.battle | `[aegon]`; PART_OF WO5K (bug); **0 incoming, 1 outgoing**; 0 causal; no role edges (no AGENT_IN varys / VICTIM_IN kevan/pycelle wired) |
| `fall-of-mistwood` | event.battle | PART_OF landing; 0 causal |
| `invasion-of-tarth` | event.battle | PART_OF landing; 0 causal |
| `taking-of-crows-nest` | event.battle | PART_OF landing; 0 causal |
| `taking-of-greenstone` | event.battle | PART_OF landing; 0 causal |
| `taking-of-griffins-roost` | event.battle | PART_OF landing; 0 causal; **has 4 granular SUB_BEAT_OF children** (ram-assault-on-gatehouse, defenders-killed-on-battlements, maester-killed, prisoners-gathered-in-yard) |
| `taking-of-rain-house` | event.battle | PART_OF landing; 0 causal |
| `taking-of-storms-end` | event.battle | **WO5K (Stannis, OUT of scope)** — PART_OF WO5K; 0 causal — see decoy table |
| `siege-of-storms-end-300` | event.battle | seam node; PART_OF WO5K; 0 causal; NOT wired to landing |
| `stone-men-attack-the-shy-maid` | event.incident | AEGON-internal; LOCATED_AT shy-maid; 4 VICTIM_IN + 1 AGENT_IN; 0 causal; untagged |

### Character nodes (HITs) — slug verification

| Brief slug | Verified | Note |
|---|---|---|
| `aegon-targaryen-young-griff` | ✅ EXISTS | **OUR Aegon** (the claimant). 27 edges. aliases: "Young Griff", "Aegon VI" |
| `jon-connington` | ✅ | |
| `illyrio-mopatis` | ✅ | |
| `varys` | ✅ | (the brief's "verify slug" → confirmed `varys`, not `varys-the-spider`) |
| `haldon` | ✅ | |
| `lemore` | ✅ | |
| `rolly-duckfield` | (not spot-checked; pass-1 edges use `duck`) | "Duck" appears as `duck` in edges |
| `harry-strickland` | ✅ | |
| `tristan-rivers` | ✅ | |
| `black-balaq` | ✅ | |
| `gorys-edoryen` | ✅ | wired GUARDS -> landing |
| `kevan-lannister` | ✅ | |
| `grand-maester-pycelle` | ❌ **WRONG** | actual slug = **`pycelle`** (`graph/nodes/characters/pycelle.node.md`). The "grand-maester-pycelle" form does not exist. |

### ⚠ DECOY: two `Aegon-son-of-Rhaegar` nodes — do not cross the wires

The brief says `aegon-targaryen-son-of-rhaegar` = "the murdered infant". **Verified true at the node level but with a trap:** the AWOIAF wiki titles OUR claimant's article `Aegon_Targaryen_(son_of_Rhaegar)` too. There are two distinct nodes:
- **`aegon-targaryen-son-of-rhaegar`** — the historical infant murdered in the Sack of King's Landing (283 AC); alias "The prince that was promised". **OUT** of the AEGON-claimant character role (he is the *identity Young Griff claims to be*).
- **`aegon-targaryen-young-griff`** — the ADWD claimant. **IN.**

The wiki-prose of `landing-of-the-golden-company` mislinks to `Aegon_Targaryen_(son_of_Rhaegar)` in its citation text, but the **graph edges** (27 Pass-1-derived) correctly attach Aegon's campaign relationships to `aegon-targaryen-young-griff`. **At build, all new AEGON causal/role edges must target `aegon-targaryen-young-griff`.** Whether the infant-vs-claimant identity is "the same person" is the GATED Blackfyre theory — keep it out of the causal map entirely.

### Dyad decision (D1) — RESOLVED: dyad-only, no conspiracy node

Verified `working/dyad-queue.md` D1: no `varys-and-illyrio-conspire-in-the-tunnels` node exists. **Recommendation: keep the default — dyad-only, do NOT mint the conspiracy-meeting node.** Justification in §6.

---

## 2. Trigger-Tree — Full AEGON Internal Map

One root entry (the AGOT conspiracy seed) feeding a single long spine that forks at the KL endgame.

```
[AEGON ROOT — AGOT seed, agot-arya-03:73–109]
varys CONSPIRES_WITH illyrio-mopatis   [DYAD on character nodes, NOT a node]
   (Arya WITNESS_IN — parked; the meeting is NOT a causal node)
   "The princess is with child. The khal will not bestir himself until his son is born."
   |
   v  [MOTIVATES, DARK — the conspiracy's purpose]
   (Aegon hidden & raised in secret — Varys epilogue speech, adwd-epilogue:297)
   |
   v
[A1] aegon-revealed-to-the-golden-company   [MISS — needs mint]
   (adwd-the-lost-lord-01:127 — "I give you Aegon Targaryen, firstborn son of Rhaegar…")
   Connington's reveal of the boy to Strickland's war council
   |
   +--[TRIGGERS, DARK]--> [A2] golden-company-sails-for-westeros   [MISS — needs mint]
   |     (adwd-the-lost-lord-01:215–223 — Aegon: "sail west instead of east";
   |      breaks the Volantis/Yunkai contract option; Tyrion's goad to prove himself)
   |     The crossing.
   |        |
   |        v [CAUSES, DARK]
   |     landing-of-the-golden-company   [HIT, [aegon], 0 causal — the campaign HUB]
   |        |  (Cape Wrath; banners hidden; Kevan misreads it as Stannis's hire)
   |        |
   |        +===[A3] STORMLANDS CONQUEST CAMPAIGN — PART_OF fan (existing scaffolding) ===
   |        |   landing  <-PART_OF-  taking-of-griffins-roost  (Connington's own seat)
   |        |   landing  <-PART_OF-  taking-of-crows-nest      (House Morrigen / Tristan Rivers)
   |        |   landing  <-PART_OF-  taking-of-rain-house      (House Wylde / Laswell Peake)
   |        |   landing  <-PART_OF-  taking-of-greenstone      (Estermont / Marq Mandrake)
   |        |   landing  <-PART_OF-  invasion-of-tarth
   |        |   landing  <-PART_OF-  fall-of-mistwood
   |        |   (PART_OF is the RIGHT structure here — siblings, simultaneous; see §4.
   |        |    Adding CAUSES between sibling takings = granularity overclaim.)
   |        |
   |        +--[CAUSES, DARK]--> [A3-terminus] siege-of-storms-end-300  [HIT, seam [aegon,wo5k], 0 causal]
   |              (Connington: "I mean to take Storm's End" — adwd-the-griffin-reborn-01:173;
   |               the GC inherits/contests the Tyrell-then-token siege. Aegon insists on leading.)
   |
   +--[the KL endgame fork — Varys acts to keep the realm in chaos for Aegon] -->
         [A4] assassinations-of-pycelle-and-kevan-lannister  [HIT, [aegon], 0 causal]
            (adwd-epilogue:269–305 — Varys kills Pycelle then Kevan with a crossbow + the
             children's daggers; motive at :293 "whilst Aegon raises his banner above Storm's End")
            |
            +--[ATTACH, not rebuild]--> kevan-lannister / pycelle / cersei-lannister  (KL endgame chars)
            +--[role edges, DARK]--> varys AGENT_IN ; kevan-lannister VICTIM_IN ; pycelle VICTIM_IN
```

**The greyscale sub-thread** (Connington, adwd-the-lost-lord-01:237 + adwd-the-griffin-reborn-01:141) is a *character-state condition*, not a causal event node. It is a slow death-clock that MOTIVATES Connington's haste ("I do not have time enough for caution"). Model as node prose / a CONDITION on jon-connington, NOT a campaign event. POINTed to harvest, not a juncture.

### Root-entry analysis

There is **one** root: the Varys/Illyrio conspiracy. Unlike NORTH (two spines sharing a WO5K root), AEGON is a single causal river — conspiracy → reveal → crossing → landing → campaign → (parallel) KL chaos-seeding. The only true fork is at the end: the Stormlands campaign (A3) and the KL assassinations (A4) are two *parallel consequences* of the same upstream (the landing makes Aegon credible; Varys's KL murders clear his path), not a sequential chain.

---

## 3. Juncture Scorecard

Scoring rubric (from `causal-arc-strategy-2026-06-18.md`; 0–2 each axis, max 12):
- **Q (Query-value):** dip failed = 2, plausible = 1, never asked = 0
- **S (Salience):** major chain = 2, minor = 1, trivia = 0
- **X (Cross-POV reach):** 3+ POVs = 2, 2 POVs = 1, 1 POV = 0
- **C (Causal load):** real consequence = 2, mixed = 1, pure sequence = 0
- **B (Beat-readiness / cost):** all/most nodes exist = 2, some = 1, none = 0
- **G (Grounding):** in-saga POV = 2, mixed = 1, wiki-only = 0

**Gate: ≥ 7/12 AND not (G=0, Q<2).**

---

### A1. Conspiracy Seed → Aegon Revealed to the Golden Company

**Description:** The AGOT tunnels conspiracy (Varys + Illyrio, witnessed by Arya, agot-arya-03:73–109) is the seed; its payoff a book later is Connington unveiling the hidden prince to Strickland's war council (adwd-the-lost-lord-01:127). The conspiracy's *content* — keep Aegon hidden, raise him for rule — is delivered verbatim in Varys's epilogue speech (adwd-epilogue:297). This juncture binds the seed to the reveal.

**Anti-signal check:** The conspiracy MOTIVATES the entire arc; the reveal is the moment the hidden plan becomes an active campaign. Genuine MOTIVATES (conspiracy → Aegon raised) + the reveal as the first *event* node. Not sequence.

**Agency-collapse check:** Between "conspiracy" and "reveal" lie ~15 years and many decisions (Illyrio funds, Connington raises, Daenerys fails to come west forcing the plan-change). The S117 edge-vs-node rule: the *tunnel meeting* does NOT get a node (Arya's seeing has no outgoing causal edge — the Ned-dismissal link is 4–5-decisions-mediated → agency-collapse). The conspiracy lives as the **`varys CONSPIRES_WITH illyrio-mopatis` dyad**. The **reveal** DOES merit a node: it has a clean outgoing causal edge (reveal → GC sails west).

**Missing beats:**
1. `aegon-revealed-to-the-golden-company` — **MISS** (event.incident; adwd-the-lost-lord-01). The anchor.
2. `varys CONSPIRES_WITH illyrio-mopatis` dyad — **MISS** (dyad, not node; D1 in dyad-queue).
3. `arya-stark WITNESS_IN <conspiracy>` — **PARKED** (no node target; waits, per dyad decision, indefinitely).

**Upstream attach-point:** the dyad on varys/illyrio (built as part of this juncture). **Terminus:** `aegon-revealed-to-the-golden-company` (new).

**Container tags:** reveal → `[aegon]`. The dyad lives on character nodes (no container tag).

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 2 | 2 | 1 | 2 | **10/12** |

**Verdict: HIGH VALUE.** X=2 (Arya AGOT, Tyrion ADWD, Connington POV all touch this thread). The reveal is the container's narrative ignition. 1 mint + 1 dyad (2 edges) + 1 MOTIVATES from conspiracy. The dyad makes B=1 (reveal node new; varys/illyrio nodes exist). Cheap and load-bearing.

---

### A2. Golden Company Sails West (Crosses to Westeros)

**Description:** Aegon's decision to "sail west instead of east" (adwd-the-lost-lord-01:215–223) — claim the Iron Throne himself rather than wait for Daenerys — is the pivot. It overrides Strickland's caution, declines the Yunkai/Volantis contract, and is goaded by Tyrion ("prove himself by invading Westeros without Daenerys's aid"). The crossing CAUSES the landing.

**Anti-signal check:** This is the single most causally-loaded decision in the container. The whole invasion exists *because* Aegon chose west. Real TRIGGERS (a specific spark — the war-council vote) and CAUSES (decision → crossing → landing). Strong C.

**Agency-collapse check:** Low-to-moderate. The agency beat (Aegon's choice + Strickland's reluctant assent) is concrete and single-scene. Model: `aegon-revealed... TRIGGERS golden-company-sails-for-westeros` + `golden-company-sails-for-westeros CAUSES landing-of-the-golden-company` + `aegon-targaryen-young-griff MOTIVATES golden-company-sails-for-westeros` (his decision). Manageable. Tyrion's goad → an optional MOTIVATES from tyrion-lannister.

**Missing beats:**
1. `golden-company-sails-for-westeros` — **MISS** (event.incident / event.campaign; the crossing). This is the causal PARENT of the landing that the brief asks A2 to find. NOTE: do NOT overload it with the *broken Volantis contract* as a separate node — the contract-decline is captured as a qualifier/prose on this beat (it's a non-event: "I told him I would think on it"). One node.
2. `landing-of-the-golden-company` — **HIT** (the consequence; just needs the incoming CAUSES).

**Upstream attach-point:** `aegon-revealed-to-the-golden-company` (A1 terminus). **Terminus:** `landing-of-the-golden-company` (HIT).

**Container tags:** `golden-company-sails-for-westeros` → `[aegon]`.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 1 | 2 | 2 | 2 | **11/12** |

**Verdict: HIGHEST VALUE.** B=2 (only 1 mint; both endpoints' nodes effectively exist — A1's reveal upstream, landing downstream). The "why did the Golden Company land in the Stormlands instead of going to Daenerys?" query is exactly the kind that fails on the dark graph. The landing HUB (6 PART_OF children) becomes causally reachable the instant this CAUSES edge lands. X=1 (Connington + Tyrion POVs; mostly Connington) is the only soft axis.

---

### A3. Stormlands Conquest Campaign → Siege of Storm's End

**Description:** The landing fans out into 6 simultaneous takings (Griffin's Roost, Crow's Nest, Rain House, Greenstone, Tarth, Mistwood) already wired as `PART_OF landing-of-the-golden-company`. The campaign then converges on the strategic prize: Storm's End (`siege-of-storms-end-300`, the seam node). Connington: "I mean to take Storm's End… winning it will prove our strength" (adwd-the-griffin-reborn-01:173).

**Anti-signal check — THE KEY A3 QUESTION:** Is there a CAUSES spine *between* the takings, or is PART_OF the right and only structure? **PART_OF is correct; the takings are siblings, not a chain.** Per adwd-the-griffin-reborn-01:93, Griffin's Roost / Crow's Nest / Rain House were taken *simultaneously* by three columns ("Ser Tristan Rivers had set off simultaneously for… Crow's Nest, and Laswell Peake for Rain House"). Greenstone was an *accident* (Volantenes dumped Mandrake on Estermont). **Adding CAUSES between sibling takings would be granularity-overclaim** — the exact NORTH §4 Wall-sub-beats trap. The ONE real causal edge is `landing --[CAUSES]--> siege-of-storms-end-300` (the campaign's strength enables/justifies the move on Storm's End: "Four castles in as many days… let us take Storm's End").

**Agency-collapse check:** The siege decision is Connington's (a war-council choice, adwd-the-griffin-reborn-01:173–185) → `landing CAUSES siege-of-storms-end-300` + `jon-connington MOTIVATES siege-of-storms-end-300`. Clean. Aegon's insistence on leading the attack → optional MOTIVATES from aegon.

**Missing beats:**
1. **NO new event mints needed for the takings** — all 6 exist and PART_OF is correct.
2. `landing-of-the-golden-company --[CAUSES]--> siege-of-storms-end-300` — **DARK** (the one causal edge that matters).
3. **DEDUP CHECK at build:** `siege-of-storms-end-300` vs `taking-of-storms-end`. `taking-of-storms-end` is the *Stannis* taking (WO5K, OUT). `siege-of-storms-end-300` is the Tyrell→GC siege (IN). Confirm the GC's Storm's End action attaches to `siege-of-storms-end-300`, NOT `taking-of-storms-end`.
4. **Container retags:** all 6 takings + siege → add `[aegon]` (most are currently untagged; siege → `[aegon, wo5k]`).

**Upstream attach-point:** `landing-of-the-golden-company` (HIT). **Terminus:** `siege-of-storms-end-300` (HIT, seam).

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 1 | 2 | 1 | 1 | 2 | 2 | **9/12** |

**Verdict: MEDIUM-HIGH VALUE, VERY LOW COST.** C=1 because most of the structure is *correctly* PART_OF, not CAUSES — the causal load is concentrated in a single landing→siege edge. B=2 (zero new mints; the work is 1 CAUSES edge + container retags + a dedup check). Score is held down by C and X, but the cost is near-zero and it makes the entire 6-node fan causally reachable from the spine. Build right after A2.

---

### A4. KL Endgame: Varys Assassinates Pycelle + Kevan (the cross-container attach)

**Description:** In the ADWD epilogue, Varys murders Grand Maester Pycelle and then Lord Regent Kevan Lannister (crossbow + the children's daggers, adwd-epilogue:269–305). His explicit motive ties directly into the AEGON campaign: "Doubt, division, and mistrust will eat the very ground beneath your boy king, whilst Aegon raises his banner above Storm's End and the lords of the realm gather round him" (epilogue:293). This is the AEGON container's reach into the already-built KL endgame (Kevan's regency, the Cersei-Tommen-Tyrell reconciliation Kevan was engineering).

**Anti-signal check:** Genuine CAUSES/MOTIVATES. Kevan was *succeeding* at stabilizing the realm under Tommen (reconcile Highgarden + Casterly Rock, bind the Faith) — which would *defeat* Aegon's chaos-dependent invasion. Varys kills him *because of* Aegon's campaign. Real consequence: the assassinations MOTIVATED-BY the landing/siege; they CAUSE the collapse of Tommen's regency. Strong C.

**Agency-collapse check:** Low — Varys is a single agent in a single scene. Model:
- `landing-of-the-golden-company --[MOTIVATES]--> assassinations-of-pycelle-and-kevan-lannister` (Varys acts to clear Aegon's path; the landing is the *reason*)
- `varys AGENT_IN assassinations...` ; `kevan-lannister VICTIM_IN ...` ; `pycelle VICTIM_IN ...` (role edges, all currently DARK)
- ATTACH (not rebuild) to the KL endgame: the assassinations terminate the Kevan-regency thread. If a `kevan-named-regent` / Cersei-trial node exists in the KL build, an ENABLES/CAUSES edge can wire the attach — verify at build; do NOT re-model KL politics.

**Missing beats:**
1. **NO new event mint** — `assassinations-of-pycelle-and-kevan-lannister` exists (just 0 causal + 0 role edges).
2. The MOTIVATES edge from the landing — **DARK**.
3. Role edges (AGENT_IN varys, VICTIM_IN kevan/pycelle) — **DARK** (the node has *no* role edges at all currently — surprising for a tier-1 event; flag at build).
4. Slug fix: VICTIM target is **`pycelle`**, not `grand-maester-pycelle`.

**Upstream attach-point:** `landing-of-the-golden-company` (HIT) — Varys's motive cites the landing/Storm's-End. **Terminus:** `assassinations-of-pycelle-and-kevan-lannister` (HIT) + ATTACH to KL-endgame characters.

**Container tags:** `assassinations...` → `[aegon]` (already). The attach edges to KL nodes carry `[aegon]` provenance; do not retag KL nodes into aegon.

| Q | S | X | C | B | G | Total |
|---|---|---|---|---|---|-------|
| 2 | 2 | 1 | 2 | 2 | 2 | **11/12** |

**Verdict: HIGHEST VALUE.** "Why did Varys kill Kevan?" is a canonical dip query that fails today (the node has 0 incoming edges). B=2 (no mint; only edges). The cross-container attach is the payoff of the whole container. X=1 (Kevan's POV epilogue; Varys; the threat is realm-wide but POV-narrow). Build after A2 so the landing is causally live as the MOTIVATES source.

---

## 4. Sequence-Only Traps (SKIP/DEFER)

| Juncture | Why Skip/Defer |
|----------|---------------|
| **CAUSES edges between sibling takings** (griffins-roost → crows-nest → rain-house, etc.) | SKIP. The takings were *simultaneous* (three columns set off at once; Greenstone was an accident). PART_OF landing is the correct and complete structure. CAUSES between siblings = granularity overclaim (the NORTH §4 Wall-sub-beats trap). |
| **`taking-of-griffins-roost` 4 SUB_BEAT_OF children** (ram-assault, defenders-killed, maester-killed, prisoners-gathered) | DEFER/SKIP. SUB_BEAT_OF is already correct granular scaffolding. Do NOT add CAUSES between these sub-beats — PRECEDES/SUB_BEAT_OF covers ordering. The causal value is the parent taking, not its blow-by-blow. |
| **Connington's greyscale progression** | NOT a juncture. A character-state CONDITION (slow death-clock) that MOTIVATES his haste. Model as jon-connington node prose, not an event chain. Harvest the two grounding quotes. |
| **The broken Volantis/Yunkai contract as its own node** | SKIP. It's a *non-decision* ("I would think on it"). Fold into A2's `golden-company-sails-for-westeros` as a qualifier/prose, not a separate event node. |
| **Aegon's legitimacy / "mummer's dragon" / Blackfyre theory** | HARD SKIP from the causal map. Route to the GATED theories track. Never a causal node or edge. The two `Aegon-son-of-Rhaegar` nodes are an identity question, not a campaign event. |
| **Daenerys / Meereen cross-theater** | SKIP. The `landing PRECEDES wedding-of-hizdahr...` edge is a likely-bad cross-theater edge (FLAG for deletion at build). Do NOT model Aegon↔Dany convergence here — that is a separate (TWOW) thread. |
| **Battle of Storm's End outcome / Aegon's later TWOW campaign** | DEFER (TWOW). The container terminates at `siege-of-storms-end-300` (the siege launches) and the assassinations (the KL chaos seed). Do not model the unwritten resolution. |
| **Stone-men-attack-the-shy-maid as a causal node** | KEEP as scaffolding only. It's AEGON-internal color (the greyscale infection vector) but has no clean outgoing causal edge into the campaign. Tag `[aegon]`, leave its rich role edges, do NOT force a CAUSES into the reveal. |

---

## 5. Ranked Build Order

Priority = cheapest real cause first, clean attach + terminus, extends/lights a built chain. Every top juncture here is **edge-cheap** (1 mint total across the top 3) because the AEGON scaffolding already exists — the container just needs causal wiring.

### Rank 1 — A2: Golden Company Sails West → Landing (spine ignition)

**Why first:** Highest score (11/12), B=2, and it is the single edge that makes the entire 6-node Stormlands fan causally reachable. 1 mint + 2–3 edges. Clean attach (A1 reveal upstream — but A2 can also attach directly to the landing even before A1, making it the most independent high-value build).

- Mint: `golden-company-sails-for-westeros` (event.incident; adwd-the-lost-lord-01:215–223)
- Wire: `golden-company-sails-for-westeros --[CAUSES]--> landing-of-the-golden-company`
- Wire: `aegon-targaryen-young-griff --[MOTIVATES]--> golden-company-sails-for-westeros` (his "sail west" decision)
- Optional: `tyrion-lannister --[MOTIVATES]--> golden-company-sails-for-westeros` (the goad)
- Scope: ~40 min. Attach: (A1 reveal) / self-rooted. Terminus: `landing` (HIT). Tag `[aegon]`.

### Rank 2 — A4: Varys Assassinations → KL Endgame Attach (the payoff)

**Why second:** 11/12, B=2 (zero mints — node exists), and it is the cross-container payoff. The `assassinations` node has 0 incoming edges AND no role edges — wiring it is pure value. Resolves the "why did Varys kill Kevan?" dip query.

- Wire: `landing-of-the-golden-company --[MOTIVATES]--> assassinations-of-pycelle-and-kevan-lannister` (Varys's motive, epilogue:293)
- Wire role edges: `varys AGENT_IN` / `kevan-lannister VICTIM_IN` / `pycelle VICTIM_IN` assassinations
- ATTACH (verify at build): assassinations → KL-endgame terminus (Kevan-regency / Cersei-trial node if present) via CAUSES/ENABLES
- **Slug fix:** target is `pycelle` (NOT `grand-maester-pycelle`)
- Scope: ~40 min. Attach: `landing` (HIT once Rank 1 lands, but the MOTIVATES works regardless). Terminus: `assassinations` (HIT). 0 mints + ~4 edges.

### Rank 3 — A3: Landing → Stormlands Campaign → Siege of Storm's End (light the fan)

**Why third:** 9/12 but VERY low cost (0 mints; the takings + siege all exist). One CAUSES edge + retags makes 7 existing nodes causally reachable. B=2.

- Wire: `landing-of-the-golden-company --[CAUSES]--> siege-of-storms-end-300`
- Wire: `jon-connington --[MOTIVATES]--> siege-of-storms-end-300` (the war-council decision)
- **DEDUP:** confirm GC Storm's End attaches to `siege-of-storms-end-300`, NOT `taking-of-storms-end` (Stannis/WO5K)
- Retag: 6 takings → add `[aegon]`; `siege-of-storms-end-300` → `[aegon, wo5k]`; `stone-men-attack-the-shy-maid` → `[aegon]`
- **DO NOT** add CAUSES between sibling takings (granularity overclaim)
- Scope: ~30 min. Attach: `landing` (HIT). Terminus: `siege-of-storms-end-300` (HIT, seam).

### Rank 4 — A1: Conspiracy Seed → Aegon Revealed (root the spine)

**Why fourth:** 10/12, but slightly higher cost (1 mint + 1 dyad + parked WITNESS_IN) and it roots the spine *backward* from where the query-value lives (A2/A4). Build after the spine is live so the reveal has a downstream to attach to.

- Mint: `aegon-revealed-to-the-golden-company` (event.incident; adwd-the-lost-lord-01:127)
- Dyad: `varys CONSPIRES_WITH illyrio-mopatis` (symmetric, tier-2/3, cite agot-arya-03:89/93)
- Wire: `<conspiracy/dyad> --[MOTIVATES]--> aegon-revealed-to-the-golden-company` (Aegon raised → revealed) — attach the MOTIVATES from a character node (varys/illyrio) since there is no conspiracy event node
- Wire: `aegon-revealed-to-the-golden-company --[TRIGGERS]--> golden-company-sails-for-westeros` (A2's mint)
- PARK: `arya-stark WITNESS_IN <conspiracy>` — no node target; remains parked (per dyad decision)
- Scope: ~45 min. Attach: dyad on varys/illyrio. Terminus: A2 mint. Tag reveal `[aegon]`.

### Build-step 0 (housekeeping, do at start of build session, NOT this dip)
- Fix the **edge bug**: re-parent / dual-tag the 2 mis-filed `PART_OF war-of-the-five-kings` rows (landing + assassinations). Leave `assassination-of-tywin-lannister PART_OF war-of-the-five-kings`.
- Delete the **suspicious** `landing PRECEDES wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` cross-theater edge.

---

## 6. Cross-Container Attach-Points + Seams Map

| Arc | Upstream Attach | Downstream Terminus | Attach status | Container tag |
|-----|----------------|---------------------|---------------|---------------|
| A1: Conspiracy → reveal | `varys`/`illyrio-mopatis` (dyad) | `aegon-revealed-to-the-golden-company` (new) | chars HIT; reveal MISS | reveal `[aegon]` |
| A2: GC sails west | `aegon-revealed...` (A1) | `landing-of-the-golden-company` (HIT) | landing HIT; sail MISS | `[aegon]` |
| A3: campaign → siege | `landing-of-the-golden-company` (HIT) | `siege-of-storms-end-300` (HIT, seam) | both HIT | `[aegon]` / siege `[aegon,wo5k]` |
| A4: Varys assassinations | `landing-of-the-golden-company` (HIT) | `assassinations-of-pycelle-and-kevan-lannister` (HIT) → KL endgame chars | both HIT | `[aegon]` |

**Cross-container seams (ATTACH, never rebuild):**
1. **`siege-of-storms-end-300`** — AEGON ∩ WO5K. The Tyrell siege (Cersei removes Mace from KL, AFFC) is WO5K-owned scaffolding; the GC inherits/contests it (ADWD). Dual-tag `[aegon, wo5k]`. The GC's action attaches *to* this node — do not mint a separate "GC besieges Storm's End".
2. **`assassinations-of-pycelle-and-kevan-lannister`** — AEGON ∩ KL-endgame. AEGON-owned node; ATTACHES to `kevan-lannister`, `pycelle`, `cersei-lannister` and (if present) the Kevan-regency / Cersei-trial KL-endgame node. Verify those KL nodes at build; wire CAUSES/ENABLES, do NOT re-model the KL regency.
3. **`taking-of-storms-end`** (Stannis, WO5K) — NOT a seam. Pure WO5K decoy. Keep OUT; ensure A3 does not accidentally wire to it.
4. **The Dany/Meereen theater** — NOT a seam in this container. The `landing PRECEDES hizdahr-wedding` edge is a likely-bad cross-theater artifact to delete, not a real bridge.

### Dyad decision (D1) — full justification

**Recommendation: dyad-only. Do NOT mint `varys-and-illyrio-conspire-in-the-tunnels`.**

Per the S117 edge-vs-node rule (in dyad-queue D1): the tunnel meeting becomes its own event node ONLY if the *seeing* (Arya's witness) or the meeting itself gets an outgoing causal edge. It does not:
- Arya's witnessing → Ned's downfall is 4–5-decisions-mediated (agency-collapse). No causal edge.
- The *content* of the conspiracy (raise Aegon) is better attached as a `MOTIVATES` from the **character** nodes (varys/illyrio) onto **A1's reveal node**, which already exists as a clean anchor. The reveal node IS the downstream attach-point A1 needs — so the conspiracy meeting does NOT need to be minted as a separate anchor.

Therefore: `varys CONSPIRES_WITH illyrio-mopatis` (dyad on the two character nodes, cite agot-arya-03:89/93) carries the relationship; `arya-stark WITNESS_IN <meeting>` stays **parked** (no node target) — and may stay parked permanently, since the AEGON spine roots fine on the reveal node without a tunnel-meeting anchor. This keeps the AGOT seed in the graph (as a character dyad + a harvest quote) without minting a thin event node that no causal edge would use.

---

## 7. Nodes to Mint (Summary Table)

Required across the ranked top-4 arcs:

| Node to Mint | Slug | Type | Source | For Juncture | Container Tag |
|---|---|---|---|---|---|
| Golden Company sails for Westeros | `golden-company-sails-for-westeros` | event.incident | adwd-the-lost-lord-01:215–223 | A2 (Rank 1) | `[aegon]` |
| Aegon revealed to the Golden Company | `aegon-revealed-to-the-golden-company` | event.incident | adwd-the-lost-lord-01:127 | A1 (Rank 4) | `[aegon]` |

**TOTAL NODES TO MINT = 2.**

**Dyad to build (not a node):**
- `varys CONSPIRES_WITH illyrio-mopatis` (A1) — 1 symmetric edge on existing character nodes.

**Nodes that EXIST but need causal/role wiring (not mints):**
- `landing-of-the-golden-company` → incoming CAUSES from `golden-company-sails-for-westeros` (A2); outgoing CAUSES to `siege-of-storms-end-300` (A3); outgoing MOTIVATES to `assassinations...` (A4)
- `assassinations-of-pycelle-and-kevan-lannister` → incoming MOTIVATES from landing; role edges AGENT_IN `varys`, VICTIM_IN `kevan-lannister`, VICTIM_IN `pycelle` (A4)
- `siege-of-storms-end-300` → incoming CAUSES from landing; MOTIVATES from `jon-connington` (A3)
- 6 takings + `stone-men-attack-the-shy-maid` → container retags `[aegon]` (A3)

**Dedup / fix checks required (run before/at build):**
- `siege-of-storms-end-300` (IN) vs `taking-of-storms-end` (Stannis/WO5K, OUT) — attach GC siege to the **-300** node.
- Slug: VICTIM target is **`pycelle`** (NOT `grand-maester-pycelle`).
- Aegon slug: all new edges target **`aegon-targaryen-young-griff`** (NOT `aegon-targaryen-son-of-rhaegar`, the historical infant).
- Edge bug: 2 mis-filed `PART_OF war-of-the-five-kings` rows (landing + assassinations).
- Suspicious edge: delete `landing PRECEDES wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen`.

---

## 8. Harvest Queue Additions

*(Collected incidentally during AEGON wiki + graph + chapter investigation — POINTED into `working/harvest-queue.md`, append-only. POINT, don't extract.)*

| status | kind | book | ref | note | session |
|--------|------|------|-----|------|---------|
| open | quote | agot | sources/chapters/agot/agot-arya-03.md:79 | Varys (torchbearer) in the tunnels: "I warn you, the wolf and lion will soon be at each other's throats, whether we will it or no." — AGOT conspiracy-seed, evidence for `varys CONSPIRES_WITH illyrio-mopatis` dyad (A1) | 2026-06-22 aegon-dip |
| open | quote | agot | sources/chapters/agot/agot-arya-03.md:93 | Illyrio (forked beard): "The princess is with child. The khal will not bestir himself until his son is born." — the Targaryen-restoration timeline seed; A1 dyad evidence | 2026-06-22 aegon-dip |
| open | quote | adwd | sources/chapters/adwd/adwd-the-lost-lord-01.md:127 | Connington reveals the prince: "My lords, I give you Aegon Targaryen, firstborn son of Rhaegar… soon, with your help, to be Aegon, the Sixth of His Name." — Tier-1 anchor for `aegon-revealed-to-the-golden-company` (A1) | 2026-06-22 aegon-dip |
| open | quote | adwd | sources/chapters/adwd/adwd-the-lost-lord-01.md:217 | Aegon: "If my aunt wants Meereen, she's welcome to it. I will claim the Iron Throne by myself… Move fast and strike hard." — the sail-west decision; Tier-1 anchor for `golden-company-sails-for-westeros` (A2) | 2026-06-22 aegon-dip |
| open | quote | adwd | sources/chapters/adwd/adwd-the-griffin-reborn-01.md:173 | Connington: "We did not cross half the world to wait… I mean to take Storm's End. A nigh-impregnable stronghold, and Stannis Baratheon's last foothold in the south." — A3 siege-decision evidence for `siege-of-storms-end-300` | 2026-06-22 aegon-dip |
| open | description | adwd | sources/chapters/adwd/adwd-the-lost-lord-01.md:237 | Connington's greyscale revealed: "The nail on his middle finger had turned as black as jet… the grey had crept up almost to the first knuckle." — character-state condition for jon-connington node (death-clock that MOTIVATES his haste) | 2026-06-22 aegon-dip |
| open | description | adwd | sources/chapters/adwd/adwd-the-griffin-reborn-01.md:141 | Connington hides his greyscale with vinegar/wine soaks: "men who would cheerfully face battle… would abandon that same companion in a heartbeat if he were known to have greyscale." — jon-connington condition + foreshadowing | 2026-06-22 aegon-dip |
| open | quote | adwd | sources/chapters/adwd/adwd-epilogue.md:281 | Varys to dying Kevan: "Forgive me if you can. I bear you no ill will. This was not done from malice. It was for the realm. For the children." — A4 evidence, Varys AGENT_IN assassinations | 2026-06-22 aegon-dip |
| open | quote | adwd | sources/chapters/adwd/adwd-epilogue.md:293 | Varys's motive: "Doubt, division, and mistrust will eat the very ground beneath your boy king, whilst Aegon raises his banner above Storm's End and the lords of the realm gather round him." — the load-bearing AEGON↔assassinations seam; A4 MOTIVATES edge evidence | 2026-06-22 aegon-dip |
| open | quote | adwd | sources/chapters/adwd/adwd-epilogue.md:297 | Varys's Aegon-upbringing speech: "Aegon has been shaped for rule since before he could walk… Tommen has been taught that kingship is his right. Aegon knows that kingship is his duty." — the conspiracy's payoff; A1 MOTIVATES (conspiracy → Aegon raised) evidence | 2026-06-22 aegon-dip |
| open | description | adwd | sources/chapters/adwd/adwd-the-lost-lord-01.md:61 | Aegon's disguise/appearance: "hair washed and cut and freshly dyed a deep, dark blue… three huge square-cut rubies on a chain of black iron, a gift from Magister Illyrio. Red and black. Dragon colors." — physical description for aegon-targaryen-young-griff | 2026-06-22 aegon-dip |
| open | food | adwd | sources/chapters/adwd/adwd-the-griffin-reborn-01.md:135 | Connington breaks his fast at reclaimed Griffin's Roost: "Boiled eggs, fried bread, and beans. And a jug of wine. The worst wine in the cellar." (the wine is for greyscale vinegar-soaks, not drinking) — hospitality/food + greyscale detail | 2026-06-22 aegon-dip |
