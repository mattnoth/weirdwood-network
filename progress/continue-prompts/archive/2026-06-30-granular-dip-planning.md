# SESSION 168 — Granular-dip PLANNING session (the 🅰 A-roundup is CLOSED)

> **This is Session 168.** Stamp your worklog entry `### Session 168` in `worklog.md` (graph track, global S-number).
> **Recommended model:** Opus 4.8 (planning/judgment session — scoping, not execution; a few Sonnet 4.6 census/scoping lenses if you fan out, per `feedback_enrichment_board_causal_lens`).
> **One live continue prompt** (graph track). This IS the live track. **This is a PLANNING session, NOT an enrichment dip** — its whole job is to *enumerate and scope the granular dip list*. Mint nothing (a graph-grounding census is fine; no edges/nodes).
> **`/endsession`: this is a PLANNING session (not a dip)** — the dip auto-run convention does NOT apply; confirm with Matt before `/endsession`.

## Why now
The 🅰 A-roundup is **CLOSED** (S167 — A2.8 Davos/Sam was the last unit; 27 major-arc dips total). Per Matt's S130 plan, **a dedicated PLANNING session sits between the arc phase and the granular phase** — its job is to scope the descent to the granular tier now that we know far more about what each cluster needs. The arc enrichments built most of the major character webs as a by-product, so the granular list is the residual: L2 sub-plots inside the enriched arcs, the cross-cutting manipulator character webs, the event-within-container deep dives, and the remaining Class-D event clusters.

## STEP 0 (mandatory) — drain the harvest queue FIRST
`grep -c '^| open ' working/harvest-queue.md` — it stands at **39 open (≥30 — over the drain threshold)** at S167 close. **DRAIN it before the planning work** (the S152/S162/S165 disjoint-dir parallel-attacher machine: route rows to disjoint node-dir groups → fan out Sonnet attachers → orchestrator flips `open`→`done` centrally → 1 independent Sonnet fresh-verify on a stratified sample). The 18 S167 rows are high-value (food nodes, appearance/place overlays, Iron-Throne/Mormont/Marwyn quotes, glass-candle object); the 21 pre-S167 rows carry from S166. This is maintenance, not a dip — it clears the deck before planning.

## The planning deliverable
Produce a **ranked, scoped granular-dip list** — the granular-phase analogue of `working/enrichment-coverage-plan.md` (which was the arc-phase planning deliverable). Update that file (or a new `granular-dip-plan.md`) with:
- **Class B — L2 sub-plots inside the enriched arcs** (remaining unrun: B5 Antler Men · B6 Ice→Widow's-Wail+Oathkeeper [check REFORGED_INTO instantiation] · B8 Lancel AGENT_IN Robert's death · + the Blackwater ship-roster Python batch [deterministic, NOT a dip]). See `enrichment-coverage-plan.md` Class B.
- **Class C — character-web residuals** (the cross-cutting manipulators whose webs no single arc covers: C1 Varys [thin, 59 edges] · C2 Petyr · C3 Bloodraven/Brynden Rivers [stub, 19 edges; the Matt-flagged dip + D&E book-cite overlay] · C4 Euron). Everyone else's web fell out of their arc.
- **Class D — big event clusters not owned by one POV** (remaining: D2 Hand's Tourney · D3 Greyjoy's Rebellion · D4 Riot of KL · D6 Rebellion prelude [theory-adjacent]).
- **Graph-ground each candidate before ranking** (don't trust stale density notes): baseline its current edge density + islanded-hub count (the `baseline_pull.py` pattern, or `graph-query.py --neighbors`). Rank by reader-salience × current-thinness × cross-arc payoff × readiness.

## The machine (planning, not minting)
Optionally fan out 2–4 **Sonnet** scoping lenses (Class-B census / Class-C character-web census / Class-D cluster census / a graph-grounding density pass) → Opus synthesis into the ranked list. Paste the harvest snippet (`working/harvest-queue.md` § "Paste-into-every-dip/research-subagent-prompt snippet") into any text-reading lens. **Do NOT paste the Pass/Track/Tier work-vocab into subagents** that name threads or number steps (they don't load CLAUDE.md) — but DO give them the edge-type taxonomy if they propose edges.

## DO NOT
re-fetch the wiki · run extractions · un-park D&E · `git add -A` (stage by path) · mint enrichment edges/nodes this session (it's planning — a read-only census is the point) · default to Opus-as-proposer for any lenses · re-open the A-roundup (it's closed).

## Read first
- `working/enrichment-coverage-plan.md` (Class B/C/D tables + the "enrich the arc, the character web comes free" organizing principle) · `working/arc-enrichment-backlog.md` (the scope model + the descent: L1 arcs → L2 sub-plots → L3 characters; the S167 A-roundup-closed update) · `worklog.md` STATUS + the S167 entry · memory `project_arc_enrichment_track`, `project_bloodraven_enrichment_dip` (C3 is Matt-flagged but ONE of many — no lead), `project_theories_track_deferred` (theory readings stay GATED — Class-D D6 + any prophecy content = evidence substrate only), `feedback_enrichment_board_causal_lens`.
- **Sequencing reminder (Matt S130/S131):** within the granular tier everything matters — no single "#1"; pick by readiness/demand. The character phase (Class C) is tentative and LAST because most character webs are already built as arc by-products. **D&E full-Opus Pass-1 batch** is scheduled to slot in after the first enrichment passes (it's currently PARKED — Matt revisits when fresh; don't un-park unprompted).
