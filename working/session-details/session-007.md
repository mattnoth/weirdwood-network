# Session 7 — Mechanical Extraction Schema v2 + Tooling

**Date:** 2026-04-22

---

## What Triggered This Session

Pass 1 v1 extraction had been run across all 73 AGOT chapters, producing a complete set of mechanical extractions. The question was: are they good enough? Matt and Claude reviewed the output together, and the answer was a clear no — not because the extractions were wrong, but because they were missing entire dimensions of the text that make ASOIAF distinctive.

## What Happened

### The Quality Review

The review of all 73 AGOT v1 extractions revealed a systematic pattern: the extractor was capturing plot events, dialogue, and character relationships competently, but was almost entirely silent on the physical world. GRRM's writing is famous for its sensory detail — the food at a feast, the exact description of a character's appearance, the architecture of a castle, the feel of weather and season. The v1 schema didn't ask for any of this, so the extractor didn't capture it.

Specific gaps identified:

- **Character appearances:** A knowledge graph that can't tell you what Tyrion looks like, or that the Alchemist in AFFC matches Jaqen H'ghar's post-face-change description, is missing one of the most useful cross-reference capabilities. Physical descriptions change across books (characters age, get scarred, cut their hair), so these need to be captured per-chapter, not assumed.

- **Food and drink:** GRRM describes meals in extraordinary detail. These aren't flavor text — they encode information about wealth, culture, regional identity, season, and political relationships. Who eats with whom matters. What's served at a feast vs. what's available during a siege tells a story.

- **Hospitality and guest right:** The moral and narrative framework around food and shelter. Guest right is a sacred custom in Westeros; its violation (the Red Wedding) is one of the series' pivotal moments. Tracking when it's invoked, offered, accepted, or violated is a distinct analytical concern from tracking what food is served.

- **Location descriptions:** Castles, taverns, godswoods, streets — GRRM describes physical spaces with enough precision to reconstruct floor plans. Defensive features, architectural style, condition (ruined vs. well-maintained), interior details. The v1 extractions captured *that* a scene takes place in Winterfell but not *what Winterfell looks like* in that scene.

- **Spatial layout and movement:** Characters move through spaces in ways that matter. Battle scenes, chase sequences, processions through cities — the path matters, not just the destination. This is inherently graph-structured: a sequence of movements between locations.

- **Weather, environment, time:** Season, time of day, lighting conditions, sounds, smells. These establish atmosphere but also encode timeline information (the slow onset of winter across the series) and foreshadowing.

### The Schema Expansion

The mechanical extractor agent prompt (`.claude/agents/mechanical-extractor.md`) was updated with six new schema sections:

1. **Physical Environment** — weather, season indicators, time of day, lighting, ambient sounds, notable smells
2. **Character Appearances** — per-character, per-chapter: hair, eyes, build, distinguishing features, scars/wounds, clothing, weapons/armor, apparent age. Explicitly: capture what the text says in *this* chapter, don't carry forward from previous chapters.
3. **Food & Drink** — specific dishes, ingredients where mentioned, preparation details, who's eating with whom, cultural significance if apparent
4. **Hospitality & Guest Right** — bread and salt offered/accepted, guest right invoked, hospitality violations, shelter offered or denied
5. **Location Descriptions** — defensive features, architecture, interiors, scale/size, condition, surrounding terrain
6. **Spatial Layout & Movement** — phase-based scene graph with a controlled vocabulary of movement types (Advance, Ambush, Assembly, Arrival, Ascent, Chase, Descent, Escape, Patrol, Procession, Retreat, Return, Sailing, Search, Siege, Sneak, and more). Each phase has a from-location, to-location, characters involved, and movement type. This creates directed-graph edges — mini scene graphs per chapter.

A `time_markers` field was added to Chapter Metadata for explicit timeline anchoring (days since an event, named dates, season references).

A new rule was added: direwolves and dragons are characters, not animals. Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog, Drogon, Rhaegal, and Viserion get their own entries in character lists, relationship tracking, and appearance descriptions. They have agency in the narrative and relationships with other characters.

### The Philosophy Shift

The most important change wasn't structural — it was philosophical. The v1 prompt's guidance was essentially "leave sections empty if not applicable." This produced terse, conservative output. The v2 prompt inverted this to "be expansive, never invent." The extractor should capture everything the text offers, err on the side of inclusion, and only hold back when something requires interpretation rather than extraction. If two runs of the same chapter produce slightly different outputs because one noticed a detail the other missed, that's a feature — it means the variance reveals the text's richness, and the union of runs is more complete than either alone.

