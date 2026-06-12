# 02 — The Book Passes

> Part of the project-story series. Written 2026-06-11, after Session 91.
> Previous: [01 — The Scaffolding Era](01-scaffolding-era.md) · Next: [03 — The Wiki Work](03-wiki-work.md)

## Vitals

| | |
|---|---|
| **Sessions** | S6–S15 (schema evolution, Apr 16–25) + S30–S35 (corpus completion, May 1–6, 2026) |
| **Recorded spend** | ~$234 for the keeper (Pass 1 v3, all five books) + ~$35 for the discarded v2 run + ~$19 of duplicate-extraction waste from the S33 incident. v1's cost went untracked. |
| **Output** | **344/344 chapters** extracted — AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73 — each to an 18-section structured file with a strict 12-category entity index |
| **Model** | Opus, every chapter, all five books — deliberately |
| **Discarded along the way** | Two full AGOT extraction runs (v1 and v2) and fifty v2 ACOK chapters, all archived, none deleted |
| **The punchline** | Bought as "mechanical extraction." Turned out to be the project's primary-source candidate generator — and its highest-ROI spend. |

## What Pass 1 actually is

Pass 1 is the project's claim on the books themselves. For every one of the 344 chapters across the five novels, an extraction agent reads the chapter — and *only* that chapter — and produces a structured markdown file inventorying everything in it: who's present versus merely mentioned, where the chapter happens, what people eat, what they wear, what they say, what they do to each other, and what the POV character privately thinks about all of it.

The final (v3) schema runs eighteen sections deep: chapter metadata, physical environment (weather, light, sounds, smells), characters present, character appearances, characters referenced, locations and their descriptions, artifacts and objects of significance, **food and drink**, **hospitality and guest right**, events and actions, spatial layout and movement, information revealed, dialogue of note, the POV character's internal state, relationships observed, unanswered questions — and, at the bottom, the **Raw Entity List**: every entity in the chapter, filed under exactly twelve mandatory category headers (Characters, Locations, Houses, Factions & Organizations, Religions & Faiths, Cultures & Peoples, Artifacts & Objects, In-world Texts & Songs, Magic & Phenomena, Wars & Conflicts, Titles & Offices, and Other). Empty categories say "None." Renaming, merging, or omitting a header is forbidden.

That bolded pair — food and hospitality — is not an accident of taxonomy. It's Matt's design conviction made schema: in these books, guest right is a load-bearing institution, meals are where alliances and betrayals are staged, and GRRM hides Chekhov's guns in the descriptions of bread and salt. The extraction rules say it outright: *"Don't skip boring details. A three-sentence description of a meal matters. A throwaway line about a character's hair color matters."* The schema also declares direwolves and dragons to be characters, not animals — Ghost and Drogon get rows in the relationship tables like anyone else.

The other defining rule is **chapter isolation**. The extractor is told to treat the chapter as if no other chapter exists. It has broad ASOIAF knowledge — it is, after all, a large language model that has read these books — and it is forbidden to use it. No citing other chapters. No "this foreshadows the Red Wedding." And explicitly: **no dramatic irony**. If a character believes something the reader knows from elsewhere to be false, Pass 1 records only that the character believes it. The prompt is blunt about it: *"If you catch yourself writing 'the reader knows from X' or 'this foreshadows Y' — stop. Delete it. That is not Pass 1 work."* Cross-chapter pattern-finding belongs to the later analytical passes; Pass 1's job is to give them a clean, uncontaminated, per-chapter inventory to build on. This discipline is what later made the extractions trustworthy as *evidence* — every row traces to one chapter's actual text, not to the model's memory of the series.

## The schema wars: v1, v2, v3 (April 16–25)

Pass 1 did not arrive fully formed. It took three schema versions and two thrown-away runs of the longest setup book to get right — about ten days, all spent on *A Game of Thrones*.

**v1** was the first honest attempt: run an extraction prompt across all 73 AGOT chapters and see what comes back. It came back competent and thin. When Session 7 (April 22) reviewed all 73 outputs, the gaps were physical: no systematic capture of character appearances, no food or drink, no hospitality, no location interiors, no weather, no sense of how bodies moved through space. The extractions knew *who* and *what happened*; they were nearly blind to *what it looked, smelled, and tasted like* — which, for this project's design values, meant they were missing the point.

**v2** (Session 7, run April 23) was the corrective: six new schema sections — Physical Environment, Character Appearances, Food & Drink, Hospitality & Guest Right, Location Descriptions, and Spatial Layout & Movement — plus time markers, the direwolves-and-dragons-are-characters rule, and a philosophical flip from "leave empty if N/A" to **"be expansive, never invent."** Variance between runs was reframed as a feature: two extractions of the same chapter that notice different details are both right, as long as neither makes anything up. The full AGOT re-run cost $35.04.

