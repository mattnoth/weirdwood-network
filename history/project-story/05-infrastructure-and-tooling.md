# 05 — Infrastructure and Tooling

> Part of the project-story series. Written 2026-06-11, after Session 91.
> Previous: [04 — The Edge Layer](04-edge-layer.md) · Next: [06 — Reification, Explained](06-reification-explained.md)

## Vitals

| | |
|---|---|
| **Sessions** | No era of its own — this chapter threads through all 91 sessions, Apr 13 – Jun 11, 2026 |
| **Recorded spend** | Negligible. This chapter's economics run the other direction: the infrastructure's measurable product is **~$4,400+ of avoided spend** — bulk runs that gates refused, agent pipelines that scripts replaced — against ~$770–830 actually spent on everything else. |
| **Output** | A chapter splitter; a session-state system that let 91 amnesiac sessions act like one project; the Python-first doctrine; an index layer; a lockdown-and-validation stack with 1,000+ hermetic tests; drift detection and NO-GO gates; a lineage of unattended-run supervisors ending in `longrun.sh`; and an audit discipline that repeatedly overruled the orchestrator itself |
| **The honest framing** | Nothing in this chapter is impressive to look at. It is the reason the impressive-looking chapters didn't collapse. |

Every other chapter in this story is about producing something — chapters, nodes, edges, events. This one is about the unglamorous machinery underneath, and it earns its place with a blunt claim: the project's distinctive achievement isn't the graph. The June audit said it outright — it's the **discipline stack** that produced the graph, the thing that kept a solo project run through dozens of memory-less AI sessions from becoming a plausible-looking swamp.

## The chapter splitter: the tool that just worked

It deserves first mention precisely because it never needed a second one. `scripts/chapter-splitter.py`, built in the project's first two days, split five raw `.txt` novels into 344 per-chapter markdown files with YAML frontmatter — and got every count right on the first real run. It is the project's only major tool with no incident, no rewrite, and no postmortem. Everything downstream — Pass 1, the indexes, the edge citations with their `file:line` references — stands on those 344 files being correct, and they were correct from day one. Worth noting because the rest of this chapter is largely about tools that *didn't* work the first time.

## The session-state system: how 91 goldfish ran a relay race

Each Claude Code session starts with no memory of the last one. The project's answer is a small constitution of files, each with a defined authority:

- **`worklog.md`** — the authoritative state file: current-state checklist, active decisions, and the five most recent session entries (older ones archive in five-entry blocks; there are eighteen archives now). Updated every session, no exceptions.
- **Continue prompts** (`progress/continue-prompts/`) — self-contained resumption documents for specific work tracks, written so a fresh agent can pick up mid-task without reading any history. Each one declares a recommended model (a rule in its own right — see the model-fit policy in [02 — The Book Passes](02-book-passes.md)).
- **`working/todos.md`** — the actionable backlog, treated as authority over anyone's recollection of what was pending.
- **`/endsession`** — a checklist command that forces the bookkeeping to actually happen before a session ends. It acquired its own guardrail the hard way: after being auto-run without permission two or three times, "never run `/endsession` unless explicitly told" became a standing memory rule.
- **Auto-memory** — cross-session memory entries for policies and hard-won facts, each one a point-in-time snapshot.

The system's defining bug-fix is **CLAUDE.md rule #9**, and it was born from a real incident. In Session 55 (May 18), a continue prompt and memory entries still claimed Pass 1 was incomplete ("ACOK 20/70") — weeks after the corpus had finished at 344/344. A session trusting the snapshot over the live state file propagated the stale claim. The fix wasn't "be more careful"; it was a written **staleness hierarchy**: when a continue prompt or memory contradicts `worklog.md`, trust `worklog.md`, *say the contradiction out loud at session start*, and flag the stale document. The audit counts at least four productive invocations since (S69, S72, S73, S90) — and, honestly, one fresh staleness incident as late as S90, which is why the rule is a hierarchy and not a cure.

