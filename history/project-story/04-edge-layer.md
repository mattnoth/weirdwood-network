# 04 — The Edge Layer

> Part of the project-story series. Written 2026-06-11, after Session 91.
> Previous: [03 — The Wiki Work](03-wiki-work.md) · Next: [05 — Infrastructure and Tooling](05-infrastructure-and-tooling.md)

## Vitals

| | |
|---|---|
| **Sessions** | S52–S64 (wiki-comention era), S65–S74 (Pass-1 pivot + edges v1), S75–S81 (Events-Haiku attempts) |
| **Dates** | May 13 – June 1, 2026 |
| **Spend** | Comention era: **~$150–190** (Sonnet ~$50–90 + Haiku ~$100, incl. ~$15–20 dual-run waste). Pass-1 spine: **$0**; Sonnet tail: **$20.88**. Extra-tables smokes: **~$11**. Events attempts: **~$75–85** ($20.81 Sonnet partial + ~$50–55 Haiku bulk + ~$3.60 bake-off + $0.93 audit). |
| **Spend avoided by gates** | **~$1,200+** ($615 Sonnet bulk remainder + $270–290 extra-tables bulk + ~$340 Sonnet Events re-run) |
| **What shipped** | `graph/edges/edges.jsonl` — **4,760 typed edges**, ~99% carrying a verbatim book quote, ~3,800 with exact `file:line` citations, 0 orphans, ~78% strict precision — plus the lockdown-and-audit machinery every later LLM pass runs on |
| **Governing value** | *"A wrong cited edge is graph pollution — worse than no edge."* It survived three NO-GO decisions, each one killing a run that money had already been budgeted for. |

This is the methodology chapter. Nodes say what exists; **edges** say how things relate — `jaime-lannister KILLS aerys-ii-targaryen`, `arya-stark SIBLING_OF sansa-stark` — and they're where a knowledge graph either earns trust or quietly poisons it. A node that exists wrongly is clutter. An edge that asserts wrongly is a *lie with a citation*. The project spent three weeks learning how to extract edges safely, mostly by failing at it in instructive ways.

---

## 1. The wiki-comention era (S52–S64): the right machinery on the wrong source

### The plan

Stage 4's original design: take the wiki's chapter-summary prose, find every pair of entities mentioned near each other — **29,259 candidate comentions** — and have an LLM classify each pair against the project's edge vocabulary, with evidence snippets. Sonnet as the worker, ~201 batches, projected several hundred dollars.

### Schema drift, discovered the hard way

The bulk launched in mid-May and got 21 of 201 batches in (~$50–90) before quality checks found the first systemic problem: **schema drift**. The model's output format wandered — missing required fields, invented edge types, evidence snippets that were section headers rather than prose. The first broken batch (batch-0012) became a calibration artifact: a new **mechanical validator** was written and self-tested against it, catching 14 of 14 known violations. A memory rule crystallized that outlived the whole track: *every bulk LLM run includes a mechanical validator + cross-model audit, and the audit verdict gates resumption — regardless of model.*

### The lockdown grind

What followed was two weeks of systematically removing every surface where a model could freestyle. In rough order:

- **Vocabulary lock rounds.** The edge-type vocabulary was empirically derived (from wiki infobox field frequencies, then from what classifiers actually encountered) and grew through governed review rounds: ~96 types at the start of the era → 132 → 149 → 159 → **163/164**, each addition debated and each rejection logged ("reverse-direction duplicate," "too generic," "derivable"). After Session 56 the vocabulary was declared **FINAL** — new gaps got rejected as `no-fitting-type-vocab-locked` instead of minting types. (Reification-era additions later brought it to ~166.)
- **Qualifier enums.** Edge qualifiers ("formerly," "claimed," "salt wife") were a freeform drift surface. Session 57 locked them: 8 edge types with *required* closed-set enums, 9 with optional enums, and the other ~140 forbidden from carrying qualifiers at all.
- **The `notes` field was deleted entirely.** Matt's "zero freeform" call: any field where a model can write prose is a field where drift hides.
- **Verb gates as schema.** ENCOUNTERS could only be emitted if the evidence contained an actual staging verb ("met," "confronted"); the validator enforced it mechanically, not just in the prompt.
- **KNOWS was deprecated** (vocab 164 → 163) after measurement showed **82.3% of KNOWS emissions were fallback** — the model reaching for it whenever nothing else fit. A type that mostly means "I don't know" isn't a type.

### The Haiku smoke that failed — and the one that passed

