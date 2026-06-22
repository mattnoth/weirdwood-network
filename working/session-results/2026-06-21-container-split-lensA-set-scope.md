# Container-Split Lens A — Set + Scope
**Date:** 2026-06-21 (S121 fan-out) · **Lens:** A (set + scope) · **Method:** live graph queries + decomposition doc review + foreshadowing-events.md mapping · **Scope:** read-only

---

## 1. Is {essos, wo5k, north, aegon} sufficient?

**Short answer: Yes, the 4-container set is the right spine for greenfield build work.** The proposal's recommendation to add `riverlands` and `kl-faith` now is premature and creates naming-before-building churn. Here is the evidence-based breakdown.

### What the live graph shows

- `--container essos` → 16 nodes (E1–E5 built, causally wired)
- `--container wo5k` → 2 nodes (`robert-orders-daenerys-assassination` + `littlefinger-betrays-ned`); the WO5K spine arcs (B1/B2/B3/Purple-Wedding/Blackwater/Tywin) are **untagged standalones** right now
- No containers exist yet for `north`, `aegon`, `riverlands`, `kl-faith`, `iron-islands`, `dorne`

The only two truly active containers with built content are ESSOS and WO5K. The rest are naming proposals pending decomp + build work.

### Why `riverlands` is a sub-thread, not a container