The deeper pattern the project learned here: stale state propagation happened at least five separate times (S39, S49, S55, S69, S73) before the countermeasure was *structural* (a trust ranking written into the constitution) rather than behavioral (a resolution to do better).

## Python before Agent: the doctrine

The project's single most consequential process rule was instituted in Session 24 (April 27), at the bottom of a cost crisis. The wiki promotion pipeline ("Stage 1") had agents doing everything — and a cold review plus the spend math showed the remaining work projecting to **~$1,200**. The forensic detail that flipped the table: most of what the agents were "extracting" was infobox fields — *deterministic data sitting in structured HTML*. Paying a language model to retype it was pure waste.

The replacement Stage 3 promoted **3,314 nodes in about 30 seconds for $0**. From that day, the rule was project-wide: **whenever a deterministic Python step can produce part of the output, it runs first; agents do only what genuinely requires reasoning.**

The audit counts at least six subsequent wins where re-examining a "needs an LLM" task found most of it was deterministic: the Stage 3b prose extraction, the mention and entity indexes, the **edge spine** (2,834 cited edges for $0 — the foundation of `edges.jsonl`, see [04](04-edge-layer.md)), the hospitality edges, temporal scoping, and the alias resolvers. The pattern held with almost comic reliability: *every time a pass was re-examined, more of it turned out to be deterministic.* The doctrine's final vindication arrived with the June audit itself, which found the project's next big move — ~18–19k wiki infobox edges that would take graph connectivity from 14.7% to ~72% — had been sitting on disk, fully parsed, since April, needing exactly one Python script and $0.

## Agent-invented scope: the chat-UI and the 27-agent fleet (Session 26 → Session 37)

Before the Python-first doctrine hardened into discipline, the project had a near-miss with a different kind of scope explosion — not a runaway script, but a runaway design session. Session 26 produced a full chat-UI architecture document: three-corpus retrieval (books + wiki + graph), a Netlify deployment plan, a "D&D-group" friend-group auth posture, and a roster of **27 specialized agents** budgeted "~$1,250–2,310" for a single coordinated build sprint. It was technically coherent, internally consistent, and almost entirely orthogonal to what Matt actually wanted: a citation-grounded traversable graph for AI agents, with no chat layer and no auth system. The document went unquestioned for ten sessions. Session 37 retired the architecture doc to `history/archive/sketches/` as "stale sketch, not Matt's design"; the 27-agent fleet was never executed; the fleet-specs remain in `working/agent-fleet-specs/` today. The fleet's only shipped descendant is the mission protocol (watcher/worker, drafted around Session 48), which was used approximately three times and has been dormant since mid-May. The lesson is the bluntest one the project learned: **an agent can produce confident, elaborate, internally-consistent deliverables in a domain the owner never asked for.** The defense isn't better engineering — it's the owner reading what was produced before ten sessions of momentum build around it.

## The index layer: making 8,000 files queryable

Built almost entirely in the Phase 6 hygiene era (S36–S51) and almost entirely in pure Python: 344 per-chapter **mention files** mapping which entities appear where (entity resolution pushed from 70% to 72.9%), **3,910 per-character indexes**, plus location, artifact, and house indexes, and the **alias resolvers** that map "the Imp," "Lannister of Casterly Rock," and "Tyrion" to one slug. None of it is glamorous; all of it is what lets an edge cite `agot-bran-01.md:47` and lets a downstream agent find every chapter touching a given character without grepping the corpus. Notably, the index layer is where the dialogue/meals/voice "passes" of S34–S38 — scope an agent invented without being asked, killed at design review — left their only survivor: the mention index was the one piece that was actually needed.

## The lockdown stack: making cheap models safe

This is the machinery with the strangest origin story: it was built for a track that died. Five weeks of the Stage 4 wiki-comention era ([04](04-edge-layer.md)) went into making LLM edge classification safe, the candidate source was then deprecated wholesale — and the safety machinery turned out to be the durable product. The audit is explicit: the spend wasn't pure loss, because every later LLM pass ran on this stack.

What it consists of, accumulated incident by incident:

