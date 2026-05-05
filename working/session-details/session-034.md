---
session: 34
date: 2026-05-04
type: design / brainstorm
model: opus-4-7-1m (orchestrator); opus-4-6 (in-flight extraction)
duration: ~1 hour
commits: 0
agent_runs: 0 (no extraction runs initiated this session; pre-existing iTerm tabs from prior launch remain in flight)
---

# Session 34 — Schema-mismatch realization + cheaper-model brainstorm

## Context coming in

User had launched (just before this session opened) `weirwood acok 2 3 claude-opus-4-6` — 2 iTerm terminals × 3 waves = 6 incomplete waves (5,6,7,8,9,10) covering the 30 v2 chapters that needed v3 re-extraction. Terminals already running.

Bug A and Bug B from Session 33 had been fixed and committed in `5f9b808f` plus a UX cleanup pass in `f3cd92ba`. The URGENT BLOCKER from Session 33's todos.md is now resolved.

## What the user asked

User opened the session asking me to verify the just-launched ACOK run was set up correctly. I confirmed:

- Wave distribution: Terminal 1 → waves 5,6,7; Terminal 2 → waves 8,9,10. No overlap (each wave appears in exactly one terminal's slice of `INCOMPLETE_WAVES`).
- Currently-in-flight chapters at session start: `acok-catelyn-04` (wave 5, terminal 1) and `acok-jon-04` (wave 8, terminal 2). Both correct first-of-wave.
- Both using `--model claude-opus-4-6`.
- Stale `/tmp/extraction-stop` cleared at launch.

That was the operational portion. The rest was design conversation.

## The schema-mismatch realization

The conversation pivoted hard when the user opened `graph/nodes/` and noticed that the directory taxonomy doesn't match the Pass 1 v3 schema's 12-category Raw Entity List.

**Pass 1 v3 categories (12):** Characters · Locations · Houses · Factions & Organizations · Religions & Faiths · Cultures & Peoples · Artifacts & Objects · In-world Texts & Songs · Magic & Phenomena · Wars & Conflicts · Titles & Offices · Other.

**`graph/nodes/` directories (18 type-dirs + 2 admin):** characters, locations, houses, factions, religions, artifacts, texts, prophecies, theories, titles, concepts, customs, foods, languages, materials, medical, species, events, `_conflicts`, `_unclassified`.

The mismatches that matter:
- **Cultures & Peoples** (Pass 1) → `concept.culture` files in `concepts/` (graph). Pass 1 has no concepts bucket.
- **Magic & Phenomena** (Pass 1) → `concept.magic` files in `concepts/` (graph). Same collapse.
- **Wars & Conflicts** (Pass 1, single bucket) → `event.war` (multi-battle) vs `event.battle` (single engagement) in graph; `_conflicts/` admin dir of unclear purpose.
- Pass 1 has no first-class home for: foods, prophecies, customs, species, languages, materials, medical conditions. All would land in `Other` or the `Artifacts & Objects` flat list.
- Some of those (e.g., food/customs) ARE captured in dedicated prose tables — see "What Pass 1 actually captures" below.

User's first reaction: "I should have just done the wiki stuff, started it and started the graph before hand. because I cannot run a pass again."

I pushed back. The reframe:

1. **Pass 1's data is richer than the 12-category Raw Entity List suggests.** The prose tables above the flat list capture much of what the graph wants:
   - `Food & Drink` is its own dedicated section (prompt line 118)
   - `Hospitality & Guest Right` is its own section (line 126)
   - `Location Descriptions` carries materials/architectural detail
   - `Character Appearances` carries fielded physical descriptions
   - `Spatial Layout & Movement` captures place transitions
   - `Information Revealed` with reader-knowledge flags
   - `POV Internal State` for character-knowledge perspective
   - `Magic & Phenomena` as a category explicitly includes "prophecies-as-phenomena" per the prompt parenthetical (line 203)

2. **Re-categorization is a derivation, not a re-extraction.** Reading completed extractions and emitting graph-aligned candidate JSONL is a Python or Sonnet-light job. The expensive read of the chapter prose has already happened. The artifact is structured markdown.

3. **The wiki Pass 2 has built the graph in parallel** (Sessions 23–29). Graph nodes mostly exist. The bridge layer that integrates books and wiki is **Stage 4** (prose-edge-classifier, cross-identity-detector, contradiction-surfacer) — and it reads extractions, not raw chapters. So Pass 1's job for the graph is providing edges and evidence, which Stage 4 hasn't run yet. Order error wasn't an order error.

4. **Theories vs prophecies in Pass 1 — a literal absence vs a coverage absence.** I clarified: Pass 1's Raw Entity List has no `### Prophecies` and no `### Theories` sub-headers (literal absence). But prophecies absolutely *are* captured — they land in Magic & Phenomena (per the prompt parenthetical), Information Revealed, Dialogue of Note, POV Internal State. Theories are different: explicitly absent from Pass 1 by design, because chapter-isolation forbids the agent from saying "this is evidence for R+L=J." Pass 5 (theory-extractor) maps chapter facts to theory seeds retroactively. So Pass 1 gives Pass 5 the raw material; the un-run pass is the gap, not the data.

User accepted the reframe, dropped the regret, committed: "opus is the foundation now so I think I will just go through all five books the same way now."

## The bigger brainstorm

User re-scoped: running full Pass 1 passes book-by-book with Opus is exhausting weekly Max limits, and they want to run *more* passes without burning a week each. Brainstorm-mode requested.

The realization: Pass 1 has been treated as the Universal Read, with everything else cascading from it. But (a) much of "extraction" is deterministic search/regex, and (b) downstream "passes" should mostly read existing extractions, not re-read chapters.

Eight directions sketched:

**1. Deterministic before agentic.** Most "extractions" downstream are grep + regex on chapter files. Examples: dialogue by speaker, POV interior monologue (italics + free-indirect-discourse), character co-presence matrix, first/last appearance, name-mention frequency. All cost $0 — Python over `sources/chapters/` and `extractions/mechanical/`. The "BE Jamie" use case is almost entirely solvable this way without new model passes.

**2. Entity-centric extractions, not chapter-centric.** Add a derivation step:
```
extractions/character-corpus/{name}/
  dialogue.jsonl
  thoughts.jsonl       # POV interior, this character's chapters only
  described-by.jsonl   # how others perceive them, with POV cite
  knowledge-state/     # union of "Information Revealed" through chapter N where present
  relationships.jsonl
  locations.jsonl
```
Mostly Python collation over Pass 1 + raw chapters.

**3. Tiered model assignment as first-class.** Orchestrator picks one model per launch. Pick per task type instead. Haiku for dialogue speaker resolution + alias lookups; Sonnet for Pass 1 mechanical extraction (smoke-test first), theory evidence scoring, voice analysis; Opus only for genuine cross-chapter inference.

**4. Derive later passes from extractions, not chapters.** Foreshadowing-scanner reading "Information Revealed" + "Unanswered Questions" across all extractions is far cheaper than re-reading prose. Theory-extractor reading "Information Revealed" + "Dialogue of Note" + "Relationships Observed" same logic. Voice-analyzer reading `dialogue/{character}.jsonl` (Direction 1's deterministic output) is cheaper *and* more accurate than reading chapters.

**5. Batch API for everything that can wait.** 50% cost. Pass 1 doesn't need to be interactive. Foreshadowing scans, theory passes, voice analyses can wait 24h. Halves the weekly burn.

**6. CLAUDE.md surgery.** Loaded every session. Keep at top: two critical rules + pipeline status table summary + read-first directives. Move directory tree, subagent inventory, working/progress conventions, two-tier session documentation explanation to `reference/` files. ~70% reduction realistic. Same applies to MEMORY.md.

**7. The "BE Jaime" forcing function.** Use it as a Minimum Viable Extraction test. Persona prompt needs dialogue corpus + interior monologue + knowledge cutoff at chapter N + key relationships. Almost none of that needs a model. If Jaime ships from mostly-deterministic processing, that proves most of the architecture's "passes" were aspirational.

**8. Stop running passes book-by-book.** Wave-by-wave is sequential and blocking. Scatter-gather: queue of (chapter, pass-type, model-tier) tasks draining in any order.

User-prioritized first three:
1. **CLAUDE.md surgery** — half-day, immediate savings.
2. **Sonnet smoke-test on Pass 1** — already in todos.md, deferred until one book remains. Friend running ASOS on Opus from shared Max; user wants Opus consistency across the five books.
3. **Build the dialogue extractor in Python** — proves Direction 1 + 2 in one shot, gives the artifact for BE Jaime.

## The food example — extractions as targeting layer

User asked: can the existing extractions help downstream passes find food references in chapters faster, without re-reading the whole chapter?

Yes, materially. Three uses:
1. **Skip empty-bucket chapters.** If `Food & Drink` and `Hospitality & Guest Right` are both empty, downstream food work skips. Filters 30-40% of chapters before any chapter-read.
2. **Jump to the right paragraph.** Extraction lists "lamprey pie" → grep chapter for the string → ±20 lines. Token cost goes from "full chapter" to "two paragraphs."
3. **Adjacency signals catch missed meals.** "Took supper in the great hall" in `Hospitality & Guest Right` or `Spatial Layout & Movement` flags a meal happened — points downstream attention at the right scene without re-reading.

Same pattern for any thematic pass with a corresponding section: hospitality (guest-right work), spatial movement (travel/journey work), dialogue (voice work), information revealed (theory work). **The extractions are an index, not just an output.** That's their real downstream value, and it's why Pass 1 time isn't wasted even when categorization doesn't align with the graph.

## Decisions logged

- **Continue all 5 books on Opus 4.6** despite knowing Sonnet might suffice. Consistency wins over per-book optimization given user is mid-corpus. ASOS in progress on friend's Max; ADWD follows on user's Max. **Sonnet smoke-test stays deferred** until ADWD is the only book remaining.
- **Schema mismatch is a derivation problem, not a re-extraction problem.** Live with it. Plan a future Python or Haiku re-categorizer pass that reads completed extractions and emits graph-aligned candidate JSONL. Not urgent.
- **Theory work is unblocked by Pass 1's deliberate "no theory tagging."** The data is there; theory-extractor (Pass 5) will do the mapping when its prompt is written. No retroactive Pass 1 work needed.
- **Brainstorm directions** captured in this file + new todos. Top three priorities: CLAUDE.md trim, dialogue extractor (Python, deterministic-first), entity-centric character corpus derivation.

## What was not done

- No code changes.
- No agent runs (in-flight ACOK extraction predates the session).
- No commits.
- No prompt revisions.

## What's in flight as session ends

- 2 iTerm terminals running ACOK waves 5–10 on Opus 4.6 via the post-Bug-A/B `weirwood`. Expected result: ACOK 70/70 v3 complete after these waves finish (~5–8 hrs wall-clock from launch).
- ASOS being run by user's friend on shared Max account, on Opus 4.6, v3 schema.
- ADWD untouched.

## What next session should pick up

1. **Verify ACOK 70/70.** Once iTerm tabs idle, confirm `extractions/mechanical/acok/` has all 70 v3 extractions; archive the now-stale `2026-05-04-acok-waves1-10-rerun.md` continue prompt.
2. **CLAUDE.md trim.** Easy win. Doesn't burn extraction budget.
3. **Dialogue-extractor Python script** (BE Jaime forcing function). Validates deterministic-first; gives the chat UI a real artifact.
4. **ADWD Pass 1** when ASOS lands, on Opus 4.6 for consistency.
5. Stage 4 v1 once 344/344 Pass 1 complete.

The brainstorm directions (1–8 above) are not blocking; they reshape *future* pass design once Pass 1 stabilizes.