The economics demanded a cheaper worker, so Session 54 smoke-tested Haiku. The result is one of the project's most instructive failures: the output was **validator-clean and ~80% semantically wrong**. SERVES emitted for everything, KILLED_BY reversed, type contracts violated wholesale. Schema compliance and truth are different properties; a lockdown that only checks shape certifies fluent nonsense.

The response was not a better prompt — it was **removing the need for the model to do anything but classify**. The enrichment pipeline (S63) rewrote all 141,067 candidate rows (in 13.5 seconds of Python) so each row arrived as a complete decision unit: the evidence paragraph pre-extracted, anchors normalized, valid edge types pre-filtered by type contract, staging-verb hints pre-computed. No file reads, no lookups, no judgment about what's relevant — just *this evidence, these allowed types, decide*.

Re-smoked under full lockdown, Haiku came back at **~3–4% violations** — on par with Sonnet's ~4.3%, at a fraction of the cost, and ~5.5× faster per batch. The pre-lockdown failure run was deliberately archived (`_archive/batch-0012-haiku-failed-2026-05-15/`) as a before/after exhibit.

### The dual-run mystery

The Tier-1 Haiku bulk launched in Session 64 and ran 60 of 222 batches ($55.66, 5,723 edge rows) — during which a **second, unexplained `run-forever` chain appeared at 04:36**, alongside the legitimate one launched at 22:58. Not Matt, not the orchestrator, no scheduler found. It re-ran ~26 finished batches (~$15–20 waste), double-burned the quota window, and clobbered 24 output files. The root cause was **never definitively found**; the mitigation was structural rather than forensic — single-instance guards, and provenance (run IDs, schema versions) stamped *into the data* instead of inferred from directory names. Some incidents you solve; some you armor against.

### Deprecation — the honest framing

Session 65's forensics on the dual-run turned into something bigger: an audit of the candidate source itself. Conclusion: **wiki chapter-summary comentions were structurally noisy** — two names appearing in the same summary sentence is weak evidence of a typed relationship, and no amount of classifier discipline fixes a weak candidate pool. The track was deprecated wholesale — not deleted, *stamped*: 133 candidate files, 11,269 rows, marked in-data with `status: superseded, do_not_promote: true`. The 27 scripts stayed on disk as a recall lever.

So: five weeks and ~$150–190 on a dead end? Yes — and no. The candidate source was wrong, and that's stated plainly here because the project's records state it plainly. But everything the dead end forced into existence — the locked vocabulary, the qualifier enums, the mechanical validators, the verb gates, the no-silent-drop pipeline, the enrichment pattern, the drift-detection-with-cross-model-audit rule, the 1,000+ hermetic tests — **became the standing safety stack for every LLM pass that followed**. Roughly a third of all project spend went into this era, and it bought the machinery without which the rest of this chapter would have been a plausible-looking swamp.

---

## 2. The Pass-1-derived pivot (S65–S74): the better source was in the house all along

### The realization

The same Session 65 forensics asked the obvious-in-retrospect question: what's the *best available* candidate source for edges? The answer was the project's own **Pass 1 extractions** — the Opus-extracted structured tables from all 344 book chapters ([02 — The Book Passes](02-book-passes.md)). Their `## Relationships Observed` tables held **7,348 first-party relationship rows**: each one an explicit claim made by the books themselves, in a known chapter, with locatable evidence. Against 29,259 noisy comentions, that's a 4.6× cleaner feed with primary-source provenance. Stage 4 pivoted in one session.

### The deterministic spine ($0)

True to Python-before-Agent, the pipeline started with what code alone could do: parse the tables, resolve names to node slugs, type the relationship phrase where it matched exact or keyword patterns, and attach evidence. The result: **2,834 typed edges at zero LLM cost**, ~99% carrying a verbatim quote plus `file:line` citation found by a deterministic evidence locator.

Two findings from the spine build are worth their own sentences:

- **Resolution, not typing, was the wall.** 5,141 of ~7,400 candidate rows initially failed name→slug resolution — "Ned," "the Greatjon," "Lord Too-Fat-to-Sit-a-Horse" don't slugify. (The section summary above says 7,348 rows; the resolution pipeline's own counter logged 7,398 — a 50-row discrepancy attributable to dedup or filtering at the parse stage; "~7,400" covers both.) A five-rung collision-aware resolver (exact / alias / unique-first-name / context-present / context-prior) and first-name alias enrichment 2.7×'d the yield.
- **Spot-audits caught what green tests didn't.** Two systematic misresolution bugs survived 278 passing tests: generic role-words resolving to concept nodes, and a title-first-token bug that resolved 341 honorific-prefixed names to **`ser-pounce`** — Tommen's cat. The project's recurring koan — *"caught by doing, not by the green tests"* — got its mascot.