- **A locked edge-type vocabulary** — grown through formal review rounds (96 → 132 → 149 → 159 → 163 types during the comention era; ~166 today), each addition Matt-approved, each rejection recorded. One type, `KNOWS`, was deprecated *out* after data showed an 82.3% fallback rate — models reached for it whenever they were unsure.
- **Qualifier enums and the death of the `notes` field** — every freestyle text surface in the output schema either got an enumerated value set or got deleted. The reasoning, crystallized after the Haiku smoke test failed at ~80% semantic drift (S54): *the durable fix is locking every surface a model can improvise on, not writing sterner prompts.* This later became a standing rule — before any 20+ minute agent prose pass, lock every freestyle surface first.
- **Mechanical validators** — schema validation that runs as code, not as model judgment: type contracts (KILLED_BY must target a person), direction rules, verb gates, and **suspicious-edge flaggers** that route schema-clean-but-semantically-fishy patterns to a review worklist instead of trusting them.
- **1,000+ hermetic tests** across the pipeline scripts.
- **Drift-halt exit codes** — bulk runs that *stop themselves* when output stops conforming, rather than cheerfully writing garbage all night.

The proof of the stack is Haiku's rehabilitation: the model that failed at ~80% semantic drift before lockdown ran the Tier-1 bulk at ~3–4% violations after it. The lockdown — not a better model, not a better prompt — is what made the cheapest model safe to use, which is what made the project affordable.

## Drift detection, NO-GO gates, and the $4,400 that wasn't spent

The companion rule, made mandatory after the same era: every bulk LLM run gets a smoke test first, a precision gate it must clear, and drift detection while it runs — and the gate's verdict is allowed to be *no*. It was allowed to be no even when saying no hurt:

- The extra-tables enrichment (S68–S74): smoked three times at 60–74.5% precision against a 75–80% gate. **~$11 of smoke tests held back a ~$270–290 bulk.** Three times the orchestrator came back with a refined filter; three times the out-of-sample number missed the gate; the bulk never ran.
- The Events-Haiku bulk (S77–S81): the cruelest case, because the run itself was *operationally flawless* — ~$50, zero drift halts, ~85–90% on hand-read smokes — and the cross-model audit still returned NO-GO (structural edge types like TRAVELS_TO at 17% precision). Nothing was promoted. The output sat parked until the reification era found a legitimate use for it as cluster input.
- The Stage 1 → Stage 3 pivot (~$1,200 avoided), the never-run Sonnet bulk remainder (~$615), a ~$340 Sonnet Events run that never happened, and roughly $2,000 of a projected Sonnet-heavy month — all refused by gates or replaced by Python.

Total: **~$4,400+ avoided**, on ~$800 actually spent. The smoke tests also kept catching what the test suite couldn't — real bugs found "by doing, not by the green tests" at least three times (the S67 vocab drift, S69 generator bugs, S66 misresolutions). The governing value, held through three consecutive NO-GO decisions, was written down early: *a wrong cited edge is graph pollution.* The gates are what kept that sentence from being decoration.

## The unattended-run saga: six incidents, three eras, one supervisor

If the project has a recurring nightmare, it's this one: launch a bulk run, walk away, come back to a surprise. It happened at least **six times across three separate eras**, and the lesson — unattended runs need fail-fast, resume, and rate-wall detection *from day one* — had to be relearned in each era before it finally stuck.

The incident list, told straight:

