# Continue Prompt — Wiki Pass 2 Stage 2: Cold Review of Core Output

**Created:** 2026-04-27 end-of-Session-23 (Stage 1 complete)
**Goal:** Single fresh-Claude session, no Stage-1 carry-over context. Read the runbook, sample the output, decide `proceed` / `remediate` / `escalate`, and emit a Stage-3 (or remediation/escalation) handoff prompt.
**Cost envelope:** Stage 2 is human + read-only sampling, no agent runs. ~$2-5 of Claude Code cycles. No new node emissions.

## Where this fits

Stage 2 of 3. Full chain: `working/runbooks/wiki-pass2-tier-handoff.md`.

```
Stage 1 (complete) ─► Stage 2 (you) ─► Stage 3 (secondary, ~472 buckets)
```

## Read first (in this order, no detours)

1. **`working/runbooks/wiki-pass2-tier-handoff.md`** — full chain spec + your checklist (§"Stage 2 — review checklist"). Top-to-bottom. The ordering matters.
2. `reference/architecture.md` — entity types, edge types, confidence tiers, file naming, `first_available` semantics. You will judge nodes against this spec.
3. **Skip the Session-22/23 detail files and worklog narrative.** They carry the launching Claude's framing — bias risk for a gate decision. Read the data, not the story.

## State at session start (verify before sampling)

```sh
# Bucket state — expect 37 complete, 0 anywhere else
python3 -c "
import json, glob, collections
status = collections.Counter()
for f in sorted(glob.glob('working/wiki-pass2/*/manifest.json')):
    d=json.load(open(f))
    if d['tier']=='core': status[d['status']] += 1
print(dict(status))"

# Node counts — expect 591 characters, 261 houses, 3 factions = 855 total; 52 conflicts
# (3 video-game-only houses deleted at end of Session 23: house-donnerly, house-sarwyck, house-westford)
find graph/nodes/ -mindepth 2 -name '*.node.md' -not -path '*_conflicts*' | awk -F/ '{print $3}' | sort | uniq -c
ls graph/nodes/_conflicts/ | wc -l

# Question queue — expect 0 OPEN (all 74 resolved at end of Session 23)
weirwood wiki questions

# Stats CSV — full run history (37 ok rows + ~16 skip-rate-limit rows from prior rate-limit windows)
wc -l working/extraction-stats/wiki-pass2-stats-core-v1.csv
```

If any expectation differs significantly, stop and figure out why before sampling.

## Carry-over context the launching Claude flagged (you decide what to do)

These are deliberately surfaced rather than buried — but **you decide whether each is systemic or noise.** Don't take them as given.

- **Cost-per-bucket: $2.58 actual vs ~$1 originally projected.** Stage 1 spent $95.33 across 37 ok buckets + 16 rate-limit retries. Per-bucket total tokens are 1.5-3M with cache_read dominant (~70-90% of token volume). At this rate, secondary's 472 buckets project to ~$1,200. The original Stage-1 envelope was $40-60. **Decide:** is the bundle audit a remediation prereq, or do you proceed and let Matt absorb the cost? Stage-2 finding §3 "cost per node" gives you the data point.
- **All 74 questions resolved** as of end-of-Session-23. Final 5 answered by Matt: video-game-only houses (Donnerly/Sarwyck/Westford) **excluded** (3 nodes deleted); Arya/Ramsay SPOUSE_OF edge **redirected** to a future jeyne-poole.node.md (removed from arya-stark.node.md); Aegon Young Griff disambiguation kept as-is (acceptable v1 ambiguity). See worklog Session 23 §"Precedent decisions" for the rules these set for tier-secondary.
- **67 questions resolved in bulk** by the launching Claude with canned resolutions ("Session 22 first_available rule", "agent reclassification accepted", etc.). **Decide whether this was warranted.** Spot-check 5-10 of the resolved questions against the actual node files. If the canned resolution papers over real issues, that's a remediation flag.
- **52 conflict files** in `graph/nodes/_conflicts/`. Most are duplicates from overlapping multi-letter character buckets (`stark-h-p ∩ stark-h-q = 26/27 pages` confirmed). The conflicts mechanism preserved data integrity, but the wasted cost is real. **Decide:** does the triage-script overlap fix block Stage 3, or does it ride the secondary triage layer's wider net?
- **Validator passed 37/37**, but the validator does NOT check slug-set equality with `expected_nodes` (silent renames possible). Sample explicitly for this in §2 of the checklist.

## Sampling guidance

§2 of the runbook says 15-20 nodes, stratified. Concrete suggestions for **this** dataset (you pick the actual sample — don't be steered):

- High-traffic / high-stakes characters: Tyrion, Jaime, Cersei, Sansa, Arya, Daenerys, Varys (all in core). Sample disambiguated Aegons.
- Ambiguous bucket overlap territory: pick one each from `stark-h-p`, `stark-h-q` and check that the conflict mechanism didn't drop content.
- A "houses" bucket node and a "characters" bucket node from the same letter range to check edge consistency.
- Direwolves (the smoke-test bucket) — the canary.
- One node from each of the 5 question-flagged pages above to see how they were emitted.

## Cost-data-point if you decide `proceed`

Include in the Stage-3 prompt:
- Total Stage-1 cost: $95.33 across 37 buckets ($2.58/bucket avg)
- Token mix: cache_read dominant (~1.5M tok/bucket), output ~25K, cache_creation ~150K
- Secondary projection at this rate: ~$1,200 across 472 buckets (multi-day, multi-rate-limit-window)
- Recommend pre-launch bundle audit if you didn't already remediate it

## Decision deliverables

One of three handoff prompts at `progress/continue-prompts/2026-04-2X-wiki-pass2-<...>.md`:

- **proceed** → Stage-3 launch prompt per template §"If decision = proceed" in handoff runbook
- **remediate** → fix-it prompt per template §"If decision = remediate". Examples: bundle audit before secondary, prompt drift fix, validator slug-equality check.
- **escalate** → discuss-with-matt prompt per template §"If decision = escalate". Use this if the cost-projection question or the open-question batch needs Matt's call before any further automation.

## Out of scope (this session only)

- Do not run any wiki-ingester agents.
- Do not modify the agent prompt, validator, or triage script unless you decide `remediate` AND the edit is a one-liner with obvious correctness — otherwise queue it in the remediation prompt.
- Do not merge, archive, or delete any of the 858 emitted node files.
- All questions are resolved; do not reopen any without strong cause.

## DoD for this session

- §1-3 of runbook completed (read data, sample, score patterns) with the score numbers written down somewhere
- One decision made: `proceed` / `remediate` / `escalate`
- Handoff prompt written at `progress/continue-prompts/2026-04-2X-...`
- This prompt archived to `progress/continue-prompts/archive/`
- Worklog Session 24 entry written (concise — what was sampled, what was found, decision + reasoning)
- /endsession (Matt-authorized at start of next session, not by default — confirm before running)
