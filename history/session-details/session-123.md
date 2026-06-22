# Session 123 — WO5K-remainder build (Q5 + J2+J9 + J7 + J4)

**Date:** 2026-06-22
**Model:** Opus 4.8 orchestrator + Sonnet-class `general-purpose` subagents (4 research/dip + 4 read-only fresh-verify). Handoff recommended Sonnet 4.6; the orchestrator ran on Opus 4.8 (continuing the S121/S122 pattern).
**Type:** Execution session — the decomposition reasoning was done in S112 (`working/wo5k-decomposition.md`). This is the build of the four remaining ranked junctures, plus the verify-driven corrections that emerged.

---

## Goal

Complete the WO5K container: build the four remaining junctures from `working/wo5k-decomposition.md` §5 (J3 was already shipped S113), in the order Q5 → J2+J9 → J7 → J4, each through the proven arc-mint machine (research dip → mint script → fresh-verify → citation-check → stamp).

## Outcome

**+6 nodes, +27 edges (22,384 → 22,411).** Every causal/agency edge fresh-subagent verified; all 27 pass `verify-edge-quotes` (0 drift); 0 new orphans (62 unchanged); 0 invented edge types (132); vocab 169. WO5K is now spine-complete, and an emergent cross-arc spine runs from Balon's opportunism to Robb's death.

---

## The four junctures

### Q5 — Storming of the Crag → Robb weds Jeyne
- **Mint:** `robb-receives-false-news-of-brans-death` (event.incident).
- **Edges (4):** `capture-of-winterfell CAUSES news`, `news TRIGGERS robb-weds-jeyne` + `MOTIVATES robb-stark`, `storming-of-the-crag ENABLES wedding` — a 2-cause convergence on the wedding (proximity/nursing from the storming + grief-comfort from the false news).
- **Dedup:** `battle-of-the-crag` is a confirmed redirect-dup (`same_as: storming-of-the-crag`, 0 edges) — no-op, canonical node is `storming-of-the-crag`.
- **Correction (source-node):** the research dip first proposed `sack-of-winterfell` as the upstream of the false-news beat. But the false deaths of Bran and Rickon come from **Theon's deception during `capture-of-winterfell`** (the tarred miller's-boy heads displayed on the gates), not Ramsay's later burning (`sack-of-winterfell`). The `capture-of-winterfell` node itself states "the grief over the alleged deaths of Bran and Rickon causes Robb Stark … to seek solace in Jeyne Westerling's arms." Corrected to `capture` before minting. Fresh-verify independently corroborated via Robb's line at asos-catelyn-03:151. This is the wrong-but-existing-target class the `mint_arc_lib` slug pre-check explicitly does NOT catch — caught by reading the node.