### The Sonnet tail ($20.88)

The rows the deterministic typer couldn't classify — 3,052 of them, genuinely context-dependent phrases — went to Sonnet in 40-row batches via `claude -p` subprocesses run from `/tmp` (skipping project context cut cost ~49%). A smoke-first gate caught a vocab-drift bug *before* the bulk: the prompt's vocabulary loader was naively scraping backticked tokens and had picked up deprecated `KNOWS` plus garbage like `ADWD` — invisible to the tests, fatal to the run. Fixed, smoked, then run: **2,385 typed edges for $20.88**, 0.88% validation violations. Add a deterministic harvest of Pass 1's Hospitality tables — 529 GUEST_OF / VIOLATES_GUEST_RIGHT edges, the Red Wedding among them, $0 — and the merge-and-filter step (endpoint quality gates, dedup, precision filter) landed **`graph/edges/edges.jsonl` v1: 3,842 cited edges**, committed Session 70. The graph was traversable for the first time.

### The S71 false alarm

One session later the edge work was **paused on a mistake**. Session 71 found 8,299 nodes in the graph but ~7,251 staged node skeletons in working directories and concluded a huge promotion backlog existed — edges couldn't be trusted until nodes were whole. Session 72 checked the same question with a **slug intersection instead of a file count**: 7,039 of 7,047 staged slugs were already promoted; the "backlog" was 8 files, all duplicates. The node layer had been whole all along. The *real* gaps the scare flushed out were an index that had never covered 14 of the node categories and a validator contract that falsely dropped real `COMMANDS → faction` edges (it only looked for targets among characters). Both fixed; 16 wrongly-dropped edges recovered; v1.2 applied; a resolver pass (disambiguating the ship *Lord Tywin* from the man, protecting the ship *Lady Marya* from becoming a person) settled the layer at **v1.3 = 3,811 edges**. The count-based-health-check lesson now had three notches in it.

### The `:11` bug — citations that all pointed at the same line

The era's last humbling: the evidence locator had a latent bug where `read_chapter_prose` stripped blank lines before sentence-splitting, so paragraph boundaries vanished and **nearly every citation pinned to the chapter's first prose line** — 3,784 of 3,811 shipped edges cited `:11` or its neighbors. The quotes were real and verbatim; the line numbers were decorative. Fixed deterministically and every citation re-grounded before the layer was declared shipped. A citation system, it turns out, needs auditing exactly as much as the claims it certifies.

### The enrichment NO-GO ($11 spent, $270–290 saved)

Pass 1 had more tables than Relationships and Hospitality: Events & Actions, Information Revealed, Food, Dialogue — **32,194 candidate rows** of potential edges. Smokes (~$3.60, then ~$4, then ~$3.40 — about $11 all told) measured strict precision at **60–74.5% against a 75–80% gate**, three separate times, including a head-to-head where post-lockdown Haiku hit 76% and Sonnet 78% — neither clearing the bar, and Sonnet's 2 points not worth 4.4× the price. One smoke run produced an apparently-passing ~80–91% — which a fresh-context Opus review exposed as **overfit to the sample the filter was built on**; out-of-sample it was ~62%. The bulk was never run. Session 74's verdict: ship the ~78% deterministic core; don't bolt a ~70% LLM layer onto it. The governing value, in its first full test: *a wrong cited edge is graph pollution.* (Matt later corrected the over-broad reading that this banned enrichment — the ruling was *gated*, not *banned*, which set up the next act.)

---

## 3. The Events-Haiku attempts (S75–S81): a flawless run that failed anyway

Enrichment came back deliberately: deterministic prep first, vocabulary locked, drift detection mandatory, Events chosen as the next surface. A Sonnet partial run ($20.81) was superseded when a model bake-off picked Haiku (~$50 projected vs ~$270 for Sonnet on the same rows). Then the bulk ran — and *operationally, it was the cleanest run of the project*:

- All **16,502 candidate rows** accounted for: **1,617 typed edges**, 14,884 rejected, 1 needs-qualifier
- Single prompt SHA, single model, **0 drift halts, 0 conform violations**, 99.6% verbatim quotes
- Real confidence-tier calibration (256 / 1,342 / 19 across tiers 1–3, where v1 had flatly said tier-1 to everything)
- The ~90% reject rate was *verified healthy* — a sampled false-reject check put unique-edge recall loss under ~15%
- Hand-read precision on in-flight output: ~85–93%

