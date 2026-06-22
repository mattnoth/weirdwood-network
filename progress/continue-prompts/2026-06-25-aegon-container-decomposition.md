# Continue — AEGON container decomposition dip (read-only)

> **Recommended model:** Sonnet 4.6 (1 `general-purpose` dip subagent + a trivial API-health probe; orchestrator coordinates).
> **This is a READ-ONLY DIP — no graph writes.** Local cache only (no HTTP / no wiki refetch). Build is a SEPARATE later session.
> **Pattern:** identical to the NORTH decomp dip (S124 → `working/north-decomposition.md`), the Essos dip (S119), and the WO5K dip (S112). Produce the decomposition doc; the build comes after.

## Why AEGON next (decided S126, subagent-backed)
Container SET = `{essos✓, wo5k✓, north✓, aegon, bran}` (S122). NORTH went spine-complete S126. Of the two remaining, **AEGON is the most beat-ready** (a fresh advisory subagent recommended it over Bran):
- **8+ Golden-Company campaign nodes already on disk**, nested under `landing-of-the-golden-company` via `PART_OF` — ready-made scaffolding to re-type into causal edges (vs Bran, whose mid/late event spine is absent entirely — a full greenfield build).
- Building AEGON **discharges parked debt**: the Varys↔Illyrio conspiracy dyad + the Jorah spy dyad in `working/dyad-queue.md` are explicitly gated on AEGON opening.
- Clean attach to the already-built WO5K / KL-endgame spine (the Kevan/Pycelle assassinations tie back in).

Bran is the runner-up — high narrative value but pure greenfield cost; build after AEGON when there's appetite for a top-to-bottom mint session.

## Task — produce `working/aegon-decomposition.md` (read-only)
Mirror the 8-section structure of `working/north-decomposition.md` (verify every causal-state claim against the LIVE graph + LOCAL book/wiki cache). Sections: (1) current causal state table, (2) full trigger-tree, (3) per-juncture scorecard (6-axis 0–2, gate ≥7/12), (4) sequence-only traps to skip/defer, (5) ranked build order, (6) cross-container attach-points + seams, (7) nodes-to-mint summary table, (8) harvest pointers (POINT, don't extract).

### Inspection starting points (the subagent should verify, not trust)
- `python3 scripts/graph-query.py --container aegon` (currently 2 tagged) + `--neighbors` on key nodes.
- Existing nodes: `ls graph/nodes/events/ | grep -iE "golden-company|aegon|griff|connington|kevan|pycelle|mistwood|griffins-roost|crows-nest|greenstone|rain-house|rooks-rest"` and characters `grep -iE "connington|young-griff|aegon-targaryen|illyrio|haldon|lemore|duckfield|halfmaester"`.
- **The edge bug (note for the BUILD, not this dip):** `grep "PART_OF" graph/edges/edges.jsonl | grep war-of-the-five-kings` — exactly 2 rows are mis-filed AEGON leakage (`landing-of-the-golden-company`, `assassinations-of-pycelle-and-kevan-lannister`). The 8 sub-conquest `PART_OF landing-of-the-golden-company` rows are CORRECT (free scaffolding). Map them in the dip; the build fixes the 2 wrong edges as its step 1.
- `working/dyad-queue.md` (D1 Varys↔Illyrio, + Jorah) — the dip must resolve the **conspiracy-meeting-NODE vs dyad-ONLY** question; default to dyad-only unless a downstream AEGON beat needs the tunnel-meeting as an attach point.

### Likely juncture skeleton to test (~4 junctures — let the dip rank/refine)
1. Varys/Illyrio conspiracy seed (AGOT tunnels) → Aegon revealed to Jon Connington (ADWD *The Lost Lord* / *The Griffin Reborn*).
2. Golden Company contracts/crosses to Westeros.
3. The Stormlands conquest campaign (the 8 nested takings — find the causal parent beyond PART_OF).
4. The KL endgame: assassinations of Kevan + Pycelle (Varys, ADWD epilogue) — ties back to the built KL spine.

### Hard rules (same as the NORTH/WO5K/Essos dips)
- **READ-ONLY.** 0 mints / 0 edges. The deliverable is the decomposition doc + harvest pointers. (Like S124: build is a separate session.)
- Spoiler/tier discipline: Aegon's legitimacy is in-universe contested (mummer's-dragon theory). Keep mapped beats to *what happens* (the landing, the conquests) at Tier 1–2; route any "is he real" claims to the gated theories track, NOT into the causal map.
- Seam discipline: the Stormlands campaign overlaps the post-Blackwater Stormlands — flag seam nodes for dual `[aegon, wo5k]` tags; never plan to re-build WO5K events.
- **Vocabulary (paste into the dip subagent — it doesn't load CLAUDE.md):** edge types are the locked set CAUSES / TRIGGERS / ENABLES / MOTIVATES (+ roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN). "Pass" = corpus sweep; "Track" = named workstream; lowercase "step" = ordered piece; "Tier" = confidence 1–5 ONLY. Don't mint new capitalized terms.
- **Harvest push (paste into the dip subagent):** while reading chapters/wiki for the map, drop one-line `| open | <kind> | <book> | <chapter:line> | <note> | aegon-dip |` pointers into `working/harvest-queue.md` for notable-but-not-task finds (quotes, appearances, food/hospitality, foreshadowing). POINT, don't extract; line-check each cite before appending.

## At session end (the dip)
- Write `working/aegon-decomposition.md`; update worklog (S127 entry) + this prompt → archive; create the AEGON **build** continue prompt as the next live track.
- Hand off the AEGON build (top-ranked junctures first, fresh-verify every causal edge, fix the 2 mis-filed PART_OF edges as step 1) — OR Bran decomp as the alternative pick.

## Reference
Decomp template: `working/north-decomposition.md` (S124) · `working/wo5k-decomposition.md` (S112) · `working/essos-decomposition.md`. Scorecard rubric: `working/causal-arc-strategy-2026-06-18.md`. Container SHAPE map: `working/session-results/2026-06-21-container-SHAPE-map.md`. Dyad queue: `working/dyad-queue.md`. AFFC decoy traps (paste into build subagents): todos.md line ~178 (`conquest-of-dorne`=historical, etc.).
