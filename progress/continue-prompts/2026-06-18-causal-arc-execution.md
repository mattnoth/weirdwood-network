# Continue — Causal-arc execution: B3 (Ned's downfall), then re-dip

> **Recommended model:** Sonnet 4.6 (graph-only dip + subagent-driven minting). Opus only for a hard interpretive call.
> **Status:** dip-driven Tier-B execution ongoing. Dip + B1 + B2 SHIPPED (S107). Next = **B3 (Ned's-downfall arc)**, the richest remaining gap, then a re-dip.

## Where this stands (after S107, 2026-06-19)

The causal/narrative-arc **machine is proven 6×**: Robert's Rebellion (S104), Bran's fall (S105), Sack of King's Landing + Purple Wedding (S106), **B1 Red-Wedding-upstream + B2 Greyjoy→Theon-ward (S107)**. Strategy + rubric: `working/causal-arc-strategy-2026-06-18.md` (read first). Terms: `reference/narrative-arc-glossary.md`.

**DONE in S107:**
- **Arc-weighted dip** (`working/session-results/2026-06-19-arc-weighted-dip.md`): 5 correct / 3 partial / 2 failed; all 4 prior arcs validated. Re-ranked Tier B.
- **B1 — Red Wedding upstream** (the Q7 fumble): 5 beats, 21 edges, two parallel chains (Catelyn-frees-Jaime→Karstark-murders→execution; Robb-weds-Jeyne→conspiracy→red-wedding/robb-is-killed). Mint: `scripts/mint_b1_red_wedding_arc.py`.
- **B2 — Greyjoy→Theon-ward** (re-dip Q8 partial): 1 beat, 5 edges (`greyjoy-rebellion CAUSES theon-greyjoy-taken-as-ward`). Mint: `scripts/mint_b2_greyjoy_theon_arc.py`.
- **Post-build re-dip** (`…-arc-weighted-redip.md`): 6 correct / 3 partial / 0 failed; **Q7 confirmed fixed**.

## The work, in order

### Step A (NEXT) — build B3: the Ned's-downfall arc
The re-dip's clearest remaining gap (Q10): `execution-of-eddard-stark` has rich role edges (Joffrey COMMANDS_IN, Ilyn Payne AGENT_IN, Ice WIELDED_IN) but **ZERO upstream causal chain** — "what set Ned's execution in motion / who is to blame" returns nothing causal. Build the upstream arc (richest remaining; ~3–4 new beats):
- Ned discovers Joffrey/Cersei's children are not Robert's → confronts Cersei / tries to act → Robert dies → Ned moves to claim regency → **Littlefinger betrays Ned** (the gold cloaks turn) → Ned arrested → Ned's forced confession → Joffrey orders the execution against counsel.
- Terminus: `execution-of-eddard-stark` (exists). Likely reuse: `gold-cloaks-betray-ned` (event.conspiracy, exists), `arrest-of-eddard-stark` (check), `death-of-robert-baratheon` / boar-hunt beat. **Pre-mint dedup is mandatory** — several of these beats likely already exist.
- **Agency-collapse**: model Littlefinger's betrayal and Joffrey's choice as beats/role edges, not collapsed arrows.

### Step B — re-dip after B3
Re-run the arc-weighted dip; confirm Q10 upgrades to correct. Let any new fumbles re-rank further. Don't mass-mint.

## The proven arc-mint machine (reuse for every arc)
1. **Research subagent** (read-only, local cache): identify reader-load-bearing beats; **dedup-check each** via `python3 scripts/event_alias_resolver.py --lookup "<phrase>"` + grep `graph/nodes/events/`; gather VERBATIM chapter quotes with `file:line`; propose nodes + role/causal edges. **VERIFY the agent's claims against `edges.jsonl` / `--neighbors`, NOT the stale node-file `## Edges` prose** (S107: research agents twice mis-read stale display bullets — wrong canonical hub, "missing" dyad that existed, mis-cited quote, wrong slugs).
2. **Orchestrator trims + mints** via a `scripts/mint_<arc>_arc.py` script (backup `edges.jsonl` to `_regrounding/` + re-run guard). Write beat-node `.md` files directly (prose + `## Quotes` + natural-phrase aliases for discoverability).
3. **Rebuild** targeted indexes (`build-entity-indexes.py --type events --slug <s>`) + `event_alias_resolver.py --build`.
4. **Fresh-subagent verify** each causal edge + agency modeling vs local cache; mint causal edges with `verified_by: pending-*`, stamp `subagent-local-source-check-<date>` on CONFIRM.
5. **Smoke-test** `graph-query.py --causal-chain <terminus>` + natural-phrase discoverability.

## Policy / guardrails (FIRM)
- **Tier:** causal edges capped **Tier-2** (interpretive link); role edges Tier-1. (Tier = confidence 1–5 ONLY.)
- **CAUSES** = mediated; **TRIGGERS** = immediate specific spark; **MOTIVATES** = event/condition → actor; **PRECEDES** = pure chronology (NOT causal).
- **Pre-mint dedup mandatory.** **Agency-collapse check** before any `A CAUSES B`. Don't assert a frame as fact.
- **Hard-stop:** don't chain CAUSES into a multi-attributed terminus (e.g. `→ war-of-the-five-kings` — Q6 staying causal-dark is correct-by-policy; do NOT attach sparks to it).
- **`event.conspiracy` is fine as a CAUSAL beat** (carries conspirators' agency via role edges) — just never as a SUB_BEAT_OF umbrella parent (chain-as-arc, S106).
- **Verification (FIRM, Matt):** interpretive/causal edges verified by fresh subagents vs LOCAL cache; never re-fetch; Matt gates at policy level, not per-edge.

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase, ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`.

## Small fixes surfaced (→ working/todos.md § Small Fixes, not blocking)
- `greyjoys-rebellion` dup of canonical `greyjoy-rebellion` (merge); `robert-baratheon`/`robert-i-baratheon` dup; sack-hub junk `DEFEATS` edge.