### J2+J9 — Blackwater UPSTREAM (the highest-salience gap)
- **Mints:** `stannis-absorbs-renly-s-host` (event.incident), `littlefinger-brokers-tyrell-lannister-alliance` (event.conspiracy).
- **Edges (9):** J2 prong — `shadow-assassination-of-renly CAUSES stannis-absorbs-host`, `absorb ENABLES battle-of-the-blackwater`, stannis AGENT_IN. J9 prong — `shadow MOTIVATES loras-tyrell`, loras AGENT_IN `fighting-at-bitterbridge`, `shadow ENABLES broker`, tyrion + petyr AGENT_IN broker, `broker ENABLES battle-of-the-blackwater`.
- **Dedup traps avoided** (sharp catches by the research dip): `sack-of-bitterbridge` = the **Dance of the Dragons** (130 AC, Maelor Targaryen) — pure name-collision; `tyrell-plot-revealed` = the **Purple Wedding** poisoning plot — unrelated. Neither wired. `fighting-at-bitterbridge` is the genuine realignment locus (kept, wired loras AGENT_IN).
- **Fresh-verify ADJUST:** the broker→blackwater edge was minted as CAUSES; the verifier argued (and I agreed) that the brokering enables the Lannister **victory** (the Tyrell relief force), not the battle's **occurrence** (which is Stannis's assault). Pointing CAUSES at the whole battle node conflates cause-of-outcome with cause-of-event. Changed to **ENABLES**. Both prongs now ENABLES the battle (one supplies Stannis's army → the battle happens; one supplies the Tyrell relief → the Lannisters win).

### J7 — Karstark execution → Robb isolation
- **Mint:** `karstark-host-deserts-robb` (event.incident).
- **Edges (2):** `karstark-murders-prisoners-at-riverrun CAUSES desertion`, `desertion ENABLES red-wedding-conspiracy`.
- **Terminus correction (decomp doc vs graph):** the decomp listed the terminus as `robb-weds-jeyne-westerling`, but the wedding (299) chronologically **precedes** the Karstark execution (299, later) — you cannot wire exec → wedding. The correct terminus is `red-wedding-conspiracy` (the Frey re-negotiation Robb's weakened position pushes him into). Verified against the live graph (occurred years + the existing `robb-weds-jeyne TRIGGERS conspiracy` edge). A "trust worklog/graph over the task-scoped decomp doc" moment (CLAUDE.md rule #9 spirit).
- **Fresh-verify RE-POINT:** the desertion edge was minted as `execution-of-rickard-karstark CAUSES desertion`. The verifier caught a **temporal inversion** — the Karstark riders desert *at nightfall*, before the *dawn* execution (they flee when Robb condemns their lord, not after the beheading). Re-pointed the source to `karstark-murders-prisoners-at-riverrun` (chronologically prior; the murders doomed Rickard → his men flee). The murders now causally produce both the execution and the desertion (accurate sibling consequences).

### J4 — Balon's invasion → Capture of Winterfell
- **Mints:** `balon-declares-himself-king` (event.ceremony), `ironborn-invasion-of-the-north` (event.incident).
- **Edges (12, from 14 minted − 2 rejected):** `declare CAUSES invasion`, `declare MOTIVATES theon-greyjoy`, `invasion CAUSES fall-of-moat-cailin` + `CAUSES harrying-of-the-stony-shore` + `ENABLES capture-of-winterfell`, `harrying ENABLES capture` (raid-as-cover), + 6 role edges (balon AGENT_IN/COMMANDS_IN, theon/asha/victarion AGENT_IN invasion, theon AGENT_IN capture).
- **Policy-driven mint drop (S120 granularity):** the research dip proposed a 3rd mint, `theon-seizes-winterfell-against-orders`, to TRIGGER `capture-of-winterfell`. Dropped — Theon's seizing-against-orders **is** the capture (a constitutive action within it), not a chronologically-prior prerequisite. Minting it to trigger the capture would be the exact "constitutive beat promoted to cause" anti-pattern the S120 policy forbids. The two-level agency was instead modeled via `MOTIVATES → theon-greyjoy` + `theon AGENT_IN capture-of-winterfell` (which filled a real role gap — Theon was not previously linked as agent to the capture) + the Stony-Shore raid as ENABLES cover.
- **Fresh-verify REJECT ×2:** (1) `theon-greyjoy-taken-as-ward ENABLES balon-declares` — rejected as **sequence-not-cause**: Balon's refusal was trait-driven and his fleet was already mustering ("Do you think I gather my ships to watch them rock at anchor?"); the ward/envoy fact is incidental occasion, not enablement. Dropped → the arc roots at `balon-declares-himself-king` as an intentional standalone (cf. the Kingsmoot arc). (2) `balon-declares MOTIVATES balon-greyjoy` — rejected as **circular self-MOTIVATES**: an event cannot motivate its own sole agent; the declaration *is* Balon's decision. Dropped; Balon's pride is captured in the node's `## Quotes`.

---

## The emergent cross-arc spine

`--full-chain balon-declares-himself-king` now walks, in one query:

```
balon-declares-himself-king
  → ironborn-invasion-of-the-north
    → capture-of-winterfell                       (ENABLES)
      → robb-receives-false-news-of-brans-death   (the Q5 node)
        → robb-weds-jeyne-westerling              (TRIGGERS)
          → red-wedding-conspiracy
            → red-wedding / robb-is-killed
```

The Q5 and J4 builds were authored independently but met at `capture-of-winterfell` — the false-deaths node (Q5) sits exactly where Theon's seizure (J4) lands. The whole Greyjoy-opportunism-to-Stark-downfall causal spine is now traversable. This is the cross-book auto-join the container strategy was designed to surface.

---

## Process notes

- **The fresh-verify layer earned its keep.** Across 4 arcs it produced: 1 ADJUST (J2+J9 broker CAUSES→ENABLES), 1 RE-POINT (J7 source exec→murders), 2 REJECT (J4 sequence + self-MOTIVATES). None of these were citation problems — all four are edge-*semantics* corrections that a citation checker cannot catch. This validates the FIRM rule (Matt gates at policy, fresh subagents adjudicate per-edge against the local cache).
- **The arc-mint machine ran clean.** Each juncture: deterministic node/script checks first (Python before Agent) → research dip (dedup + grounding proposal) → orchestrator scrutiny (I corrected sack→capture and the J7 terminus *before* dispatching the verify) → mint script (with `mint_arc_lib.precheck_slugs` floor) → `weirwood refresh` → `verify-edge-quotes` (caught 4 quote-splice mismatches across the session, all from splicing across dialogue attributions — fixed to clean contiguous substrings) → fresh-verify → stamp `verified_by`.
- **Quote-splice failure mode (recurring):** the citation checker flagged quotes that combined two sentences across a `," said X, "` attribution. The fix is always to use a single clean contiguous span; the embedded dialogue-quote characters break the substring match. Worth pushing into the research-subagent prompt next time (ask for contiguous substrings only).
- **Harvest:** 16 rows captured (Grey Wind/Ser Rolph Spicer treachery-detector foreshadowing, "five wolf pups" omen, Garlan-as-Renly's-ghost at the Blackwater, the Balon "iron price" cite confirmed at acok-theon-01:361, Theon-defiance + "thirty men" book-cite overlays onto `capture-of-winterfell`, Theon's occupied-Winterfell cruelty). The moon-tea/Sybell Spicer fertility-sabotage material was **parked** (theories track is gated).

## What's next

WO5K is spine-complete. The remaining three containers each need their own decomposition dip before building (per S122): **NORTH** (Theon/Reek + Bolton + Stannis-marches), **AEGON** (Golden Company landing; fix the `PART_OF war-of-the-five-kings` edge-hygiene bug first), **Bran** (greenfield flight-to-the-north spine). No single obvious next — Matt picks the container, then a decomp dip runs on the `working/wo5k-decomposition.md` / `working/essos-decomposition.md` template. The chat-ui-personality-design track remains independently runnable.
