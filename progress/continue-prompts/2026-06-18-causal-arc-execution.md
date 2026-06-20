# Continue — Causal-arc: planned major-arc backlog (STRATEGY PIVOTED S112)

> **Recommended model:** Sonnet 4.6 (subagent-driven minting). Opus only for a hard interpretive call.
> **STRATEGY PIVOTED (S112, 2026-06-20):** the track is **no longer dip-cheapest-driven.** S111's 3-edge session exposed that the dip ranks by *cheapest gap* and was scraping refinements while the major arcs stayed dark (causal layer reaches only ~8% of event nodes; zero AFFC/ADWD). **New model = two tracks:** PRIMARY = a planned, magnitude-ordered **major-arc backlog** (`working/major-arc-backlog.md`, anchored on the 30 foreshadowed events) + **container decomposition dips**; SECONDARY = opportunistic cheap dips (`working/cheap-dip-backlog.md`). **The dip is now a post-build CHECK, not the prioritizer.** Full rationale: worklog S112 + `history/session-details/session-112.md`.

## Where this stands (after S112, 2026-06-20)

The arc machine is proven 9× (RR, Bran, Sack, PW, B1, B2, B3, Tywin, Blackwater-downstream). The WO5K **container** has been decomposed (`working/wo5k-decomposition.md`) — it's a trigger-tree rooted at `death-of-robert-baratheon`, with 6–10 real junctures, ranked. **NEXT BUILD = J3 below.** Cross-book chains auto-join via shared nodes + the `--causal-chain` walk (chain-as-arc, no umbrella) — so root each new arc at its existing upstream node.

## J3 DONE (S113, 2026-06-20) — NEXT = AFFC smoke test, then Q5

