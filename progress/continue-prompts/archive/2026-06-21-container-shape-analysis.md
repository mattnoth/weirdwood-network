# Continue — Container-SHAPE analysis (dedicated session, subagents ACTIVE)

> **Recommended model:** Sonnet 4.6 (orchestration + 4 read-only lens subagents + synthesis). Opus only for a hard adjudication.
> **Prereq:** the Anthropic subagent API must be healthy — this session was BLOCKED in S121 by a persistent 529 overload (every dispatch died, 0 tool uses). Probe with one trivial agent first; if it 529s, stop and try later.

## Purpose (Matt, S121)
Settle the **SHAPE** of the container partition — *with subagents active* — because the container SET is a
**graph-shape decision**, not a labeling chore. This is its own dedicated session.

## The governing principle — SHAPE > NAMES
Container **names/tags are trivially reversible** (a `containers:` tag is metadata, NOT an umbrella node:
retag = find-replace via `scripts/stamp_containers.py`; it touches **no edges, no causal walk, no derived
artifacts**). So **do NOT agonize over names** — they can be provisional and refactored freely later.

What is EXPENSIVE — and what this session must get right — is the **SHAPE**:
1. **The partition** — what is / isn't a container at all (over-fragmenting into micro-containers is as bad
   as orphaning a whole storyline).
2. **The boundaries** — where each container starts and stops (this determines *where every future arc gets
   built and rooted*).
3. **The seams** — which nodes are dual-membership, and **which container OWNS the build** of each (build-once).
4. **The granularity** — Jon/Bran own-container vs nested-in-NORTH.

**Why shape is the costly axis:** you build arcs (node + edge mints) *under a boundary assumption*. A seam
node built twice, or an arc rooted in the wrong container's spine, is real rework — unlike a tag rename,
which is free. Get the shape roughly right BEFORE mass-building arcs. (This is also why build [Step 3 below]
is a *later* session, gated on this one.)

## STEP 1 — run the 4-lens fan-out (the analysis engine)
Re-dispatch 4 read-only Sonnet `general-purpose` subagents, each: `Read working/session-results/2026-06-21-container-split-BRIEFING.md, then execute LENS <X>`. The briefing names each lens + output file + tells them to PRESSURE-TEST (not echo) the orchestrator proposal.
- **Lens A — partition + scope:** is `{essos, wo5k, north, aegon}` the right SET, or are more needed? Map all 30 foreshadowed events → a container home; scope NORTH + AEGON (root/terminus/junctures). Pressure-test the proposal's claim that `riverlands` + `kl-faith` are also container-sized.
- **Lens B — Jon/Bran granularity:** own-container vs nested-in-NORTH vs hybrid dual-tag.
- **Lens C — seams + build-once ownership:** enumerate every cross-container seam; give the ownership rule (which container builds, which only tags); Theon/Reek verdict.
- **Lens D — retro-grouping:** the ~12 built standalones — tag the clean subset now vs defer; float policy.

## STEP 2 — synthesize the SHAPE map
Fold the 4 lens reports + `working/session-results/2026-06-21-container-split-PROPOSAL.md` into ONE shape
map organized around the 4 shape questions above (partition / boundaries / seams+ownership / granularity).
Keep names provisional. Surface the genuinely-open SHAPE choices for Matt — do NOT pick the SET yourself.

## STEP 3 — Matt decides the SET (shape-first)
Present the synthesis; Matt picks the partition + boundaries + seam-ownership + granularity. Names can be
tentative and changed later. THEN (mechanical, after his call): `stamp_containers.py` the agreed tags +
retro-tag the clean subset. Do NOT tag before the shape is settled.

## AFTER this session (separate build session — NOT here)
Build arcs with settled boundaries — WO5K-remainder is seam-safe (Blackwater-upstream J2+J9 · Karstark J7 ·
Balon→Winterfell J4 [SKIP J6], `working/wo5k-decomposition.md`), or whichever container the shape session
prioritizes (NORTH is the biggest greenfield gap). Arc-mint machine + the FIRM fresh-verify rule apply.

## State (S121, trust worklog.md)
nodes 8,574 · edges 22,384 · edge types 132 · vocab 169. Step 1 hardening DONE (`--full-chain`/`--expand-beats`/`--container` shipped; `containers:` field live; 15 Essos nodes tagged). Concept reference: `graph-concepts-explainer.md` (gitignored). Reversibility facts: see `[[project_containers_field_and_query_modes]]` (memory).

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase ordered piece) · Tier (confidence 1–5 ONLY). Containers are TAGS, not graph objects. Source: `reference/glossary.md`.

## DO NOT
Re-fetch the wiki · invent edge types · use kebab aliases (SPACED phrases) · let names block a shape decision (names are cheap) · tag containers before the shape is settled · build arcs this session (shape first) · run `/endsession` without explicit permission.