**v3** (Session 10, April 24) fixed what v2 had left soft: the entity index at the bottom. v2's Raw Entity List had only four loose categories, and a coverage analysis showed magic, wars, and titles severely under-indexed — exactly the entity types a knowledge graph needs to be able to find later. v3 expanded the list to the strict twelve categories with the no-rename/no-merge/mandatory-headers formatting rules, and — decisively — **archived every prior extraction and started AGOT clean for a third time.** Sessions 10–12 ran the full v3 pass; by April 25, AGOT was 73/73 in v3 and both earlier runs were sitting in `extractions/archives/` (a standing project rule: archives are never deleted — v1 and v2 remain on disk today as comparison artifacts).

Two full re-runs of a 73-chapter book is an expensive way to design a schema, and it's worth being honest that it happened because the schema was designed against real output rather than in the abstract. It's equally worth being honest that the abstract approach had been tried first and produced v1. The lesson the project actually banked: **you find out what an extraction schema is missing by reading what it extracted**, not by reviewing the prompt — and re-running a book is cheaper than carrying a known-deficient corpus through every downstream pass forever. The corollary lesson — *finish the schema before you run five books* — was learned just in time. Every book after AGOT ran exactly once. (Almost. See ACOK, below.)

This stretch also built most of the project's session-state machinery — continue prompts, `/endsession`, todos-as-authority, and the "no extractions without asking" rule, instituted after the orchestrator violated it — but that story belongs to [05 — Infrastructure and Tooling](05-infrastructure-and-tooling.md).

## The interlude, and "I need to get the books in then"

After AGOT v3, Pass 1 paused for a month. Sessions 16–29 went to the wiki: the Pass 2 promotion campaigns, the cost blowout, the Python-first pivot ([03 — The Wiki Work](03-wiki-work.md)). Pass 1 resumed only when Session 30 (May 1) forced a sequencing decision: the upcoming wiki edge-discovery work wanted to compare wiki claims against Pass 1 mentions, and doing that against an AGOT-only corpus meant re-running the comparison every time another book landed. Matt's call, quoted in the worklog: **"I need to get the books in then."** Pass 1 corpus completion jumped the queue. It was the right call for reasons nobody fully appreciated at the time — see the punchline section below.

## The completion campaign (May 1–6)

Five days, four books, one shared-account favor, and the project's most embarrassing operational incident.

**ACOK and the schema mix.** ACOK had actually been run overnight before Session 30 — on v2, because the run predated v3. Session 30 finished the remaining 20 chapters on v3 and then had to admit what it had: a 70/70 "complete" book that was secretly a schema mix, chapters 1–50 in v2 and 51–70 in v3. The fix was a 50-chapter re-run; the v2 originals were archived (never deleted) to `extractions/archives/acok-v2-original-2026-05-04/`.

**The `--chain` terminal explosion (Session 33, May 4).** To make the ACOK re-run hands-off, Session 31 added `--chain` and `--delay` flags to the extraction launcher: launch a batch, wait two hours, automatically launch the next, spreading token usage across rate-limit windows. Session 33 launched it. What happened instead: every spawned terminal independently re-ran the launcher *with `--chain` still set*, so each batch spawned its own next batch — the iTerm tab count doubled every cycle, 2 → 4 → 8. Worse, a second latent bug fired underneath: the completion check only recognized *finished* extraction files, not in-progress ones, so overlapping terminals would each decide a chapter was "missing" and extract it simultaneously, last writer wins. And the attempted cleanup made it *worse*: the terminal commands were chained with `;`, so killing a step simply advanced each terminal to its next step — which spawned more tabs. Total damage: roughly **$19 in duplicate extractions**, plus the in-flight API calls killed mid-stream. The `--chain` feature was deleted outright within two sessions — not patched, deleted — and replaced by a six-item hardening patch: per-chapter status enums with heartbeats in the stats CSV, atomic claims via `flock`, stale-claim sweeps, a live status table, and streamed extraction output in the terminal. The durable rule it minted: **never let spawned workers spawn workers.** Every unattended-run wrapper the project built afterward — and it built several ([05](05-infrastructure-and-tooling.md)) — uses a single coordinator loop.

**The all-Opus decision — made in the same breath as the cheapness rule.** Session 33 has a second claim to fame: it's where Matt instituted the project's **model-fit policy** — default to the cheapest model that can do the job, Opus only when reasoning depth genuinely requires it. And in the very same session, he explicitly scoped Pass 1 *out* of that policy: every book would get at least one full Opus pass before any cheaper model was even smoke-tested, for consistency with the AGOT v3 baseline. The irony is real, and so was the reasoning: Pass 1 is the corpus's foundation layer, variance-between-runs was already a tolerated property, and stacking *model* variance on top of *run* variance across books would have made the five books subtly non-comparable. So Pass 1 became the all-Opus exception to the cheapest-viable rule — bought once, at full price, deliberately. (No extraction file records its model; "all five books were Opus" survives only as a Matt-confirmed memory entry, which is its own small lesson about provenance.)

**AFFC, ADWD, and the fixed launcher.** AFFC (46 chapters) ran as the canary book; ADWD's 73 chapters completed May 5 under the post-fix launcher, with some duplicate wave residue from before the fix landed — all valid v3, last-writer-wins. By Session 34 the count stood at 262/344.

