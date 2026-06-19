# Continue — Causal-arc execution: re-dip, then Tier B

> **Recommended model:** Sonnet 4.6 (the dip is graph-only Q&A + scoring; arc minting is subagent-driven). Opus only if a hard interpretive judgment needs it.
> **Status:** chain-as-arc ratified (S106). `--causal-chain` primitive + 2 Tier-A arcs SHIPPED. Next action is a re-dip — NOT more minting yet.

## Where this stands (after S106, 2026-06-19)

The causal/narrative-arc **technique is proven 4× and productionized**: Robert's Rebellion (S104), Bran's fall (S105), **Sack of King's Landing + Purple Wedding (S106)**. The scaling strategy + rubric is `working/causal-arc-strategy-2026-06-18.md` (read it first). Term reference: `reference/narrative-arc-glossary.md`.

**DONE in S106:**
- **Step 1 — `--causal-chain <slug>` primitive** in `scripts/graph-query.py` (walks CAUSES/TRIGGERS/MOTIVATES both directions; +10 tests). The whole-arc query that made "no umbrella parent" real.
- **Chain-as-arc ratified by Matt** — arcs live as causal chains queried via `--causal-chain`; NO `event.arc` umbrella nodes. (Supersedes the umbrella-vs-chain fork in `archive/2026-06-15-arc-wave1-mint.md`.)
- **Sack of KL** (4 beats, 21 edges) + **Purple Wedding** (4 beats, 20 edges) — both fresh-subagent verified ALL-CONFIRM. Mint scripts: `scripts/mint_{sack_kl,purple_wedding}_arc.py`.

## The work, in order

### Step A (NEXT) — arc-weighted Mode-3 dip, BEFORE any Tier-B minting
The strategy's cadence is **dip-driven, not mass-mint**. Run a Mode-3 grounded-agent dip (a graph-only agent answers reader-style questions; the ones it fumbles for lack of structure are the evidence) **weighted toward arc/consequence shapes** ("what set X in motion", "what were the consequences of Y", "who is to blame for Z"). Prior dips: `working/session-results/2026-06-15-mode3-dip-rerun.md` + the S96 dip. Let the failures **re-rank Tier B** — don't pre-commit.

### Step B — Tier-B arcs, ordered by what the dip surfaces
Candidates (strategy §3 Tier B): **Catelyn-frees-Jaime → Robb's-host-turns → Jeyne-Westerling → (feeds) Red Wedding**; **Greyjoy Rebellion → Theon-as-hostage → ironborn invasion of the North**. Reuse the proven machine (below). Mint only what the dip shows agents fumble.

## The proven arc-mint machine (reuse for every arc)
1. **Research subagent** (read-only, local cache): identify reader-load-bearing beats; **dedup-check each** via `python3 scripts/event_alias_resolver.py --lookup "<phrase>"` + grep `graph/nodes/events/`; gather VERBATIM chapter quotes with `file:line`; propose nodes + role/SUB_BEAT_OF/causal edges.
2. **Orchestrator trims + mints** via a `scripts/mint_<arc>_arc.py` script (backup `edges.jsonl` to `_regrounding/` + re-run guard). Write beat-node `.md` files directly (prose + `## Quotes`).
3. **Rebuild** targeted indexes (`build-entity-indexes.py --type events --slug <s>`) + `event_alias_resolver.py --build`.
4. **Fresh-subagent verify** each causal edge + agency modeling vs local cache; mint causal edges with `verified_by: pending-*` then stamp on CONFIRM.
5. **Smoke-test** `graph-query.py --causal-chain <beat>` + natural-phrase discoverability.

## Policy / guardrails (FIRM)
- **Tier:** causal edges capped **Tier-2** (interpretive link); role edges Tier-1. (Tier = confidence 1–5 ONLY.)
- **CAUSES** = mediated; **TRIGGERS** = immediate specific spark; **MOTIVATES** = event/condition → actor; **PRECEDES** = pure chronology (NOT causal).
- **Pre-mint dedup is mandatory** (S105 minted a dup without it; S106 it caught `fall-of-kings-landing` + 2 already-modeled layers).
- **Agency-collapse check:** before `A CAUSES B`, model the human decision between them (beat node OR MOTIVATES→actor + COMMANDS_IN/AGENT_IN). Don't assert a frame as fact (PW: Tyrion VICTIM_IN only, never POISONS).
- **Hard-stop:** don't chain CAUSES into a multi-attributed terminus (e.g. `→ war-of-the-five-kings`).
- **Verification (FIRM, Matt):** interpretive/causal edges verified by fresh subagents vs LOCAL cache; never re-fetch; Matt gates at policy level, not per-edge.

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase, ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`.
