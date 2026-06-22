---
session: 121
date: 2026-06-21
model: claude-opus-4-8 (orchestrator); all subagents attempted on Sonnet 4.6 (died to API overload)
title: Essos hardening pass + container-split — adapting around a persistent API outage
---

# Session 121 — Essos hardening + container-split (under an API outage)

Human-facing narrative. Agent-facing summary is the worklog S121 entry. Concise counts there; this file
records the reasoning, the incident, and two lessons worth keeping.

## What this session was supposed to be
The S120 handoff queued a 3-step plan off the advisory board: (1) a HARDENING pass (mostly deterministic
tooling + doc edits), (2) a 4-lens container-split advisory fan-out, (3) build the WO5K remainder. The plan
leaned heavily on subagents — script-builder for the tooling, a research subagent for the wedding refactor,
4 read-only lens subagents for the container split, and research+verify subagents for the build.

## The incident — a persistent Anthropic 529 overload
Every subagent dispatch this session died on `API Error: 529 Overloaded`. Six agents in the first wave
(script-builder, wedding-research, 4 container lenses) — the first round managed a few tool uses each before
erroring on a later call; the second round (a re-dispatch of the 4 lenses) returned **0 tool uses** — they
failed at dispatch. A single one-word probe agent ("reply ALIVE") also 529'd. The orchestrator's own
main-loop calls kept working throughout, so the overload was specific to subagent dispatch / a capacity pool,
not a total outage.

**The adaptation:** rather than repeatedly hammer a known-overloaded API, the orchestrator did all the
*deterministic and single-book* work in-house — which is defensible: the graph-query flags are deterministic
Python with a written spec; the Littlefinger mint was fully pre-researched in the S120 continue prompt
(verified + fresh-critic-reviewed); the wedding refactor is single-book ADWD close-reading. What it did NOT
do in-house: the 4-lens container split (the whole value is *independent parallel perspectives* — a solo
substitute loses that) and the WO5K build (Matt's FIRM rule: causal edges get fresh-subagent verify, not
the orchestrator). Those were deferred.

## Step 1 — what landed (complete)
Tooling (built in-house after script-builder 529'd): `graph-query.py` gained `--full-chain`/`--include-enables`
(causal walk that also follows ENABLES, labeled "(precondition)"), `--expand-beats` (surfaces SUB_BEAT_OF
children + role edges on chain nodes), and `--container <name>` (bag-retrieval over the new `containers:`
frontmatter). The headline payoff: `--full-chain fall-of-astapor` now walks the entire 9-edge Essos spine
to `dany-lost-on-dothraki-sea`, while `--causal-chain` stays correctly 0/0 — the #1 advisory-board finding
fixed, with the semantic ENABLES≠CAUSES distinction preserved. Plus `mint_arc_lib.py` (a `precheck_slugs`
floor-check) and `stamp_containers.py` (idempotent tagger). 17 new tests; full suite 1322 pass / 3
pre-existing fails (2 stale vocab-count assertions — 167 vs the real 169, drift from S116/S117 — and the
documented `cwd-is-tmp`).

Docs: architecture.md gained the ENABLES-vs-CAUSES-vs-TRIGGERS contract (with the `--causal-chain`
segment-break note), the L1/L2 verify gate-levels, and the `containers:` field schema. harvest-queue.md got
the line-check rule.

Graph: `arrest-of-eddard-stark` retyped event.battle→event.incident (+ its junk infobox display-bullets
corrected); `littlefinger-betrays-ned` minted as a constitutive SUB_BEAT_OF the arrest (NO CAUSES, per the
S120 granularity policy) with petyr AGENT_IN; the pre-existing `petyr-baelish BETRAYS eddard-stark` dyad's
broken evidence_quote repaired (it had cited the will-reading at :63, not a betrayal — repointed to the
dagger-under-chin payoff at :125).

## The wedding join-hub — and a lesson about connectivity
The continue prompt framed item 1.6 as "drop the over-strong `sons-of-the-harpy TRIGGERS wedding`; add
MOTIVATES daenerys." But grepping the live graph first showed the MOTIVATES-daenerys edges *already existed*
(S119 built them). So the real gap was different: the *proximate* cause of the Hizdahr marriage was
unmodeled. Close-reading ADWD Daenerys IV–VI surfaced it — **the Green Grace Galazza Galare's counsel** to
take a Ghiscari king is what answers *why Hizdahr* (vs the insurgency, which answers *why marry*). Minted
`galazza-counsels-the-ghiscari-marriage` → CAUSES wedding + MOTIVATES dany + AGENT_IN.

**The lesson (a near-miss):** the first pass *dropped* the TRIGGERS entirely. A `--full-chain` smoke test
caught the consequence — with the killings now only `MOTIVATES daenerys` (an actor-terminus) and the wedding's
only causal-in being Galazza's counsel (which has no upstream into the Slaver's-Bay spine), the wedding/Daznak
terminus was **orphaned from the astapor root**. Routing causation *through an actor via MOTIVATES* breaks the
event-to-event walk. The fix was to *downgrade* (not drop) the killings edge to `sons-of-harpy CAUSES wedding`
(the explicit 90-day bargain makes the insurgency a genuine mediated cause) — exactly the concept-doc §7
both-and pattern (MOTIVATES the actor AND CAUSES the event). Result: an honest 2-cause convergence hub that
still walks end-to-end. Takeaway: **after any edge drop/retype on a spine, run `--full-chain` to confirm you
didn't sever the walk.**

## Step 2 — container split: blocked, so a proposal stood in
The 4-lens fan-out couldn't run. The orchestrator authored a stand-in proposal
(`working/session-results/2026-06-21-container-split-PROPOSAL.md`): the factual backbone (all 30 foreshadowed
events → candidate containers, grounded by node-existence probes) plus recommendations, explicitly flagged as
a hypothesis for the fan-out to pressure-test, not a decision. **Key finding:** the board's NORTH + AEGON are
necessary but not sufficient — `riverlands` (Brotherhood/Stoneheart/Arya) and `kl-faith` (Cersei's arrest)
are also container-sized, and several already-built AFFC arcs are floating untagged.

## Matt's calls at close
- **Container choices are graph-shape decisions — give them their own dedicated subagent session.** Don't
  rush the SET at the tail of a hardening pass.
- **SHAPE > NAMES.** When asked how hard containers are to change later, the answer (by design) is: tags are
  trivially reversible — a `containers:` tag is metadata, not an umbrella node, so retag = find-replace,
  touching no edges/traversal/derived-artifacts. The *expensive* axis is the shape (partition / boundaries /
  seams / granularity) because **arcs get built under a boundary assumption** — a seam node built twice or an
  arc rooted in the wrong spine is real rework. So: get the shape right before mass-building; names can be
  provisional and refactored freely. This is the payoff of the tag-not-umbrella decision.
- The next live continue prompt was reframed accordingly:
  `progress/continue-prompts/2026-06-21-container-shape-analysis.md` (shape-first; build is a separate later
  session). The old fan-out→build prompt was archived with a superseded banner.

## Net
nodes 8,572→8,574 (+2); edges 22,379→22,384 (+5 net); edge types 132 (no new — all locked vocab); vocab 169
(unchanged); orphans 62 (unchanged). All S121 citation checks pass. `containers:` field adopted + 15 Essos
nodes tagged. Backups in `graph/edges/_regrounding/`.