This is the key insight of the session: **variance between extraction runs is a feature, not a bug.** The goal isn't reproducible minimal output; it's maximal faithful capture of what the text contains.

### Archival and Tooling

The 73 AGOT v1 extractions were moved to `extractions/archives/agot-v1/` to preserve them for comparison with v2 output. Schema evolution is itself interesting data — comparing what v1 captured vs. what v2 captures on the same chapter reveals both what was missing and what the extractor naturally prioritized.

A suite of shell tooling was built to support extraction at scale:

- **`scripts/run-extraction-wave.sh`** — takes a book code as its first argument, auto-discovers chapter files from the directory, and batches them into waves
- **`scripts/launch-extraction.sh`** — opens N iTerm2 tabs and distributes wave assignments automatically
- **`weirwood-mechanical` shell function** — convenience wrapper for launching extraction from anywhere in the terminal
- **Extraction runbook** at `working/runbooks/extraction-pass1.md` — step-by-step procedure for running a full book's extraction

The operational model: 4 iTerm2 terminals, each running Claude Code with the mechanical-extractor subagent, processing 5-chapter waves. This gives roughly 20 chapters in parallel, with each chapter taking a few minutes. A full book (73 chapters for AGOT) completes in about 4 waves.

### Housekeeping

- Added orchestration rules to CLAUDE.md: when modifying an agent prompt's schema, `reference/architecture.md` must be updated to match (these two must stay in sync)
- Added worklog archival rule: when the session log exceeds ~150 lines, older sessions get archived to `working/worklog-archives/`
- Archived Sessions 0-4 to `working/worklog-archives/archive001.md`
- Updated `working/todos.md` with items surfaced during the review: timeline reconstruction needs, direwolves/dragons tracking

## Key Decisions and Why

**Food and Hospitality as separate concerns.** Initially these seemed like one category — "food stuff." But they serve completely different functions in the text. Food descriptions are queryable data about GRRM's world-building (what do Dothraki eat? What's served at a Lannister feast vs. a Night's Watch meal?). Hospitality is a moral and narrative framework — guest right is a sacred law whose observance and violation drives major plot events. Merging them would lose the ability to query "every instance of guest right being invoked" vs. "every detailed meal description."

**Physical descriptions at cross-identity-matching granularity.** Matt specifically flagged the Jaqen H'ghar / Alchemist use case. In ACOK, Jaqen changes his face before leaving Arya. In AFFC, a character called "the Alchemist" appears with a specific physical description. The graph should be able to surface the connection: these descriptions match because they're the same person. This requires capturing physical details at a level of specificity that most extraction schemas would consider excessive — exact hair color, eye color, nose shape, build. It's not excessive for this project's goals.

**Spatial Layout as directed-graph edges.** The movement vocabulary (Advance, Ambush, Chase, etc.) creates typed edges between locations with characters attached. This means a chapter's spatial content becomes a mini graph that can be queried: "trace Arya's path through King's Landing in AGOT Arya 4" or "find every Ambush-type movement in ASOS." The graph structure here prefigures the main knowledge graph's edge types.

**Opus for extraction quality.** The mechanical extractor runs on Claude's most capable model. The cost is higher and the throughput is lower than Sonnet, but extraction quality is the foundation everything else builds on. Bad extractions propagate errors through every downstream pass. This is the wrong place to economize.

**Preserve v1 extractions.** Rather than deleting the v1 output, archiving it preserves the ability to compare schema versions on the same text. This is useful for validating that v2 actually captures more, and for understanding what the extractor naturally prioritizes vs. what it needs explicit schema guidance to notice.

**"Be expansive, never invent" over "leave empty if N/A."** The v1 philosophy produced minimal output because the extractor interpreted silence as permission to skip. The v2 philosophy sets the expectation that every section will have content for most chapters (GRRM's writing is dense enough that this is true), and that the extractor's job is to capture everything present rather than to judge what's important enough to include. Importance is a downstream concern — extraction should be maximalist.

## What Was Left Open

- **AGOT v2 extraction was launched but not yet complete.** The tooling was ready and the first waves were running by end of session.
- **V1 vs. v2 comparison not yet done.** Planned once v2 completes — pick a few chapters and compare side-by-side to validate the schema expansion actually produces richer output.
- **`reference/architecture.md` sync.** The new extraction schema sections needed to be reflected in architecture.md per the new sync rule. This was flagged but not completed in-session.
- **ACOK extraction.** Blocked on validating AGOT v2 output quality first. No point running a second book through a prompt that might need further tuning.
- **Timeline reconstruction.** The `time_markers` field enables timeline work, but the actual reconstruction (building a coherent chronology from scattered temporal references) is a future analytical pass, not a mechanical extraction concern.
