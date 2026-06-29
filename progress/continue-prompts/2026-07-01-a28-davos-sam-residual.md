# SESSION 167 — A2.8 Davos / Sam residual (CLOSES the 🅰 A-roundup)

> **This is Session 167.** Stamp your worklog entry `### Session 167` in `worklog.md`.
> **Recommended model:** Opus 4.8 for orchestration + the causal-wiring judgment; Sonnet 4.6 for the per-thread research/verify subagents.
> **One live continue prompt** (graph track). This is the live track. **It CLOSES the A-roundup** — after it, the descent drops to granular L2 / character / (gated) work; run a dedicated PLANNING session next (Matt S130) to scope the granular dip list.
> **`/endsession`: this IS an enrichment dip** (the auto-run convention applies, but still confirm per Matt's standing preference).

## Why now
The 🅰 A-roundup is six units deep (A2.7 Stannis S155 · A1.5 Dorne S156 · A1.6 Euron S157 · A2.6 Jaime/Riverlands S159 · A2.4 Tyrion/Essos S161 · **A2.5 WO5K-battles PASS 1–3 S163/S164/S166**). **A2.8 Davos/Sam is the LAST residual** — both arcs are Stannis/Jon-adjacent and substantially pre-wired (Blackwater S138 for Davos; Jon/Wall S145 + Battle of Castle Black S153 for Sam), so expect **HEAVY dedup, WIRE+ENRICH, few new nodes**. Coverage card: `working/enrichment-coverage-plan.md` line 88 ("Davos: Blackwater near-death → Manderly mission → Skagos. Sam: Fist → Gilly → Citadel road. Smaller, Stannis/Jon-adjacent; do as residuals.").

## The two halves (scope — run your own `baseline_pull.py` first to dedup)
**HALF A — Davos:**
- Blackwater near-death → washed up on the spur of rock → rescued by Salladhor Saan (the `davos RESCUES`/`RESCUED_BY` cluster — check what S138 already built). Source: ACOK Davos III + ASOS Davos I.
- The **Manderly mission** (ADWD): Davos sent to White Harbor → imprisoned → **Wyman Manderly's STAGED execution of "Davos"** (S93 built 4 Wyman/Davos `event.deception` beats + `wylis-manderly`/`wyman-manderly` — DEDUP HARD, do NOT rebuild) → the Rickon/Skagos commission. Source: ADWD Davos I–IV.
- **Skagos** — Davos dispatched to fetch Rickon Stark from Skagos (the unresolved quest). Source: ADWD Davos IV.
**HALF B — Sam:**
- The **Fist of the First Men** — the Others' attack / the Great Ranging's retreat (likely wired by the Jon/Wall S145 + the ASOS Sam chapters; DEDUP vs `fight-at-the-fist`). Source: ASOS Samwell I.
- **Gilly + Craster's Keep** — the mutiny at Craster's, Sam & Gilly's flight, the baby, Coldhands. Source: ASOS Samwell II–III (`bran-meets-coldhands` S130 is adjacent — DEDUP).
- **The Citadel road** — Sam/Gilly/Aemon to Oldtown via Braavos; **Aemon's death**; Sam reaches the Citadel. Source: AFFC Samwell I–V.

## The machine (proven S133/S163/S164/S166 arc-enrichment)
`baseline_pull.py` (pull the Davos + Sam webs, flag islanded hubs + dup minefields) → fan out 2–4 fresh **Sonnet** lenses (per-half roster/whodunit/descriptive + a **4th existing-node↔existing-node causal-wiring lens** — memory `feedback_enrichment_board_causal_lens`) → synthesize + dedup → `mint_enrichment.py --candidates …` → node-edits (container tags / book-cite overlays) → `weirwood-refresh` (if nodes added) → **independent Sonnet fresh-verify** of interpretive/causal/SUSPECTED_OF edges vs the LOCAL cache → `finalize_enrichment.py --verdicts …` → smoke. Cheap Sonnet board ≈ max-effort Opus (~90%) — **don't default to Opus-as-proposer.** Paste the harvest snippet + the capture-quotes rule into every text-reading subagent.

## DO NOT
re-fetch the wiki · run extractions · un-park D&E · `git add -A` (stage by path) · rebuild the S93 Wyman/Davos deception spine or the S138 Blackwater Davos cluster (dedup against them) · default to Opus-as-proposer · paste the Pass/Track/Tier vocab into any subagent that names a thread or numbers steps (they don't load CLAUDE.md).

## Read first
- `working/enrichment-coverage-plan.md` (the A2.8 card + Class A context) · `working/arc-enrichment-backlog.md` (the scope model + the machine) · `worklog.md` STATUS + the S166 entry · memory `project_arc_enrichment_track`, `feedback_enrichment_board_causal_lens`, `project_narrative_arc_reification`, `feedback_subagent_verify_not_matt`, `feedback_harvest_queue`, `feedback_capture_quotes_during_research`.
- **Container tags:** Davos/Sam beats are mostly `[north]` / `[aegon]`-adjacent or untagged — only tag with one of the 5 approved containers (essos/wo5k/north/aegon/bran) when the beat genuinely belongs; do NOT mint a new container.
- After A2.8: **the A-roundup is CLOSED** → next session is the **granular-dip PLANNING session** (scope the L2 / character / event-within-container list — Matt S130), NOT another arc dip.
