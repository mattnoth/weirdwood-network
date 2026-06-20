# Continue — Causal-arc execution: dip-gated refinements (Tier-B done)

> **Recommended model:** Sonnet 4.6 (graph-only dip + subagent-driven minting). Opus only for a hard interpretive call.
> **Status:** Tier-A (S106) + Tier-B (B1/B2/B3, S107–S108) all SHIPPED. The arc layer now answers **8 of 10** arc-weighted dip questions correctly (1 policy-stop-short, 2 partial). What remains are **refinements, dip-gated** — NOT critical gaps. **Do NOT mass-mint.**

## Where this stands (after S108, 2026-06-19)

The causal/narrative-arc **machine is proven 7×**: Robert's Rebellion (S104), Bran's fall (S105), Sack of King's Landing + Purple Wedding (S106), B1 Red-Wedding-upstream + B2 Greyjoy→Theon-ward (S107), **B3 Ned's-downfall (S108)**. Strategy + rubric: `working/causal-arc-strategy-2026-06-18.md`. Terms: `reference/narrative-arc-glossary.md`.

**Latest dip:** `working/session-results/2026-06-19-post-b3-redip.md` — Q10 (Ned's execution) and Q8 (Greyjoy→Theon) both upgraded to CORRECT. The two remaining partials are refinements.

## The work, in order (each dip-gated — re-dip BEFORE building to confirm demand)

### Step A (NEXT, optional) — Q7 refinement: `robb-weds-jeyne-westerling` upstream
The B1 Red-Wedding chain bottoms out at `robb-weds-jeyne-westerling` with no upstream — "why did Robb marry Jeyne?" is unplumbed. Add the 1–2 beats that led there (the fall of the Crag / Jeyne nursing a wounded Robb → Robb dishonors the Frey betrothal). Extends B1; closes the one strict-reading partial. ~1–2 beats. In-saga ASOS (Robb is off-page; Catelyn/Jaime POV recall + the Westerling material).

### Step B (optional) — Q3 refinement: Battle of the Trident inbound CAUSES
`battle-of-the-trident` has only `PART_OF roberts-rebellion` + `PRECEDES` — no inbound CAUSES, so `--causal-chain` can't answer "what caused the Trident." Add `roberts-rebellion CAUSES battle-of-the-trident` (or a PRECEDES→CAUSES promotion for the load-bearing junctures). 1 edge.

### Step C (lower priority) — `execution-of-eddard-stark` downstream consequences
The execution has no downstream causal edges (Robb crowned, war escalates, Arya on the run…). The asked Q10 facet (blame/cause) is covered; consequences are a separate "what did X lead to" shape. Defer unless a dip shows demand.

**If none of these surface as a real fumble in a fresh arc-weighted dip, the causal-arc track is at a natural pause** — archive this prompt and move to another track (theory-node layer, TWOIAF ingestion for deep-lore wiki-only wars, etc.).

## The proven arc-mint machine (reuse for every arc)
1. **Research subagent** (read-only, local cache): identify reader-load-bearing beats; **dedup-check each** via `python3 scripts/event_alias_resolver.py --lookup "<phrase>"` + grep `graph/nodes/events/`; gather VERBATIM chapter quotes with `file:line`; propose nodes + role/causal edges. **VERIFY the agent's claims against `edges.jsonl` / `--neighbors`, NOT the stale node-file `## Edges` prose** (research agents repeatedly mis-read stale display bullets — wrong canonical hub, "missing" dyad that existed, mis-cited quote, wrong slugs). **PASTE the canonical harvest snippet** (from `working/harvest-queue.md` § "Paste-into-every-dip/research-subagent-prompt snippet") into this subagent's prompt — subagents don't load CLAUDE.md, so the harvest instruction must be pushed.
2. **Orchestrator trims + mints** via a `scripts/mint_<arc>_arc.py` script (backup `edges.jsonl` to `_regrounding/` + re-run guard). Write beat-node `.md` files directly (prose + `## Quotes` + natural-phrase aliases for discoverability).
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