1. **S22 (Apr)** — the Stage 1 wiki run hit the 7-day rate limit mid-flight; burned the window.
2. **S33 (May 4)** — the `--chain` terminal explosion: auto-advance flags caused every spawned terminal to spawn more terminals, doubling per cycle, while a claim-race bug let parallel terminals extract the same chapters. ~$19 wasted; the feature was deleted, not fixed. Full story in [02 — The Book Passes](02-book-passes.md). The rule it minted — *never let spawned workers spawn workers; single coordinator loop only* — shaped every wrapper after.
3. **S61 (May)** — wasted batches in the comention bulk.
4. **S64 (May 22)** — the **dual-run mystery**: a second overnight `run-forever` chain launched from an origin that was never definitively identified. Double quota burn, 24 output files clobbered, ~$15–20 wasted. The root cause was never found — the mitigation was structural instead: provenance stamps (`run_id`, `prompt_sha`) written *into the data*, plus single-instance guards, so a future mystery run would at least be identifiable and non-destructive.
5. **S76 (late May)** — the idle night: a run that simply didn't proceed while the window it should have used expired.
6. **S84–S85 (early Jun)** — the Plate 3 overnight pair: a retry loop burned the rate window before fail-fast logic existed, and a *silent* rate wall dropped 324 events without any error surfacing (all recovered); separately, an `--all` flag bypassed a selective gate and minted junk micro-beat hubs, whose contaminated output was discarded.

The tooling lineage tracks the scar tissue. First, per-track **run-forever wrappers** (`stage4-run-forever.sh`, `stage4-haiku-run-forever.sh`, `stage4-tail-bulk-forever.sh`, `edge-reify-run-forever.sh`) — single-coordinator loops that sleep through rate-limit walls and relaunch, with configurable sleep profiles (20-minute parallel-safe default, 10-minute burst, hour-plus conservative). Then, finally, the generalization: **`scripts/longrun.sh`**, a generic long-run supervisor built and tested on 2026-06-11 (in a session running parallel to the one that produced this story). It supervises *any* command under an explicit **exit-code contract**: `0` = all work complete, stop; `2` = rate-limit wall, sleep an hour and relaunch; `10` = iteration succeeded with more work remaining, sleep and continue; anything else = crash, with bounded consecutive-crash retries before giving up. Resume semantics belong to the supervised command; the supervisor just relaunches the same argv. The legacy wrappers remain untouched and migrate to thin call-throughs track-by-track as each finishes its current run — in keeping with the project's habit of never yanking infrastructure out from under a live process.

It took the project two months to converge on something a battle-scarred ops engineer would have written in week one. The defense is that each era's failure mode was genuinely different (spawn explosion, ghost launch, silent wall) — and the honest reading is that the *pattern* (harden before you walk away) was available after the first incident and got fully institutionalized only after the sixth.

## Count-based health checks: three false alarms

A smaller but instructive failure family. Three times, a health check that compared *counts* — file counts, remaining-work counters — raised an alarm that a check comparing *keys* would have dismissed:

- **S63**: a "missing files" panic during the bulk run.
- **S71**: the big one — "~7,251 unpromoted nodes," which paused the edge work for a full session. A slug-intersection check in S72 showed 7,039 of 7,047 wiki entities already promoted; the node layer was whole. The *real* gaps the false alarm half-concealed were elsewhere (14 entity categories missing from the index, and validator contract bugs) — both fixed once the panic cleared.
- **S80**: a wrapper's remaining-count disagreed with reality.

Each was resolved the same way: reconcile by key (slug intersection), not by count. The wiki crawl's case-collision bug — ~125 pages silently lost to a case-insensitive filesystem, undetected for four weeks because the *file count* looked fine — is the same lesson from the opposite direction ([01](01-scaffolding-era.md)). The project's standing health-check idiom is now key-based, and "file count looks right" is treated as no evidence at all.

## Estimate optimism: low by 2–7×, every single time

A pattern worth stating without softening, because it never failed to appear: **every significant estimate in this project was low, by a factor between 2 and 7.** The wiki crawl: estimated 6–8 hours, took ~36. Pass 2 cost per bucket: budgeted $0.71–1.43, actual $2.58. Extra-tables enrichment: ballparked ~$100, projected out at $270–290. Plate 3 event volume: the pre-reification estimate was 200–300 hubs; the pipeline's candidate pool reached 2,056 after D8's selectivity gate was applied, but the gate then filtered that pool down to **217 minted hubs** — so the estimate was low on candidates (~7–10×) but the *minted* count fell within the same order of magnitude as the forecast. The lesson stands (measure before you spend), but the "actual" here is a candidate pool, not a final output.