**J3 Robb-proclaimed-King-in-the-North SHIPPED:** minted `robb-proclaimed-king-in-the-north` (event.ceremony, AGOT Catelyn XI) + 3 edges (`execution-of-eddard-stark CAUSES` it + `execution-of-eddard-stark MOTIVATES robb-stark`, both Tier-2 fresh-subagent CONFIRMED + `robb-stark AGENT_IN` Tier-1). `scripts/mint_robb_king_arc.py`. Bran spaced-alias fix done (corrected target — "bran's fall" → `jaime-pushes-bran-from-the-tower`, the fall node; `assassination-of-tywin-lannister` "tyrion kills tywin" was already present). `robert-orders-daenerys-assassination` mint still deferred to the Essos bridges. S113 also ran the harvest settling pass (folded in the parallel demo-window's 9 attachments incl. the Ned-execution `## Quotes`; 5 net-new; 6 rows left open).

## NEXT (Matt's steer, S113 endsession) — AFFC smoke test FIRST

The causal layer has **~zero AFFC/ADWD coverage** (S112 note: causal reaches ~8% of event nodes, all AGOT–ASOS). Before building the next arc, run a **read-only smoke test** to find where AFFC arc-shaped queries go dark — this is the S112 "dip-as-check" used as a *prioritizer* for the next book's worth of arcs.

**How:** run the Loremaster demo (`working/demo-asoiaf-loremaster.md`) and/or an arc-weighted dip against **AFFC-centric arc-queries** — e.g. Cersei's downfall (small-council paranoia → arming the Faith → her own walk of atonement), Brienne's hunt → Lady Stoneheart, the Kingsmoot → Euron seizing the Seastone Chair → Reach raids, Dorne / Myrcella / the Sand Snakes' vengeance plot, Greyjoy succession. Grade each: does `--causal-chain` / `--neighbors` return a walkable arc, or is it dark? Record fumbles in `working/session-results/<date>-affc-smoke.md`. **The demo doubles as QA (Matt's S112 note #1) — it surfaces bare nodes** (e.g. `gregor-confesses-and-kills-oberyn` is bare → harvest-queue row open). **Demo prompt must NOT spoiler-check** (gating deferred; already fixed in the demo file). Output = a ranked AFFC fumble list that **re-prioritizes the next build** (it may bump Q5).

## NEXT BUILD (after the smoke test) — default Rank 2 / Q5: Storming of the Crag → Robb weds Jeyne

"Why did Robb marry Jeyne?" — the B1 chain bottoms out at the marriage. Both `storming-of-the-crag` AND `robb-weds-jeyne-westerling` exist → likely a **1-edge wire** (`storming-of-the-crag CAUSES robb-weds-jeyne-westerling`), maybe + 1 intermediate mint (`robb-receives-false-news-of-brans-death`? check existence). **Dedup-check `battle-of-the-crag` vs `storming-of-the-crag` FIRST.** Theory-loaded (Sybell Spicer / moon-tea reading) — Matt flagged: do NOT lose. In-saga ASOS (Catelyn/Jaime POV recall). Then re-dip-check. Full ranked queue (#3 Blackwater-upstream J2+J9 Renly→Stannis→Tyrell · #4 Karstark→Robb-isolation J7 · #5 Balon→Winterfell J4; SKIP westerlands battle sequence J6) + scopes + attach-points: `working/wo5k-decomposition.md`.

## (historical) The pre-pivot dip queue — superseded by the backlog above, kept for reference

**Q12 Battle-of-the-Blackwater downstream ✅ DONE (S111)**: `battle-of-the-blackwater` 0→3 downstream CAUSES (→ joffrey-sets-sansa-aside [existing] / stannis-retreats-to-dragonstone / tywin-named-savior-of-the-city); `scripts/mint_blackwater_arc.py`.

## (historical) Where this stood (after S109, 2026-06-19)

The causal/narrative-arc **machine is proven 8×**: Robert's Rebellion (S104), Bran's fall (S105), Sack of KL + Purple Wedding (S106), B1 Red-Wedding-upstream + B2 Greyjoy→Theon-ward (S107), B3 Ned's-downfall (S108), **Tywin's-death (S109)**. Strategy + rubric: `working/causal-arc-strategy-2026-06-18.md`. Terms: `reference/narrative-arc-glossary.md`.

**Latest dip:** `working/session-results/2026-06-19-fresh-arc-dip.md` — a FRESH 14-question dip (7 new probes) confirmed the track is NOT at a pause (3 new failures). Q14 (Tywin) was the #1 fumble and is now built + CORRECT. The remaining queue is below.

## (historical, pre-S112-pivot) The old dip queue — SUPERSEDED by the major-arc backlog + WO5K decomposition above. Kept for reference only.

### Q12: Battle of the Blackwater downstream consequences ✅ DONE (S111)
SHIPPED 2026-06-20: `battle-of-the-blackwater` 0→3 downstream CAUSES (→ `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` [existing] / → `stannis-retreats-to-dragonstone` [new] / → `tywin-named-savior-of-the-city` [new]); all Tier-2 fresh-subagent CONFIRMED. `scripts/mint_blackwater_arc.py`.

### Q5: `robb-weds-jeyne-westerling` upstream (now a SECONDARY cheap dip — `working/cheap-dip-backlog.md`; also = WO5K decomposition #2)
"Why did Robb marry Jeyne?" — the B1 chain bottoms out at the marriage. Both `storming-of-the-crag` AND `robb-weds-jeyne-westerling` exist — likely a **1-edge wire** (`storming-of-the-crag CAUSES robb-weds-jeyne-westerling`). **Dedup-check `battle-of-the-crag` vs `storming-of-the-crag` first.** Theory-loaded (Sybell Spicer / moon-tea reading) — Matt flagged: do NOT lose. Build between major arcs or when a session ends light.

### Step B — Q11: Daenerys / fall of Astapor → Slaver's Bay campaign
NEW Essos territory (no prior arc there). `fall-of-astapor` has 0 causal edges; the campaign sub-battles exist as PART_OF but no causal spine; `targaryen-campaign-in-slavers-bay` has an alias gap ("Daenerys conquest of Slaver's Bay" misses). Larger: ~3–5 beats + 4–6 edges. In-saga ASOS Daenerys.

### Step C — Q5: `robb-weds-jeyne-westerling` upstream (extends B1)
"Why did Robb marry Jeyne?" is unplumbed — the B1 chain bottoms out at the marriage. Add the storming-of-the-Crag beat (Robb wounded → Jeyne nurses him → he dishonors the Frey betrothal). ~1–2 beats, in-saga ASOS (Catelyn/Jaime POV recall).

### Also-confirmed (lower): Q6 Trident inbound CAUSES (1 edge: `roberts-rebellion CAUSES battle-of-the-trident`) · Q13 Sack-of-Winterfell (extends B2 downstream, 2–3 beats) · Q7 `execution-of-eddard-stark` downstream (separate consequences shape) · Tywin-death downstream (Cersei regency / Tommen — needs intermediate nodes first).

**If a fresh arc-weighted dip shows none of these as a real fumble, the track is at a natural pause** — archive this prompt and move to another track (theory-node layer, TWOIAF ingestion for deep-lore wiki-only wars, etc.).

## The proven arc-mint machine (reuse for every arc)
1. **Research subagent** (read-only, local cache): identify reader-load-bearing beats; **dedup-check each** via `python3 scripts/event_alias_resolver.py --lookup "<phrase>"` + grep `graph/nodes/events/`; gather VERBATIM chapter quotes with `file:line`; propose nodes + role/causal edges. **VERIFY the agent's claims against `edges.jsonl` / `--neighbors`, NOT the stale node-file `## Edges` prose** (research agents repeatedly mis-read stale display bullets — wrong canonical hub, "missing" dyad that existed, mis-cited quote, wrong slugs). **PASTE the canonical harvest snippet** (from `working/harvest-queue.md` § "Paste-into-every-dip/research-subagent-prompt snippet") into this subagent's prompt — subagents don't load CLAUDE.md, so the harvest instruction must be pushed.
2. **Orchestrator trims + mints** via a `scripts/mint_<arc>_arc.py` script (backup `edges.jsonl` to `_regrounding/` + re-run guard). Write beat-node `.md` files directly (prose + `## Quotes` + aliases). **Aliases MUST be natural SPACED phrases ("death of Tywin"), NOT kebab slugs ("death-of-tywin")** — the resolver's `normalize()` keeps hyphens, so a kebab alias only matches a kebab query and a reader's "death of Tywin" never resolves (S109 lesson; older arc nodes incl. B3 have this latent gap, discoverable only via their spaced node-NAME). If you REPAIR an existing wiki-derived hub (wrong type / empty aliases / junk `## Edges` infobox prose like `DEFEATS`/`FIGHTS_IN`), fix the frontmatter type + add spaced aliases + clean the prose in the same pass.
3. **Rebuild** targeted indexes (`build-entity-indexes.py --type events --slug <s>`) + `event_alias_resolver.py --build`.
4. **Fresh-subagent verify** each causal edge + agency modeling vs local cache; mint causal edges with `verified_by: pending-*`, stamp `subagent-local-source-check-<date>` on CONFIRM.
5. **Smoke-test** `graph-query.py --causal-chain <terminus>` + natural-phrase discoverability; then re-dip. **The dip subagent ALSO gets the canonical harvest snippet pasted in** (it reads chapter/wiki cache to grade — prime territory for incidental finds). Harvest is part of *every* prompt that reads the text, not just arc research.
6. **Harvest sweep before finishing:** home any *load-bearing* quotes the research agent surfaced that lack a beat-node home (attach to the relevant node `## Quotes`), and confirm incidental finds (food/descriptions) landed in `working/harvest-queue.md` for a later harvest pass. (Capture-quotes rule + the harvest-queue convention.)

## Policy / guardrails (FIRM)
- **Tier:** causal edges capped **Tier-2** (interpretive link); role edges Tier-1. (Tier = confidence 1–5 ONLY.)
- **CAUSES** = mediated; **TRIGGERS** = immediate specific spark; **MOTIVATES** = event/condition → actor; **PRECEDES** = pure chronology (NOT causal).
- **Pre-mint dedup mandatory.** **Agency-collapse check** before any `A CAUSES B`. Don't assert a frame as fact.
- **Hard-stop:** don't chain CAUSES into a multi-attributed terminus (e.g. `→ war-of-the-five-kings` — staying causal-dark is correct-by-policy).
- **`event.conspiracy` is fine as a CAUSAL beat** (carries conspirators' agency via role edges) — just never as a SUB_BEAT_OF umbrella parent (chain-as-arc, S106).
- **Verification (FIRM, Matt):** interpretive/causal edges verified by fresh subagents vs LOCAL cache; never re-fetch; Matt gates at policy level, not per-edge.

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase, ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`.

## Small fixes surfaced (→ working/todos.md § Small Fixes, not blocking)
- `robert-baratheon` / `robert-i-baratheon` dup (B3 used `robert-baratheon`, the in-saga node, for the death beat; merge the wiki/historical `robert-i-baratheon` into it).
- (prior) `greyjoys-rebellion` dup of canonical `greyjoy-rebellion`; sack-hub junk `DEFEATS` edge; `roberts-rebellion`/`dance-of-the-dragons` mistyped `event.battle`.
