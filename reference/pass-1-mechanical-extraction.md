# Pass 1: Mechanical Extraction

> How we turn raw chapter text into structured, queryable inventories.

---

## What This Pass Does

Pass 1 reads a single ASOIAF chapter and produces a structured markdown file that catalogs every named entity, location, artifact, event, relationship, and piece of information revealed in that chapter — and *only* that chapter.

The output is deliberately boring. No interpretation, no thematic analysis, no "this foreshadows X." Just facts, organized into tables that later passes can build on.

Think of it as a court reporter's transcript: everything that happened, who was there, what they said, what the POV character was thinking — recorded without editorial judgment.

---

## Why It Matters

Every later pass in the pipeline depends on Pass 1 output:

- **Pass 3 (Voice Analysis)** reads all of a POV character's extractions to build voice profiles
- **Pass 4 (Foreshadowing)** scans extractions for details that connect to known future events
- **Pass 5 (Theory Extraction)** looks for textual evidence supporting or contradicting specific theories
- **Pass 6 (Discovery)** searches the full extraction corpus for patterns no one has flagged yet

If Pass 1 misses a detail, every downstream pass is blind to it. If Pass 1 editorializes, downstream passes inherit bias. The mechanical pass needs to be comprehensive and neutral.

---

## Key Design Rules

### Chapter Isolation

Each extraction treats its chapter as if no other chapters exist. The agent has broad ASOIAF knowledge but is forbidden from using it.

- No "as we saw in Bran I" or "this foreshadows the Red Wedding"
- No dramatic irony based on what the reader knows from other chapters
- The "Known To (Reader Only?)" column refers to what the reader learns *within this chapter*, not from the series at large

This keeps each extraction clean and self-contained. Cross-chapter connections are Pass 4's job.

### Confidence Tiers

Everything in a Pass 1 extraction is **Tier 1 (Verified Canon)** by default — it's extracted directly from the text. Only two exceptions need marking:

- `(inferred)` — the text strongly implies something but doesn't state it outright
- `(uncertain — verify)` — not sure if an entity appeared in a prior chapter

### Spoiler Gating

Every extraction carries a `first_available` field in its metadata (e.g., `AGOT Bran II`). This is the earliest point in the series where the information becomes available to the reader. The system uses this to filter content based on a user's spoiler ceiling.

### Comprehensiveness Over Elegance

GRRM hides Chekhov's guns in food descriptions, heraldry details, weather patterns, and architectural minutiae. The extractor logs everything: the number of skulls in a cellar, the color of a horse, the pattern on a sword hilt, the contents of a meal. Boring details in AGOT become load-bearing details in ADWD.

---

## Output Schema

Each extraction is a markdown file with the following sections:

### Chapter Metadata
```yaml
book: AGOT              # Which book
chapter_number: 1        # Overall chapter number in the book
pov_character: Bran      # Whose head we're in
pov_chapter_number: Bran I  # This character's Nth chapter
first_available: AGOT Bran I  # Spoiler gate anchor
location_primary: Winterfell  # Main setting
location_secondary: ...       # Other locations mentioned
approximate_timeline: ...     # Relative positioning (within this book only)
chapter_summary: ...          # 3-5 factual sentences
```

### Characters Present
Who is physically in the chapter. Each row captures:
- Role in the chapter (POV, antagonist, bystander, etc.)
- Whether this is their first appearance in the series
- Notable physical or contextual details

### Characters Referenced
Who is mentioned but not physically present. Captures:
- Context of the reference (memory, dialogue, rumor)
- Who references them

### Locations
Every named place, with:
- Its role in the chapter (primary setting, referenced, recalled)
- First appearance flag
- Physical description notes

### Artifacts & Objects of Significance
Named objects, weapons, books, letters — anything with narrative weight:
- Context of appearance
- Current holder or location

### Events & Actions
Numbered list of what happens, in order. Factual descriptions, not analysis.

