# SESSION 223 — D&E event-wiring slice: reify the novella events + drain the 75 causal-spine seeds

> **This is Session 223** — unless the theories wave-2 mint-gate fired first; **CHECK (rule 9):**
> grep `^### Session` in `worklog.md` and take the next free number (this prompt and the mint-gate
> prompt are BOTH stamped 223; whichever fires second becomes 224 — note it in your entry).
> **Recommended model: Fable or Opus 4.8 orchestrator, Sonnet proposers + Haiku fresh-verifiers**
> (the S204 causal-spine pattern). **GRAPH-MUTATING — never run alongside another graph-mutating window.**

## Context (post-S222)

D&E is integrated and deployed: 241 relationship edges + 56 aliases (`233a8ea058`) + 259 book-cited
quotes (`b8cc918cab`) live on prod (`6a5d4ba1` — "Gallows Knight" resolves exact → duncan-the-tall).
**The visible remaining gap:** D&E EVENT nodes have no roles or causal wiring —
`neighbors(wedding-tourney-at-whitewalls)` returns 0 on prod. Relationship edges landed; event
reification did not (deliberately deferred as this slice).

## Substrate (all staged, read first)

1. **`working/dunk-egg-graph-ingest/harvest/causal-spine-seeds.jsonl`** — 75 causal-spine rows
   (`BOOK / quote-or-pointer / causal-spine / note`), e.g. "Aerion demands a trial of seven → Dunk must
   field seven champions → Baelor joins → Baelor dies in the melee." These are the chains to wire.
2. **The 24 extractions' `## Events & Actions` sections** (`extractions/mechanical/{thk,tss,tmk}/`) —
   numbered beats with Agent/Patient/Instrument/Location/Outcome — the role-edge substrate
   (reification roles per `reference/architecture.md`: AGENT_IN / VICTIM_IN / WITNESS_IN /
   COMMANDS_IN / PARTICIPATES_IN …).
3. **Existing event nodes** (wiki layer): `ashford-tourney` AND `tourney-at-ashford-meadow` AND
   `battle-of-ashford` (⚠️ possible dup/disambiguation trap — settle which is THE THK tourney node
   before wiring), `wedding-tourney-at-whitewalls`, `second-blackfyre-rebellion`,
   `first-blackfyre-rebellion`, `battle-of-the-redgrass-field`, `great-spring-sickness`,
   `trial-of-seven` (concept), `maegors-trial-of-seven` (the OTHER trial — don't collide).

## The work

1. Inventory: which marquee D&E events have nodes / which need mints. Expected mint candidates
   (dip-scale, NOT mass-mint — chain-as-arc conventions, S105/106): the Ashford trial of seven,
   death-of-baelor-breakspear, the Whitewalls dragon-egg theft / tourney collapse, TSS's
   Chequy-Water duel + Coldmoat resolution. Check each against existing nodes first.
2. Role edges from the Events tables onto the settled event nodes (deterministic prep where possible;
   Sonnet proposers for judgment; every edge quote-grounded to `sources/chapters/{thk,tss,tmk}`).
3. Causal seams from the 75 seeds (TRIGGERS/ENABLES/CAUSES/MOTIVATES per the locked causal set),
   incl. cross-era: whitewalls/second-blackfyre-rebellion ↔ the F&B/Blackfyre layer (dark-sister →
   Bloodraven seams already exist from S206 — extend, don't duplicate).
4. Gates (non-negotiable, the S222 lesson — weak-rung resolution had a ~25% wrong-node rate):
   dry-run → fresh pressure-test subagent w/ BLOCK authority → exhaustive re-pass of any risky bucket →
   apply → `bash scripts/weirwood-refresh.sh` → pytest + deno → commit. Mint via
   `scripts/mint_enrichment.py --candidates …` / finalize via `scripts/finalize_enrichment.py` if the
   generic tools fit; else extend `scripts/dunk-egg-graph-ingest.py` patterns.
5. Optional riders if budget allows: the 35 overlay candidates
   (`working/dunk-egg-graph-ingest/out/final-overlay.jsonl` + `out/overlay-candidates.jsonl` —
   book-evidence overlays onto existing wiki edges); the 3 food-mint candidates from
   `harvest/*-parked.jsonl`.
6. Deploy at the end (per `DEPLOY.md`: `npx netlify deploy --prod --build`) and live-verify with
   *"What happened at the Whitewalls tourney?"* — `neighbors` should return roles now.

## Success criteria

- `weirwood query --neighbors wedding-tourney-at-whitewalls` (and the settled Ashford node) return
  role + causal edges; `--full-chain` walks the trial-of-seven → Baelor's-death chain.
- All 75 seeds dispositioned (wired / already-present / parked-with-reason) — stamp the seeds file.
- 0 vocab drift · fresh-verify on every minted edge batch · all suites green.

## DO NOT

- Mass-mint every Events-table beat (dip discipline: marquee events only).
- Touch the theories staging (`working/theories/jonsnow-cluster/` — separate Matt-gated track).
- Re-run `scripts/dunk-egg-graph-ingest.py --apply` (sentinel-guarded, already landed).
- `/endsession` unasked.
