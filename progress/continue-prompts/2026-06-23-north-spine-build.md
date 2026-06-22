# Continue — NORTH spine build (top-3 junctures from the decomp dip)

> **Recommended model:** Sonnet 4.6 subagents for research/verify; orchestrator coordinates. (Same recipe as the
> WO5K-remainder build, S123.)
> **This is a BUILD session — it mutates the graph** (mints nodes + edges). Read-only decomp is DONE (S124).
> **Prereq:** subagent API healthy (probe one trivial agent first; S121 was 529-blocked).

## State (S124)
The NORTH **decomposition dip is DONE** (read-only) → `working/north-decomposition.md` (603 lines, the trigger-tree +
juncture scorecard + ranked build order + attach-points + nodes-to-mint + harvest §8). **Read it first — it is the spec.**
The container SET is settled (5: `essos✓, wo5k✓, north, aegon, bran`). `essos` + `wo5k` are spine-complete;
**NORTH is greenfield** with two spines (Jon's Watch arc + the Bolton/Stannis political thread).

## The task — build the top-3 ranked NORTH junctures (in order), fresh-verifying every causal edge
Build N5 → N2 → N1 (cheapest-real-cause / clean-attach first). **3 mints total for the top-3.** Use the proven
arc-mint machine (research dip → `scripts/mint_*_arc.py` → fresh-verify → `verify-edge-quotes.py` → index/alias
rebuild → `stamp_containers.py` → `--causal-chain` smoke). Lib: `scripts/mint_arc_lib.py` (`precheck_slugs`).

### N5 (Rank 1, score 11/12) — Red Wedding → Roose named Warden (Bolton-thread entry)
- **1 mint:** `roose-named-warden-of-the-north` (event.ceremony/incident — pick per the text; ASOS/AFFC). **2 edges:**
  `red-wedding CAUSES roose-named-warden-of-the-north` + `MOTIVATES roose-bolton` (his Frey turn → the wardenship reward).
- Attach: `red-wedding` (HIT, built). Container tag `[north]`. This opens the whole Bolton political spine.

### N2 (Rank 2, score 11/12) — Wall battle → Stannis defeats wildlings (the NORTH pivot)
- **2 mints:** `stannis-defeats-wildlings-at-the-wall` + the bridge `stannis-moves-to-the-wall` (`[wo5k, north]` seam —
  Stannis answers the Watch's plea; this is the WO5K↔NORTH bridge). **CHECK FIRST:** `battle-beneath-the-wall` may
  already be the right node for "Stannis routs the wildlings" — enrich it instead of minting a duplicate (boundary
  call flagged in the dip). Attach at `attack-on-castle-black` (HIT). Tag the new ADWD-Jon authority beats `[north, jon]`.

### N1 (Rank 3, score 10/12) — Great Ranging → Fist → Craster's mutiny
- **0 mints.** `great-ranging.node.md` already DECLARES the two CAUSES edges in its `## Edges` prose but they are
  **NOT in `edges.jsonl`** (a Plate-3 staging-vs-live gap — orchestrator confirmed: `grep great-ranging edges.jsonl` = 0).
  **Wire the declared edges directly** (great-ranging → fight-at-the-fist → mutiny-at-crasters-keep), fresh-verify the
  quotes, + 3 container tags `[north]`/`[north, jon]`. Highest beat-readiness of any juncture.

## Boundary calls to resolve at build (from the dip)
1. **`great-ranging` staging-vs-live:** wire the declared edges, don't re-mint.
2. **Dedup `mutiny-at-castle-black` ↔ `jon-is-stabbed-repeatedly`** (likely the SAME ADWD event) BEFORE touching the
   stabbing terminus. `mutiny-at-crasters-keep` is the DISTINCT ASOS Mormont mutiny — keep separate.
3. **Add `[north]`** to 3 WO5K-tagged NORTH-theater nodes: `robb-proclaimed-king-in-the-north`,
   `ironborn-invasion-of-the-north`, `balon-declares-himself-king` (Matt-confirm at build).
4. `battle-beneath-the-wall` enrich-vs-mint (see N2).

## Hard rules
- Edge types ONLY: **CAUSES / TRIGGERS / ENABLES / MOTIVATES** (MOTIVATES target = a character). Never invent.
- **FIRM fresh-verify** on every causal edge (separate read-only subagent CONFIRM vs LOCAL cache; Matt gates at policy,
  not per-edge). **Dedup before every mint** (`event_alias_resolver.py --lookup` + `grep graph/nodes/events/`).
- Granularity policy (S120): a constitutive beat gets `SUB_BEAT_OF` only, NO causal edge; a prior PREREQUISITE gets
  CAUSES/TRIGGERS. Agency-collapse check per juncture. No terminus into `war-of-the-five-kings` (hard-stop).
- Stamp `containers:` at mint (`[north]`, `[north, jon]` for Jon-authority beats, `[wo5k, north]` only at a genuine seam;
  never `[]`). Node aliases = natural SPACED phrases, not kebab.
- **Quote rule for research subagents:** quote a SINGLE contiguous substring, never splice across a dialogue
  attribution (`," said X, "`) — it breaks `verify-edge-quotes` (4 such flags in S123).
- Rebuild indexes + alias-resolver after any node ADD/RENAME (`weirwood refresh` / `scripts/build-entity-indexes.py`
  + `event_alias_resolver.py`).

## Vocabulary to paste into subagents (they don't load CLAUDE.md)
Pass = numbered corpus sweep · Track = named workstream · step (lowercase) = ordered piece · Tier = confidence 1–5 ONLY.
Containers are frontmatter TAGS, not graph objects. Node aliases = natural SPACED phrases.

## DO NOT
Refetch the wiki (cache is local at `sources/wiki/_raw/`) · build a White-Walkers/Others arc (out of scope) · rebuild
the Theon/Reek capture+sack (WO5K owns it) · pull R+L=J or the greenseer/TWOW thread into NORTH · mass-mint (top-3 only,
re-dip after) · `/endsession` without explicit permission.

## At session end
Update worklog (S125 entry + totals), migrate the 10 dip-§8 harvest pointers if running a harvest pass, archive this
prompt, and hand off the NEXT NORTH junctures (or pivot to AEGON/Bran decomp — Matt picks).

## Reference
Spec: `working/north-decomposition.md`. Template build: worklog S123 (WO5K-remainder). Arc-mint machine:
`progress/continue-prompts/archive/2026-06-18-causal-arc-execution.md` + `scripts/mint_arc_lib.py` +
`scripts/stamp_containers.py`. Scorecard rubric: `working/causal-arc-strategy-2026-06-18.md`. SHAPE map (NORTH §):
`working/session-results/2026-06-21-container-SHAPE-map.md`.
