# Wiki Pass 2 — Tier Handoff Chain (Core → Review → Secondary)

> **STATUS — SUPERSEDED FOR STAGE 3 (2026-04-27).** Stage 1 (core) and Stage 2 (review) ran as documented here and are complete. **Stage 3 (secondary) was redesigned** mid-Stage-2. The new pipeline splits secondary into Stage 3a (deterministic Python emission for all Tier A+B pages) and Stage 3b (agent prose-only fill, Tier A only). See `wiki-pass2-pipeline.md` (canonical) and `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md` for the actual Stage 3 plan. The Stage 1/2 narrative below remains accurate; ignore this doc's Stage 3 description.

**Purpose:** Encode the chain-of-analysis pattern between tier-core and tier-secondary launches. Pass 2 is structurally one ingestion job, but tier-secondary's scale (472 buckets, ~10× core cost) demands an explicit gate. The gate is a **fresh-Claude review session** — context-isolated from the launching session — that evaluates the core output and decides whether to proceed.

**Audience:** Whichever Claude session ends up at any of the three stages. Read this in full at start of any tier-handoff session.

**Status:** v1 (2026-04-26). Stage 1+2 complete; Stage 3 superseded by `wiki-pass2-pipeline.md`.

---

## The chain

```
Stage 1 ─────────────► Stage 2 ─────────────► Stage 3
(launch core)        (fresh review)        (launch secondary)

  Sessions: 1-N        Sessions: 1           Sessions: 1-N
  Output: 37 nodes     Output: gate          Output: ~2,000 nodes
          buckets      decision +            (estimate)
          complete     handoff prompt
```

### Stage 1 — Run core

- Continue prompt: `progress/continue-prompts/2026-04-26-wiki-pass2-scale-core.md`
- May span multiple sessions (rate-limit windows, triage-rule fixes, validator re-runs)
- Same Claude line of context across sessions is fine — Stage 1 is execution, not evaluation
- Stage 1 ends when its DoD is met (see scale-core prompt)

### Stage 2 — Fresh-Claude review

- Continue prompt: written by the final Stage-1 session, ad-hoc filename
- **Single session, fresh Claude** — no Stage-1 carry-over, no session-detail files from Stage 1, no "last Claude said" hints
- Reads the runbook + the data, forms its own read
- Output: **decision + handoff prompt**
- Decision is one of: `proceed`, `remediate`, or `escalate`

### Stage 3 — Run secondary

- Continue prompt: written by Stage 2 only if it decides `proceed`
- May span many sessions (472 buckets, 8-15× more wall time than core)
- Same multi-pass expectations as Stage 1

---

## Stage 2 — review checklist

A fresh Claude session runs this checklist top-to-bottom. The order matters: surface raw data first, then sample, then synthesize.

### 1. Read the data, not the narrative

Open these files cold. **Skip session-detail files** for the Stage-1 sessions — those carry the launching Claude's framing.

```sh
# Bucket state — should all be complete
python3 -c "
import json, glob, collections
status = collections.Counter()
for f in sorted(glob.glob('working/wiki/pass2-buckets/*/manifest.json')):
    d=json.load(open(f))
    if d['tier']=='core': status[d['status']] += 1
print(dict(status))"

# Stats CSV — full run history
cat working/extraction-stats/wiki-pass2-stats-core-v1.csv

# Question queue — should all be resolved
cat working/wiki/pass2-buckets/questions-for-matt.jsonl

# Conflict + contradiction queues
cat working/wiki/pass2-buckets/conflicts.jsonl
cat working/wiki/pass2-buckets/pass1-contradictions.jsonl

# Node count by directory
find graph/nodes/ -name '*.node.md' | awk -F/ '{print $3}' | sort | uniq -c
```

### 2. Sample 15-20 nodes by hand

Don't sample randomly — stratify. Pull 3-5 from each of:

