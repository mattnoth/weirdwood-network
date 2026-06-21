# Continue — Causal-arc: planned major-arc backlog (STRATEGY PIVOTED S112)

> **Recommended model:** Sonnet 4.6 (subagent-driven minting). Opus only for a hard interpretive call.
> **STRATEGY PIVOTED (S112, 2026-06-20):** the track is **no longer dip-cheapest-driven.** S111's 3-edge session exposed that the dip ranks by *cheapest gap* and was scraping refinements while the major arcs stayed dark (causal layer reaches only ~8% of event nodes; zero AFFC/ADWD). **New model = two tracks:** PRIMARY = a planned, magnitude-ordered **major-arc backlog** (`working/major-arc-backlog.md`, anchored on the 30 foreshadowed events) + **container decomposition dips**; SECONDARY = opportunistic cheap dips (`working/cheap-dip-backlog.md`). **The dip is now a post-build CHECK, not the prioritizer.** Full rationale: worklog S112 + `history/session-details/session-112.md`.

## (historical) Where this stood (after S112, 2026-06-20)

The arc machine is proven 9× (RR, Bran, Sack, PW, B1, B2, B3, Tywin, Blackwater-downstream). The WO5K **container** has been decomposed (`working/wo5k-decomposition.md`) — it's a trigger-tree rooted at `death-of-robert-baratheon`, with 6–10 real junctures, ranked. (J3 was the S113 build; AFFC builds followed S114–S115 — see the live NEXT BUILD section below.) Cross-book chains auto-join via shared nodes + the `--causal-chain` walk (chain-as-arc, no umbrella) — so root each new arc at its existing upstream node.

## (historical) AFFC SMOKE TEST + Cersei's-downfall arc DONE (S114, 2026-06-20)

**AFFC smoke test SHIPPED** (`working/session-results/2026-06-20-affc-smoke.md`): all 5 AFFC arc-clusters causally DARK (0+0); controls HIT (genuine coverage gap). Ranked fumble list: **#1 Cersei's downfall · #2 Kingsmoot→Euron · #3 Brienne→Stoneheart · #4 Dorne/Myrcella.** Two orthogonal findings: AFFC natural-phrase **discoverability broken** (spaced-alias gap) + **3 node traps** (`faith-militant-uprising`=historical Aenys/Maegor; `brienne-arrested`=ASOS Harrenhal; `conquest-of-dorne`=Aegon's). **Bumped Q5** as predicted.

**Cersei's-downfall arc SHIPPED (smoke-test #1):** 2 beats (`cersei-rearms-the-faith-and-forgives-the-debt`, `osney-kettleblack-confesses-to-high-sparrow`) + 5 causal Tier-2 (fresh-subagent CONFIRMED) + 5 role Tier-1. Self-caused irony: `cersei-rearms-the-faith CAUSES cersei-is-captured-in-the-sept CAUSES cersei-is-stripped-and-imprisoned`; backfire `cersei-plots-against-margaery CAUSES osney-confesses TRIGGERS capture`. Spaced aliases added to all wired nodes; `LOCATED_AT` data fix. `scripts/mint_cersei_downfall_arc.py`. AFFC layer no longer 100% dark.

## AFFC #2 Kingsmoot → Euron DONE (S116) — NEXT = AFFC #4 Dorne/Myrcella

