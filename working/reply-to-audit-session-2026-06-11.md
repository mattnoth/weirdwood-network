# Reply to audit session — 2026-06-11

(If you are the audit session reading this file directly: this IS Matt's reply. Execute it.)

Synthesis accepted — all three wiki-layer verdicts agreed, infobox merge greenlit as next track, prose-comention stays dead.

PRIORITY, so this doesn't get twisted: the PROJECT is the main thing — organizing the repo, making the documentation tell the truth, the merge spec, the outline. The human-readable deliverables (project story, explainers, glossary) are byproducts we harvest BECAUSE the organizing work has the right context loaded — produce them along the way, never at the expense of project work. If anything has to give, the human-readable docs give first.

EXECUTION MODEL: you are the coordinator for ALL of this — every step below, not just Step 4, runs through subagents. You scope each task, fan it out fresh, review what comes back, integrate. Do not write deliverables inline in your own context; spend your context on coordination and review. This session does NOT defer the way past sessions did. Read nothing beyond what's listed; trust your synthesis.

Work in this order so nothing is lost if context runs short.

STANDING RULE FOR THIS SESSION — fresh-eyes critique: every major deliverable (the doc fixes, the project story, the reification explainer, the nomenclature proposal, the merge spec + explainer, the outline, the schema legend) gets reviewed by a FRESH subagent that had no part in producing it, prompted to find what's wrong, missing, or unclear — not to admire it. You read the critique, fix what's real, note what you rejected and why. Same principle as our out-of-sample validation rule: never trust work reviewed only by the context that produced it.

## STEP 0 — Persist first (cheap insurance)

Write your full synthesis + the complete doc-rot punch list to disk (working/audits/ or wherever fits) before anything else. Everything below draws on them, and subagents can read them from disk instead of you re-explaining.

## STEP 1 — Fix the documentation NOW (punch list, mechanical edits)

- CLAUDE.md pipeline table: Pass 2 / index rows say "Not started" — correct to actual state.
- worklog.md Principles #4: still asserts the pre-S24 spoiler-gating position — fix.
- worklog.md Current State: "graph/edges/ still EMPTY" contradicts the 4,757-edge entry below it — reconcile.
- Ideas/HIGH backlog: prune shipped items ("write the chapter splitter" etc.).
- Plus everything else on your punch list. A fresh agent reading top-down should no longer get lied to.

THE REAL TARGET of this step: when it's done, there must be ONE trustworthy "where am I" surface — worklog.md Current State — that answers, at a glance: what's shipped, what's in flight, what's gated on what, what Matt reviews next. Matt opens this project and currently has to re-derive his own position every time. Fix that. If Current State can't carry it alone, propose the minimal extra surface (e.g., a short STATUS section) — but ONE surface, not another scattered file.

## STEP 1b — todos.md cleanup

working/todos.md has accreted: resolved sections still sitting at full length (NODE/EDGE RECOVERY marked RESOLVED since S72, Path B Promotion "complete", Session 27/28 audit findings), stale items mixed with live ones, no quick way to see what's actually actionable. Clean it: move resolved/historical blocks to history/ (or collapse to one-line pointers), group what remains by live track, every surviving item gets a status the eye can scan. Same rule as everywhere tonight: nothing deleted, only moved or collapsed — and the result must make "what's actually open" obvious at a glance.

## STEP 1c — Continue-prompt triage (progress/continue-prompts/)

Subagent-able. There's a pile of continue prompts and no way to tell live from stale. Produce a manifest (progress/continue-prompts/README.md): one line per prompt — date, track, status (LIVE / DONE / STALE-superseded-by-X / MERGED-into-worklog), recommended model if declared. Per CLAUDE.md rule 9, worklog.md wins every conflict — mark contradicting prompts STALE with a one-line note rather than editing their content. Matt should be able to open this README and know exactly which threads are actually open.

## STEP 1d — Canonical design document(s): the organizing spine

This is HOW we organize from now on: the project's design lives in one all-encompassing design document — or a small canonical set if one is genuinely too much (e.g., data model / pipeline / tooling / features) — and everything else in the repo either feeds them or points at them. Right now design intent is scattered across architecture.md, agent-fleet-specs/, mission-protocol, runbooks, stale sketches, and 91 sessions of worklog decisions.
- Inventory what design-ish material exists and where.
- Propose the canonical structure (one doc vs the small set, and what lives in each) — brief proposal, I pick.
- Then build it via subagents: consolidate the scattered material into the canonical doc(s), with every absorbed source either retired to history/ with a stale-tag or rewritten as a pointer. architecture.md stays the data-model spec (CLAUDE.md rule 6) — it likely becomes one of the canonical set, not a casualty.
- End state: a new contributor (or a fresh agent, or me after two weeks away) reads the design doc(s) and understands what this system IS and WHY — without archaeology. The Step 3b outline and Step 2c legend plug into this set rather than floating free.

## STEP 2 — Project story (history/project-story/)

Expand your history audit into a human-readable narrative while it's in context — a byproduct of the organizing work, harvested now because rebuilding this context later would be expensive. It's for ME first (I don't remember the twists and turns); it may feed articles later, but that's not the goal here. Write for a reader with zero project context.

- A glossary decoding ALL internal verbiage: Passes 1–6, Stages, Plates 0–5, Tracks, Tiers 1–5, Modes, buckets, sessions/sprints, "smoke before spend," the discipline stack. The verbiage has gotten genuinely confusing — this is where it gets untangled.
- The chronological story with the twists and turns preserved: what we tried, what failed, what it cost, what we learned, what compounded. Expound on the wiki work especially — crawl, Pass 2 promotion, the comention deprecation, the infobox-layer irony you identified.
- Keep the spend/savings/failure-mode quantifications — those numbers are the spine of any article.
- ORGANIZATION: structure the story by major workstream, weighted by how long each was actually worked on — one chapter per big effort, depth proportional to the sessions it consumed. From your audit you know the real proportions; expect something like: Book passes (Pass 1 across 5 books), Wiki work (crawl → Pass 2 promotion → comention saga → infobox layer), Stage 4 / the edge layer, Reification (Plates 0–5), Infrastructure & tooling (splitter, weirwood CLI, wrappers, validators), plus a short one for the early scaffolding era. Each chapter opens with its vitals: session range, calendar span, approximate spend, what shipped. The overview file is the spine that links them in chronological order.
- Multiple files fine (overview + glossary + workstream chapters). Human-facing prose, not agent-facing bullets.
- REQUIRED CHAPTER — event reification, explained in detail. I don't really get it, and I approved it. Write a dedicated explainer (its own file) for someone who didn't sit through the design sessions: the problem it solves (why an n-ary event like the Red Wedding can't be honest dyadic edges), what an event hub node is, what the role edges mean (AGENT_IN, VICTIM_IN, COMMANDS_IN, LOCATED_AT), what SUB_BEAT_OF beats are and why they exist, what Plates 0–5 each actually did, and what the graph could NOT answer before that it can now. Walk the Red Wedding through end-to-end as the worked example — the actual nodes and edges in our graph, the 8 sub-beats, a 2-hop traversal shown step by step ("who ordered whom to do what" answered by following real edges). Diagrams-in-text (ASCII or mermaid) welcome.

## STEP 2c — Schema legend (one-page cheat sheet)

A quick key/legend I can keep open while looking at the graph — reference/schema-legend.md (and keep it in sync with architecture.md, per CLAUDE.md rule 6):
- The locked edge vocabulary: every edge type, grouped by family (kinship, fealty/politics, affect, interaction, event-role, structural...), one line each — meaning, direction convention (who is source, who is target), and current count in graph/edges/. Derive the canonical list via scripts/build-edge-type-counts.py (the canonical extraction — never a naive grep of prompt files).
- The node schema: entity types and their subtypes (entity.type.subtypes) as they actually exist in graph/nodes/ — one line per type with count, key frontmatter fields, and where multi-type cases stand (Citadel, Faith of the Seven).
- Confidence tiers 1–5 and the evidence_kind values, one line each.
Compact over complete — this is the at-a-glance card; architecture.md stays the full spec.

## STEP 2d — The honest worth assessment (domain-agnostic take)

Your synthesis hinted at this ("the distinctive achievement is the discipline stack"); make it a real deliverable — a standalone piece giving your unsentimental take on what this project is actually worth. No flattery, no hedging:
- THE AGNOSTIC BENEFITS: strip away ASOIAF — what here transfers to any domain? The methodology (Python-before-agent, smoke-before-spend, vocab lockdown, drift detection, provenance-in-every-row, audit gates, cross-model review) as a reusable playbook for building LLM-extracted knowledge graphs from any corpus; which parts of the pipeline are corpus-agnostic machinery vs ASOIAF-specific; what someone would pay for / reuse / learn from.
- YOUR TAKE on the real worth: what's genuinely novel here vs what's commodity; who this matters to (me, agents traversing it, fans, a hiring manager reading the repo, someone replicating the method); what the strongest single claim the project can honestly make is.
- THE WEAKNESSES, same candor: what's overbuilt, what a skeptic would say, what would have to be true for this to matter beyond a portfolio.
This one especially gets the fresh-critic treatment — a take that flatters me is worthless.

## STEP 2b — Nomenclature reform proposal (the verbiage gets FOCUSED, not just documented)

The glossary above decodes the historical terms; this deliverable retires the chaos going forward. You have the full history loaded — you know better than anyone where the terms overlap, collide, and confuse. Produce a short proposal (working/, for my decision — propose, don't enact):
- The canonical scheme going forward: a small fixed set of term categories with clear definitions (e.g., what kind of work gets called a Pass vs a Stage vs a Track — and which of Plates/Modes/Sprints/buckets were one-off internal names that should never be reused for new work).
- A collision map: which existing terms overlap or mean different things in different eras (e.g., "Stage" in wiki Pass 2 vs "Stage 4"), and what each should be called unambiguously when referenced from now on.
- Rules for naming NEW work so this doesn't re-accrete (e.g., "new multi-step efforts get a named track + numbered steps; no new top-level term categories without a worklog decision").
- What it costs to adopt: which living docs (CLAUDE.md, worklog, todos, agent prompts) reference old terms and would need a one-time terminology sweep. Historical docs and history/ stay as-is — the glossary maps old→new; no retroactive rewrites.
I review the proposal, pick the scheme, and the terminology sweep runs as a later mechanical pass.

## STEP 3 — Infobox-merge spec (spec now; build via subagent in Step 4)

- Wiki edges Tier 2 maximum, never Tier 1 (Tier 1 stays earned-by-book-quote).
- Every merged edge: `evidence_kind: wiki-infobox`, `typed_by: python-infobox-map`, cite `wiki:<Page>`.
- Quarantine multi-value speculative fields (Jon's two listed mothers = no PARENT_OF mint); filter Unknown/None/Extinct targets (~2.5%).
- Fold in both hygiene fixes as part of the same script pass: the 115 orphan endpoint slugs + the missing typed_by/file:line on the 948 reified role edges.
- THE SPEC MUST EXPLAIN ITSELF TO ME, not just instruct the script. I want to actually understand what's being promoted before I approve anything. Include a plain-language explainer section: what the infobox layer IS (where the 20,614 rows came from, what a row looks like raw), what "promotion" means concretely (this row → this edge in graph/edges/, shown with 3-4 real before/after examples), the full promotion rule set with a worked example PER RULE — one row that gets accepted and why, one that gets filtered and why, one that gets quarantined and why (use the Jon Snow two-mothers case) — and the expected counts by edge type after filtering. The dry-run report later checks against these expectations.

## STEP 3b — Overall outline: from here to the features

One document (working/ or reference/, your call): the map from where the graph is NOW to the things I actually want to build with it. This is the "where is this all going" doc that doesn't exist anywhere.
- The destination features, named explicitly: talking to a character (voice profiles + perception edges + graph traversal grounding the dialog), theory exploration (theory nodes + evidence scoring), foreshadowing/Chekhov's-gun lookups, timeline/chronology queries, spoiler-gated reading companion (deferred but on the map), and whatever else the existing pass stubs (Passes 3–6) imply.
- For each feature: what graph capability it needs, what of that already exists, what's missing, and the rough sequence of work to close the gap.
- For each piece of remaining work, TAG THE EXECUTION MODE: deterministic script (Python, $0, no approval friction) vs LLM pass (gated, costed, needs lockdown per our rules) vs Matt-decision. The script-taggable items matter most — they can run anytime without ceremony, and I want to see how much of the remaining road is actually free.
- Keep it honest about sequencing: infobox merge → Mode 3 dip → whatever the dip's failures say. Don't present a fixed grand plan; present the map plus the decision points.

## STEP 4 — Subagent fan-out: push it (after Steps 0–3 are done)

So much has been deferred session after session; you have the whole project loaded, so spend it. Delegate to subagents in this priority order, as far as your context allows. Hard rules: NOTHING writes to graph/ this session — anything graph-bound stops at a dry-run report or a curation/ proposal; sources/ and scratch files untouched as always; you review each subagent's output before accepting it.

1. **Merge script build to dry-run** — subagent implements the Step 3 spec (deterministic Python), produces the dry-run report (counts by edge type, what got filtered and why, 20-edge sample). No graph writes; I review the dry-run, then a later session ships it.
2. **Organize history/** — worklog-archives and session-details are a pile. Subagent gives each folder a README/index (what's in each file, date ranges, sessions covered), normalizes naming if inconsistent, and cross-links to the project-story chapters from Step 2. Moves within history/ are fine; nothing leaves history/.
2b. **scripts/ inventory** — there are dozens of scripts and no map. Subagent produces scripts/README.md: one line per script — what it does, which track owns it, status (LIVE / LEGACY-migrate-to-longrun / SUPERSEDED-by-X / ARCHIVE-CANDIDATE). The six run-forever wrappers get tagged LEGACY-migrate-to-longrun. Do NOT move or delete anything — this is the map; archiving moves happen in a later session off this inventory.
3. **Small Plate-4/5 TODOs** — the 2 deferred collisions and the mutual-kill reverse-direction edges (propose to curation/, don't write graph/); the 32 empty-quote SUB_BEAT_OF rows (write me a one-page decision memo with a recommendation, don't act); display-bullet regen (dry-run diff only).
4. **109 hub-review-queue triage** — subagent triages into keep/fix/quarantine buckets with one-line reasons, output to curation/ for my review.
5. **`weirwood run` subcommand** — bank the long-run supervisor off the weirwood CLI so every long-running claude job launches the same way and logs the same way. Subagent (script-builder style) extends scripts/weirwood.zsh with a `run` case forwarding to a new scripts/weirwood-run.sh: a declarative track registry (`weirwood run start edge-reify`), commands list/start/logs/status/stop, every run logged to working/logs/longrun/<track>-<timestamp>.log via LONGRUN_LOG with a latest-symlink and pidfile, legacy tracks (stage4-tail, stage4-haiku, stage4-events) listed but marked LEGACY-not-yet-migrated (refuse to launch them), plus a `start custom -- <cmd>` escape hatch. scripts/longrun.sh already exists and is tested — build on it, don't reinvent it. Match the dispatcher conventions already in weirwood.zsh (wiki/stage4 cases). Test against a scripted child before calling it done; add working/logs/ to .gitignore if not covered.
6. **Deeper repo organizing** — if you STILL have room: draft the reorganization plan the 2026-06-07 repo-audit continue prompt was going to produce (what moves where and why — a plan document, not the moves themselves).

## QUESTION (answer from data you already have, no new agents)

Of the 85% isolated nodes, how do theories/prophecies/speculation nodes specifically fare, and what would connect them? The infobox merge won't touch those — I want the shape of that gap.

## FYI for your worklog entry

A couple of legacy run-forever wrappers failed; a central supervisor (`scripts/longrun.sh`, exit contract 0=done / 2=wall / 10=more-work / other=crash) was built and 4-scenario tested in a parallel session today. Legacy wrappers migrate to it per-track as their runs finish — see working/todos.md, Extraction Infrastructure. Also new in todos.md under Doc Hygiene: the project-story item (Step 2 here).

## Still deferred (the short list that genuinely must wait)

- Mode 3 validation dip — runs AFTER the merge lands, on the merged graph.
- Shipping the merge to graph/ — gated on my dry-run review.
- Backfill tracks A/B/C — gated on what the Mode 3 dip reveals.

## End-of-session

Update worklog + todos.md. Write a continue prompt (with Recommended model line) for the merge-ship step. Do NOT run /endsession without asking me.

---

## ADDENDUM (added after initial send — applies to the whole session)

The organizing principle for ALL of the organization work — the repo-reorg plan, the todos grouping, the scripts inventory, the history/ indexes, the design-doc set — is BY WORKSTREAM / TASK: edge modeling, wiki work, book passes, reification, infrastructure, etc. The random files scattered through working/ and progress/ should map (in the plan, and eventually in the moves) to the workstream that produced them, mirroring the project-story chapters and the Step 2b nomenclature scheme. One taxonomy everywhere: the story's chapters, the nomenclature's track names, the todos' groups, and the directory structure should all speak the same workstream names. If a file genuinely belongs to no workstream, that's a finding, not a misfit — list those separately.