The proposal classifies events 15 (Stoneheart reveal) and 19 (Brienne's "death") as `riverlands`. Live graph check:

- `catelyn-rises-as-lady-stoneheart` → 1 downstream CAUSES → `brienne-brought-before-lady-stoneheart` → 0 outgoing. That is 2 wired nodes with a 1-hop chain — not a container; it's a WO5K tail.
- The Stoneheart thread's upstream is the Red Wedding (`catelyn-is-killed` is immediately above it). That root is `[wo5k]`.
- Arya's Riverlands wandering and the Brotherhood have no built causal arc at all — no root, no junctures, no decomp doc.
- **Verdict:** `riverlands` is a real GRRM geographic cluster but NOT container-sized yet. It has ≤3 built nodes with 1 causal hop. Tag these as `[wo5k]` for now (Stoneheart is a direct consequence of the Red Wedding) and revisit `riverlands` only after the Brotherhood arc gets a decomp dip and 4+ junctures.

### Why `kl-faith` is a dependency, not a container

The `kl-faith` thread — Cersei rearms the Faith → Cersei's plot against Margaery → Osney confesses → Cersei arrested → stripped — is 4 causally wired nodes (`cersei-rearms → cersei-is-captured-in-the-sept → cersei-is-stripped-and-imprisoned`, with the `cersei-plots-against-margaery` branch adding 2 more). That is a real 5-node arc (event #17).

**BUT:** `--causal-chain cersei-is-stripped-and-imprisoned` shows its upstream roots in `death-of-joffrey-baratheon` via the Tyrion trial → Gregor confesses chain. The kl-faith thread is downstream of the Purple Wedding (`wo5k`). It is structurally a **downstream branch of WO5K**, not a standalone theater. Naming it a separate container now — before even building Cersei's walk of shame or the High Sparrow's broader arc (ADWD/TWOW territory) — would fragment a thread that naturally belongs to `[wo5k]` retro-tagging.

- **Verdict:** Tag the built AFFC #1 arc as `[wo5k]` on the Lens D retro-grouping pass. If the Faith Militant arc gets a full decomp dip and spawns 6+ independent junctures, reconsider naming `kl-faith` then.

### Why `iron-islands` is a micro-container, not a standalone container

`death-of-balon-greyjoy --full-chain` yields 8 chain edges through `kingsmoot → taking-of-shields → euron-commissions-victarion`. That is container-adjacent in depth, BUT:
- The chain terminates directly into ESSOS (Victarion goes to fetch Dany)
- The chain roots in no causal upstream (Balon dies as a standalone prime mover)
- All nodes exist; no greenfield decomp dip needed

This is a **small, complete causal arc** (AFFC #2), not a growing container. Tag it `[essos]` at the seam node (`euron-commissions-victarion-to-fetch-daenerys`) and `[wo5k]` for Balon's death (which is a WO5K-adjacent prime mover). No `iron-islands` tag needed.

### Why `dorne` is the same as `iron-islands`: a complete sub-arc, not a container

`the-queenmaker-plot → areo-hotah-springs-the-ambush → arianne-collapses-and-is-captured → doran-reveals-fire-and-blood-pact → death-of-quentyn-martell (ESSOS)` — 5 nodes, all built or queued. The Dorne thread's natural terminus is `death-of-quentyn-martell` which belongs to ESSOS (E5). Like iron-islands, this is a **sub-arc that terminates into an existing container**, not a new theater. Tag AFFC #4 arc nodes as `[essos]` at the seam.

### Conclusion on container SET

**Adopt {essos, wo5k, north, aegon} as the 4-container spine.** Do not name `riverlands`, `kl-faith`, `iron-islands`, or `dorne` as containers now. The AFFC floating arcs (AFFC #1/#2/#3/#4) all naturally fold into existing containers on the Lens D retro-pass:
- AFFC #1 (Cersei/Faith) → `[wo5k]`
- AFFC #2 (Kingsmoot/Euron) → `[wo5k, essos]` (seam at `euron-commissions-victarion`)
- AFFC #3 (Brienne/Stoneheart) → `[wo5k]`
- AFFC #4 (Dorne/Queenmaker) → `[essos]` (seam at `doran-reveals-fire-and-blood-pact` and `death-of-quentyn-martell`)

---

## 2. The 30 Foreshadowed Events → Container Mapping

Ground rule: "built" means a causal node exists for this event (not just a `node.md` file, but causal edges wired or a node with role edges that can become a juncture). "Dark" = node exists with 0 causal edges. "MISS" = no event node exists.

| # | Event | Recommended container(s) | Node status |
|---|-------|--------------------------|-------------|
| 1 | Jon Arryn's murder | **standalone** (`null`) — Littlefinger backstory; inciting cause of everything but belongs to no single causal container | no event node |
| 2 | Bran's fall | **standalone** (`null`) or `[bran]` if Bran gets tagged — already a built arc | built (standalone) |
| 3 | Ned's execution | `[wo5k]` — core B3 arc | built ✅ |
| 4 | Robert's death | `[wo5k]` — root | built ✅ |
| 5 | Drogo's death / Dragon birth | `[essos]` — E1 | built ✅ |
| 6 | Catelyn seizes Tyrion | `[wo5k]` — war trigger | partial (1 CAUSES outgoing) |
| 7 | Battle of the Blackwater | `[wo5k]` — built downstream; upstream dark | partial ✅ |
| 8 | Theon takes Winterfell | `[wo5k, north]` — WO5K-owned seam | dark (`capture-of-winterfell` has 0 causal) |
| 9 | House of the Undying visions | `[essos, aegon]` — cloth dragon = fAegon; cross-cut | no causal event node (the vision is Dany's POV experience, not a causal event currently modeled) |
| 10 | Renly's death | `[wo5k]` — upstream of Blackwater | dark (`shadow-assassination-of-renly` exists, 0 causal) |
| 11 | Red Wedding | `[wo5k]` — B1 | built ✅ |
| 12 | Purple Wedding | `[wo5k]` — built | built ✅ |
| 13 | Oberyn vs. the Mountain | `[wo5k]` — trial cascade that causes Cersei to rearm | `gregor-confesses-and-kills-oberyn` is HIT with CAUSES outgoing ✅ |
| 14 | Tyrion kills Tywin | `[wo5k]` | `assassination-of-tywin-lannister` built ✅ |
| 15 | Stoneheart reveal | `[wo5k]` (NOT a separate `riverlands` tag; upstream is Red Wedding) | `catelyn-rises-as-lady-stoneheart` built, 1 CAUSES out ✅ |
| 16 | Jon becomes Lord Commander | `[north]` (or `[north, jon]` per Lens B) | MISS — no event node |
| 17 | Cersei's arrest by the Faith | `[wo5k]` (kl-faith is a downstream WO5K branch) | `cersei-is-captured-in-the-sept` built ✅ |
| 18 | Pate's murder / Jaqen at Citadel | **standalone** (`null`) — Faceless Men; no causal attach to any container | no event node |
| 19 | Brienne's "death" | `[wo5k]` (Stoneheart is WO5K downstream; no separate `riverlands`) | `brienne-brought-before-lady-stoneheart` built, 0 outgoing |
| 20 | Euron's Kingsmoot | `[essos]` (seam: Victarion → Essos spine) — NOT `iron-islands` | `kingsmoot-on-old-wyk` built ✅ |
| 21 | Jon's assassination | `[north]` (or `[north, jon]`) | `jon-is-stabbed-repeatedly` EXISTS, 0 causal in/out |
| 22 | Dany rides Drogon / escapes | `[essos]` — E3 | built ✅ |
| 23 | Aegon's landing | `[aegon]` | `landing-of-the-golden-company` EXISTS; `aegons-landing` EXISTS — both DARK (0 causal) |
| 24 | Stannis marches on Winterfell | `[wo5k, north]` — seam | MISS — no event node |
| 25 | Varys assassinates Kevan | `[aegon]` — explicit AEGON motivation (clear the path for Aegon) | MISS — no event node |
| 26 | Quentyn's death | `[essos]` — E5 | `death-of-quentyn-martell` built ✅ |
| 27 | Manderly's Frey pies | `[north]` | `wyman-manderly-stages-fake-execution-of-davos` EXISTS (WO5K-adjacent staging, 0 causal); no Frey-pies event node |
| 28 | R+L=J | **standalone** (`null`) — cross-book revelation; fits no single container | no event node |
| 29 | The Others' true nature | **standalone** (`null`) — deep-lore, not a causal arc | no event node |
| 30 | Doom of Valyria | **standalone** (`null`) — pre-series deep-lore | no event node |

**Summary:**
- `[essos]`: 5, 9 (partial), 20, 22, 26 + Quentyn thread (Dorne seam)
- `[wo5k]`: 3, 4, 6, 7, 11, 12, 13, 14, 15, 17, 19
- `[wo5k, north]` (seams): 8, 24
- `[north]`: 16, 21, 27
- `[aegon]`: 23, 25 + HotU fAegon cross-cut (9)
- **Genuine standalones** (`null`): 1, 2 (or `[bran]`), 18, 28, 29, 30 — **6 events**

---

## 3. NORTH — Scope

### Boundary (in / out)

**In:** The Night's Watch politics + Jon's arc (election → wildling diplomacy → assassination); the Mance Rayder/wildling invasion; Stannis-at-the-Wall and the Stannis-marches-on-Winterfell sequence; the Grand Northern Conspiracy (Manderly, faux-Davos execution, Frey pies); the Bolton-held-Winterfell situation (Ramsay/Jeyne, ADWD Bolton chapters). The capture-of-winterfell and sack-of-winterfell carry `[wo5k, north]` (dual-membership, WO5K-owned).

**Out:** The Others/White Walkers themselves (in-text presence too sparse through ADWD to form a causal arc — they are a looming condition, not a built sequence); Bran's greensight arc (different theater — see §3 boundary collision note); Jon's parentage / R+L=J (standalone, not a NORTH causal event).

### Spine root + terminus

- **Root (causal):** No clean single upstream anchor exists. The closest is `robb-proclaimed-king-in-the-north` (WO5K-BUILT, `execution-of-eddard-stark CAUSES`), which is where the North's political POV diverges from WO5K. Practically, declare NORTH's build root at a new node: **`jon-joins-the-nights-watch`** (event.incident; AGOT Jon V — when Jon takes his vows; this is the point where Jon's thread becomes independent of WO5K). Alternatively, the Watch's own prime mover is **`deserter-beheaded-by-ned`** (AGOT prologue/Bran I — the deserter whom Ned beheads is a Watch member fleeing the Others; this is the first in-saga NORTH beat). Check: this node may or may not exist.

  > **Node check for `deserter-beheaded-by-ned`:** MISS on lookup. The prologue deserter is named Will (killed by White Walkers before Ned), and Gared (beheaded by Ned). A node for this event would be: `ned-beheads-the-deserter` (event.execution; AGOT Bran I). Needs mint if used as spine root.

- **Terminus (ADWD):** `jon-is-stabbed-repeatedly` (HIT — exists, 0 causal) — this IS the published terminus for the NORTH arc through ADWD.

### 6 Candidate Junctures with Build-Readiness Notes

**N1. Jon takes the Watch vows** (`jon-joins-the-nights-watch` or similar)
- MISS — no event node
- Build-readiness: Low. Would need a mint. Value: establishes the NORTH thread's divergence from WO5K. Low cost if minted as a simple prime-mover anchor.
- Causal role: standalone prime mover for the Jon sub-thread; connects to Mormont assigning Jon to stewards → Ghost beyond the wall → Fist → etc.

**N2. Battle at the Fist of the First Men** (`battle-of-the-fist-of-the-first-men`)
- HIT — node exists, **COMPLETELY DARK (0 edges of any type)**
- Build-readiness: Medium. Node exists but has zero edges (not even PART_OF). The mass wight attack on the ranging party is a real causal event (triggers the retreat to Craster's Keep → mutiny → Sam's escape). Upstream: Mormont leads the Great Ranging (dark). Downstream: `mutiny-at-castle-black` (HIT, but only 1 PRECEDES incoming from wrong context).
- Causal role: TRIGGERS the Watch's crisis — the Fist disaster forces the retreat that causes the mutiny. Real CAUSES/TRIGGERS chain.

**N3. Mutiny at Castle Black / Craster's Keep** (`mutiny-at-castle-black`)
- HIT — node exists, 0 causal, 1 PRECEDES incoming (from wrong node)
- Build-readiness: Medium. Node exists. This is the Watch mutiny where Mormont is killed — it enables Sam's escape and the ravens. Upstream: Fist of First Men (N2). Downstream: Sam eventually reaches Eastwatch, gets the news to the Watch, triggers the election context.
- Causal role: enables the Lord Commander election storyline. Real causal hinge.

**N4. Jon elected Lord Commander** (no node — MISS)
- MISS — `jon-snow-elected-lord-commander` does not exist under any alias
- Build-readiness: Low (needs mint). The election is event #16 in the foreshadowing list — the key political beat that sets up all of Jon's ADWD decisions and the assassination.
- Causal role: the election creates Jon's authority → his wildling diplomacy → the Shieldhall speech → assassination. Essential spine node.

**N5. Jon opens the gates to the wildlings / Hardhome decision** (no node confirmed)
- MISS on any alias lookup
- Build-readiness: Low (needs mint). Jon's decision to bring surviving wildlings south through the Wall is the immediate political trigger for Watch resentment that builds to the assassination. `cersei-s-plot-to-assassinate-jon-snow` EXISTS but is a Cersei POV event (0 causal in/out); the real decision node needs to be Jon's agency.
- Causal role: MOTIVATES the Watch's opposition → the Shieldhall speech → `jon-is-stabbed-repeatedly`.

**N6. Jon is stabbed repeatedly** (`jon-is-stabbed-repeatedly`)
- HIT — node exists (role edges: Bowen Marsh + Wick + Jon as victim), 0 causal in/out, 1 LOCATED_AT
- Build-readiness: HIGH (node exists, richly citable). Just needs upstream causal wiring from N5 and the Pink Letter ("bastard-letter" artifact exists). The terminus node of the NORTH spine is already in the graph — it just has no upstream.
- Causal role: NORTH terminus (ADWD). TRIGGERS the "man, then wolf, then man again" Melisandre arc into TWOW.

**Additional notes for NORTH build:**
- `wyman-manderly-stages-fake-execution-of-davos` (HIT) is a 4-node SUB_BEAT_OF cluster (0 causal in/out) — buildable as the Grand Northern Conspiracy thread that parallels Jon's Wall arc. Attach upstream from `sack-of-winterfell → north-political-situation` (seam node), downstream to Manderly's Frey pies (event #27, no node yet).
- `battle-of-winterfell` and `battle-outside-the-gates-of-winterfell` (both HIT) are Stannis-arc nodes.
- `queen-s-men-push-stannis-harder-for-sacrifice` (HIT) is a Stannis-encampment sub-beat.

**NORTH build-readiness verdict: near-zero for the spine** — 4 of 6 key junctures are MISS; the 2 existing nodes (Fist + Jon-stabbed) have 0 causal wiring. This is a full decomp-dip session (like Essos was at the start of S119) before any minting begins.

---

## 4. AEGON / Targaryen-Restoration — Scope

### Boundary (in / out)

**In:** The Varys/Illyrio tunnel conspiracy (AGOT, Arya-witnessed — `dyad-queue.md` D1); JonCon + fAegon raised in exile; Golden Company hired; `landing-of-the-golden-company` + `aegons-landing` (both exist, both DARK); the Stormlands campaign (taking-of-griffins-roost + related sub-beats exist); Varys kills Kevan (event #25, MISS). HotU "cloth dragon on poles" vision (event #9 cross-cut) seeds it.

**Out:** Dany's eventual encounter with Aegon (if it happens) — that will be an ESSOS∩AEGON seam. The Golden Company's Blackfyre-lineage theory (candidate `[aegon]` evidence nodes, not causal spine).

### Spine root + terminus

- **Root:** Varys/Illyrio conspire in the tunnels (`varys-and-illyrio-conspire-in-the-tunnels` — no event node yet; dyad-queue D1 says mint this as a light anchor when AEGON is opened, ONLY IF downstream AEGON beats need it as attach point). The practical root for the causal build is likely **`golden-company-contracted-by-illyrio`** or `aegons-landing` directly as a standalone prime mover (similar to how `robert-orders-daenerys-assassination` was declared standalone for Essos E4 rather than chaining back to Robert's birth).
- **Terminus:** `varys-assassinates-kevan-lannister` (event #25 — explicitly: "to clear the path for Aegon"). MISS — no event node. This is the ADWD published terminus for the AEGON thread.

### 5 Candidate Junctures with Build-Readiness Notes

**A1. Varys/Illyrio conspire (AGOT dungeon scene)**
- MISS — no event node (`varys-and-illyrio-conspire-in-the-tunnels` not yet minted; dyad-queue D1)
- Build-readiness: Low (needs mint). Per dyad-queue guidance: only mint if needed as an attach point for downstream AEGON beats. The CONSPIRES_WITH dyad edge on the two character nodes may be sufficient without a full event node.
- Causal role: AEGON spine root / prime mover; establishes the conspiracy as a causal thread.

**A2. Golden Company hired / Young Griff raised in exile**
- No event node found for "Golden Company contracted" or "Aegon raised in exile"
- Build-readiness: Low (needs mint or scoping). The exile years are a background condition, not a dated causal event. The key causal node is probably `golden-company-sails-for-westeros` (ADWD — the departure from Essos that enables the landing).
- Causal role: ENABLES the landing (precondition, not force).

**A3. Landing of the Golden Company / Aegon's Landing** (`landing-of-the-golden-company`, `aegons-landing`)
- Both HIT — both nodes exist
- `landing-of-the-golden-company`: 1 PART_OF outgoing, 8 incoming (mostly PART_OF campaign sub-beats like taking-of-griffins-roost), 1 spurious PRECEDES
- `aegons-landing`: completely DARK (0 edges of any type)
- Build-readiness: HIGH for `landing-of-the-golden-company` (the sub-beats are already in the graph: `taking-of-griffins-roost`, `fall-of-mistwood`, `taking-of-crows-nest`, `taking-of-greenstone`, `taking-of-rain-house`, `invasion-of-tarth`). **This node cluster is the most build-ready in the AEGON container** — 6 sub-beats exist, all as PART_OF edges with 0 causal; needs 1 upstream CAUSES + a few causal arcs through the campaign.
- Causal role: spine mid-point; the landing CAUSES the Stormlands campaign which establishes fAegon's military position.

**A4. Storm's End falls / Stormlands secured** (existence unclear)
- Likely exists as a battle node; needs alias lookup to confirm
  > `python3 scripts/event_alias_resolver.py --lookup "siege of Storm's End"` would clarify, but the sub-beats (`taking-of-griffins-roost` etc.) suggest the Storm's End battle probably has a node.
- Build-readiness: Medium. The Stormlands campaign is well-documented in ADWD JonCon chapters; node may exist; 0 causal likely.
- Causal role: enables Aegon's political legitimacy claim + march northward (or toward KL).

**A5. Varys assassinates Kevan (and Pycelle)**
- MISS — no event node
- Build-readiness: Low (needs mint). The terminus of the AEGON spine as published. Varys's monologue makes the causal reason explicit: the realm must be destabilized to clear the path for Aegon. Real CAUSES logic.
- Causal role: AEGON terminus (ADWD). Mirrors Essos's `dany-lost-on-dothraki-sea` as the published-series endpoint.

**AEGON build-readiness verdict: partially built** at the Stormlands campaign level (6 sub-beat nodes exist); completely dark for the causal chain. The best entry point for AEGON is `landing-of-the-golden-company` → wire the Stormlands sub-beats as causal → declare `varys-kills-kevan` as terminus (needs mint).

---

## 5. Confirming E7 (Varys/Illyrio) Belongs to AEGON

**Confirmed.** `working/dyad-queue.md` D1 explicitly states this, and the live graph supports it:
- `jon-connington` has `RESENTS varys` + `RESENTS illyrio-mopatis` edges — the conspiracy is a JonCon/AEGON-thread character relationship, not an Essos-Daenerys one
- `varys` character node has `ALLIES_WITH illyrio-mopatis` from `adwd-tyrion-03`
- The tunnel scene (agot-arya-03:73–97) is the AGOT seed of the Varys/Illyrio conspiracy that eventually delivers fAegon into Westeros — it has zero causal connection to the Daenerys-Essos thread (Varys is managing her as a *distraction* / timing signal, not as the main beneficiary)
- The proposal's `dyad-queue.md` correctly extracted this from Essos E7 to AEGON

**If the AEGON container needs a causal attach point for the conspiracy**, the right model is: mint `varys-and-illyrio-conspire-in-the-tunnels` (event.conspiracy; agot-arya-03:73) with `containers: [aegon]`, `CONSPIRES_WITH(varys, illyrio)` on both character nodes, and `arya-stark WITNESS_IN` it.

---

## 6. Boundary Collisions

| Collision | Nodes Involved | Resolution |
|-----------|---------------|------------|
| **WO5K ∩ NORTH (Theon/Winterfell)** | `capture-of-winterfell`, `sack-of-winterfell` | WO5K owns the build (ironborn invasion is a WO5K front); NORTH adds its tag. Dual: `[wo5k, north]`. Already documented in `wo5k-decomposition.md`. |
| **WO5K ∩ NORTH (Stannis arc)** | `stannis-marches-on-winterfell` (MISS), `queen-s-men-push-stannis-harder-for-sacrifice` (HIT) | Stannis's WO5K trajectory (Blackwater defeat → Dragonstone → Wall → Winterfell march). His Wall arrival is NORTH-territory; the retreat from Blackwater is WO5K. The seam node is `stannis-retreats-to-dragonstone` (built, WO5K) → new beat `stannis-arrives-at-the-wall` (to mint, NORTH). Ownership: `stannis-retreats-to-dragonstone CAUSES stannis-arrives-at-the-wall` (NORTH-owned). Dual-tag the Wall-arrival + Winterfell-march nodes as `[wo5k, north]`. |
| **ESSOS ∩ AEGON (HotU visions)** | The `House of the Undying` event (#9) shows Dany the fAegon "cloth dragon" vision | This is an ESSOS event (Dany's arc, Qarth) that foreshadows AEGON content. Tag it `[essos, aegon]` if it ever gets a causal event node. The cross-cut is informational (the vision doesn't causally connect to the AEGON thread — it's a foreshadowing of something that already exists as a plan). Lean `[essos]` as primary, add `aegon` as a sub-tag. |
| **WO5K ∩ ESSOS (already stamped)** | `robert-orders-daenerys-assassination` | Stamped `[essos, wo5k]` in S121. WO5K owns the build (Small Council meeting), Essos adds its tag. Working correctly. |
| **ESSOS ∩ AEGON (Dany's eventual Westeros return)** | Not yet built; Dany's march to Westeros is TWOW+ territory | Future collision. When it arrives: the node where Dany commits to invading Westeros (which is the AEGON theater) becomes the seam. ESSOS owns the upstream (she's still in Essos); AEGON adds its tag when she crosses. Defer until built. |
| **WO5K ∩ AEGON (Varys kills Kevan)** | `varys-kills-kevan-lannister` (to mint) | Kevan is a KL political figure (WO5K aftermath); Varys's stated motive is explicitly AEGON. The event is Varys acting for AEGON against the stabilized realm. Own under AEGON; add `wo5k` tag since it's located in KL political space. Dual: `[aegon, wo5k]`. |
| **NORTH ∩ AEGON** | None found yet in the built or MISS state | The proposal noted "thin" overlap. Confirmed thin — no built or obvious seam nodes. The only plausible seam would be if/when Jon Snow's resurrection connects to the AEGON legitimacy question (TWOW territory). Defer. |

---

## 7. Summary Assessment vs. the Proposal

| Claim in proposal | Lens A verdict |
|---|---|
| "6 containers needed: + `riverlands` + `kl-faith`" | **REFUTED.** Both fold into `[wo5k]`. Not container-sized in the current graph. |
| "`iron-islands` or fold into Greyjoy thread" | **Fold into `[essos]`** at seam node. Not a standalone container. |
| "`dorne` or fold" | **Fold into `[essos]`** (Doran's pact thread terminates in Essos E5). |
| "~5 genuine standalones: Jon Arryn, Jaqen/Citadel, R+L=J, Doom of Valyria" | **Confirmed** — these 4 + Bran's fall (or `[bran]`) = 5 standalones. Pate/Jaqen #18 = standalone. |
| "E7 Varys/Illyrio belongs to AEGON" | **Confirmed.** Dyad-queue D1. Evidence from JonCon node edges. |
| "NORTH is greenfield — near-zero readiness" | **Confirmed and strengthened.** 4 of 6 spine junctures MISS; 2 existing nodes have 0 causal wiring. Needs a full decomp dip before any minting. |
| "AEGON partially built at Stormlands level" | **Confirmed.** 6 sub-beat nodes exist under `landing-of-the-golden-company` as PART_OF; `aegons-landing` itself is DARK. Spine root (conspiracy) and terminus (Varys kills Kevan) both MISS. |

---

## Recommendation

**Adopt the 4-container spine: {essos, wo5k, north, aegon}.** Do not name `riverlands`, `kl-faith`, `iron-islands`, or `dorne` as containers — all four fold cleanly into the existing four via Lens D retro-tagging. The proposal's 6-container push would bake in container names for arcs that haven't been decomped and might never grow to independent container size. The 4-container rule also keeps `--container` queries meaningful: a `--container riverlands` returning 2 nodes alongside a `--container wo5k` returning 40+ would be misleading asymmetry.

Build priority once the set is settled: NORTH (greenfield, full decomp dip needed) is the biggest gap. AEGON is partially seeded (Stormlands sub-beats exist) and a shorter path to first wired nodes. WO5K has outstanding junctures (J2+J9 Blackwater upstream) that are the highest-salience built-arc completions. Start WO5K-remainder while the NORTH decomp dip is being written.