**Okey's ASOS run.** The fifth book wasn't extracted by Matt at all. Okey — a friend with access to a shared Max account — ran all 82 ASOS chapters as a parallel Opus pass between May 1 and May 6, pushed them on branch `pass1-asos-extraction`, and Session 35 spot-checked early, middle, and late waves before merging: full v3 schema, healthy, ~$54.85. It was a one-off favor, not a collaboration model (the worklog is careful about this — the project is solo), but it's the reason the corpus finished on May 6 instead of days later, and it doubled as an accidental robustness test: the v3 prompt produced conformant output in someone else's hands, on someone else's machine, with no prompt adjustments.

**May 6, 2026: 344/344.** All five books, single schema, single model.

## The punchline: what $234 actually bought

Here is the part nobody wrote down in April, because nobody knew it yet.

Pass 1 was budgeted, justified, and executed as *mechanical extraction* — step 4 of a pipeline, a preprocessing stage whose product would be indexed and then mostly superseded by the analytical passes. What it actually became is visible only from the far end of the project, and the June audit said it plainly: **Pass 1 is the project's primary-source candidate generator, and easily its highest-ROI spend.**

The evidence, in sequence:

- **The edge spine.** When five weeks of trying to classify edges out of wiki prose dead-ended (the Stage 4 comention saga — [04 — The Edge Layer](04-edge-layer.md)), the Session 65 forensics that killed it also found the replacement sitting in the project's own repo: the **Relationships Observed** tables across 344 extractions held 7,348 first-party relationship rows — observed in the books, chapter-attributed, against 29,259 noisy wiki comentions. The deterministic spine built from those tables produced 2,834 cited edges for $0, and `edges.jsonl` — the project's central artifact — descends from it directly.
- **Hospitality edges.** The Hospitality & Guest Right section — the one that exists because Matt insisted food and guest right were first-class data back in v2 — was mined deterministically into typed edges. A design value became a schema section became graph structure, with no model in between.
- **Temporal scoping.** The `time_markers` metadata field, added in v2, fed the deterministic temporal-scoping work on the edge layer.
- **Reification.** When the project rebuilt events as first-class hub nodes (the Plates era — [06 — Reification, Explained](06-reification-explained.md)), the event beats came from Pass 1's **Events & Actions** tables.
- **POV canonicalization and the indexes.** The mention files, character indexes, and alias resolution that make the graph navigable are all built over Pass 1 output.

Every one of those was possible because Pass 1 had been run **expansively** (capture everything, even the boring meals), **isolated** (every row grounded in one chapter's text, citable to file and line), **uniformly** (one schema, one model, five books), and **structurally** (twelve mandatory categories, strict tables — machine-mineable, not prose). The properties that made the v1→v3 schema war and the all-Opus decision feel expensive in April are exactly the properties that made the corpus *re-minable* in May and June. The wiki gave the project its nodes; Pass 1 gave it everything the graph can actually *prove*.

About $234 for the keeper run. Roughly $54 more in tuition — the discarded v2, the S33 waste — to learn how to do it. The audit's spend ledger puts total recorded project spend at ~$770–830; no other line item on it comes close to Pass 1's downstream yield per dollar.

## What it taught

- **Design schemas against real output.** v1's gaps were invisible in the prompt and obvious in the extractions. The cost of finding out (two AGOT re-runs) was real, but it was paid *before* scaling to five books — the order matters more than the waste.
- **Lock the schema, then run the corpus once.** The ACOK schema mix was the price of running a book the night before the schema finished. Every subsequent book was single-pass.
- **Constraint at extraction time is value at mining time.** Chapter isolation, the no-dramatic-irony rule, mandatory category headers, no meta-commentary in table cells — every rule that made the extractor's job stricter made the corpus more machine-readable later. The strictness *was* the product.
- **Never let spawned workers spawn workers.** ~$19 and one exploding terminal wall bought a coordinator-loop rule that every later unattended run obeyed.
- **Uniformity is a feature you buy up front.** The all-Opus, single-schema decision can't be retrofitted. It looked like gold-plating in May; by June it's why cross-book comparisons need no caveats.
- **You don't always know what you're buying.** The project's best purchase was justified by a pipeline role it ultimately outgrew. The honest generalization isn't "extractions are magic" — it's that *expansive, well-structured, provenance-clean primary-source data keeps paying in ways its original justification didn't predict*, and cheap-but-loose data (the wiki comentions) keeps costing in ways its low price didn't predict.

## What compounds

The 344 extraction files themselves — still being re-mined as of Session 91. The 12-category Raw Entity List as the corpus's stable index surface. The hospitality and food tables, waiting for whatever the dialog era wants from them. The chapter-isolation discipline, which is why a Pass 4 foreshadowing pass (designed, never yet built) can trust that its inputs aren't contaminated with hindsight. And the coordinator-loop rule from S33, which threads through every overnight wrapper the project has run since.

*Next: [03 — The Wiki Work](03-wiki-work.md), or jump to [04 — The Edge Layer](04-edge-layer.md) to see the Pass-1 tables get mined.*
