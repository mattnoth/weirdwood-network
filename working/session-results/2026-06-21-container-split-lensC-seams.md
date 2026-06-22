# Lens C — Seams + Dual-Membership (container-split pressure-test)

> **Assigned lens:** C — seams + dual-membership
> **Date:** 2026-06-21 (S121 fan-out)
> **Method:** Independent read-only graph analysis. All claims grounded against the live graph via
> `graph-query.py --neighbors`, `--causal-chain`, and `event_alias_resolver.py --lookup`.
> Source docs read: `working/wo5k-decomposition.md`, `working/essos-decomposition.md`,
> `working/dyad-queue.md`, `reference/architecture.md`, the proposal, the advisory board report.
> **Not echoing the proposal.** Findings are independently derived.

---

## Part 1 — Complete Seam Inventory

A **seam** is a node (or cluster) that belongs to two or more containers. A **bridge** is a seam that also
has causal edges *crossing* the container boundary — i.e. a CAUSES/TRIGGERS/ENABLES/MOTIVATES edge whose
source and target belong to different containers. A pure seam shares no causal edge crossing the boundary;
it is just claimed by both.

### Seam 1 — `robert-orders-daenerys-assassination`  [WO5K ∩ ESSOS]

| Field | Value |
|-------|-------|
| **Slugs** | `robert-orders-daenerys-assassination` |
| **Containers** | `[wo5k, essos]` |
| **Built?** | YES — verified `containers: [essos, wo5k]` on disk |
| **Live causal state** | CAUSES → `the-wine-merchant-attempts-to-poison-dany` (outgoing, wired S119); CAUSES → `ned-orders-daenerys-s-assassination-cancelled` (wired S119); **upstream: standalone root** (Robert's order precedes his death — no causal edge from `death-of-robert-baratheon` to this node) |
| **Seam type** | **BRIDGE** — causal edges cross from WO5K (Robert's Small Council, his political domain) into Essos (the prime mover of Dany's spine). The CAUSES edge from this node → wine-merchant-attempt crosses the container boundary. |
| **Note** | The proposal calls this "standalone prime mover." More precise: it is the **join point** between the two biggest containers. It was built once, correctly dual-tagged. |

---

### Seam 2 — `capture-of-winterfell` / `sack-of-winterfell`  [WO5K ∩ NORTH]

| Field | Value |
|-------|-------|
| **Slugs** | `capture-of-winterfell`, `sack-of-winterfell` |
| **Containers** | should be `[wo5k, north]` — currently NO containers tag (neither node has frontmatter `containers:`) |
| **Built?** | Nodes EXIST; causal state DARK. `capture-of-winterfell`: 2 outgoing (PART_OF war, PRECEDES sack), 2 incoming (PRECEDES ← battle-outside-gates, SUB_BEAT_OF ← ser-rodrik-offers-himself). `sack-of-winterfell`: 3 outgoing (LOCATED_AT, PART_OF, PRECEDES → purple-wedding), 12 incoming — all role/structural, 0 causal. |
| **Causal chain result** | `--causal-chain capture-of-winterfell` = 0 upstream, 0 downstream. `--causal-chain sack-of-winterfell` = same. Both are causally isolated. |
| **Seam type** | **SEAM (not yet a bridge)** — the ironborn invasion is the WO5K front that produces these events; Winterfell's political aftermath is NORTH territory. Once the ironborn-invasion causal arc (WO5K J4) is built, `capture-of-winterfell` becomes a bridge because it will carry an upstream WO5K CAUSES edge and downstream NORTH consequences. |
| **Action required** | Add `containers: [wo5k, north]` to both nodes' frontmatter. Do NOT wait for J4 to build the causal arc — the tag should reflect the node's inherent membership, independent of whether the causal arc is wired yet. |

---

### Seam 3 — Theon/Reek arc  [WO5K ∩ NORTH]

This is a character-arc seam, not a single event node. The arc spans multiple events:

| Event | Slug | Exists? | Containers |
|-------|------|---------|------------|
| Theon taken as ward | `theon-greyjoy-taken-as-ward` | HIT (1 CAUSES incoming from greyjoy-rebellion) | should be `[wo5k]` — origins pre-date NORTH |
| Theon captures Winterfell | `capture-of-winterfell` | HIT (dark) | `[wo5k, north]` (Seam 2 above) |
| Theon burns the "Stark boys" | no dedicated node | MISS | would be `[wo5k, north]` |
| Theon is Reek / Ramsay's captive | no node | MISS | `[north]` — now fully in NORTH theater |
| Theon carries Jeyne up battlements | `theon-carries-jeyne-up-battlements-stairs` | HIT (3 role edges, 0 causal) | `[north]` — this is ADWD NORTH territory |

**Live check:** `theon-carries-jeyne-up-battlements-stairs` has 0 containers tag and 0 causal edges. `theon-greyjoy-taken-as-ward` has no containers tag.

**Seam characterization:** The arc **pivots** from WO5K to NORTH at the moment Theon acts against his orders at Winterfell. The WO5K segment is `greyjoy-rebellion → theon-ward → balon-dispatches-theon`. The NORTH segment begins at `capture-of-winterfell` and deepens through the Reek chapters. The pivot event (`capture-of-winterfell`) is the seam node proper. See ownership ruling in Part 3.

---

### Seam 4 — Stannis: Blackwater → Wall → Winterfell  [WO5K ∩ NORTH]

This is a **character-path seam** across multiple events (not a single node).

| Event | Slug | Exists? | Causal State | Containers |
|-------|------|---------|--------------|------------|
| Battle of the Blackwater | `battle-of-the-blackwater` | HIT | 3 CAUSES outgoing (wired S111), 0 causal incoming | `[wo5k]` |
| Stannis retreats to Dragonstone | `stannis-retreats-to-dragonstone` | HIT | 1 CAUSES incoming ← Blackwater, 0 outgoing | `[wo5k]` |
| Stannis moves to the Wall | no node | MISS | — | `[wo5k, north]` — the seam event |
| Stannis saves the Wall / defeats Mance | no node | MISS | — | `[north]` |
| Stannis marches on Winterfell | no node | MISS | — | `[north]` (ASOS/ADWD) |

**Seam node (the join):** The event "Stannis moves to/arrives at the Wall" is the WO5K→NORTH transition for the Stannis thread. It should carry `[wo5k, north]` because Stannis's decision to go north originates from his Blackwater defeat (WO5K) and arrives in the NORTH theater. Once minted, this is a **bridge** — it will carry an upstream WO5K CAUSES edge (from `stannis-retreats-to-dragonstone`) and downstream NORTH CAUSES edges (Wall defense, march on Winterfell).

**Current graph gap:** `stannis-retreats-to-dragonstone` has 0 outgoing — the chain from Blackwater→Wall is entirely dark. `stannis-retreats-to-dragonstone` is already WO5K-tagged (implicitly; it's a downstream consequence of `battle-of-the-blackwater`). The `stannis-marches-on-winterfell` node does NOT exist (confirmed MISS).

---

### Seam 5 — The Pink Letter / Bastard Letter  [NORTH ∩ WO5K]

| Field | Value |
|-------|-------|
| **Artifact** | `bastard-letter` (object.artifact; 0 edges — confirmed completely dark) |
| **Content** | Ramsay's letter to Jon, claiming Stannis is dead, demanding Theon/Jeyne/Shireen/Selyse back |
| **Containers** | The LETTER'S cross-container significance: Ramsay is `[north]` (Bolton-held Winterfell); Stannis is `[wo5k, north]` (straddles both); the letter's provocation triggers Jon's decision that causes the `mutiny-at-castle-black` |
| **Seam type** | NOT a single seam node — the letter is an artifact that *links* NORTH agents to WO5K characters. The **event nodes** that are the seam are: (a) whatever "Ramsay sends the Pink Letter" event gets minted (NORTH-owned — Ramsay is a NORTH actor); (b) "Jon reads the Pink Letter and resolves to march south" (NORTH-owned). These events MOTIVATE the mutiny, which is NORTH. |
| **WO5K connection** | Stannis's fate (claimed dead by Ramsay) is a WO5K outcome. If Stannis is confirmed dead north of the Wall in a future NORTH arc, that event (`stannis-marches-on-winterfell` → outcome) would carry `[wo5k, north]`. The letter claiming his death is a NORTH event that *references* WO5K consequences. It is a pure seam, not a bridge — causation doesn't cross containers. |
| **Current state** | `bastard-letter` has 0 edges. `mutiny-at-castle-black` has 0 outgoing, 1 incoming PRECEDES (spurious). No event node for "Jon reads and reacts to the letter." All dark. |

---

### Seam 6 — Davos: WO5K agent → NORTH mission  [WO5K ∩ NORTH]

Davos is a **character** who bridges containers, not an event. But specific events he participates in are seam events.

| Event | Slug | Containers |
|-------|------|------------|
| Battle of Blackwater (Davos fights) | `battle-of-the-blackwater` | `[wo5k]` — canonical |
| Stannis imprisons Davos (Dragonstone) | no node | `[wo5k]` |
| Davos arrested at White Harbor | `wyman-publicly-arrests-davos-at-white-harbor` | `[north]` — White Harbor is NORTH political theater |
| Wyman stages fake execution of Davos | `wyman-manderly-stages-fake-execution-of-davos` | `[north]` |
| Davos is sent to recruit Manderly for Stannis | underlying mission node missing | `[wo5k, north]` — the **seam event** |

**Seam node:** "Stannis sends Davos to recruit Wyman Manderly" is the transition event — it is WO5K (Stannis's political strategy, a consequence of needing northern allies after Blackwater) and NORTH (White Harbor, Manderly's political situation, the Grand Northern Conspiracy). This event node does not exist yet. When minted, it should carry `[wo5k, north]`.

**Live state:** `wyman-publicly-arrests-davos-at-white-harbor` → SUB_BEAT_OF → `wyman-manderly-stages-fake-execution-of-davos` (both have role edges, 0 causal out). Both are NORTH-theater events. The upstream WO5K causation (Stannis dispatching Davos) is entirely dark.

---

### Seam 7 — House of the Undying Visions  [ESSOS ∩ AEGON]

| Field | Value |
|-------|-------|
| **Event** | Dany's visit to the House of the Undying in Qarth (ACOK) |
| **Slug** | No event node for the visit itself. `final-vision-human-sacrifice` EXISTS as an events node (confirmed in `ls graph/nodes/events/`); unclear scope. |
| **Containers** | The visit is physically in Essos (Qarth), but the "cloth dragon on poles" vision foreshadows fAegon / the AEGON container. `final-vision-human-sacrifice` should minimally carry `[essos]`; if it shows the cloth-dragon motif, `[essos, aegon]`. |
| **Seam type** | **Pure seam (not a bridge)** — the visions foretell AEGON events but carry no causal edge to AEGON. They are a narrative foreshadowing in Essos that the reader connects to AEGON-container events. The `FORESHADOWS` edge type is the correct link, not a causal CAUSES edge. No container boundary is crossed causally. |
| **Action** | When AEGON is scoped: the House of Undying visit event (to be minted) should carry `[essos, aegon]` because of its prophetic AEGON content. The causal arc stays ESSOS-owned; the AEGON tag enables `--container aegon` retrieval of the vision. |

---

### Seam 8 — Dany's Westeros Intent / Essos spine terminus  [ESSOS ∩ AEGON]

| Field | Value |
|-------|-------|
| **Event** | Dany deciding to sail for Westeros (published series terminus for this intent; no in-print sailing event — she's lost on the Dothraki sea at ADWD close) |
| **Published node** | `dany-lost-on-dothraki-sea` carries `containers: [essos]` — this is the true ADWD terminus |
| **AEGON-seam context** | Dany's Westeros intent is the *intended* downstream of the Essos arc — it's why she's building an army. Causally, the chain ESSOS → Westeros conquest belongs to AEGON (Varys/Illyrio planned for Dany to return). But the *published-series* connection has not yet happened in text. |
| **Recommendation** | Do NOT dual-tag `dany-lost-on-dothraki-sea` as `[essos, aegon]` based on authorial intent not realized in text. The AEGON seam activates only at the node where Dany or her army *crosses into Westerosi waters or politics*. That node does not exist in the 5 published books. The seam is a **future bridge**, not a current one. |

---

### Seam 9 — Varys / AEGON thread in King's Landing  [WO5K ∩ AEGON]

| Field | Value |
|-------|-------|
| **Events** | Varys's presence throughout WO5K-theater events (counsel to Ned, intel-sharing, Tyrion's rescue) + the AEGON-container endpoint (`assassinations-of-pycelle-and-kevan-lannister`) |
| **`assassinations-of-pycelle-and-kevan-lannister`** | EXISTS; 1 PART_OF → war-of-the-five-kings; 0 causal in or out |
| **Character Varys** | `varys CONSPIRES_WITH illyrio-mopatis` (confirmed in graph); `varys CONSPIRES_WITH house-targaryen` — these character edges exist; no event node yet for the tunnel conspiracy (see `dyad-queue.md` D1) |
| **Seam type** | `assassinations-of-pycelle-and-kevan-lannister` is an AEGON container event (it occurs in King's Landing and directly serves the AEGON restoration strategy) but is currently tagged `PART_OF war-of-the-five-kings` — it appears WO5K-scoped. It should be `containers: [aegon]` or `[aegon, wo5k]` depending on the causal chain: Varys acts on behalf of fAegon's restoration; the war is merely the context. Recommend `[aegon]` as primary; `[aegon, wo5k]` if the causal link from WO5K events (Cersei's arrest, Kevan's regency) is modeled. |
| **`landing-of-the-golden-company`** | EXISTS; PART_OF war-of-the-five-kings + 6 SUB_BEAT_OF incoming (military beats); should carry `containers: [aegon]`. |

---

## Part 2 — Bridge vs Seam Clarification

| Term | Definition | Graph test |
|------|-----------|------------|
| **Seam** | A node (or cluster) that belongs to two or more containers — dual-tagged because two storylines both claim it | `containers:` array has ≥2 values |
| **Bridge** | A seam node that ALSO has at least one causal edge (CAUSES / TRIGGERS / ENABLES / MOTIVATES) whose **source** belongs to container A and **target** belongs to container B — i.e. the edge crosses the boundary | `--causal-chain <slug>` returns upstream nodes with one container and downstream nodes with a different one |
| **Pure seam** | A seam with no cross-container causal edge; both containers claim it but causation doesn't cross | Same as seam but `--full-chain` shows only same-container endpoints |

**Already-built bridge:** `robert-orders-daenerys-assassination` — its upstream (Robert's court, WO5K) and its downstream (wine-merchant-attempt, Essos spine) are in different containers. This is the only built bridge in the current graph.

**Future bridges on mint:** `stannis-moves-to-the-wall` (WO5K upstream → NORTH downstream) and "Stannis sends Davos to Manderly" event will become bridges once their causal chains are wired. `capture-of-winterfell` will become a bridge when J4 (ironborn invasion arc) wires its upstream.

**Not bridges (pure seams):** House of the Undying visions (Essos ∩ AEGON), Pink Letter (NORTH ∩ WO5K) — both involve cross-container characters or themes but carry no causal edge crossing the boundary.

---

## Part 3 — Build-Once Ownership Rule

**The rule:**

> The container whose spine **causally roots** the node OWNS the build. The other container(s) only ADD their tag. Causal root = the node's most direct upstream CAUSES/TRIGGERS parent belongs to that container.

**Pressure-test on hard cases:**

| Node | Causal root belongs to | Owner | Other tags |
|------|----------------------|-------|------------|
| `robert-orders-daenerys-assassination` | WO5K (Robert's council) | WO5K | + essos |
| `capture-of-winterfell` | WO5K (ironborn invasion = J4, a WO5K arc) | WO5K | + north |
| `sack-of-winterfell` | WO5K (follows capture, same ironborn arc) | WO5K | + north |
| `stannis-moves-to-the-wall` (to mint) | WO5K (`stannis-retreats-to-dragonstone` is the upstream, WO5K-built) | WO5K | + north |
| "Stannis sends Davos to Manderly" (to mint) | WO5K (Stannis's political strategy post-Blackwater) | WO5K | + north |
| `wyman-publicly-arrests-davos-at-white-harbor` | NORTH (White Harbor political theater — no WO5K upstream wired) | NORTH | (no WO5K tag needed — WO5K upstream is upstream of Davos's mission, not this event) |
| `assassinations-of-pycelle-and-kevan-lannister` | AEGON (Varys acts for fAegon's restoration) | AEGON | + wo5k (if wired causally from Cersei's arrest chain) |
| `bastard-letter` (the letter, when wired) | NORTH (Ramsay sends it from Winterfell) | NORTH | (no WO5K tag — Stannis's fate is referenced but Stannis's actions are upstream, not the letter's cause) |

**Non-obvious corollary:** A node can carry container B's tag even if its spine is 100% in container A, IF it is a pivot point that container B queries will legitimately need. The Davos White Harbor nodes are a good example: they are pure NORTH events but Davos got there through a WO5K chain. The White Harbor *events themselves* are NORTH-owned; only the *dispatch event* (to mint) is the seam.

---

## Part 4 — Theon/Reek Ownership Verdict

**The case for WO5K ownership:** Theon's arc roots unambiguously in WO5K. The causal chain is: `greyjoy-rebellion CAUSES theon-greyjoy-taken-as-ward` → (B2 built arc) → Robb returns Theon to Balon as envoy → Balon rejects the alliance → ironborn invasion. All of this is WO5K causal territory. The seizure of Winterfell (`capture-of-winterfell`) is a WO5K event that happens to occur at a NORTH location.

**The case for NORTH ownership:** Theon's ADWD arc (the Reek chapters) takes place entirely in NORTH political space — Ramsay Bolton's Winterfell, the Bolton-Stark power struggle, the Grand Northern Conspiracy context. The `theon-carries-jeyne-up-battlements-stairs` node is purely NORTH. "Reek" is a NORTH character, not a WO5K one.

**Verdict: WO5K owns the build; tag dual `[wo5k, north]` at the pivot.**

- `theon-greyjoy-taken-as-ward` → `[wo5k]` (pure WO5K; precedes NORTH theater)
- `capture-of-winterfell` → `[wo5k, north]` (pivot; WO5K-owned build, NORTH claims its location/consequences)
- `sack-of-winterfell` → `[wo5k, north]` (same — the ironborn chain still owns the upstream)
- Reek-arc nodes (to mint: Theon tortured by Ramsay, Theon as Reek) → `[north]` (the WO5K causation is upstream of the pivot; these events are pure NORTH theater)
- `theon-carries-jeyne-up-battlements-stairs` → `[north]` (no WO5K causal edge reaches this; it's ADWD NORTH)

**Pivot definition:** The pivot is `capture-of-winterfell`. Before it: WO5K. At it: both. After the Sack and Theon's capture by Ramsay: NORTH only.

This is NOT a "build it twice" scenario. One series of events, built once, with the container array reflecting where each node sits in the causal landscape.

---

## Part 5 — Builder Checklist for Boundary Nodes

Use this checklist before minting OR tagging any node at a container boundary.

**Step 1: Existence check (prevent double-built duplicates)**
```
python3 scripts/event_alias_resolver.py --lookup "<natural phrase>"
```
If HIT: don't mint. Add the missing container tag to the existing node instead.
If MISS: mint once, tag with ALL containers it belongs to from the start.

**Step 2: Ownership determination (prevent spine-roots-in-wrong-container)**
- Ask: what is the direct upstream CAUSES/TRIGGERS parent?
- That parent's container = owning container.
- If the upstream parent doesn't exist yet (you're building a new chain), the container whose existing spine gets extended owns it.
- If no existing attach-point: the container whose thematic logic drives the event (WO5K = war politics, NORTH = Wall/wildling/northern-political, AEGON = Targaryen-restoration, ESSOS = Dany's arc in Essos) owns it.

**Step 3: Tag completeness (prevent orphans claimed by neither)**
- Stamp ALL containers the node belongs to in the same `containers:` array at mint time.
- Never leave a seam node with only ONE container when you know it's dual.
- Never use `containers: []` — omit the field entirely if no container applies (null = omit, not empty array).

**Step 4: Causal-chain verify (prevent tag-in-X-but-spine-roots-in-Y)**
```
python3 scripts/graph-query.py --causal-chain <slug>
```
Verify that the node's causal upstream traces to the container declared as owner. If the `--causal-chain` upstream walks into a different container than the one you declared as owner, reconsider the ownership assignment.

**Step 5: --full-chain confirm (once both arcs are built)**
```
python3 scripts/graph-query.py --full-chain <slug>
```
A bridge node's `--full-chain` should return endpoints in different containers (the ENABLES hops that a bridge traverses across the boundary). This is a post-build check, not a pre-build gate.

---

## Part 6 — Seam Summary Table (all seams, ordered by build priority)

| # | Seam node(s) | Containers | Type | Built? | Owner | Action |
|---|-------------|-----------|------|--------|-------|--------|
| 1 | `robert-orders-daenerys-assassination` | `[wo5k, essos]` | **Bridge** | ✅ YES (S119) | WO5K | Done — no action |
| 2 | `capture-of-winterfell` | `[wo5k, north]` | Seam → future bridge | Nodes exist, DARK | WO5K | Add `containers: [wo5k, north]` now |
| 3 | `sack-of-winterfell` | `[wo5k, north]` | Seam → future bridge | Nodes exist, DARK | WO5K | Add `containers: [wo5k, north]` now |
| 4 | "stannis-moves-to-the-wall" (to mint) | `[wo5k, north]` | Bridge (once wired) | MISS | WO5K | Mint when NORTH or WO5K builds Stannis's post-Blackwater path |
| 5 | "stannis-sends-davos-to-manderly" (to mint) | `[wo5k, north]` | Bridge (once wired) | MISS | WO5K | Mint when the Davos-Manderly arc is built |
| 6 | Theon pivot at `capture-of-winterfell` | (covered by #2) | — | — | — | — |
| 7 | `assassinations-of-pycelle-and-kevan-lannister` | `[aegon]` or `[aegon, wo5k]` | Pure seam (for now) | Exists, DARK | AEGON | Tag `containers: [aegon]`; add wo5k when causally wired |
| 8 | `landing-of-the-golden-company` | `[aegon]` | AEGON node, mistagged via PART_OF war | Exists, DARK | AEGON | Add `containers: [aegon]`; `PART_OF war-of-the-five-kings` is an error — the Golden Company is not fighting the WO5K, they're the AEGON-container invasion |
| 9 | House of Undying visit (to mint) | `[essos, aegon]` | Pure seam | MISS | ESSOS | Mint when ESSOS HotU beats are built; dual-tag at mint |
| 10 | Dany → Westeros intent | future node | Bridge (future) | Does not exist in text yet | AEGON | Do not mint; no published-canon crossing event exists |
| 11 | `bastard-letter` (the letter artifact) | `[north]` | NORTH artifact | Exists, 0 edges | NORTH | The artifact is NORTH; event nodes around it (sending, receiving) are also NORTH |
| 12 | `theon-carries-jeyne-up-battlements-stairs` | `[north]` | NORTH node | Exists, DARK | NORTH | Add `containers: [north]`; this is past the seam pivot |
| 13 | `theon-greyjoy-taken-as-ward` | `[wo5k]` | WO5K node | Exists, has 1 CAUSES in | WO5K | Add `containers: [wo5k]` |

---

## Part 7 — Non-Obvious Seams the Proposal Missed or Underspecified

**1. `landing-of-the-golden-company` is misclassified as WO5K**
The node has `PART_OF war-of-the-five-kings` — but the Golden Company is not a WO5K belligerent. They serve fAegon / AEGON-container. This `PART_OF` edge should be removed or corrected; the node belongs to `containers: [aegon]`. This is a **wiki-ingestion artifact** — the wiki's categorization lumped it under the war because it's a military landing, but the narrative containers are different.

**2. `assassinations-of-pycelle-and-kevan-lannister` is a WO5K misfiling**
Same pattern: `PART_OF war-of-the-five-kings`. Varys's killings serve the AEGON restoration, not the five-king succession fight. This should be `containers: [aegon]`.

**3. The Davos thread is a multi-hop seam, not a single node**
The proposal identifies Stannis's Blackwater→Wall path as a seam, but it doesn't name the specific *dispatch event* (Stannis sends Davos north) as the seam node. The dispatch event is the WO5K→NORTH bridge; the White Harbor arrest events are pure NORTH. Without naming the dispatch node as the seam's attach-point, builders might dual-tag the wrong events.

**4. The Pink Letter is NOT a causal bridge — it's an artifact that crosses container narrative space**
Ramsay's letter references WO5K characters (Stannis) but does not carry a causal edge into WO5K container space. The events it triggers (Jon's decision, mutiny-at-castle-black) are pure NORTH. Marking the bastard-letter as `[wo5k, north]` would be wrong — it is a NORTH-authored artifact that REFERENCES WO5K events. Keep it `[north]` only.

**5. Essos ∩ AEGON seam is premature for the current build state**
Dany's intent to sail west is not a built node. The HotU visit has no event node. Neither exists in the graph. The ESSOS/AEGON seam is real in narrative terms but has nothing to dual-tag yet. Flag as a future seam; don't let it block current work.

---

## Confidence Notes

All statements about node existence and causal state are ground-truth from live graph queries run 2026-06-21.
All MISS verdicts (stannis-moves-to-the-wall, stannis-marches-on-winterfell, bastard-letter event, HotU visit event, Theon/Reek capture nodes) confirmed via `event_alias_resolver.py --lookup`.
The `landing-of-the-golden-company PART_OF war-of-the-five-kings` finding is a live edge verified via `--neighbors`.
Causal edge counts are from `--causal-chain` and `--neighbors` runs; no inferences from text alone.