- **High-traffic POVs** (e.g., Eddard Stark, Jon Snow, Daenerys, Tyrion if they made it into core)
- **Ambiguous-name buckets** (e.g., Aegon, Brandon, Robert — anything where disambiguation could bite)
- **Single-page oversized buckets** if any (long wiki pages chunked section-by-section)
- **Routine buckets** (a typical small bucket of related entities)
- **Anything that surfaced a question during Stage 1**

For each sampled node, check:

- **Frontmatter:** `name`, `type`, `slug`, `confidence`, `wiki_source`, `bucket_id`, `prompt_version`, `node_version`, `pass_origin`, `first_available` all present and sane
- **Slug match:** does the file slug match the manifest's `expected_nodes`? (Silent renames are the known validator gap.)
- **Wiki grounding:** do citations like `(wiki:Eddard_Stark)` appear in body sections? Are they consistent with `wiki_source`?
- **Identity section:** present, factual, doesn't drift into speculation
- **Edges section:** populated from infobox-derived relationships (`OWNS`, `BORN_AT`, `DIED_AT`, `SIBLING_OF`, `MEMBER_OF`, etc.); edge targets look correct
- **Notes section:** any disclosed overrides, anomalies, or self-corrections
- **Body length:** roughly proportional to source page richness (5-15 short sections is typical)

### 3. Score the systemic patterns

After sampling, answer these in writing (in the Stage-2 session, not in the handoff prompt):

- **Slug rename rate:** how many sampled nodes have slugs that don't match `expected_nodes`? Anything >10% means the validator gap is starting to hurt.
- **Disambiguation incidents:** how many surfaced as questions? Were they all resolved cleanly upstream (triage rule fix) or just papered over (resolution = "agreed")?
- **Type override frequency:** how often did the agent apply a `type:` other than what the bucket suggested (e.g., `character.human` → `character.direwolf`)? High frequency means the triage type-classification needs work.
- **Cite-source bias:** are nodes citing `wiki:` predominantly, or `track_b:`, or chapter narrative? Wiki-heavy is expected for Pass 2.
- **Edge yield:** mean edges per node. Sparse edges (<3) suggest the parser isn't extracting infobox relationships well.
- **Cost per node:** total core spend / total nodes. Ballpark sanity check against the direwolves baseline ($1.15 / 6 nodes = ~$0.19/node).

### 4. Decision

Pick exactly one:

- **`proceed`** — Output is good enough to scale. No systemic issues. Sampled nodes are wiki-grounded, slugs match (or renames are transparent + filed as questions), edges populate.
- **`remediate`** — Surface-fixable issues found that would compound across 472 secondary buckets. Examples: a triage rule that miscategorizes a known pattern, a prompt drift that slowly degrades node quality, a validator gap that lets bad output through. Write a remediation continue prompt; defer Stage 3.
- **`escalate`** — Issues that can't be solved by the next Claude alone. Examples: ambiguity about what the secondary tier should even contain, a finding that suggests Pass 2 itself needs rethinking, a discovered cost dynamic that breaks the budget assumption. Write a `discuss-with-matt` continue prompt.

### 5. Write the handoff prompt

Use the template below. Land it at `progress/continue-prompts/<YYYY-MM-DD>-<short-description>.md`.

---

## Stage 2 prompt template (review session DoD)

The Stage-2 session's terminal output is a continue prompt for the next session. The shape depends on the decision:

### If decision = `proceed` → write Stage 3 prompt