Then the gate did its job. The promotion chain's step 1 was a **cross-model drift audit**: a stratified 50-row sample, byte-identical prompts, Sonnet as judge ($0.93). Result: **48% triple-level agreement against a 70% floor** (56% pair-level against 85%). The structural edge types Haiku had emitted most confidently were where it agreed least: TRAVELS_TO 17%, TRAVELS_WITH 0%, LOCATED_AT 20%.

Matt didn't trust the number — in either direction — so a fresh-eyes subagent was sent in cold to pressure-test the audit itself. Its findings cut both ways, and both mattered:

- About **11 of the 22 disputed rows were genuine Haiku drift** (evidence-hint leakage, quotes not supporting both endpoints). The No-Go was substantively right.
- **3–4 were the judge over-rejecting** perfectly good edges, and ~7–8 were genuinely ambiguous — so the honest agreement range was ~56–70%: *borderline*, not catastrophic.
- The audit had **miscited its own baseline**: the "contradicting" smoke was from Session 77, not 69, and it measured a *different metric on a different sample shape* (a human hand-reading fresh candidates vs. a model judging stratified emits). The 85–90% and the 48% were both true. They were answers to different questions.

Verdict: **No-Go stands, borderline; nothing promoted; output parked.** The ~$50 wasn't wasted — the parked rows' event-title groupings became ready-made clustering input for Plate 4 of the reification era (~$35), which absorbed the best of them by a structurally different route. The deepest lesson of the whole arc sits here: *hand-read precision and judge-model agreement are different instruments, and a promotion gate needs to know which one it's reading.*

---

## 4. Where the layer stands

After the reification plates (the structural era that followed — events rebuilt as hub nodes with role edges; that story is told properly in [06 — Reification, Explained](06-reification-explained.md)) and the Session 88–91 validation work, the edge layer at the close of this story:

- **4,760 edges**: 3,809 from the Pass-1 pipeline, 897 reified event-role edges, 51 Plate-4 cluster edges, 3 curator-pilot edges
- **4,728 of 4,760 carry a verbatim evidence quote**; ~3,800 carry exact `file:line` references — a 2026-06-11 spot-check read 20 random rows and verified 5 of 5 sampled citations *verbatim at the cited line*
- **0 orphan edges, 100% endpoint resolution** (115 alias-mismatched slugs noted for hygiene), **~78% strict precision** on the deterministic core, with the known soft spot being hint-mapped affect edges that run slightly hot
- Confidence tiers actually mean something: 4,553 tier-1, 194 tier-2, 13 tier-3

And the governing value held. Three times — extra-tables, the overfit smoke, Events-Haiku — a run that money, momentum, and (twice) genuinely good-looking numbers argued for promoting was refused because it couldn't clear a precision gate. The edge layer is small because of those refusals. It is *trustworthy* for the same reason.

---

## What it taught

1. **The candidate source matters more than the model.** Five weeks of world-class lockdown engineering could not make 29,259 weak comentions into a good edge feed; one pivot to 7,348 primary-source rows produced a better layer in days, mostly for free. Improve the input before disciplining the worker.
2. **Lock every freestyle surface, then verify mechanically.** Vocab lock, qualifier enums, deleted notes field, verb gates, type contracts, no-silent-drop. Validator-clean is not the same as true (Haiku's 80%-wrong clean output proved it) — but validator-clean plus cross-model audit plus out-of-sample smoke is a floor you can build on. The machinery outlived the track that forced its creation.
3. **Smoke before spend, and never trust a filter on the sample it was built from.** ~$11 of smokes killed a ~$270–290 bulk; the gates collectively held back ~$1,200+. The one near-miss was an overfit filter — caught only because a fresh-context reviewer re-measured out-of-sample.
4. **Know which instrument you're reading.** Hand-read precision on fresh candidates and judge-model agreement on stratified emits gave answers 40 points apart on the same run, and both were correct. The S81 audit also miscited its own baseline — audits need auditing.
5. **Count-based health checks lie; reconcile by key.** The S71 "7,251 unpromoted nodes" panic paused real work on a file count. Slug intersection took an hour and ended it. (Third occurrence of the pattern; it finally stuck.)
6. **Cite, then audit the citations.** The `:11` bug shipped 3,784 confident, verbatim, *wrong-line* references. Provenance machinery is part of the trusted computing base, not an accessory.
7. **A wrong cited edge is graph pollution — worse than no edge.** The value survived three NO-GO decisions because it was applied when it was expensive and embarrassing, not just when it was convenient. That, more than any script, is why the graph can be handed to an agent.

*Next: [05 — Infrastructure and Tooling](05-infrastructure-and-tooling.md) — the wrappers, validators, and process discipline underneath all of this. For the structural era that followed the edge layer, see [06 — Reification, Explained](06-reification-explained.md).*
