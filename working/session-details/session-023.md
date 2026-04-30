# Session 023 — Wiki Pass 2 Stage 1 Drain Complete (2026-04-27)

**Type:** Execution-heavy. Mostly monitoring scheduled wakeups while Matt was away.

## What happened

Resumed Stage 1 wiki Pass 2 after Session 22's 7-day rate-limit hit. Initial state: 9/37 buckets complete, 21 pending, 7 fail (rate-limit orphans with stale tmp/). Question queue: 3 entries, 2 resolved, 1 OPEN.

Verified state pre-launch:
- Bucket statuses matched the continue prompt's expectations
- Node count breakdown was off in the prompt (88 chars + 47 houses + 1 faction = 136 total claimed) — reality was 136 chars + 47 houses + 1 faction = 184 total. Prompt math had mis-attributed the worklog's "136 new node files" total to characters alone. Sane data, just a transcription artifact.
- Question state was 2 resolved + 1 OPEN (Dragonkeepers), prompt claimed 3 resolved. Surfaced both discrepancies to Matt before launching.
- Rate-limit reset window: hit ~31 hours prior; 7-day cap meant we were ~14% into the reset window. The prompt warned against re-launching too early. Surfaced to Matt; he authorized launch anyway.

Wiped tmp/ for the 7 fail buckets per the script in the continue prompt. Verified iTerm2 had ≥1 window. Launched `weirwood wiki core 3 3` — 28 launchable buckets across 3 tabs in 7 waves of 4. Monitoring strategy: scheduled wakeups at 5/20/30/30/15/13/7 minute intervals, sized to bucket-cycle (~6 min) for early rate-limit detection, then to wave-cycle for steady-state monitoring.

Run timeline:
- 09:53 — launch. All 3 tabs immediately past the rate-limit gate. Cap had cleared.
- 10:23 — 17/37 done at 22 min mark (8 buckets in first chunk).
- 10:53 — 23/37 done. Slight slowdown as T3 (only 4 buckets assigned to wave 7) finished and exited.
- 11:34 — `houses-reach-h` hit a fresh rate-limit (took 696s before final reject; cost $4.24 for nothing). Tabs paused.
- 14:10 (Matt back, his session reset too) — relaunched `weirwood wiki core 3 1` for the 9 remaining buckets (3 tabs × 1 wave = exactly 9 buckets distributed). Option A confirmed.
- 15:11 — last 2 buckets (`houses-dorne`, `characters-house-martell-m-t`) finished. 37/37 complete.

Cost surprise (the main finding, surfaced mid-session at the 102-min mark):
- Session 22: ~$25 cumulative + $8 burned on retry attempts
- Session 23: $68.10 across 28 ok buckets + 1 skip-rate-limit ($4.24 wasted)
- **Cumulative Stage 1: $95.33 / 37 ok buckets = $2.58/bucket**
- Original Stage 1 envelope was $40-60 / ~$1 per bucket
- Per-bucket token mix shows cache_read at 70-90% of total tokens (1.5-3M tokens per bucket); suggests the agent prompt + page bundle is heavier than planning estimates
- **Tier-secondary projection at this rate: ~$1,200 across 472 buckets**

When Matt asked about the cost overrun, gave him three options: (A) finish the 9 remaining at ~$23 more (gets clean DoD + real data for secondary), (B) pause and audit before further spend, (C) end Stage 1 at 28/37 and finish later. He picked A. Stage 1 closed cleanly at $95.33.

Validator: 37/37 passed cleanly. Sanity: 858 nodes promoted (591 chars + 264 houses + 3 factions). Conflicts: 52 files in `_conflicts/` (carry-over from the multi-letter character bucket overlap pattern; data integrity preserved by the conflict mechanism, just wasted $$).

## Question triage

