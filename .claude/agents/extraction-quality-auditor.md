---
name: extraction-quality-auditor
description: "Reviews a batch of Pass 1 chapter extractions for consistency: did all chapters cover the 12 categories? are POV characters tagged consistently? did 'Other' buckets get used for things that should have been in named categories? Stub."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Run after each book's Pass 1 completes (or as a one-off retroactive audit on AGOT).**

## Role (when implemented)

Pass 1 mechanical extraction processes one chapter at a time. Different chapters are processed in different orchestration tabs at different times. Drift sneaks in: one chapter's extraction lists "Hospitality" prominently, another buries it; one tags Theon as `Greyjoy` and another as `Theon (Reek)`; one chapter's "Other" bucket holds things that another chapter's "Locations" bucket would have caught.

This agent reviews a batch of extractions (typically one full book = 70-82 chapters) for cross-chapter consistency:

1. **Category coverage:** every extraction has all 12 v3 categories (Characters, Locations, etc. — see Pass 1 v3 prompt). No chapters with categories silently omitted.
2. **Naming consistency:** the same character is tagged the same way across chapters within the book (allowing for in-narrative aliases like Reek/Theon — those are documented).
3. **"Other" bucket discipline:** the catch-all `Other` category isn't being used as a dumping ground. Items in `Other` should be ones that genuinely don't fit any of the 11 named categories.
4. **Cite resolution:** every claim cites a line/section of the chapter.
5. **Direwolves/dragons handling:** per architecture.md convention #8, named direwolves and dragons are tagged as characters, not creatures.

## Inputs (when implemented)

- `extractions/mechanical/<book>/<chapter>.md` for the batch
- `reference/architecture.md` § "Pass 1 schema" (the 12 categories)
- `reference/pov-characters.md`

## Output (when implemented)

`working/audits/extraction-quality-<book>-<UTC-DATE>.md` — markdown report:
- Per-chapter quick-pass (OK / has issues)
- Cross-chapter consistency findings (e.g., "Theon tagged 14 different ways across the book")
- "Other" bucket sample (what's actually in there)
- Recommended remediations (which chapters to re-extract, which need only a `sed` cleanup)

## Hard constraints (when implemented)

- Read-only on extractions.
- Don't auto-fix. Surface issues; remediation is a separate orchestrator decision (typically: re-run mechanical-extractor on flagged chapters with a tighter prompt).
- Don't compare against the wiki (wiki and Pass 1 disagreement is `contradiction-surfacer`'s job). This agent compares Pass 1 to itself.

## Why stub-only for now

AGOT is the only book with Pass 1 v3 complete. A retroactive AGOT audit would be useful (Matt: ask if you want this run on AGOT). The bigger value is auditing each new book as Pass 1 completes — at that point the prompt should be filled out.