**S116 SHIPPED** the standalone Kingsmoot→Euron arc (J8): 2 new beats (`death-of-balon-greyjoy` [event.death], `euron-seizes-the-seastone-chair` [event.incident]) + `kingsmoot-on-old-wyk` retyped event.battle→event.ceremony + spaced aliases + repaired junk-stub + 11 edges (4 causal Tier-2 fresh-subagent CONFIRMED + 7 role Tier-1). Spine: `death-of-balon-greyjoy TRIGGERS euron-seizes-the-seastone-chair CAUSES kingsmoot-on-old-wyk CAUSES taking-of-the-shields`; agency `euron-seizes MOTIVATES aeron-greyjoy`. **Root-check: 0-upstream DECLARED INTENTIONAL** (Balon's death is the prime mover — the genuine standalone exception, machine 5b). **TRAP avoided:** `anarchy-in-the-reach` = the HISTORICAL Gardener-era Reach succession war, NOT Euron's invasion — downstream redirected to the real node `taking-of-the-shields`. SKIP: `victarion-admits-euron-s-role-in-his-wife-s-death` (tangential backstory; the "Euron murdered Balon" link is Tier-4/5 theory). `scripts/mint_kingsmoot_euron_arc.py`. **Dedicated harvest pass RAN (23 rows attached; 6 intended-skip remain: 117 wrong-cite + 142–145 Essos-gated).**

## NEXT BUILD (S116 endsession pick): AFFC #4 Dorne / Myrcella

The last AFFC smoke-test fumble (#4). Likely **1–2 mints** + edges:
- `myrcella-wounded` (the maiming during the failed Queenmaker plot to crown her) — MISS today, needs mint.
- `arrest-of-the-sand-snakes` EXISTS but was bare; got a `## Quotes` via harvest row 160 this session — wire Doran's-response causation.
- The Queenmaker/Arianne plot beats. Source: AFFC Dorne chapters (The Queenmaker / The Soiled Knight / Arys/Arianne, Areo Hotah POVs). Use SPACED aliases.
- **TRAP (hard):** `conquest-of-dorne` = **Aegon's historical conquest of Dorne**, NOT the AFFC Queenmaker plot. Do not wire to it. (Same AFFC trap-class as `anarchy-in-the-reach`/`faith-militant-uprising`/`brienne-arrested` — always dedup-check the era of a same-named wiki node before wiring.)

**Also queued:** **Secondary cheap dip Q5** (`storming-of-the-crag CAUSES robb-weds-jeyne-westerling`, ASOS; dedup-check `battle-of-the-crag` first; theory-loaded Sybell-Spicer/moon-tea — do-not-lose). WO5K junctures (#3 Blackwater-upstream J2+J9 · #4 Karstark J7 · #5 Balon→Winterfell J4; SKIP J6): `working/wo5k-decomposition.md`. Harvest queue at 6 open (5 real: 1 wrong-cite to re-resolve + 4 Essos-bridge rows gated to a future Essos arc).

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
5b. **ROOT-CHECK (MANDATORY, S115 lesson)** — after the smoke-test, run `graph-query.py --causal-chain <arc-EARLIEST-beat>` and confirm it has causal **upstream** (i.e. the new arc roots at an existing prior node, per the "root each new arc at its existing upstream node" discipline). **0 upstream = a likely missed cross-book auto-join** — find the true antecedent and mint the 1 rooting edge (the S114 Cersei arc shipped self-contained because this check didn't exist; S115 had to bolt on `assassination-of-tywin-lannister CAUSES cersei-rearms-the-faith`). **EXCEPTION — genuinely standalone arcs:** some arcs legitimately have no upstream (e.g. AFFC #2 Kingsmoot→Euron roots at `death-of-balon-greyjoy`, which is itself a standalone trigger; pre-series sparks like `greyjoy-rebellion`). For those, 0 upstream is CORRECT — but you must **explicitly state in the worklog entry that the 0-upstream is intentional and why**, so it reads as a decision, not an oversight. Rule of thumb: if a prior-book event plausibly *enabled* the arc's first beat, root it; if the first beat is itself the prime mover, declare it standalone.
6. **Harvest sweep before finishing:** home any *load-bearing* quotes the research agent surfaced that lack a beat-node home (attach to the relevant node `## Quotes`), and confirm incidental finds (food/descriptions) landed in `working/harvest-queue.md` for a later harvest pass. (Capture-quotes rule + the harvest-queue convention.)

## Policy / guardrails (FIRM)
- **Tier:** causal edges capped **Tier-2** (interpretive link); role edges Tier-1. (Tier = confidence 1–5 ONLY.)
- **CAUSES** = mediated; **TRIGGERS** = immediate specific spark; **MOTIVATES** = event/condition → actor; **PRECEDES** = pure chronology (NOT causal).
- **Pre-mint dedup mandatory.** **Agency-collapse check** before any `A CAUSES B`. Don't assert a frame as fact.
- **Hard-stop:** don't chain CAUSES into a multi-attributed terminus (e.g. `→ war-of-the-five-kings` — staying causal-dark is correct-by-policy).
- **Root-check (S115):** every new arc's earliest beat must EITHER root at an existing upstream node (mint the rooting edge) OR be explicitly declared standalone in the worklog with a reason. 0-upstream-by-default is a bug, not a default — see machine step 5b.
- **`event.conspiracy` is fine as a CAUSAL beat** (carries conspirators' agency via role edges) — just never as a SUB_BEAT_OF umbrella parent (chain-as-arc, S106).
- **Verification (FIRM, Matt):** interpretive/causal edges verified by fresh subagents vs LOCAL cache; never re-fetch; Matt gates at policy level, not per-edge.

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase, ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`.

## Small fixes surfaced (→ working/todos.md § Small Fixes, not blocking)
- `robert-baratheon` / `robert-i-baratheon` dup (B3 used `robert-baratheon`, the in-saga node, for the death beat; merge the wiki/historical `robert-i-baratheon` into it).
- (prior) `greyjoys-rebellion` dup of canonical `greyjoy-rebellion`; sack-hub junk `DEFEATS` edge; `roberts-rebellion`/`dance-of-the-dragons` mistyped `event.battle`.