Question queue ballooned from 3 → 74 during the run. Most were filed automatically per the Session 22 first_available rule (parser said one book, cite_refs spanned earlier ones, agent set "always available" and filed a question per the rule's instructions).

Categorized:
- **67 bulk-resolved** with 4 canned templates: first_available rule confirmation (~60), type-classification reclass (Dragonkeepers / Brotherhood of Winged Knights / Order of the Green Hand all → `organization.faction`), House Sweet region overlap accepted, generic agent self-correction accepted
- **5 surfaced for Matt** as genuinely needing his domain calls: House Donnerly / Sarwyck / Westford (video-game-only Cyanide RPG entities, non-canon), Arya Stark SPOUSE_OF Ramsay (Jeyne-as-Arya impersonation), Aegon Targaryen Young Griff (parser used baby-Aegon's AGOT cite_refs)
- **0 unhandled** — every question fit one of the patterns

When Matt got back and answered the 5:
- **Video-game-only houses → EXCLUDE.** Three node files deleted: `house-donnerly.node.md`, `house-sarwyck.node.md`, `house-westford.node.md`. Not demoted to a tier or flagged with `disputed:true` — actually deleted. Sets precedent for tier-secondary triage (pre-filter rather than emit-then-delete).
- **Arya/Ramsay edge → REDIRECT.** Removed `SPOUSE_OF: Ramsay Bolton` from arya-stark.node.md (line 74); rewrote the Notes section to explain the impersonation and flag that the edge belongs to a future `jeyne-poole.node.md`. Pattern: in-universe identity-fraud edges attach to the impersonator's node, not the victim's.
- **Young Griff → confirmed canonical** (ADWD: Tyrion meets him aboard *Shy Maid*, claimed by Jon Connington as Aegon Targaryen). Real-vs-Blackfyre-impostor remains canonically unresolved. Parser's first_available value retained — disambiguation precision is a v2 concern.

Final question state: 74/74 resolved, 0 open.

## Three precedent decisions saved to memory

After Matt's calls, captured as project memories so they persist past worklog archival:
1. `project_video_game_entities_excluded.md` — Cyanide RPG / non-canon licensed-derivative pages excluded from graph
2. `project_impersonation_edges_redirect.md` — identity-fraud edges go to the impersonator
3. `project_wiki_pass2_cost_per_bucket.md` — $2.58/bucket actual; tier-secondary needs bundle audit before launch

Also added 3 lines to MEMORY.md index.

## Stage-2 handoff

Wrote `progress/continue-prompts/2026-04-27-wiki-pass2-core-review.md` per the runbook's §"Stage 2 prompt template". Key design decisions in the handoff:
- Explicitly tells fresh Claude to **skip session-detail files** and worklog narrative — those carry the launching Claude's framing, which is bias for a gate decision
- Surfaces the cost-per-bucket finding as a Stage-2 decision input (audit before Stage 3?), not a unilateral remediation call from Session 23
- Notes the 67 bulk-resolved questions as a spot-check target ("verify the canned resolution didn't paper over real issues")
- Lays out the proceed/remediate/escalate decision matrix from the runbook

Stage-2 session expectations: read-only sampling, no agent runs, ~$2-5 of Claude Code cycles. Output is one of three downstream prompts (Stage 3 launch, remediation, or escalate-to-Matt).

## Notable observations

- **Orphan fail buckets self-recovered without manual relaunch.** Session 22 left 7 buckets in `fail` status from rate-limit skips. After wiping tmp/, the launcher's `cmd_run` correctly re-attempted them across this session — iron-islands-h, lannister-j-q, targaryen-t-y, reach-h all recovered. The `version-stale` and `fail` retry paths are working.
- **Wave-math distribution was uneven.** With 28 buckets / WAVE_SIZE=4 = 7 waves and 3 tabs, T3 got only wave 7 (4 buckets) and finished in ~25 min. T1 and T2 each had 12 buckets and ground through them serially. Net effect: parallelism dropped from 3 to 2 to 1 over the run. Not a bug, just a consequence of the wave-distribution algorithm. Future runs with uneven bucket counts could benefit from rebalancing or a different distribution heuristic.
- **The 7-day rate-limit cap is real but recoverable mid-window.** Hit cap once mid-run on `houses-reach-h`. Burned $4.24. Restarted ~3 hours later (after Matt's session reset) and the second attempt succeeded for $2.07. So the cap is more like "rolling exhaustion" than a hard 7-day lockout — recoverable within a session if you wait out the soft window.

## What's next

- **Stage-2 cold review** per the new continue prompt. Fresh Claude session, no Session-22/23 context.
- After Stage 2 clears: bundle audit (recommended) → tier-secondary launch (Stage 3, multi-day, ~472 buckets, ~$1,200 at current rate).
- Carryover open todos (none added this session — todos from prior sessions still apply).
