# Continue — Causal-arc execution: dip-gated refinements (Tywin arc done)

> **Recommended model:** Sonnet 4.6 (graph-only dip + subagent-driven minting). Opus only for a hard interpretive call.
> **Status:** Tier-A (S106) + Tier-B (B1/B2/B3, S107–S108) + Tywin's-death arc (S109) all SHIPPED. The arc layer now spans Purple-Wedding → trial → patricide as one walkable chain. What remains are **dip-gated refinements** — NOT critical gaps. **Do NOT mass-mint. Re-run a fresh arc-weighted dip BEFORE building, to confirm demand.**

## Where this stands (after S109, 2026-06-19)

The causal/narrative-arc **machine is proven 8×**: Robert's Rebellion (S104), Bran's fall (S105), Sack of KL + Purple Wedding (S106), B1 Red-Wedding-upstream + B2 Greyjoy→Theon-ward (S107), B3 Ned's-downfall (S108), **Tywin's-death (S109)**. Strategy + rubric: `working/causal-arc-strategy-2026-06-18.md`. Terms: `reference/narrative-arc-glossary.md`.

**Latest dip:** `working/session-results/2026-06-19-fresh-arc-dip.md` — a FRESH 14-question dip (7 new probes) confirmed the track is NOT at a pause (3 new failures). Q14 (Tywin) was the #1 fumble and is now built + CORRECT. The remaining queue is below.

## The work, in order (each dip-gated — re-run a fresh arc-weighted dip BEFORE building to confirm demand)

### Step A (NEXT) — Q12: Battle of the Blackwater downstream consequences
CHEAPEST real gap. `battle-of-the-blackwater` has 0 causal edges; the node `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` ALREADY EXISTS but isn't wired. Add 2–3 downstream CAUSES (Blackwater → Joffrey sets Sansa aside / wed Margaery; → Stannis retreats to Dragonstone; → Lannister-Tyrell alliance / Tywin Savior of the City). In-saga ACOK Tyrion/Davos + ASOS aftermath. ~2–3 edges, mostly to existing nodes.

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