### Information Revealed
What the reader learns in this chapter, tracked in a table with:
- How it's revealed (dialogue, internal thought, narration, letter)
- Which characters know it
- Whether it's reader-only knowledge (the POV character thinks it but doesn't say it)

### Dialogue of Note
Significant lines of dialogue, captured with:
- Speaker and listener
- Exact quote or close paraphrase
- Context

### POV Character's Internal State
The POV character's emotional state, preoccupations, key decisions, and self-deception flags (moments where what they think contradicts what they do, or where they rationalize).

### Relationships Observed
Character-to-character relationships evidenced in this chapter:
- What type of relationship (ally, antagonist, mentor, subordinate)
- What textual evidence supports it

### Unanswered Questions
Questions raised by the chapter that the chapter itself doesn't answer. These are hooks for later passes — mysteries, ambiguities, conspicuous omissions.

### Raw Entity List
A flat inventory of every named entity, grouped by type:
- Characters
- Locations
- Artifacts
- Houses/Factions

---

## How It Runs

### The Agent

The mechanical extractor is defined in `.claude/agents/mechanical-extractor.md`. It runs on Claude (currently Opus 4.6) with read/write access to the repository. Each invocation:

1. Reads `reference/architecture.md` for system conventions
2. Reads its own agent prompt for extraction rules and schema
3. Reads the source chapter file
4. Writes the extraction to `extractions/mechanical/{book}/{chapter}.extraction.md`

### Batch Execution

Chapters are processed in waves of 5 using `scripts/run-extraction-wave.sh`. Each wave runs 5 chapters sequentially (each chapter is a fresh Claude invocation with no shared context). Multiple waves can run in parallel across separate terminals.

```bash
# Run a single wave
./scripts/run-extraction-wave.sh 6

# Run 4 waves in parallel (4 terminals)
./scripts/run-extraction-wave.sh 10  # Terminal A
./scripts/run-extraction-wave.sh 11  # Terminal B
./scripts/run-extraction-wave.sh 12  # Terminal C
./scripts/run-extraction-wave.sh 13  # Terminal D
```

The script logs progress to `working/progress.md` and per-chapter stats (timing, token usage) to `working/extraction-stats.csv`.

### Current Status

| Book | Chapters | Status |
|------|----------|--------|
| AGOT | 73 | Complete (all 73 extracted) |
| ACOK | 70 | Not started |
| ASOS | 82 | Not started |
| AFFC | 46 | Not started |
| ADWD | 73 | Not started |

---

## Example Output

Here's a condensed look at the Prologue extraction to show what the output actually looks like:

**Characters Present:** Will (POV, former poacher, 4 years on the Wall), Ser Waymar Royce (18, youngest son of an ancient house, commander), Gared (50+, 40 years in the Watch), The Others (tall, gaunt, pale, crystal swords, shifting armor)

**Key Events:** Rangers track missing wildlings → bodies have vanished → Others emerge → single combat with Royce → his sword shatters against crystal blade → Others kill Royce → Will hides in tree → Royce reanimates with blue eyes → kills Will

**Artifacts:** Royce's longsword (castle-forged, shatters), Other's crystal blade (translucent, blue shimmer), double-bladed battle-axe (abandoned at camp), Royce's sable cloak, moleskin gloves (bloody on reanimated hands)

**Unanswered Questions:** What killed the wildlings? Where did the bodies go? What language do the Others speak? Why did one Other fight Royce alone while others watched?

Full extraction files are in `extractions/mechanical/agot/`.

---

## Contributing

If you want to help with extraction on remaining books, the process is:

1. You'll need chapter source files in `sources/chapters/{book}/` (not committed — contact Matt)
2. Run `./scripts/run-extraction-wave.sh <wave_number>` with `--dangerously-skip-permissions`
3. The script handles everything: reading the chapter, running the agent, writing the output, logging progress
4. Review a few extractions for quality — check that chapter isolation is maintained and no cross-chapter references leaked in
