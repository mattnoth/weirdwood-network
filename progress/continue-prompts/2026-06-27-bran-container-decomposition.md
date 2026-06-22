# SESSION 129 — BRAN container decomposition dip (read-only)

> **This is Session 129.** Stamp your worklog entry `### Session 129` at endsession.

> **Recommended model:** Sonnet 4.6 (Opus 4.8 orchestrator + 1 Sonnet-class `general-purpose` research subagent for the dip). Same read-only decomposition machine as the NORTH (S124) and AEGON (S127) dips.
> **This is a READ-ONLY DIP — 0 graph writes (0 nodes minted, 0 edges added).** Local cache only: no HTTP, no wiki refetch. The deliverable is a planning doc; the BUILD is a separate later session.

## Goal
Produce `working/bran-decomposition.md` — the BRAN container's internal causal trigger-tree, juncture scorecard, and ranked build order — following the **8-section structure of `working/aegon-decomposition.md` / `working/north-decomposition.md`** (use those as the template, exactly). BRAN is the 5th and last of Matt's approved containers (`{essos, wo5k, north, aegon, bran}`) without a decomposition dip. It is **greenfield** (Bran added by Matt's override — container-sized but with almost no scaffolding).

## Current container state (verified at handoff, S128)
`python3 scripts/graph-query.py --container bran` returns **exactly 3 nodes**:
- `jaime-pushes-bran-from-the-tower` (event.incident, `[bran, wo5k]` seam)
- `bran-witnesses-jaime-and-cersei` (event.incident) — the witnessing that OWNS an outgoing causal edge (it CAUSES the push), so it is correctly already a node per the S117 edge-vs-node rule
- `six-wildling-deserters-ambush-bran` (event.incident)

Many BRAN-relevant event nodes already EXIST on disk but are **not container-tagged and likely causally dark** — verify each at the dip, do not assume. Confirmed present: `bran-s-direwolf-kills-the-assassin`, `sack-of-winterfell`, `capture-of-winterfell`, `battle-of-winterfell`, `robb-receives-false-news-of-brans-death`. Search `graph/nodes/events/` for more (warging/coma/three-eyed-crow/Bloodraven/Reed/Hodor/flight-north/Rickon-splits beats may be MISS = need mint at build).

## What the dip must do (mirror the AEGON/NORTH dips)
1. **Verify causal state against the LIVE graph** — `--container bran`, `--neighbors <slug>`, `--causal-chain <slug>` on every candidate node + direct node reads. State HIT (exists) / MISS (needs mint) / dark (exists, 0 causal) per beat. Do NOT trust node prose for edge-state — verify against `graph/edges/edges.jsonl`.
2. **Map the trigger-tree** — Bran's arc is roughly: the catspaw assassination attempt (`bran-s-direwolf-kills-the-assassin`) → Catelyn rides south (cross-links to WO5K/Ned); the fall (`bran-witnesses-jaime-and-cersei CAUSES jaime-pushes-bran-from-the-tower`) → coma → warging/wolf-dreams → Theon's sack of Winterfell forces Bran's flight → journey beyond the Wall (Reeds, Hodor, Rickon splits off, Jojen) → Bloodraven / three-eyed crow → Bran becomes a greenseer. Confirm the real spine from the text; do not impose this sketch.
3. **Score every juncture** with the rubric in `working/causal-arc-strategy-2026-06-18.md` (Q/S/X/C/B/G, 0–2 each, max 12; gate ≥7/12 AND not (G=0,Q<2)). Rank a build order (cheapest real cause first, clean attach + terminus).
4. **Ground every cited quote** in the LOCAL book cache (`sources/chapters/`) — line-check each cite exactly (the AEGON dip's cites all line-checked; hold that bar).
5. **Flag (don't fix) any edge bugs / suspicious edges / slug traps** for the build session — exactly as the AEGON dip flagged the `PART_OF wo5k` bug + the cross-theater PRECEDES (both fixed clean at S128 build-step 0).

## Seams to annotate (ATTACH at build, never rebuild)
- `jaime-pushes-bran-from-the-tower` = BRAN ∩ WO5K (already `[bran, wo5k]`) — the assassination attempt → Catelyn's southern ride → arrest of Tyrion is a WO5K trigger.
- `sack-of-winterfell` / `capture-of-winterfell` = BRAN ∩ NORTH ∩ WO5K (Theon's taking, already built in the NORTH/WO5K work — Bran's flight ATTACHES to it; do NOT rebuild).
- `robb-receives-false-news-of-brans-death` (minted S123, WO5K) — the false-death is a consequence of the sack; cross-links BRAN→WO5K.

## Spoiler / tier discipline
Map only WHAT HAPPENS (the fall, coma, warging, flight, journey north, reaching Bloodraven, becoming a greenseer) at Tier 1–2. Route any **"Bran is the Night King / Bran-as-Bloodraven-successor cosmology / time-travel / hodor-origin"** speculation to the GATED theories track — NEVER a causal node or edge. The greenseer/three-eyed-crow material that is *textual fact* (he reaches the cave, eats the weirwood paste, sees through the trees) is in-scope; the *theory* layer about what it means is not.

## Dyad note
`working/dyad-queue.md` D2 (Jorah) is Essos, not Bran. No parked Bran dyads exist; surface any new dyad candidates (e.g. Bran↔Jojen greendreaming relationship) into the queue rather than forcing them into the causal map.

## Vocabulary (PASTE into the research subagent — it does NOT load CLAUDE.md)
Edge types = locked set: CAUSES / TRIGGERS / ENABLES / MOTIVATES / CONSPIRES_WITH (+ roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN / GUARDS / WIELDED_IN). "Pass" = corpus sweep · "Track" = named workstream · lowercase "step" = ordered piece · "Tier" = confidence 1–5 ONLY. No new capitalized terms. Slug discipline: spot-check every slug exists (`scripts/mint_arc_lib.py <slug> …`) — record the verified slug for each beat so the build session doesn't cross wires.

## Harvest push (PASTE into the research subagent)
While in the text, drop `| open | <kind> | <book> | <chapter:line> | <note> | bran-dip |` rows into `working/harvest-queue.md` (POINT, don't extract; line-check each cite). Bran's chapters are the most foreshadowing-dense in the corpus — expect a rich harvest (the crow, the three-eyed crow's "fly or die," the comet, Old Nan's tales, the crypts).

## Read first
- `working/aegon-decomposition.md` + `working/north-decomposition.md` — the 8-section template (copy the structure exactly).
- `working/causal-arc-strategy-2026-06-18.md` — the scorecard rubric.
- `working/session-results/2026-06-21-container-SHAPE-map.md` — the 5-container SHAPE map (bran = greenfield, 3 nodes at map time).
- `working/dyad-queue.md` — dyad-vs-node guidance + the S117 edge-vs-node rule.

## At session end
Update worklog (S129 entry; **archive the oldest Session-Log entry per rule #8** — after S128's endsession, archive026 holds 2/5, so S124 archives next). Archive this prompt; create the next live track = **BRAN spine BUILD** (the build session this dip specs out). Open question for Matt at that point: build BRAN next, or revisit the parked AEGON-remainder / lower-value NORTH remainder first.

## DO NOT
- Refetch wiki / make any HTTP call · write to `graph/` (read-only dip — 0 mints / 0 edges) · pull Night-King / greenseer-cosmology *theories* into the causal map (gated) · rebuild the NORTH/WO5K Theon-sack nodes (ATTACH) · `/endsession` without explicit permission.
