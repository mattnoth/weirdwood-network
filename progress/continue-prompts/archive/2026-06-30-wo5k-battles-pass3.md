# A2.5 WO5K-battles — PASS 3 (the Spicer-betrayal mechanism / Fords→Duskendale → RW-upstream)

> **This will be Session 166** (graph track, global S-number). Stamp your worklog entry `### Session 166` in `worklog.md`.
> **Recommended model:** Opus 4.8 for orchestration + the causal-wiring judgment; Sonnet 4.6 for the per-thread research/verify subagents.
> **One live continue prompt** (graph track). This is the live track. After it, **A2.8 Davos/Sam residual** closes the A-roundup.
> **`/endsession`: this IS an enrichment dip** (PASS 3 of the WO5K-battles arc enrichment) — the enrichment auto-run convention applies, but still confirm per Matt's standing preference.

## Why now
S163 (PASS 1, Robb's Riverlands-relief rise, net +19 edges) and S164 (PASS 2, the Westerlands raid, net +14 edges) built and deepened the WO5K-battles spine. S165 drained the harvest queue those passes refilled (35→0). PASS 3 is the **unravelling half**: the Spicer betrayal mechanism and the army-thinning losses (the Fords / Duskendale) that feed the Red-Wedding-upstream (B1) arc.

## The thread list (PRE-SCOUTED — fold these in)
The S164 Lens-B run logged a clean PASS-3 thread list in `working/enrichment/wo5k-battles-pass2/lens-B.md` § "PASS-3 thread list". The Spicer-betrayal threads (mint from `affc-jaime-05` / `affc-jaime-07`, both in the local chapter cache):
1. `tywin-lannister MANIPULATES sybell-spicer` — Tier-1; affc-jaime-07:79 ("as your lord father bid me"). Tywin set the terms.
2. `rolph-spicer HOLDS_TITLE` Lord of Castamere — Tier-1; affc-jaime-07:81 ("your brother Rolph has been made Lord of Castamere") — the reward for betrayal.
3. `sybell-spicer BETRAYS robb-stark` (consider event node `the-spicer-trap`) — Tier-1; affc-jaime-07:79.
4. `jeyne-westerling VICTIM_IN` the trap (bait + kept barren) — affc-jaime-07:79; consider the event node.
5. `raynald-westerling AGENT_IN [freeing Grey Wind at the Red Wedding]` — affc-jaime-07:157 (freed Grey Wind from the net, threw himself into the river; NOT party to his mother's conspiracy). Belongs to the Red-Wedding enrichment track.
6. `grey-wind FORESHADOWS robb-weds-jeyne-westerling` (or → spicer-betrayal) — craft/foreshadowing layer; cite asos-catelyn-02:189 (this is the **parked harvest row 999** — it un-parks here).
7. `sybell-spicer AGENT_IN [jeyne-made-barren]` + `jeyne-westerling VICTIM_IN` — affc-jaime-07:79.

## The army-thinning half (the Fords / Duskendale — research from the chapter cache)
The losses that gut Robb's host before the RW. Scout the local wiki + Pass-1 cache for: the **Battle of Duskendale** (Robett Glover & Ser Helman Tallhart, ordered by Roose Bolton — a deliberate sacrifice?), the **Battle of the Ruby Ford / the Fords** (Roose Bolton vs. Tywin at the Trident), and how these tie to Roose's pre-Red-Wedding defection. These wire into the B1 RW-upstream spine (already built — see memory `project_narrative_arc_reification`).

## The machine (proven S133/S163/S164 arc-enrichment)
Fan-out lenses (per-topic) + a **4th existing-node↔existing-node causal-wiring lens** (memory `feedback_enrichment_board_causal_lens` — the per-topic lenses miss cross-arc seams) → verify-lines vs the LOCAL book/wiki cache → fresh-verify a sample (independent subagent) → mint. Cheap Sonnet board ≈ max-effort Opus (~90% convergence) — proposer tier is not the bottleneck, orchestration is; **don't default to Opus-as-proposer.**

## DO NOT
re-fetch the wiki · run extractions · un-park D&E · `git add -A` (stage by path) · re-mint the S163/S164 edges (dedup against the existing WO5K spine — `graph/index/` + `working/enrichment/wo5k-battles-pass2/`) · paste the Pass/Track/Tier vocab into any subagent that names a thread or numbers steps (subagents don't load CLAUDE.md).

## Read first
- `working/enrichment/wo5k-battles-pass2/lens-B.md` (the PASS-3 thread list + Spicer mechanism) · `working/arc-enrichment-backlog.md` · `worklog.md` S163/S164 entries · memory `project_arc_enrichment_track`, `feedback_enrichment_board_causal_lens`, `project_narrative_arc_reification`, `feedback_subagent_verify_not_matt`, `feedback_harvest_queue` (PUSH the harvest-pointer rule into research subagents — they refill the queue as they read).
- Capture-during-research is FIRM: any load-bearing verbatim quote found while in the text gets attached (or a harvest-queue pointer dropped) before moving on (memory `feedback_capture_quotes_during_research`).
