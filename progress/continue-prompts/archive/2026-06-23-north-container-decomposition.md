# Continue — NORTH container decomposition dip (the next graph track)

> **Recommended model:** Sonnet 4.6 (read-only research dip + reasoning; same as the WO5K/Essos decomps).
> **This is a READ-ONLY decomposition dip — NO graph mutation, no mints, no edges.** Deliverable is a map +
> ranked-juncture doc, exactly like `working/wo5k-decomposition.md` and `working/essos-decomposition.md`.
> **Prereq:** subagent API healthy (probe one trivial agent first; S121 was 529-blocked).
> **Matt's pick is not locked:** NORTH is the recommended next container (adjacent to the Theon/Winterfell seam
> just built S123), but AEGON or Bran are valid alternatives — if Matt says one of those, swap the target and
> follow the same dip recipe. AEGON has a prereq: fix the `PART_OF war-of-the-five-kings` edge-hygiene bug first.

## Why this is next (state, S123)
The container SET is settled (5: `essos, wo5k, north, aegon, bran`; `working/session-results/2026-06-21-container-SHAPE-map.md`).
**essos ✓ and wo5k ✓ are spine-complete** (Essos S119–120; WO5K-remainder S123 = Q5+J2+J9+J7+J4). The three
remaining containers each need their own decomposition dip before building. **NORTH is the biggest greenfield gap**
and is adjacent to the seam just built (`capture-of-winterfell`/`sack-of-winterfell` are `[wo5k, north]`).

## The task — produce `working/north-decomposition.md`
Run the same decomposition the WO5K and Essos dips ran. Read `working/wo5k-decomposition.md` first as the template
(trigger-tree → juncture scorecard → ranked build order → attach-points map → nodes-to-mint summary → harvest queue).
Output a parallel `working/north-decomposition.md`. Verify every claim against the LOCAL graph (`graph-query.py
--neighbors/--causal-chain`, `event_alias_resolver.py --lookup`) and LOCAL book/wiki cache — **no wiki re-fetch.**

### NORTH scope (from the SHAPE map, §"NORTH")
- **Theater = the Watch + wildling + political North.** NOT "the White Walkers" (sparse in text — do not build a
  Others arc). The political/Watch/wildling causal chains are the target.
- **Jon's arc** is the spine: roots at `execution-of-eddard-stark` (HIT), terminus `jon-is-stabbed-repeatedly`
  (HIT, 0 causal edges yet). Expect junctures: Jon joins the Watch → ranging → Halfhand → among the wildlings →
  Ygritte → returns/defends the Wall → Lord Commander election → Stannis dealings → the Pink Letter → the stabbing.
- **Jon is a SUB-TAG axis:** the SHAPE map calls for tagging Jon's personal-authority nodes `[north, jon]` so
  `--container jon` and `--container north` return meaningfully different sets. Decide the jon-subtag boundary in
  the dip (his command decisions intersect the political theater; the R+L=J parentage thread belongs to WO5K/standalone,
  and the greenseer/TWOW tail is orthogonal — keep those OUT of NORTH).
- **Already-owned by WO5K (do NOT rebuild):** the Theon/Reek capture+sack of Winterfell (built S123 / dual-tagged
  `[wo5k, north]`). **Post-Ramsay-capture** Winterfell nodes (Ramsay's marriage, Theon-as-Reek's arc, the Stannis
  march on Winterfell) are `[north]`-only and ARE in scope.
- **Bridges:** `stannis-retreats-to-dragonstone` (already `[essos? no — wo5k]`) → `stannis-moves-to-the-wall`
  becomes the bridge once built (Stannis answers the Watch's plea). The Pink Letter (`bastard-letter`) is NOT a
  bridge — it references WO5K characters but causes only NORTH-internal events → keep `[north]`.

### Dip deliverable (what `working/north-decomposition.md` must contain)
1. **Current causal state** — verify which NORTH event nodes exist and their causal state (`--neighbors`); list the
   dark junctures. (SHAPE map says ~4 of 6 key junctures MISS — confirm and enumerate.)
2. **Trigger-tree** — the NORTH internal causal map rooted at `execution-of-eddard-stark` (Jon's spine) + the
   Bolton/Stannis political thread.
3. **Juncture scorecard** — score each (Q/S/X/C/B/G, gate ≥7/12) using the rubric in `working/causal-arc-strategy-2026-06-18.md`.
4. **Ranked build order** — cheapest-real-cause first, clean attach+terminus, extends built chains.
5. **Nodes-to-mint summary** + **harvest queue** (POINT, don't extract — push the harvest snippet into any
   text-reading subagent you spawn).

Then **STOP** — the build is a separate session (like WO5K decomp S112 → build S123). Hand off the top-ranked
junctures to a build continue-prompt.

## Hard rules (carry into the build that follows)
- Edge types ONLY: **CAUSES / TRIGGERS / ENABLES / MOTIVATES** (MOTIVATES target = a character). Never invent.
- **FIRM fresh-verify** on every causal edge at build time (read-only subagent CONFIRM vs LOCAL cache; Matt gates at
  policy, not per-edge). Dedup before every mint (`event_alias_resolver.py --lookup` + `grep graph/nodes/events/`).
- No terminus into `war-of-the-five-kings` (hard-stop). Agency-collapse check per juncture. Stamp `containers:`
  (`[north]`, or `[north, jon]` for Jon-authority nodes, or `[wo5k, north]` only at a genuine seam) at mint.
- **Quote rule for research subagents:** quote a SINGLE contiguous substring, never splice across a dialogue
  attribution (`," said X, "`) — that breaks `verify-edge-quotes` (4 such flags in S123, all reworked).

## Vocabulary to paste into subagents (they don't load CLAUDE.md)
Pass = numbered corpus sweep · Track = named workstream · step (lowercase) = ordered piece · Tier = confidence
1–5 ONLY. Containers are frontmatter TAGS, not graph objects. Node aliases = natural SPACED phrases, not kebab.

## DO NOT
Build/mint during the dip (it's read-only) · refetch the wiki · build a White-Walkers/Others arc (out of scope) ·
rebuild the Theon/Reek capture+sack (WO5K owns it) · pull the R+L=J or greenseer threads into NORTH ·
`/endsession` without explicit permission.

## Reference
Template: `working/wo5k-decomposition.md` + `working/essos-decomposition.md`. SHAPE map (NORTH §):
`working/session-results/2026-06-21-container-SHAPE-map.md`. Arc-mint machine (for the build that follows):
`progress/continue-prompts/archive/2026-06-18-causal-arc-execution.md` + `scripts/mint_arc_lib.py` +
`scripts/stamp_containers.py`. Strategy/scorecard rubric: `working/causal-arc-strategy-2026-06-18.md`.
