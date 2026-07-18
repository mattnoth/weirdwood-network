---
session: 218
date: 2026-07-16
track: graph
model: Fable 5 orchestrator + 1 Haiku adversarial fresh-verifier
graph_mutation: yes — first theory mint (edges 26,740 → 26,860; +7 nodes)
deploys: none
---

# Session 218 — The First Theory Mint

## Shape of the session

Opened as the S216-staged mint-gate review (continue prompt said "S217"; the
parallel README-sweep meta session had already taken that number in the worklog —
rule-9, worklog wins, this is S218). Instead of walking straight into the four
queued gate decisions, Matt stopped on the honest admission that he'd lost the
thread on how theory nodes actually work — "how the persona will differentiate
theories vs the source material… if theories will accidentally be displayed as
facts." The session's real value came out of answering that properly.

## The explainer that became a design

Walked the mechanics against the real files: the `concept.theory` node anatomy
(jojen-paste as the example — `claim:`/`status:`/`origin:` frontmatter, attributed
"The theory holds that…" prose), the SUPPORTS/CONTRADICTS one-level-removed
semantics ("this real passage is what the community reads as evidence" — verifiable
even though the theory isn't), and the four structural separations (tier floor,
edge-type isolation from the causal vocabulary, the layer rule keeping canon node
prose untouched, evidence-direction pointing INTO theory nodes).

The honest caveat given: the chat guardrail (agent.ts SHARED_RULES "do NOT
assert, allude to, hint at…") is prompt-level, not code-level — the bundle
builder ships all of edges.jsonl unfiltered, so a post-mint deploy would put
theory edges in the tools' reachable data with only the prompt standing between
them and an answer.

Matt's response was the design: **make it a toggle** — theories off by default,
and when on, the persona integrates them but always labels ("it's a theory /
this is speculation"). Adopted as the exposure plan of record:

- **OFF (default):** runtime tool-layer filter strips `concept.theory` nodes +
  SUPPORTS/CONTRADICTS edges from tool results — upgrades "the model is told
  not to" into "the model physically can't." Prompt guardrail stays as layer 2.
- **ON:** SHARED_RULES swaps the no-theories block for an attribution contract
  (name the theory, never state as narration, distinguish text-establishes from
  theory-infers, mention status incl. show-confirmed spoiler flavor). The
  `claim:` field is the ready-made summary; per-edge quotes keep it cite-gated.
- All three pieces have codebase precedent (parked Bloodraven voice toggle,
  persona prompt switch, tool handlers). Build = its own gated session.

## The foreshadowing thread → a new convention

Matt asked whether the evidence quotes would be foreshadowing-related ("that
would be good evidence and Alt Shift X does have those in videos"). They largely
are — for unconfirmed claims, planted material (songs, dreams, visions) is the
only on-page evidence that CAN exist. This surfaced the seam with the existing
factual-layer `FORESHADOWS` type and produced the **parallel-FORESHADOWS
convention** (Matt: "yes"): theory-evidence quotes that foreshadow *confirmed
on-page* events also get a canon-visible FORESHADOWS edge — dual-register, one
passage, two layers, two claims. This also resolved the Patchface subject-link
open question from S216 in the affirmative direction.

## The go and the execution

Matt: "okay go for it use cheaper sub agents when possible, etc im stepping
away" — mint all 13, ratify everything recommended (whodunit question-form
names, fab-* in wave 2, the S216 convention set), toggle as plan of record.

Execution (all deterministic where possible, per the Python-before-Agent rule):

1. Pre-req + baseline: S216 committed, tree clean, edges 26,740. **Tally
   correction found on the way in:** the "105 edges / 8 new + 6 enrich" figure
   in the prompt and worklog was stale — staged reality was **118 / 7 / 8**
   (verified by summing candidates.json files; the prompt's own per-cluster
   list already summed to 118).
2. 13× `mint_enrichment.py` (ajt first as live smoke) — every cluster: slug
   pre-check, re-run guard, line-check (118/118 quotes located at mint time),
   0 dup skips. 8 enrich files copied over live stubs.
3. Rider: 3 event nodes' dangling `](ramsay-bolton)` prose links → `ramsay-snow`.
4. `weirwood refresh` 5/5; probes: resolve "R+L=J" → r-plus-l-equals-j top
   candidate; neighbors returns the 8-edge evidence sheet.
5. architecture.md rule-6 sync: `concept.theory` type row rewritten + the
   Evidentiary section expanded into the canonical convention record.
6. **FORESHADOWS sweep:** deterministic scan of all 13 sheets for
   prediction-flavored beats → exactly 3 candidates (the Patchface songs).
   **P3 self-excluded by the convention's own test** — "we will march into the
   sea and out again" foreshadows the Hardhome *ranging*, which never departs
   on page (TWOW); the confirmed hardhome-catastrophe node covers the wildling
   disaster, not the marching. F1 (→red-wedding t3) + F2 (→purple-wedding,
   proposed t3) staged; **Haiku adversarial fresh-verifier: F1 CONFIRM, F2
   ADJUST→t4** (image-association vs narrative precision) — adopted, minted +2.
   Architecture wording widened to "tier 2–4 by mapping strength."
7. Gates: node quotes 3083/3083 · pytest 1458 · deno 102 · tier-floor audit
   118/118 ≥ t3.
8. Audit surprise: 4 pre-existing tier-1 SUPPORTS edges in the OLD interpersonal
   sense (luwin↔osha, renly→jon-arryn, haldon→ysilla) — semantic collision with
   the now-reserved Evidence→Theory meaning. Logged to todos as a 4-edge retype
   rider; not touched (outside the go).

## Worth remembering

- The wave's verification machine kept paying off at mint time: the mint
  script's own line-check independently re-verified all 118 quotes.
- The sweep pattern — adopt a convention, then let the convention's own test
  exclude a candidate (P3) — is the right shape; conventions that can say "no"
  to their own examples are trustworthy.
- Session numbering collided with a same-day parallel meta session for the
  first time since the S132 split; the write-order tiebreaker handled it, but
  continue prompts that pre-stamp session numbers will keep being wrong when
  tracks run same-day. (The foreshadows-sweep run_id carries the stale s217
  stamp — harmless, noted in the worklog.)
