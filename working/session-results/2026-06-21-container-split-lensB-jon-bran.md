# Lens B — Jon/Bran Granularity: Independent Pressure-Test

> **Date:** 2026-06-21 (S121 container-split fan-out)
> **Scope:** Are Jon Snow and Bran Stark big enough to be their OWN containers vs sub-threads of
> NORTH? Independent verification vs the orchestrator's first-draft proposal (hybrid dual-tag).
> **Method:** All claims grounded against the live graph via `graph-query.py` and
> `event_alias_resolver.py`. Read-only. No graph writes.

---

## 0. Setup: What "Container-sized" Means

The size bar is Essos (~16 nodes stamped, with ~8 buildable causal junctures) and WO5K (~6–10 junctures).
A container justifies its own tag when:
1. It has ≥5 buildable causal junctures (distinct arc moments with strong CAUSES/TRIGGERS/ENABLES logic)
2. Those junctures span ≥2 books and form a coherent story unit a user would query as a group
3. A `--container <name>` query returns a meaningfully different set from `--container north`

---

## 1. Jon Snow: Juncture Inventory

**Chapter footprint (verified from disk):** AGOT×9 + ACOK×8 + ASOS×12 + AFFC×0 + ADWD×13 = **42 POV chapters.**
Jon is the single largest POV in terms of chapters after Tyrion (who spans all books). His arc is absent only from AFFC, where it pivots entirely to Sam carrying the LC-election thread.

### Foreshadowed events in Jon's arc (from reference/foreshadowing-events.md)
- **#16 Jon elected Lord Commander** (ASOS Jon XII) — "Sam's political maneuvering, Mormont's raven saying 'Snow' and 'king'"
- **#21 Jon's assassination** (ADWD Jon XIII) — "Ghost being locked away, Melisandre's visions of Jon as 'a man, then a wolf, then a man again'"
- **#28 R+L=J revelation setup** (cross-book) — labelled standalone but Jon is the subject; Ned's fever dream, Tower of Joy, "promise me Ned"
- **#29 The Others' true nature** (cross-book) — Jon is the Watch's foremost witness; prologue → LC arc → assassination

### Buildable juncture inventory (verified with `--neighbors`, `--lookup`)

