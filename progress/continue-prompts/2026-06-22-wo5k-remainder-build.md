# Continue — WO5K-remainder arc build (the next build session)

> **Recommended model:** Sonnet 4.6 (orchestration + arc-mint + read-only fresh-verify subagents).
> Opus only for a hard causal adjudication. The decomposition reasoning is already done — this is execution.
> **Prereq:** subagent API healthy (probe one trivial agent first; S121 was 529-blocked).

## Why this is next (decided S122)
The container SHAPE is settled (5 containers: `essos, wo5k, north, aegon, bran`; see
`working/session-results/2026-06-21-container-SHAPE-map.md`). Matt picked **WO5K-remainder to build first**:
it's the only container that's build-ready *today* (no decomp dip needed — `working/wo5k-decomposition.md`
already maps + ranks every juncture), it's seam-safe per the Lens-C analysis, and S122's retro-tagging just
took `--container wo5k` from 2 → 24 nodes, so new mints slot into a live container.

## The build queue (from `working/wo5k-decomposition.md` §5 Ranked Build Order)
J3 (Robb proclaimed King) is **DONE (S113)**. Build the rest in this order:
1. **Q5 — Storming of the Crag → Robb weds Jeyne.** 1–2 edges, nodes mostly exist. Cheapest. Dip-confirm first.
   Attach `storming-of-the-crag` (HIT) → `robb-weds-jeyne-westerling` (HIT). Maybe mint
   `robb-receives-false-news-of-brans-death` — check existence first.
2. **J2+J9 — Blackwater UPSTREAM (highest-salience gap).** 3–4 mints, 5–7 edges. Renly's shadow-death →
   Stannis absorbs host + Littlefinger brokers the Tyrell realignment → both feed `battle-of-the-blackwater`
   (downstream already wired S111). Attach `shadow-assassination-of-renly` (HIT) → `battle-of-the-blackwater`
   (HIT). Completes foreshadowed event #7 (PARTIAL → COMPLETE). Mints: `stannis-absorbs-renly-s-host`,
   `littlefinger-brokers-tyrell-lannister-alliance`, optionally `tyrell-forces-march-to-join-tywin`.
3. **J7 — Karstark execution → Robb isolation.** 1–2 edges, closes a gap between two built B1 segments.
4. **J4 — Balon's invasion → Capture of Winterfell.** 3–4 mints. ⚠ **NORTH seam:** terminates at
   `capture-of-winterfell` / `sack-of-winterfell`, which S122 already dual-tagged `[wo5k, north]`. Build
   under WO5K, do NOT re-tag north (it's there). Two-level agency-collapse (Balon decides; Theon
   sub-decides against orders) — model with MOTIVATES, don't collapse.

## Hard rules for the build (do not skip)
- **Edge types: only CAUSES / TRIGGERS / ENABLES / MOTIVATES** (MOTIVATES target = a character). Never invent.
- **FIRM fresh-verify:** every interpretive/causal edge gets a fresh read-only subagent CONFIRM against the
  LOCAL book/wiki cache before it's committed (Matt does not review individual edges). Gate at policy level.
- **Dedup before every mint:** `event_alias_resolver.py --lookup "<phrase>"` + `grep graph/nodes/events/`.
  The ~200 verbose Plate-3 slugs are the main collision surface.
- **No terminus into `war-of-the-five-kings`** (hard-stop) — arcs end at concrete sub-event nodes.
- **Agency-collapse check** per juncture (see decomp §3 each J). Disaggregate multi-decision chains.
- **Capture quotes / harvest while in the text:** decomp §8 already has an open harvest queue (Balon's
  "iron price" line, the Renly-host-swears-to-Stannis line, etc.) — attach load-bearing quotes as you mint.
- **Stamp containers as you build:** every new WO5K node gets `containers: [wo5k]` at mint time
  (`scripts/stamp_containers.py wo5k <slug>`); J4's Winterfell termini are already `[wo5k, north]`.
- After any node ADD: `weirwood refresh` (rebuild indexes + alias resolver) so new nodes are discoverable.

## Vocabulary to paste into subagents (they don't load CLAUDE.md)
Pass = numbered corpus sweep · Track = named workstream · step (lowercase) = ordered piece · Tier = confidence
1–5 ONLY. Containers are frontmatter TAGS, not graph objects. Node aliases = natural SPACED phrases, not kebab.

## DO NOT
Re-fetch the wiki · build NORTH/AEGON/Bran here (those need their own decomp dips first) · re-tag the
Winterfell seams · run extractions without asking · `/endsession` without explicit permission.

## State (S122, trust worklog.md)
5 containers settled + stamped: `--container` wo5k=24 · essos=16 · north=2 (seams) · aegon=2 · bran=3.
Deferred fold interiors (iron-islands/dorne) + the AEGON `PART_OF war-of-the-five-kings` edge-hygiene bug
are noted in the SHAPE map — not on this build's critical path.