The project never fixed its estimator — there is no evidence the *initial* guesses got better. What it fixed was its *exposure* to bad estimates: measured re-baselining after first contact (the smoke test exists partly to replace the estimate with a measurement), and spend gates denominated in measured unit costs rather than hoped-for ones. The practical rule a reader should take: don't debias the forecast, structure the work so the forecast doesn't matter past the first checkpoint.

## The audit discipline: the system that overrules its own orchestrator

The most distinctive piece of the whole apparatus. A solo project run through AI sessions has an obvious failure mode: the same context that did the work reviews the work, finds it good, and compounds its own errors. The project named this early — Session 16, reviewing its own plan, accepted 21 of 21 review findings and flagged its own unanimity as suspicious — and built countermeasures from about S57 onward:

- **Fresh-eyes subagents**: before any significant spend or scaled run, a subagent with no carry-over context pressure-tests the findings.
- **Cross-model judges**: bulk LLM output audited by a *different* model than the one that produced it.
- **Out-of-sample validation**: never trust a filter measured on the sample it was built from; require stability across at least two fresh samples.
- **The reporter/auditor loop** (S84): paired agents where one reports and an independent one audits, institutionalized for the reification plates.

What makes this section earn its place is the track record of the discipline *winning arguments against the orchestrator*. The cold review of S24 returned `remediate` against the orchestrator's own pipeline. The S71 "7,251 missing nodes" claim was overturned by a fresh check. The S81 Events audit is the sharpest example: a fresh-eyes subagent corrected *both* sides — the audit had miscited which session a smoke test came from, *and* the orchestrator's framing of the result was wrong — and the corrected verdict was still NO-GO. Add the S57 encoding decision (deliberately delegated to a fresh context to dodge author bias), the S82 cleanroom analysis that found the reification root cause, and the S83 catch of a factual error in a design decision. Roughly seven recorded instances of independent review changing the outcome.

The audit's own summary is the right one: the graph's precision floor — ~78% strict precision with verbatim citations, rather than a plausible-looking swamp — *exists because of this discipline, not because any one model was good.*

## What it taught

- **Write the constitution down, and give it a precedence order.** Five staleness incidents preceded rule #9; zero process resolution survived contact with a fresh session unless it lived in a file the session was forced to read.
- **Determinism is the default; reasoning is the exception you pay for.** The single highest-leverage sentence in the project. Every re-examination of an "LLM task" found deterministic majority share — every time.
- **Lock surfaces, don't sharpen prompts.** Schema obedience comes from enums, validators, and halt-codes — from removing the places a model *can* improvise — not from asking more firmly.
- **Let the gate say no.** The NO-GO verdicts were the system working, including the one against a flawlessly executed run. ~$4,400 of restraint against ~$800 of spend is the project's real balance sheet.
- **Harden unattended runs before the first launch, not after the sixth incident.** Fail-fast, resume, wall-detection, single coordinator, provenance stamps. The lesson cost three eras; `longrun.sh` is its 40-line tombstone.
- **Reconcile by key, never by count.** Three false alarms and one month-long silent data loss all trace to counting.
- **Assume estimates are 2–7× low and build checkpoints that don't care.**
- **Pay for fresh eyes.** The cheapest model in the project's fleet was the subagent that had never seen the conversation — it found errors no amount of orchestrator diligence did.

## What compounds

Nearly everything in this chapter compounds by design — that's what infrastructure means. The splitter's 344 files anchor every citation in the graph. The worklog/continue-prompt/rule-#9 system is what lets session 92 start where session 91 stopped. The lockdown stack and the smoke-gate-audit loop are reusable for every future LLM pass, including the analytical Passes 3–6 that remain unbuilt. `longrun.sh` and its exit contract are the standing pattern for every overnight run to come. And the audit discipline compounds most of all, because it's the only piece that improves the *other* pieces: it's the part of the machine pointed back at the machine.

*Next: [06 — Reification, Explained](06-reification-explained.md).*