| # | Juncture slug (proposed or exists) | Exists? | Causal state | Build-readiness |
|---|-------------------------------------|---------|--------------|-----------------|
| J1 | `jon-takes-his-vows` (AGOT Jon VI) | **NO NODE** | DARK | Needs mint; clean single-POV event |
| J2 | `wight-attacks` (AGOT Jon VII — Mormont wight) | **EXISTS** | 0 causal | Needs wiring; wight attacks Mormont's cell; Jon burns it |
| J3 | `jon-kills-qhorin-halfhand` (ACOK Jon VIII — infiltration pivot) | **EXISTS** | 0 causal | Needs 1 CAUSES out → Jon undercover in Mance's camp |
| J4 | `attack-on-castle-black` (ASOS Jon VII/VIII — Mance's assault) | **EXISTS** | 0 causal | Needs upstream (Mance march ENABLES) + downstream |
| J5 | `jon-overhears-the-conspiracy` (ASOS Jon XII — Thorne/Marsh/Yarwyck plot) | **EXISTS** | 0 causal | Needs CAUSES → Sam's LC-campaign maneuver |
| J6 | `jon-elected-lord-commander` (ASOS Jon XII) | **NO NODE** | DARK | Key terminus of ASOS arc; needs mint |
| J7 | `execution-of-janos-slynt` (ADWD Jon II) | **EXISTS** | 0 causal | Needs wiring; Jon's first act as LC |
| J8 | `mance-rayder-brought-to-execution` (ADWD Jon III) | **EXISTS** | 0 causal | Needs wiring; Wall tension with Stannis |
| J9 | `free-folk-allowed-through-the-wall` (ADWD Jon VIII) | **NO NODE** | DARK | Jon's fateful political decision; directly triggers assassination |
| J10 | `jon-is-stabbed-repeatedly` (ADWD Jon XIII) | **EXISTS** | 0 causal | Terminus; needs upstream CAUSES |

**Jon juncture count: 10** (7 existing nodes needing wiring, 3 to mint).

### Intersection with NORTH vs standing apart

Nodes J1–J4 sit in the Watch/wildling theater — deeply Watch-internal, but the Wall is the northern frontier. The political-north thread (Manderly, Stannis marching, Bolton-held Winterfell) runs in parallel POVs (Theon-as-Reek, Asha, Davos-in-Manderly) and crosses Jon's arc at: Stannis arriving (J8 upstream), the pink letter from Ramsay (J9 upstream), and Jon's announcement to march on Winterfell triggering J10. So:

- **J1–J5** are Watch-internal (Jon's POV only, mostly Castle Black / Beyond the Wall). Negligible overlap with pure-NORTH political beats.
- **J6–J10** are the LC arc where Jon's authority intersects the broader NORTH: Slynt (WO5K agent), Mance-execution (Stannis-at-Wall), free-folk decision (impacts wildling-NORTH seam), stabbing (Bowen Marsh = NORTH military establishment reacting to Jon's LC decisions).

Key finding: **roughly half of Jon's junctures (J6–J10) are the causal zone where Jon and NORTH-political converge.** The other half (J1–J5) are pure Watch-internal and would be orphaned inside a [north]-only tag — a user querying `--container north` for Manderly pies and Stannis's march would drown in Watch-infiltration sub-beats.

---

## 2. Bran Stark: Juncture Inventory

**Chapter footprint (verified from disk):** AGOT×7 + ACOK×7 + ASOS×4 + AFFC×0 + ADWD×3 = **21 POV chapters.**
Bran has roughly HALF Jon's chapter count, concentrated in AGOT/ACOK, then tapering sharply to 4 in ASOS and 3 in ADWD.

### Foreshadowed events in Bran's arc (from reference/foreshadowing-events.md)
- **#2 Bran's fall** (AGOT Bran II) — already built: `jaime-pushes-bran-from-the-tower`
- **#29 The Others' true nature** (cross-book) — Bran's prologue dream and warg contact with the White Walkers in ADWD is indirect evidence; primarily Others' domain, not Bran-specific

No foreshadowed events are uniquely "Bran-container events" the way #16/#21 are Jon's.

### Buildable juncture inventory

| # | Juncture slug (proposed or exists) | Exists? | Causal state | Build-readiness |
|---|-------------------------------------|---------|--------------|-----------------|
| B1 | `jaime-pushes-bran-from-the-tower` (AGOT Bran II) | **EXISTS** | **BUILT** — 1 upstream + 5 downstream causal edges | Arc ROOT; downstream chain leads to WO5K (Littlefinger→Catelyn) |
| B2 | `six-wildling-deserters-ambush-bran` (AGOT Bran V) | **EXISTS** | 0 causal | Isolated incident; 0 causal edges; low arc significance |
| B3 | `bran-flees-winterfell-north` (ACOK — after Theon's capture) | **NO NODE** | DARK | Pivot event separating Bran from all political NORTH; needs mint |
| B4 | `bran-learns-to-warg-hodor` (ASOS Bran III — ethical threshold) | **NO NODE** | DARK | Only in Bran's greenseer arc; no other POV sees it |
| B5 | `bran-enters-cave-of-three-eyed-crow` (ADWD Bran II) | **NO NODE** | DARK | Arc terminus; location node `cave-of-the-three-eyed-crow` EXISTS; event node does not |

**Bran juncture count: 5** (1 built, 1 existing but dark/isolated, 3 to mint).

### Intersection with NORTH vs standing apart

B1 (`jaime-pushes-bran-from-the-tower`) is already the root of the WO5K arc, not NORTH. Its downstream chain is `bran-fall → dagger → Littlefinger → Catelyn-seizes-Tyrion → Gregor-raids-Riverlands → war`. This event belongs to WO5K causally, not NORTH.

B3–B5 are **completely isolated from NORTH political beats**. Bran fleeing north doesn't interact with Manderly, the Boltons, or Stannis. Bran's greenseer arc is spiritually/geographically "beyond the Wall" — a different theater from the Watch/wildling theater Jon occupies and from the political-north theater (Winterfell/Bolton/Manderly).

Key finding: **Bran's arc, after B1, has NO causal intersection with NORTH-political events.** B1 itself belongs to WO5K. B3–B5 belong to a "beyond-the-wall / greenseer" theater that is geographically north but narratively orthogonal to everything NORTH is supposed to capture.

---

## 3. Comparison to the Size Bar

| Container | Built nodes (tagged) | Causal junctures (buildable) | Books spanned | User-query distinctiveness |
|-----------|---------------------|------------------------------|---------------|---------------------------|
| ESSOS | 16 | ~8 (E1–E5 built; E6–E8 pending) | AGOT–ADWD | High: Dany's arc is entirely distinct |
| WO5K | 2 (many untagged) | ~8–10 | AGOT–ADWD | High: five-kings war + King's Landing |
| **jon** (proposed) | 0 | **10** | AGOT–ADWD (gap AFFC) | High: Watch-arc is distinct from political NORTH |
| **bran** (proposed) | 1 (B1 = jaime-pushes-bran) | **5** | AGOT–ADWD | **Low**: only 4 buildable beats; B1 belongs to WO5K causally |

Jon clears the size bar. Bran does not.

---

## 4. Intersection Analysis: How Much Each Overlaps NORTH

### Jon × NORTH overlap
Jon's arc **lives inside NORTH's theater** (Wall, Castle Black, wildlings, Stannis) but is a **distinct causal thread** within it. A `--container north` query without a `jon` tag would need to include ~10 Watch-specific events that clutter any query about Manderly, Bolton, or the Grand Northern Conspiracy. Conversely, `--container jon` cleanly returns the Watch-leadership spine without the political-north beats.

The overlap zone is J6–J10 (ADWD LC arc), where Jon's decisions directly interact with the northern political situation (pink letter, march announcement). These 5 junctures merit dual-tag `[north, jon]`. The AGOT/ACOK/ASOS Watch-internal beats (J1–J5) are `[jon]` only — they are not "the political north."

**Conclusion: Jon is large enough for its own container AND deeply embedded in NORTH. Hybrid dual-tag is the right model.**

### Bran × NORTH overlap
Bran's arc has almost zero overlap with NORTH-political:
- B1 (`jaime-pushes-bran-from-the-tower`) belongs to **WO5K**, not NORTH
- B2 (`six-wildling-deserters-ambush-bran`) is pre-NORTH-political in AGOT; Bran is still at Winterfell
- B3–B5 are geographically north of the Wall but causally independent of any NORTH thread

Bran never attends a Winterfell political council after AGOT, never interacts with Manderly or Davos, never affects the Watch-leadership thread. He is on a **separate spiritual/mystical track** that intersects NORTH's geography but not its causal web. Tagging Bran under `[north]` would be accurate only in the sense that "Bran is from the North" — not useful container-membership.

**Conclusion: Bran's arc is not a sub-thread of NORTH. It is its own distinct thing. The question is whether that thing is large enough for a container.**

---

## 5. The Proposal Under Scrutiny

The orchestrator's draft recommends:
- Jon: hybrid dual-tag `[north, jon]` for Watch beats, `[north]` only for pure-NORTH-political beats
- Bran: own tag `[bran]` (not nested under north)

### Verification of Jon recommendation
**CONFIRMED.** The graph evidence supports it:
- 10 buildable junctures (above Essos's ~8 bar)
- Clear query-value: `--container jon` returns Watch spine; `--container north` returns political NORTH; the ADWD LC beats are dual-tagged where causation crosses
- Build order: Jon's AGOT/ACOK/ASOS beats can be built independently of NORTH; only J6–J10 need NORTH to exist first (for the cross-container seams to make sense)

One refinement: the proposal says "pure-NORTH-political beats (Manderly, Stannis-marches) carry `[north]` only." This is correct — Manderly and Stannis are NORTH-political actors, not Jon's arc. Jon's stabbing at the end is dual-tagged `[north, jon]` because it occurs in the Watch context AND is the direct consequence of Jon's NORTH-entangled LC decisions.

### Verification of Bran recommendation
**PARTIALLY CONFIRMED, with a significant caveat.**

The proposal is correct that Bran is NOT nested under north — Bran's arc doesn't belong to NORTH. But the size question is live:

- 5 junctures is below the bar (Essos has ~8 built, more pending)
- 1 of those 5 (B1) belongs to WO5K, not Bran's own arc
- Only 4 are genuinely Bran-internal, with 3 needing mint
- ADWD has only 3 Bran chapters — the arc barely gets off the ground before the series goes on hold (TWOW is unwritten)

**A `[bran]` container with 4–5 junctures is a micro-container risk.** It passes the "nobody would query this as a group" test only if users specifically want the greenseer/warg arc. That IS a real query — "what causes Bran to become a greenseer?" — but the arc is so thin in the extant text that the container would be nearly empty at build time and mostly speculative until TWOW.

---

## 6. Recommendation: Option (c) Modified

The briefing offers three options: (a) Jon+Bran each own container; (b) both tagged `[north]` only; (c) hybrid dual-tag the overlap.

**Recommendation: (c) hybrid, but with a split treatment of Jon vs Bran.**

### Jon: hybrid dual-tag — CONFIRMED

Build Jon as its own container `[jon]`, dual-stamped with `[north]` on the LC-era beats (J6–J10 where causation crosses the boundary). This is:
- Container-sized (10 junctures, above the bar)
- Query-distinct from NORTH
- Practically required: without `[jon]`, Watch-spine queries drown in political-NORTH noise

**Build order dependency:** Jon's AGOT–ASOS Watch-internal beats (J1–J5) are NORTH-independent. Jon's ADWD LC beats (J6–J10) depend on NORTH being named/scoped first (so the dual-tag `[north, jon]` is coherent). NORTH does not need to be BUILT first — the tag can be applied before NORTH's causal spine is constructed. But NORTH must be named as a container in the manifest before dual-tagging begins.

### Bran: NOT its own container yet — DIVERGES from proposal

**Do not mint `[bran]` as a live container now.** The arc has only 4 genuinely-Bran-internal buildable junctures, B1 belongs to WO5K, and the arc's most interesting events (TWOW greenseer arc, Bran as cosmic figure) are unwritten. A `[bran]` container built now would be:
- 4–5 nodes maximum
- 75% unminted
- Mostly a placeholder for future books, not a retrieval tool for the existing corpus

**Instead: hold `[bran]` in reserve as a named-but-not-yet-built container.** Add it to the container manifest alongside the other proposed containers, but do not begin the decomposition dip until the existing 4 junctures are understood as a coherent unit (B3–B5 need individual verification) AND there is user demand for greenseer-arc queries.

In the interim: Bran-related events that exist or get minted carry either:
- `containers: [wo5k]` for B1 (Bran's fall is a WO5K prime mover)
- No container tag (null) for B2 (isolated incident, no arc membership yet)
- Pending `[bran]` stamp when the container is opened

**This differs from the proposal.** The proposal says "Bran as its own tag (not nested under north)" — that direction is correct, but the proposal implies it should be built now. The graph evidence says not yet: the arc is too thin for the current corpus to justify a container-sized build.

---

## 7. Concrete Example Slugs with Recommended `containers:` Arrays

| Slug | Event | Recommended `containers:` |
|------|-------|--------------------------|
| `wight-attacks` | Jon fights wight at Castle Black (AGOT) | `[jon]` |
| `jon-kills-qhorin-halfhand` | Jon's Watch infiltration pivot (ACOK) | `[jon]` |
| `attack-on-castle-black` | Mance's assault on the Wall (ASOS) | `[jon]` |
| `jon-elected-lord-commander` | (to mint) Sam's political maneuver → Jon elected (ASOS) | `[jon]` |
| `execution-of-janos-slynt` | Jon's authority established as LC (ADWD) | `[north, jon]` |
| `mance-rayder-brought-to-execution` | Wall politics with Stannis (ADWD) | `[north, jon]` |
| `free-folk-allowed-through-the-wall` | (to mint) Jon's fateful decision; ADWD trigger | `[north, jon]` |
| `jon-is-stabbed-repeatedly` | Jon's assassination; arc terminus (ADWD) | `[north, jon]` |
| `stannis-marches-on-winterfell` | (to mint) Pure NORTH-political beat, Stannis not Jon | `[north]` |
| `wymans-frey-pies` | (to mint) Grand Northern Conspiracy; no Jon involvement | `[north]` |
| `jaime-pushes-bran-from-the-tower` | Arc ROOT; downstream leads to WO5K war trigger | `[wo5k]` (not north, not bran) |
| `bran-enters-cave-of-three-eyed-crow` | (to mint when bran-container opened) | `[bran]` (deferred) |

**The dual-tag boundary:** events where Jon is AGENT_IN or VICTIM_IN AND the event is causally downstream of his LC authority → `[north, jon]`. Events where Jon acts in the Watch-internal sphere (infiltration, Wall defense, Halfhand, castle-black battle) → `[jon]` only.

---

## 8. Build-Order Dependency vs NORTH

**Jon's AGOT–ASOS junctures (J1–J5):** NORTH-independent. These can be decomposed and built in any order before NORTH exists. No dual-tag needed; they are pure `[jon]`.

**Jon's ADWD junctures (J6–J10):** NORTH must be named in the container manifest before the dual-tag `[north, jon]` is applied. NORTH does not need to be causally built — just named as a container. This is the only dependency.

**Bran's junctures:** B1 goes to WO5K regardless of NORTH or Bran-container timing. B3–B5 are held until `[bran]` is opened. No dependency on NORTH.

**Build order implication for this session:** If Matt opens NORTH next (likely, per the proposal), Jon's decomposition dip can be kicked off in parallel with NORTH's decomposition — they are independent up to J6. The ADWD LC beats are the seam, built last, after NORTH's spine root is established.

---

## 9. Anti-micro-container Check

The briefing warns: "Avoid micro-containers nobody queries; never `[]`."

- `[jon]`: 10 junctures, 42 chapters of source material, one of the most-queried characters. NOT a micro-container.
- `[bran]`: 4–5 junctures in the current corpus. **IS a micro-container risk.** Deferred until TWOW or until the existing junctures form a coherent queryable unit.

The orchestrator's proposal would mint `[bran]` now. This analysis says defer — the cost of minting a nearly-empty container is low, but the cost of building out an underspecified decomp and then having to retag when TWOW rewrites our understanding of Bran's arc is higher.

---

## 10. Summary Table

| Question | Finding |
|----------|---------|
| Is Jon container-sized? | YES — 10 buildable junctures, 42 chapters, clears the Essos bar |
| Is Bran container-sized (now)? | NO — 4–5 junctures in extant corpus; B1 belongs to WO5K; arc too thin |
| Should Jon be nested under NORTH? | PARTIAL — AGOT–ASOS Watch beats are `[jon]` only; ADWD LC beats dual-tag `[north, jon]` |
| Should Bran be nested under NORTH? | NO — Bran's greenseer arc is orthogonal to NORTH-political; B1 belongs to WO5K |
| Does the proposal hold? | Jon: CONFIRMED. Bran: DIVERGES — defer container open, don't build now |
| Build order dependency? | Jon's J1–J5 = NORTH-independent; J6–J10 need NORTH named (not built) first |