```markdown
# Continue Prompt — Wiki Pass 2: Scale to Secondary Tier (~472 buckets)

**Created:** <date> end-of-Session-NN (Stage 2 review session)
**Goal:** Run all secondary-tier buckets through `weirwood wiki run secondary` to promote ~? wiki nodes.
**Cost envelope:** ~$<X-Y> ballpark, multi-day run. Authorized at Stage-2 review.
**Authorization context:** Stage-2 review of <N> sampled core nodes found no systemic issues. Slug rename rate <X>%, disambiguation rate <Y>%, type override rate <Z>%. Decision logged in worklog Session NN.

## Where this fits in the chain
Stage 3 of 3. See `working/runbooks/wiki-pass2-tier-handoff.md`.

## State at session start (verify before launching)
[same shape as scale-core prompt — bucket counts, node counts, question queue]

## How to launch
`weirwood wiki secondary <terms> <waves>` — same mechanism as core, larger surface.

## Multi-pass expectation
Same as core but more pronounced: expect 5-15 sessions across rate-limit windows. Triage-rule fixes from core may have already healed a chunk of secondary; re-run any `version-stale` buckets first.

## DoD
[same shape as scale-core DoD; final stage of Pass 2; no further handoff]

## Out of scope
[carry-over from runbook + Stage-2 findings]
```

### If decision = `remediate` → write fix-it prompt

```markdown
# Continue Prompt — Wiki Pass 2: Pre-Secondary Remediation

**Created:** <date> end-of-Stage-2 review
**Goal:** Fix <N> issues found in Stage-2 sampling that would compound across 472 secondary buckets. After fixes land, write a fresh Stage-2 review prompt; do NOT auto-proceed to Stage 3.

## Findings from Stage-2 sample
- [ ] Issue A: <description, sample evidence, proposed fix>
- [ ] Issue B: ...

## Why these block Stage 3
[1-2 sentences each]

## DoD
- All findings resolved (code change, prompt update, or triage-rule edit)
- Affected buckets re-run if needed (triage script flips them to `version-stale`)
- New Stage-2 review prompt written; this prompt archived
```

### If decision = `escalate` → write discussion prompt

```markdown
# Continue Prompt — Wiki Pass 2: Discuss with Matt Before Proceeding

**Created:** <date> end-of-Stage-2 review
**Goal:** Surface findings to Matt; do not proceed to Stage 3 without explicit direction.

## What I found
[narrative — concrete examples, not vibes]

## What I'm uncertain about
[explicit list]

## Options I see
[2-4 concrete paths, with trade-offs]

## What I need from Matt
[clear ask]
```

---

## Remediation branch

If at any point during Stage 1 a systemic blocker emerges (not a single-bucket question, but a pattern that suggests scaling will compound the issue), pause Stage 1, write a remediation continue prompt, archive the scale-core prompt only after the fix lands and the chain returns to Stage 1.

Examples of systemic blockers:
- Validator passing visibly bad output (not just slug renames — actual content drift)
- Cost-per-bucket diverging from baseline by >3× without explanation
- Multiple buckets producing nodes that contradict Pass 1 extractions in ways the contradictions queue isn't catching
- An auth / rate-limit pattern that the existing handlers can't recover from cleanly

Examples of NOT-systemic (handle in-line, don't pause):
- A single disambiguation question (file, resolve, move on)
- A single rate-limit window (already handled by existing rate-limit code path)
- A bucket that surfaces a "no infobox, can't extract" question (file as a tier-classification bug, defer)

---

## Why fresh Claude at Stage 2

The launching Claude knows what it ran, what surprised it, what it papered over. That context is useful during Stage 1 — it's how questions get triaged in-flight. But for the gate-or-proceed decision, that context is **bias**: the launching Claude is implicitly defending the choices it just made.

A fresh Claude reads the data only, has no investment in any prior framing, and can flag patterns the launching Claude rationalized away. This is the same reason Session 16's review caught 21 issues in the runbook the same Claude had drafted — context isolation buys honest evaluation.

The cost is one full session of Claude time spent reading instead of producing. Worth it before committing to a 472-bucket run.

---

## When this runbook needs updating

After the first end-to-end chain run completes (whatever date that is), revisit:

- Were the Stage-2 review checks the right ones, or did meaningful issues slip through?
- Did the decision tree map cleanly onto what was actually found?
- Are the prompt templates the right shape for the writer to fill in, or do they ask for context that isn't available?

Update v1 → v2 with what actually happened. Don't pre-optimize this runbook beyond what the first run teaches.
