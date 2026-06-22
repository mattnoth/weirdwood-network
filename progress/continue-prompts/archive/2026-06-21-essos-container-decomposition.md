> **⚠️ SUPERSEDED 2026-06-21 (S121).** Replaced by `progress/continue-prompts/2026-06-21-container-shape-analysis.md`,
> which reframes the next session as a dedicated CONTAINER-SHAPE analysis (Matt: shape > names; the SET is a
> graph-shape decision deserving its own subagent session). Kept for history; do not run this version.

# Continue — container-split fan-out (re-run) → build (next-session plan, set S121)

> **Recommended model:** Sonnet 4.6 (orchestration + research/verify + container-lens subagents). Opus only for a hard adjudication.

> **State trust (CLAUDE.md rule #9):** `worklog.md` is authoritative. As of **S121**: nodes **8,574** ·
> edges **22,384** · edge types **132** · vocab **169**. **Step 1 (hardening) is COMPLETE.** Step 2
> (container-split fan-out) was **blocked by a persistent Anthropic 529 overload** — a stand-in proposal
> exists but the independent fan-out still needs to run. Step 3 (build) is deferred behind it.

## WHY THIS STATE (read first)
S121 executed the 3-step plan from the S120 board, but a **severe Anthropic API 529 overload killed every
subagent dispatch** (6 agents, 2 rounds, the 2nd round 0 tool uses). The orchestrator therefore did all of
Step 1 in-house (it's deterministic + single-book research, defensible solo) and authored a **stand-in
container-split proposal** for Step 2 instead of the intended independent 4-lens fan-out. **Read these:**
- `working/session-results/2026-06-21-container-split-PROPOSAL.md` — the orchestrator's Step-2 synthesis
  (30-event→container backbone + recommendations). **This is a hypothesis to pressure-test, not a decision.**
- `working/session-results/2026-06-21-container-split-BRIEFING.md` — the ready-to-run 4-lens fan-out brief.
- `graph-concepts-explainer.md` (gitignored) — the concept model.

## STEP A — run the container-split fan-out (Matt's explicit request; do FIRST)
The API was down in S121. **Re-dispatch the 4 lenses** (each: `Read working/session-results/2026-06-21-container-split-BRIEFING.md, then execute LENS <X>`). They are read-only Sonnet `general-purpose` subagents; the briefing names each lens + its output file + asks them to pressure-test the PROPOSAL, not echo it. Lenses: A (set+scope: confirm/revise the 6-container set incl. the proposal's NEW `riverlands`+`kl-faith`; scope NORTH + AEGON), B (Jon/Bran granularity), C (seams + build-once rule), D (retro-grouping the ~12 standalones).
- If the API is still overloaded: the proposal stands as the working decision; flag it to Matt and proceed cautiously, OR wait.
- **Synthesize** the 4 lens reports + the proposal into a final container map. **Surface the open questions to Matt** (the proposal's §"Open questions for Matt": the container SET, Jon/Bran scheme, build priority, retro-tag-now-or-defer). "Agents propose, Matt decides."

## STEP B — fold Matt's decisions + (if approved) retro-tag
Once Matt picks the container SET: use `scripts/stamp_containers.py <name> <slug>…` (idempotent, dry-run first) to stamp the agreed tags. The proposal's §"Lens D" has the recommended tag-now subset. Do NOT tag before the SET is settled (names may change). NORTH/AEGON nodes are mostly greenfield (unbuilt).

## STEP C — build (with settled boundaries)
Default = **WO5K remainder** (`working/wo5k-decomposition.md`): #3 Blackwater-upstream (J2+J9) · #4 Karstark (J7) · #5 Balon→Winterfell (J4, dual-tag `[wo5k, north]` per the seam rule); SKIP J6. **The proposal confirms WO5K-remainder is seam-safe to build now.** OR build whichever container Step A prioritizes (NORTH is the biggest greenfield gap). Use the arc-mint machine — **causal edges MUST be fresh-subagent verified** (Matt's FIRM rule; L2 for cross-book/contested CAUSES). Stamp `containers:` as you build.

## The arc-mint machine (reuse for every juncture)
1. Research+verify subagent (read-only, LOCAL cache; dedup via `event_alias_resolver.py --lookup` + `mint_arc_lib.precheck_slugs`; verbatim `file:line` quotes; adjudicate edge types; verify vs `edges.jsonl`/`--neighbors`; PASTE vocab + harvest snippet in). 2. Orchestrator writes node `.md` (prose + `## Quotes` + SPACED aliases + `containers:`) + mints via a `scripts/mint_*_arc.py` script (backup + re-run guard; `precheck_slugs`; re-pin every evidence_ref vs the chapter file). 3. Rebuild indexes + `event_alias_resolver.py --build`. 4. `verify-edge-quotes.py --run-id <id>`. 5. `--causal-chain`/`--full-chain` smoke + root-check. 6. Harvest sweep.

## CARRIED (small, unblocked when API is up) — from `working/dyad-queue.md`
WITNESS_IN role edges (verify the line, append): Jorah WITNESS_IN `drogo-blood-magic-ritual` (agot-daenerys-08:225) · Strong-Belwas/Barristan/Reznak WITNESS_IN `drogon-returns-to-daznak-pit` (adwd-daenerys-09:233) · Mossador SIBLING_OF Missandei (adwd-daenerys-02:35). Also D1 (Varys/Illyrio → AEGON) + D2 (Jorah channel) dyads when AEGON is opened.

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`. Containers are TAGS, not graph objects.

## DO NOT
Re-fetch the wiki · invent edge types (verify vocab first) · use kebab aliases (SPACED phrases) · assert unproven agency as fact (`SUSPECTED_OF`, Tier-2) · mass-mint a container in one pass · retro-tag containers before Matt picks the SET · run `/endsession` without explicit permission.
